import openai

from app.core.config import settings


class ChatGPTService:
    def __init__(self):
        openai.api_key = settings.openai_api_key

    async def generate_response(self, messages: list) -> str:
        # Implement ChatGPT API call
        pass
