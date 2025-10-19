import logging

from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenAIClient:
    """
    Centralized OpenAI API interface
    Handles all interactions with OpenAI services
    """

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-4",
        max_tokens: int | None = None,
        temperature: float = 0.7,
        **kwargs,
    ):
        """
        Generate chat completion
        """
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
        """
        Create text embedding
        """
        try:
            response = await self.client.embeddings.create(model=model, input=text)
            return response.data[0].embedding

        except Exception as e:
            logger.error(f"OpenAI embedding error: {str(e)}")
            raise

    async def moderate_content(self, text: str):
        """
        Moderate content using OpenAI moderation API
        """
        try:
            response = await self.client.moderations.create(input=text)
            return response.results[0]

        except Exception as e:
            logger.error(f"OpenAI moderation error: {str(e)}")
            raise

    async def batch_embeddings(
        self, texts: list[str], model: str = "text-embedding-3-small"
    ) -> list[list[float]]:
        """
        Create embeddings for multiple texts
        """
        try:
            response = await self.client.embeddings.create(model=model, input=texts)
            return [data.embedding for data in response.data]

        except Exception as e:
            logger.error(f"OpenAI batch embedding error: {str(e)}")
            raise
