from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import models
from app.schemas import user_schema

# --- User CRUD operations --- #


async def create_user(db: AsyncSession, user: user_schema.UserCreate):
    new_user = models.User(email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()


# --- Conversation CRUD operations --- #


async def create_conversation(db: AsyncSession, user_id: str, title: str | None = None):
    new_conversation = models.Conversation(user_id=user_id, title=title)
    db.add(new_conversation)
    await db.commit()
    await db.refresh(new_conversation)
    return new_conversation


async def get_conversation_messages(db: AsyncSession, conversation_id: str):
    result = await db.execute(
        select(models.Message)
        .where(models.Message.conversation_id == conversation_id)
        .order_by(models.Message.created_at)
    )
    return result.scalars().all()


# --- Message CRUD operations --- #


async def create_message(
    db: AsyncSession, conversation_id: str, content: str, sender_role: str
):
    new_message = models.Message(
        conversation_id=conversation_id, content=content, sender_role=sender_role
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message
