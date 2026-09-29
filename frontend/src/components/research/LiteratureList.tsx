import { ExternalLink } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";
import type { Paper } from "@/lib/types";

interface LiteratureListProps {
  papers: Paper[];
}

export function LiteratureList({ papers }: LiteratureListProps) {
  if (papers.length === 0) return null;

  return (
    <Card>
      <CardHeader>
        <h3 className="text-sm font-semibold text-slate-900 dark:text-white">
          Retrieved literature ({papers.length})
        </h3>
      </CardHeader>
      <CardContent className="max-h-96 space-y-3 overflow-y-auto">
        {papers.map((paper) => (
          <div
            key={paper.id}
            className="rounded-lg border border-slate-100 p-3 dark:border-slate-800"
          >
            <div className="flex items-start justify-between gap-2">
              <p className="text-sm font-medium text-slate-900 dark:text-white">{paper.title}</p>
              {paper.url && (
                <a
                  href={paper.url}
                  target="_blank"
                  rel="noreferrer"
                  className="shrink-0 text-slate-400 hover:text-brand-600"
                >
                  <ExternalLink size={14} />
                </a>
              )}
            </div>
            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
              {paper.authors.slice(0, 3).join(", ")}
              {paper.authors.length > 3 ? " et al." : ""} · {paper.published_year ?? "n.d."}
            </p>
            {paper.summary && (
              <p className="mt-2 text-xs text-slate-600 dark:text-slate-300">{paper.summary}</p>
            )}
            <div className="mt-2 flex flex-wrap gap-1.5">
              <Badge variant="info">{paper.source}</Badge>
              {typeof paper.citation_count === "number" && (
                <Badge>{paper.citation_count} citations</Badge>
              )}
              {paper.venue && <Badge>{paper.venue}</Badge>}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
