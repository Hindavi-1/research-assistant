import type { HTMLAttributes } from "react";
import { cn } from "@/lib/cn";

type BadgeVariant = "default" | "success" | "warning" | "danger" | "info";

const VARIANT_CLASSES: Record<BadgeVariant, string> = {
  default: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300",
  success: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
  warning: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
  danger: "bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300",
  info: "bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300",
};

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium",
        VARIANT_CLASSES[variant],
        className
      )}
      {...props}
    />
  );
}
