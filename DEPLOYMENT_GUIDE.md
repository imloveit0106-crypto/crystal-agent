# 🚀 Streamlit Cloud デプロイガイド

## セキュリティ確認済み ✅
- APIキーはGit履歴に含まれていません
- .envファイルは完全に除外されています
- デプロイ可能な状態です

## デプロイ手順

### 1. GitHub準備
```bash
# ブランチをメインにマージ（GitHub上でPRを作成）
1. GitHub で Pull Request を作成
2. claude/crystal-agent-setup-XXnVM → main
3. レビュー後にマージ
```

### 2. Streamlit Cloud設定

#### 2.1 サインアップ
- https://share.streamlit.io/ にアクセス
- GitHubアカウントでサインイン

#### 2.2 アプリをデプロイ
1. "New app" をクリック
2. 設定:
   - **Repository**: `imloveit0106-crypto/crystal-agent`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. "Advanced settings" をクリック
4. **Python version**: 3.10 以上

#### 2.3 Secrets 設定（重要！）
"Advanced settings" → "Secrets" に以下を追加:

```toml
GEMINI_API_KEY = "your_actual_gemini_key_here"
NOTION_API_KEY = "your_actual_notion_key_here"
NOTION_LIFE_LOG_DB_ID = "your_actual_database_id_here"
```

⚠️ **注意**: 必ず実際のAPIキーに置き換えてください

5. "Deploy!" をクリック

### 3. 動作確認

デプロイ後、以下を確認:
- ✅ アプリが起動する
- ✅ サイドバーに "✅ Gemini AI: 接続OK" と表示
- ✅ サイドバーに "✅ Notion DB: 接続OK" と表示
- ✅ チャットでメッセージ送信が可能
- ✅ Notionにデータが保存される
- ✅ 統計グラフが表示される

## トラブルシューティング

### エラー: "ModuleNotFoundError"
- requirements.txt が正しくコミットされているか確認
- Streamlit Cloud でアプリを再起動

### エラー: "Notion DB: 未接続"
- Secrets の `NOTION_API_KEY` と `NOTION_LIFE_LOG_DB_ID` を確認
- Notion Integration がデータベースにアクセス権限を持っているか確認

### エラー: "Gemini APIエラー"
- Secrets の `GEMINI_API_KEY` を確認
- APIキーが有効か確認: https://aistudio.google.com/api-keys

## 無料プランの制限

Streamlit Cloud 無料プランの制限:
- ✅ 1つのプライベートアプリ
- ✅ 無制限のパブリックアプリ
- ✅ 1GB メモリ
- ✅ 1 CPU

Crystal Agent は無料プランで十分動作します！

## 次のステップ

デプロイが成功したら:
1. 📱 スマホからアクセスしてUIを確認
2. 💬 いくつかメッセージを送信してテスト
3. 📊 Notionで統計データを確認
4. 🎉 完成！

## サポート

問題が発生した場合:
- Streamlit Cloud のログを確認
- GitHub Issues で報告
- docs/SETUP.md を参照
