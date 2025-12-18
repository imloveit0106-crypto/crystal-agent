import streamlit as st
import google.generativeai as genai
from notion_client import Client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="Crystal Agent",
    page_icon="🔮",
    layout="wide"
)

load_dotenv()

# API設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY") or st.secrets.get("NOTION_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_LIFE_LOG_DB_ID") or st.secrets.get("NOTION_LIFE_LOG_DB_ID")

# Notion接続チェック
is_notion_active = False
notion = None

if NOTION_API_KEY and NOTION_DB_ID:
    try:
        notion = Client(auth=NOTION_API_KEY)
        notion.databases.retrieve(database_id=NOTION_DB_ID)
        is_notion_active = True
    except Exception as e:
        is_notion_active = False

# Geminiチェック
if not GEMINI_API_KEY:
    st.error("⚠️ Gemini APIキーが設定されていません。")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# システムプロンプト
SYSTEM_PROMPT = """
あなたは「Crystal Agent」という親切なAIアシスタントです。
ユーザーの日々の行動や思考を記録し、ポジティブに励ましてください。
口調は親しみやすく、絵文字を適度に使ってください。
"""

# タイプ自動判定
def detect_type(text):
    """テキストからタイプを自動判定"""
    text_lower = text.lower()

    # 支出キーワード
    expense_keywords = ['円', '¥', 'yen', '買った', '購入', 'ランチ', '飲み会', '払った', '使った']
    if any(keyword in text for keyword in expense_keywords):
        return "支出"

    # タスクキーワード
    task_keywords = ['やる', 'する', 'まで', '期限', '締切', 'todo', 'タスク', '予定']
    if any(keyword in text_lower for keyword in task_keywords):
        return "タスク"

    # 悩みキーワード
    worry_keywords = ['悩', '不安', '心配', 'モヤモヤ', '困', 'つらい', 'しんどい']
    if any(keyword in text for keyword in worry_keywords):
        return "悩み"

    # デフォルトは日記
    return "日記"

# 金額抽出
def extract_amount(text):
    """テキストから金額を抽出"""
    pattern = r'(\d+(?:,\d{3})*(?:\.\d+)?)円'
    match = re.search(pattern, text)
    if match:
        return float(match.group(1).replace(',', ''))
    return None

# Notionからデータ取得
def get_notion_stats():
    """Notionから統計データを取得"""
    if not is_notion_active:
        return {"total": 0, "types": {}, "recent": []}

    try:
        # 過去30日のデータを取得
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()

        results = notion.databases.query(
            database_id=NOTION_DB_ID,
            filter={
                "property": "Date",
                "date": {
                    "after": thirty_days_ago
                }
            },
            sorts=[
                {
                    "property": "Date",
                    "direction": "descending"
                }
            ],
            page_size=100
        )

        stats = {
            "total": len(results.get("results", [])),
            "types": {},
            "amounts": [],
            "recent": []
        }

        for page in results.get("results", []):
            props = page.get("properties", {})

            # タイプ集計
            type_prop = props.get("Type", {})
            if type_prop.get("select"):
                type_name = type_prop["select"]["name"]
                stats["types"][type_name] = stats["types"].get(type_name, 0) + 1

            # 金額集計
            amount_prop = props.get("Amount", {})
            if amount_prop.get("number"):
                stats["amounts"].append(amount_prop["number"])

            # 最近のエントリー
            if len(stats["recent"]) < 5:
                title_prop = props.get("Title", {})
                date_prop = props.get("Date", {})

                title = ""
                if title_prop.get("title"):
                    title = title_prop["title"][0]["plain_text"] if title_prop["title"] else ""

                date = ""
                if date_prop.get("date"):
                    date = date_prop["date"]["start"]

                stats["recent"].append({"title": title, "date": date})

        return stats
    except Exception as e:
        st.error(f"データ取得エラー: {e}")
        return {"total": 0, "types": {}, "recent": []}

