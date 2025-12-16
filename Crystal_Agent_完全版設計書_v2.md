# Crystal Agent 完全版設計書 v2.0

**ドキュメント作成日**: 2025-12-16
**バージョン**: 2.0
**ステータス**: プロトタイプ完成

---

## 📋 目次

1. [プロジェクト概要](#1-プロジェクト概要)
2. [システムアーキテクチャ](#2-システムアーキテクチャ)
3. [技術仕様](#3-技術仕様)
4. [データベース設計](#4-データベース設計)
5. [API仕様](#5-api仕様)
6. [UI/UX設計](#6-uiux設計)
7. [セキュリティ](#7-セキュリティ)
8. [開発フロー](#8-開発フロー)
9. [将来の拡張](#9-将来の拡張)
10. [付録](#10-付録)

---

## 1. プロジェクト概要

### 1.1 目的

Crystal Agentは、ユーザーの日々の行動・思考・目標を記録し、AIとデータベースを活用してパーソナライズされたアドバイスを提供するAIエージェントです。

### 1.2 主要機能

| 機能 | 説明 | 優先度 |
|------|------|--------|
| 自然言語対話 | LINE風のチャットインターフェース | 高 |
| 自動分類 | 日記・支出・タスク・悩みを自動判定 | 高 |
| データ保存 | Notionデータベースへの自動保存 | 高 |
| パーソナライズ助言 | 過去データに基づくAI助言 | 中 |
| データ可視化 | 統計情報・グラフ表示 | 中 |
| 検索機能 | 過去のログを検索 | 低 |

### 1.3 ターゲットユーザー

- 自己管理を改善したい社会人
- 習慣化が苦手な人
- データに基づいた自己成長を望む人
- プログラミング初心者

### 1.4 成功指標（KPI）

- ユーザーが1週間継続して使用する率: 70%以上
- 1日あたりの平均ログ数: 3件以上
- ユーザー満足度: 4/5以上

---

## 2. システムアーキテクチャ

### 2.1 全体構成図

```
┌─────────────────────────────────────────────────────────┐
│                      User Interface                      │
│  ┌──────────────────┐       ┌──────────────────┐       │
│  │  Streamlit UI    │       │  Terminal UI     │       │
│  │  (app.py)        │       │  (simple_agent)  │       │
│  └────────┬─────────┘       └────────┬─────────┘       │
└───────────┼──────────────────────────┼─────────────────┘
            │                          │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   Application Layer    │
            │  ┌──────────────────┐  │
            │  │  Crystal Agent   │  │
            │  │  Core Logic      │  │
            │  └──────────────────┘  │
            └────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌───────────────┐ ┌──────────────┐ ┌──────────────┐
│  Gemini API   │ │  Notion API  │ │  Local Cache │
│  (AI Model)   │ │  (Database)  │ │  (Session)   │
└───────────────┘ └──────────────┘ └──────────────┘
```

### 2.2 データフロー

```
ユーザー入力
    ↓
入力検証・前処理
    ↓
Gemini API → AI応答生成
    ↓
応答の後処理・分類
    ↓
Notion DB保存
    ↓
UI表示
```

### 2.3 技術スタック詳細

#### フロントエンド
- **Streamlit 1.30+**: Webアプリケーションフレームワーク
- **カスタムCSS**: UI/UXの強化

#### バックエンド
- **Python 3.10+**: メインプログラミング言語
- **google-generativeai**: Gemini API クライアント
- **notion-client**: Notion API クライアント

#### インフラ
- **ローカル実行**: 開発・個人利用
- **将来**: クラウドデプロイ（Streamlit Cloud等）

---

## 3. 技術仕様

### 3.1 システム要件

#### 最小要件
- Python 3.10以上
- メモリ: 512MB以上
- ストレージ: 100MB以上
- インターネット接続: 必須

#### 推奨要件
- Python 3.11以上
- メモリ: 2GB以上
- ストレージ: 1GB以上
- ブロードバンド接続

### 3.2 依存ライブラリ

```python
streamlit>=1.30.0           # UI フレームワーク
google-generativeai>=0.3.0  # Gemini API
notion-client>=2.2.0         # Notion API
python-dotenv>=1.0.0        # 環境変数管理
requests>=2.31.0            # HTTP通信
```

### 3.3 ファイル構成

```
crystal-agent/
├── app.py                          # Streamlit メインアプリ
├── simple_agent.py                 # ターミナル版
├── test_api.py                     # API接続テスト
├── requirements.txt                # 依存関係
├── .env                            # 環境変数（Git除外）
├── .env.example                    # 環境変数テンプレート
├── .gitignore                      # Git除外設定
├── README.md                       # ユーザー向けドキュメント
├── Crystal_Agent_完全版設計書_v2.md # このファイル
└── future/                         # 将来実装予定
    ├── modules/                    # モジュール化されたコード
    │   ├── ai_engine.py           # AI処理
    │   ├── notion_handler.py      # Notion操作
    │   └── analyzer.py            # データ分析
    └── tests/                      # テストコード
        └── test_*.py
```

---

## 4. データベース設計

### 4.1 Notion データベース構造

#### 4.1.1 User_Profile（ユーザープロフィール）

| プロパティ名 | タイプ | 説明 | 必須 |
|-------------|--------|------|------|
| Name | タイトル | ユーザー名 | ✅ |
| Age | 数値 | 年齢 | ❌ |
| Goals | テキスト | 目標・ゴール | ❌ |
| Values | テキスト | 大切にしていること | ❌ |
| Skills | マルチセレクト | スキル・興味 | ❌ |
| Created | 作成日時 | 作成日時 | 自動 |
| Updated | 更新日時 | 更新日時 | 自動 |

**使用例:**
```json
{
  "Name": "ゆうや",
  "Age": 25,
  "Goals": "プログラミングスキルを向上させる",
  "Values": "継続は力なり",
  "Skills": ["Python", "AI", "Web開発"]
}
```

#### 4.1.2 Life_Log（ライフログ）

| プロパティ名 | タイプ | 説明 | 必須 |
|-------------|--------|------|------|
| Title | タイトル | ログのタイトル | ✅ |
| Date | 日付 | 記録日 | ✅ |
| Type | セレクト | 日記/支出/タスク/悩み | ✅ |
| Content | テキスト | 内容詳細 | ✅ |
| Amount | 数値 | 金額（支出のみ） | ❌ |
| Status | セレクト | 完了/未完了 | ❌ |
| Tags | マルチセレクト | タグ | ❌ |
| AI_Advice | テキスト | AIからの助言 | ❌ |
| Created | 作成日時 | 作成日時 | 自動 |

**使用例:**
```json
{
  "Title": "今日の振り返り",
  "Date": "2025-12-16",
  "Type": "日記",
  "Content": "Crystal Agentのプロトタイプが完成した！",
  "Tags": ["開発", "達成感"],
  "AI_Advice": "素晴らしい進捗ですね！明日は..."
}
```

### 4.2 データ保存フロー

```python
def save_to_notion(log_type, content, metadata):
    """
    Notionにデータを保存

    Args:
        log_type (str): ログタイプ（日記/支出/タスク/悩み）
        content (str): 内容
        metadata (dict): 追加メタデータ
    """
    # 1. Notion API初期化
    notion = Client(auth=NOTION_API_KEY)

    # 2. データ構造作成
    page_data = {
        "parent": {"database_id": LIFE_LOG_DB_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": metadata.get("title")}}]},
            "Date": {"date": {"start": datetime.now().isoformat()}},
            "Type": {"select": {"name": log_type}},
            "Content": {"rich_text": [{"text": {"content": content}}]}
        }
    }

    # 3. Notionに保存
    notion.pages.create(**page_data)
```

---

## 5. API仕様

### 5.1 Gemini API

#### 5.1.1 基本設定

```python
import google.generativeai as genai

# API設定
genai.configure(api_key=GEMINI_API_KEY)

# モデル選択
model = genai.GenerativeModel('gemini-1.5-flash')
```

#### 5.1.2 プロンプト設計

```python
SYSTEM_PROMPT = """
あなたは「Crystal Agent」という名前の親切なAIアシスタントです。

【役割】
- ユーザーの日々の行動を記録し、成長をサポートする
- 共感的で温かい対話を心がける
- 具体的で実践的なアドバイスを提供する

【対話スタイル】
- 敬語ではなく、親しみやすい口調
- 絵文字を適度に使用
- ポジティブなフィードバック

【自動分類】
ユーザーの入力から以下を判定:
- 日記: 出来事・感情の記録
- 支出: 金額を含む買い物の記録
- タスク: やるべきことの記録
- 悩み: 相談・悩みの共有
"""

def generate_response(user_message, context=None):
    """AI応答を生成"""
    prompt = f"{SYSTEM_PROMPT}\n\nユーザー: {user_message}"

    if context:
        prompt += f"\n\n過去の会話:\n{context}"

    response = model.generate_content(prompt)
    return response.text
```

#### 5.1.3 レート制限

- **無料枠**: 1,500 requests/day
- **対策**: ローカルキャッシュ、バッチ処理

### 5.2 Notion API

#### 5.2.1 データ取得

```python
def get_user_profile():
    """ユーザープロフィールを取得"""
    notion = Client(auth=NOTION_API_KEY)

    # データベースをクエリ
    results = notion.databases.query(
        database_id=USER_PROFILE_DB_ID
    )

    return results['results'][0] if results['results'] else None
```

#### 5.2.2 データ作成

```python
def create_life_log(title, log_type, content):
    """ライフログを作成"""
    notion = Client(auth=NOTION_API_KEY)

    notion.pages.create(
        parent={"database_id": LIFE_LOG_DB_ID},
        properties={
            "Title": {"title": [{"text": {"content": title}}]},
            "Type": {"select": {"name": log_type}},
            "Content": {"rich_text": [{"text": {"content": content}}]}
        }
    )
```

---

## 6. UI/UX設計

### 6.1 Streamlit UI仕様

#### 6.1.1 カラーパレット

```css
Primary Gradient: #667eea → #764ba2
Background: 同グラデーション
User Message: #ffffff (白)
Agent Message: Primary Gradient
Text: #333333 (ダークグレー)
Accent: #667eea (紫)
```

#### 6.1.2 レイアウト

```
┌─────────────────────────────────────────────┐
│              Header (固定)                   │
│          🔮 Crystal Agent                    │
├──────────┬──────────────────────────────────┤
│          │                                  │
│ Sidebar  │      Chat Area                   │
│          │                                  │
│ - Status │  [User Message]                  │
│ - Stats  │  [Agent Message]                 │
│ - Quick  │  [User Message]                  │
│   Action │  [Agent Message]                 │
│          │                                  │
│          │                                  │
├──────────┴──────────────────────────────────┤
│         Input Area (固定)                    │
│  [メッセージ入力...] [送信]                   │
└─────────────────────────────────────────────┘
```

#### 6.1.3 インタラクション

1. **メッセージ送信**
   - ユーザーが入力 → Enterまたは送信ボタン
   - スピナー表示「考え中...」
   - AI応答を表示
   - スクロールを最下部に自動移動

2. **クイックアクション**
   - ボタンクリック → 事前定義メッセージを入力欄に挿入
   - 自動送信はしない（ユーザーが確認可能）

3. **統計表示**
   - リアルタイム更新
   - カウントアップアニメーション

### 6.2 ターミナルUI仕様

```
====================================================
  🔮 Crystal Agent - ターミナル版
  あなた専用のマルチモーダルAIエージェント
====================================================

⚠️  デモモードで動作中

📖 使い方:
  - メッセージを入力してEnterキーを押す
  - 'help' でヘルプ表示
  - 'quit' または 'exit' で終了

🔮 Crystal Agent: こんにちは！何でも話しかけてください。

------------------------------------------------------------
あなた: [ユーザー入力]

🔮 Crystal Agent: [AI応答]
```

---

## 7. セキュリティ

### 7.1 APIキー管理

```bash
# .env ファイル（Gitに含めない）
GEMINI_API_KEY=secret_key_here
NOTION_API_KEY=secret_key_here

# .gitignore に追加
.env
*.pyc
__pycache__/
```

### 7.2 データプライバシー

- **ローカル処理**: 可能な限りローカルで処理
- **最小限のデータ送信**: 必要なデータのみAPI送信
- **ユーザーコントロール**: データ削除機能（将来実装）

### 7.3 エラーハンドリング

```python
try:
    # API呼び出し
    response = model.generate_content(prompt)
except Exception as e:
    # ユーザーフレンドリーなエラーメッセージ
    return "申し訳ございません。一時的にエラーが発生しました。"
```

---

## 8. 開発フロー

### 8.1 Git ワークフロー

```bash
# ブランチ戦略
main          # 本番環境
├── develop   # 開発環境
    ├── feature/ui-improvement    # 機能追加
    ├── feature/notion-integration
    └── bugfix/api-error
```

### 8.2 コミットメッセージ規約

```
feat: 新機能追加
fix: バグ修正
docs: ドキュメント更新
style: コードスタイル変更
refactor: リファクタリング
test: テスト追加
chore: ビルド・設定変更

例:
feat: Notion API連携を実装
fix: Gemini API接続エラーを修正
docs: README にセットアップ手順を追加
```

### 8.3 テスト戦略

```python
# future/tests/test_api.py
def test_gemini_connection():
    """Gemini API接続テスト"""
    assert agent.gemini_model is not None

def test_notion_connection():
    """Notion API接続テスト"""
    assert agent.notion is not None

def test_message_classification():
    """メッセージ分類テスト"""
    assert classify("今日は1000円使った") == "支出"
    assert classify("タスクを追加") == "タスク"
```

---

## 9. 将来の拡張

### 9.1 Phase 3: 高度な機能

#### 9.1.1 コンテキスト検索
```python
def search_context(query, limit=5):
    """
    過去のログから関連情報を検索

    - ベクトル検索（埋め込み）
    - キーワード検索
    - 時系列検索
    """
    pass
```

#### 9.1.2 パーソナライズ助言
```python
def personalized_advice(user_profile, recent_logs):
    """
    ユーザープロフィールと過去ログから
    パーソナライズされた助言を生成
    """
    pass
```

#### 9.1.3 データ可視化
```python
import plotly.express as px

def visualize_spending(logs):
    """支出データをグラフ化"""
    df = pd.DataFrame(logs)
    fig = px.line(df, x='date', y='amount')
    st.plotly_chart(fig)
```

### 9.2 Phase 4: 最適化

- **パフォーマンス**: 非同期処理、キャッシング
- **UI/UX**: アニメーション、レスポンシブデザイン
- **モバイル対応**: PWA化

### 9.3 技術的負債の管理

| 項目 | 現状 | 改善案 | 優先度 |
|------|------|--------|--------|
| モジュール化 | 単一ファイル | クラス・モジュール分割 | 高 |
| テスト | なし | ユニットテスト実装 | 高 |
| ログ | print文 | loggingモジュール | 中 |
| 設定管理 | ハードコード | config.yaml | 中 |

---

## 10. 付録

### 10.1 用語集

| 用語 | 説明 |
|------|------|
| Gemini | Googleの生成AIモデル |
| Notion | オールインワンワークスペース |
| Streamlit | Pythonで作るWebアプリフレームワーク |
| API | Application Programming Interface |
| UI/UX | User Interface / User Experience |

### 10.2 参考資料

- [Gemini API ドキュメント](https://ai.google.dev/docs)
- [Notion API ドキュメント](https://developers.notion.com/)
- [Streamlit ドキュメント](https://docs.streamlit.io/)

### 10.3 トラブルシューティング

詳細は `README.md` の「トラブルシューティング」セクションを参照

### 10.4 変更履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|----------|
| 2.0 | 2025-12-16 | プロトタイプ完成版 |
| 1.0 | 2025-12-01 | 初版作成 |

---

**ドキュメント終了**

このプロジェクトは継続的に進化しています。
質問・提案があれば、Issuesで報告してください！
