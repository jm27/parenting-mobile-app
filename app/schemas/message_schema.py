from datetime import datetime

from pydantic import BaseModel


class MessageUsage(BaseModel):
    """Token usage information"""

    input_tokens: int
    output_tokens: int
    total_tokens: int


class MessageBase(BaseModel):
    content: str
    role: str  # "user" or "assistant"


class MessageCreate(MessageBase):
    conversation_id: int | None = None
    user_id: int | None = None


class MessageResponse(MessageBase):
    id: int | None = None
    conversation_id: int | None = None
    user_id: int | None = None
    created_at: datetime | None = None
    model: str = "gpt-4"
    usage: MessageUsage | None = None
    retrieved_sources: list[str] | None = None

    class Config:
        from_attributes = True


class MessageInDB(MessageBase):
    id: int
    conversation_id: int
    user_id: int
    created_at: datetime
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None

    class Config:
        from_attributes = True
