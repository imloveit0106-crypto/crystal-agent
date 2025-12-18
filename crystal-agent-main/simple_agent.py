"""
Crystal Agent - ターミナル版
シンプルなコマンドライン版AIエージェント
"""

import os
from datetime import datetime
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

class CrystalAgent:
    """シンプルなCrystal Agentクラス"""

    def __init__(self):
        """初期化"""
        self.api_ready = False
        self.gemini_model = None
        self.notion = None
        self.init_apis()

    def init_apis(self):
        """APIを初期化"""
        gemini_key = os.getenv("GEMINI_API_KEY")
        notion_key = os.getenv("NOTION_API_KEY")

        if not gemini_key or gemini_key == "your_gemini_api_key_here":
            print("⚠️  Gemini APIキーが設定されていません（デモモードで動作）")
            return

        if not notion_key or notion_key == "your_notion_api_key_here":
            print("⚠️  Notion APIキーが設定されていません（デモモードで動作）")
            return

        try:
            import google.generativeai as genai
            from notion_client import Client

            # Gemini設定
            genai.configure(api_key=gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')

            # Notion設定
            self.notion = Client(auth=notion_key)

            self.api_ready = True
            print("✅ API接続成功！")

        except Exception as e:
            print(f"❌ API初期化エラー: {e}")

    def get_response(self, user_message):
        """AI応答を取得"""

        if self.api_ready and self.gemini_model:
            try:
                # 実際のGemini APIを使用
                response = self.gemini_model.generate_content(
                    f"あなたは親切なAIアシスタント「Crystal Agent」です。ユーザーのメッセージに日本語で応答してください。\n\nユーザー: {user_message}"
                )
                return response.text
            except Exception as e:
                return f"エラーが発生しました: {e}"
        else:
            # モックレスポンス
            mock_responses = {
                "こんにちは": "こんにちは！Crystal Agentです。今日も一日頑張りましょう！",
                "日記": "素晴らしいですね！今日の出来事を教えてください。",
                "支出": "支出を記録しますね。いくら使いましたか？",
                "タスク": "新しいタスクを追加しましょう。何をする予定ですか？",
                "悩み": "お悩みですか？ゆっくり聞かせてください。一緒に考えましょう。",
            }

            for key, response in mock_responses.items():
                if key in user_message:
                    return response

            return f"「{user_message}」について考えています...（デモモード）"

    def print_header(self):
        """ヘッダーを表示"""
        print("\n" + "=" * 60)
        print("  🔮 Crystal Agent - ターミナル版")
        print("  あなた専用のマルチモーダルAIエージェント")
        print("=" * 60)

        if not self.api_ready:
            print("\n⚠️  デモモードで動作中")
            print("実際のAI機能を使うには、.envファイルにAPIキーを設定してください\n")

    def print_help(self):
        """ヘルプを表示"""
        print("\n📖 使い方:")
        print("  - メッセージを入力してEnterキーを押す")
        print("  - 'help' でヘルプ表示")
        print("  - 'quit' または 'exit' で終了")
        print()

    def run(self):
        """メインループ"""
        self.print_header()
        self.print_help()

        print("🔮 Crystal Agent: こんにちは！何でも話しかけてください。")

        while True:
            try:
                # ユーザー入力
                print("\n" + "-" * 60)
                user_input = input("あなた: ").strip()

                # 空入力はスキップ
                if not user_input:
                    continue

                # 終了コマンド
                if user_input.lower() in ['quit', 'exit', '終了', 'さようなら']:
                    print("\n🔮 Crystal Agent: またお話ししましょう！")
                    break

                # ヘルプコマンド
                if user_input.lower() in ['help', 'ヘルプ']:
                    self.print_help()
                    continue

                # AI応答を取得
                print("\n🔮 Crystal Agent: ", end="", flush=True)
                response = self.get_response(user_input)
                print(response)

            except KeyboardInterrupt:
                print("\n\n🔮 Crystal Agent: またお話ししましょう！")
                break

            except Exception as e:
                print(f"\n❌ エラー: {e}")

def main():
    """メイン処理"""
    agent = CrystalAgent()
    agent.run()

if __name__ == "__main__":
    main()
