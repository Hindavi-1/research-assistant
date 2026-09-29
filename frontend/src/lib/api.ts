// Minimal typed fetch client for the backend API. Centralizing this here
// means components never construct URLs or handle fetch/JSON boilerplate
// themselves — they just call e.g. `api.createSession(...)`.
import type {
  CreateSessionPayload,
  HumanReviewPayload,
  Paper,
  ResearchGap,
  ResearchIdea,
  ResearchSession,
} from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {
      // response wasn't JSON; keep statusText
    }
    throw new ApiError(detail, res.status);
  }

  return res.json() as Promise<T>;
}

export const api = {
  createSession: (payload: CreateSessionPayload) =>
    request<ResearchSession>("/sessions", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  listSessions: () => request<ResearchSession[]>("/sessions"),

  getSession: (sessionId: string) =>
    request<ResearchSession>(`/sessions/${sessionId}`),

  getSessionStatus: (sessionId: string) =>
    request<Pick<ResearchSession, "id" | "stage" | "error_message">>(
      `/sessions/${sessionId}/status`
    ),

  getPapers: (sessionId: string) =>
    request<Paper[]>(`/sessions/${sessionId}/papers`),

  getGaps: (sessionId: string) =>
    request<ResearchGap[]>(`/sessions/${sessionId}/gaps`),

  getIdeas: (sessionId: string) =>
    request<ResearchIdea[]>(`/sessions/${sessionId}/ideas`),

  submitReview: (payload: HumanReviewPayload) =>
    request<ResearchIdea>("/research/review", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};

export { ApiError };
