import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.schemas.message_schema import MessageCreate, MessageResponse, MessageUsage
from app.services.langgraph_pipeline import LangGraphPipeline

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=MessageResponse)
async def chat_endpoint(message: MessageCreate, db: Session = Depends(get_db)):
    """
    Chat endpoint with LangGraph pipeline and OpenAI integration
    """
    try:
        # Check if OpenAI is configured with better validation
        cleaned_key = settings.openai_api_key.strip() if settings.openai_api_key else ""

        if (
            not cleaned_key
            or cleaned_key == "your_openai_api_key_here"
            or not cleaned_key.startswith(("sk-", "sk-proj-"))
            or len(cleaned_key) < 20  # OpenAI keys are much longer
        ):
            return MessageResponse(
                content="AI chat is not properly configured. Please contact support.",
                role="assistant",
                conversation_id=message.conversation_id,
                user_id=message.user_id,
                model="fallback",
            )

        # Initialize pipeline
        pipeline = LangGraphPipeline()

        # TODO: Get conversation history from database
        conversation_history = []

        # Process through pipeline
        result = await pipeline.process_chat(
            user_message=message.content, conversation_history=conversation_history
        )

        # Build response
        usage = None
        if "usage" in result.get("metadata", {}):
            usage_data = result["metadata"]["usage"]
            usage = MessageUsage(
                input_tokens=usage_data["prompt_tokens"],
                output_tokens=usage_data["completion_tokens"],
                total_tokens=usage_data["total_tokens"],
            )

        response = MessageResponse(
            content=result["response"],
            role="assistant",
            conversation_id=message.conversation_id,
            user_id=message.user_id,
            model=result.get("metadata", {}).get("model", "gpt-4o-mini"),
            usage=usage,
        )

        logger.info(f"Chat response generated for user {message.user_id}")
        return response

    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")

        # Handle specific OpenAI errors
        error_str = str(e).lower()
        if "401" in error_str or "invalid_api_key" in error_str:
            return MessageResponse(
                content="There's an authentication issue with the AI service. Please contact support.",
                role="assistant",
                conversation_id=message.conversation_id,
                user_id=message.user_id,
                model="error-fallback",
            )
        elif "quota" in error_str or "429" in error_str:
            return MessageResponse(
                content="The AI service is temporarily unavailable due to high demand. Please try again later.",
                role="assistant",
                conversation_id=message.conversation_id,
                user_id=message.user_id,
                model="error-fallback",
            )

        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/chat/test")
async def test_openai_connection():
    """Test endpoint to verify OpenAI connection"""
    try:

        cleaned_key = settings.openai_api_key.strip() if settings.openai_api_key else ""

        return {
            "key_configured": bool(cleaned_key),
            "key_format_valid": cleaned_key.startswith(("sk-", "sk-proj-")),
            "key_length": len(cleaned_key),
            "key_preview": (
                f"{cleaned_key[:10]}...{cleaned_key[-4:]}" if cleaned_key else "None"
            ),
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


@router.get("/chat/test-live")
async def test_live_connection():
    """Actually test the OpenAI API"""
    try:
        from app.services.openai_client import OpenAIClient

        client = OpenAIClient()

        response = await client.chat_completion(
            messages=[{"role": "user", "content": "Say hello!"}], max_tokens=5
        )

        return {
            "status": "success",
            "response": response.choices[0].message.content,
            "model": response.model,
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "error_type": type(e).__name__}
