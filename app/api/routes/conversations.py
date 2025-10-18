from fastapi import APIRouter

from app.schemas.conversation_schemas import ConversationCreate, ConversationResponse

router = APIRouter()

@router.get("/conversations", response_model=list[ConversationResponse])
async def get_conversations():
    return {"message": "List of conversations"}

@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(conversation: ConversationCreate):
    return {"message": "Conversation created", "conversation": conversation}
