# file_index.md — ファイルインデックス

新規ファイル作成時は即座にこのインデックスを更新すること。

最終更新: 2026-06-09

---

## コアファイル

| パス | 説明 | 最終更新 | 優先度 |
|---|---|---|---|
| CLAUDE.md | リポジトリ運用ガイド（軽量コア） | 2026-04-19 | 高 |
| tasks.md | タスク管理（完了/進行中/バックログ） | 2026-06-09 | 高 |
| file_index.md | このファイル。全ファイル一覧 | 2026-06-09 | 高 |
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
| reports/index.txt | レポート履歴インデックス | 2026-06-09 | 高 |
| reports/TEMPLATE.txt | プレーンテキストレポート雛形 | - | 中 |
| reports/dog_breed_comparison_20260413.md | 犬種比較レポート（柴犬/コーギー/スピッツ/ボーダー/ハスキー） | 2026-04-13 | 中 |
| reports/hair_removal_guide_20260417.md | 脱毛ガイド（眉毛 Kenon + 渋谷美容外科 / VIO SBC） | 2026-04-17 | 中 |
| reports/search_20260408_1046_v4.md | GPS トラッカー検索レポート最終版 | 2026-04-08 | 低 |
| reports/search_20260409_0607_finasteride_v1.md | フィナステリド検索レポート | 2026-04-09 | 低 |
| reports/search_20260410_0717_picturebooks_v1.md | 子ども向け絵本検索レポート | 2026-04-10 | 低 |
| reports/search_20260410_0940_waterbottle_v1.md | 水筒検索レポート | 2026-04-10 | 低 |
| reports/search_20260410_1200_waterbottle_budget_v1.txt | 水筒（バジェット版）テキストレポート | 2026-04-10 | 低 |
| reports/search_20260411_0216_smartphone_v1.md | スマートフォン検索レポート | 2026-04-11 | 低 |
| reports/search_20260411_0837_smartspeaker_v1.md | スマートスピーカー検索レポート | 2026-04-11 | 低 |
| reports/search_20260419_0422_loxonin_tape_v1.md | ロキソニンSテープ 7cm・14cm 最安値TOP3（最終版） | 2026-04-19 | 中 |
| reports/search_20260419_hamigaki_ehon_v1.md | こどもが歯磨きしたくなる絵本 TOP3（最終版） | 2026-04-19 | 中 |
| reports/search_20260419_loxonin_tape_v2.md | ロキソプロフェンNaテープ 最安値TOP3 v2（代替品含む最終版） | 2026-04-19 | 中 |
| reports/search_20260422_room_socks_v1.md | 室内用靴下（夏用・27cm以上）TOP3 最終版 | 2026-04-22 | 中 |
| reports/search_20260426_turtleneck_pocket_v1.md | メンズ タートルネック/ハイネック/モックネック ロングTシャツ 胸ポケット付き TOP3 最終版（3チャネル） | 2026-04-26 | 高 |
| reports/search_20260427_projector_smartphone_v1.md | スマートフォン接続対応 小型プロジェクター TOP3 最終版（Yahoo!+楽天+Amazon 3チャネル） | 2026-04-27 | 高 |
| reports/research_20260428_rakuten_fake_reviews_v1.md | 楽天市場偽レビュー・サクラレビュー実態調査 | 2026-04-28 | 高 |
| reports/research_20260428_fake_reviews_yahoo_ec.txt | Yahoo!ショッピング偽レビュー実態・消費者庁ECサイト横断調査 | 2026-04-28 | 高 |
| reports/research_20260428_fake_reviews_ec_comparison_v1.md | ECサイト別偽レビュー実態比較 最終版 | 2026-04-28 | 高 |
| reports/search_20260428_projector_sakura_v2.md | スマートフォン接続対応 小型プロジェクター TOP3 v2（Amazon・サクラ合格限定） | 2026-04-28 | 高 |
| reports/search_20260506_uv_face_cover_parka_v1.md | UVカット・フェイスカバー付き・接触冷感パーカー TOP3 最終版（楽天+Yahoo!+Amazon 3チャネル） | 2026-05-06 | 高 |
| reports/search_20260517_pet_deodorizer_v1.md | 犬のうんち臭対策 ゴミ箱・消臭グッズ TOP3 最終版（楽天+Yahoo!+Amazon 3チャネル） | 2026-05-17 | 高 |
| reports/search_20260518_usb_earphone_meeting_v1.md | Windows PC用 USB/USB-C 接続イヤホン TOP3 最終版（楽天+Yahoo!+Amazon 3チャネル） | 2026-05-18 | 高 |
| reports/search_20260518_2200_socks_grey_v2.md | メンズ靴下 グレー無地・27-29cm・ハーフ丈・口ゆったり 改訂版 v2 最終版（楽天+Yahoo!+Amazon 3チャネル・TOP5） | 2026-05-18 | 高 |
| reports/search_20260519_notebook_pc_v1.md | カフェ作業用 軽量ノートPC TOP3 最終版（楽天+Yahoo!+Amazon 3チャネル横断）v1 | 2026-05-19 | 高 |
| reports/search_20260522_1000_mens_waterrepellent_uv_parka_v1.txt | メンズ 撥水・UVカット パーカー TOP3（Amazon.co.jp 専属・サクラチェッカー検証済み） | 2026-05-22 | 高 |
| reports/search_20260522_1000_mens_waterrepellent_uv_parka_rakuten_v1.txt | メンズ 撥水・UVカット パーカー 楽天市場専属調査 v1 | 2026-05-22 | 高 |
| reports/search_20260522_1000_mens_waterrepellent_uv_parka_yahoo_v1.txt | メンズ 撥水・UVカット パーカー Yahoo!ショッピング専属調査 v1 | 2026-05-22 | 高 |
| reports/search_20260522_mens_waterrepellent_uv_parka_v1.md | メンズ 撥水・UVカット パーカー TOP3 最終版（Amazon+楽天+Yahoo! 3チャネル横断）v1 | 2026-05-22 | 高 |
| reports/research_20260531_movicol_otc_alternatives_v1.md | モビコール・類似品 処方なし入手方法 調査レポート v1（OTC代替・オンライン診療・iHerb MiraLax・個人輸入代行 4ルート比較） | 2026-05-31 | 高 |
| reports/search_20260604_1200_lactobacillus_highcfu_v1.txt | 乳酸菌サプリ 高菌数（1,000億CFU以上）Amazon.co.jp 専属調査 v1（TOP3+参考候補・サクラ除外4件） | 2026-06-04 | 高 |
| reports/search_20260604_1200_probiotic_high_cfu_v1.txt | 楽天市場 乳酸菌サプリ 高菌数（1,000億CFU以上）調査 TOP3+参考3件 v1 | 2026-06-04 | 高 |
| reports/search_20260604_lactobacillus_1000billion_final.md | 乳酸菌 1日1,000億個 コスパ最強 最終版（Amazon/楽天/iHerb/市販品 全チャネル横断・ピルクル含む） | 2026-06-04 | 中 |
| reports/search_20260604_lactobacillus_1000billion_final-v2.md | 乳酸菌 1日1,000億個 コスパ最強 改訂版 v2（ファクトチェック反映・生菌CFU/死菌2軸・Yahoo!追加・mermaid図＋付録:科学的エビデンス[効果量/有効用量/効果発現期間/安全性・論文22本] | 2026-06-04 | 高 |
| reports/research_20260604_cooling_wear_womens_v1.md | 気温35度の屋外で涼しく過ごすウェア・装備 総合リサーチ（女性向け）— 科学的指標定義・6カテゴリ横断比較 | 2026-06-04 | 高 |
| reports/research_20260604_cooling_wear_womens_v2.md | 同上 v2 — ファクトチェック追加・GU/しまむら/ミズノ/デサント/アームカバー/冷感スプレー新収録・優先順位付きランキング | 2026-06-04 | 高 |
| reports/research_20260604_cooling_wear_womens_v3.md | 同上【決定版v3】— 科学的根拠で評価軸再設計（輻射遮断/蒸発主軸）・日傘新規追加・加重スコアリング・品質レビュー済 | 2026-06-04 | 高 |
| reports/search_20260607_3wheel_ebike_child2_v1.md | 3輪・4輪 子ども2人乗せ電動アシスト自転車 調査レポート v1（⚠️ bikke POLAR e 3輪誤記あり・v2で修正済み） | 2026-06-07 | 低 |
| reports/search_20260607_3wheel_ebike_child2_v2.md | 3輪・4輪 子ども2人乗せ電動アシスト自転車 調査レポート v2【正式版】（v1修正・商品リンク列追加・3輪唯一品＝ふたごじてんしゃアシスト確定・ギュット比較スコア100点） | 2026-06-08 | 高 |
| reports/search_20260608_1400_wood_round_rod_v1.txt | 木の丸棒（長さ120〜140cm・直径10〜30mm・木製・¥5,000以下）Amazon.co.jp 専属調査 v1（確認済み1件・注意フラグ1件・3件目なし） | 2026-06-08 | 高 |
| reports/search_20260608_childseat_cushion_v1.md | 自転車チャイルドシート用 振動吸収クッション 調査レポート v1（3チャネル横断・段差衝撃吸収・LABOCLE GEL+/MARUTO CCK-Y02/socca CSC-SA02 TOP3） | 2026-06-08 | 高 |
| reports/search_20260608_wood_round_rod_v1.md | 木の丸棒 最終版 v1（Amazon+楽天+Yahoo! 3チャネル横断・TOP3確定：Yahoo!¥1,885/Amazon¥2,020/楽天¥410〜+カット） | 2026-06-08 | 高 |
| reports/search_20260609_1000_tsuppari_bo_v1.txt | つっぱり棒 Amazon.co.jp 専属調査 中間ファイル（NSW-5¥793確認済み） | 2026-06-09 | 中 |
| reports/search_20260609_wood_rod_tsuppari_v1.md | 木の丸棒+つっぱり棒 4本¥4,000以内 最終版 v1（2ルート横断・予算再検索） | 2026-06-09 | 高 |
| reports/search_20260617_voice_to_text_tools_v1.md | 音声テキスト変換ツール 比較調査レポート v1（PC+iPhone両対応・日本語精度重視・Typeless/AquaVoice/Notta/MacWhisper/Google Docs/Apple標準 6ツール100点スコア比較） | 2026-06-17 | 高 |
| reports/search_20260620_cordless_vacuum_v1.md | コードレス掃除機 比較調査レポート v1（ダイソン除く・5年耐久・メンテ重視・Shark BOOST+/マキタCL182/日立PV-BH900SL/CL107/Shark NEO II 5製品100点スコア比較） | 2026-06-20 | 高 |
| reports/search_20260620_cordless_vacuum_v2.md | コードレス掃除機 比較調査レポート v2（v1配点改訂・第⑤軸をトータルコスト25点に再定義/性能二重評価を排除・マキタCL107首位/マキタCL182/Shark NEO II TOP3・6製品100点スコア比較） | 2026-06-20 | 高 |
| reports/search_20260621_cordless_vacuum.md | コードレス掃除機 比較調査レポート【最終版】（ダイソン除く・ファクトチェック済・トータルコスト25点配点・マキタCL107/CL182/SharkBOOST+ TOP3・Shark NEO II SOLD OUT確認・全6製品100点スコア） | 2026-06-21 | 高 |
| reports/search_20260621_cordless_vacuum-v2.md | コードレス掃除機 市場全体スキャン比較レポート v2【最終版】（日本市場網羅スキャン・14製品100点スコア・Roborock H5/マキタCL107/Dreame X1 Slim TOP3・除外製品15社網羅） | 2026-06-21 | 高 |
| reports/search_20260621_cordless_vacuum-v3.md | コードレス掃除機 市場全体スキャン比較レポート【最終版】（日本市場14製品100点スコア・商品リンク付き・Roborock H5/マキタCL107/Dreame X1 Slim TOP3・除外製品16件明記） | 2026-06-22 | 高 |
| reports/search_20260623_whey_protein_yogurt.md | ホエイプロテイン ヨーグルト味 比較レポート【最終版】（Amazon・楽天・Yahoo横断・12製品100点スコア・ザプロ/REYS/エクスプロージョン/ビーレジェンド TOP5・ザバス製造終了確認・iHerb廃番） | 2026-06-24 | 高 |

<!-- ブランチマージで追加 2026-05-11 -->
- reports/search_20260507_1200_triple_combo_skincare_v1.md
- reports/search_20260508_1200_diclofenac_topical_costcomp_v1.md
