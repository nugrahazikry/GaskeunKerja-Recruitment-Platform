import type { ReactNode } from "react";
import { Navigate, useLocation, useParams, useSearchParams } from "react-router-dom";
import { useCandidateSelf } from "./useCandidateSelf";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { InvalidLinkPage } from "../pages/InvalidLinkPage";

type CandidateSelf = {
  id: number;
  alias: string;
  job_title: string;
  has_consent: boolean;
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
  const location = useLocation();
  const token = searchParams.get("token");
  const id = Number(candidateId);

  const state = useCandidateSelf(id, token);

  if (state.status === "loading") {
    return <SpinnerWithLabel label="Memuat..." />;
  }
  if (state.status === "invalid") {
    return <InvalidLinkPage />;
  }
  // Once the interview is done, re-clicking the invite link (or the consent/camera-test steps
  // within it) must never re-enter consent/camera-test — it should land straight on the
  // "wawancara selesai" screen. Checked before the consent gate so it wins regardless of
  // has_consent. Guarded on the current path so the interview page itself (which renders that
  // screen) doesn't redirect into a loop.
  if (state.candidate.interview_completed && !location.pathname.endsWith("/interview")) {
    return <Navigate to={`/candidate/${id}/interview?token=${token}`} replace />;
  }
  if (requireConsent && !state.candidate.has_consent) {
    return <Navigate to={`/candidate/${id}/consent?token=${token}`} replace />;
  }
  return <>{children(state.candidate, token!)}</>;
}
