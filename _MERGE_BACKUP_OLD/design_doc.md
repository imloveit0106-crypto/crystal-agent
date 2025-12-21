# Crystal Agent 設計仕様書

**Version:** 1.0
**Last Updated:** 2025-12-20
**Status:** 確定版

---

## 📋 目次

1. [プロジェクト概要](#1-プロジェクト概要)
2. [コンセプト](#2-コンセプト)
3. [機能要件](#3-機能要件)
4. [技術スタック](#4-技術スタック)
5. [デザインシステム](#5-デザインシステム)
6. [アーキテクチャ](#6-アーキテクチャ)
7. [実装ルール](#7-実装ルール)
8. [禁止事項](#8-禁止事項)

---

## 1. プロジェクト概要

### プロダクト名
**Crystal Agent** - AI Personal Assistant

### 目的
日々の行動・思考を記録し、AIが過去のデータを基にパーソナライズされたサポートを提供する、知的でミニマルなパーソナルアシスタント。

### ターゲットユーザー
- デジタルミニマリスト
- 知的生産性を重視するビジネスパーソン
- Notion、Claude、Linearなどのモダンツールを愛用するユーザー

---

## 2. コンセプト

### 世界観
**"Intellectual Minimalism（知的なミニマリズム）"**

NotionやClaudeのような、洗練された知的な雰囲気を持つプロダクト。
過度な装飾を排し、本質的な機能と美しいタイポグラフィに焦点を当てる。

### デザイン哲学
> 「紙媒体のような、文字だけの美しさ」

- **Less is More:** 必要最小限の要素のみ
- **Typography First:** 美しいフォントと余白が主役
- **Calm Technology:** 主張せず、ユーザーの思考を邪魔しない

### キーワード
- 静謐
- 知的
- 洗練
- ミニマル
- タイポグラフィ

---

## 3. 機能要件

### 3.1 実装する機能（これ以外は実装しない）

#### ✅ チャット機能
- **AI応答生成:** Google Gemini 1.5 Flash使用
- **リアルタイム会話:** ユーザー入力 → AI応答
- **タイピングインジケーター:** 3つのドット（黒、アニメーション）
- **メッセージバブル:**
  - ユーザー: 右揃え、黒背景・白文字
  - AI: 左揃え、薄グレー背景・黒文字

#### ✅ Notion連携
- **データ保存:** 日記、家計簿、タスクを自動判別して保存
- **RAG（検索拡張生成）:** 過去のNotion履歴を基にパーソナライズ応答
- **統計表示:** Total / Diary / Tasks のカウント
- **自動抽出:**
  - テキストタイプ判定（日記/タスク/支出/メモ）
  - 金額抽出（正規表現）

#### ✅ ウェルカム画面（Notion/Claudeスタイル）
- **アートワーク:** ランダム表示（4種類のイラスト、グレースケール）
- **タイトル & サブタイトル:** "Crystal Agent" + 説明文
- **サジェストチップ（4つ）:**
  1. 家計簿をつける（wallet アイコン）
  2. 日記を書く（book-open アイコン）
  3. 今日の運勢（sparkles アイコン）
  4. タスク確認（list-todo アイコン）
- **インタラクション:** メッセージ送信時に自動フェードアウト（0.5秒）

#### ✅ 接続ステータス
- **ヘッダー表示:** 緑/黄/赤のドット + "Online"/"Limited"/"Offline"
- **リアルタイム監視:** Gemini + Notion 接続状態

#### ✅ クイックアクション
- **フッターボタン（3つ）:**
  1. 支出を記録
  2. 日記を書く
  3. タスク追加
- **機能:** 入力欄に定型文を挿入

---

### 3.2 実装しない機能（スコープ外）

❌ **ユーザー認証・ログイン機能**
❌ **マルチユーザー対応**
❌ **音声入力・音声出力**
❌ **画像アップロード・画像生成**
❌ **グラフ・チャート表示**（Plotlyなど）
❌ **ダークモード切り替え**（白背景のみ）
❌ **設定画面・カスタマイズ機能**
❌ **通知機能・プッシュ通知**
❌ **ステータスカード（MBTI、パーソナルカラーなど）**

---

## 4. 技術スタック

### 4.1 Backend

```yaml
言語: Python 3.8+
フレームワーク: FastAPI 0.104.0+
サーバー: Uvicorn (標準設定)
```

**依存ライブラリ:**
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
google-generativeai>=0.8.0
notion-client>=2.2.0
python-dotenv>=1.0.0
```

**エンドポイント:**
- `GET /` - HTMLページ配信
- `GET /health` - ヘルスチェック
- `GET /stats` - Notion統計取得
- `POST /chat` - チャット送信

---

### 4.2 Frontend

```yaml
マークアップ: HTML5
スタイル: Tailwind CSS 3.x (CDN)
スクリプト: Vanilla JavaScript (ES6+)
アイコン: Lucide Icons (CDN)
```

**CDN:**
```html
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Lucide Icons -->
<script src="https://unpkg.com/lucide@latest"></script>
```

**禁止事項:**
- ❌ React、Vue、Svelte などのフレームワーク
- ❌ jQuery
- ❌ Bootstrap、Material-UI などのUIライブラリ
- ❌ Webpack、Vite などのビルドツール

---

### 4.3 起動方法

```bash
# 推奨（自動インストール付き）
python start.py

# または（手動）
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 5. デザインシステム

### 5.1 カラーパレット

```css
背景: bg-white (白)
メインテキスト: text-gray-900 (ほぼ黒)
サブテキスト: text-gray-500, text-gray-600
ボーダー: border-gray-100 (薄いグレー)
アクセント: bg-gray-50, bg-gray-100 (極薄グレー)
ホバー: bg-gray-200
ユーザーバブル: bg-gray-900, text-white
```

**禁止:**
- ❌ グラデーション（linear-gradient, radial-gradient）
- ❌ カラフルな色（青、赤、紫、緑、黄など）
- ❌ ネオンカラー、蛍光色
- ❌ 複雑な影（drop-shadow）

---

### 5.2 タイポグラフィ

**フォントスタック:**
```css
font-family: -apple-system, BlinkMacSystemFont,
             'San Francisco', 'Segoe UI',
             'Roboto', 'Helvetica Neue',
             Arial, sans-serif;
```

**サイズ体系:**
```css
見出し（H1）: text-2xl sm:text-3xl (24px / 30px)
見出し（H2）: text-2xl (24px)
本文: text-base (16px)
補足: text-sm (14px)
キャプション: text-xs (12px)
```

**スタイル:**
```css
見出し: font-bold, tracking-tight (文字詰め)
本文: leading-relaxed (行間広め)
ボタン: font-medium, font-semibold
```

**禁止:**
- ❌ Serifフォント（※コンセプトと矛盾するため除外）
- ❌ 装飾フォント
- ❌ 4xl以上の巨大テキスト

---

### 5.3 レイアウト

**最大幅:**
```css
コンテンツ: max-w-3xl (768px)
ヘッダー: max-w-5xl (1024px)
```

**余白:**
```css
セクション間: py-8, py-12
コンポーネント間: gap-2, gap-3, gap-4
内部余白: px-4, px-5, px-6 / py-3, py-4
```

**角丸:**
```css
ボタン: rounded-lg, rounded-xl
チップ: rounded-full
メッセージバブル: rounded-xl
```

---

### 5.4 アイコン

**使用ライブラリ:** Lucide Icons

**使用アイコン:**
- `user` - ユーザーアバター
- `sparkles` - AIアバター
- `arrow-up` - 送信ボタン
- `wallet` - 家計簿
- `book-open` - 日記
- `list-todo` - タスク

**スタイル:**
```css
サイズ: w-4 h-4 (16px)
カラー: text-gray-400
```

**禁止:**
- ❌ 絵文字（🔮💰📝✨など）
- ❌ カラフルアイコン
- ❌ アイコンフォント（Font Awesome など）

---

### 5.5 アニメーション

**許可されるアニメーション:**
```css
1. メッセージフェードイン:
   - opacity: 0 → 1
   - transform: translateY(10px) → 0
   - duration: 0.3s

2. タイピングドット:
   - transform: translateY(0) ↔ translateY(-8px)
   - opacity: 0.4 ↔ 1
   - duration: 1.4s (無限ループ)

3. ウェルカムスクリーンフェードアウト:
   - opacity: 1 → 0
   - transform: translateY(0) → translateY(-20px)
   - duration: 0.5s

4. ホバー効果:
   - background-color変化
   - duration: 0.2s
```

**禁止:**
- ❌ bounce, wiggle などの派手なアニメーション
- ❌ rotate, scale などの回転・拡大縮小
- ❌ 1秒以上の長時間アニメーション
- ❌ パーティクル、キラキラ効果

---

## 6. アーキテクチャ

### 6.1 ディレクトリ構成

```
crystal-agent/
├── backend/
│   └── main.py              # FastAPI本体
├── frontend/
│   ├── templates/
│   │   └── index.html       # メインUI
│   └── static/
│       ├── js/
│       │   └── script.js    # フロントエンドロジック
│       └── css/
│           └── style.css    # ミニマルCSS
├── start.py                 # 起動スクリプト
├── start.bat                # Windows用起動
├── requirements.txt         # 依存パッケージ
├── .env                     # 環境変数
└── design_doc.md            # 本ドキュメント
```

**削除対象（未使用ファイル）:**
```
❌ app.py
❌ run.py
❌ simple_agent.py
❌ utils/
❌ config/
❌ tests/
```

---

### 6.2 データフロー

```
ユーザー入力
    ↓
frontend/script.js (sendMessage)
    ↓
POST /chat (backend/main.py)
    ↓
┌─────────────────────────────┐
│ 1. テキスト解析             │
│    - detect_type()          │
│    - extract_amount()       │
├─────────────────────────────┤
│ 2. RAGコンテキスト生成      │
│    - get_notion_stats()     │
│    - build_rag_context()    │
├─────────────────────────────┤
│ 3. Gemini API呼び出し       │
│    - model.generate_content │
├─────────────────────────────┤
│ 4. Notionへ保存             │
│    - notion.pages.create()  │
└─────────────────────────────┘
    ↓
ChatResponse (JSON)
    ↓
frontend/script.js (addMessage)
    ↓
画面にメッセージ表示
```

---

## 7. 実装ルール

### 7.1 コーディング規約

**Python (Backend):**
```python
# 関数名: スネークケース
def detect_type(text: str) -> str:
    pass

# クラス名: パスカルケース
class ChatRequest(BaseModel):
    pass

# 定数: 大文字スネークケース
API_BASE_URL = "http://localhost:8000"

# 型ヒント必須
from typing import Optional, Dict, List
```

**JavaScript (Frontend):**
```javascript
// 関数名: キャメルケース
async function sendMessage() { }

// 定数: UPPER_CASE
const API_BASE_URL = 'http://localhost:8000';

// グローバル関数: window.xxx
window.sendMessage = async function() { }
```

**HTML:**
```html
<!-- Tailwind クラスのみ使用 -->
<div class="bg-white text-gray-900 px-4 py-2">

<!-- カスタムクラスは最小限 -->
<div class="message-fade-in">
```

**CSS:**
```css
/* カスタムCSSは最小限（アニメーションのみ） */
@keyframes messageFadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
```

---

### 7.2 コメント規約

**必須コメント:**
```python
# セクション区切り
# ============================================
# Core Functions
# ============================================

# 関数説明（docstring不要）
def detect_type(text: str) -> str:
    """テキストタイプ判定"""
    pass
```

**禁止:**
- ❌ 過剰なコメント
- ❌ TODOコメント（issueで管理）
- ❌ コメントアウトされた古いコード

---

### 7.3 ファイルサイズ制限

```
backend/main.py:     500行以内
frontend/script.js:  400行以内
frontend/index.html: 250行以内
frontend/style.css:  150行以内
```

500行を超える場合は、ファイル分割を検討すること。

---

## 8. 禁止事項

### 8.1 デザイン

❌ **派手な視覚効果:**
- グラデーション
- ネオンカラー
- 影（drop-shadow）
- 光沢効果

❌ **装飾要素:**
- 絵文字
- アニメーションGIF
- 背景画像（アートワーク除く）
- パーティクル

❌ **複雑なレイアウト:**
- 3カラム以上のレイアウト
- サイドバー
- モーダル（ダイアログ）
- ドロワー

---

### 8.2 機能

❌ **スコープ外の機能:**
- ユーザー認証
- マルチユーザー
- ファイルアップロード
- 音声・画像処理
- グラフ・チャート

❌ **過剰な最適化:**
- キャッシュ機構
- バックグラウンドジョブ
- WebSocket（リアルタイム通信）

---

### 8.3 技術

❌ **フレームワーク:**
- React, Vue, Svelte
- jQuery
- Bootstrap, Material-UI

❌ **ビルドツール:**
- Webpack, Vite, Rollup
- Babel, TypeScript

❌ **データベース:**
- PostgreSQL, MySQL（Notionで代替）
- Redis（不要）

---

## 9. 品質基準

### 9.1 パフォーマンス

- 初回ロード: 2秒以内
- AI応答時間: 3秒以内（Gemini依存）
- アニメーション: 60fps維持

### 9.2 ブラウザ対応

- Chrome 90+
- Safari 14+
- Edge 90+
- Firefox 88+

### 9.3 レスポンシブ

- デスクトップ: 1024px以上
- タブレット: 768px以上
- モバイル: 375px以上

---

## 10. 今後の展望（Phase 2）

**現在は実装しないが、将来検討する機能:**

- 📅 カレンダービュー（日記の日付表示）
- 🔍 検索機能（Notion履歴の全文検索）
- 📊 簡易グラフ（支出の月次推移）
- 🎨 テーマ切り替え（ライト/ダーク）
- 🔔 リマインダー機能

---

## 11. 参考プロダクト

**デザイン参考:**
- [Notion](https://notion.so) - ミニマルUI、タイポグラフィ
- [Claude](https://claude.ai) - ウェルカム画面、チャットUI
- [Linear](https://linear.app) - クリーンなデザイン

**技術参考:**
- FastAPI公式ドキュメント
- Tailwind CSS公式ドキュメント
- Lucide Icons公式サイト

---

**このドキュメントは、Crystal Agentプロジェクトの憲法です。**
**すべての実装は、この仕様書に準拠すること。**
