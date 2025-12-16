"""
Crystal Agent - メインアプリ
あなた専用のマルチモーダルAIエージェント
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="Crystal Agent",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS - モダンなデザイン
st.markdown("""
<style>
    /* メイン背景 */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* チャットメッセージスタイル */
    .user-message {
        background: #ffffff;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        max-width: 70%;
        margin-left: auto;
    }

    .agent-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        max-width: 70%;
    }

    /* ヘッダー */
    .header {
        text-align: center;
        padding: 20px;
        color: white;
    }

    /* サイドバー */
    .css-1d391kg {
        background: rgba(255,255,255,0.95);
    }

    /* ボタン */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }

    /* 入力フィールド */
    .stTextInput>div>div>input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 10px 20px;
    }

    /* サイドバー統計カード */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
        text-align: center;
    }

    .stat-number {
        font-size: 36px;
        font-weight: bold;
        color: #667eea;
    }

    .stat-label {
        color: #666;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_ready" not in st.session_state:
    # APIキーのチェック
    gemini_key = os.getenv("GEMINI_API_KEY")
    notion_key = os.getenv("NOTION_API_KEY")
    st.session_state.api_ready = (
        gemini_key and gemini_key != "your_gemini_api_key_here" and
        notion_key and notion_key != "your_notion_api_key_here"
    )

def init_apis():
    """APIを初期化"""
    if not st.session_state.api_ready:
        return False

    try:
        import google.generativeai as genai
        from notion_client import Client

        # Gemini設定
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        st.session_state.gemini_model = genai.GenerativeModel('gemini-1.5-flash')

        # Notion設定
        st.session_state.notion = Client(auth=os.getenv("NOTION_API_KEY"))

        return True
    except Exception as e:
        st.error(f"API初期化エラー: {e}")
        return False

def get_ai_response(user_message):
    """AI応答を取得（モックまたは実際のAPI）"""

    if st.session_state.api_ready and "gemini_model" in st.session_state:
        try:
            # 実際のGemini APIを使用
            response = st.session_state.gemini_model.generate_content(
                f"あなたは親切なAIアシスタント「Crystal Agent」です。ユーザーのメッセージに日本語で応答してください。\n\nユーザー: {user_message}"
            )
            return response.text
        except Exception as e:
            return f"エラーが発生しました: {e}"
    else:
        # モックレスポンス（開発用）
        mock_responses = {
            "こんにちは": "こんにちは！Crystal Agentです。今日も一日頑張りましょう！",
            "日記": "素晴らしいですね！今日の出来事を教えてください。",
            "支出": "支出を記録しますね。いくら使いましたか？",
            "タスク": "新しいタスクを追加しましょう。何をする予定ですか？",
            "悩み": "お悩みですか？ゆっくり聞かせてください。一緒に考えましょう。",
        }

        for key, response in mock_responses.items():
            if key in user_message:
                return response

        return f"「{user_message}」について考えています...現在はデモモードで動作中です。実際のAI応答を使うには、.envファイルにAPIキーを設定してください。"

def save_to_notion(message_type, content):
    """Notionに保存（将来実装）"""
    if st.session_state.api_ready and "notion" in st.session_state:
        try:
            # ここでNotionに保存する処理を実装
            pass
        except Exception as e:
            st.error(f"Notion保存エラー: {e}")

# ヘッダー
st.markdown("""
<div class="header">
    <h1>🔮 Crystal Agent</h1>
    <p>あなた専用のマルチモーダルAIエージェント</p>
</div>
""", unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.markdown("## 📊 ダッシュボード")

    # API状態
    if st.session_state.api_ready:
        st.success("✅ API接続済み")
        if st.button("🔄 API再初期化"):
            init_apis()
    else:
        st.warning("⚠️ デモモード")
        st.info("実際のAI機能を使うには、`.env`ファイルにAPIキーを設定してください")

        if st.button("📖 セットアップ方法"):
            st.markdown("""
            ### セットアップ手順

            1. `.env.example`を`.env`にコピー
            2. Gemini APIキーを取得
            3. Notion APIキーを取得
            4. `.env`ファイルに貼り付け
            5. `python test_api.py`で確認
            6. アプリを再起動

            詳しくは`README.md`を参照
            """)

    st.markdown("---")

    # 統計情報（モックデータ）
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">28</div>
        <div class="stat-label">記録した日数</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">156</div>
        <div class="stat-label">総ログ数</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">12</div>
        <div class="stat-label">完了タスク</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # クイックアクション
    st.markdown("## ⚡ クイックアクション")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 日記"):
            st.session_state.quick_action = "日記を書きたい"
        if st.button("💰 支出"):
            st.session_state.quick_action = "支出を記録したい"

    with col2:
        if st.button("✅ タスク"):
            st.session_state.quick_action = "タスクを追加したい"
        if st.button("💭 悩み"):
            st.session_state.quick_action = "悩みを相談したい"

# メインチャットエリア
st.markdown("### 💬 チャット")

# チャット履歴を表示
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>あなた</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="agent-message">
                <strong>🔮 Crystal Agent</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

# クイックアクションからの入力
if "quick_action" in st.session_state and st.session_state.quick_action:
    user_input = st.session_state.quick_action
    st.session_state.quick_action = None
else:
    user_input = None

# チャット入力
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])

    with col1:
        message_input = st.text_input(
            "メッセージを入力...",
            key="message_input",
            placeholder="例: 今日は楽しかった！",
            label_visibility="collapsed",
            value=user_input if user_input else ""
        )

    with col2:
        submit_button = st.form_submit_button("送信 📤")

# メッセージ送信処理
if submit_button and message_input:
    # ユーザーメッセージを追加
    st.session_state.messages.append({
        "role": "user",
        "content": message_input,
        "timestamp": datetime.now()
    })

    # AI応答を取得
    with st.spinner("考え中..."):
        ai_response = get_ai_response(message_input)

    # AI応答を追加
    st.session_state.messages.append({
        "role": "agent",
        "content": ai_response,
        "timestamp": datetime.now()
    })

    # Notionに保存（将来実装）
    # save_to_notion("chat", message_input)

    # ページをリロード
    st.rerun()

# 初回表示時のウェルカムメッセージ
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="agent-message">
        <strong>🔮 Crystal Agent</strong><br>
        こんにちは！私はあなた専用のAIエージェントです。<br><br>
        日記、支出、タスク、悩み...何でも話してください。<br>
        あなたの人生をもっと豊かにするお手伝いをします！
    </div>
    """, unsafe_allow_html=True)

# フッター
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 20px;">
    Made with ❤️ by Crystal Agent Team | Powered by Gemini & Notion
</div>
""", unsafe_allow_html=True)

# APIの初期化（初回のみ）
if st.session_state.api_ready and "gemini_model" not in st.session_state:
    init_apis()
