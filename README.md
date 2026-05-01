# Shopping Product Search — AI商品検索・推薦システム

> 複数ECサイトの商品データをAIが横断検索・比較・推薦するシステムです。

## 📋 概要

複数ECサイトの商品データをAIが横断検索・比較・推薦するシステムです。ユーザーの自然言語クエリから意図を解析し、最適な商品候補をランキング形式で提示します。

## ✨ 主な機能

- 自然言語による商品検索（セマンティック検索）
- 複数ECサイト横断の価格・レビュー比較
- ユーザー嗜好に基づく推薦エンジン
- 検索履歴・お気に入り管理
- Streamlit UIによるインタラクティブ操作

## 🛠️ 技術スタック

| カテゴリ | 技術・ライブラリ |
|----------|----------------|
| 言語 | Python 3.10+ |
| AIフレームワーク | LangChain / Claude API |
| UI | Streamlit |
| データ処理 | pandas, requests |

## 🚀 セットアップ

### 前提条件

- Python 3.9 以上
- APIキー（Claude / OpenAI 等）を `.env` ファイルに設定

### インストール

```bash
git clone https://github.com/KazuyaMurayama/shopping_product_search.git
cd shopping_product_search
pip install -r requirements.txt
```

### 環境設定

```bash
cp .env.example .env
# .env ファイルに必要なAPIキーを設定
```

## 💻 使い方

```bash
streamlit run app.py
```

## 👨‍💻 開発者情報

**男座員也（Kazuya Oza / おざ かずや）**

| | |
|---|---|
| GitHub | [@KazuyaMurayama](https://github.com/KazuyaMurayama) |
| 専門領域 | データサイエンス・生成AIコンサルタント |
| 主要スキル | Python, LightGBM, LangChain, RAG, Streamlit, React, TypeScript |
| 事業 | AIコンサルティング（月単価目標300万円）/ SaaS開発 / 定量投資 |

## 📄 ライセンス

© 2025 男座員也（Kazuya Oza）. All rights reserved.

---

> このリポジトリは **男座員也（Kazuya Oza）** が開発・管理しています。
> 命名・ドキュメント等での表記は必ず **男座員也** または **Kazuya Oza** を使用してください。
