# AI Research Assistant — Agentic Research Discovery & Idea Generation

An agentic system that automates the **early stages** of the research process:
finding literature → analyzing it → identifying research gaps → generating
evidence-backed research ideas and titles → human review.

This repo implements a **vertical slice** (Phases 0–4). Full paper generation
(abstract, methodology, references, diagrams) is intentionally **out of scope**
for now — see `docs/roadmap.md` conceptually via the phase table below.

## Phases

| Phase | Purpose | Status |
|-------|---------|--------|
| 0 | Environment & infrastructure setup | ✅ implemented |
| 1 | Research discovery & paper retrieval (arXiv, Semantic Scholar, ...) | ✅ implemented |
| 2 | Literature intelligence & research-gap analysis (RAG-backed) | ✅ implemented |
| 3 | Research idea & title generation with evidence | ✅ implemented |
| 4 | Human review & research-project state (approve/reject/edit) | ✅ implemented |
| Future | Abstract, methodology, full sections, references, diagrams | 🚧 not built |

## Pipeline (this slice)

```
User Input (keywords/description)
   → Literature Retrieval        (Phase 1 — search provider factory)
   → Literature Analysis         (Phase 2 — RAG: chunk, embed, summarize)
   → Research Gap Identification (Phase 2 — LLM reasoning over retrieved evidence)
   → Evidence Synthesis          (Phase 2 — grounds each gap in cited papers)
   → Research Idea Generation    (Phase 3 — LLM, grounded in gaps + evidence)
   → Title Generation            (Phase 3 — LLM, multiple candidates per idea)
   → Human Selection             (Phase 4 — approve/edit/reject, persisted state)
```

## Architecture Highlights

- **LangGraph** orchestrates the pipeline as a stateful graph (`backend/app/graph`),
  with each phase as a node, so it's resumable, inspectable and easy to extend
  (future phases just become new nodes appended to the graph).
- **Postgres** stores sessions, papers, gaps, ideas, titles and human-review
  state (`backend/app/models`), plus `pgvector` for embeddings.
- **RAG layer** (`backend/app/rag`) chunks & embeds retrieved papers so gap
  analysis and idea generation are grounded in retrieved evidence, not
  hallucinated.
- **LLM providers are pluggable** via a factory (`backend/app/llm`). Groq is
  the default; OpenAI/Anthropic are implemented too. Swap via `.env`, no code
  changes required elsewhere in the app.
- **Search sources are pluggable** the same way (`backend/app/search`):
  arXiv and Semantic Scholar are implemented; Google Scholar has a stub
  provider (scraping ToS caveats noted in code) behind the same interface.
- **Frontend**: Next.js (App Router) + TypeScript + Tailwind, with reusable,
  typed components and a small API client / hook layer.

## Project layout

```
research-assistant/
├── backend/     # FastAPI + LangGraph + Postgres
└── frontend/    # Next.js
```

See `backend/README.md` and `frontend/README.md` for setup instructions.

## Quick start

```bash
cp .env.example .env        # fill in GROQ_API_KEY etc.
docker compose up --build   # starts postgres (with pgvector), backend, frontend
```

- Backend: http://localhost:8000/docs
- Frontend: http://localhost:3000
