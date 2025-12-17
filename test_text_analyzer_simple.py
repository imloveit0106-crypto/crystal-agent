"""TextAnalyzer の簡易テスト"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# 直接インポート
import re
from typing import Dict, Optional

class TextAnalyzer:
    TYPE_KEYWORDS = {
        '支出': ['円', '¥', 'yen', '買った', '購入', 'ランチ', '飲み会'],
        'タスク': ['やる', 'する', 'まで', '期限', '締切', 'TODO'],
        '悩み': ['悩', '不安', '心配', 'モヤモヤ', '困'],
        '日記': []
    }

    EMOTION_KEYWORDS = {
        '良好': ['嬉しい', '楽しい', '最高', '良い'],
        '疲労': ['疲れ', 'しんどい', 'きつい', '眠い'],
        '悩み': ['悩', '不安', '心配'],
        '普通': []
    }

    def analyze(self, text: str) -> Dict:
        return {
            'type': self.detect_type(text),
            'emotion': self.detect_emotion(text),
            'amount': self.extract_amount(text),
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

    def detect_emotion(self, text: str) -> str:
        scores = {}
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            if emotion == '普通':
                continue
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[emotion] = score
        return max(scores, key=scores.get) if scores else '普通'

    def extract_amount(self, text: str) -> Optional[float]:
        pattern1 = r'(\d+(?:,\d{3})*(?:\.\d+)?)円'
        match1 = re.search(pattern1, text)
        if match1:
            return float(match1.group(1).replace(',', ''))
        return None

# テスト実行
print("=" * 60)
print("  🧪 TextAnalyzer テスト")
print("=" * 60)

analyzer = TextAnalyzer()

test_cases = [
    ("ランチで1000円使った", "支出", "普通", 1000.0),
    ("今日は嬉しい", "日記", "良好", None),
    ("明日までに資料作成する", "タスク", "普通", None),
    ("最近疲れてる", "日記", "疲労", None),
    ("悩みがある", "悩み", "悩み", None),
]

passed = 0
failed = 0

for i, (text, expected_type, expected_emotion, expected_amount) in enumerate(test_cases, 1):
    result = analyzer.analyze(text)

    type_ok = result['type'] == expected_type
    emotion_ok = result['emotion'] == expected_emotion
    amount_ok = result['amount'] == expected_amount

    if type_ok and emotion_ok and amount_ok:
        print(f"\n✅ テスト{i}: 成功")
        passed += 1
    else:
        print(f"\n❌ テスト{i}: 失敗")
        failed += 1

    print(f"   入力: {text}")
    print(f"   期待: タイプ={expected_type}, 感情={expected_emotion}, 金額={expected_amount}")
    print(f"   結果: タイプ={result['type']}, 感情={result['emotion']}, 金額={result['amount']}")
    if not type_ok:
        print(f"   ❌ タイプが不一致")
    if not emotion_ok:
        print(f"   ❌ 感情が不一致")
    if not amount_ok:
        print(f"   ❌ 金額が不一致")

print("\n" + "=" * 60)
print(f"  📊 結果: {passed}件成功 / {failed}件失敗")
print("=" * 60)

if failed == 0:
    print("\n🎉 すべてのテストが成功しました！")
else:
    print(f"\n⚠️  {failed}件のテストが失敗しました。")
