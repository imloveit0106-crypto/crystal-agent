"""AI Brain - Gemini API ハンドラー"""
import google.generativeai as genai
from typing import Dict, Optional

class AIBrain:
    def __init__(self, api_key: str, model_name: str = 'gemini-1.5-flash'):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_response(self, user_input: str, context: Optional[Dict] = None) -> str:
        try:
            prompt = self._build_prompt(user_input, context)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"エラー: {str(e)}"

    def _build_prompt(self, user_input: str, context: Optional[Dict] = None) -> str:
        if not context:
            return user_input

        context_str = ""
        if 'profile' in context:
            profile_str = "\n".join([f"- {k}: {v}" for k, v in context['profile'].items()])
            context_str += f"\n【あなたの情報】\n{profile_str}\n"

        return f"{context_str}\n【入力】\n{user_input}\n\n親しみやすく応答してください。"
