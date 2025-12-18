"""
Crystal Agent - API接続テスト
このスクリプトでGemini APIとNotion APIの接続をテストします
"""

import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

def print_header(text):
    """見やすいヘッダーを表示"""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)

def test_gemini_api():
    """Gemini API接続テスト"""
    print_header("🤖 Gemini API 接続テスト")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ GEMINI_API_KEY が設定されていません")
        print("   .env ファイルにAPIキーを設定してください")
        return False

    try:
        import google.generativeai as genai

        # API設定
        genai.configure(api_key=api_key)

        # 簡単なテスト
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("こんにちは！元気ですか？")

        print("✅ Gemini API 接続成功！")
        print(f"   レスポンス: {response.text[:50]}...")
        return True

    except Exception as e:
        print(f"❌ Gemini API 接続失敗: {e}")
        return False

def test_notion_api():
    """Notion API接続テスト"""
    print_header("📝 Notion API 接続テスト")

    api_key = os.getenv("NOTION_API_KEY")
    user_db_id = os.getenv("NOTION_USER_PROFILE_DB_ID")
    log_db_id = os.getenv("NOTION_LIFE_LOG_DB_ID")

    if not api_key or api_key == "your_notion_api_key_here":
        print("❌ NOTION_API_KEY が設定されていません")
        print("   .env ファイルにAPIキーを設定してください")
        return False

    if not user_db_id or user_db_id == "your_user_profile_database_id_here":
        print("⚠️  User Profile データベースIDが設定されていません")
        print("   後で .env ファイルに設定してください")

    if not log_db_id or log_db_id == "your_life_log_database_id_here":
        print("⚠️  Life Log データベースIDが設定されていません")
        print("   後で .env ファイルに設定してください")

    try:
        from notion_client import Client

        # Notionクライアント作成
        notion = Client(auth=api_key)

        # 自分の情報を取得してテスト
        me = notion.users.me()

        print("✅ Notion API 接続成功！")
        print(f"   ユーザー: {me.get('name', 'Unknown')}")
        return True

    except Exception as e:
        print(f"❌ Notion API 接続失敗: {e}")
        return False

def main():
    """メイン処理"""
    print("\n🔮 Crystal Agent - API接続テスト開始")
    print("=" * 50)

    # テスト実行
    gemini_ok = test_gemini_api()
    notion_ok = test_notion_api()

    # 結果サマリー
    print_header("📊 テスト結果サマリー")
    print(f"Gemini API: {'✅ 成功' if gemini_ok else '❌ 失敗'}")
    print(f"Notion API: {'✅ 成功' if notion_ok else '❌ 失敗'}")

    if gemini_ok and notion_ok:
        print("\n🎉 すべてのAPI接続に成功しました！")
        print("   次は 'streamlit run app.py' でアプリを起動してください")
    else:
        print("\n⚠️  一部のAPIに接続できませんでした")
        print("   .env ファイルを確認してください")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
