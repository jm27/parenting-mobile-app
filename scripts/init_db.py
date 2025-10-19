import logging

from app.db.models import Base
from app.db.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")


if __name__ == "__main__":
    create_tables()
