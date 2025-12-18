"""テキスト分析ユーティリティ"""
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
