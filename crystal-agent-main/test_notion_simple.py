"""Notion API 簡易テスト"""
import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

print("=" * 50)
print("  📝 Notion API 接続テスト")
print("=" * 50)

api_key = os.getenv("NOTION_API_KEY")
user_db_id = os.getenv("NOTION_USER_PROFILE_DB_ID")
log_db_id = os.getenv("NOTION_LIFE_LOG_DB_ID")

if not api_key:
    print("❌ NOTION_API_KEY が設定されていません")
    exit(1)

try:
    notion = Client(auth=api_key)

    # 自分の情報を取得
    me = notion.users.me()
    print(f"✅ Notion API 接続成功！")
    print(f"   ユーザー: {me.get('name', 'Unknown')}")

    # User Profile DBをクエリ
    if user_db_id:
        print(f"\n📊 User Profile DB をクエリ中...")
        results = notion.databases.query(database_id=user_db_id)
        print(f"   取得件数: {len(results.get('results', []))} 件")

    # Life Log DBをクエリ
    if log_db_id:
        print(f"\n📊 Life Log DB をクエリ中...")
        results = notion.databases.query(database_id=log_db_id)
        print(f"   取得件数: {len(results.get('results', []))} 件")

    print("\n🎉 Notion接続テスト完了！")

except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()

print("=" * 50)
