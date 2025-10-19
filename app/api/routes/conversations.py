from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.conversation_schema import ConversationCreate, ConversationResponse

router = APIRouter()


@router.get("/conversations", response_model=list[ConversationResponse])
async def get_conversations(db: Session = Depends(get_db)):
    """Get all conversations - returns empty list for now"""
    # TODO: Implement actual database query
    # For now, return an empty list to match the expected response model
    return []


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate, db: Session = Depends(get_db)
):
    """Create a new conversation"""
    # TODO: Implement actual database creation
    # For now, return a mock response that matches the schema
    from datetime import datetime

    return ConversationResponse(
        id=1,  # Mock ID
        title=conversation.title or "New Conversation",
        user_id=conversation.user_id,
        created_at=datetime.utcnow(),
        message_count=0,
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """Get a specific conversation"""
    from datetime import datetime

    # TODO: Implement actual database query
    return ConversationResponse(
        id=conversation_id,
        title=f"Conversation {conversation_id}",
        user_id=1,  # Mock user ID
        created_at=datetime.utcnow(),
        message_count=0,
    )
