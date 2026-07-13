import type { ReactNode } from "react";
import { Navigate, useParams, useSearchParams } from "react-router-dom";
import { useCandidateSelf } from "./useCandidateSelf";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { InvalidLinkPage } from "../pages/InvalidLinkPage";

type CandidateSelf = {
  id: number;
  job_title: string;
  has_consent: boolean;
  has_telegram_link: boolean;
  interview_completed: boolean;
};

/** Resolves the candidate by token from the URL, then either renders children (passing
 * the resolved candidate + token down via render prop) or redirects: invalid/expired
 * token -> shared "link tidak valid" screen; no consent yet -> /candidate/:id/consent. */
export function CandidateTokenGuard({
  requireConsent,
  children,
}: {
  requireConsent: boolean;
  children: (candidate: CandidateSelf, token: string) => ReactNode;
}) {
  const { candidateId } = useParams();
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const id = Number(candidateId);

  const state = useCandidateSelf(id, token);

  if (state.status === "loading") {
    return <SpinnerWithLabel label="Memuat..." />;
  }
  if (state.status === "invalid") {
    return <InvalidLinkPage />;
  }
  if (requireConsent && !state.candidate.has_consent) {
    return <Navigate to={`/candidate/${id}/consent?token=${token}`} replace />;
  }
  return <>{children(state.candidate, token!)}</>;
}
