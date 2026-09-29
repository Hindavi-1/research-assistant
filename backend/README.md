# Backend — AI Research Assistant

FastAPI + LangGraph + Postgres (pgvector) service implementing Phases 0-4.

## Setup (local, without Docker)

```bash

python -m venv .venv 
.venv\Scripts\activate
pip install -r requirements.txt

# Postgres with pgvector must be running and reachable at DATABASE_URL (see ../.env.example)
alembic upgrade head

uvicorn app.main:app --reload
```

Docs at http://localhost:8000/docs

## Project layout

```
app/
├── main.py              # FastAPI app, CORS, exception handlers
├── config.py             # Settings (env-driven), single source of truth
├── core/                  # db session, logging, exceptions
├── api/v1/                # HTTP routes (sessions, research/review)
├── models/                # SQLAlchemy ORM models
├── schemas/               # Pydantic request/response + LLM structured-output shapes
├── llm/                   # LLM provider interface + factory (Groq default)
│   └── providers/         # groq / openai / anthropic implementations
├── search/                # Search provider interface + factory
│   └── providers/         # arxiv / semantic_scholar / google_scholar(stub)
├── rag/                    # chunking, embeddings, pgvector store, retriever
├── graph/                  # LangGraph state, nodes, workflow assembly
│   └── nodes/               # one file per pipeline stage
├── services/                # orchestration + read-side query services
└── utils/                    # prompts, JSON parsing helpers
```

## Swapping providers

- LLM: set `LLM_PROVIDER=openai|anthropic|groq` and the matching API key + `LLM_MODEL` in `.env`.
- Search: set `SEARCH_PROVIDERS=arxiv,semantic_scholar` (comma-separated, order = priority).

No other code changes are needed — both are resolved via factories at call time.

## Running the pipeline manually (without the API)

```python
import asyncio, uuid
from app.graph.workflow import get_compiled_graph
from app.graph.state import new_state

async def main():
    graph = get_compiled_graph()
    state = new_state(uuid.uuid4(), "graph neural networks for drug discovery", "Machine Learning")
    result = await graph.ainvoke(state, config={"configurable": {"thread_id": "demo"}})
    print(result["ideas"])

asyncio.run(main())
```
