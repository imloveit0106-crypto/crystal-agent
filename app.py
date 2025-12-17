"""
Crystal Agent - メインアプリ（モジュール版）
あなた専用のマルチモーダルAIエージェント
"""

import streamlit as st
from datetime import datetime

# モジュールをインポート
from config.settings import Settings
from utils.ai_brain import AIBrain
from utils.notion_handler import NotionHandler
from utils.text_analyzer import TextAnalyzer

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
    st.session_state.api_ready = (
        Settings.GEMINI_API_KEY and Settings.GEMINI_API_KEY != "your_gemini_api_key_here" and
        Settings.NOTION_API_KEY and Settings.NOTION_API_KEY != "your_notion_api_key_here"
    )

def init_modules():
    """モジュールを初期化"""
    if not st.session_state.api_ready:
        return False

    try:
        # AI Brain初期化
        if "ai_brain" not in st.session_state:
            st.session_state.ai_brain = AIBrain(Settings.GEMINI_API_KEY, Settings.AI_MODEL)

        # Notion Handler初期化
        if "notion_handler" not in st.session_state and Settings.USER_PROFILE_DB_ID and Settings.LIFE_LOG_DB_ID:
            st.session_state.notion_handler = NotionHandler(
                Settings.NOTION_API_KEY,
                Settings.USER_PROFILE_DB_ID,
                Settings.LIFE_LOG_DB_ID
            )

        # Text Analyzer初期化
        if "text_analyzer" not in st.session_state:
            st.session_state.text_analyzer = TextAnalyzer()

        return True
    except Exception as e:
        st.error(f"モジュール初期化エラー: {e}")
        return False

def get_ai_response(user_message):
    """AI応答を取得"""

    # テキスト分析
    if "text_analyzer" in st.session_state:
        analysis = st.session_state.text_analyzer.analyze(user_message)
        detected_type = analysis.get('type', '日記')
        detected_emotion = analysis.get('emotion', '普通')
        detected_amount = analysis.get('amount')
    else:
        detected_type = '日記'
        detected_emotion = '普通'
        detected_amount = None

    # AI応答生成
    if st.session_state.api_ready and "ai_brain" in st.session_state:
        try:
            # コンテキスト構築
            context = {}
            if "notion_handler" in st.session_state:
                profile = st.session_state.notion_handler.get_user_profile()
                if profile:
                    context['profile'] = profile

            # AI応答取得
            response = st.session_state.ai_brain.generate_response(user_message, context)

            # Notionに保存
            if "notion_handler" in st.session_state:
                st.session_state.notion_handler.add_life_log(
                    content=user_message,
                    type_=detected_type,
                    amount=detected_amount,
                    emotion=detected_emotion
                )

            return response, detected_type, detected_emotion
        except Exception as e:
            return f"エラーが発生しました: {e}", detected_type, detected_emotion
    else:
        # モックレスポンス（デモモード）
        mock_responses = {
            "こんにちは": "こんにちは！Crystal Agentです。今日も一日頑張りましょう！",
            "日記": "素晴らしいですね！今日の出来事を教えてください。",
            "支出": "支出を記録しますね。いくら使いましたか？",
            "タスク": "新しいタスクを追加しましょう。何をする予定ですか？",
            "悩み": "お悩みですか？ゆっくり聞かせてください。一緒に考えましょう。",
        }

        for key, response in mock_responses.items():
            if key in user_message:
                return response, detected_type, detected_emotion

        return f"「{user_message}」について考えています...（デモモード：{detected_type}として分類）", detected_type, detected_emotion

# ヘッダー
st.markdown(f"""
<div class="header">
    <h1>🔮 {Settings.APP_NAME}</h1>
    <p>あなた専用のマルチモーダルAIエージェント v{Settings.APP_VERSION}</p>
</div>
""", unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.markdown("## 📊 ダッシュボード")

    # API状態
    if st.session_state.api_ready:
        st.success("✅ API接続済み")
        if st.button("🔄 モジュール再初期化"):
            init_modules()
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
            type_badge = f"<span style='background:#667eea;color:white;padding:2px 8px;border-radius:10px;font-size:12px;margin-left:5px;'>{message.get('type', '日記')}</span>"
            emotion_emoji = {'良好': '😊', '普通': '😐', '疲労': '😫', '悩み': '😟'}.get(message.get('emotion', '普通'), '😐')

            st.markdown(f"""
            <div class="agent-message">
                <strong>🔮 Crystal Agent</strong> {type_badge} {emotion_emoji}<br>
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
        ai_response, detected_type, detected_emotion = get_ai_response(message_input)

    # AI応答を追加
    st.session_state.messages.append({
        "role": "agent",
        "content": ai_response,
        "type": detected_type,
        "emotion": detected_emotion,
        "timestamp": datetime.now()
    })

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
st.markdown(f"""
<div style="text-align: center; color: white; padding: 20px;">
    Made with ❤️ by Crystal Agent Team | Powered by Gemini & Notion | v{Settings.APP_VERSION}
</div>
""", unsafe_allow_html=True)

# モジュールの初期化（初回のみ）
if st.session_state.api_ready and "ai_brain" not in st.session_state:
    init_modules()
