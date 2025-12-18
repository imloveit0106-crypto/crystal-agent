# 🚀 Crystal Agent - FastAPI版 セットアップガイド

## アーキテクチャ概要

```
┌─────────────────────────────────────────┐
│  Frontend (HTML/Tailwind/Vanilla JS)   │
│  frontend/index.html                    │
│  - Apple Quality デザイン               │
│  - Fetch APIでバックエンド通信          │
└──────────────┬──────────────────────────┘
               │ HTTP REST API
               │ (POST /chat, GET /stats)
┌──────────────▼──────────────────────────┐
│  Backend (FastAPI)                      │
│  backend/main.py                        │
│  - Gemini API連携                       │
│  - Notion API連携                       │
│  - RAG（検索拡張生成）機能              │
└─────────────────────────────────────────┘
```

## 🔧 セットアップ手順

### 1. 依存関係のインストール

```bash
# 仮想環境を使用している場合は、まずアクティベート
pip install -r requirements.txt
```

新しく追加されたパッケージ：
- `fastapi>=0.104.0` - 高速なWeb API フレームワーク
- `uvicorn[standard]>=0.24.0` - ASGI サーバー
- `pydantic>=2.5.0` - データバリデーション

### 2. 環境変数の確認

`.env` ファイルに以下が設定されていることを確認：

```env
GEMINI_API_KEY=your_gemini_api_key_here
NOTION_API_KEY=your_notion_api_key_here
NOTION_LIFE_LOG_DB_ID=your_life_log_database_id_here
```

### 3. バックエンドサーバーの起動

```bash
# プロジェクトルートから実行
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

オプション：
- `--reload`: コード変更時に自動再起動
- `--host 0.0.0.0`: すべてのネットワークインターフェースでリッスン
- `--port 8000`: ポート番号（デフォルト）

### 4. ブラウザでフロントエンドを開く

```bash
# frontend/index.html を直接ブラウザで開く
# macOS
open frontend/index.html

# Linux
xdg-open frontend/index.html

# Windows
start frontend/index.html
```

または、お好みのブラウザで `frontend/index.html` を開いてください。

## ✅ 動作確認手順

### Step 1: ヘルスチェック

サーバー起動後、以下のURLにアクセス：

```
http://localhost:8000/
```

期待されるレスポンス：
```json
{
  "status": "ok",
  "app": "Crystal Agent API",
  "gemini": "connected",
  "notion": "connected"
}
```

### Step 2: ターミナルでログ確認

バックエンドのターミナルで以下のログが出力されているか確認：

```
✅ Notion DB接続成功
✅ Gemini API接続成功
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 3: RAG機能の確認

1. ブラウザでチャットにメッセージを送信
2. バックエンドのターミナルで以下のようなログを確認：

```
📊 Notionから 15 件のデータを取得（RAGコンテキスト）
🔍 RAGコンテキスト生成: 523 文字
💾 Notionに保存: 支出 - 今日のランチに1000円使った...
```

**重要**: `🔍 RAGコンテキスト生成` のログが出力されていれば、RAG機能が正常に動作しています。

### Step 4: Notion統合の確認

1. チャットで「今日のランチに1000円使った」と送信
2. Notionの `Life_Log` データベースを確認
3. 新しいエントリーが作成されていることを確認

## 🐛 トラブルシューティング

### エラー: "ModuleNotFoundError: No module named 'fastapi'"

```bash
pip install -r requirements.txt
```

### エラー: "Connection refused"

- バックエンドサーバーが起動しているか確認
- ポート8000が他のアプリケーションで使用されていないか確認

### エラー: "CORS policy"

- `backend/main.py` の CORS設定を確認
- ブラウザの開発者ツールでエラー詳細を確認

### Notionに保存されない

1. `.env` ファイルの `NOTION_API_KEY` と `NOTION_LIFE_LOG_DB_ID` を確認
2. Notion Integrationがデータベースへのアクセス権を持っているか確認
3. バックエンドのログで「Notion DB接続成功」が表示されているか確認

## 📊 API エンドポイント一覧

### `GET /`
ヘルスチェック

### `GET /stats`
Notionから統計データを取得

レスポンス例：
```json
{
  "total": 15,
  "types": {
    "日記": 8,
    "支出": 5,
    "タスク": 2
  },
  "recent": [...],
  "amounts": [1000, 500, 2000]
}
```

### `POST /chat`
チャットメッセージを送信

リクエスト：
```json
{
  "message": "今日のランチに1000円使った",
  "use_rag": true
}
```

レスポンス：
```json
{
  "response": "1000円のランチ、いいですね！美味しかったですか？",
  "detected_type": "支出",
  "detected_amount": 1000.0,
  "saved_to_notion": true,
  "rag_used": true
}
```

## 🎨 フロントエンドの特徴

### Apple Quality デザイン
- **フォント**: -apple-system (San Francisco)
- **カラー**: Apple Blue (#007AFF)
- **アニメーション**: cubic-bezier イージング
- **Frosted Glass**: すりガラス効果

### レスポンシブ
- モバイル、タブレット、デスクトップに対応
- 最大幅1200pxで中央配置

### リアルタイム統計
- 自動的にNotionから統計情報を取得
- チャット後に自動更新

## 🔍 RAG（検索拡張生成）の仕組み

1. **コンテキスト取得**: Notionから過去30日間のデータを取得
2. **コンテキスト構築**: 最新5件のエントリーをプロンプトに追加
3. **AI応答生成**: Geminiがコンテキストを踏まえて回答
4. **保存**: 新しいメッセージをNotionに保存

これにより、AIがユーザーの過去の行動パターンを理解した上で応答できます。

## 🚀 本番環境へのデプロイ

### バックエンド
- Render.com, Railway.app, Google Cloud Run などにデプロイ可能
- 環境変数を適切に設定

### フロントエンド
- Netlify, Vercel, GitHub Pages などにデプロイ可能
- `API_BASE_URL` を本番環境のURLに変更

## 📝 次のステップ

- [ ] 認証機能の追加（JWT等）
- [ ] WebSocket対応（リアルタイムチャット）
- [ ] データベースのページネーション
- [ ] エラーハンドリングの強化
- [ ] テストの追加

---

**Apple Quality基準を維持しながら、必要に応じてデザインを磨き上げてください。** 🍎
