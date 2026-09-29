"use client";

import { GapCard } from "@/components/research/GapCard";
import { IdeaCard } from "@/components/research/IdeaCard";
import { LiteratureList } from "@/components/research/LiteratureList";
import { PipelineProgress } from "@/components/research/PipelineProgress";
import { ResearchInputForm } from "@/components/research/ResearchInputForm";
import { useResearchSession } from "@/hooks/useResearchSession";

export default function HomePage() {
  const {
    session,
    papers,
    gaps,
    ideas,
    isSubmitting,
    submitQuery,
    submitReview,
    error,
  } = useResearchSession();

  const handleSubmit = (query: string, domain: string) => {
    submitQuery({ query, domain: domain || null });
  };

  const showProgress = session && session.stage !== "awaiting_human_review" && session.stage !== "completed";
  const showResults = session && (session.stage === "awaiting_human_review" || session.stage === "completed");

  const gapById = (id: string) => gaps.find((g) => g.id === id);

  return (
    <div className="space-y-6">
      <ResearchInputForm onSubmit={handleSubmit} isSubmitting={isSubmitting} />

      {error && (
        <p className="rounded-lg bg-rose-50 px-4 py-3 text-sm text-rose-700 dark:bg-rose-900/30 dark:text-rose-300">
          {error}
        </p>
      )}

      {showProgress && (
        <PipelineProgress stage={session!.stage} errorMessage={session!.error_message} />
      )}

      {showResults && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_1.3fr]">
          <div className="space-y-6">
            <LiteratureList papers={papers} />
            <div className="space-y-3">
              <h3 className="text-sm font-semibold text-slate-900 dark:text-white">
                Identified research gaps ({gaps.length})
              </h3>
              {gaps.map((gap) => (
                <GapCard key={gap.id} gap={gap} papers={papers} />
              ))}
            </div>
          </div>

          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-slate-900 dark:text-white">
              Research ideas &amp; titles — for your review ({ideas.length})
            </h3>
            {ideas.map((idea) => (
              <IdeaCard
                key={idea.id}
                idea={idea}
                gap={gapById(idea.gap_id)}
                papers={papers}
                onReview={submitReview}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
