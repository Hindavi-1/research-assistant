import { Badge } from "@/components/ui/Badge";
import { Card, CardContent } from "@/components/ui/Card";
import type { GapType, Paper, ResearchGap } from "@/lib/types";

interface GapCardProps {
  gap: ResearchGap;
  papers: Paper[];
}

const GAP_TYPE_VARIANT: Record<GapType, "info" | "warning" | "default" | "danger"> = {
  methodological: "info",
  empirical: "default",
  theoretical: "warning",
  application: "info",
  contradiction: "danger",
};

export function GapCard({ gap, papers }: GapCardProps) {
  const supportingPapers = papers.filter((p) => gap.supporting_paper_ids.includes(p.id));

  return (
    <Card>
      <CardContent className="space-y-3">
        <div className="flex items-start justify-between gap-2">
          <h4 className="text-sm font-semibold text-slate-900 dark:text-white">{gap.title}</h4>
          <Badge variant={GAP_TYPE_VARIANT[gap.gap_type]}>{gap.gap_type}</Badge>
        </div>

        <p className="text-sm text-slate-600 dark:text-slate-300">{gap.description}</p>

        <div className="rounded-lg bg-slate-50 p-3 dark:bg-slate-800/50">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
            Why this is a gap
          </p>
          <p className="mt-1 text-xs text-slate-600 dark:text-slate-300">{gap.evidence_summary}</p>
        </div>

        {supportingPapers.length > 0 && (
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
              Evidenced by
            </p>
            <ul className="mt-1 space-y-1">
              {supportingPapers.map((p) => (
                <li key={p.id} className="text-xs text-slate-500 dark:text-slate-400">
                  · {p.title} ({p.published_year ?? "n.d."})
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="flex items-center justify-between text-xs text-slate-400">
          <span>Confidence</span>
          <span className="font-medium text-slate-600 dark:text-slate-300">
            {Math.round(gap.confidence_score * 100)}%
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
