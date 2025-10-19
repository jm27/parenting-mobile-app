from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    is_active: bool | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    conversation_count: int | None = 0

    class Config:
        from_attributes = True


class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None
