import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import ARRAY, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import get_settings
from app.core.database import Base

settings = get_settings()


class Paper(Base):
    """A single retrieved literature item (Phase 1 output), normalized across sources."""

    __tablename__ = "papers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False
    )

    source: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. "arxiv", "semantic_scholar"
    source_id: Mapped[str] = mapped_column(String(255), nullable=False)  # provider-native id
    title: Mapped[str] = mapped_column(Text, nullable=False)
    abstract: Mapped[str] = mapped_column(Text, nullable=True)
    authors: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    published_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    pdf_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    citation_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    venue: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Phase 2 output: short LLM-generated summary of this paper's contribution/limitations.
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["ResearchSession"] = relationship(back_populates="papers")
    chunks: Mapped[list["PaperChunk"]] = relationship(back_populates="paper", cascade="all, delete-orphan")

    def citation_label(self) -> str:
        """Short human-readable citation key, e.g. (Smith et al., 2023)."""
        first_author = self.authors[0].split()[-1] if self.authors else "Unknown"
        suffix = "et al." if len(self.authors) > 1 else ""
        year = self.published_year or "n.d."
        return f"({first_author} {suffix}, {year})".replace("  ", " ")


class PaperChunk(Base):
    """A chunk of a paper's abstract/text with its embedding — the RAG retrieval unit."""

    __tablename__ = "paper_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paper_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("papers.id", ondelete="CASCADE"), nullable=False
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(settings.EMBEDDING_DIM), nullable=True)

    paper: Mapped["Paper"] = relationship(back_populates="chunks")
