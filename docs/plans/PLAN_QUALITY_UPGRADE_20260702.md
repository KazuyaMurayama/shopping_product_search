# 調査網羅性・ハルシネーション対策・スキル拡張 実装計画

作成日: 2026-07-02
最終更新日: 2026-07-02

> **実行担当（agentic workers）へ:** 本計画は sp-writing-plans スキルに基づき Fable（計画担当）が作成した。
> 実行は Sonnet サブエージェント（E1〜E4・R1）がタスク単位で担当し、Fable がレビューする。
> ステップはチェックボックス（`- [ ]`）で管理する。
> **実行エージェントは git commit を行わないこと**（並列実行のため、コミットはオーケストレーター（Fable）が統合レビュー後に実施する。sp-writing-plans の「頻繁なコミット」原則からの意図的逸脱）。

**Goal:** 本リポの調査タスク全般に (1) 網羅性ゲート（観点マトリクス＋抜け漏れ監査）、(2) ハルシネーション3層防御（出典規律・独立レビューア・機械検証）、(3) スキル改善＋公開スキル導入 を組み込む。

**Architecture:** 既存の「ルール文書 → SessionStartフック注入 → エージェント → PostToolUse機械検証」という4層構造を踏襲し、比較レポート限定だった防御を「調査タスク全般」へ拡張する。新規ルールは `docs/rules-research.md` に集約し、CLAUDE.md からは参照のみ（肥大化防止）。

**Tech Stack:** Markdown（ルール・エージェント・スキル定義）/ Bash（フック）/ Python 3（リンター）/ Claude Code サブエージェント（sonnet）

---

## 背景（現状分析・Fable による）

| 領域 | 現状 | ギャップ |
|---|---|---|
| 網羅性 | 失敗パターン6＋ルールA＋§4.0/4.5 着手時ゲート（比較系限定） | 非比較の調査・リサーチ依頼には網羅性の仕組みが**皆無**。観点（評価軸・情報源・反証視点）の設計手順がない |
| ハルシネーション | 価格出典表＋`check_comparison_report.py`（comparison マーカー限定）、quality-rules.md の URL 実在確認 | research 系レポートは機械検証ゼロ。**独立レビューア不在**（作成者自身のセルフチェックのみ）。出典規律がルール文書に分散 |
| セルフチェック | §6.0/6.1、各エージェントのチェックリスト | 「チェックリストを読むだけでは守られない」ことが失敗パターン6再発で実証済み。機械検証・成果物ゲートへの落とし込みが不足 |
| スキル | sp-brainstorming / sp-writing-plans / sp-executing-plans / sp-verification-before-completion（superpowers 由来・汎用のまま） | リポ固有の検証コマンド・網羅性設計と未接続。公開スキルの導入検討は未実施 |

---

## ファイル構成（新規/変更の全体マップと担当）

| # | パス | 新規/変更 | 担当 |
|---|---|---|---|
| 1 | `docs/rules-research.md` | 新規 | E1 |
| 2 | `.claude/skills/coverage-planning/SKILL.md` | 新規 | E1 |
| 3 | `.claude/agents/coverage-critic.md` | 新規 | E1 |
| 4 | `.claude/agents/fact-check-reviewer.md` | 新規 | E2 |
| 5 | `scripts/check_research_report.py` | 新規 | E2 |
| 6 | `.claude/hooks/check_report.sh` | 変更 | E2 |
| 7 | `docs/rules-search-product.md` | 変更（ゲート4追加ほか） | E2 |
| 8 | `.claude/quality-rules.md` | 変更（ハルシネーション章） | E2 |
| 9 | `.claude/skills/sp-verification-before-completion/SKILL.md`、`.claude/agents/report-writer.md`、`.claude/commands/search-product.md`、`.claude/commands/generate-report.md` | 変更 | E2 |
| 10 | `reports/research_20260702_public_skills_v1.md` | 新規（調査報告） | R1 |
| 11 | `.claude/skills/sp-brainstorming/SKILL.md`、`.claude/skills/sp-writing-plans/SKILL.md`、`.claude/skills/sp-executing-plans/SKILL.md` | 変更 | E3 |
| 12 | `.claude/skills/<採用スキル>/SKILL.md`（最大3件） | 新規 | E3 |
| 13 | `CLAUDE.md`、`.claude/hooks/session_start_gate.sh`、`FILE_INDEX.md`、`file_index.md`、`tasks.md` | 変更（統合） | E4 |

**ファイル所有権は厳格に守る**（E1〜E4 は自分の担当ファイル以外を編集しない。並列実行時の衝突防止）。

