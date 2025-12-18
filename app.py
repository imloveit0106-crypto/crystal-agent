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

# カスタムCSS - 高級感のあるクリーム色 × Times New Roman テーマ
st.markdown("""
<style>
    /* フォント設定 - Times New Roman で統一 */
    * {
        font-family: 'Times New Roman', Times, serif !important;
    }

    /* アプリ全体の背景色 - クリーム色 */
    .stApp {
        background-color: #FFFEF5 !important;
    }

    /* メインコンテンツエリア */
    .main .block-container {
        background-color: #FFFEF5 !important;
    }

    /* 文字色 - 真っ黒 */
    * {
        color: #000000 !important;
    }

    /* タイトル - 大きくスタイリッシュに */
    h1 {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 1.5rem !important;
        text-align: center !important;
    }

    /* サブタイトル */
    h2, h3 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        letter-spacing: 0.03em !important;
    }

    /* 本文 */
    p, div, span {
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
    }

    /* チャットメッセージ - 枠線削除 */
    .stChatMessage {
        border: none !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        margin-bottom: 1rem !important;
    }

    /* ユーザーメッセージ - 薄い青色 */
    .stChatMessage[data-testid="user-message"] {
        background-color: #E3F2FD !important;
        border-radius: 16px !important;
    }

    /* AIメッセージ - 白 + 影 */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }

    /* メトリックカード - クリーム色に調和 */
    .metric-card {
        background: #000000 !important;
        border: 2px solid #000000 !important;
        padding: 2rem !important;
        border-radius: 12px !important;
        color: #FFFEF5 !important;
        text-align: center !important;
        margin: 0.75rem 0 !important;
        transition: all 0.3s ease !important;
    }

    .metric-card:hover {
        background: #FFFEF5 !important;
        color: #000000 !important;
    }

    .metric-number {
        font-size: 3rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    .metric-label {
        font-size: 1rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin-top: 0.5rem !important;
    }

    /* サイドバー - クリーム色の薄いバージョン */
    [data-testid="stSidebar"] {
        background-color: #FFF9E6 !important;
        border-right: 2px solid #E8E4D5 !important;
    }

    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    /* ボタン - エレガントなスタイル */
    .stButton button {
        border: 2px solid #000000 !important;
        background: #FFFEF5 !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        font-size: 1.1rem !important;
    }

    .stButton button:hover {
        background: #000000 !important;
        color: #FFFEF5 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }

    /* 入力欄 */
    .stTextInput input, .stChatInput input {
        border: 2px solid #E8E4D5 !important;
        border-radius: 12px !important;
        background-color: #FFFFFF !important;
        padding: 0.75rem !important;
        font-size: 1.1rem !important;
    }

    .stTextInput input:focus, .stChatInput input:focus {
        border-color: #000000 !important;
        box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.1) !important;
    }

    /* グラフエリア */
    .js-plotly-plot {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    }

    /* 区切り線 */
    hr {
        border-color: #E8E4D5 !important;
        margin: 2rem 0 !important;
    }

    /* スピナー */
    .stSpinner > div {
        border-top-color: #000000 !important;
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

        # タイプ別グラフ
        if stats['types']:
            st.subheader("📈 タイプ別内訳")
            fig = px.pie(
                values=list(stats['types'].values()),
                names=list(stats['types'].keys()),
                color_discrete_sequence=['#000000', '#404040', '#808080', '#BFBFBF', '#E0E0E0']
            )
            fig.update_layout(
                height=250,
                margin=dict(l=0, r=0, t=30, b=0),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#000000', size=12)
            )
            st.plotly_chart(fig, use_container_width=True)

        # 支出トレンド
        if len(stats['amounts']) > 1:
            st.subheader("💰 支出トレンド")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=stats['amounts'][-10:],  # 最新10件
                mode='lines+markers',
                line=dict(color='#000000', width=2),
                marker=dict(size=6, color='#000000'),
                fill='tozeroy',
                fillcolor='rgba(0,0,0,0.05)'
            ))
            fig.update_layout(
                height=200,
                margin=dict(l=0, r=0, t=10, b=0),
                showlegend=False,
                xaxis_title="記録",
                yaxis_title="金額(円)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#000000', size=12),
                xaxis=dict(showgrid=True, gridcolor='#E5E5E5'),
                yaxis=dict(showgrid=True, gridcolor='#E5E5E5')
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
