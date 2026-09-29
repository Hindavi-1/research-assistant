import { cn } from "@/lib/cn";

interface ScoreBarProps {
  label: string;
  value: number; // 0-1
}

/** Small horizontal bar used for novelty/feasibility/impact scores on idea cards. */
export function ScoreBar({ label, value }: ScoreBarProps) {
  const pct = Math.round(value * 100);
  const colorClass =
    pct >= 70 ? "bg-emerald-500" : pct >= 40 ? "bg-amber-500" : "bg-rose-500";

  return (
    <div className="flex-1">
      <div className="mb-1 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
        <span>{label}</span>
        <span className="font-medium">{pct}%</span>
      </div>
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
        <div className={cn("h-full rounded-full", colorClass)} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
