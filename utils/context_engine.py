"""コンテキスト検索エンジン"""
from typing import Dict, List, Optional
import re
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ContextEngine:
    """過去ログからコンテキストを抽出するエンジン"""

    def __init__(self, storage):
        """
        初期化

        Args:
            storage: LocalStorage または NotionHandler
        """
        self.storage = storage

    def extract_keywords(self, text: str) -> List[str]:
        """テキストからキーワードを抽出"""
        # 助詞・接続詞を除外
        stop_words = ['は', 'が', 'を', 'に', 'で', 'と', 'の', 'や', 'から', 'まで',
                      'した', 'する', 'ある', 'いる', 'です', 'ます', 'でした']

        # 単語に分割（簡易版）
        words = re.findall(r'\w+', text)

        # ストップワードを除外し、2文字以上のキーワードを抽出
        keywords = [w for w in words if len(w) >= 2 and w not in stop_words]

        return keywords[:5]  # 上位5つ

    def search_similar_logs(self, user_input: str, limit: int = 3) -> List[Dict]:
        """類似ログを検索"""
        try:
            # キーワード抽出
            keywords = self.extract_keywords(user_input)

            if not keywords:
                return []

            # ログを取得
            all_logs = self.storage.get_all_logs()

            if not all_logs:
                return []

            # スコアリング
            scored_logs = []
            for log in all_logs:
                score = 0
                content = log.get('content', '').lower()

                # キーワードマッチング
                for keyword in keywords:
                    if keyword.lower() in content:
                        score += 1

                if score > 0:
                    scored_logs.append((score, log))

            # スコア順にソート
            scored_logs.sort(key=lambda x: x[0], reverse=True)

            # 上位N件を返す
            return [log for score, log in scored_logs[:limit]]

        except Exception as e:
            logger.error(f"類似ログ検索エラー: {e}")
            return []

    def get_context_for_ai(self, user_input: str, user_profile: Optional[Dict] = None) -> Dict:
        """AIに渡すコンテキストを構築"""
        context = {}

        # ユーザープロフィール
        if user_profile:
            context['profile'] = user_profile

        # 最近のログ（直近5件）
        recent_logs = self.storage.get_recent_logs(limit=5)
        if recent_logs:
            context['recent_logs'] = [
                f"{log.get('type', '日記')}: {log.get('content', '')} ({log.get('emotion', '普通')})"
                for log in recent_logs
            ]

        # 類似ログ（関連性の高い過去ログ）
        similar_logs = self.search_similar_logs(user_input, limit=3)
        if similar_logs:
            context['similar_logs'] = [
                f"{log.get('type', '日記')}: {log.get('content', '')}"
                for log in similar_logs
            ]

        return context

    def analyze_patterns(self) -> Dict:
        """ユーザーの行動パターンを分析"""
        try:
            all_logs = self.storage.get_all_logs()

            if not all_logs:
                return {}

            # よく使う言葉
            word_freq = {}
            for log in all_logs:
                keywords = self.extract_keywords(log.get('content', ''))
                for keyword in keywords:
                    word_freq[keyword] = word_freq.get(keyword, 0) + 1

            # 上位10ワード
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

            # タイプ別傾向
            type_counts = {}
            for log in all_logs:
                type_ = log.get('type', '日記')
                type_counts[type_] = type_counts.get(type_, 0) + 1

            # 感情の傾向
            emotion_counts = {}
            for log in all_logs:
                emotion = log.get('emotion', '普通')
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

            return {
                "top_words": [word for word, count in top_words],
                "type_distribution": type_counts,
                "emotion_distribution": emotion_counts,
                "total_logs": len(all_logs)
            }

        except Exception as e:
            logger.error(f"パターン分析エラー: {e}")
            return {}

    def get_spending_insights(self) -> Dict:
        """支出の分析"""
        try:
            spending_logs = self.storage.get_logs_by_type('支出', limit=100)

            if not spending_logs:
                return {}

            # 合計金額
            total = sum(log.get('amount', 0) or 0 for log in spending_logs)

            # 平均金額
            avg = total / len(spending_logs) if spending_logs else 0

            # よく買うもの
            items = {}
            for log in spending_logs:
                content = log.get('content', '')
                keywords = self.extract_keywords(content)
                for keyword in keywords:
                    items[keyword] = items.get(keyword, 0) + 1

            top_items = sorted(items.items(), key=lambda x: x[1], reverse=True)[:5]

            return {
                "total_spending": total,
                "average_spending": avg,
                "transaction_count": len(spending_logs),
                "frequent_items": [item for item, count in top_items]
            }

        except Exception as e:
            logger.error(f"支出分析エラー: {e}")
            return {}

    def get_task_insights(self) -> Dict:
        """タスクの分析"""
        try:
            task_logs = self.storage.get_logs_by_type('タスク', limit=100)

            if not task_logs:
                return {}

            # タスクのキーワード頻度
            task_keywords = {}
            for log in task_logs:
                content = log.get('content', '')
                keywords = self.extract_keywords(content)
                for keyword in keywords:
                    task_keywords[keyword] = task_keywords.get(keyword, 0) + 1

            top_tasks = sorted(task_keywords.items(), key=lambda x: x[1], reverse=True)[:5]

            return {
                "total_tasks": len(task_logs),
                "frequent_tasks": [task for task, count in top_tasks]
            }

        except Exception as e:
            logger.error(f"タスク分析エラー: {e}")
            return {}
