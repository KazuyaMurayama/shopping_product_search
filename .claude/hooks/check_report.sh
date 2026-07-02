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
