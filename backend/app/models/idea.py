import enum
import uuid
from datetime import datetime

from sqlalchemy import ARRAY, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ReviewStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EDITED = "edited"


class ResearchIdea(Base):
    """A Phase-3 output: a concrete research idea grounded in one or more gaps."""

    __tablename__ = "research_ideas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False
    )
    gap_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("research_gaps.id", ondelete="CASCADE"), nullable=False
    )

    summary: Mapped[str] = mapped_column(Text, nullable=False)
    proposed_approach: Mapped[str] = mapped_column(Text, nullable=False)

    # "Why work on this" — the required justification + evidence.
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_citations: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)  # paper ids
    novelty_score: Mapped[float] = mapped_column(default=0.5)     # 0-1, LLM self-estimated
    feasibility_score: Mapped[float] = mapped_column(default=0.5)  # 0-1, LLM self-estimated
    impact_score: Mapped[float] = mapped_column(default=0.5)       # 0-1, LLM self-estimated

    review_status: Mapped[ReviewStatus] = mapped_column(
        Enum(ReviewStatus, name="review_status", values_callable=lambda obj: [e.value for e in obj]), default=ReviewStatus.PENDING
    )
    reviewer_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    session: Mapped["ResearchSession"] = relationship(back_populates="ideas")
    gap: Mapped["ResearchGap"] = relationship(back_populates="ideas")
    titles: Mapped[list["ResearchTitle"]] = relationship(back_populates="idea", cascade="all, delete-orphan")


class ResearchTitle(Base):
    """A Phase-3 output: a candidate paper title for a given idea."""

    __tablename__ = "research_titles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idea_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("research_ideas.id", ondelete="CASCADE"), nullable=False
    )

    title_text: Mapped[str] = mapped_column(String(500), nullable=False)
    style: Mapped[str] = mapped_column(String(50), default="descriptive")  # descriptive | catchy | technical
    review_status: Mapped[ReviewStatus] = mapped_column(
        Enum(ReviewStatus, name="title_review_status", values_callable=lambda obj: [e.value for e in obj]), default=ReviewStatus.PENDING
    )
    is_selected: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    idea: Mapped["ResearchIdea"] = relationship(back_populates="titles")
