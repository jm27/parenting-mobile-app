from datetime import datetime

from pydantic import BaseModel


class ConversationBase(BaseModel):
    title: str

class ConversationCreate(ConversationBase):
    user_id: int

class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
