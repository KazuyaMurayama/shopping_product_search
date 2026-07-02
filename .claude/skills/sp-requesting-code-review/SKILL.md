---
name: requesting-code-review
description: "Use when completing tasks, implementing major features, or before merging to verify work meets requirements. 本リポでは scripts/*.py・.claude/hooks/*.sh・.claude/agents/*.md 等のコード/設定変更をコミット・main へマージする前に必ず参照する（レポート本文の事実検証は fact-check-reviewer＝ゲート4が担当し、本スキルはコード・設定の正しさ専用）。"
---

<!--
出典: https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md
原作者: obra（Jesse Vincent）/ obra/superpowers
ライセンス: MIT（https://github.com/obra/superpowers/blob/main/LICENSE ／確認: 2026-07-02）
取得方法: WebFetch（raw.githubusercontent.com）で原文を取得済み。

原文は付属テンプレート `code-reviewer.md`（別ファイル）を参照する構成だが、本リポでは
Task 12 の作成対象を本 SKILL.md 1 ファイルに限定しているため、レビュー依頼テンプレートは
本ファイル内にインライン化した。本文は日本語化し、本リポの検証対象（scripts/ の Python
リンター・.claude/hooks/ のフック・.claude/agents/ のエージェント定義）向けに適合させた。
原文の逐語コピーではない。
-->

# コードレビュー依頼（Requesting Code Review）

コードレビュー担当のサブエージェントをディスパッチし、問題が連鎖する前に検出する手順スキル。
レビューアには厳密に組み立てたコンテキストだけを渡す — オーケストレーターのセッション履歴は
渡さない。これによりレビューアは作業成果物そのものに集中でき（作業者の思考過程に引きずられない）、
オーケストレーター自身のコンテキストも温存できる。

**核心原則:** 早く・頻繁にレビューする。

## レビューを依頼すべき場面

**必須:**
- 計画の各タスク完了後（サブエージェント駆動開発の場合。本リポでは
  `docs/plans/<TOPIC>_YYYYMMDD.md` のタスク単位）
- 主要な機能・スクリプト・フックの実装完了後
- main へマージ（コミット）する前

**任意だが価値がある:**
- 行き詰まったとき（新しい視点を得る）
- リファクタリング前（ベースライン確認）
- 複雑なバグ修正の後

## 依頼方法

**1. git SHA を取得する**

```bash
BASE_SHA=$(git rev-parse HEAD~1)  # または origin/main
HEAD_SHA=$(git rev-parse HEAD)    # 作業ツリーの差分を見る場合は HEAD のままでもよい
```

**2. レビュー担当サブエージェントをディスパッチする**

`general-purpose` サブエージェント（または `code-review` スキルが利用可能ならそれ）に、
以下のテンプレートを埋めて渡す：

```markdown
以下のコード変更をレビューしてください。

対象: {DESCRIPTION}（例: scripts/check_research_report.py の新規追加）
要件: {PLAN_OR_REQUIREMENTS}（例: docs/plans/PLAN_QUALITY_UPGRADE_20260702.md Task 5）
差分: git diff {BASE_SHA}..{HEAD_SHA} -- {対象パス}

観点:
1. 要件（計画のタスク記述）を満たしているか
2. エラーハンドリング・境界値（空ファイル・存在しないパス等）
3. 本リポの既存パターンとの整合性（他の scripts/*.py・他の .claude/agents/*.md との一貫性）
4. セキュリティ・破壊的変更（git 操作・ファイル削除等が安全か）

出力形式:
  Critical: [即修正が必要な問題]
  Important: [次に進む前に直すべき問題]
  Minor: [後回しでよい改善点]
  総合判定: 対応済み・提案どおり進めてよい / 修正が必要
```

**プレースホルダ:**
- `{DESCRIPTION}` — 何を作ったかの簡潔な要約
- `{PLAN_OR_REQUIREMENTS}` — 何をすべきだったか（計画のタスク番号・要件）
- `{BASE_SHA}` / `{HEAD_SHA}` — 差分の開始・終了コミット

**3. フィードバックに対応する**

- Critical は即座に修正
- Important は次のタスクに進む前に修正
- Minor は後回し（tasks.md のバックログに追記してよい）
- レビューアが誤っている場合は、根拠（テスト結果・実際の挙動）を示して反論してよい

## 統合先ワークフローとの関係

**sp-executing-plans（計画実行）:**
- 各タスク完了後にレビューを依頼し、問題が積み重なる前に修正する

**アドホックな変更:**
- main へのマージ前に必ずレビュー
- 行き詰まったときに依頼

## Red Flags（やってはならないこと）

**絶対にしてはいけない:**
- 「単純だから」とレビューを省略する
- Critical な指摘を無視する
- Important な指摘を未修正のまま次に進む
- 妥当な技術的指摘に対して根拠なく反論する

**レビューアが誤っていると思ったら:**
- 技術的根拠（テスト結果・ログ・実際の挙動）を示して反論する
- 明確化を求める

## This Repository（本リポ適用）

1. **対象範囲の明確化**: 本スキルは **コード・設定の正しさ**（`scripts/*.py` の
   リンターロジック・`.claude/hooks/*.sh` のフック・`.claude/agents/*.md` /
   `.claude/skills/*/SKILL.md` の frontmatter/構造整合性）を対象とする。
   **レポート本文の事実正確性**（数値・引用・URL の実在等のハルシネーション検証）は
   `fact-check-reviewer`（ゲート4・`docs/rules-research.md` §3）の担当であり、本スキルとは
   対象が異なるため重複しない。コード変更とレポート成果物の両方を含むタスクでは、
   両方のレビューを実施する。
2. **本リポでの実行手段**: 本リポには専用の `code-reviewer` サブエージェント定義は無いため、
   `general-purpose` サブエージェントに上記テンプレートを渡してディスパッチするか、
   Claude Code 組み込みの `code-review` スキル（利用可能な場合）を使う。
3. **検証コマンドとの併用**: レビュー依頼の前に、可能であれば機械検証
   （`python3 scripts/check_research_report.py` / `python3 scripts/check_comparison_report.py` /
   `bash -n .claude/hooks/*.sh`）を実行し、その結果もレビューア向けコンテキストに含める
   （レビューアが同じ検証を再実行する手間を省く）。
4. **push・main マージ前の必須ゲート**: `CLAUDE.md` §5「既定: main へ直接コミット」の運用上、
   push 前のレビューは特に重要（ブランチでの隔離が無いため）。`.claude/skills/sp-executing-plans/SKILL.md`
   の完了条件（リンター exit 0・ゲート4承認）に加えて、コード変更を含むタスクは本スキルの
   レビューも完了条件に含める。
