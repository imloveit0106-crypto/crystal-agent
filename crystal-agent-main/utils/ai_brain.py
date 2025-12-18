"""AI Brain - Gemini API ハンドラー"""
import google.generativeai as genai
from typing import Dict, Optional

class AIBrain:
    # Crystal Agentのシステムプロンプト
    SYSTEM_PROMPT = """あなたは「Crystal Agent」という名前の親しみやすいAIアシスタントです。

【あなたの役割】
- ユーザーの日々の行動・思考・感情を記録し、成長をサポートする
- 共感的で温かい対話を心がける
- 具体的で実践的なアドバイスを提供する
- ユーザーの過去の記録を活かしてパーソナライズされた助言をする

【対話スタイル】
- 敬語ではなく、親しい友達のような口調（「〜だよ」「〜だね」）
- 適度に絵文字を使用（😊✨💪など）
- ポジティブで前向きなフィードバック
- 短めの文章で簡潔に（2-3文程度）
- ユーザーの気持ちに寄り添う共感的な応答

【対応するログタイプ】
- 日記: 出来事や感情の記録 → 共感と振り返りを促す
- 支出: 金額を含む買い物の記録 → 無駄遣いを指摘せず、次へのアドバイス
- タスク: やるべきことの記録 → 実現可能なステップに分解
- 悩み: 相談や悩みの共有 → 傾聴し、一緒に考える姿勢

【禁止事項】
- 説教や上から目線の発言
- 長すぎる説明（簡潔に！）
- ネガティブな批判
- 専門的すぎる用語の使用
"""

    def __init__(self, api_key: str, model_name: str = 'gemini-1.5-flash'):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_response(self, user_input: str, context: Optional[Dict] = None) -> str:
        try:
            prompt = self._build_prompt(user_input, context)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # エラー時は親しみやすいメッセージを返す
            return "ごめんね、ちょっと考え中にエラーが起きちゃった...💦 もう一度試してみてくれる？"

    def _build_prompt(self, user_input: str, context: Optional[Dict] = None) -> str:
        """プロンプトを構築"""
        prompt_parts = [self.SYSTEM_PROMPT]

        # コンテキスト情報を追加
        if context:
            if 'profile' in context and context['profile']:
                profile_str = "\n".join([f"- {k}: {v}" for k, v in context['profile'].items()])
                prompt_parts.append(f"\n【ユーザーの基本情報】\n{profile_str}\n")

            if 'recent_logs' in context and context['recent_logs']:
                logs_str = "\n".join([f"- {log}" for log in context['recent_logs'][:5]])
                prompt_parts.append(f"\n【最近の記録】\n{logs_str}\n")

        # ユーザー入力を追加
        prompt_parts.append(f"\n【ユーザーの入力】\n{user_input}\n")
        prompt_parts.append("\n【応答】\n上記を踏まえて、親しみやすく簡潔に応答してください（2-3文程度、絵文字も使ってOK）。")

        return "\n".join(prompt_parts)
