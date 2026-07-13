import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Card } from "../components/Card";
import { Badge } from "../components/Badge";
import { Button } from "../components/Button";
import { SkeletonLoader } from "../components/SkeletonLoader";
import { ErrorState } from "../components/ErrorState";
import { EmptyState } from "../components/EmptyState";
import { api } from "../api/client";

type CandidateMatch = {
  candidate_id: number;
  alias: string;
  overall_score: number;
  rank: number;
  competency_breakdown: {
    semantic_similarity?: number;
    graph_boost?: number;
    matched_competencies?: string[];
  };
  invited: boolean;
  interview_completed: boolean;
  decided: boolean;
};

type State =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; candidates: CandidateMatch[] };

function statusFor(c: CandidateMatch): { label: string; tone: "neutral" | "warning" | "success" } {
  if (c.decided || c.interview_completed) return { label: "Selesai wawancara", tone: "success" };
  if (c.invited) return { label: "Menunggu wawancara", tone: "warning" };
  return { label: "Belum diundang", tone: "neutral" };
}

export function ShortlistPage() {
  const { jobId } = useParams();
  const [state, setState] = useState<State>({ status: "loading" });
  const [reloadKey, setReloadKey] = useState(0);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });
    api
      .GET("/jobs/{job_id}/candidates", { params: { path: { job_id: Number(jobId) } } })
      .then(({ data, error }) => {
        if (cancelled) return;
        if (error || !data) {
          setState({ status: "error" });
          return;
        }
        setState({ status: "ready", candidates: data });
      });
    return () => {
      cancelled = true;
    };
  }, [jobId, reloadKey]);

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", padding: "0 16px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <h1>Kandidat</h1>
        <div style={{ display: "flex", gap: 12 }}>
          <Link to={`/jobs/${jobId}/questions`}>
            <Button variant="secondary">Pertanyaan Wawancara</Button>
          </Link>
          <Link to="/jobs">
            <Button variant="secondary">Kembali ke Daftar Lowongan</Button>
          </Link>
        </div>
      </div>

      <Card>
        {state.status === "loading" && <SkeletonLoader rows={4} />}
        {state.status === "error" && (
          <ErrorState message="Gagal memuat kandidat." onRetry={() => setReloadKey((k) => k + 1)} />
        )}
        {state.status === "ready" && state.candidates.length === 0 && (
          <EmptyState message="Belum ada kandidat yang cocok untuk lowongan ini." />
        )}
        {state.status === "ready" && state.candidates.length > 0 && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "40px 1fr 100px 160px 160px",
                gap: 8,
                fontWeight: 600,
                fontSize: 13,
                color: "var(--color-ink-500)",
                padding: "0 12px",
              }}
            >
              <span>#</span>
              <span>Kandidat</span>
              <span>Skor</span>
              <span>Status</span>
              <span></span>
            </div>
            {state.candidates.map((c) => {
              const status = statusFor(c);
              const isExpanded = expandedId === c.candidate_id;
              return (
                <div key={c.candidate_id} style={{ border: "1px solid var(--color-border)", borderRadius: "var(--radius-md)" }}>
                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: "40px 1fr 100px 160px 160px",
                      gap: 8,
                      alignItems: "center",
                      padding: 12,
                      cursor: "pointer",
                    }}
                    onClick={() => setExpandedId(isExpanded ? null : c.candidate_id)}
                  >
                    <span>{c.rank}</span>
                    <span>{c.alias}</span>
                    <span>{c.overall_score.toFixed(2)}</span>
                    <Badge tone={status.tone}>{status.label}</Badge>
                    <Button
                      variant={c.invited ? "secondary" : "primary"}
                      onClick={(e) => {
                        e.stopPropagation();
                        alert(c.invited ? "T5c: Lihat Link Undangan (belum dibangun)" : "T5c: Undang ke Interview (belum dibangun)");
                      }}
                    >
                      {c.invited ? "Lihat Link Undangan" : "Undang ke Interview"}
                    </Button>
                  </div>
                  {isExpanded && (
                    <div style={{ padding: "0 12px 12px 52px", fontSize: 14 }}>
                      <p style={{ margin: "4px 0" }}>
                        Kemiripan semantik:{" "}
                        <strong>{((c.competency_breakdown.semantic_similarity ?? 0) * 100).toFixed(0)}%</strong>
                      </p>
                      <p style={{ margin: "4px 0" }}>
                        Bonus graf kompetensi: <strong>{((c.competency_breakdown.graph_boost ?? 0) * 100).toFixed(0)}%</strong>
                      </p>
                      <p style={{ margin: "4px 0" }}>
                        Kompetensi yang cocok:{" "}
                        {c.competency_breakdown.matched_competencies?.length ? (
                          <span style={{ display: "inline-flex", gap: 6, flexWrap: "wrap" }}>
                            {c.competency_breakdown.matched_competencies.map((name) => (
                              <Badge key={name} tone="info">
                                {name}
                              </Badge>
                            ))}
                          </span>
                        ) : (
                          <span style={{ opacity: 0.6 }}>Tidak ada kompetensi eksplisit yang cocok</span>
                        )}
                      </p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </Card>
    </div>
  );
}
