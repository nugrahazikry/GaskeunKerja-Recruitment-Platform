import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { TopBar } from "../components/TopBar";
import { Button } from "../components/Button";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { ErrorState } from "../components/ErrorState";
import { BASE_URL, getHrToken, api } from "../api/client";

function fitLabel(score: number): string {
  const pct = score * 100;
  if (pct >= 75) return "Sangat Cocok";
  if (pct >= 50) return "Cocok";
  return "Kurang Cocok";
}

type State =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; alias: string; jobTitle: string; matchScore: number | null; pdfUrl: string };

/** Round-3 Task 18: HR-facing raw CV viewer, alongside the candidate's match score, so HR can
 * check the actual uploaded document rather than only the parsed/redacted profile. Same
 * blob-fetch pattern as AudioPlayer.tsx (Bearer-token fetch -> object URL), since the PDF endpoint
 * is HR-scoped like every other candidate-detail route. */
export function CandidateCvPage() {
  const { jobId, candidateId } = useParams();
  const navigate = useNavigate();
  const [state, setState] = useState<State>({ status: "loading" });

  useEffect(() => {
    let cancelled = false;
    let objectUrl: string | null = null;
    setState({ status: "loading" });

    api
      .GET("/candidates/{candidate_id}/detail", { params: { path: { candidate_id: Number(candidateId) } } })
      .then(async ({ data, error }) => {
        if (cancelled) return;
        if (error || !data || !data.cv_url) {
          setState({ status: "error", message: "CV tidak tersedia untuk kandidat ini." });
          return;
        }
        try {
          const res = await fetch(`${BASE_URL}${data.cv_url}`, {
            headers: { Authorization: `Bearer ${getHrToken()}` },
          });
          if (!res.ok) throw new Error("failed");
          const blob = await res.blob();
          if (cancelled) return;
          objectUrl = URL.createObjectURL(blob);
          setState({
            status: "ready",
            alias: data.alias,
            jobTitle: data.job_title,
            matchScore: data.match_score,
            pdfUrl: objectUrl,
          });
        } catch {
          if (!cancelled) setState({ status: "error", message: "Gagal memuat CV." });
        }
      });

    return () => {
      cancelled = true;
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [candidateId]);

  return (
    <div>
      <TopBar active="kandidat" jobId={Number(jobId)} />
      <div className="main wide">
        <div
          className="pagehead"
          style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}
        >
          <div>
            <h1>{state.status === "ready" ? `CV · ${state.alias}` : "CV Kandidat"}</h1>
            <p>
              {state.status === "ready" ? (
                <>
                  {state.jobTitle}
                  {state.matchScore !== null && (
                    <>
                      {" "}
                      &middot; Skor Kecocokan {Math.round(state.matchScore * 100)} &middot;{" "}
                      {fitLabel(state.matchScore)}
                    </>
                  )}
                </>
              ) : (
                "..."
              )}
            </p>
          </div>
          <Button variant="ghost" onClick={() => navigate(`/jobs/${jobId}/candidates/${candidateId}`)}>
            Kembali ke Detail Kandidat
          </Button>
        </div>

        {state.status === "loading" && <SpinnerWithLabel label="Memuat CV..." />}
        {state.status === "error" && <ErrorState message={state.message} />}
        {state.status === "ready" && (
          <div className="card" style={{ padding: 0, overflow: "hidden" }}>
            <iframe
              src={state.pdfUrl}
              title="CV Kandidat"
              style={{ width: "100%", height: "80vh", border: "none", display: "block" }}
            />
          </div>
        )}
      </div>
    </div>
  );
}
