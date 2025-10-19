from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    """Get all users - returns empty list for now"""
    # TODO: Implement actual database query
    return []


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    from datetime import datetime

    # TODO: Implement actual database creation and password hashing
    return UserResponse(
        id=1,  # Mock ID
        email=user.email,
        username=user.username,
        is_active=True,
        created_at=datetime.utcnow(),
        conversation_count=0,
    )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user"""
    from datetime import datetime

    # TODO: Implement actual database query
    return UserResponse(
        id=user_id,
        email=f"user{user_id}@example.com",
        username=f"user{user_id}",
        is_active=True,
        created_at=datetime.utcnow(),
        conversation_count=0,
    )
