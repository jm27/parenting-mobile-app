from fastapi import APIRouter

from app.schemas.message_schemas import MessageCreate, MessageResponse

router = APIRouter()


@router.get("/messages", response_model=list[MessageResponse])
async def get_messages():
    return {"message": "List of messages"}


@router.post("/messages", response_model=MessageResponse)
async def create_message(message: MessageCreate):
    return {"message": message}
