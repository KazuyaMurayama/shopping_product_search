---
description: 新しい EC 媒体を検索対象チャネルとして追加する。URL 形式・禁止パターン・scout サブエージェントの雛形を生成する。
argument-hint: [チャネル名] [個別商品 URL 形式] [禁止パターン]
allowed-tools: Read, Write, Edit
---

# /add-channel

新しい検索対象チャネル（Yahoo!ショッピング / Qoo10 / AliExpress / eBay 等）を
追加する。既存 5 媒体と同じ 3 ゲート検証ルールを適用できる形でセットアップする。

## 引数

$ARGUMENTS

形式（例）：

    channel: yahoo-shopping
    domain: store.shopping.yahoo.co.jp
    product_url_format: https://store.shopping.yahoo.co.jp/[shop]/[item].html
    forbidden_patterns: /search, ?p=, ?query=

## 実行ステップ

1. 引数のパース。不足情報はユーザーに質問する
2. `.claude/agents/[channel]-scout.md` を既存 scout を雛形として生成：
   - `amazon-scout.md` をベースにコピー
   - ドメイン、URL 形式、禁止パターン、抽出ロジックを差し替え
3. `CLAUDE.md` の「対象チャネルと URL 形式」セクションに新チャネルの記述を追加
4. `CLAUDE.md` の禁止 URL パターン例に新チャネルの検索結果 URL 例を追加
5. 生成したファイルをユーザーに提示し、差分を確認してもらう

## 新 scout サブエージェントが満たすべき条件

- `---` フロントマター（name, description, tools）あり
- 担当ドメイン明記
- 個別商品 URL 形式明記
- 禁止パターン明記
- 抽出ロジック説明
- 自己チェックリスト
- 失敗時の振る舞い

## 注意

- 既存のエージェント・コマンドは破壊しない
- CLAUDE.md の編集は該当セクションのみを Edit で変更する
- 追加後の動作確認として、ダミー URL で `/verify-url` を実行することを提案する
