#!/usr/bin/env python3
"""
比較・ランキング・スコアリングレポートの機械検証リンター。

目的（失敗パターン 4・5・6／ルール D／価格乖離問題の再発防止）:
  - 価格が「リンク先チャネルの現行価格」であることを出典で機械検証する
  - リンク先チャネル ≠ 価格ソースチャネル、または出典種別が非ライブ（公式/スニペット）
    の場合は ⚠️ フラグを必須にする（"公式価格を Amazon 価格として掲載" を遮断）
  - 確認日・除外一覧・候補件数・禁止 URL を機械チェックする

対象の判定:
  ファイル先頭付近に `<!-- report-type: comparison -->` を含むレポートのみ検証する。
  含まない場合は SKIP（exit 0）。

検証する「価格出典」表（レポートに必須・人間にも可読）:
  ## 価格出典・在庫確認（機械検証用）
  | 商品 | リンク先 | 表示価格 | 価格の出典 | 出典種別 | 確認日 | フラグ |
  - リンク先 / 価格の出典: amazon / rakuten / yahoo / mercari / iherb / official のいずれか
  - 出典種別: live / snippet / official / marketplace / 2source のいずれか
  - 確認日: YYYY-MM-DD
  - フラグ: none または ⚠️ を含む

使い方:
  python3 scripts/check_comparison_report.py <report.md>
  exit 0 = 合格 / exit 1 = 違反あり（標準エラーに理由を出力）
"""
import sys
import re
import datetime

CHANNELS = {"amazon", "rakuten", "yahoo", "mercari", "iherb", "official"}
SOURCE_TYPES = {"live", "snippet", "official", "marketplace", "aggregator", "2source"}
# 出典種別がこれらの場合、リンク先チャネルの一次ライブ価格とは言えないため ⚠️ 必須。
# aggregator = kakaku.com 等の価格集約サイト経由（Amazon/楽天の一次ページが
# 取得不可な環境で、対象チャネルの価格を間接取得した場合に使う。要 ⚠️）。
NONLIVE_TYPES = {"snippet", "official", "aggregator"}
FORBIDDEN_URL = ["/s?k=", "search.rakuten", "/search/", "?keyword=", "?kw=", "?q=", "&k=", "?k="]
MIN_CANDIDATES = 15


def fail(errors):
    sys.stderr.write("\n".join(errors) + "\n")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: check_comparison_report.py <report.md>\n")
        sys.exit(1)
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        sys.stderr.write(f"読み込み不可: {e}\n")
        sys.exit(1)

    # 比較レポートでなければ検証対象外
    if "<!-- report-type: comparison -->" not in text[:2000]:
        sys.exit(0)

    errors = []
    lines = text.splitlines()

    # 1) 禁止 URL パターン
    for pat in FORBIDDEN_URL:
        if pat in text:
            errors.append(f"[禁止URL] 検索結果URLパターン '{pat}' を検出（失敗パターン1）")

    # 2) 除外製品一覧の存在
    if not re.search(r"##\s*除外", text):
        errors.append("[除外一覧] '## 除外製品' 節が無い（失敗パターン6／ルールA）")

    # 3) 価格出典表の抽出・検証
    prov_idx = None
    for i, ln in enumerate(lines):
        if "価格出典" in ln and ln.lstrip().startswith("#"):
            prov_idx = i
            break
    if prov_idx is None:
        errors.append("[価格出典] '## 価格出典・在庫確認（機械検証用）' 表が無い"
                      "（価格乖離・失敗パターン4/5の再発防止に必須）")
        fail(errors)

    # 表の行（| 始まり）を集める。ヘッダ行と区切り行を除く
    rows = []
    for ln in lines[prov_idx + 1:]:
        s = ln.strip()
        if s.startswith("#"):
            break
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        rows.append(cells)
    # ヘッダ行(商品|リンク先|...)・区切り行(---)を除外
    data_rows = []
    for cells in rows:
        joined = "".join(cells)
        if set(joined) <= set("-: "):  # 区切り行
            continue
        if cells and cells[0] in ("商品", "商品名"):
            continue
        if len(cells) >= 7:
            data_rows.append(cells)

    if len(data_rows) == 0:
        errors.append("[価格出典] 価格出典表にデータ行が無い")

    today = datetime.date.today()
    for cells in data_rows:
        name, link_ch, price, src, src_type, checked, flag = cells[:7]
        ctx = f"（行: {name}）"
        link_ch_l = link_ch.lower()
        src_l = src.lower()
        src_type_l = src_type.lower()

        if link_ch_l not in CHANNELS:
            errors.append(f"[リンク先] 不正なチャネル '{link_ch}' {ctx} 許容: {sorted(CHANNELS)}")
        if src_l not in CHANNELS:
            errors.append(f"[価格出典] 不正なソースチャネル '{src}' {ctx}")
        if src_type_l not in SOURCE_TYPES:
            errors.append(f"[出典種別] 不正な種別 '{src_type}' {ctx} 許容: {sorted(SOURCE_TYPES)}")

        # 価格に通貨数値があるか
        if not re.search(r"[¥￥]\s*[\d,]+", price) and "取得不可" not in price:
            errors.append(f"[価格] 価格に数値(¥)が無い '{price}' {ctx}（失敗パターン4）")

        # 確認日チェック
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})", checked)
        if not m:
            errors.append(f"[確認日] YYYY-MM-DD 形式でない '{checked}' {ctx}")
        else:
            try:
                d = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                if (today - d).days > 30:
                    errors.append(f"[確認日] 30日より古い '{checked}' {ctx}（価格は変動）")
            except ValueError:
                errors.append(f"[確認日] 不正な日付 '{checked}' {ctx}")

        has_warn = ("⚠" in flag) or ("warn" in flag.lower())

        # 中核ルール: リンク先と価格ソースが違えば ⚠️ 必須
        if link_ch_l in CHANNELS and src_l in CHANNELS and link_ch_l != src_l and not has_warn:
            errors.append(
                f"[価格×リンク不一致] リンク先='{link_ch}' だが価格出典='{src}' で ⚠️ 無し {ctx}。"
                "別チャネルの価格をリンク先の価格として掲載しているおそれ。⚠️ を付すか価格を取り直すこと")

        # 非ライブ出典（公式/スニペット）は ⚠️ 必須
        if src_type_l in NONLIVE_TYPES and not has_warn:
            errors.append(
                f"[非ライブ価格] 出典種別='{src_type}' はリンク先の現行価格と断定不可 {ctx}。"
                "⚠️ を付すこと（失敗パターン5）")

    # 4) 候補件数の下限（スコア表の行数で近似: '| N |' 行を数える代わりに価格出典表の件数で判定）
    scored = len(data_rows)
    if scored < MIN_CANDIDATES and "<!-- candidates-justified" not in text:
        errors.append(
            f"[網羅性] 価格出典表の候補が {scored} 件で下限 {MIN_CANDIDATES} 未満（失敗パターン6）。"
            "市場全体スキャンが不足。網羅した上で件数が妥当な理由がある場合は "
            "'<!-- candidates-justified: 理由 -->' を本文に記載すること")

    if errors:
        header = f"=== 比較レポート機械検証 NG: {path} ===\n検出 {len(errors)} 件:"
        fail([header] + [f"  - {e}" for e in errors])

    sys.exit(0)


if __name__ == "__main__":
    main()
