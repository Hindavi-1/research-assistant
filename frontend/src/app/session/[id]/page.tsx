"use client";

import { useEffect, useState } from "react";
import { GapCard } from "@/components/research/GapCard";
import { IdeaCard } from "@/components/research/IdeaCard";
import { LiteratureList } from "@/components/research/LiteratureList";
import { PipelineProgress } from "@/components/research/PipelineProgress";
import { Spinner } from "@/components/ui/Spinner";
import { api } from "@/lib/api";
import type { Paper, ResearchGap, ResearchIdea, ResearchSession } from "@/lib/types";

export default function SessionDetailPage({ params }: { params: { id: string } }) {
  const [session, setSession] = useState<ResearchSession | null>(null);
  const [papers, setPapers] = useState<Paper[]>([]);
  const [gaps, setGaps] = useState<ResearchGap[]>([]);
  const [ideas, setIdeas] = useState<ResearchIdea[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const s = await api.getSession(params.id);
      setSession(s);

      if (s.stage === "awaiting_human_review" || s.stage === "completed") {
        const [p, g, i] = await Promise.all([
          api.getPapers(s.id),
          api.getGaps(s.id),
          api.getIdeas(s.id),
        ]);
        setPapers(p);
        setGaps(g);
        setIdeas(i);
      }
      setLoading(false);
    })();
  }, [params.id]);

  const handleReview = async (
    ideaId: string,
    status: "approved" | "rejected",
    selectedTitleId?: string
  ) => {
    const updated = await api.submitReview({
      idea_id: ideaId,
      status,
      selected_title_id: selectedTitleId ?? null,
    });
    setIdeas((prev) => prev.map((idea) => (idea.id === updated.id ? updated : idea)));
  };

  if (loading) {
    return (
      <div className="flex items-center gap-2 text-sm text-slate-500">
        <Spinner /> Loading session...
      </div>
    );
  }

  if (!session) return <p className="text-sm text-slate-500">Session not found.</p>;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">{session.query}</h2>
        {session.domain && <p className="text-sm text-slate-500">Domain: {session.domain}</p>}
      </div>

      {session.stage !== "awaiting_human_review" && session.stage !== "completed" && (
        <PipelineProgress stage={session.stage} errorMessage={session.error_message} />
      )}

      {(session.stage === "awaiting_human_review" || session.stage === "completed") && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_1.3fr]">
          <div className="space-y-6">
            <LiteratureList papers={papers} />
            <div className="space-y-3">
              {gaps.map((gap) => (
                <GapCard key={gap.id} gap={gap} papers={papers} />
              ))}
            </div>
          </div>
          <div className="space-y-3">
            {ideas.map((idea) => (
              <IdeaCard
                key={idea.id}
                idea={idea}
                gap={gaps.find((g) => g.id === idea.gap_id)}
                papers={papers}
                onReview={handleReview}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
