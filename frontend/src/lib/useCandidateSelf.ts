import { useEffect, useState } from "react";
import { api } from "../api/client";

type CandidateSelf = {
  id: number;
  job_title: string;
  has_consent: boolean;
  has_telegram_link: boolean;
  interview_completed: boolean;
};

type State =
  | { status: "loading" }
  | { status: "invalid" }
  | { status: "ready"; candidate: CandidateSelf };

/** Resolves a candidate's own token against the backend. A 401 (expired/unknown token)
 * is what Area 1 T3's route guard renders as the shared "link tidak valid" screen. */
export function useCandidateSelf(candidateId: number, token: string | null): State {
  const [state, setState] = useState<State>({ status: "loading" });

  useEffect(() => {
    if (!token) {
      setState({ status: "invalid" });
      return;
    }

    let cancelled = false;
    setState({ status: "loading" });

    api
      .GET("/candidates/{candidate_id}/self", {
        params: { path: { candidate_id: candidateId }, query: { token } },
      })
      .then(({ data, error }) => {
        if (cancelled) return;
        if (error || !data) {
          setState({ status: "invalid" });
          return;
        }
        setState({ status: "ready", candidate: data });
      })
      .catch(() => {
        if (!cancelled) setState({ status: "invalid" });
      });

    return () => {
      cancelled = true;
    };
  }, [candidateId, token]);

  return state;
}
