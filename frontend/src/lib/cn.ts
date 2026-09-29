import { clsx, type ClassValue } from "clsx";

/** Tiny className joiner used across all UI components. */
export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}
