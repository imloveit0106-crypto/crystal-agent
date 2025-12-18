# 🔮 Crystal Agent

**あなた専用のマルチモーダルAIエージェント**

Python + Gemini + Notion で作る、パーソナライズされたAI秘書

![Status](https://img.shields.io/badge/Status-Prototype-yellow)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 概要

Crystal Agent は、あなたの日々の行動・思考・目標を記録し、
Gemini AI と Notion データベースを連携させることで、
パーソナライズされたアドバイスを提供するAIエージェントです。

### ✨ 主な機能

- 💬 **自然な会話インターフェース**: LINE風のモダンなチャットUI
- 📝 **自動分類ログ**: 日記・支出・タスク・悩みを自動判定
- 🧠 **パーソナライズAI**: あなたの過去データから最適な助言
- 📊 **データ可視化**: 統計情報・進捗管理
- 🔄 **Notion連携**: データは全てNotionに自動保存

### 🎯 こんな方におすすめ

- 📔 日記を続けたいけど、三日坊主になってしまう
- 💰 支出を管理したいけど、家計簿アプリは面倒
- ✅ タスクを忘れがち
- 🤔 悩みを整理したい
- 🚀 自己成長を記録したい

---

## 🛠️ 技術スタック

| 役割 | 技術 | 理由 |
|------|------|------|
| **言語** | Python 3.10+ | シンプルで初心者にも優しい |
| **UI** | Streamlit | コード数行で美しいUIが作れる |
| **AI** | Google Gemini 1.5 Flash | 高性能で無料枠が大きい |
| **DB** | Notion API | 柔軟で拡張性が高い |
| **環境管理** | python-dotenv | APIキーを安全に管理 |

---

## 🚀 クイックスタート

### 必要要件

- Python 3.10 以上
- インターネット接続
- Gemini API Key（無料）
- Notion API Key（無料）

### 5分で始める！

```bash
# 1. リポジトリをクローン
git clone https://github.com/imloveit0106-crypto/crystal-agent.git
cd crystal-agent

# 2. ライブラリをインストール
pip install -r requirements.txt

# 3. 環境変数ファイルを作成
cp .env.example .env

# 4. .env ファイルを編集（後述）
# エディタで .env を開いて、APIキーを入力

# 5. API接続テスト
python test_api.py

# 6. アプリを起動！
streamlit run app.py
```

ブラウザで `http://localhost:8501` を開く → **完了！** 🎉

---

## 🔑 APIキーの取得方法

### 1️⃣ Gemini API Key（所要時間: 2分）

1. [Google AI Studio](https://aistudio.google.com/api-keys) にアクセス
2. Googleアカウントでログイン
3. 「Get API Key」→「Create API Key」をクリック
4. 生成されたキーをコピー
5. `.env` ファイルの `GEMINI_API_KEY=` の後に貼り付け

**無料枠**: 1日あたり1,500リクエスト（個人利用なら十分！）

### 2️⃣ Notion API Key（所要時間: 3分）

1. [Notion Integrations](https://www.notion.so/my-integrations) にアクセス
2. 「+ New integration」をクリック
3. 名前を「**Crystal Agent**」に設定
4. 「Submit」をクリック
5. 「Internal Integration Token」をコピー
6. `.env` ファイルの `NOTION_API_KEY=` の後に貼り付け

### 3️⃣ Notion データベース作成（所要時間: 5分）

#### データベース1: User Profile（あなたの基本情報）

1. Notionで新しいページを作成
2. `/database` と入力して「Table Database」を選択
3. タイトルを「**User_Profile**」に変更
4. 以下のプロパティを追加:
   - `Name`（テキスト）: あなたの名前
   - `Age`（数値）: 年齢
   - `Goals`（テキスト）: 目標
   - `Values`（テキスト）: 大切にしていること

5. データベースページで右上の「**...**」→「**Add connections**」→「**Crystal Agent**」を選択
6. URLから32文字のIDをコピー（例: `https://notion.so/xxxxx?v=yyyyy` の `xxxxx` 部分）
7. `.env` ファイルの `NOTION_USER_PROFILE_DB_ID=` の後に貼り付け

#### データベース2: Life Log（日々の行動ログ）

1. Notionで新しいページを作成
2. `/database` と入力して「Table Database」を選択
3. タイトルを「**Life_Log**」に変更
4. 以下のプロパティを追加:
   - `Date`（日付）: 日付
   - `Type`（セレクト）: 日記/支出/タスク/悩み
   - `Content`（テキスト）: 内容
   - `Amount`（数値）: 金額（支出の場合）
   - `Status`（セレクト）: 完了/未完了

5. データベースページで右上の「**...**」→「**Add connections**」→「**Crystal Agent**」を選択
6. URLから32文字のIDをコピー
7. `.env` ファイルの `NOTION_LIFE_LOG_DB_ID=` の後に貼り付け

### ✅ .env ファイルの完成例

```env
GEMINI_API_KEY=AIzaSyABC123...（あなたのキー）
NOTION_API_KEY=secret_ABC123...（あなたのキー）
NOTION_USER_PROFILE_DB_ID=abc123def456...（32文字）
NOTION_LIFE_LOG_DB_ID=xyz789ghi012...（32文字）
```

---

## 📱 使い方

### Streamlit版（推奨）- イケてるUI ✨

```bash
streamlit run app.py
```

**特徴:**
- 📱 LINE風のモダンなチャットUI
- 📊 リアルタイム統計表示
- ⚡ クイックアクションボタン
- 🎨 グラデーション背景

**使い方:**
1. メッセージを入力して送信
2. サイドバーのクイックアクションを使用
3. 統計情報を確認

### ターミナル版 - シンプル 💻

```bash
python simple_agent.py
```

**特徴:**
- 🖥️ コマンドラインで動作
- 🚀 軽量・高速
- 📝 シンプルな対話

**使い方:**
1. メッセージを入力してEnter
2. `help` でヘルプ表示
3. `quit` で終了

---

## 📁 プロジェクト構成

```
crystal-agent/
├── app.py                          # 🎨 Streamlit UI（メインアプリ）
├── simple_agent.py                 # 💻 ターミナル版
├── test_api.py                     # 🧪 API接続テスト
├── requirements.txt                # 📦 必要なライブラリ
├── .env.example                    # 🔑 環境変数テンプレート
├── .env                            # 🔒 環境変数（自分で作成）
├── .gitignore                      # 🚫 Git除外設定
├── README.md                       # 📖 このファイル
└── Crystal_Agent_完全版設計書_v2.md # 📚 詳細設計書
```

---

## 🎯 開発ロードマップ

### Phase 0: 事前準備 ✅
- ✅ APIキー取得
- ✅ Notion DB作成
- ✅ プロジェクト構造設計

### Phase 1: プロトタイプ ✅
- ✅ UI作成（Streamlit）
- ✅ モックデータで動作確認
- ✅ GitHub セットアップ

### Phase 2: 基本機能（進行中 🚧）
- ⏳ Gemini API 接続
- ⏳ Notion API 接続
- ⏳ 自動分類機能
- ⏳ データ保存機能

### Phase 3: 高度な機能（予定 📅）
- ⏳ コンテキスト検索
- ⏳ パーソナライズ助言
- ⏳ データ分析・可視化
- ⏳ 週次・月次レポート

### Phase 4: 最適化（予定 🚀）
- ⏳ パフォーマンス改善
- ⏳ UI/UX向上
- ⏳ モバイル対応

---

## 🐛 トラブルシューティング

### ❌ Gemini接続失敗: 403 Forbidden

**原因**: APIキーが無効または未設定

**解決策**:
```bash
# 1. APIキーを再確認
cat .env | grep GEMINI_API_KEY

# 2. キーが正しいか確認（Google AI Studioで再生成）

# 3. テストを再実行
python test_api.py
```

### ❌ Notion接続失敗: 403 Forbidden

**原因**: Integrationの権限がない

**解決策**:
1. Notionデータベースを開く
2. 右上の「...」→「Add connections」→「Crystal Agent」を選択
3. テストを再実行

### ❌ ModuleNotFoundError: No module named 'streamlit'

**原因**: ライブラリがインストールされていない

**解決策**:
```bash
# 仮想環境を使用（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# ライブラリをインストール
pip install -r requirements.txt
```

### ❌ Streamlitが起動しない

**原因**: ポートが使用中

**解決策**:
```bash
# 別のポートで起動
streamlit run app.py --server.port 8502
```

---

## 💡 よくある質問（FAQ）

### Q1: APIキーは有料ですか？

**A**: いいえ、どちらも無料枠があります！
- **Gemini**: 1日1,500リクエスト（個人利用なら十分）
- **Notion**: 無制限（API利用は無料）

### Q2: データはどこに保存されますか？

**A**: すべてあなたのNotion Workspaceに保存されます。外部サーバーには保存されません。

### Q3: プログラミング初心者でも使えますか？

**A**: はい！このREADMEの手順通りに進めれば、初心者でも5-10分で起動できます。

### Q4: スマホで使えますか？

**A**: Streamlit版はスマホブラウザでも表示できますが、PCでの利用を推奨します。

### Q5: カスタマイズできますか？

**A**: はい！Pythonコードを編集すれば、自由にカスタマイズできます。

---

## 🤝 コントリビューション

プルリクエスト大歓迎です！

1. このリポジトリをフォーク
2. 新しいブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを作成

---

## 📝 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照

---

## 👤 作者

**ゆうや**

- GitHub: [@imloveit0106-crypto](https://github.com/imloveit0106-crypto)
- プロジェクト: Crystal Agent
- Email: your-email@example.com（オプション）

---

## 🙏 謝辞

このプロジェクトは以下の素晴らしい技術で作られています：

- [Streamlit](https://streamlit.io/) - 美しいUIフレームワーク
- [Google Gemini](https://ai.google.dev/) - 高性能AIモデル
- [Notion](https://www.notion.so/) - 柔軟なデータベース
- Python コミュニティの皆様

---

## 🎬 次のステップ

1. ✅ セットアップを完了させる
2. 📝 毎日ログを記録する習慣をつける
3. 📊 1週間後に統計データを確認
4. 🚀 自分好みにカスタマイズ
5. 🌟 友達にシェア！

---

**Crystal Agent で、あなたの人生を整理しましょう！** 🚀

質問や問題があれば、[Issues](https://github.com/imloveit0106-crypto/crystal-agent/issues) で報告してください。

---

<div align="center">

Made with ❤️ by Crystal Agent Team

[⭐ Star this repo](https://github.com/imloveit0106-crypto/crystal-agent) | [🐛 Report Bug](https://github.com/imloveit0106-crypto/crystal-agent/issues) | [💡 Request Feature](https://github.com/imloveit0106-crypto/crystal-agent/issues)

</div>
