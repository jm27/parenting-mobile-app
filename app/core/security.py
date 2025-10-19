from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 18  # 18 hours


def create_access_token(data: dict):
    #     # Safe data to include in JWT
    # payload = {
    #     "user_id": user_data["id"],
    #     "username": user_data["username"],
    #     "email": user_data["email"],
    #     "role": user_data.get("role", "user"),  # user, premium, admin
    #     "subscription_type": user_data.get("subscription", "free"),
    #     "family_id": user_data.get("family_id"),  # For family accounts

    #     # Permissions for authorization
    #     "permissions": [
    #         "read:own_conversations",
    #         "write:own_conversations",
    #         "read:parenting_resources"
    #     ] + (["access:ai_features"] if user_data.get("subscription") == "premium" else []),

    #     # Token metadata
    #     "iat": datetime.utcnow(),  # Issued at
    #     "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # }
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


# get_current_user and verify_token functions would go here as well
