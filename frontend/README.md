# Frontend — AI Research Assistant

Next.js (App Router) + TypeScript + Tailwind UI for the vertical slice pipeline.

## Setup

```bash
npm install
cp .env.local.example .env.local   # point at your backend
npm run dev
```

Visit http://localhost:3000

## Structure

```
src/
├── app/
│   ├── page.tsx              # main flow: input -> progress -> results -> review
│   ├── session/[id]/page.tsx # revisit a past session by id
│   └── layout.tsx
├── components/
│   ├── ui/                    # generic, reusable primitives (Button, Card, Badge, ScoreBar, Spinner)
│   ├── research/               # domain components (ResearchInputForm, PipelineProgress,
│   │                              LiteratureList, GapCard, IdeaCard, TitleSelector)
│   └── layout/                  # Header, Footer
├── hooks/
│   └── useResearchSession.ts     # submit query, poll pipeline stage, fetch results, submit review
└── lib/
    ├── api.ts                     # typed fetch client
    ├── types.ts                    # types mirroring backend schemas
    └── cn.ts                        # classname helper
```

## Notes

- Polling: after submitting a query, the UI polls `GET /sessions/{id}/status` every 2.5s and
  fetches full results once the pipeline reaches `awaiting_human_review`.
- Human review (Phase 4): each `IdeaCard` lets you approve/reject an idea and pick one of its
  generated titles, persisted via `POST /research/review`.
