"""Centralized loguru-based logging setup."""
import sys

from loguru import logger

from app.config import get_settings

settings = get_settings()


def setup_logging() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        level="DEBUG" if settings.APP_ENV == "development" else "INFO",
    )


__all__ = ["logger", "setup_logging"]
