import { cn } from "@/lib/cn";

interface ScoreBarProps {
  label: string;
  value: number; // 0-1
}

/** Small horizontal bar used for novelty/feasibility/impact scores on idea cards. */
export function ScoreBar({ label, value }: ScoreBarProps) {
  const pct = Math.round(value * 100);
  const colorClass =
    pct >= 70
      ? "from-emerald-400 to-emerald-500"
      : pct >= 40
      ? "from-amber-400 to-orange-400"
      : "from-rose-400 to-rose-500";

  return (
    <div className="flex-1">
      <div className="mb-1.5 flex items-center justify-between">
        <span className="text-[11px] font-semibold uppercase tracking-wide text-slate-400 dark:text-slate-500">
          {label}
        </span>
        <span
          className={cn(
            "text-xs font-bold",
            pct >= 70
              ? "text-emerald-600 dark:text-emerald-400"
              : pct >= 40
              ? "text-amber-600 dark:text-amber-400"
              : "text-rose-600 dark:text-rose-400"
          )}
        >
          {pct}%
        </span>
      </div>
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
        <div
          className={cn("h-full rounded-full bg-gradient-to-r transition-all duration-700", colorClass)}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