実行順序: Wave 1 = R1・E1・E2（並列）→ Wave 2 = E3（R1 完了後）→ Wave 3 = E4（E1〜E3 完了後）→ 最終 = Fable レビュー・リンターテスト・コミット・push。

---

## Task 1: `docs/rules-research.md` 新規作成（調査タスク共通ルール）【E1】

**Files:** Create: `docs/rules-research.md`

- [ ] **Step 1: 下記の章立て・内容で作成する**（文体は `docs/rules-search-product.md` に合わせる。約 150〜250 行）

必須の章と内容（この骨子の全項目を含めること。文言は磨いてよいが項目の削除は不可）：

```markdown
# 調査・リサーチ共通ルール — 網羅性とハルシネーション対策

> 商品検索に限らず、本リポの **すべての調査・リサーチ・比較タスク** に適用する共通ルール。
> 商品検索固有の詳細は docs/rules-search-product.md を参照（本ファイルはその上位・共通層）。

## 1. 網羅性ゲート（着手時・必須）

### 1.1 観点マトリクスの作成（調査を始める前に必ず）
調査に着手する前に、以下の 6 軸で「調べるべき観点」を列挙した観点マトリクスを作成し、
ユーザーに提示する（比較系タスクのブランド地図はこのマトリクスの 1 行目に相当する）：
  1. 選択肢空間 — 直接候補（ブランド・製品・手段）／代替カテゴリ／「買わない・別解」の選択肢
  2. 評価軸 — 価格・性能・品質・安全性・利便性・維持費・リスク/副作用（依頼文にない軸も列挙して取捨を明示）
  3. ユーザー文脈 — 対象者・利用シーン・制約条件（依頼文から抽出し、不明点は仮定を明示）
  4. チャネル・情報源の多様性 — EC5媒体/公式/実店舗/中古、一次情報（製品ページ・メーカー）と
     二次情報（第三者比較記事 2 本以上・レビュー・公的機関/専門家）を必ず混在させる
  5. 時間軸 — 現行品か・後継/新モデルの有無・季節性・情報の鮮度（古いキャッシュ問題）
  6. 反証視点 — デメリット・非推奨情報・リコール・偽レビュー・「この結論を覆す情報は何か」

### 1.2 検索クエリの多様化（単一クエリ族での打ち切り禁止）
  - 同義語・言い換え・英語/日本語・カテゴリ名・競合名で最低 3 系統のクエリを使う
  - 「◯◯ 比較」「◯◯ おすすめ」「◯◯ 一覧」「◯◯ デメリット」「◯◯ 欠点」を系統に含める
  - 最初の数件で「わかった気」にならず、新情報が 2 クエリ連続で出なくなるまで広げる（飽和判定）

### 1.3 抜け漏れ監査（coverage-critic）
  - 本調査に入る前に、観点マトリクス（比較系ではブランド地図も）を coverage-critic
    サブエージェントに渡し、抜け漏れ監査を受ける
  - 指摘（重大）が 1 件でもあれば観点マトリクスを補強してから本調査に入る
  - 監査結果（指摘と対応）はレポートの「調査範囲」節に要約を残す

### 1.4 調査範囲の明示（レポート必須要素）
  - レポートに「調査した範囲」と「調査しなかった範囲（理由つき）」を必ず書く
  - 「調べていないのに調べたように見える」レポートを作らない（網羅性の偽装禁止）

## 2. ハルシネーション対策（出典規律）

### 2.1 事実主張の3分類とラベル
  - 【引用】原文ママ＋ソース URL 必須（`>` ブロック）
  - 【要約】（出典: URL）必須。ソースにない属性・数値の追加禁止
  - 【推定】「と考えられる」等のヘッジ語＋⚠️ 必須。出典なしの断定は禁止
  - 数値（価格・%・件数・容量・成分量）は必ず出典 URL＋確認日とセット。
    出典を示せない数値は推定に格下げするか削除する

### 2.2 「知識」でなく「取得した情報」で書く
  - モデルの記憶にある商品名・型番・価格・URL をそのまま書かない（実在しない型番の捏造が
    ハルシネーションの典型）。必ず WebSearch/WebFetch で当該情報を取得してから書く
  - URL は取得した実 URL のみ。記憶から組み立てた URL は禁止
  - 確認できなかったことは「確認できなかった」と書く（埋めない勇気）

### 2.3 research レポートの機械検証
  - 調査・リサーチ系レポートには先頭に `<!-- report-type: research -->` を付ける
  - scripts/check_research_report.py が保存時に自動検証する（出典節・リンク本数・確認日・
    H1 メタデータ・禁止 URL）。違反は差し戻し

## 3. レビューゲート（ゲート4・レポート単位の独立検証）

  - レポート（比較・検索・リサーチとも）を確定・納品する前に、fact-check-reviewer
    サブエージェントによる独立検証を必ず通す
  - レビューアは作成に関与していない新しいコンテキストで、主張の抽出→出典との突合→
    ライブ検証（可能なチャネルのみ）を行い、✅/⚠️/❌ の判定表を返す
  - ❌ が 1 件でもあれば修正して再レビュー。⚠️ は本文に ⚠️ 表記を反映してから納品
  - レビュー実施の記録（実施日・指摘件数・対応）をレポート末尾の「検証記録」節に 3 行以内で記す

## 4. セルフチェック（作成者自身・レビュー前）

  - [ ] 観点マトリクスを作成し提示したか（着手時）
  - [ ] coverage-critic の監査を受けたか（着手時）
  - [ ] 数値・引用のすべてに出典 URL＋確認日があるか
  - [ ] 記憶ベースの URL・型番・価格を 1 つも書いていないか
  - [ ] 未確認事項を ⚠️/「確認できなかった」と明示したか
  - [ ] 「調査しなかった範囲」を明記したか
  - [ ] `<!-- report-type: ... -->` マーカーを付けたか（research / comparison）
  - [ ] fact-check-reviewer のレビューを通したか（ゲート4）
```

