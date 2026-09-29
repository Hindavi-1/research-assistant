import { CheckCircle2, CircleDashed, XCircle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/Card";
import { Spinner } from "@/components/ui/Spinner";
import { cn } from "@/lib/cn";
import {
  PIPELINE_STAGE_LABELS,
  PIPELINE_STAGE_ORDER,
  type PipelineStage,
} from "@/lib/types";

interface PipelineProgressProps {
  stage: PipelineStage;
  errorMessage?: string | null;
}

export function PipelineProgress({ stage, errorMessage }: PipelineProgressProps) {
  const currentIndex = PIPELINE_STAGE_ORDER.indexOf(stage);
  const failed = stage === "failed";

  return (
    <Card>
      <CardContent className="space-y-3">
        <h3 className="text-sm font-semibold text-slate-900 dark:text-white">Pipeline progress</h3>
        <ol className="space-y-2">
          {PIPELINE_STAGE_ORDER.map((s, idx) => {
            const isDone = !failed && idx < currentIndex;
            const isCurrent = !failed && idx === currentIndex;
            const isPending = !failed && idx > currentIndex;

            return (
              <li key={s} className="flex items-center gap-2 text-sm">
                {isDone && <CheckCircle2 size={16} className="shrink-0 text-emerald-500" />}
                {isCurrent && <Spinner className="shrink-0 text-brand-600" />}
                {isPending && <CircleDashed size={16} className="shrink-0 text-slate-300 dark:text-slate-700" />}
                {failed && <XCircle size={16} className="shrink-0 text-rose-500" />}
                <span
                  className={cn(
                    isCurrent && "font-medium text-brand-700 dark:text-brand-400",
                    isDone && "text-slate-500 dark:text-slate-400",
                    isPending && "text-slate-300 dark:text-slate-600",
                    failed && "text-slate-400"
                  )}
                >
                  {PIPELINE_STAGE_LABELS[s]}
                </span>
              </li>
            );
          })}
        </ol>
        {failed && (
          <p className="rounded-lg bg-rose-50 px-3 py-2 text-xs text-rose-700 dark:bg-rose-900/30 dark:text-rose-300">
            {errorMessage || "The pipeline failed. Please try again with a different query."}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
