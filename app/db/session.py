import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create engine with error handling
try:
    if not settings.database_url:
        raise ValueError("DATABASE_URL not configured")

    engine = create_engine(
        settings.database_url,
        echo=settings.debug,  # Log SQL queries in debug mode
        connect_args=(
            {"check_same_thread": False} if "sqlite" in settings.database_url else {}
        ),
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info(f"Database connected: {settings.database_url}")

except Exception as e:
    logger.error(f"Database connection failed: {str(e)}")
    # For development, we'll create a fallback in-memory SQLite database
    logger.warning("Using fallback in-memory SQLite database")
    engine = create_engine(
        "sqlite:///:memory:",
        echo=settings.debug,
        connect_args={"check_same_thread": False},
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