- [ ] **Step 2: 検証** — `python3 -c` 等は不要。以下を目視確認：全 4 章が存在／既存 `docs/rules-search-product.md` と矛盾する記述がない（ゲート1〜3 の定義は再掲せず参照に留める）／ファイル名が命名ルールの対象外（docs 配下のルール文書のため日付サフィックス不要、`rules-search-product.md` と同形式）

## Task 2: `.claude/skills/coverage-planning/SKILL.md` 新規作成【E1】

**Files:** Create: `.claude/skills/coverage-planning/SKILL.md`

- [ ] **Step 1: 作成**。frontmatter は既存スキル（sp-brainstorming）に倣い `name: coverage-planning` / `description:`（トリガー明記: 「調査・リサーチ・商品検索・比較タスクの着手時に必ず使用。観点マトリクスを作成し coverage-critic の監査を受けるまで本調査に入らない」）。本文は **手順スキル** として：
  1. 依頼文から「問い」と必須条件を抽出（不明点は仮定を明示）
  2. `docs/rules-research.md` §1.1 の 6 軸で観点マトリクスを作成（Markdown 表。各軸 3 項目以上、埋まらない軸は「該当なし＋理由」）
  3. 比較・ランキング系ならブランド地図（rules-search-product.md §4.5 ステップ1）もここで作成
  4. coverage-critic サブエージェントに監査を依頼（渡すもの: 依頼原文＋マトリクス＋ブランド地図）
  5. 重大指摘ゼロになるまで補強（最大 2 巡。2 巡で収束しない場合は残課題を明示して進む）
  6. 成果物（マトリクス＋監査結果サマリ）をユーザーに提示してから本調査に入る
  - 「アンチパターン」節：最初に思いついた 3 ブランドだけ調べる／評価軸を価格だけにする／肯定情報だけ集める（反証視点の欠落）／1 系統のクエリで打ち切る
- [ ] **Step 2: 検証** — frontmatter が既存スキルと同形式か、docs/rules-research.md への参照パスが正しいか目視確認

## Task 3: `.claude/agents/coverage-critic.md` 新規作成【E1】

**Files:** Create: `.claude/agents/coverage-critic.md`

- [ ] **Step 1: 作成**。frontmatter: `name: coverage-critic` / `description: 調査着手前の観点マトリクス・ブランド地図の抜け漏れ監査を担当。悪魔の代弁者として「何が欠けているか」だけを指摘する。` / `tools: WebSearch, WebFetch, Read, Write` / `model: sonnet`。本文の必須要素：
  - 役割: 入力（依頼原文・観点マトリクス・ブランド地図）に対し、**追加すべき観点・ブランド・情報源・反証視点** を挙げる。調査の実行はしない
  - 動作: 独自に `"カテゴリ名 比較"` `"カテゴリ名 メーカー 一覧"` `"カテゴリ名 デメリット"` で最低 3 回 WebSearch し、マトリクスに無い候補・観点を突き合わせる
  - 出力形式（プレーンテキスト）: 指摘ごとに `[重大/中/軽] 欠けている観点/ブランド / 根拠(検索で見つけた情報源) / 推奨追加クエリ` ＋ 最後に `判定: 承認 / 差し戻し（重大指摘 N 件）`
  - 判定ルール: 主要ブランドの欠落・評価軸の重大な欠落・反証視点ゼロ は「重大」= 差し戻し
  - 自己チェック: 指摘に根拠 URL を添えたか／「もっと調べろ」だけの空虚な指摘をしていないか
