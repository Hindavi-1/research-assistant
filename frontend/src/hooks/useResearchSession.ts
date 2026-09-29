"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type {
  CreateSessionPayload,
  Paper,
  PipelineStage,
  ResearchGap,
  ResearchIdea,
  ResearchSession,
} from "@/lib/types";

const TERMINAL_STAGES: PipelineStage[] = [
  "awaiting_human_review",
  "completed",
  "failed",
];

const POLL_INTERVAL_MS = 2500;

interface UseResearchSessionState {
  session: ResearchSession | null;
  papers: Paper[];
  gaps: ResearchGap[];
  ideas: ResearchIdea[];
  isSubmitting: boolean;
  isPolling: boolean;
  error: string | null;
}

/**
 * Encapsulates the whole client-side lifecycle of a research session:
 * submit query -> poll pipeline stage -> fetch results once the pipeline
 * reaches a terminal stage. Any page/component can reuse this instead of
 * re-implementing polling logic.
 */
export function useResearchSession() {
  const [state, setState] = useState<UseResearchSessionState>({
    session: null,
    papers: [],
    gaps: [],
    ideas: [],
    isSubmitting: false,
    isPolling: false,
    error: null,
  });

  const pollTimer = useRef<ReturnType<typeof setInterval> | null>(null);

  const clearPolling = useCallback(() => {
    if (pollTimer.current) {
      clearInterval(pollTimer.current);
      pollTimer.current = null;
    }
    setState((s) => ({ ...s, isPolling: false }));
  }, []);

  const fetchResults = useCallback(async (sessionId: string) => {
    const [papers, gaps, ideas] = await Promise.all([
      api.getPapers(sessionId),
      api.getGaps(sessionId),
      api.getIdeas(sessionId),
    ]);
    setState((s) => ({ ...s, papers, gaps, ideas }));
  }, []);

  const pollStatus = useCallback(
    (sessionId: string) => {
      pollTimer.current = setInterval(async () => {
        try {
          const status = await api.getSessionStatus(sessionId);
          setState((s) =>
            s.session ? { ...s, session: { ...s.session, ...status } } : s
          );

          if (TERMINAL_STAGES.includes(status.stage)) {
            clearPolling();
            if (status.stage !== "failed") {
              await fetchResults(sessionId);
            }
          }
        } catch (err) {
          clearPolling();
          setState((s) => ({
            ...s,
            error: err instanceof ApiError ? err.message : "Failed to poll session status.",
          }));
        }
      }, POLL_INTERVAL_MS);
    },
    [clearPolling, fetchResults]
  );

  const submitQuery = useCallback(
    async (payload: CreateSessionPayload) => {
      setState((s) => ({ ...s, isSubmitting: true, error: null }));
      try {
        const session = await api.createSession(payload);
        setState((s) => ({
          ...s,
          session,
          papers: [],
          gaps: [],
          ideas: [],
          isSubmitting: false,
          isPolling: true,
        }));
        pollStatus(session.id);
      } catch (err) {
        setState((s) => ({
          ...s,
          isSubmitting: false,
          error: err instanceof ApiError ? err.message : "Failed to create session.",
        }));
      }
    },
    [pollStatus]
  );

  const submitReview = useCallback(
    async (ideaId: string, status: "approved" | "rejected", selectedTitleId?: string) => {
      const updated = await api.submitReview({
        idea_id: ideaId,
        status,
        selected_title_id: selectedTitleId ?? null,
      });
      setState((s) => ({
        ...s,
        ideas: s.ideas.map((idea) => (idea.id === updated.id ? updated : idea)),
      }));
    },
    []
  );

  useEffect(() => clearPolling, [clearPolling]);

  return { ...state, submitQuery, submitReview };
}
