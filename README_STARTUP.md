# 🚀 Crystal Agent - 起動ガイド

このドキュメントでは、Crystal Agentをローカル環境で起動する方法を説明します。

---

## 📋 必要な環境

- **Python 3.8以上**
- **インターネット接続**（初回のみ、パッケージインストールに必要）

---

## ⚡ クイックスタート（3つの方法）

### 🪟 方法1: Windows - バッチファイルで起動（最も簡単！）

プロジェクトフォルダ内の **`start.bat`** をダブルクリックするだけ！

**または、コマンドプロンプト/PowerShellで:**
```cmd
start.bat
```

### 🐍 方法2: Python - 自動起動スクリプト（推奨）

**Windows/Mac/Linux すべてで動作:**
```bash
python start.py
```

**または:**
```bash
py start.py       # Windowsでpythonコマンドが使えない場合
python3 start.py  # Mac/Linuxの場合
```

### 🔧 方法3: 手動起動（開発者向け）

```bash
# 必要なパッケージをインストール
pip install -r requirements.txt

# サーバーを起動
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🌐 起動後のアクセス

サーバーが起動したら、ブラウザで以下のURLを開いてください:

| URL | 説明 |
|-----|------|
| **http://localhost:8000** | メインアプリ（次世代OS級UI） |
| http://localhost:8000/health | ヘルスチェック |
| http://localhost:8000/stats | 統計API |

---

## 🔑 環境変数の設定（オプション）

フル機能を使用するには、プロジェクトルートに **`.env`** ファイルを作成してください。

### `.env` ファイルの例:
```env
GEMINI_API_KEY=your_gemini_api_key_here
NOTION_API_KEY=your_notion_integration_key
NOTION_LIFE_LOG_DB_ID=your_notion_database_id
```

`.env.example` ファイルを参考にしてください。

---

## 🛑 サーバーの停止方法

**ターミナル/コマンドプロンプトで:**
```
Ctrl + C
```

---

## 🐛 トラブルシューティング

### ❌ `python` コマンドが見つからない

**Windows:**
- `py start.py` を試してください
- または、Pythonをインストール: https://www.python.org/downloads/

**Mac/Linux:**
- `python3 start.py` を試してください

### ❌ ポート8000が既に使用中

別のポートで起動してください:
```bash
python -m uvicorn backend.main:app --reload --port 8001
```

その後、http://localhost:8001 にアクセス

### ❌ モジュールが見つからない (ModuleNotFoundError)

必要なパッケージを手動でインストール:
```bash
pip install fastapi uvicorn python-dotenv google-generativeai notion-client pydantic
```

または:
```bash
pip install -r requirements.txt
```

### ❌ `.env` ファイルがない警告

- 警告が出ても起動は可能です
- フル機能を使うには `.env` ファイルを作成してください

---

## 📦 自動起動スクリプト（start.py）の機能

`start.py` は以下を自動的に実行します:

1. ✅ Pythonバージョンチェック（3.8以上必要）
2. ✅ 不足しているパッケージを自動インストール
3. ✅ `.env` ファイルの存在確認
4. ✅ FastAPIサーバーを起動（ホットリロード有効）

---

## 🎨 次世代OS級UIの特徴

起動後、以下の機能が体験できます:

- 🌌 **3層レイヤーアーキテクチャ** - 奥行きのある空間設計
- 🎨 **Apple標準デザインシステム** - 物理的な慣性運動
- ⚡ **マイクロインタラクション** - すべてのUIに弾力
- 🛸 **フローティングHUD** - ノイズテクスチャ付きガラス
- 💎 **Crystal Status Card** - SF映画級ホログラムUI

---

## 📞 サポート

問題が解決しない場合は、GitHubのIssuesで報告してください。

---

**🎉 Enjoy Crystal Agent!**
