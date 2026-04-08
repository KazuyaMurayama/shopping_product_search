---
description: 提示された URL が各チャネルの個別商品ページ形式か、検索結果 URL を含まないかを厳格に検証する
argument-hint: [URL またはチャネル名: URL のリスト]
allowed-tools: Task, Read
---

# /verify-url

URL 検証のスタンドアロン実行。`url-validator` サブエージェントに渡して
3 ゲート検証のゲート 1 のみを実行する。

## 引数

$ARGUMENTS

形式：

    amazon: https://www.amazon.co.jp/dp/B0XXXXXXXX
    rakuten: https://item.rakuten.co.jp/shop/item/
    mercari: https://jp.mercari.com/item/m1234567890
    iherb: https://jp.iherb.com/pr/example-12345
    osakado: https://osakado.org/products/12345.html

## 判定ルール（要約）

url-validator サブエージェントが以下を厳格適用：

- 禁止パターン（1 つでも含めば即 FAIL）：
  `/search`, `?k=`, `?s=`, `?q=`, `?kw=`, `?keyword=`, `/s?`,
  `search.rakuten.co.jp`
- 各チャネルの個別商品 URL 形式に合致すること
- Amazon の ASIN は英数字 10 文字厳守

## 出力

判定結果リスト：

    [URL]
      判定: PASS / FAIL
      理由: [詳細]

## タスク実行

url-validator サブエージェントを Task ツールで呼び出し、
結果をそのままユーザーに提示する。
