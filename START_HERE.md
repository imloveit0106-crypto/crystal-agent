# 🚀 Crystal Agent - クイックスタートガイド

## Cursorでテストする方法

### 1️⃣ サーバーを起動

Cursorのターミナルで以下のコマンドを実行：

```bash
cd crystal-agent-main
python backend/main.py
```

### 2️⃣ ブラウザでアクセス

サーバーが起動したら、ブラウザで以下を開く：

```
http://localhost:8000
```

### 3️⃣ Zero Latency UXをテスト

チャット画面で以下を試してください：

✨ **即座のフィードバック**
- メッセージを入力して送信
- ユーザーメッセージが**瞬時に**表示される（スライドアップアニメーション）
- 入力フィールドが**即座に**クリアされる
- すぐに次のメッセージを入力可能

🔮 **AIストリーミング**
- AIの応答がリアルタイムでタイプされる
- Markdownとコードハイライトが動作

🍞 **エラートースト**
- エラー時に画面下部に赤いトースト通知
- 3秒後に自動消去

---

## 📁 重要なファイル

### フロントエンド（Zero Latency UX実装）
- **HTML**: `crystal-agent-main/frontend/templates/index.html`
- **JavaScript**: `crystal-agent-main/frontend/static/js/chat.js`
- **CSS**: `crystal-agent-main/frontend/static/css/style.css`

### バックエンド（ストリーミング＋会話履歴）
- **FastAPI**: `crystal-agent-main/backend/main.py`
- **AI Brain**: `crystal-agent-main/utils/ai_brain.py`

---

## 🔧 環境設定

環境変数が必要な場合は `.env` ファイルを作成：

```bash
cd crystal-agent-main
cp .env.example .env
```

`.env` ファイルを編集してAPIキーを設定：
```
GEMINI_API_KEY=your_api_key_here
NOTION_API_KEY=your_notion_key_here
```

---

## ❓ トラブルシューティング

### ポート8000が使用中の場合
```bash
# 既存のプロセスを停止
pkill -f "python.*backend/main.py"
```

### 依存関係のインストール
```bash
cd crystal-agent-main
pip install -r requirements.txt
```

---

## ✨ 実装された新機能

### 1. Zero Latency UX（最新）
- オプティミスティックUI更新
- 即座の入力クリア＆フォーカス復帰
- エラートースト通知
- スムーズなアニメーション

### 2. 会話履歴バッファ
- 最新5ターンの会話を記憶
- コンテキスト保持で自然な対話

### 3. リアルタイムストリーミング
- Server-Sent Events（SSE）
- Markdownレンダリング
- コードシンタックスハイライト

---

## 📊 ディレクトリ構造

```
crystal-agent-main/
├── backend/
│   ├── main.py              # FastAPI サーバー（SSE + 会話履歴）
│   └── services/
├── frontend/
│   ├── templates/
│   │   └── index.html       # メインHTML
│   └── static/
│       ├── js/
│       │   └── chat.js      # Zero Latency UX実装
│       └── css/
│           └── style.css    # アニメーション＆トースト
├── utils/
│   ├── ai_brain.py          # Gemini AI（会話履歴対応）
│   ├── text_analyzer.py
│   ├── local_storage.py
│   └── context_engine.py
├── config/
│   └── settings.py
└── requirements.txt
```

---

## 🎯 次のステップ

1. サーバーを起動
2. ブラウザで `http://localhost:8000` にアクセス
3. チャットを試して Zero Latency UX を体験！

Enjoy! 🔮✨
