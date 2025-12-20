"""設定ファイル"""
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    APP_NAME = "Crystal Agent"
    APP_VERSION = "1.0.0"  # Production-ready with streaming chat
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
    USER_PROFILE_DB_ID = os.getenv("NOTION_USER_PROFILE_DB_ID", "")
    LIFE_LOG_DB_ID = os.getenv("NOTION_LIFE_LOG_DB_ID", "")
    AI_MODEL = "gemini-1.5-flash"  # Latest stable Gemini model
    TYPE_OPTIONS = ["日記", "支出", "タスク", "悩み"]
    EMOTION_OPTIONS = ["良好", "普通", "疲労", "悩み"]
    MOCK_MODE = os.getenv("MOCK_MODE", "False").lower() == "true"  # Production: False by default
