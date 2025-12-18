import streamlit as st
import google.generativeai as genai
from notion_client import Client
import os
from dotenv import load_dotenv
from datetime import datetime

st.set_page_config(
    page_title="Crystal Agent",
    page_icon="🔮",
    layout="wide"
)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY") or st.secrets.get("NOTION_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_LIFE_LOG_DB_ID") or st.secrets.get("NOTION_LIFE_LOG_DB_ID")

is_notion_active = False

if NOTION_API_KEY and NOTION_DB_ID:
    try:
        notion = Client(auth=NOTION_API_KEY)
        notion.databases.retrieve(database_id=NOTION_DB_ID)
        is_notion_active = True
    except Exception as e:
        is_notion_active = False
else:
    is_notion_active = False

if not GEMINI_API_KEY:
    st.error("⚠️ Gemini APIキーが設定されていません。.envファイルを確認してください。")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
あなたは「Crystal Agent」という親切なAIアシスタントです。
ユーザーの日々の行動や思考を記録し、ポジティブに励ましてください。
口調は親しみやすく、絵文字を適度に使ってください。
"""

st.markdown("""
<style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
    .stTextInput input {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🔮 Crystal Agent")
    st.caption("v0.2.0 - Beta")
    st.divider()
    st.subheader("接続ステータス")
    st.success("✅ Gemini AI: 接続OK")
    if is_notion_active:
        st.success("✅ Notion DB: 接続OK")
    else:
        st.warning("⚠️ Notion DB: 未接続 (保存されません)")
        st.caption("※チャットは可能です")
    st.divider()
    st.subheader("クイック入力")
    if st.button("💰 今日使ったお金を記録"):
        st.session_state.input_text = "今日のランチに1000円使った"
    if st.button("📔 日記を書く"):
        st.session_state.input_text = "今日はこんなことがあった..."

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "こんにちは！今日はどんなことがありましたか？"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("メッセージを入力..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            try:
                full_prompt = SYSTEM_PROMPT + "\n\n" + prompt
                response = model.generate_content(full_prompt)
                ai_response = response.text
                st.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

                if is_notion_active:
                    try:
                        now = datetime.now()
                        notion.pages.create(
                            parent={"database_id": NOTION_DB_ID},
                            properties={
                                "Title": {"title": [{"text": {"content": now.strftime("%Y-%m-%d %H:%M")}}]},
                                "Date": {"date": {"start": now.isoformat()}},
                                "Type": {"select": {"name": "日記"}},
                                "Content": {"rich_text": [{"text": {"content": prompt}}]}
                            }
                        )
                        st.toast("Notionに保存しました！", icon="✅")
                    except Exception as e:
                        st.error(f"保存エラー: {e}")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