# カスタムCSS - Apple Quality: 究極のミニマリズムと洗練
st.markdown("""
<style>
    /* フォント設定 - Apple San Francisco UI */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }

    /* アプリ全体の背景 - Pure White */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* メインコンテンツエリア */
    .main .block-container {
        background-color: #FFFFFF !important;
        padding: 3rem 2rem !important;
        max-width: 1200px !important;
    }

    /* 文字色 - Deep Black */
    * {
        color: #1D1D1F !important;
    }

    /* タイトル - Apple Style Typography */
    h1 {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        margin-bottom: 2rem !important;
        text-align: center !important;
        line-height: 1.1 !important;
    }

    /* サブタイトル */
    h2, h3 {
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        margin-top: 3rem !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.02em !important;
    }

    /* 本文 - 読みやすさ最優先 */
    p, div, span {
        font-size: 1.0625rem !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
    }

    /* チャットメッセージ - 深度のある影 */
    .stChatMessage {
        border: none !important;
        border-radius: 24px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stChatMessage:hover {
        transform: translateY(-2px) !important;
    }

    /* ユーザーメッセージ - Apple Blue Accent */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #E8F0FE 0%, #F0F4FF 100%) !important;
        box-shadow: 0 4px 16px rgba(0, 122, 255, 0.08) !important;
    }

    /* AIメッセージ - Frosted Glass Effect */
    .stChatMessage[data-testid="assistant-message"] {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
    }

    /* メトリックカード - Modern Depth */
    .metric-card {
        background: linear-gradient(135deg, #1D1D1F 0%, #2D2D2F 100%) !important;
        border: none !important;
        padding: 2.5rem !important;
        border-radius: 28px !important;
        color: #FFFFFF !important;
        text-align: center !important;
        margin: 1rem 0 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12) !important;
    }

    .metric-card:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.18) !important;
    }

    .metric-number {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.04em !important;
        margin-bottom: 0.5rem !important;
    }

    .metric-label {
        font-size: 0.9375rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        opacity: 0.8 !important;
    }

    /* サイドバー - Clean Separation */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F5F5F7 0%, #FAFAFA 100%) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.06) !important;
        padding: 2rem 1.5rem !important;
    }

    [data-testid="stSidebar"] * {
        color: #1D1D1F !important;
    }

    /* ボタン - Capsule Design */
    .stButton button {
        border: none !important;
        background: #007AFF !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 9999px !important;
        padding: 0.875rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-size: 1.0625rem !important;
        box-shadow: 0 4px 16px rgba(0, 122, 255, 0.3) !important;
        letter-spacing: -0.01em !important;
    }

    .stButton button:hover {
        background: #0051D5 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(0, 122, 255, 0.4) !important;
    }

    .stButton button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px rgba(0, 122, 255, 0.3) !important;
    }

    /* 入力欄 - Refined Input */
    .stTextInput input, .stChatInput input {
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 20px !important;
        background-color: #F5F5F7 !important;
        padding: 1rem 1.5rem !important;
        font-size: 1.0625rem !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput input:focus, .stChatInput input:focus {
        border-color: #007AFF !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1) !important;
        outline: none !important;
    }

    /* グラフエリア - Card Style */
    .js-plotly-plot {
        background: #FAFAFA !important;
        border-radius: 24px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04) !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
    }

    /* 区切り線 - Subtle Divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: rgba(0, 0, 0, 0.06) !important;
        margin: 3rem 0 !important;
    }

    /* スピナー - Apple Blue */
    .stSpinner > div {
        border-top-color: #007AFF !important;
    }

    /* チャットアイコン - Material Icons Fix */
    .stChatMessage [data-testid="chatAvatarIcon-user"] span,
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] span,
    span[data-testid*="stMarkdownContainer"] span[class*="material"],
    [class*="material-icons"] {
        font-family: 'Material Icons', 'Material Symbols Outlined' !important;
        -webkit-font-feature-settings: 'liga' !important;
        font-feature-settings: 'liga' !important;
        text-rendering: optimizeLegibility !important;
        -webkit-font-smoothing: antialiased !important;
    }

    /* Success/Error Messages - Refined */
    .stSuccess, .stError, .stWarning {
        border-radius: 16px !important;
        border: none !important;
        padding: 1rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    }

    /* Toast Notifications */
    .stToast {
        border-radius: 20px !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
    }

    /* Smooth Scrolling */
    html {
        scroll-behavior: smooth !important;
    }
</style>
""", unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.title("🔮 Crystal Agent")
    st.caption("v0.3.0 - Complete")

    st.divider()

    # 接続ステータス
    st.subheader("📡 接続ステータス")
    st.success("✅ Gemini AI: 接続OK")
    if is_notion_active:
        st.success("✅ Notion DB: 接続OK")
    else:
        st.warning("⚠️ Notion DB: 未接続")
        st.caption("※チャットは可能です")

    st.divider()

    # 統計情報
    if is_notion_active:
        st.subheader("📊 統計情報（30日間）")
        stats = get_notion_stats()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">{stats['total']}</div>
                <div class="metric-label">総ログ数</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            total_amount = sum(stats['amounts']) if stats['amounts'] else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-number">¥{total_amount:,.0f}</div>
                <div class="metric-label">総支出</div>
            </div>
            """, unsafe_allow_html=True)

        # タイプ別グラフ - Apple Color Palette
        if stats['types']:
            st.subheader("📈 タイプ別内訳")
            fig = px.pie(
                values=list(stats['types'].values()),
                names=list(stats['types'].keys()),
                color_discrete_sequence=['#007AFF', '#5AC8FA', '#34C759', '#FF9500', '#FF3B30']
            )
            fig.update_layout(
                height=280,
                margin=dict(l=0, r=0, t=40, b=0),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=13)
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1D1D1F', size=13, family='-apple-system, BlinkMacSystemFont, sans-serif')
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#FFFFFF', width=3))
            )
            st.plotly_chart(fig, use_container_width=True)

        # 支出トレンド - Apple Graph Style
        if len(stats['amounts']) > 1:
            st.subheader("💰 支出トレンド")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=stats['amounts'][-10:],  # 最新10件
                mode='lines+markers',
                line=dict(color='#007AFF', width=3, shape='spline'),
                marker=dict(
                    size=8,
                    color='#007AFF',
                    line=dict(color='#FFFFFF', width=2)
                ),
                fill='tozeroy',
                fillcolor='rgba(0, 122, 255, 0.1)'
            ))
            fig.update_layout(
                height=240,
                margin=dict(l=20, r=20, t=20, b=40),
                showlegend=False,
                xaxis_title="記録",
                yaxis_title="金額 (円)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1D1D1F', size=13, family='-apple-system, BlinkMacSystemFont, sans-serif'),
                xaxis=dict(
                    showgrid=False,
                    showline=True,
                    linecolor='rgba(0,0,0,0.1)',
                    zeroline=False
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.06)',
                    showline=False,
                    zeroline=False
                )
            )
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # クイック入力
    st.subheader("⚡ クイック入力")

    if st.button("💰 支出を記録", use_container_width=True):
        st.session_state.quick_message = "今日のランチに1000円使った"
        st.rerun()

    if st.button("📔 日記を書く", use_container_width=True):
        st.session_state.quick_message = "今日は"
        st.rerun()

    if st.button("✅ タスクを追加", use_container_width=True):
        st.session_state.quick_message = "明日までに"
        st.rerun()

    if st.button("🗑️ 履歴をクリア", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "履歴をクリアしました。また話しかけてください！"}
        ]
        st.rerun()

# メインエリア
st.title("💬 チャット")

# メッセージ履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "こんにちは！今日はどんなことがありましたか？"}
    ]

# メッセージ表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# クイックメッセージの処理
quick_msg = None
if "quick_message" in st.session_state:
    quick_msg = st.session_state.quick_message
    del st.session_state.quick_message

# チャット入力
prompt = st.chat_input("メッセージを入力...")

# クイックメッセージまたは通常入力の処理
if quick_msg:
    prompt = quick_msg

if prompt:
    # ユーザーメッセージを追加
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # AI応答
    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            try:
                # タイプと金額を判定
                detected_type = detect_type(prompt)
                detected_amount = extract_amount(prompt)

                # AI応答生成
                full_prompt = SYSTEM_PROMPT + "\n\n" + prompt
                response = model.generate_content(full_prompt)
                ai_response = response.text
                st.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

                # Notionに保存
                if is_notion_active:
                    try:
                        now = datetime.now()
                        properties = {
                            "Title": {"title": [{"text": {"content": now.strftime("%Y-%m-%d %H:%M")}}]},
                            "Date": {"date": {"start": now.isoformat()}},
                            "Type": {"select": {"name": detected_type}},
                            "Content": {"rich_text": [{"text": {"content": prompt}}]}
                        }

                        # 金額があれば追加
                        if detected_amount:
                            properties["Amount"] = {"number": detected_amount}

                        notion.pages.create(
                            parent={"database_id": NOTION_DB_ID},
                            properties=properties
                        )
                        st.toast(f"✅ Notionに保存（{detected_type}）", icon="💾")
                    except Exception as e:
                        st.toast(f"⚠️ 保存エラー: {str(e)[:50]}", icon="❌")

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"申し訳ございません。エラーが発生しました: {str(e)}"
                })
