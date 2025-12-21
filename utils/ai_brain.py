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
        """プロンプトを構築（コンテキスト強化版）"""
        prompt_parts = [self.SYSTEM_PROMPT]

        # コンテキスト情報を追加
        if context:
            # ユーザープロフィール
            if 'profile' in context and context['profile']:
                profile_str = "\n".join([f"- {k}: {v}" for k, v in context['profile'].items()])
                prompt_parts.append(f"\n【ユーザーの基本情報】\n{profile_str}\n")

            # 最近の記録（直近5件）
            if 'recent_logs' in context and context['recent_logs']:
                logs_str = "\n".join([f"- {log}" for log in context['recent_logs'][:5]])
                prompt_parts.append(f"\n【最近の記録（直近5件）】\n{logs_str}\n")

            # 類似する過去ログ
            if 'similar_logs' in context and context['similar_logs']:
                similar_str = "\n".join([f"- {log}" for log in context['similar_logs'][:3]])
                prompt_parts.append(f"\n【関連する過去の記録】\n{similar_str}\n")

            # 行動パターン
            if 'patterns' in context and context['patterns']:
                patterns = context['patterns']
                pattern_info = []

                if 'top_words' in patterns and patterns['top_words']:
                    pattern_info.append(f"よく使う言葉: {', '.join(patterns['top_words'][:5])}")

                if 'emotion_distribution' in patterns:
                    emotions = patterns['emotion_distribution']
                    dominant_emotion = max(emotions, key=emotions.get) if emotions else None
                    if dominant_emotion:
                        pattern_info.append(f"最近の気分: {dominant_emotion}が多い")

                if pattern_info:
                    prompt_parts.append(f"\n【ユーザーの傾向】\n" + "\n".join([f"- {info}" for info in pattern_info]) + "\n")

            # 支出分析
            if 'spending_insights' in context and context['spending_insights']:
                spending = context['spending_insights']
                if spending.get('frequent_items'):
                    items_str = ', '.join(spending['frequent_items'][:3])
                    prompt_parts.append(f"\n【支出傾向】\nよく買うもの: {items_str}\n")

            # 会話履歴（最新の3-5ターンの会話）
            if 'conversation_history' in context and context['conversation_history']:
                history = context['conversation_history']
                if history:
                    history_str = "\n".join([
                        f"{'ユーザー' if msg['role'] == 'user' else 'あなた（Crystal Agent）'}: {msg['content']}"
                        for msg in history
                    ])
                    prompt_parts.append(f"\n【これまでの会話】\n{history_str}\n")

        # ユーザー入力を追加
        prompt_parts.append(f"\n【ユーザーの入力】\n{user_input}\n")
        prompt_parts.append("\n【応答】\n上記のすべての情報（会話履歴を含む）を踏まえて、ユーザーの状況や過去の記録を活かしたパーソナライズされた応答をしてください。会話の文脈を理解し、自然な対話を続けてください。親しみやすく簡潔に（2-3文程度、絵文字も使ってOK）。")

        return "\n".join(prompt_parts)