- [ ] **Step 2: 検証** — 既存エージェント（condition-checker.md）と frontmatter 形式が揃っているか確認

## Task 4: `.claude/agents/fact-check-reviewer.md` 新規作成【E2】

**Files:** Create: `.claude/agents/fact-check-reviewer.md`

- [ ] **Step 1: 作成**。frontmatter: `name: fact-check-reviewer` / `description: ゲート4（レポート単位の独立ファクトチェック）を担当。レポート草稿から検証可能な主張を抽出し、出典との突合・ライブ再検証を行い ✅/⚠️/❌ 判定表を返す。❌が1件でもあれば差し戻し。` / `tools: WebSearch, WebFetch, Read, Write` / `model: sonnet`。本文の必須要素：
  - 入力: レポート草稿のファイルパス（Read で読む）＋ユーザーの依頼原文
  - 検証対象の抽出: URL（全件）／価格・数値（全件）／商品の実在・在庫主張（TOP 候補は全件、他はサンプリング可）／引用文
  - 検証方法（環境制約を明記）: Yahoo!ショッピングはライブ取得可・Amazon(/dp/) は 503・楽天はボット遮断のため、Amazon/楽天は kakaku.com 等の集約サイト＋検索スニペット日付でクロスチェック。サクラチェッカーは WebFetch 可
  - URL 検証: 禁止パターン（`/s?k=` `search.rakuten` `/search/` `?keyword=` `?kw=` `?q=`）を含まないか＋WebFetch/検索で実在確認
  - 判定表（プレーンテキスト）: `主張 | 出典 | 検証方法 | 結果(✅/⚠️/❌) | 備考`
  - 総合判定: `承認` / `条件付き承認（⚠️ N 件を本文に反映せよ）` / `差し戻し（❌ N 件）`
  - 心得: **作成者の主張を信じない**。出典に書いていないことがレポートに書かれていたら ❌（ハルシネーションの定義）。検証できない主張は ⚠️
  - 自己チェック: TOP 候補の価格・在庫・URL を全件検証したか／判定に根拠を添えたか
- [ ] **Step 2: 検証** — frontmatter 形式確認

## Task 5: `scripts/check_research_report.py` 新規作成【E2】

**Files:** Create: `scripts/check_research_report.py`

- [ ] **Step 1: 下記コードで作成する**（このまま使用してよい）

