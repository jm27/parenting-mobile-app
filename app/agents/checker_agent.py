import logging

from pydantic import BaseModel

from app.services.openai_client import OpenAIClient

logger = logging.getLogger(__name__)


class ModerationResult(BaseModel):
    is_safe: bool
    reason: str = ""
    confidence: float = 0.0


class CheckerAgent:
    """
    Lightweight input/output moderation agent
    Ensures content safety and appropriateness for parenting context
    """

    def __init__(self):
        self.client = OpenAIClient()
        self.system_prompt = """
        You are a content moderation agent for a parenting advice platform.
        
        Check if the content is:
        1. Safe and appropriate for parenting discussions
        2. Free from harmful, abusive, or inappropriate content
        3. Relevant to parenting, child development, or family topics
        
        Respond with:
        - "SAFE" if content is appropriate
        - "UNSAFE: [reason]" if content should be blocked
        
        Be permissive for genuine parenting questions, even if they involve challenges.
        """

    async def check_input(self, user_input: str) -> ModerationResult:
        """Check user input for safety and relevance"""
        try:
            # Use OpenAI moderation API first
            moderation = await self.client.moderate_content(user_input)

            if moderation.flagged:
                return ModerationResult(
                    is_safe=False,
                    reason="Content flagged by moderation system",
                    confidence=0.9,
                )

            # Custom parenting context check
            response = await self.client.chat_completion(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Check this input: {user_input}"},
                ],
                model="gpt-3.5-turbo",
                max_tokens=50,
            )

            result_text = response.choices[0].message.content.strip()

            if result_text.startswith("SAFE"):
                return ModerationResult(is_safe=True, confidence=0.8)
            else:
                reason = result_text.replace("UNSAFE:", "").strip()
                return ModerationResult(
                    is_safe=False,
                    reason=reason or "Content not appropriate for parenting platform",
                    confidence=0.8,
                )

        except Exception as e:
            logger.error(f"Input moderation error: {str(e)}")
            # Fail open for now, but log the error
            return ModerationResult(is_safe=True, reason="Moderation check failed")

    async def check_output(self, ai_response: str) -> ModerationResult:
        """Check AI-generated output for safety"""
        try:
            # Quick safety check on AI output
            moderation = await self.client.moderate_content(ai_response)

            if moderation.flagged:
                return ModerationResult(
                    is_safe=False,
                    reason="AI response flagged by moderation",
                    confidence=0.9,
                )

            return ModerationResult(is_safe=True, confidence=0.9)

        except Exception as e:
            logger.error(f"Output moderation error: {str(e)}")
            return ModerationResult(is_safe=True, reason="Output check failed")
