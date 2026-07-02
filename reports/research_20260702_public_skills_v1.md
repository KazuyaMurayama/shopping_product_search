<!-- report-type: research -->
# 公開 Claude Code スキル調査 & ハルシネーション対策ベストプラクティス調査

作成日: 2026-07-02
最終更新日: 2026-07-02

> `docs/plans/PLAN_QUALITY_UPGRADE_20260702.md` Task 10 に基づく Web 調査レポート。
> R1（Sonnet・調査担当）が作成。対象: (1) Anthropic 公式スキル、(2) obra/superpowers 現行スキル一覧、
> (3) コミュニティのスキル集（awesome-claude-code / awesome-claude-skills 等）からリサーチ・ファクトチェック系、
> (4) LLM 検索/リサーチエージェントのハルシネーション対策ベストプラクティス（2025〜2026）。

---

## 0. 調査範囲

**調査した範囲**:
- Anthropic 公式リポジトリ `github.com/anthropics/skills`（README・`skills/` ディレクトリ構成・`skill-creator/SKILL.md`）
- 公式ドキュメント `code.claude.com/docs/en/skills`（Agent Skills の仕様・frontmatter・運用ベストプラクティス）
- `obra/superpowers`（README・LICENSE・`dispatching-parallel-agents` / `requesting-code-review` / `systematic-debugging` の SKILL.md 本文）
- コミュニティのスキル集（`karanb192/awesome-claude-skills`、`hesreallyhim/awesome-claude-code`、`shubhamsaboo/awesome-llm-apps` の fact-checker、`imbad0202/academic-research-skills`）
- ハルシネーション対策の学術文献（MDPI・arXiv の 2025 年サーベイ／提案手法）

**調査しなかった範囲（理由つき）**:
- `obra/superpowers-skills`（コミュニティ編集可能フォーク）の個別スキル本文 — README に一覧が明示されておらず、確認できなかった
- `hesreallyhim/awesome-claude-code` の個別エントリ — 取得時点で目次が「準備中」表示で本文未公開だった
- 有償・エンタープライズ向け skills marketplace（LobeHub・skills.sh 等の二次配布サイト）の実体コード — 一次情報（GitHub 本体）を優先し、二次配布サイトはリンク掲載を見送った
- 日本語コミュニティのスキル集 — 英語圏中心の検索で見つからず、時間内に十分な件数を確認できなかった

---

## 1. 候補スキル一覧表

