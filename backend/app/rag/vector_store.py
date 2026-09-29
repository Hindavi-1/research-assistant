"""
pgvector-backed vector store operations.

Rather than standing up a separate vector DB, we store embeddings directly
in Postgres (`paper_chunks.embedding`, a `pgvector` column) — one database
for both relational and vector data, matching the project's "use Postgres
wherever needed" requirement. Similarity search uses pgvector's cosine
distance operator (`<=>`).
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.paper import Paper, PaperChunk
from app.rag.chunking import build_paper_document, chunk_text
from app.rag.embeddings import embed_query, embed_texts


async def ingest_paper_chunks(db: AsyncSession, paper: Paper) -> None:
    """Chunk + embed a paper's title/abstract and store as PaperChunk rows."""
    document = build_paper_document(paper.title, paper.abstract, paper.authors, paper.published_year)
    chunks = chunk_text(document)
    if not chunks:
        return

    vectors = embed_texts(chunks)
    for idx, (content, vector) in enumerate(zip(chunks, vectors)):
        db.add(
            PaperChunk(
                id=uuid.uuid4(),
                paper_id=paper.id,
                chunk_index=idx,
                content=content,
                embedding=vector,
            )
        )
    await db.flush()


async def similarity_search(
    db: AsyncSession, session_id: uuid.UUID, query: str, top_k: int = 8
) -> list[tuple[PaperChunk, float]]:
    """Return the top_k most relevant chunks (scoped to one research session) for a query."""
    query_vector = embed_query(query)

    stmt = (
        select(
            PaperChunk,
            PaperChunk.embedding.cosine_distance(query_vector).label("distance"),
        )
        .join(Paper, Paper.id == PaperChunk.paper_id)
        .where(Paper.session_id == session_id)
        .options(selectinload(PaperChunk.paper))
        .order_by("distance")
        .limit(top_k)
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [(row[0], row[1]) for row in rows]
