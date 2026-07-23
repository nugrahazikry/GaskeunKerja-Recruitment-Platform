import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { TopBar } from "../components/TopBar";
import { Button } from "../components/Button";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { ErrorState } from "../components/ErrorState";
import { BASE_URL, getHrToken, api } from "../api/client";

type State =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; alias: string; jobTitle: string; pdfUrl: string };

/** HR-facing PDF preview for the laporan pengembangan — "Lihat Laporan" opens this. Same
 * blob-fetch pattern as CandidateCvPage.tsx (Bearer-token fetch -> object URL -> <iframe>), since
 * the PDF endpoint is HR-scoped like every other candidate-detail route.
 *
 * 2026-07-22 (user-requested): "Kirim Laporan via Email" removed from here — sending the report
 * is no longer a standalone action. It now only ever happens as part of "Ambil Keputusan" on
 * ReportPage.tsx, which sends the decision AND the report together in one combined email. */
export function ReportPdfPage() {
  const { jobId, candidateId } = useParams();
  const navigate = useNavigate();
  const [state, setState] = useState<State>({ status: "loading" });

  useEffect(() => {
    let cancelled = false;
    let objectUrl: string | null = null;
    setState({ status: "loading" });

    api
      .GET("/candidates/{candidate_id}/report", { params: { path: { candidate_id: Number(candidateId) } } })
      .then(async ({ data, error }) => {
        if (cancelled) return;
        if (error || !data) {
          setState({
            status: "error",
            message: (error as { detail?: string } | undefined)?.detail ?? "Gagal memuat laporan.",
          });
          return;
        }
        try {
          const res = await fetch(`${BASE_URL}/candidates/${candidateId}/report/pdf`, {
            headers: { Authorization: `Bearer ${getHrToken()}` },
          });
          if (!res.ok) throw new Error("failed");
          const blob = await res.blob();
          if (cancelled) return;
          objectUrl = URL.createObjectURL(blob);
          setState({ status: "ready", alias: data.candidate_alias, jobTitle: data.job_title, pdfUrl: objectUrl });
        } catch {
          if (!cancelled) setState({ status: "error", message: "Gagal memuat laporan PDF." });
        }
      });

    return () => {
      cancelled = true;
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [candidateId]);

  return (
    <div>
      <TopBar active="laporan" jobId={Number(jobId)} />
      <div className="main wide">
        <div className="pagehead">
          <h1 style={{ textTransform: "uppercase" }}>
            {state.status === "ready"
              ? `Laporan Feedback CV dan Wawancara · ${state.alias}`
              : "Laporan Feedback CV dan Wawancara"}
          </h1>
          <p style={{ textTransform: "uppercase" }}>{state.status === "ready" ? state.jobTitle : "..."}</p>
          <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
            <Button variant="ghost" onClick={() => navigate(`/jobs/${jobId}/candidates/${candidateId}/report`)}>
              Kembali ke Laporan
            </Button>
          </div>
        </div>

        {state.status === "loading" && <SpinnerWithLabel label="Memuat laporan..." />}
        {state.status === "error" && <ErrorState message={state.message} />}
        {state.status === "ready" && (
          <div className="card" style={{ padding: 0, overflow: "hidden" }}>
            <iframe
              src={state.pdfUrl}
              title="Laporan Kandidat"
              style={{ width: "100%", height: "80vh", border: "none", display: "block" }}
            />
          </div>
        )}
      </div>
    </div>
  );
}