```python
#!/usr/bin/env python3
"""
リサーチ系レポートの機械検証リンター（ハルシネーション対策・出典規律）。

対象の判定:
  ファイル先頭 2000 字に `<!-- report-type: research -->` を含むレポートのみ検証する。
  `<!-- report-type: comparison -->` は check_comparison_report.py の担当なので SKIP。
  マーカーが無いファイルも SKIP（exit 0）。

検証項目:
  R1: 禁止 URL パターン（検索結果 URL・失敗パターン1）
  R2: H1 直下メタデータ（作成日/最終更新日 YYYY-MM-DD）
  R3: 出典セクション（## 出典 / 参考文献 / 情報源）の存在
  R4: Markdown リンク [text](http...) が 5 本以上（主要な事実に出典リンク必須）
  R5: 確認日 `（確認: YYYY-MM-DD）` / `取得: YYYY-MM-DD` が本文に 1 つ以上

使い方:
  python3 scripts/check_research_report.py <report.md>
  exit 0 = 合格または対象外 / exit 1 = 違反あり（標準エラーに理由を出力）
"""
import sys
import re

FORBIDDEN_URL = ["/s?k=", "search.rakuten", "/search/", "?keyword=", "?kw=", "?q=", "&k=", "?k="]
MIN_LINKS = 5


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: check_research_report.py <report.md>\n")
        sys.exit(1)
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        sys.stderr.write(f"読み込み不可: {e}\n")
        sys.exit(1)

    head = text[:2000]
    if "<!-- report-type: comparison -->" in head:
        sys.exit(0)  # 比較レポートは check_comparison_report.py が担当
    if "<!-- report-type: research -->" not in head:
        sys.exit(0)  # マーカーなしは対象外

    errors = []

    # R1: 禁止 URL パターン
    for pat in FORBIDDEN_URL:
        if pat in text:
            errors.append(f"[禁止URL] 検索結果URLパターン '{pat}' を検出（失敗パターン1）")

    # R2: H1 直下メタデータ
    if not re.search(r"作成日[:：]\s*\d{4}-\d{2}-\d{2}", text):
        errors.append("[メタデータ] '作成日: YYYY-MM-DD' が無い（CLAUDE.md §8）")
    if not re.search(r"最終更新日[:：]\s*\d{4}-\d{2}-\d{2}", text):
        errors.append("[メタデータ] '最終更新日: YYYY-MM-DD' が無い（CLAUDE.md §8）")

    # R3: 出典セクション
    if not re.search(r"^#{2,3}\s*(出典|参考文献|情報源|検証記録)", text, re.M):
        errors.append("[出典] '## 出典'（または参考文献/情報源）節が無い（ハルシネーション対策・docs/rules-research.md §2）")

    # R4: リンク本数
    links = re.findall(r"\[[^\]]+\]\(https?://[^)\s]+\)", text)
    if len(links) < MIN_LINKS:
        errors.append(
            f"[出典] Markdownリンクが {len(links)} 本で下限 {MIN_LINKS} 未満。"
            "主要な事実・数値に出典リンクを付けること")

    # R5: 確認日
    if not re.search(r"(確認|取得)[:：]\s*\d{4}-\d{2}-\d{2}", text):
        errors.append("[確認日] '（確認: YYYY-MM-DD）' 形式の確認日が本文に 1 つも無い（quality-rules.md）")

    if errors:
        sys.stderr.write(f"=== リサーチレポート機械検証 NG: {path} ===\n検出 {len(errors)} 件:\n")
        sys.stderr.write("\n".join(f"  - {e}" for e in errors) + "\n")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 不合格ケースのテスト** — スクラッチパッドに `<!-- report-type: research -->` だけのダミー md を作り実行し、exit 1 と R2〜R5 の違反 4 件超が出ることを確認：
  `python3 scripts/check_research_report.py /tmp/.../bad.md; echo $?` → `1`
- [ ] **Step 3: 合格ケースのテスト** — メタデータ・出典節・リンク5本・確認日を備えたダミー md で exit 0 を確認
- [ ] **Step 4: 対象外ケースのテスト** — マーカー無し md で exit 0 を確認

## Task 6: `.claude/hooks/check_report.sh` 更新（両リンター実行）【E2】

**Files:** Modify: `.claude/hooks/check_report.sh`

- [ ] **Step 1: 全体を下記に置き換える**

```bash
#!/usr/bin/env bash
# PostToolUse フック: Write/Edit で reports/*.md が保存されたらレポートリンター群を実行する。
# 違反があれば exit 2 で stderr を Claude に返し、修正を促す（機械的強制）。
# 入力: stdin に PostToolUse の JSON（tool_input.file_path を含む）
set -euo pipefail

input="$(cat)"
file_path="$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.path // empty')"

