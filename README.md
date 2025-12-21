# Crystal Agent

**AI Personal Assistant with Notion Integration**

Notion/Claude風のミニマルで洗練されたAIアシスタント

![Status](https://img.shields.io/badge/Status-Production-success)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

---

## 📖 概要

Crystal Agentは、日々の行動・思考・目標を記録し、
Google Gemini AIとNotion データベースを連携させることで、
パーソナライズされたサポートを提供するAIアシスタントです。

### ✨ 主な機能

- 💬 **自然な会話**: Gemini 1.5 Flash による高速AI応答
- 📝 **自動分類**: 日記・支出・タスク・メモを自動判定
- 💰 **金額抽出**: テキストから金額を自動で検出
- 🔄 **Notion連携**: すべてのログをNotionに自動保存
- 📊 **統計表示**: Total / Diary / Tasks のカウント
- ⚡ **クイック入力**: ワンクリックで定型文を入力
- 🎨 **ミニマルUI**: Notion/Claudeのような洗練されたデザイン

### 🎯 デザインコンセプト

**"Intellectual Minimalism（知的なミニマリズム）"**

- 白背景・ダークグレー文字のみ
- タイポグラフィ重視
- 絵文字排除、Lucide Iconsのみ使用
- フェード・スライドなど微細なアニメーション

---

## 🛠️ 技術スタック

| 役割 | 技術 | 備考 |
|------|------|------|
| **Backend** | FastAPI + Uvicorn | 高速・モダンなWeb API |
| **Frontend** | HTML + Tailwind CSS (CDN) | ビルド不要 |
| **JavaScript** | Vanilla JS (ES6+) | フレームワーク不使用 |
| **AI** | Google Gemini 1.5 Flash | 高性能・高速 |
| **Database** | Notion API | 柔軟で拡張性が高い |
| **Design** | Lucide Icons (CDN) | 軽量アイコンライブラリ |

---

## 🚀 クイックスタート

### 1. 必要なもの

- Python 3.8以上
- Google Gemini APIキー
- Notion Integration Token + Database ID

### 2. インストール

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/crystal-agent.git
cd crystal-agent

# 環境変数を設定（.envファイルを作成）
cp .env.example .env
# .envを編集してAPIキーを設定
```

### 3. 起動

```bash
# 自動インストール＆起動（推奨）
python start.py

# または手動起動
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. アクセス

ブラウザで `http://localhost:8000` を開く

---

## 📁 プロジェクト構成

```
crystal-agent/
├── backend/
│   └── main.py              # FastAPI サーバー
├── frontend/
│   ├── templates/
│   │   └── index.html       # メインUI
│   └── static/
│       ├── js/
│       │   └── script.js    # フロントエンドロジック
│       └── css/
│           └── style.css    # ミニマルCSS
├── start.py                 # 起動スクリプト
├── requirements.txt         # 依存パッケージ
├── design_doc.md            # 設計仕様書
└── .env                     # 環境変数（要作成）
```

---

## 🎨 UI/UX

### ウェルカムスクリーン（Notion/Claudeスタイル）

- ランダムアートワーク（4種類）
- サジェストチップ（4つ）
  - 家計簿をつける
  - 日記を書く
  - 今日の運勢
  - タスク確認
- メッセージ送信時に自動フェードアウト

### チャットUI

- **ユーザーメッセージ**: 右揃え、黒背景・白文字
- **AIメッセージ**: 左揃え、薄グレー背景・黒文字
- **アバター**: Lucide Iconsの `user` と `sparkles`
- **最大幅**: 75%（可読性重視）

### 統計バー

- Total / Diary / Tasks の3カラム
- リアルタイム更新

---

## ⚙️ 設定

### 環境変数（.env）

```env
GEMINI_API_KEY=your_gemini_api_key
NOTION_API_KEY=your_notion_integration_token
NOTION_LIFE_LOG_DB_ID=your_notion_database_id
```

### Notion データベース構造

以下のプロパティが必要です：

- **タイプ**: Select（日記/タスク/支出/メモ）
- **内容**: Text
- **日付**: Date
- **金額**: Number（オプション）
- **タグ**: Multi-select（オプション）

---

## 📚 ドキュメント

詳細な設計仕様は `design_doc.md` を参照してください。

- プロジェクト概要
- 機能要件（実装する/しない機能）
- 技術スタック
- デザインシステム
- 実装ルール
- 禁止事項

---

## 🤝 コントリビューション

プルリクエストを歓迎します。

大きな変更を行う場合は、まず issue を開いて変更内容を議論してください。

---

## 📄 ライセンス

MIT License

---

## 🙏 謝辞

デザイン参考：

- [Notion](https://notion.so) - ミニマルUI、タイポグラフィ
- [Claude](https://claude.ai) - ウェルカム画面、チャットUI
- [Linear](https://linear.app) - クリーンなデザイン

---

**Made with ❤️ and Minimal Design**
