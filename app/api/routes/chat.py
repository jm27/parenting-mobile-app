import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.message_schema import MessageCreate, MessageResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=MessageResponse)
async def chat_endpoint(message: MessageCreate, db: Session = Depends(get_db)):
    """
    Basic chat endpoint - simplified for now
    """
    try:
        # For now, return a simple response
        # TODO: Integrate with AI agents when OpenAI is configured

        response = MessageResponse(
            content="Hello! I'm here to help with your parenting questions. This is a test response.",
            role="assistant",
            conversation_id=message.conversation_id,
            user_id=message.user_id,
            model="test-model",
        )

        return response

    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/chat/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: int, db: Session = Depends(get_db)
):
    """Get all messages for a conversation"""
    return {"messages": [], "conversation_id": conversation_id}
