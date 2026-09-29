"""
Async SQLAlchemy engine + session management.

Uses Postgres (via asyncpg) as the single source of truth for all
persisted state: research sessions, retrieved papers, gaps, ideas,
titles and human-review decisions. `pgvector` extension is used for
embedding storage (see app/rag/vector_store.py).
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — yields a transactional session, rolls back on error."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def db_session_ctx() -> AsyncGenerator[AsyncSession, None]:
    """Context manager for use outside of FastAPI's DI (e.g. inside LangGraph nodes)."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_models() -> None:
    """Create tables directly (used only for quick local dev; prefer Alembic in real use)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
