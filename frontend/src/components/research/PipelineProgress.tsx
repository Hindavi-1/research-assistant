import { CheckCircle2, CircleDashed, XCircle, Loader2 } from "lucide-react";
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
  const totalSteps = PIPELINE_STAGE_ORDER.length;
  const progressPct = failed ? 0 : Math.round((currentIndex / (totalSteps - 1)) * 100);

  return (
    <div className="rounded-2xl border border-slate-200/80 bg-white shadow-sm dark:border-slate-800/70 dark:bg-slate-900/60 animate-fade-in">
      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-100/80 dark:border-slate-800/60">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">
            Pipeline running
          </h3>
          <span className="text-xs font-semibold text-slate-400">
            {failed ? "Failed" : `${progressPct}%`}
          </span>
        </div>
        {/* Progress bar */}
        <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
          <div
            className={cn(
              "h-full rounded-full transition-all duration-700",
              failed
                ? "bg-rose-400"
                : "bg-gradient-to-r from-brand-500 to-violet-500"
            )}
            style={{ width: `${failed ? 100 : progressPct}%` }}
          />
        </div>
      </div>

      {/* Steps */}
      <div className="px-5 py-4">
        <ol className="space-y-2.5">
          {PIPELINE_STAGE_ORDER.map((s, idx) => {
            const isDone = !failed && idx < currentIndex;
            const isCurrent = !failed && idx === currentIndex;
            const isPending = !failed && idx > currentIndex;

            return (
              <li key={s} className="flex items-center gap-3">
                {/* Icon */}
                <span className="flex h-5 w-5 shrink-0 items-center justify-center">
                  {isDone && (
                    <CheckCircle2
                      size={16}
                      className="text-emerald-500"
                    />
                  )}
                  {isCurrent && (
                    <Loader2
                      size={16}
                      className="animate-spin text-brand-600 dark:text-brand-400"
                    />
                  )}
                  {isPending && (
                    <CircleDashed
                      size={16}
                      className="text-slate-200 dark:text-slate-700"
                    />
                  )}
                  {failed && (
                    <XCircle size={16} className="text-rose-400" />
                  )}
                </span>

                {/* Label */}
                <span
                  className={cn(
                    "text-sm",
                    isCurrent && "font-semibold text-brand-700 dark:text-brand-400",
                    isDone && "text-slate-400 dark:text-slate-500 line-through",
                    isPending && "text-slate-300 dark:text-slate-600",
                    failed && "text-slate-300 dark:text-slate-600"
                  )}
                >
                  {PIPELINE_STAGE_LABELS[s]}
                </span>

                {isCurrent && (
                  <span className="ml-auto text-[10px] font-semibold uppercase tracking-wide text-brand-500 dark:text-brand-400 animate-pulse">
                    Running…
                  </span>
                )}
              </li>
            );
          })}
        </ol>

        {failed && (
          <div className="mt-3 rounded-xl bg-rose-50 px-4 py-3 dark:bg-rose-900/20">
            <p className="text-xs font-semibold text-rose-700 dark:text-rose-300">
              {errorMessage || "The pipeline failed. Please try again with a different query."}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
