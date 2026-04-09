# docs/channels.md — 対象チャネル詳細リファレンス

このファイルは CLAUDE.md セクション 1 から抽出された詳細リファレンスです。
個別スカウトエージェント（`.claude/agents/*-scout.md`）が起動されたときに
参照されます。毎回の会話で読み込む必要はありません。

各チャネルに共通する禁止パターン：
`search`, `?k=`, `?s=`, `?keyword=`, `?kw=`, `?q=`, `/search/`, `/s?`

---

## Amazon.co.jp

- 個別商品 URL：`https://www.amazon.co.jp/dp/[ASIN]`
- ASIN 形式：`[A-Z0-9]{10}`
- robots.txt により直接フェッチ不可。検索スニペット内から ASIN を抽出して
  URL を組み立てる
- 「Currently unavailable」「在庫切れ」は除外
- スカウト定義：`.claude/agents/amazon-scout.md`

---

## メルカリ

- 個別商品 URL：`https://jp.mercari.com/item/[ITEM_ID]`
- ITEM_ID 形式：`m[0-9]{10,}` または英数字の商品 ID
- 出品終了・売り切れ（SOLD）は除外
- 中古品のため**状態（新品 / 未使用 / 目立った傷なし 等）必須記載**
- 出品者評価が確認できる場合は付記
- 譲渡解除（旧出品者からの紐付け解除）の要否を要確認（特に Tile / MAMORIO / Chipolo）
- スカウト定義：`.claude/agents/mercari-scout.md`

---

## 楽天市場

- 個別商品 URL：`https://item.rakuten.co.jp/[SHOP]/[ITEM_ID]/`
- 文字化け（EUC-JP）対応：URL 存在確認は検索スニペットで行う
- ショップレビュー / 商品レビューの両方を確認
- 「あす楽」対応の有無を付記
- 検索結果 URL：`search.rakuten.co.jp` ← **絶対禁止**
- 楽天市場は構造上、Bluetooth トラッカー等の小型電子機器の中古流通は
  ほぼ無い点に留意
- スカウト定義：`.claude/agents/rakuten-scout.md`

---

## iHerb

- 個別商品 URL：`https://jp.iherb.com/pr/[商品名スラッグ-ID]`
- サプリ・健康食品中心。**成分表記の確認が重要**
- 在庫状況（In Stock / Out of Stock）必須確認
- セール価格表示時は**通常価格も併記**
- 個人輸入（米国発送）になることを注意事項に含める
- スカウト定義：`.claude/agents/iherb-scout.md`

---

## オオサカ堂

- 個別商品 URL：`https://osakado.org/products/[ITEM_ID].html`
- 海外医薬品・ジェネリック中心
- **成分・用量の明記必須**
- 在庫状況と発送国を確認
- **個人輸入の注意事項を必ず付記**（厚生労働省ガイドライン、医師指示、
  通関時間、保証限定）
- 本人使用以外の目的（販売・転売）は法令違反
- スカウト定義：`.claude/agents/osakado-scout.md`

---

## Yahoo!ショッピング（中古・並行輸入を含む価格比較に有効）

- 個別商品 URL（形式 1）：`https://store.shopping.yahoo.co.jp/[SHOP]/[ITEM_ID].html`
- 個別商品 URL（形式 2）：`https://shopping.yahoo.co.jp/products/[PRODUCT_ID]`
- 検索結果 URL：`https://shopping.yahoo.co.jp/search?p=...` ← **絶対禁止**
- PayPay ポイント還元率を取得できれば付記
- 「ストア評価」「商品レビュー」を確認
- スカウト定義：`.claude/agents/yahoo-shopping-scout.md`

---

## Yahoo!オークション（中古市場として利用）

- 個別商品 URL：`https://page.auctions.yahoo.co.jp/jp/auction/[ITEM_ID]`
- 検索結果 URL：`https://auctions.yahoo.co.jp/search/search?p=...` ← **絶対禁止**
- 即決価格・現在価格・入札数を取得
- 残り時間と終了済み区分を確認
- スカウト定義：`.claude/agents/yahoo-shopping-scout.md`（共用）

---

## 追加チャネル（ユーザー指示時のみ）

Qoo10 / AliExpress / eBay 等。追加時は同一の 3 ゲート検証ルールを適用。
新規チャネル追加は `/add-channel` スラッシュコマンドを利用すること。
