"""
Notion API Service - Singleton Implementation
Provides async interface to Notion API with proper error handling
"""

import os
from typing import Optional, Dict, Any, List
from datetime import datetime
from notion_client import Client, APIResponseError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotionService:
    """
    Singleton Notion API Client
    Handles all interactions with Notion API
    """
    _instance: Optional['NotionService'] = None
    _client: Optional[Client] = None
    _database_id: Optional[str] = None
    _is_active: bool = False

    def __new__(cls):
        """Singleton pattern: ensure only one instance exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize Notion client if not already initialized"""
        if self._client is None:
            self._initialize()

    def _initialize(self):
        """
        Initialize Notion client with environment variables
        Implements Graceful Degradation: warns but doesn't crash if missing
        """
        api_key = os.getenv("NOTION_API_KEY")
        # Support multiple environment variable names for flexibility
        database_id = os.getenv("NOTION_DATABASE_ID") or os.getenv("NOTION_LIFE_LOG_DB_ID")

        if not api_key:
            logger.warning("⚠️ NOTION_API_KEY not found in environment. Notion features will be disabled.")
            self._is_active = False
            return

        if not database_id:
            logger.warning("⚠️ NOTION_DATABASE_ID not found in environment. Notion features will be disabled.")
            self._is_active = False
            return

        try:
            self._client = Client(auth=api_key)
            self._database_id = database_id

            # Test connection by retrieving database info
            db_info = self._client.databases.retrieve(database_id=database_id)
            db_name = db_info.get('title', [{}])[0].get('plain_text', 'N/A')

            self._is_active = True
            logger.info(f"✓ Notion API connected successfully")
            logger.info(f"  └─ Database: {db_name}")
            logger.info(f"  └─ Database ID: {database_id[:8]}...")

        except APIResponseError as e:
            logger.error(f"❌ Notion API connection failed: {e.code}")
            logger.error(f"  └─ Message: {e.message}")
            self._is_active = False

        except Exception as e:
            logger.error(f"❌ Unexpected error initializing Notion: {type(e).__name__}")
            logger.error(f"  └─ Details: {str(e)}")
            self._is_active = False

    @property
    def is_active(self) -> bool:
        """Check if Notion service is active and ready"""
        return self._is_active

    async def add_expense(
        self,
        item: str,
        amount: int,
        category: str
    ) -> Dict[str, Any]:
        """
        Add an expense entry to Notion database

        Args:
            item: Description of the expense item
            amount: Amount in yen (positive integer)
            category: Category/type (e.g., "支出", "食費", "交通費")

        Returns:
            Dict containing:
                - success: bool
                - page_url: Optional[str]
                - error: Optional[str]
        """
        if not self._is_active:
            return {
                "success": False,
                "page_url": None,
                "error": "Notion service is not active"
            }

        try:
            # Construct strict JSON payload for Notion API
            now = datetime.now()
            properties = {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": item
                            }
                        }
                    ]
                },
                "Amount": {
                    "number": amount
                },
                "Type": {
                    "select": {
                        "name": category
                    }
                },
                "Date": {
                    "date": {
                        "start": now.isoformat()
                    }
                },
                "Content": {
                    "rich_text": [
                        {
                            "text": {
                                "content": f"{item} - ¥{amount:,}"
                            }
                        }
                    ]
                }
            }

            # Create page in Notion database
            response = self._client.pages.create(
                parent={"database_id": self._database_id},
                properties=properties
            )

            page_url = response.get("url", "")
            page_id = response.get("id", "")

            logger.info(f"✓ Expense added to Notion: {item} (¥{amount:,})")
            logger.info(f"  └─ Page ID: {page_id[:8]}...")

            return {
                "success": True,
                "page_url": page_url,
                "page_id": page_id,
                "error": None
            }

        except APIResponseError as e:
            logger.error(f"❌ Notion API error while adding expense: {e.code}")
            logger.error(f"  └─ Message: {e.message}")
            return {
                "success": False,
                "page_url": None,
                "error": f"Notion API error: {e.message}"
            }

        except Exception as e:
            logger.error(f"❌ Unexpected error while adding expense: {type(e).__name__}")
            logger.error(f"  └─ Details: {str(e)}")
            return {
                "success": False,
                "page_url": None,
                "error": f"Unexpected error: {str(e)}"
            }

    async def add_entry(
        self,
        title: str,
        content: str,
        entry_type: str,
        amount: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generic method to add any type of entry to Notion

        Args:
            title: Entry title (usually timestamp)
            content: Main content of the entry
            entry_type: Type/category (e.g., "日記", "タスク", "支出")
            amount: Optional amount for expense entries

        Returns:
            Dict containing success status, page_url, and error
        """
        if not self._is_active:
            return {
                "success": False,
                "page_url": None,
                "error": "Notion service is not active"
            }

        try:
            now = datetime.now()
            properties = {
                "Title": {
                    "title": [{"text": {"content": title}}]
                },
                "Date": {
                    "date": {"start": now.isoformat()}
                },
                "Type": {
                    "select": {"name": entry_type}
                },
                "Content": {
                    "rich_text": [{"text": {"content": content}}]
                }
            }

            # Add amount if provided
            if amount is not None:
                properties["Amount"] = {"number": amount}

            response = self._client.pages.create(
                parent={"database_id": self._database_id},
                properties=properties
            )

            page_url = response.get("url", "")
            page_id = response.get("id", "")

            logger.info(f"✓ Entry added to Notion: {entry_type} - {content[:30]}...")
            logger.info(f"  └─ Page ID: {page_id[:8]}...")

            return {
                "success": True,
                "page_url": page_url,
                "page_id": page_id,
                "error": None
            }

        except APIResponseError as e:
            logger.error(f"❌ Notion API error: {e.code} - {e.message}")
            return {
                "success": False,
                "page_url": None,
                "error": f"Notion API error: {e.message}"
            }

        except Exception as e:
            logger.error(f"❌ Unexpected error: {type(e).__name__} - {str(e)}")
            return {
                "success": False,
                "page_url": None,
                "error": f"Unexpected error: {str(e)}"
            }

    async def query_entries(
        self,
        entry_type: Optional[str] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Query entries from Notion database

        Args:
            entry_type: Optional filter by type (e.g., "日記", "タスク")
            limit: Maximum number of entries to retrieve

        Returns:
            Dict containing success status, entries list, and error
        """
        if not self._is_active:
            return {
                "success": False,
                "entries": [],
                "error": "Notion service is not active"
            }

        try:
            # Build filter if type is specified
            filter_obj = None
            if entry_type:
                filter_obj = {
                    "property": "Type",
                    "select": {
                        "equals": entry_type
                    }
                }

            # Query database
            response = self._client.databases.query(
                database_id=self._database_id,
                filter=filter_obj,
                sorts=[
                    {
                        "property": "Date",
                        "direction": "descending"
                    }
                ],
                page_size=min(limit, 100)
            )

            entries = []
            for page in response.get("results", []):
                props = page.get("properties", {})

                # Extract title
                title_prop = props.get("Title", {})
                title = ""
                if title_prop.get("title") and len(title_prop["title"]) > 0:
                    title = title_prop["title"][0].get("plain_text", "")

                # Extract content
                content_prop = props.get("Content", {})
                content = ""
                if content_prop.get("rich_text") and len(content_prop["rich_text"]) > 0:
                    content = content_prop["rich_text"][0].get("plain_text", "")

                # Extract type
                type_prop = props.get("Type", {})
                type_name = ""
                if type_prop.get("select"):
                    type_name = type_prop["select"]["name"]

                # Extract date
                date_prop = props.get("Date", {})
                date = ""
                if date_prop.get("date"):
                    date = date_prop["date"]["start"]

                # Extract amount if exists
                amount_prop = props.get("Amount", {})
                amount = amount_prop.get("number")

                entries.append({
                    "title": title,
                    "content": content,
                    "type": type_name,
                    "date": date,
                    "amount": amount
                })

            logger.info(f"✓ Retrieved {len(entries)} entries from Notion")

            return {
                "success": True,
                "entries": entries,
                "total": len(entries),
                "error": None
            }

        except APIResponseError as e:
            logger.error(f"❌ Notion API error while querying: {e.code} - {e.message}")
            return {
                "success": False,
                "entries": [],
                "error": f"Notion API error: {e.message}"
            }

        except Exception as e:
            logger.error(f"❌ Unexpected error while querying: {type(e).__name__} - {str(e)}")
            return {
                "success": False,
                "entries": [],
                "error": f"Unexpected error: {str(e)}"
            }


# Singleton instance accessor
def get_notion_service() -> NotionService:
    """Get the singleton NotionService instance"""
    return NotionService()