| 名称 | 提供元 | ライセンス | 概要 | 本リポとの関連度 | 導入判断案 |
|---|---|---|---|---|---|
| **skill-creator** | Anthropic（[anthropics/skills](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)） | Apache-2.0（README記載、大半のスキルが該当） | スキルの新規作成・改善・評価（テストケース作成→ベンチマーク→description最適化）を行うメタスキル | 高 | **導入推奨（TOP3）** |
| **dispatching-parallel-agents** | obra/superpowers（[SKILL.md](https://github.com/obra/superpowers/blob/main/skills/dispatching-parallel-agents/SKILL.md)） | MIT（[LICENSE](https://github.com/obra/superpowers/blob/main/LICENSE)） | 独立した2件以上のタスクを、専用スコープを与えたサブエージェントに並列ディスパッチし、統合レビューする手順 | 高 | **導入推奨（TOP3）** |
| **requesting-code-review** | obra/superpowers（[SKILL.md](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md)） | MIT | 完了タスク・マージ前に code-reviewer サブエージェントを派遣し Critical/Important/Minor で判定させる手順 | 中〜高 | **導入推奨（TOP3）** |
| systematic-debugging | obra/superpowers（[SKILL.md](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md)） | MIT | 「症状ではなく根本原因を直す」4段階プロセス（調査→パターン分析→仮説検証→実装） | 中 | 見送り（次点） |
| receiving-code-review | obra/superpowers | MIT | レビューコメントへの建設的な対応手順（[karanb192/awesome-claude-skills](https://raw.githubusercontent.com/karanb192/awesome-claude-skills/main/README.md) に概要記載） | 中 | 見送り |
| subagent-driven-development | obra/superpowers | MIT | 計画をタスク単位でサブエージェントに委譲し2段階レビューする開発手法 | 中 | 見送り |
| writing-skills | obra/superpowers | MIT | superpowers 独自のスキル作成・改善メタスキル | 中 | 見送り（skill-creator と重複） |
| test-driven-development | obra/superpowers | MIT | テストファースト開発の手順 | 低 | 見送り |
| using-git-worktrees | obra/superpowers | MIT | 設計承認後に新ブランチ・worktree を作成する手順 | 低 | 見送り |
| finishing-a-development-branch | obra/superpowers | MIT | 開発ブランチの完了・マージ処理 | 低 | 見送り |
| using-superpowers | obra/superpowers | MIT | superpowers フレームワーク全体の導入・運用ガイド | 低 | 見送り |
| brainstorming（superpowers版） | obra/superpowers | MIT | 本リポ既存の `sp-brainstorming` の原典 | — | 導入済み（比較対象外） |
| fact-checker | shubhamsaboo/awesome-llm-apps（[repo](https://github.com/shubhamsaboo/awesome-llm-apps)、[紹介ページ](https://awesomeskill.ai/skill/shubhamsaboo-awesome-llm-apps-fact-checker)） | Apache-2.0 | 主張の特定→証拠評価→情報源信頼性評価→TRUE/FALSE/UNVERIFIABLE 判定 | 中 | 見送り（本リポは同種の `fact-check-reviewer` を Task 4 で専用構築済み） |
| academic-research-skills（Deep Research / Paper Reviewer 等） | Cheng-I Wu（[imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills)） | CC-BY-NC 4.0（非商用・要帰属） | 研究→執筆→査読（Devil's Advocate 含む7エージェント）→修正→最終化の10段階パイプライン | 中 | 見送り（設計思想は `coverage-critic` に反映済み。非商用ライセンスのためコード転用不可） |
| 公式 anthropics/skills のドメイン特化スキル13件（`docx` / `pdf` / `pptx` / `xlsx` / `algorithmic-art` / `brand-guidelines` / `canvas-design` / `claude-api` / `doc-coauthoring` / `frontend-design` / `internal-comms` / `mcp-builder` / `slack-gif-creator` / `theme-factory` / `web-artifacts-builder` / `webapp-testing`） | Anthropic（[skills/ 一覧](https://github.com/anthropics/skills/tree/main/skills)） | Apache-2.0（`docx`/`pdf`/`pptx`/`xlsx` はソースアベイラブルで非OSS） | Office文書処理・デザイン・Webアプリテスト・MCPサーバー生成等 | 低 | 見送り（本リポのドメイン＝EC横断商品検索・Markdownレポートと不一致） |
| recursive-research / business-research 系コミュニティスキル | 不明（検索結果のみで一次情報未確認） | 不明 | 「博士レベルまでの再帰的リサーチ」「戦略フレームワーク＋エビデンス格付け」等の記述あり | 低 | 見送り（提供元・ライセンス・実体を確認できなかったため不採用） |

---

## 2. 導入推奨 TOP3（理由つき）

### 1位: dispatching-parallel-agents（obra/superpowers, MIT）
本リポは Amazon / 楽天 / Yahoo!ショッピング / iHerb / メルカリ / Osakado の 6 チャネルを scout エージェントで並列調査する構成であり、[dispatching-parallel-agents の SKILL.md](https://github.com/obra/superpowers/blob/main/skills/dispatching-parallel-agents/SKILL.md) が定める「独立した領域を特定→焦点を絞ったタスクを作成→同一レスポンス内で並列ディスパッチ→レビューと統合」という手順は、現状 `search-product` コマンドに暗黙的にしか書かれていないパターンを明文化できる。ライセンス（MIT）上も改変・再配布に問題がない。

### 2位: skill-creator（Anthropic 公式, Apache-2.0）
本リポは今回の計画だけでも `coverage-planning` を含む複数の独自スキルを新規作成しており、今後も増える見込みである。[skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) が提供する「テストケース作成→ベンチマーク→ユーザーフィードバック→description最適化」という評価駆動のスキル改善サイクルは、本リポの既存スキル（`sp-brainstorming` 等）に現状欠けている「スキルが実際にトリガーし機能しているかの検証手段」を補う。Anthropic 公式・大半 Apache-2.0 で改変可能な点も導入障壁が低い。

### 3位: requesting-code-review（obra/superpowers, MIT）
本計画自体が `scripts/check_research_report.py`・`.claude/hooks/check_report.sh` 等のコード変更を含み、`docs/plans/PLAN_QUALITY_UPGRADE_20260702.md` の Task 14 でも「統合差分レビュー」を最終ステップに置いている。[requesting-code-review](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md) の Critical/Important/Minor 判定・BASE_SHA/HEAD_SHA を明示したサブエージェント派遣手順は、この統合レビュー工程をそのまま形式化できる。`fact-check-reviewer`（レポート内容の事実検証）とは対象が異なり（コード正しさ vs 事実正確性）、重複しない。

---

## 3. 見送り理由リスト（見送り候補も全件明記）

| # | 候補 | 見送り理由 |
|---|---|---|
| 1 | systematic-debugging | 有効だが今回の3枠には入らない次点。フック/リンターが原因不明のエラーを出した際の「4段階根本原因プロセス」として今後導入価値あり |
| 2 | receiving-code-review | requesting-code-review と対だが、今回は「レビューを依頼する側」の手順整備を優先し、受け手側は既存の `sp-executing-plans` の運用でカバー可能と判断 |
| 3 | subagent-driven-development | 本リポは既に `sp-executing-plans`（superpowers の executing-plans 由来）を採用済みで役割が重複する |
| 4 | writing-skills（superpowers版） | 同種のメタスキルとして Anthropic 公式 `skill-creator` を優先するため重複導入を避ける |
| 5 | test-driven-development | 本リポはテストコードを持つソフトウェア開発ではなく、Markdown/Bash/Python の小規模スクリプトが中心で適用範囲が薄い |
| 6 | using-git-worktrees | CLAUDE.md §5「既定: main へ直接コミット」の運用方針と衝突するため導入しない |
| 7 | finishing-a-development-branch | 同等機能を本リポ独自の `branch-cleanup` スキルが既にカバーしている |
| 8 | using-superpowers | フレームワーク全体ではなく個別スキルの部分採用方針のため、導入ガイド自体は不要 |
| 9 | fact-checker（shubhamsaboo/awesome-llm-apps） | `docs/plans/PLAN_QUALITY_UPGRADE_20260702.md` Task 4 で、Amazon 503／楽天ボット遮断など本リポ固有の制約に対応した `fact-check-reviewer` を専用構築済みのため機能が重複する。TRUE/FALSE/UNVERIFIABLE の3値判定という設計思想は参考にした |
| 10 | academic-research-skills（Deep Research 等） | Devil's Advocate レビュー・段階的品質ゲートという設計思想は `coverage-critic` に反映済みだが、CC-BY-NC 4.0（非商用・要帰属）のためコードそのものの転用はできない |
| 11 | anthropics/skills のドメイン特化13スキル（docx/pdf/pptx/xlsx/algorithmic-art/brand-guidelines/canvas-design/claude-api/doc-coauthoring/frontend-design/internal-comms/mcp-builder/slack-gif-creator/theme-factory/web-artifacts-builder/webapp-testing） | 本リポのドメイン（EC横断商品検索・比較・Markdownレポート生成）と直接の接点がない。レポートの PDF/Word 出力ニーズが将来発生すれば `docx`/`pdf` を再検討 |
| 12 | recursive-research / business-research 系コミュニティスキル | 提供元・ライセンス・実体（実際の SKILL.md 本文）を検索結果の要約以上に確認できなかった。記憶や推測で埋めず、確認できなかった事項として明記する |

---

## 4. ハルシネーション対策ベストプラクティス（2025〜2026）

### 4.1 主要な知見

1. **Claim extraction + 独立検証**: 生成された回答を原子的な主張（atomic claims）に分解し、各主張を取得済みコンテキストと突き合わせて LLM-as-a-judge で検証する手法が一般化している。段階的な HiSS（Hierarchical Step-by-Step）プロンプティングのように、複雑な主張を部分クレームに分解し「単一の誤りが全体の誤った結論に波及するリスク」を下げる設計が推奨されている（[arXiv 2508.03860](https://arxiv.org/html/2508.03860v1)）。
2. **Consultant/Evaluator の反復修正ループ**: 生成担当エージェント（Consultant）と、ルールベース＋LLM 評価担当エージェント（Evaluator）を分離し、類似度スコアが閾値未満なら最大数回の反復修正を行うフレームワークで、実験ではハルシネーション率を LLaMA-3-8B で 32.6%→4.7%、Mistral-7B で 60.2%→19.5% まで低減したと報告されている（【要約】出典: [MDPI Information 16(7):517](https://www.mdpi.com/2078-2489/16/7/517)。数値は当該論文の実験結果であり、一般化を保証するものではない）。
3. **Retrieval-Augmented Generation（RAG）によるグラウンディング**: 外部の検証可能な知識源に出力を基盤化することが最重要とされ、複数ソース（検索API・知識グラフ等）からの交差検証が推奨されている（[arXiv 2508.03860](https://arxiv.org/html/2508.03860v1)）。
4. **説明可能性・監査可能性**: 正誤の二値判定だけでなく、証拠源の引用・推論過程の記録・ユーザーが監査できるシグナルの生成が2025年の実務的推奨事項として挙げられている（同上）。
5. **Adversarial/Red-team的な出力検証**: 2026年にかけて、AIエージェントの出力検証にも敵対的（adversarial）なテスト・非決定性を前提にした複数回試行評価という発想が広がっており、単発の確認では見逃す欠陥を洗い出す考え方が強調されている（検索結果の要約に基づく一般的傾向であり、個別の一次資料までは確認できなかった）。

### 4.2 本リポ既存仕組みとの対応・ギャップ表

| ベストプラクティス | 本リポの既存仕組み | ギャップ |
|---|---|---|
| Claim extraction + 独立検証エージェント | `fact-check-reviewer`（`docs/plans/PLAN_QUALITY_UPGRADE_20260702.md` Task 4・ゲート4） | 今回の計画で新設されたばかりで実運用実績がゼロ。主張ごとの✅/⚠️/❌判定表は定義されているが、運用開始後の効果測定（誤検出率・見逃し率）の仕組みはまだ無い |
| 出典グラウンディング（引用/要約/推定の3分類） | `.claude/quality-rules.md` ルール2(b)、`docs/rules-research.md` §2 | 数値・引用には出典URL＋確認日を必須化しているが、「主張1件ごとに出典が1対1で対応しているか」の自動検証は無く、人手のセルフチェックに依存 |
| Consultant/Evaluator の反復修正ループ（閾値ベース自動反復） | ゲート4は「❌があれば修正して再レビュー」の1往復のみ | 反復回数の上限・スコアリング閾値・自動化された再試行の仕組みは無い（現状は定性的な承認/差し戻しのみ） |
| Adversarial/Devil's-Advocate的な反証検証 | `coverage-critic`（着手前の観点・ブランド地図の抜け漏れ監査） | 着手前の網羅性チェックには反証視点が組み込まれているが、成果物（完成後のレポート）そのものへの反証的な圧力テストは `fact-check-reviewer` の役割に一部含まれるのみで、専用の red-team 的レビューは無い |
| 機械検証（linter）による最終ゲート | `scripts/check_comparison_report.py`、`scripts/check_research_report.py`、`.claude/hooks/check_report.sh` | URL禁止パターン・出典セクション・リンク本数・確認日の形式検証はできるが、「本文の主張と出典URLの内容が実際に一致しているか」までは機械検証できない（意味的な照合は人間/レビューアの担当） |
| 説明可能性・監査可能性（確信度・推論過程の記録） | ヘッジ語必須（「考えられる」「推定される」等）、【引用】【要約】【推定】ラベル | 定性的なラベルのみで、数値的な confidence score は導入していない |

---

## 5. 導入結果

Task 12（E3・担当）にて、上記「2. 導入推奨 TOP3」の 3 件を採用した。見送り対象は
「3. 見送り理由リスト」（本レポート内・既存節）を参照（本節では追加の見送り判断は発生していない）。

| # | 採用スキル | ファイルパス | 適合内容の要約 |
|---|---|---|---|
| 1 | dispatching-parallel-agents（obra/superpowers, MIT） | `.claude/skills/sp-dispatching-parallel-agents/SKILL.md` | 原文の章立て（When to Use／The Pattern／Agent Prompt Structure／Common Mistakes／Verification）を踏襲し日本語化。本リポの 6 チャネル scout（amazon-scout / rakuten-scout / yahoo-shopping-scout / iherb-scout / mercari-scout / osakado-scout）を並列ディスパッチの実例として追加し、`coverage-critic` と `fact-check-reviewer` を並列化してよい局面／してはいけない局面（両ゲートの想定順序は変更しない）を明記。統合ステップに `scripts/check_comparison_report.py` / `scripts/check_research_report.py` の機械検証を組み込んだ |
| 2 | skill-creator（Anthropic 公式, Apache-2.0） | `.claude/skills/skill-creator/SKILL.md` | 原文は `scripts/init_skill.py` 等の同梱スクリプト・自動ベンチマークを前提とするため WebFetch では要約のみ取得（frontmatter は verbatim 確認）。本リポには同梱スクリプトが無いため、スクリプトなし・Markdown 完結型の簡易ワークフロー（意図把握→ヒアリング→執筆→目視でのトリガー精度確認→改善）として再構成。本リポ既存スキルの frontmatter 形式（`name`/`description` のみ）・出典コメント明記ルールとの一貫性維持を「This Repository」節に明記 |
| 3 | requesting-code-review（obra/superpowers, MIT） | `.claude/skills/sp-requesting-code-review/SKILL.md` | 原文が参照する別ファイル `code-reviewer.md` は本リポでは作成対象外のため、レビュー依頼テンプレートを本ファイル内にインライン化。対象を「コード・設定の正しさ」（`scripts/*.py`・`.claude/hooks/*.sh`・`.claude/agents/*.md`）に限定し、レポート内容の事実検証を担当する `fact-check-reviewer`（ゲート4）とは対象が異なり重複しないことを明記。本リポに専用 `code-reviewer` サブエージェントが無いため `general-purpose` サブエージェントへのディスパッチ手順とした |

**原典取得可否**: dispatching-parallel-agents・requesting-code-review は WebFetch
（`raw.githubusercontent.com`）で原文全文を verbatim 取得できた。skill-creator は
frontmatter のみ verbatim 取得でき、本文は WebFetch の要約結果に基づく再構成（自作）である
旨を各 SKILL.md 冒頭のコメントに明記した。

`.claude/skills/sp-brainstorming/SKILL.md` / `sp-writing-plans/SKILL.md` /
`sp-executing-plans/SKILL.md` の 3 件には、本リポの `docs/rules-research.md`（観点マトリクス・
ゲート4）と接続する「## This Repository（本リポ適用）」節を追記し、既存構造は変更していない
（`docs/plans/PLAN_QUALITY_UPGRADE_20260702.md` Task 11）。

`CLAUDE.md` §10 のスキル表への登録は本レポート・本タスクの担当外（後続 E4 が実施）。

---

## 検証記録

- 本レポートは `scripts/check_research_report.py` によるリンター（禁止URLパターン・H1メタデータ・出典節・リンク本数・確認日）の対象。保存時に自動検証される。
- fact-check-reviewer による独立レビュー（ゲート4）は本タスク（Task 10）の要件外のため未実施。Task 12 で本レポートの推奨内容を採用する際に、必要であれば別途レビューを検討する。

---

## 出典

- [GitHub - anthropics/skills: Public repository for Agent Skills](https://github.com/anthropics/skills)（確認: 2026-07-02）
- [skills/skills/skill-creator/SKILL.md at main · anthropics/skills](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)（確認: 2026-07-02）
- [skills/skills at main · anthropics/skills（全17スキルのディレクトリ一覧）](https://github.com/anthropics/skills/tree/main/skills)（確認: 2026-07-02）
- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills)（確認: 2026-07-02）
- [GitHub - obra/superpowers: An agentic skills framework & software development methodology](https://github.com/obra/superpowers)（確認: 2026-07-02）
- [obra/superpowers LICENSE（MIT）](https://github.com/obra/superpowers/blob/main/LICENSE)（確認: 2026-07-02）
- [superpowers/skills/dispatching-parallel-agents/SKILL.md at main · obra/superpowers](https://github.com/obra/superpowers/blob/main/skills/dispatching-parallel-agents/SKILL.md)（確認: 2026-07-02）
- [superpowers/skills/requesting-code-review/SKILL.md at main · obra/superpowers](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md)（確認: 2026-07-02）
- [superpowers/skills/systematic-debugging/SKILL.md at main · obra/superpowers](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md)（確認: 2026-07-02）
- [GitHub - obra/superpowers-skills: Community-editable skills for Claude Code's superpowers plugin](https://github.com/obra/superpowers-skills)（確認: 2026-07-02、個別スキル本文は未公開で確認できず）
- [GitHub - hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)（確認: 2026-07-02、目次「準備中」で個別エントリ未確認）
- [karanb192/awesome-claude-skills README](https://raw.githubusercontent.com/karanb192/awesome-claude-skills/main/README.md)（確認: 2026-07-02）
- [fact-checker - Claude Skill（shubhamsaboo/awesome-llm-apps 紹介ページ）](https://awesomeskill.ai/skill/shubhamsaboo-awesome-llm-apps-fact-checker)（確認: 2026-07-02）
- [GitHub - shubhamsaboo/awesome-llm-apps](https://github.com/shubhamsaboo/awesome-llm-apps)（確認: 2026-07-02）
- [GitHub - imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills)（確認: 2026-07-02）
- [Mitigating LLM Hallucinations Using a Multi-Agent Framework - MDPI Information 16(7):517](https://www.mdpi.com/2078-2489/16/7/517)（確認: 2026-07-02）
- [Hallucination to Truth: A Review of Fact-Checking and Factuality Evaluation in Large Language Models - arXiv 2508.03860](https://arxiv.org/html/2508.03860v1)（確認: 2026-07-02）

---

## 参照（本リポ内・調査前提として確認した既存ファイル）

- `.claude/skills/`（`branch-cleanup` / `mermaid-agents365` / `sp-brainstorming` / `sp-executing-plans` / `sp-verification-before-completion` / `sp-writing-plans`。今回の並行タスクで `coverage-planning` が追加済み）
- `.claude/quality-rules.md`（ルール1: ブランチ衛生、ルール2: リサーチ・ファクトチェック）
- `docs/rules-search-product.md`（失敗パターン1〜6、ゲート1〜3、第0.5章 ルールD 等）
- `docs/rules-research.md`（本計画の Task 1 で E1 が新設。網羅性ゲート・ハルシネーション対策・レビューゲートの共通ルール）
