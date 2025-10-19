import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import conversations, health, users
from app.core.config import settings

# Setup basic logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Parenting App API",
    description="AI-powered parenting advice platform",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include basic routers first
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(conversations.router, prefix="/api/v1", tags=["conversations"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])

# Only include chat router if everything is properly configured
try:
    if (
        settings.openai_api_key
        and settings.openai_api_key != "your_openai_api_key_here"
    ):
        from app.api.routes import chat

        app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
        logger.info("Chat endpoints enabled")
    else:
        logger.warning("OpenAI API key not configured - chat endpoints disabled")
except ImportError as e:
    logger.warning(f"Could not import chat module: {e}")


@app.get("/")
async def root():
    return {
        "message": "Parenting App API",
        "version": "0.1.0",
        "docs": "/docs",
        "status": "running",
    }


@app.get("/api/v1")
async def api_info():
    return {
        "message": "Parenting App API v1",
        "endpoints": {
            "health": "/api/v1/health",
            "conversations": "/api/v1/conversations",
            "users": "/api/v1/users",
        },
    }
