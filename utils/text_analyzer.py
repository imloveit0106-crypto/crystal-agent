"""テキスト分析ユーティリティ"""
import re
from typing import Dict, Optional

class TextAnalyzer:
    # ログタイプ判定用キーワード（優先度順）
    TYPE_KEYWORDS = {
        '支出': [
            '円', '¥', 'yen', '買った', '購入', 'ランチ', '飲み会',
            '使った', '払った', 'ディナー', 'カフェ', 'コーヒー',
            'コンビニ', 'スーパー', '食費', '交通費', '本', '服',
            '美容院', '化粧品', 'ガソリン', '映画', 'Netflix'
        ],
        'タスク': [
            'やる', 'する', 'しなきゃ', 'せねば', 'まで', '期限',
            '締切', 'TODO', 'ToDo', 'todo', '提出', '完成', '終わらせ',
            '作る', '書く', '読む', '勉強', '準備', '片付け',
            '掃除', '洗濯', '買い物リスト', 'やること', '予定'
        ],
        '悩み': [
            '悩', '不安', '心配', 'モヤモヤ', '困', 'つらい', '辛い',
            '悲しい', '寂しい', 'ストレス', 'イライラ', '落ち込',
            'どうしよう', '分からない', 'わからない', '迷',
            '失敗', 'ミス', '後悔', '嫌', 'しんどい'
        ],
        '日記': []  # デフォルト
    }

    # 感情分析用キーワード
    EMOTION_KEYWORDS = {
        '良好': [
            '嬉しい', '楽しい', '最高', '良い', 'よい', 'いい',
            'ハッピー', '幸せ', '満足', '達成', 'できた', '成功',
            'ワクワク', 'ドキドキ', '感謝', 'ありがとう', '素敵',
            '美味しい', 'おいしい', '快適', '気持ちいい'
        ],
        '疲労': [
            '疲れ', 'しんどい', 'きつい', '眠い', 'だるい',
            '忙しい', 'バタバタ', 'ヘトヘト', 'クタクタ',
            '寝不足', '休みたい', '限界', 'もう無理'
        ],
        '悩み': [
            '悩', '不安', '心配', 'つらい', '辛い', '悲しい',
            'ストレス', 'イライラ', '落ち込', 'モヤモヤ',
            '迷', '困', '嫌', '寂しい'
        ],
        '普通': []  # デフォルト
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
        """金額を抽出（複数パターン対応）"""
        # パターン1: 1000円、1,000円、1000.5円
        pattern1 = r'(\d+(?:,\d{3})*(?:\.\d+)?)円'
        match1 = re.search(pattern1, text)
        if match1:
            return float(match1.group(1).replace(',', ''))

        # パターン2: ¥1000、¥1,000
        pattern2 = r'¥(\d+(?:,\d{3})*(?:\.\d+)?)'
        match2 = re.search(pattern2, text)
        if match2:
            return float(match2.group(1).replace(',', ''))

        # パターン3: 半角数字のみ（4桁以上の場合のみ金額と判定）
        pattern3 = r'(\d{4,})(?![\d])'
        match3 = re.search(pattern3, text)
        if match3 and any(keyword in text for keyword in ['買', '購入', '使', '払']):
            return float(match3.group(1))

        return None
