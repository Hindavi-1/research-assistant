"use client";

import { BookOpen, Lightbulb, AlertTriangle } from "lucide-react";
import { GapCard } from "@/components/research/GapCard";
import { IdeaCard } from "@/components/research/IdeaCard";
import { LiteratureList } from "@/components/research/LiteratureList";
import { PipelineProgress } from "@/components/research/PipelineProgress";
import { ResearchInputForm } from "@/components/research/ResearchInputForm";
import { useResearchSession } from "@/hooks/useResearchSession";

function SectionHeader({
  icon: Icon,
  title,
  count,
  color = "brand",
}: {
  icon: React.ElementType;
  title: string;
  count: number;
  color?: "brand" | "violet" | "emerald";
}) {
  const colorMap = {
    brand: {
      icon: "bg-brand-100 dark:bg-brand-900/40",
      iconText: "text-brand-600 dark:text-brand-400",
      count: "bg-brand-100 text-brand-600 dark:bg-brand-900/40 dark:text-brand-400",
    },
    violet: {
      icon: "bg-violet-100 dark:bg-violet-900/40",
      iconText: "text-violet-600 dark:text-violet-400",
      count: "bg-violet-100 text-violet-600 dark:bg-violet-900/40 dark:text-violet-400",
    },
    emerald: {
      icon: "bg-emerald-100 dark:bg-emerald-900/40",
      iconText: "text-emerald-600 dark:text-emerald-400",
      count: "bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-400",
    },
  };
  const c = colorMap[color];

  return (
    <div className="mb-3 flex items-center gap-2.5">
      <div className={`flex h-7 w-7 items-center justify-center rounded-lg ${c.icon}`}>
        <Icon size={14} className={c.iconText} />
      </div>
      <h3 className="text-sm font-bold text-slate-800 dark:text-white">{title}</h3>
      <span
        className={`ml-auto rounded-full px-2.5 py-0.5 text-xs font-bold ${c.count}`}
      >
        {count}
      </span>
    </div>
  );
}

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

  const showProgress =
    session &&
    session.stage !== "awaiting_human_review" &&
    session.stage !== "completed";
  const showResults =
    session &&
    (session.stage === "awaiting_human_review" || session.stage === "completed");

  const gapById = (id: string) => gaps.find((g) => g.id === id);

  return (
    <div className="space-y-6">
      {/* Input form */}
      <ResearchInputForm onSubmit={handleSubmit} isSubmitting={isSubmitting} />

      {/* Error */}
      {error && (
        <div className="flex items-start gap-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 dark:border-rose-800/40 dark:bg-rose-900/20">
          <AlertTriangle size={15} className="mt-0.5 shrink-0 text-rose-500" />
          <p className="text-sm text-rose-700 dark:text-rose-300">{error}</p>
        </div>
      )}

      {/* Pipeline progress */}
      {showProgress && (
        <PipelineProgress stage={session!.stage} errorMessage={session!.error_message} />
      )}

      {/* Results grid */}
      {showResults && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_1.4fr]">
          {/* Left column: literature + gaps */}
          <div className="space-y-6 min-w-0">
            {/* Literature */}
            <LiteratureList papers={papers} />

            {/* Gaps */}
            {gaps.length > 0 && (
              <div>
                <SectionHeader
                  icon={BookOpen}
                  title="Research gaps identified"
                  count={gaps.length}
                  color="brand"
                />
                <div className="space-y-2 stagger-children">
                  {gaps.map((gap, i) => (
                    <GapCard key={gap.id} gap={gap} papers={papers} index={i} />
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right column: ideas */}
          <div className="min-w-0">
            {ideas.length > 0 && (
              <>
                <SectionHeader
                  icon={Lightbulb}
                  title="Research ideas for your review"
                  count={ideas.length}
                  color="violet"
                />
                <div className="space-y-3 stagger-children">
                  {ideas.map((idea, i) => (
                    <IdeaCard
                      key={idea.id}
                      idea={idea}
                      gap={gapById(idea.gap_id)}
                      papers={papers}
                      onReview={submitReview}
                      index={i}
                    />
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
