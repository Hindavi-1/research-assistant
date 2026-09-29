"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-24

"""
from typing import Sequence, Union

import pgvector.sqlalchemy
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

EMBEDDING_DIM = 384  # must match settings.EMBEDDING_DIM (bge-small-en-v1.5)


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    pipeline_stage = postgresql.ENUM(
        "created", "retrieving_literature", "analyzing_literature", "identifying_gaps",
        "synthesizing_evidence", "generating_ideas", "generating_titles",
        "awaiting_human_review", "completed", "failed",
        name="pipeline_stage",
        create_type=False,
    )
    gap_type = postgresql.ENUM(
        "methodological", "empirical", "theoretical", "application", "contradiction",
        name="gap_type",
        create_type=False,
    )
    review_status = postgresql.ENUM(
        "pending", "approved", "rejected", "edited", name="review_status", create_type=False
    )
    title_review_status = postgresql.ENUM(
        "pending", "approved", "rejected", "edited", name="title_review_status", create_type=False
    )

    bind = op.get_bind()
    pipeline_stage.create(bind, checkfirst=True)
    gap_type.create(bind, checkfirst=True)
    review_status.create(bind, checkfirst=True)
    title_review_status.create(bind, checkfirst=True)

    op.create_table(
        "research_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("query", sa.Text, nullable=False),
        sa.Column("domain", sa.String(255), nullable=True),
        sa.Column("stage", pipeline_stage, nullable=False, server_default="created"),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("llm_provider", sa.String(50), nullable=False),
        sa.Column("llm_model", sa.String(100), nullable=False),
        sa.Column("search_providers", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "papers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "session_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False,
        ),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("source_id", sa.String(255), nullable=False),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("abstract", sa.Text, nullable=True),
        sa.Column("authors", postgresql.ARRAY(sa.String), server_default="{}"),
        sa.Column("published_year", sa.Integer, nullable=True),
        sa.Column("url", sa.String(1000), nullable=True),
        sa.Column("pdf_url", sa.String(1000), nullable=True),
        sa.Column("citation_count", sa.Integer, nullable=True),
        sa.Column("venue", sa.String(500), nullable=True),
        sa.Column("summary", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_papers_session_id", "papers", ["session_id"])

    op.create_table(
        "paper_chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "paper_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("papers.id", ondelete="CASCADE"), nullable=False,
        ),
        sa.Column("chunk_index", sa.Integer, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("embedding", pgvector.sqlalchemy.Vector(EMBEDDING_DIM), nullable=True),
    )
    op.create_index("ix_paper_chunks_paper_id", "paper_chunks", ["paper_id"])
    op.execute(
        "CREATE INDEX ix_paper_chunks_embedding ON paper_chunks "
        "USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
    )

    op.create_table(
        "research_gaps",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "session_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False,
        ),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("gap_type", gap_type, nullable=False),
        sa.Column("supporting_paper_ids", postgresql.ARRAY(sa.String), server_default="{}"),
        sa.Column("evidence_summary", sa.Text, nullable=False),
        sa.Column("confidence_score", sa.Float, server_default="0.6"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_research_gaps_session_id", "research_gaps", ["session_id"])

    op.create_table(
        "research_ideas",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "session_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("research_sessions.id", ondelete="CASCADE"), nullable=False,
        ),
        sa.Column(
            "gap_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("research_gaps.id", ondelete="CASCADE"), nullable=False,
        ),
        sa.Column("summary", sa.Text, nullable=False),
        sa.Column("proposed_approach", sa.Text, nullable=False),
        sa.Column("rationale", sa.Text, nullable=False),
        sa.Column("evidence_citations", postgresql.ARRAY(sa.String), server_default="{}"),
        sa.Column("novelty_score", sa.Float, server_default="0.5"),
        sa.Column("feasibility_score", sa.Float, server_default="0.5"),
        sa.Column("impact_score", sa.Float, server_default="0.5"),
        sa.Column("review_status", review_status, server_default="pending"),
        sa.Column("reviewer_notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_research_ideas_session_id", "research_ideas", ["session_id"])
    op.create_index("ix_research_ideas_gap_id", "research_ideas", ["gap_id"])

    op.create_table(
        "research_titles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "idea_id", postgresql.UUID(as_uuid=True),
            sa.ForeignKey("research_ideas.id", ondelete="CASCADE"), nullable=False,
        ),
        sa.Column("title_text", sa.String(500), nullable=False),
        sa.Column("style", sa.String(50), server_default="descriptive"),
        sa.Column("review_status", title_review_status, server_default="pending"),
        sa.Column("is_selected", sa.Boolean, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_research_titles_idea_id", "research_titles", ["idea_id"])


def downgrade() -> None:
    op.drop_table("research_titles")
    op.drop_table("research_ideas")
    op.drop_table("research_gaps")
    op.drop_table("paper_chunks")
    op.drop_table("papers")
    op.drop_table("research_sessions")

    bind = op.get_bind()
    postgresql.ENUM(name="title_review_status").drop(bind, checkfirst=True)
    postgresql.ENUM(name="review_status").drop(bind, checkfirst=True)
    postgresql.ENUM(name="gap_type").drop(bind, checkfirst=True)
    postgresql.ENUM(name="pipeline_stage").drop(bind, checkfirst=True)

    op.execute("DROP EXTENSION IF EXISTS vector")
