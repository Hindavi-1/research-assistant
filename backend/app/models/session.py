import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PipelineStage(str, enum.Enum):
    """Tracks which node of the LangGraph pipeline a session currently sits at.

    This is the persisted mirror of the LangGraph `AgentState.stage`, so the
    frontend can poll/resume a session and show progress even if the graph
    run happened in a previous request.
    """
    CREATED = "created"
    RETRIEVING_LITERATURE = "retrieving_literature"
    ANALYZING_LITERATURE = "analyzing_literature"
    IDENTIFYING_GAPS = "identifying_gaps"
    SYNTHESIZING_EVIDENCE = "synthesizing_evidence"
    GENERATING_IDEAS = "generating_ideas"
    GENERATING_TITLES = "generating_titles"
    AWAITING_HUMAN_REVIEW = "awaiting_human_review"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchSession(Base):
    """A single end-to-end run of the research-discovery pipeline for one user query."""

    __tablename__ = "research_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Raw user input: keywords or a free-text description of the research interest.
    query: Mapped[str] = mapped_column(Text, nullable=False)

    # Optional structured refinements (domain, constraints) the user can supply.
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)

    stage: Mapped[PipelineStage] = mapped_column(
        Enum(PipelineStage, name="pipeline_stage", values_callable=lambda obj: [e.value for e in obj]), default=PipelineStage.CREATED, nullable=False
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Which providers were used, persisted for reproducibility/debugging.
    llm_provider: Mapped[str] = mapped_column(String(50), nullable=False)
    llm_model: Mapped[str] = mapped_column(String(100), nullable=False)
    search_providers: Mapped[str] = mapped_column(String(255), nullable=False)  # comma-separated

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    papers: Mapped[list["Paper"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    gaps: Mapped[list["ResearchGap"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    ideas: Mapped[list["ResearchIdea"]] = relationship(back_populates="session", cascade="all, delete-orphan")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ResearchSession {self.id} stage={self.stage}>"
