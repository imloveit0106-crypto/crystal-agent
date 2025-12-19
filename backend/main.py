"""
Crystal Agent Backend - FastAPI
Streamlit app.py からの完全移植 - RAG機能を含む全ロジックを保持
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, List
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
import re

# Gemini & Notion
import google.generativeai as genai
from notion_client import Client

# 環境変数読み込み
load_dotenv()

# FastAPI アプリ
app = FastAPI(title="Crystal Agent API")

# CORS設定 - ローカル開発用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイルのマウント（CSS, JS用）
# プロジェクトルートからの相対パスを計算
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "frontend" / "static"
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"

# /static パスに静的ファイルをマウント
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# API設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
# 複数の変数名に対応（柔軟性向上）
NOTION_DB_ID = os.getenv("NOTION_LIFE_LOG_DB_ID") or os.getenv("NOTION_DATABASE_ID")

# デバッグ: 環境変数の読み込み状況を詳細に表示
print("\n" + "="*67)
print("環境変数読み込み状況")
print("="*67)
print(f"GEMINI_API_KEY: {'設定済み' if GEMINI_API_KEY else '未設定 (None)'}")
print(f"NOTION_API_KEY: {'設定済み' if NOTION_API_KEY else '未設定 (None)'}")
if NOTION_API_KEY:
    print(f"  └─ 値の先頭: {NOTION_API_KEY[:20]}...")
print(f"NOTION_DB_ID: {'設定済み' if NOTION_DB_ID else '未設定 (None)'}")
if NOTION_DB_ID:
    print(f"  └─ 値: {NOTION_DB_ID}")
print("="*67 + "\n")

# Notion接続チェック
is_notion_active = False
notion = None

if NOTION_API_KEY and NOTION_DB_ID:
    try:
        print("Notion接続を試行中...")
        notion = Client(auth=NOTION_API_KEY)
        # データベース接続テスト
        db_info = notion.databases.retrieve(database_id=NOTION_DB_ID)
        is_notion_active = True
        print("Notion DB接続成功")
        print(f"  └─ データベース名: {db_info.get('title', [{}])[0].get('plain_text', 'N/A')}")
    except Exception as e:
        print(f"Notion DB接続失敗")
        print(f"  └─ エラータイプ: {type(e).__name__}")
        print(f"  └─ エラー詳細: {str(e)}")
        if "Unauthorized" in str(e) or "API token is invalid" in str(e):
            print(f"  └─ ヒント: NOTION_API_KEYが正しいか確認してください")
            print(f"     - Integration Tokenは 'secret_' で始まります")
            print(f"     - データベースにIntegrationを招待しましたか？")
        if "object_not_found" in str(e).lower() or "Could not find" in str(e):
            print(f"  └─ ヒント: NOTION_DB_IDが正しいか確認してください")
            print(f"     - データベースURLから32文字のIDを取得")
        is_notion_active = False
else:
    print("Notion接続スキップ（環境変数が未設定）")
    if not NOTION_API_KEY:
        print("  └─ NOTION_API_KEYが未設定です")
    if not NOTION_DB_ID:
        print("  └─ NOTION_DB_ID（またはNOTION_LIFE_LOG_DB_ID）が未設定です")

# Gemini設定
if not GEMINI_API_KEY:
    raise ValueError("Gemini APIキーが設定されていません")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
print("Gemini API接続成功 (gemini-1.5-flash)")

# システムプロンプト
SYSTEM_PROMPT = """
あなたは「Crystal Agent」という親切なAIアシスタントです。
ユーザーの日々の行動や思考を記録し、ポジティブに励ましてください。
口調は親しみやすく、絵文字を適度に使ってください。
"""

# =========================
# ユーティリティ関数（app.pyから移植）
# =========================

def detect_type(text: str) -> str:
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


def extract_amount(text: str) -> Optional[float]:
    """テキストから金額を抽出"""
    pattern = r'(\d+(?:,\d{3})*(?:\.\d+)?)円'
    match = re.search(pattern, text)
    if match:
        return float(match.group(1).replace(',', ''))
    return None


def get_notion_stats() -> Dict:
    """
    Notionから統計データを取得
    RAG（検索拡張生成）のコンテキスト取得機能
    """
    if not is_notion_active:
        return {"total": 0, "types": {}, "recent": [], "amounts": []}

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

            # 最近のエントリー（RAGコンテキスト用）
            if len(stats["recent"]) < 10:  # 最近10件を取得
                title_prop = props.get("Title", {})
                content_prop = props.get("Content", {})
                date_prop = props.get("Date", {})

                title = ""
                if title_prop.get("title") and len(title_prop["title"]) > 0:
                    title = title_prop["title"][0].get("plain_text", "")

                content = ""
                if content_prop.get("rich_text") and len(content_prop["rich_text"]) > 0:
                    content = content_prop["rich_text"][0].get("plain_text", "")

                date = ""
                if date_prop.get("date"):
                    date = date_prop["date"]["start"]

                stats["recent"].append({
                    "title": title,
                    "content": content,
                    "date": date
                })

        print(f"Notionから {stats['total']} 件のデータを取得（RAGコンテキスト）")
        return stats

    except Exception as e:
        print(f"データ取得エラー: {e}")
        return {"total": 0, "types": {}, "recent": [], "amounts": []}


def build_rag_context(stats: Dict) -> str:
    """
    RAG: Notionデータからコンテキストを構築
    これにより、AIがユーザーの過去の行動を踏まえた回答を生成
    """
    if not stats or stats["total"] == 0:
        return ""

    context = "\n\n【ユーザーの最近の記録（参考情報）】\n"

    # 最近のエントリーをコンテキストに追加
    for entry in stats["recent"][:5]:  # 最新5件
        if entry["content"]:
            context += f"- {entry['date']}: {entry['content']}\n"

    # 統計情報を追加
    if stats["types"]:
        context += f"\n統計: "
        for type_name, count in stats["types"].items():
            context += f"{type_name}({count}件) "

    return context


# =========================
# APIモデル
# =========================

class ChatRequest(BaseModel):
    message: str
    use_rag: bool = True  # RAGを使用するかどうか


class ChatResponse(BaseModel):
    response: str
    detected_type: str
    detected_amount: Optional[float]
    saved_to_notion: bool
    rag_used: bool


class StatsResponse(BaseModel):
    total: int
    types: Dict[str, int]
    recent: List[Dict]
    amounts: List[float]


# =========================
# API エンドポイント
# =========================

@app.get("/")
async def root():
    """メインHTMLページを返す"""
    html_path = TEMPLATES_DIR / "index.html"
    return FileResponse(html_path)


@app.get("/health")
async def health_check():
    """ヘルスチェック（API用）"""
    return {
        "status": "ok",
        "app": "Crystal Agent API",
        "gemini": "connected",
        "notion": "connected" if is_notion_active else "disconnected"
    }


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Notionから統計データを取得"""
    stats = get_notion_stats()
    return stats


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    チャットエンドポイント
    RAG機能により、Notionのデータをコンテキストとして使用
    """
    try:
        user_message = request.message

        # タイプと金額を判定
        detected_type = detect_type(user_message)
        detected_amount = extract_amount(user_message)

        # RAG: Notionからコンテキストを取得
        rag_context = ""
        if request.use_rag and is_notion_active:
            stats = get_notion_stats()
            rag_context = build_rag_context(stats)
            print(f"RAGコンテキスト生成: {len(rag_context)} 文字")

        # AI応答生成（RAGコンテキスト付き）
        full_prompt = SYSTEM_PROMPT + rag_context + f"\n\nユーザー: {user_message}"
        response = model.generate_content(full_prompt)
        ai_response = response.text

        # Notionに保存
        saved_to_notion = False
        if is_notion_active:
            try:
                now = datetime.now()
                properties = {
                    "Title": {"title": [{"text": {"content": now.strftime("%Y-%m-%d %H:%M")}}]},
                    "Date": {"date": {"start": now.isoformat()}},
                    "Type": {"select": {"name": detected_type}},
                    "Content": {"rich_text": [{"text": {"content": user_message}}]}
                }

                # 金額があれば追加
                if detected_amount:
                    properties["Amount"] = {"number": detected_amount}

                notion.pages.create(
                    parent={"database_id": NOTION_DB_ID},
                    properties=properties
                )
                saved_to_notion = True
                print(f"💾 Notionに保存: {detected_type} - {user_message[:30]}...")

            except Exception as e:
                print(f"⚠️ Notion保存エラー: {e}")

        return ChatResponse(
            response=ai_response,
            detected_type=detected_type,
            detected_amount=detected_amount,
            saved_to_notion=saved_to_notion,
            rag_used=request.use_rag and is_notion_active
        )

    except Exception as e:
        print(f"チャットエラー: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
