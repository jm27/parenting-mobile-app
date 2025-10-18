﻿import logging
import sys

from app.core.config import settings


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG if settings.debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("app.log"), logging.StreamHandler(sys.stdout)],
    )
