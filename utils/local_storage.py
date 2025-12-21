"""ローカルデータストレージ - JSON保存"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class LocalStorage:
    """ローカルJSONファイルでデータを永続化"""

    def __init__(self, data_dir: str = "data"):
        """
        初期化

        Args:
            data_dir: データ保存ディレクトリ
        """
        self.data_dir = data_dir
        self.profile_file = os.path.join(data_dir, "user_profile.json")
        self.logs_file = os.path.join(data_dir, "life_logs.json")

        # ディレクトリが存在しない場合は作成
        os.makedirs(data_dir, exist_ok=True)

        # 初期化
        self._init_files()

    def _init_files(self):
        """ファイルを初期化"""
        # プロフィールファイル
        if not os.path.exists(self.profile_file):
            self._save_json(self.profile_file, {})

        # ログファイル
        if not os.path.exists(self.logs_file):
            self._save_json(self.logs_file, [])

    def _load_json(self, file_path: str) -> any:
        """JSONファイルを読み込み"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"JSON読み込みエラー: {e}")
            return {} if file_path == self.profile_file else []

    def _save_json(self, file_path: str, data: any):
        """JSONファイルに保存"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"保存成功: {file_path}")
        except Exception as e:
            logger.error(f"JSON保存エラー: {e}")

    # ===== ユーザープロフィール =====

    def get_user_profile(self) -> Dict:
        """ユーザープロフィールを取得"""
        return self._load_json(self.profile_file)

    def update_user_profile(self, profile: Dict) -> bool:
        """ユーザープロフィールを更新"""
        try:
            self._save_json(self.profile_file, profile)
            return True
        except Exception as e:
            logger.error(f"プロフィール更新エラー: {e}")
            return False

    # ===== ライフログ =====

    def add_life_log(self, content: str, type_: str, amount: Optional[float] = None,
                     emotion: Optional[str] = None, date: Optional[str] = None) -> bool:
        """ライフログを追加"""
        try:
            logs = self._load_json(self.logs_file)

            log_entry = {
                "id": len(logs) + 1,
                "content": content,
                "type": type_,
                "emotion": emotion or "普通",
                "amount": amount,
                "date": date or datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }

            logs.append(log_entry)
            self._save_json(self.logs_file, logs)
            logger.info(f"ログ追加成功: {type_} - {content[:20]}...")
            return True
        except Exception as e:
            logger.error(f"ログ追加エラー: {e}")
            return False

    def get_all_logs(self) -> List[Dict]:
        """全ログを取得"""
        return self._load_json(self.logs_file)

    def get_recent_logs(self, limit: int = 10) -> List[Dict]:
        """最近のログを取得"""
        logs = self.get_all_logs()
        return logs[-limit:] if logs else []

    def search_logs(self, query: str, limit: int = 5) -> List[Dict]:
        """ログを検索（キーワードマッチング）"""
        logs = self.get_all_logs()
        matching_logs = []

        query_lower = query.lower()

        for log in logs:
            # コンテンツ、タイプ、感情でマッチング
            if (query_lower in log.get('content', '').lower() or
                query_lower in log.get('type', '').lower() or
                query_lower in log.get('emotion', '').lower()):
                matching_logs.append(log)

        # 新しい順に返す
        return matching_logs[-limit:][::-1]

    def get_logs_by_type(self, type_: str, limit: int = 10) -> List[Dict]:
        """タイプ別にログを取得"""
        logs = self.get_all_logs()
        filtered = [log for log in logs if log.get('type') == type_]
        return filtered[-limit:][::-1]

    def get_stats(self) -> Dict:
        """統計情報を取得"""
        logs = self.get_all_logs()

        if not logs:
            return {
                "total_logs": 0,
                "by_type": {},
                "by_emotion": {},
                "total_amount": 0
            }

        # タイプ別カウント
        type_counts = {}
        for log in logs:
            type_ = log.get('type', '日記')
            type_counts[type_] = type_counts.get(type_, 0) + 1

        # 感情別カウント
        emotion_counts = {}
        for log in logs:
            emotion = log.get('emotion', '普通')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        # 支出合計
        total_amount = sum(log.get('amount', 0) or 0 for log in logs)

        return {
            "total_logs": len(logs),
            "by_type": type_counts,
            "by_emotion": emotion_counts,
            "total_amount": total_amount
        }
