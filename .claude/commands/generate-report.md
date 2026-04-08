---
description: スカウト・検証済みの候補情報から最終レポートを生成し、reports/ に保存する
argument-hint: [検索メタ情報と候補リスト]
allowed-tools: Task, Read, Write, Bash
---

# /generate-report

レポート生成のスタンドアロン実行。`report-writer` サブエージェントを呼び、
プレーンテキストの表形式レポートを `reports/search_YYYYMMDD_HHMM.txt` に保存する。

## 引数

$ARGUMENTS

以下の情報を含めること：

    [検索条件]
      商品: ...
      必須条件: ...
      予算: ...
      対象チャネル: ...

    [推奨TOP3候補]（全ゲート通過品のみ）
      1. ...
      2. ...
      3. ...

    [全候補一覧]
      ...

    [選外商品と理由]
      ...

## 実行ステップ

1. 引数をパース
2. 現在日時を `date +%Y%m%d_%H%M` で取得
3. report-writer サブエージェントを呼び出し、レポート本文を生成
4. `reports/search_YYYYMMDD_HHMM.txt` に保存
5. `reports/index.txt` に履歴 1 行追記
6. 保存パスをユーザーに提示

## 出力禁止事項

- Markdown 記号（`#`, `*`, `[]()`, バッククォート等）
- 検索結果 URL の掲載
- 推測での掲載
