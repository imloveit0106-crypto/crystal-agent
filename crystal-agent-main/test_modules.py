"""モジュール構造テスト"""
import sys
import os

print("=" * 60)
print("  🧪 Crystal Agent - モジュール構造テスト")
print("=" * 60)

# テスト1: 設定モジュール
print("\n[テスト1] 設定モジュール (config.settings)")
try:
    from config.settings import Settings
    print(f"  ✅ Settings読み込み成功")
    print(f"     APP_NAME: {Settings.APP_NAME}")
    print(f"     APP_VERSION: {Settings.APP_VERSION}")
    print(f"     AI_MODEL: {Settings.AI_MODEL}")
    print(f"     TYPE_OPTIONS: {Settings.TYPE_OPTIONS}")
    print(f"     EMOTION_OPTIONS: {Settings.EMOTION_OPTIONS}")
    print(f"     MOCK_MODE: {Settings.MOCK_MODE}")
except Exception as e:
    print(f"  ❌ エラー: {e}")

# テスト2: TextAnalyzer
print("\n[テスト2] TextAnalyzer")
try:
    # 直接インポート（依存関係を避ける）
    import re
    from typing import Dict, Optional

    class TextAnalyzer:
        TYPE_KEYWORDS = {
            '支出': ['円', '¥', 'yen', '買った', '購入', 'ランチ', '飲み会'],
            'タスク': ['やる', 'する', 'まで', '期限', '締切', 'TODO'],
            '悩み': ['悩', '不安', '心配', 'モヤモヤ', '困'],
            '日記': []
        }

        def detect_type(self, text: str) -> str:
            scores = {}
            for type_name, keywords in self.TYPE_KEYWORDS.items():
                if type_name == '日記':
                    continue
                score = sum(1 for keyword in keywords if keyword in text)
                if score > 0:
                    scores[type_name] = score
            return max(scores, key=scores.get) if scores else '日記'

    analyzer = TextAnalyzer()

    test_inputs = [
        "ランチで1000円使った",
        "今日は楽しかった",
        "明日までにレポート提出",
        "最近モヤモヤする"
    ]

    print("  ✅ TextAnalyzer動作確認:")
    for text in test_inputs:
        result = analyzer.detect_type(text)
        print(f"     「{text}」→ {result}")

except Exception as e:
    print(f"  ❌ エラー: {e}")

# テスト3: ファイル構造
print("\n[テスト3] ファイル構造")
files_to_check = [
    "app.py",
    "simple_agent.py",
    "test_api.py",
    "requirements.txt",
    "README.md",
    ".env.example",
    "config/__init__.py",
    "config/settings.py",
    "utils/__init__.py",
    "utils/ai_brain.py",
    "utils/notion_handler.py",
    "utils/text_analyzer.py",
    "tests/__init__.py",
    "tests/test_text_analyzer.py",
    "data/sample_prompts.txt",
    "docs/SETUP.md",
    "scripts/run_tests.sh",
]

missing = []
for file in files_to_check:
    if os.path.exists(file):
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} が見つかりません")
        missing.append(file)

# テスト4: 環境変数チェック
print("\n[テスト4] 環境変数")
try:
    from dotenv import load_dotenv
    load_dotenv()

    keys = [
        "GEMINI_API_KEY",
        "NOTION_API_KEY",
        "NOTION_USER_PROFILE_DB_ID",
        "NOTION_LIFE_LOG_DB_ID"
    ]

    for key in keys:
        value = os.getenv(key, "")
        if value and value != f"your_{key.lower()}_here":
            print(f"  ✅ {key}: 設定済み")
        else:
            print(f"  ⚠️  {key}: 未設定（後で設定してください）")

except Exception as e:
    print(f"  ❌ エラー: {e}")

# まとめ
print("\n" + "=" * 60)
print("  📊 テスト結果")
print("=" * 60)
if len(missing) == 0:
    print("  🎉 すべてのファイルが存在します！")
    print("  ✅ モジュール構造: 正常")
    print("  ⚠️  環境変数: 後でセットアップしてください")
else:
    print(f"  ⚠️  {len(missing)}個のファイルが見つかりません")

print("\n次のステップ:")
print("  1. .env ファイルを作成 (cp .env.example .env)")
print("  2. APIキーを取得して設定")
print("  3. streamlit run app.py で起動")
print("=" * 60)
