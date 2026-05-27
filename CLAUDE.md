# CLAUDE.md — リポジトリ運用ガイド

このリポジトリは AI エージェントによる調査・商品検索・レポート生成を行う定義集です。
Claude Code は本ファイルの規約を**必ず**遵守してください。

---

## 1. 回答フォーマット

- 回答は**日本語**で行う
- コードブロック・表・箇条書きを積極活用し、視認性を高める
- 長い回答は見出し（`##`）でセクション分割する
- 推測での回答は禁止。不明点は作業前に質問する

---

## 2. タスク管理（tasks.md）

- `tasks.md` を常に最新に保つ。新しいタスクが発生したら即座に追記する
- ステータスは以下 3 種類のみ：
  - `[ ]` 未着手
  - `[~]` 進行中
  - `[x]` 完了
- タスク完了時は `[x]` に更新してからコミットする
- タスク追加・更新は単独コミットにせず、作業コミットに含める

---

## 3. ファイルインデックス（file_index.md）

- `file_index.md` を常に最新に保つ
- 新しいファイルを作成したら即座に追記する
- 各エントリは以下の形式：
  ```
  | パス | 説明 | 最終更新 | 優先度 |
  ```
- 優先度：`高` / `中` / `低`
- ファイルを削除した場合も即座にインデックスから除去する

---

## 4. モデル使用方針

- **計画・分析・設計フェーズ**：Claude Opus（最高品質が必要な判断）
- **実行・コーディング・サブエージェント**：Claude Sonnet（速度と品質のバランス）
- ユーザーから明示的な指定がある場合はそれを優先する

---

## 5. Git ルール（厳守）

- **新しいブランチを作成しない**（ユーザーから明示的な指示がある場合を除く）
- 常に現在のブランチ（`main`）で作業する
- コミットメッセージは日本語または英語、内容を端的に表すものにする
- プッシュは `git push -u origin <branch>` を使用する
- プッシュ失敗時は指数バックオフ（2s → 4s → 8s → 16s）で最大 4 回リトライする
- **PR は明示的に指示された場合のみ作成する**

---

## 6. GitHub ハイパーリンク必須ルール

レポートをユーザーに納品する際は、必ず GitHub リポジトリ上の
該当ファイル URL をハイパーリンク（ワンクリックで開ける形）で提示する。

- ベース URL：`https://github.com/KazuyaMurayama/shopping_product_search/blob/main/[PATH]`
- チャット（Markdown 許容）では `[表示名](URL)` 形式でハイパーリンク化
- プレーンテキストレポート本文には生 URL をそのまま記載（Markdown 禁止）
- 同時に提示すべきリンク（最低 3 つ）：
  1. 今回のレポートファイル
  2. `reports/index.txt`（履歴インデックス）
  3. `reports/` ディレクトリ（`tree` パスで組む）

---

## 7. 商品検索タスク

商品検索を行う場合は、詳細ルールを必ず参照する：

- **検索ルール詳細**：`docs/rules-search-product.md`
- **チャネル仕様**：`docs/channels.md`
- **中古市場ルール**：`docs/used-market-rules.md`
- **エージェント定義**：`.claude/agents/*-scout.md`

### 商品検索の要点（詳細は上記ファイル参照）

- 検索結果ページ URL は絶対に掲載しない（個別商品 URL のみ）
- 候補は 3 ゲート検証（URL検証 → 存在・在庫検証 → 条件充足検証）を必ず通過させる
- 価格は必須出力項目（数値がなければ TOP3 除外）
- レポートはプレーンテキスト形式で `reports/search_YYYYMMDD_HHMM.txt` に保存

---

## 8. スラッシュコマンド

| コマンド | 機能 |
|---|---|
| `/add-channel` | 新チャネル追加の雛形を生成 |

---

## 9. ファイル構成

```
/
├── CLAUDE.md             # このファイル（軽量コア）
├── tasks.md              # タスク管理
├── file_index.md         # ファイルインデックス
├── docs/
│   ├── rules-search-product.md  # 商品検索詳細ルール
│   ├── channels.md               # チャネル仕様
│   └── used-market-rules.md      # 中古市場ルール
├── reports/              # レポート出力先
└── .claude/
    └── agents/           # エージェント定義
```

## 開発者情報・命名ルール

このリポジトリの開発者・所有者は **男座員也（Kazuya Oza / おざ かずや）** です。

- ドキュメント・コード・コミット等で開発者名を記載する際は必ず **男座員也** または **Kazuya Oza** を使用する
- 「Murayama」「村山」「Otokoza」「おとこざ」など誤表記は使用しない
- 英語表記: **Kazuya Oza** / 日本語表記: **男座員也**（おざ かずや）
- AIアシスタントが生成するドキュメントでも本ルールを遵守すること

### 開発者の作業環境
- **OS:** Windows 11（Macではない）。シェルは PowerShell 5.1 / Bash（WSL/Git Bash）。`brew` / `Cmd+` / Mac専用コマンドは使用不可。パッケージ管理は `winget` / `scoop`。
- **スマートフォン:** iPhone（iOS）。Android固有の手順・adb・Play Store等は不要。
- コマンド例はPowerShell構文（`;` 連結、`$env:VAR`）で提示。macOS専用ツールを回答に含めない。


