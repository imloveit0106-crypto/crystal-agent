"""Notion API ハンドラー"""
import os
from typing import Dict, List, Optional
from notion_client import Client
from datetime import datetime

class NotionHandler:
    def __init__(self, api_key: str, user_profile_db_id: str, life_log_db_id: str):
        self.client = Client(auth=api_key)
        self.user_profile_db_id = user_profile_db_id
        self.life_log_db_id = life_log_db_id

    def get_user_profile(self) -> Dict:
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
            print(f"Error: {e}")
            return {}

    def add_life_log(self, content: str, type_: str, amount: Optional[float] = None,
                     emotion: Optional[str] = None, date: Optional[str] = None) -> bool:
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
            return True
        except Exception as e:
            print(f"Error: {e}")
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
