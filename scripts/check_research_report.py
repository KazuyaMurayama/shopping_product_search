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
