# Changelog

All notable changes to Crystal Agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.2.0] - 2025-12-18

### ✨ Added
- **AIプロンプト強化**: Crystal Agentの詳細なシステムプロンプトを実装
  - 親しみやすい友達のような口調（「〜だよ」「〜だね」）
  - 適度な絵文字使用（😊✨💪など）
  - 2-3文程度の簡潔な応答
  - ユーザーの気持ちに寄り添う共感的な対話

- **テキスト分析大幅改善**:
  - 支出キーワード: 7個 → 18個に拡充
  - タスクキーワード: 6個 → 20個に拡充
  - 悩みキーワード: 5個 → 18個に拡充
  - 感情分析キーワードも大幅追加（各カテゴリ4個 → 10個以上）

- **金額抽出機能の強化**:
  - 3パターンに対応: 「1000円」「¥1000」「1000（文脈から判定）」
  - カンマ区切りにも対応

- **Notion Handlerの改善**:
  - 接続テストを初期化時に自動実行
  - `is_connected`プロパティで接続状態を管理
  - ロギング機能の追加

### 🛡️ Fixed
- **エラーハンドリングの強化**:
  - Notion API未接続でもアプリが正常動作
  - Gemini APIのみでアプリを使用可能に
  - 親しみやすいエラーメッセージ

- **UI改善**:
  - Gemini/Notionの接続状態を個別表示
  - 再接続ボタンの追加
  - サイドバーの情報表示改善

### 🔧 Changed
- Notion APIをオプション扱いに変更（必須 → オプション）
- ステータスバッジを Prototype → Beta に変更
- バージョン番号を v0.1.0 → v0.2.0 に更新

---

## [0.1.0] - 2025-12-16

### ✨ Initial Release
- Streamlit UIの実装
- Gemini API連携
- Notion API連携（基本機能）
- テキスト分析（基本機能）
- デモモード実装
- ターミナル版の実装
