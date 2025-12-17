"""
Crystal Agent - 実際のAPI接続テスト
"""

import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

def print_header(text):
    """見やすいヘッダーを表示"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_environment():
    """環境変数テスト"""
    print_header("🔑 環境変数チェック")

    keys = {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "NOTION_API_KEY": os.getenv("NOTION_API_KEY"),
        "NOTION_USER_PROFILE_DB_ID": os.getenv("NOTION_USER_PROFILE_DB_ID"),
        "NOTION_LIFE_LOG_DB_ID": os.getenv("NOTION_LIFE_LOG_DB_ID"),
    }

    all_set = True
    for key, value in keys.items():
        if value and value != f"your_{key.lower()}_here":
            # 最初の10文字だけ表示（セキュリティのため）
            masked = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {key}: {masked}")
        else:
            print(f"❌ {key}: 未設定")
            all_set = False

    return all_set

def test_notion_api():
    """Notion API接続テスト（簡易版）"""
    print_header("📝 Notion API 接続テスト")

    api_key = os.getenv("NOTION_API_KEY")
    user_db_id = os.getenv("NOTION_USER_PROFILE_DB_ID")

    if not api_key:
        print("❌ NOTION_API_KEY が設定されていません")
        return False

    try:
        from notion_client import Client

        # Notionクライアント作成
        notion = Client(auth=api_key)

        # 自分の情報を取得してテスト
        me = notion.users.me()

        print("✅ Notion API 接続成功！")
        print(f"   Bot: {me.get('name', 'Unknown')}")
        print(f"   Type: {me.get('type', 'Unknown')}")

        # データベースにアクセスしてみる
        if user_db_id:
            try:
                db = notion.databases.retrieve(database_id=user_db_id)
                print(f"✅ User Profile DB アクセス成功！")
                print(f"   タイトル: {db.get('title', [{}])[0].get('plain_text', 'Unknown')}")
            except Exception as e:
                print(f"⚠️  User Profile DB アクセス失敗: {e}")
                print(f"   ※ データベースに「Crystal Agent」を接続してください")

        return True

    except Exception as e:
        print(f"❌ Notion API 接続失敗: {e}")
        return False

def test_gemini_api():
    """Gemini API接続テスト（簡易版）"""
    print_header("🤖 Gemini API 接続テスト")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ GEMINI_API_KEY が設定されていません")
        return False

    try:
        import google.generativeai as genai

        # API設定
        genai.configure(api_key=api_key)

        # 簡単なテスト
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("こんにちは！元気ですか？")

        print("✅ Gemini API 接続成功！")
        print(f"   レスポンス: {response.text[:100]}...")
        return True

    except Exception as e:
        print(f"❌ Gemini API 接続失敗: {e}")
        return False

def main():
    """メイン処理"""
    print("\n🔮 Crystal Agent - 実際のAPI接続テスト開始")
    print("=" * 60)

    # 環境変数チェック
    env_ok = test_environment()

    if not env_ok:
        print("\n⚠️  環境変数が正しく設定されていません")
        print("   .env ファイルを確認してください")
        return

    # テスト実行
    notion_ok = test_notion_api()
    gemini_ok = test_gemini_api()

    # 結果サマリー
    print_header("📊 テスト結果サマリー")
    print(f"環境変数: {'✅ 成功' if env_ok else '❌ 失敗'}")
    print(f"Notion API: {'✅ 成功' if notion_ok else '❌ 失敗'}")
    print(f"Gemini API: {'✅ 成功' if gemini_ok else '❌ 失敗'}")

    if env_ok and notion_ok and gemini_ok:
        print("\n🎉 すべてのAPI接続に成功しました！")
        print("   次は 'streamlit run app.py' でアプリを起動してください")
    else:
        print("\n⚠️  一部のAPIに接続できませんでした")
        print("   上記のエラーメッセージを確認してください")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
