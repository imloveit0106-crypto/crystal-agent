"""Notion API ハンドラー"""
import os
from typing import Dict, List, Optional
from notion_client import Client
from datetime import datetime
import logging

# ロギング設定
logger = logging.getLogger(__name__)

class NotionHandler:
    def __init__(self, api_key: str, user_profile_db_id: str, life_log_db_id: str):
        """
        Notion APIハンドラーを初期化

        Args:
            api_key: Notion APIキー
            user_profile_db_id: User ProfileデータベースID
            life_log_db_id: Life LogデータベースID
        """
        self.client = Client(auth=api_key)
        self.user_profile_db_id = user_profile_db_id
        self.life_log_db_id = life_log_db_id
        self.is_connected = self._test_connection()

    def _test_connection(self) -> bool:
        """Notion APIへの接続をテスト"""
        try:
            self.client.users.me()
            logger.info("Notion API接続成功")
            return True
        except Exception as e:
            logger.warning(f"Notion API接続失敗: {e}")
            return False

    def get_user_profile(self) -> Dict:
        """ユーザープロフィールを取得"""
        if not self.is_connected:
            logger.warning("Notion未接続のため、プロフィールを取得できません")
            return {}

        try:
            results = self.client.databases.query(database_id=self.user_profile_db_id)
            profile = {}
            for page in results.get('results', []):
                properties = page.get('properties', {})
                key = self._extract_title(properties.get('Key', {}))
                value = self._extract_rich_text(properties.get('Value', {}))
                if key and value:
                    profile[key] = value
            return profile
        except Exception as e:
            logger.error(f"プロフィール取得エラー: {e}")
            return {}

    def add_life_log(self, content: str, type_: str, amount: Optional[float] = None,
                     emotion: Optional[str] = None, date: Optional[str] = None) -> bool:
        """ライフログを追加"""
        if not self.is_connected:
            logger.warning("Notion未接続のため、ログを保存できません（ローカルには記録されています）")
            return False

        try:
            properties = {
                'Content': {'title': [{'text': {'content': content}}]},
                'Type': {'select': {'name': type_}}
            }
            if amount is not None:
                properties['Amount'] = {'number': amount}
            if emotion:
                properties['Emotion'] = {'select': {'name': emotion}}
            if date:
                properties['Date'] = {'date': {'start': date}}
            else:
                properties['Date'] = {'date': {'start': datetime.now().isoformat()}}

            self.client.pages.create(
                parent={'database_id': self.life_log_db_id},
                properties=properties
            )
            logger.info(f"ログ保存成功: {type_} - {content[:20]}...")
            return True
        except Exception as e:
            logger.error(f"ログ保存エラー: {e}")
            return False

    def _extract_title(self, prop: Dict) -> str:
        try:
            return prop.get('title', [{}])[0].get('plain_text', '')
        except (IndexError, KeyError):
            return ''

    def _extract_rich_text(self, prop: Dict) -> str:
        try:
            return prop.get('rich_text', [{}])[0].get('plain_text', '')
        except (IndexError, KeyError):
            return ''
