---
name: skill-creator
description: "Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. 本リポでは `.claude/skills/` 配下の新規スキル作成・既存スキル改訂・トリガー精度の見直し（例: 本計画 Task 1〜12 で作成した coverage-planning / sp-* 系スキル群）を行う際に必ず参照する。"
---

<!--
出典: https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md
提供元: Anthropic（anthropics/skills）
ライセンス: Apache-2.0（README 記載。docx/pdf/pptx/xlsx の 4 スキルのみソースアベイラブルで
  非 OSS だが、skill-creator はそれに該当しない。確認: 2026-07-02）
取得方法: WebFetch で frontmatter は verbatim 確認済み。本文は原文が
  `scripts/init_skill.py`・`scripts/package_skill`・`scripts/run_loop`・
  `agents/grader.md`・`eval-viewer/generate_review.py` 等の同梱スクリプト群を前提にした
  長大な内容のため、WebFetch では要約された内容のみを取得できた（原文全文の逐語取得はできず）。
  本ファイルは、取得できた要約（5段階ワークフロー・SKILL.md構造・トリガー精度最適化の考え方）
  と公式ドキュメント（code.claude.com/docs/en/skills）の記述に基づき、同梱スクリプトを持たない
  本リポ向けに Markdown 完結型（スクリプト同梱なし）ワークフローとして再構成した自作コンテンツ
  である。原文の逐語コピーではない。
-->

# スキル作成・改善（Skill Creator）

`.claude/skills/` 配下のスキル（SKILL.md）を新規作成・改善・評価するためのメタスキル。
本リポでは、商品検索専用スキル（例: `add-channel`）から汎用開発スキル（`sp-writing-plans` 等）
まで性質の異なるスキル群を運用しており、新規スキルの追加や既存スキルの改訂が今後も発生する
見込みである。本スキルはその際の標準手順を定義する。

## コア原則

- **説明より理由付け（Explanation over Rules）**: 些末な「〜してはいけない」の羅列で縛るより、
  なぜその手順が必要かを説明する方が、モデルは丸暗記の手順を超えて応用的に判断できる
- **汎化を優先する（Generalization）**: 特定の 1 ケースだけに過学習した改善をしない。
  スキルは将来の多様な依頼に対して機能する必要がある
- **description がトリガー精度を決める**: frontmatter の `description` は、いつ・どんな依頼で
  このスキルが呼ばれるかを決める最重要フィールド。「何をするスキルか」と「どんな文脈で
  トリガーすべきか」の両方を含める

## SKILL.md の構造

- **YAML frontmatter**（`name` / `description` のみ。本リポの既存スキルと同形式）
- **Markdown 本文の指示**（目安 500 行以内。長すぎる場合は分割・要約を検討する）
- 必要であれば `references/` 等の補助ファイルを同梱してよいが、本リポの既存スキルは
  現状すべて単一ファイル構成（`SKILL.md` のみ）であり、その慣習に従うことを推奨する

## 手順

### 1. 意図の把握

- このスキルは何を達成すべきか、いつトリガーされるべきか、期待される出力は何かを整理する
- 既存スキル（`.claude/skills/*/SKILL.md`）と役割が重複しないか確認する
  （重複が疑われる場合は新規作成ではなく既存スキルの改訂を検討する）

### 2. ヒアリングと調査

- エッジケース・出力フォーマット・成功基準について具体的に詰める
- 本リポ固有の参照先（`docs/rules-research.md` / `docs/rules-search-product.md` /
  `.claude/agents/*.md` / `scripts/*.py`）のうち、このスキルが接続すべきものを洗い出す

### 3. SKILL.md の執筆

- frontmatter は `name` / `description` のみ（本リポの既存スキルと同形式）
- 本文は日本語で、原典がある場合は出典・ライセンスを frontmatter 直後にコメントで明記する
- プレースホルダ（TBD 等）を残さない。本リポの命名・参照ルールを実際のパスで埋める

### 4. トリガー精度の検証（簡易版・スクリプトなし）

原典は自動評価スクリプト（`scripts/run_loop` 等）でトリガー精度を最適化するが、本リポには
同梱スクリプトが無いため、以下の簡易手順で代替する：

1. 「このスキルが呼ばれるべき依頼文」を 5〜10 件、日本語で書き出す
2. 「このスキルが呼ばれるべきでない依頼文（紛らわしい近縁ケース）」も 5 件程度書き出す
3. `description` を読み直し、上記の依頼文それぞれに対して自然にトリガーされそうか目視で確認する
4. トリガー条件が曖昧な場合、`description` にトリガー語句（依頼文に出現しやすい具体的な
   キーワード）を追記する（本リポの他スキルの例: `coverage-planning` の
   「調査・リサーチ・商品検索・比較タスクの着手時に必ず使用」という明示的トリガー文）

### 5. 改善・反復

- ユーザーフィードバックや実運用での「トリガーされなかった」「意図と違う動作をした」報告を
  受けたら、`description` または本文の手順を調整する
- 改訂の際も、Task 11 で `sp-brainstorming` 等に適用したのと同様に「原文の構造を壊さず
  末尾に追記する」形を優先し、既存の参照関係（他スキル・エージェント・ドキュメントからの
  リンク）を壊さないようにする

## This Repository（本リポ適用）

1. **既存スキルとの一貫性**: 新規スキル作成時は、本リポ既存スキル（`add-channel` /
   `check-conditions` / `coverage-planning` / `sp-brainstorming` 等）の frontmatter 形式
   （`name` / `description` のみ）とファイル配置（`.claude/skills/<name>/SKILL.md`）に必ず
   従う。ライセンス上の理由で外部由来のコンテンツを含む場合は、frontmatter 直後にコメントで
   出典 URL・原作者・ライセンスを明記する（本ファイル自身がその実例）。
2. **CLAUDE.md §10 との連携**: 新規作成したスキルは `CLAUDE.md` §10 のスキル表に
   「トリガー → スキルパス」の形式で追記する（本リポでは E4 が統合担当。本スキル単体では
   CLAUDE.md を編集しない）。
3. **調査系スキルとの役割分担**: `coverage-planning`（着手時の網羅性設計）・
   `sp-verification-before-completion`（完了前検証）・`sp-dispatching-parallel-agents`
   （並列委譲）・`sp-requesting-code-review`（コードレビュー依頼）は、いずれも本スキルで
   新規追加・改訂されうる対象である。新スキルを作る前に、これらで代替できないか確認する。
4. **評価データが無い前提での運用**: 原典が前提とする自動ベンチマーク（`total_tokens` /
   `duration_ms` の計測、baseline との比較実行）は本リポの運用では実施しない。トリガー精度は
   上記「手順 4」の目視チェックで代替し、精度に不安が残る場合はその旨を
   `reports/` の該当レポートまたは `tasks.md` に明記して次回レビューに引き継ぐ。
