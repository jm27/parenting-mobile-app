from datetime import datetime

from pydantic import BaseModel

from app.schemas.message_schema import MessageInDB


class ConversationBase(BaseModel):
    title: str | None = None


class ConversationCreate(ConversationBase):
    user_id: int
    title: str | None = "New Conversation"


class ConversationUpdate(BaseModel):
    title: str | None = None


class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None
    message_count: int | None = 0

    class Config:
        from_attributes = True


class ConversationWithMessages(ConversationResponse):
    messages: list[MessageInDB] = []


class ConversationInDB(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
