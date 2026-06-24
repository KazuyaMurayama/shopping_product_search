#!/usr/bin/env bash
# PostToolUse フック: Write/Edit で reports/*.md が保存されたら比較レポートリンターを実行する。
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
linter="$repo_root/scripts/check_comparison_report.py"
[ -f "$linter" ] || exit 0

if ! out="$(python3 "$linter" "$file_path" 2>&1)"; then
  {
    echo "比較レポートの機械検証で違反を検出しました。修正してから完了してください。"
    echo "$out"
  } >&2
  exit 2
fi
exit 0
