"""Shared FastAPI dependencies (currently just the DB session, re-exported for convenience)."""
from app.core.database import get_db

__all__ = ["get_db"]
