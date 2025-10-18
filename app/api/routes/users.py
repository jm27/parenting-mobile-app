from fastapi import APIRouter

from app.schemas.user_schemas import UserCreate, UserResponse

router = APIRouter()

@router.get("/users", response_model=list[UserResponse])
async def get_users():
    return {"message": "List of users"}

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    return {"message": "User created", "user": user}
