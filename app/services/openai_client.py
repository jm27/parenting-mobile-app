import logging

from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenAIClient:
    """
    Centralized OpenAI API interface
    """

    def __init__(self):
        # Get the key from settings and clean it
        api_key = settings.openai_api_key.strip() if settings.openai_api_key else None

        if not api_key:
            raise ValueError("OpenAI API key not configured in settings")

        # Explicitly pass the API key to the client
        self.client = AsyncOpenAI(api_key=api_key)
        logger.info(
            f"OpenAI client initialized with key: {api_key[:15]}...{api_key[-4:]}"
        )

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-4o-mini",
        max_tokens: int | None = None,
        temperature: float = 0.7,
        **kwargs,
    ):
        """Generate chat completion"""
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs,
            )
            return response

        except Exception as e:
            logger.error(f"OpenAI chat completion error: {str(e)}")
            raise

    async def create_embedding(self, text: str, model: str = "text-embedding-3-small"):
        """Create text embedding"""
        try:
            response = await self.client.embeddings.create(model=model, input=text)
            return response.data[0].embedding

        except Exception as e:
            logger.error(f"OpenAI embedding error: {str(e)}")
            raise

    async def moderate_content(self, text: str):
        """Moderate content using OpenAI moderation API"""
        try:
            response = await self.client.moderations.create(input=text)
            return response.results[0]

        except Exception as e:
            logger.error(f"OpenAI moderation error: {str(e)}")
            raise
