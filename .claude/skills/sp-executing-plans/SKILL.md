---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** Tell your human partner that Superpowers works much better with access to subagents. The quality of its work will be significantly higher if run on a platform with subagent support (such as Claude Code or Codex). If subagents are available, use superpowers:subagent-driven-development instead of this skill.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required workflow skills:**
- **superpowers:using-git-worktrees** - Ensures isolated workspace (creates one or verifies existing)
- **superpowers:writing-plans** - Creates the plan this skill executes
- **superpowers:finishing-a-development-branch** - Complete development after all tasks

## This Repository（本リポ適用）

各タスク完了時の verification には、`.claude/skills/sp-verification-before-completion/SKILL.md`
の「This Repository's Verification Commands」節にある本リポ固有検証コマンド表を用いる
（`scripts/check_comparison_report.py` / `scripts/check_research_report.py` の exit 0、
fact-check-reviewer の承認ログ、URL 実在確認、push 済みコミットの確認 等）。

レポート系タスク（`reports/` 配下への保存を伴うタスク）は、以下の両方が揃って初めて
「完了」とみなす（Step 2 の各タスク完了マークの条件）：

1. 該当リンター（`check_comparison_report.py` / `check_research_report.py`）が exit 0
2. `fact-check-reviewer`（ゲート 4・`docs/rules-research.md` §3）の判定が「承認」
   （または「条件付き承認」で指摘を本文に反映済み）

CLAUDE.md §5 の既定（main へ直接コミット）により、本リポでは
`superpowers:using-git-worktrees` / `superpowers:finishing-a-development-branch` の
ブランチ運用はユーザーが明示指示した場合のみ適用する。