## 🚀 自動実行ポリシー

### 確認不要で即実行する操作
- 全ファイル操作（作成・編集・削除）
- 全シェルコマンド（PowerShell, Bash, git, gh, npm, node, python）
- Git操作: add / commit / push（featureブランチ）/ pull / fetch / merge / branch -D / reset --hard
- GitHub操作: gh pr create / gh api 全般 / ブランチ削除
- パッケージ操作: npm install / pip install
- Web検索・フェッチ
- バックグラウンドプロセス起動

### 事前確認が必要な操作（例外のみ）
- `git push --force` を main / master ブランチに対して実行する場合
- `gh repo delete` 実行時

### 動作原則
- 計画提示（簡潔）→ 即実行 → 結果報告 のフロー厳守
- 事前確認文（「Should I run...?」等）を出力しない
- エラー時は即再試行 or 別アプローチで対応、判断が必要な場合のみ報告

## ドキュメント日付ルール

レポート・分析・調査系 .md ファイルを新規作成する際は、H1直下に必ず記載:

```
作成日: YYYY-MM-DD
最終更新日: YYYY-MM-DD
```

- 更新時は **最終更新日のみ** を当日付に書き換える（作成日は固定）
- 除外: README / CLAUDE.md / FILE_INDEX / tasks.md / CHANGELOG / LICENSE

## 作業品質ルール

### Git・ブランチ管理
- 作業前: `git branch --show-current` でブランチ確認 → main以外なら `git checkout main && git pull` してから開始。

### ファイル特定（編集前）
- ユーザー発話のキーワード全てをファイル名と照合してから編集。キーワード不完全一致・候補不確かなら必ず確認。

### 成果物報告
- ファイル作成・更新・push後は必ず3列表で報告: `| 成果物 | 説明 | リンク |`
- リンクは `/blob/<実ブランチ>/<パス>` 形式。報告前に `gh api repos/OWNER/REPO/contents/PATH?ref=BRANCH` で存在確認。push前はURL生成しない。

### ドキュメント品質
- UIパス・コマンド・設定名は公式ドキュメントで確認後に記載。確認不可なら「[要確認]」と明記。
- OS/環境制約（例: Windows専用）をタスク開始時に確認。完成後に `brew`/`Cmd`/`macOS` 等をgrepして除去。

<!-- GLOBAL_RULES_START -->
## Global Rules (synced from ~/.claude/CLAUDE.md)

### 成果物報告（最重要・毎回必須）
ファイルを1つでも作成・更新・pushしたら、**すべて**を3列表で報告する。例外なし。

| 成果物 | 説明 | リンク |
|---|---|---|
| ファイル名 | 1行説明 | [開く](https://github.com/OWNER/REPO/blob/BRANCH/PATH) |

厳守事項（違反＝再提出）:
1. Markdownリンク `[表示名](URL)` 形式必須。plain URL禁止。
2. `/blob/<実ブランチ名>/<実パス>` 形式。トップURL禁止。
3. 提示前に `gh api repos/OWNER/REPO/contents/PATH?ref=BRANCH` で存在確認。
4. ブランチ名は `git rev-parse --abbrev-ref HEAD` で取得。推測禁止。
5. push完了後のみURL生成。未pushはローカル絶対パス＋「（ローカル）」明記。
6. 404発生時は即訂正＋原因1行報告。

### ツール実行
- 確認不要・即実行。「Should I...?」等の事前確認文は出力しない。
- 例外（事前確認必須）: main/masterへの `git push --force`、`gh repo delete`。
- 長時間処理は `run_in_background: true` を積極使用。

### モデル・サブエージェント
- 全タスク Opus（期間限定）。サブエージェントも `model: "opus"` を明示。
- サブ起動promptに必ず明記:「成果物は3列表報告・URL検証必須・Markdownリンク形式」

### 回答スタイル
- 回答末尾に「**Next Action:**」でユーザーの次アクションを具体推奨。
## 他リポジトリ参照ルール
別リポジトリの内容を参照する必要が生じたら、必ず `.claude/cross-repo.md` を読み、その手順に従って `WebFetch` で取得する（「できない」と返さない）。

### 品質ルール（必読）
- ブランチ衛生・リサーチファクトチェックは `.claude/quality-rules.md` を参照し、ファイル生成前・push前に必ず適用する。
- Repo type: research

### ビジュアルルール（レポートMD生成時）
- レポート・成果物MDの新規作成／更新時は `.claude/visual-rules.md` を読み、図の種類判定（§2）と Mermaid 最適化（§3）を毎回適用する。
- 適用対象: `## ` 見出しが2つ以上ある構造化MD（README・調査メモ・設計書・PR説明など）。

<!-- SKILLS_RULES_START -->
## Skill 起動ルール（v1.0 / 2026-05-27）
- **新機能実装前** → `sp-brainstorming` → `sp-writing-plans` で設計
- **コミット/PR 前** → `code-review`（5 並列・confidence 80+）
- **アーキ図/フロー図が必要な時** → `mermaid-agents365`
- **要件調査が真に必要な時のみ** → `research-deep`
<!-- SKILLS_RULES_END -->

<!-- GLOBAL_RULES_END -->