# reports 配下の .md 以外は対象外
case "$file_path" in
  *reports/*.md) ;;
  *) exit 0 ;;
esac

[ -f "$file_path" ] || exit 0

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

fail=0
out_all=""
for name in check_comparison_report.py check_research_report.py; do
  linter="$repo_root/scripts/$name"
  [ -f "$linter" ] || continue
  if ! out="$(python3 "$linter" "$file_path" 2>&1)"; then
    fail=1
    out_all="${out_all}${out}
"
  fi
done

if [ "$fail" -ne 0 ]; then
  {
    echo "レポートの機械検証で違反を検出しました。修正してから完了してください。"
    printf '%s' "$out_all"
  } >&2
  exit 2
fi
exit 0
```

- [ ] **Step 2: 検証** — `bash -n .claude/hooks/check_report.sh`（構文 OK）＋ 手動疑似実行：
  `echo '{"tool_input":{"file_path":"<bad.mdのパス>"}}' | bash .claude/hooks/check_report.sh; echo $?` → reports 外なので 0。reports 配下にコピーした bad ファイルで 2 になることを確認（確認後にテストファイルは削除）

## Task 7: `docs/rules-search-product.md` へゲート4等を追記【E2】

**Files:** Modify: `docs/rules-search-product.md`

- [ ] **Step 1: §2 の末尾（ゲート3 の後・§3 の前）に追記**

```markdown
ゲート 4：独立ファクトチェックレビュー（レポート単位・納品前必須）

- ゲート 1〜3 は候補単位、ゲート 4 は **レポート単位** の最終検証
- レポート草稿の完成後、`fact-check-reviewer` サブエージェントに草稿パスと依頼原文を渡し、
  独立コンテキストで検証させる（作成者自身のセルフチェックでは代替不可）
- ❌ が 1 件でもあれば修正して再レビュー。⚠️ は本文に ⚠️ 表記を反映してから納品
- レビュー実施の記録（実施日・指摘件数・対応）をレポート末尾「検証記録」節に残す
- 共通ルールの詳細は `docs/rules-research.md` §3 を参照
```

- [ ] **Step 2: §4.5 のワークフロー末尾に `ステップ 5【レビューゲート】fact-check-reviewer による独立検証（ゲート 4）を通過後に納品` を追加。§4.1 の手順 5〜7 の後にも同趣旨の手順 8 を追加**
- [ ] **Step 3: §6.1 チェックリスト末尾に追記**：
  - `**fact-check-reviewer（ゲート 4）のレビューを通し、「検証記録」節を書いたか**`
  - `**観点マトリクス（docs/rules-research.md §1）を着手時に作成・提示したか**`
  - `**記憶ベースの URL・型番・価格を書いていないか（取得した実データのみか）**`
- [ ] **Step 4: 検証** — 追記後に既存の章番号・相互参照が壊れていないか目視確認

## Task 8: `.claude/quality-rules.md` 増強【E2】

**Files:** Modify: `.claude/quality-rules.md`

- [ ] **Step 1: 末尾に「ルール3: ハルシネーション対策（3層防御）」章を追加**。内容：
  - 第1層＝作成時の出典規律（rules-research.md §2 参照。数値・引用は出典＋確認日、記憶ベース URL/型番禁止、不確実は ⚠️＋ヘッジ語、「確認できなかった」と書く勇気）
  - 第2層＝独立レビュー（fact-check-reviewer・ゲート4。作成者と別コンテキストで検証）
  - 第3層＝機械検証（check_comparison_report.py / check_research_report.py・PostToolUse フック）
  - ハルシネーション典型4類型と対策対応表: 実在しない商品/型番の捏造→2.2 取得情報のみ／誤価格→価格出典表＋ライブ検証／誤属性（ソースにない仕様の付加）→引用/要約/推定ラベル／リンク切れ・偽URL→URL実在確認＋禁止パターン検査
- [ ] **Step 2: 検証** — 既存ルール1・2 と番号が連続し、矛盾がないこと（ルール1 のブランチ規則は変更しない）

## Task 9: 検証スキル・エージェント・コマンドへの組み込み【E2】

**Files:** Modify: `.claude/skills/sp-verification-before-completion/SKILL.md`, `.claude/agents/report-writer.md`, `.claude/commands/search-product.md`, `.claude/commands/generate-report.md`

- [ ] **Step 1: sp-verification-before-completion/SKILL.md の末尾にリポ固有節を追加**

```markdown
## This Repository's Verification Commands（本リポ固有・必須）

レポート・調査成果物の完了を主張する前に、以下を実際に実行して出力を確認する:

| Claim | Verification |
|-------|--------------|
| 比較レポート完成 | `python3 scripts/check_comparison_report.py reports/<file>.md` → exit 0 |
| リサーチレポート完成 | `python3 scripts/check_research_report.py reports/<file>.md` → exit 0 |
| レビュー済み | fact-check-reviewer の判定が「承認」であるログ／「検証記録」節の存在 |
| URL 有効 | 全リンクに禁止パターンなし＋主要 URL の WebFetch/検索での実在確認 |
| push 完了 | `git log origin/<branch> -1` に当該コミットが存在 |
| 成果物リンク有効 | GitHub API（contents API, ref=実ブランチ）で 200 を確認してから報告 |
```

- [ ] **Step 2: report-writer.md の自己チェックに 3 行追記**： `- [ ] 数値・引用に出典（URL または情報源名）を添えたか` ／ `- [ ] 記憶ベースの URL・型番を書いていないか（スカウト出力にある実データのみか）` ／ `- [ ] このレポートはゲート 4（fact-check-reviewer）のレビュー対象であることをオーケストレーターに伝えたか`
- [ ] **Step 3: search-product.md に「フェーズ 4.5: レビューゲート（ゲート 4）」を追加**（フェーズ 4 と 5 の間）：「report-writer の出力後、fact-check-reviewer サブエージェントで独立検証。❌ があれば修正して再レビュー。承認後にのみユーザーへ納品」。フェーズ 1 の直後に「フェーズ 1.5: 観点マトリクス（coverage-planning スキル・比較系はブランド地図）」も追加
- [ ] **Step 4: generate-report.md の手順末尾に 1 行追加**：「保存前に fact-check-reviewer（ゲート 4）の承認を得ること」
- [ ] **Step 5: 検証** — 4 ファイルの追記が既存書式（見出しレベル・チェックボックス形式）と揃っているか目視確認

## Task 10: 公開スキル・ベストプラクティス調査【R1・Web 調査】

**Files:** Create: `reports/research_20260702_public_skills_v1.md`

- [ ] **Step 1: WebSearch/WebFetch で以下を調査**（GitHub MCP ツールは本リポ以外に使用禁止。公開ページの閲覧は WebFetch で行う）：
  1. Anthropic 公式スキル（github.com/anthropics/skills ほか公式ドキュメント）— 特に skill-creator 等のメタスキル
  2. obra/superpowers の現行スキル一覧 — 本リポ未導入で有効なもの（例: dispatching-parallel-agents, requesting-code-review, systematic-debugging 等の現況・内容）
  3. コミュニティのスキル集（awesome-claude-code / awesome-claude-skills 等）から、リサーチ・ファクトチェック・検証系スキル
  4. LLM リサーチ/検索エージェントのハルシネーション対策ベストプラクティス（出典グラウンディング・検証エージェント・claim extraction 等、2025〜2026 の情報）
- [ ] **Step 2: レポート作成**。要件：
  - 先頭に `<!-- report-type: research -->`、H1 直下に `作成日: 2026-07-02` `最終更新日: 2026-07-02`
  - 候補スキル一覧表（名称/提供元/ライセンス/概要/本リポとの関連度 高中低/導入判断案）
  - ベストプラクティス章（本リポの既存仕組みとの対応・ギャップ）
  - `## 出典` 節（全参照 URL＋`（確認: 2026-07-02）`）、リンクは Markdown 形式のみ
  - **導入推奨 TOP3（理由つき）** と見送り理由リスト（網羅性ルールの適用: 見送りも全件明記）
- [ ] **Step 3: 検証** — `python3 scripts/check_research_report.py reports/research_20260702_public_skills_v1.md` が存在すれば exit 0 を確認（未作成なら R1 は要件を目視確認）

## Task 11: 既存 sp-* スキルの改善【E3】

**Files:** Modify: `.claude/skills/sp-brainstorming/SKILL.md`, `.claude/skills/sp-writing-plans/SKILL.md`, `.claude/skills/sp-executing-plans/SKILL.md`

- [ ] **Step 1: 各スキルを読み、以下の「本リポ適用（This Repository）」節を末尾に追加**：
  - sp-brainstorming: 「調査・比較系の依頼では、ブレインストーミングの一部として観点マトリクス（docs/rules-research.md §1.1 の 6 軸）を作成し、coverage-critic の監査を受けてから設計を確定する」
  - sp-writing-plans: 「計画の保存先は本リポでは `docs/plans/<TOPIC>_YYYYMMDD.md`（CLAUDE.md §8 命名）。調査系計画には観点マトリクスを含め、納品前タスクとしてゲート 4（fact-check-reviewer）を必ず計画に入れる」
  - sp-executing-plans: 「各タスク完了時の verification には Task 9 の本リポ固有検証コマンド表（sp-verification-before-completion 参照）を用いる。レポート系タスクはリンター exit 0 とゲート 4 承認が完了条件」
- [ ] **Step 2: 検証** — 追記が原文の構造（英語スキルなら英語見出しでも可・日本語でも可）を壊していないか確認

## Task 12: 公開スキルの導入（最大 3 件）【E3・R1 完了後】

**Files:** Create: `.claude/skills/<採用スキル名>/SKILL.md`（最大 3 ディレクトリ）

- [ ] **Step 1: R1 レポートの導入推奨 TOP3 を読み、採用判断**。採用基準：(a) 本リポの調査・検証・網羅性ワークフローに直結する／(b) ライセンス上再配布・改変可（MIT 等。不明なら URL 参照＋自作リライトで対応）／(c) 既存スキルと重複しない
- [ ] **Step 2: 採用スキルを `.claude/skills/<name>/SKILL.md` として作成**。原文コピペではなく本リポ向けに適合（チャネル・ルールファイル参照を織り込む）。ファイル冒頭コメントに出典 URL・原作者・ライセンスを明記
- [ ] **Step 3: 採用・見送りの結論を R1 レポートの「導入結果」節に追記**（最終更新日を当日に）
- [ ] **Step 4: 検証** — 新スキルの frontmatter 形式・参照パスの実在を確認

## Task 13: 統合更新（CLAUDE.md・セッションゲート・索引）【E4・E1〜E3 完了後】

**Files:** Modify: `CLAUDE.md`, `.claude/hooks/session_start_gate.sh`, `FILE_INDEX.md`, `file_index.md`, `tasks.md`

- [ ] **Step 1: session_start_gate.sh の EOF 直前に追記**（簡潔に。注入コンテキスト肥大防止のため 8 行以内）

```
■ 全ての調査・リサーチ・検索タスク共通（網羅性ゲート・docs/rules-research.md）:
  - 着手前に観点マトリクス（6軸: 選択肢空間/評価軸/ユーザー文脈/チャネル・情報源/時間軸/反証視点）を
    作成・提示し、coverage-critic サブエージェントの抜け漏れ監査を受けてから本調査に入る
■ ハルシネーション3原則: ①数値・引用は出典URL+確認日必須（記憶ベースのURL・型番・価格は禁止）
  ②未検証・推定は⚠️+ヘッジ語 ③納品前に fact-check-reviewer の独立レビュー（ゲート4）を必ず通す
  リサーチ系レポートは <!-- report-type: research --> を付与（check_research_report.py が機械検証）
```

- [ ] **Step 2: CLAUDE.md 更新**（最小限のポインタ追加のみ・肥大化させない）：
  - §2 エージェント表に `coverage-critic`（調査観点の抜け漏れ監査）と `fact-check-reviewer`（ゲート4・独立ファクトチェック）の 2 行追加
  - §2 ドキュメント一覧を `channels.md` / `rules-search-product.md` / `used-market-rules.md` / `rules-research.md` に更新
  - §10 スキル表に「調査・検索・比較の着手時（網羅性設計）→ `.claude/skills/coverage-planning/SKILL.md`」と E3 採用スキルの行を追加
  - §3.1 の要点の後に 1 行: 「全調査タスク共通の網羅性・ハルシネーション対策は `docs/rules-research.md` を参照（着手時: 観点マトリクス＋coverage-critic ／ 納品前: fact-check-reviewer＝ゲート4）」
- [ ] **Step 3: FILE_INDEX.md / file_index.md に新規ファイルを追記・更新日更新**（ディレクトリツリーと一覧。SHA/サイズは `git ls-files -s` と `wc -c` で実値取得）
- [ ] **Step 4: tasks.md 更新** — 完了済みに本タスクを 1 エントリ追加（成果物列挙）。バックログに「ゲート4 運用の実効性レビュー（初回運用 3 件後）」を追加
- [ ] **Step 5: 検証** — `bash -n .claude/hooks/session_start_gate.sh` ＋ CLAUDE.md の表が壊れていないか目視確認

## Task 14: 統合レビュー・テスト・コミット・push【オーケストレーター（Fable）】

- [ ] **Step 1: 全差分レビュー**（`git diff` / `git status`）— ファイル所有権違反・矛盾・プレースホルダ残りがないか。問題は担当エージェント（SendMessage）または直接修正で解消
- [ ] **Step 2: リンターテスト再実行** — Task 5 Step 2〜4 の 3 ケース＋ `bash -n` 2 本＋ R1 レポートへの実リンター適用で exit 0
- [ ] **Step 3: コミット**（論理単位で 2〜3 コミット: 網羅性／ハルシネーション対策／スキル・統合）
- [ ] **Step 4: push** — `git push -u origin claude/repo-investigation-coverage-bie54i`（失敗時 2s/4s/8s/16s リトライ）
- [ ] **Step 5: 成果物 URL 検証** — GitHub contents API（ref=実ブランチ）で全成果物 200 確認後、3 列表で報告

---

## 受け入れ基準（全体）

1. 新規 6 ファイル＋変更 12 ファイルが上記仕様どおり存在し、相互参照パスがすべて実在する
2. `check_research_report.py` が合格/不合格/対象外の 3 ケースで正しい exit code を返す
3. R1 調査レポートが自ら research マーカー付きでリンター合格している（ドッグフーディング）
4. CLAUDE.md・session_start_gate.sh から新ルール・新エージェント・新スキルに到達可能
5. 既存ルール（ゲート1〜3・ルールA〜D・価格出典表）と矛盾する記述がない

## Self-Review（sp-writing-plans 準拠・Fable 実施済み）

- 依頼 3 項目との対応: 網羅性→Task 1-3,13 ／ ハルシネーション (a)→Task 1§2,8 (b)→Task 4,7,9 (c)→Task 5,6,9,13 ／ スキル (a)→Task 9,11 (b)→Task 10,12 — 欠落なし
- プレースホルダ: コード系（Task 5,6）は完全コード掲載。文書系は骨子＋必須項目を明記（執筆はSonnet担当・受け入れ基準で担保）
- 参照整合: coverage-critic / fact-check-reviewer / rules-research.md / check_research_report.py の名称はタスク間で一致確認済み
