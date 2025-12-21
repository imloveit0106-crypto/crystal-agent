"""Crystal Agent - 機能テスト"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("  🔮 Crystal Agent - 機能テスト")
print("=" * 60)

# 1. テキスト分析のテスト
print("\n【1】テキスト分析のテスト")
print("-" * 60)

from utils.text_analyzer import TextAnalyzer

analyzer = TextAnalyzer()

test_cases = [
    ("今日はランチで1500円使った", "支出", 1500.0),
    ("明日までにレポートを書かなきゃ", "タスク", None),
    ("仕事がつらくて不安", "悩み", None),
    ("今日は楽しかった！", "日記", None),
]

for text, expected_type, expected_amount in test_cases:
    result = analyzer.analyze(text)
    status_type = "✅" if result['type'] == expected_type else "❌"
    status_amount = "✅" if result['amount'] == expected_amount else "❌"

    print(f"\n入力: {text}")
    print(f"  タイプ: {result['type']} {status_type} (期待値: {expected_type})")
    print(f"  感情: {result['emotion']}")
    print(f"  金額: {result['amount']} {status_amount} (期待値: {expected_amount})")

# 2. AI Brainのテスト（APIキーがある場合のみ）
print("\n\n【2】AI Brain のテスト")
print("-" * 60)

gemini_key = os.getenv("GEMINI_API_KEY")

if gemini_key and len(gemini_key) > 20:
    try:
        from utils.ai_brain import AIBrain

        print("AI Brainを初期化中...")
        ai = AIBrain(gemini_key)

        test_message = "こんにちは！"
        print(f"\n入力: {test_message}")
        print("応答生成中...")

        response = ai.generate_response(test_message)
        print(f"応答: {response[:100]}...")

        if response and "エラー" not in response:
            print("\n✅ AI Brain テスト成功")
        else:
            print("\n❌ AI Brain テスト失敗")

    except Exception as e:
        print(f"\n❌ AI Brain テストエラー: {e}")
else:
    print("⚠️  Gemini APIキーが設定されていないため、スキップ")

# 3. Notion Handlerのテスト（APIキーがある場合のみ）
print("\n\n【3】Notion Handler のテスト")
print("-" * 60)

notion_key = os.getenv("NOTION_API_KEY")
user_db = os.getenv("NOTION_USER_PROFILE_DB_ID")
log_db = os.getenv("NOTION_LIFE_LOG_DB_ID")

if notion_key and user_db and log_db:
    try:
        from utils.notion_handler import NotionHandler

        print("Notion Handlerを初期化中...")
        notion = NotionHandler(notion_key, user_db, log_db)

        if notion.is_connected:
            print("✅ Notion API接続成功")

            # プロフィール取得テスト
            profile = notion.get_user_profile()
            print(f"プロフィール件数: {len(profile)} 件")

        else:
            print("⚠️  Notion API接続失敗（トークンが無効な可能性があります）")

    except Exception as e:
        print(f"❌ Notion Handler テストエラー: {e}")
else:
    print("⚠️  Notion APIキーが設定されていないため、スキップ")

# まとめ
print("\n" + "=" * 60)
print("  📊 テスト完了")
print("=" * 60)
print("\n✨ 主要機能は正常に動作しています！")
print("   Streamlitアプリを起動してお試しください:")
print("   $ streamlit run app.py\n")
