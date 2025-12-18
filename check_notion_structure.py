"""Notionデータベース構造チェック"""
import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

print("=" * 60)
print("  🔍 Notion データベース構造チェック")
print("=" * 60)

api_key = os.getenv("NOTION_API_KEY")
life_log_db_id = os.getenv("NOTION_LIFE_LOG_DB_ID")
user_profile_db_id = os.getenv("NOTION_USER_PROFILE_DB_ID")

if not api_key:
    print("❌ NOTION_API_KEY が設定されていません")
    exit(1)

notion = Client(auth=api_key)

# Life_Log データベース
print("\n[Life_Log データベース]")
print(f"ID: {life_log_db_id}")

try:
    db = notion.databases.retrieve(database_id=life_log_db_id)
    print(f"✅ タイトル: {db['title'][0]['plain_text']}")

    print("\nプロパティ一覧:")
    for prop_name, prop_data in db['properties'].items():
        prop_type = prop_data['type']
        print(f"  • {prop_name}: {prop_type}")

        # セレクトの場合、オプションを表示
        if prop_type == 'select' and 'select' in prop_data:
            options = prop_data['select'].get('options', [])
            if options:
                print(f"    オプション: {[opt['name'] for opt in options]}")

    # 必要なプロパティをチェック
    required_props = {
        'Content': 'title',
        'Type': 'select',
        'Amount': 'number',
        'Emotion': 'select',
        'Date': 'date'
    }

    print("\n必要なプロパティのチェック:")
    missing = []
    wrong_type = []

    for prop_name, expected_type in required_props.items():
        if prop_name in db['properties']:
            actual_type = db['properties'][prop_name]['type']
            if actual_type == expected_type:
                print(f"  ✅ {prop_name} ({actual_type})")
            else:
                print(f"  ⚠️  {prop_name} - タイプ不一致: 期待={expected_type}, 実際={actual_type}")
                wrong_type.append(prop_name)
        else:
            print(f"  ❌ {prop_name} - 存在しません")
            missing.append(prop_name)

    # サマリー
    print("\n" + "=" * 60)
    print("  📊 チェック結果")
    print("=" * 60)

    if not missing and not wrong_type:
        print("✅ すべてのプロパティが正しく設定されています！")
    else:
        if missing:
            print(f"❌ 不足しているプロパティ: {', '.join(missing)}")
        if wrong_type:
            print(f"⚠️  タイプが異なるプロパティ: {', '.join(wrong_type)}")

except Exception as e:
    print(f"❌ エラー: {e}")

# User_Profile データベース
print("\n\n[User_Profile データベース]")
print(f"ID: {user_profile_db_id}")

try:
    db = notion.databases.retrieve(database_id=user_profile_db_id)
    print(f"✅ タイトル: {db['title'][0]['plain_text']}")

    print("\nプロパティ一覧:")
    for prop_name, prop_data in db['properties'].items():
        prop_type = prop_data['type']
        print(f"  • {prop_name}: {prop_type}")

    # 必要なプロパティをチェック
    required_props = {
        'Key': 'title',
        'Value': 'rich_text'
    }

    print("\n必要なプロパティのチェック:")
    missing = []

    for prop_name, expected_type in required_props.items():
        if prop_name in db['properties']:
            actual_type = db['properties'][prop_name]['type']
            if actual_type == expected_type:
                print(f"  ✅ {prop_name} ({actual_type})")
            else:
                print(f"  ⚠️  {prop_name} - タイプ不一致: 期待={expected_type}, 実際={actual_type}")
        else:
            print(f"  ❌ {prop_name} - 存在しません")
            missing.append(prop_name)

    print("\n" + "=" * 60)
    if not missing:
        print("✅ すべてのプロパティが正しく設定されています！")
    else:
        print(f"❌ 不足しているプロパティ: {', '.join(missing)}")

except Exception as e:
    print(f"❌ エラー: {e}")

print("\n" + "=" * 60)
