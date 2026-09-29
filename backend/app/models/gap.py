import enum
import uuid
from datetime import datetime

from sqlalchemy import ARRAY, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class GapType(str, enum.Enum):
    METHODOLOGICAL = "methodological"     # existing methods are flawed/limited
    EMPIRICAL = "empirical"                # missing datasets/experiments/domains
    THEORETICAL = "theoretical"            # missing theory/formal understanding
    APPLICATION = "application"            # unexplored real-world application
    CONTRADICTION = "contradiction"        # conflicting findings across papers


class ResearchGap(Base):
    """A Phase-2 output: a specific gap identified in the literature, with evidence."""

    __tablename__ = "research_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    gap_type: Mapped[GapType] = mapped_column(Enum(GapType, name="gap_type", values_callable=lambda obj: [e.value for e in obj]), nullable=False)

    # Evidence: which papers (by id) support this gap, plus a short justification quote/paraphrase.
    supporting_paper_ids: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    evidence_summary: Mapped[str] = mapped_column(Text, nullable=False)

    confidence_score: Mapped[float] = mapped_column(default=0.6)  # 0-1, LLM self-estimated

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["ResearchSession"] = relationship(back_populates="gaps")
    ideas: Mapped[list["ResearchIdea"]] = relationship(back_populates="gap")
