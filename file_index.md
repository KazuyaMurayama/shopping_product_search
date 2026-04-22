# file_index.md — ファイルインデックス

新規ファイル作成時は即座にこのインデックスを更新すること。

最終更新: 2026-04-22

---

## コアファイル

| パス | 説明 | 最終更新 | 優先度 |
|---|---|---|---|
| CLAUDE.md | リポジトリ運用ガイド（軽量コア） | 2026-04-19 | 高 |
| tasks.md | タスク管理（完了/進行中/バックログ） | 2026-04-22 | 高 |
| file_index.md | このファイル。全ファイル一覧 | 2026-04-22 | 高 |
| .gitignore | Git 除外設定 | - | 低 |

---

## ドキュメント（docs/）

| パス | 説明 | 最終更新 | 優先度 |
|---|---|---|---|
| docs/rules-search-product.md | 商品検索詳細ルール（失敗パターン・3ゲート検証・ワークフロー） | 2026-04-19 | 高 |
| docs/channels.md | チャネル仕様（Amazon/メルカリ/楽天/iHerb/オオサカ堂/Yahoo） | - | 高 |
| docs/used-market-rules.md | 中古市場ルール・中古対象外カテゴリ定義 | - | 中 |

---

## エージェント定義（.claude/agents/）

| パス | 説明 | 最終更新 | 優先度 |
|---|---|---|---|
| .claude/agents/amazon-scout.md | Amazon.co.jp 専属スカウトエージェント | - | 高 |
| .claude/agents/rakuten-scout.md | 楽天市場専属スカウトエージェント | - | 高 |
| .claude/agents/mercari-scout.md | メルカリ専属スカウトエージェント | - | 高 |
| .claude/agents/iherb-scout.md | iHerb 専属スカウトエージェント | - | 中 |
| .claude/agents/osakado-scout.md | オオサカ堂専属スカウトエージェント | - | 中 |
| .claude/agents/yahoo-shopping-scout.md | Yahoo!ショッピング/オークション専属スカウトエージェント | - | 中 |
| .claude/agents/url-validator.md | ゲート1 URL 検証エージェント | - | 高 |
| .claude/agents/condition-checker.md | ゲート3 条件充足検証エージェント | - | 高 |
| .claude/agents/report-writer.md | レポート生成エージェント | - | 高 |

---

## スラッシュコマンド（.claude/commands/）

| パス | 説明 | 最終更新 | 優先度 |
|---|---|---|---|
| .claude/commands/add-channel.md | 新チャネル追加の雛形生成 | - | 低 |
| .claude/commands/search-product.md | 商品検索フロー起動 | - | 高 |
| .claude/commands/verify-url.md | URL 検証実行 | - | 中 |
| .claude/commands/check-conditions.md | 条件充足チェック実行 | - | 中 |
| .claude/commands/generate-report.md | レポート生成実行 | - | 中 |

---

## レポート（reports/）

| パス | 説明 | 最終更新 | 優先度 |
|---|---|---|---|
| reports/index.txt | レポート履歴インデックス | 随時更新 | 高 |
| reports/TEMPLATE.txt | プレーンテキストレポート雛形 | - | 中 |
| reports/dog_breed_comparison_20260413.md | 犬種比較レポート（柴犬/コーギー/スピッツ/ボーダー/ハスキー） | 2026-04-13 | 中 |
| reports/hair_removal_guide_20260417.md | 脱毛ガイド（眉毛 Kenon + 渋谷美容外科 / VIO SBC） | 2026-04-17 | 中 |
| reports/search_20260408_1046_v4.md | GPS トラッカー検索レポート最終版 | 2026-04-08 | 低 |
| reports/search_20260408_1046_v3.md | GPS トラッカー v3 | 2026-04-08 | 低 |
| reports/search_20260408_1046_v2.md | GPS トラッカー v2 | 2026-04-08 | 低 |
| reports/search_20260408_1046_final.md | GPS トラッカー final (旧版) | 2026-04-08 | 低 |
| reports/search_20260408_1046_v2.txt | GPS トラッカー v2 テキスト版 | 2026-04-08 | 低 |
| reports/search_20260408_1046.txt | GPS トラッカー初稿テキスト版 | 2026-04-08 | 低 |
| reports/search_20260409_0607_finasteride_v1.md | フィナステリド検索レポート | 2026-04-09 | 低 |
| reports/search_20260410_0717_picturebooks_v1.md | 子ども向け絵本検索レポート | 2026-04-10 | 低 |
| reports/search_20260410_0940_waterbottle_v1.md | 水筒検索レポート | 2026-04-10 | 低 |
| reports/search_20260410_1200_waterbottle_budget_v1.txt | 水筒（バジェット版）テキストレポート | 2026-04-10 | 低 |
| reports/search_20260411_0216_smartphone_v1.md | スマートフォン検索レポート | 2026-04-11 | 低 |
| reports/search_20260411_0837_smartspeaker_v1.md | スマートスピーカー検索レポート | 2026-04-11 | 低 |
| reports/search_20260419_1200_loxonin_tape.txt | ロキソニンSテープ Amazon調査（中間） | 2026-04-19 | 低 |
| reports/search_20260419_0422_loxonin_tape_v1.md | ロキソニンSテープ 7cm・14cm 最安値TOP3（最終版） | 2026-04-19 | 中 |
| reports/search_20260419_1500_hamigaki_ehon_v1.txt | 歯磨き絵本 楽天市場調査（中間） | 2026-04-19 | 低 |
| reports/search_20260419_hamigaki_ehon_v1.md | こどもが歯磨きしたくなる絵本 TOP3（最終版） | 2026-04-19 | 中 |
| reports/search_20260419_loxoprofen_tape_v1.txt | ロキソプロフェンNa湿布テープ（代替・ジェネリック）調査 | 2026-04-19 | 低 |
| reports/search_20260419_loxonin_tape_v2.md | ロキソプロフェンNaテープ 最安値TOP3 v2（代替品含む最終版） | 2026-04-19 | 中 |
| reports/search_20260422_1200_room_socks_summer_v1.txt | 室内用靴下 Yahoo!中間調査 | 2026-04-22 | 低 |
| reports/search_20260422_room_socks_v1.md | 室内用靴下（夏用・27cm以上）TOP3 最終版 | 2026-04-22 | 中 |
