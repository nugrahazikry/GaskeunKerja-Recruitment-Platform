import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { TopBar } from "../components/TopBar";
import { Badge } from "../components/Badge";
import { Button } from "../components/Button";
import { Modal } from "../components/Modal";
import { SkeletonLoader } from "../components/SkeletonLoader";
import { ErrorState } from "../components/ErrorState";
import { EmptyState } from "../components/EmptyState";
import { api } from "../api/client";

type ReportListItem = {
  candidate_id: number;
  alias: string;
  interview_completed: boolean;
  // 2026-07-22 (user-reported "glitch"): true only once the post-interview LLM chain (through the
  // upskilling plan) has actually finished — interview_completed alone just means the videos
  // exist. Gates "Lihat Laporan" so a candidate can't be opened mid-pipeline with a hollow report.
  processing_complete: boolean;
  decision: string | null;
  decided_at: string | null;
  match_score: number | null;
  report_sent: boolean;
};

type State =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; jobTitle: string; items: ReportListItem[] };

type JobOption = { id: number; title: string; candidate_count: number };

type KeputusanFilter = "semua" | "menunggu_wawancara" | "menunggu_keputusan" | "advance" | "reject";

function scoreColor(scoreOn100: number): string {
  if (scoreOn100 >= 70) return "var(--success)";
  if (scoreOn100 >= 40) return "var(--warning)";
  return "var(--danger)";
}

// Round 12 follow-up: the Laporan page now shows every candidate (not just decided ones), so
// "Keputusan" needs two extra states beyond Lanjutkan/Tolak — mirrors the real pipeline: a
// candidate can't be decided before they're interviewed, and can't be interviewed-and-decided
// without passing through "interviewed, no decision yet" first.
function keputusanFor(item: ReportListItem): { key: KeputusanFilter; label: string; tone: "neutral" | "warning" | "success" | "danger" } {
  if (item.decision === "advance") return { key: "advance", label: "Lanjutkan", tone: "success" };
  if (item.decision === "reject") return { key: "reject", label: "Tolak", tone: "danger" };
  if (item.interview_completed) return { key: "menunggu_keputusan", label: "Menunggu Keputusan HR", tone: "warning" };
  return { key: "menunggu_wawancara", label: "Menunggu Wawancara", tone: "neutral" };
}

export function JobReportsPage() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [state, setState] = useState<State>({ status: "loading" });
  const [reloadKey, setReloadKey] = useState(0);
  const [jobOptions, setJobOptions] = useState<JobOption[]>([]);
  const [query, setQuery] = useState("");
  const [decisionFilter, setDecisionFilter] = useState<KeputusanFilter>("semua");
  const [sortMode, setSortMode] = useState<"date" | "score">("score");
  const [blockedNotice, setBlockedNotice] = useState<string | null>(null);

  useEffect(() => {
    api.GET("/jobs").then(({ data }) => {
      if (data) {
        // Same convention as the Kandidat page's job picker — only jobs with at least one
        // analyzed CV are offered, plus whichever job is currently open (so the dropdown never
        // silently loses its own current value).
        const options = data
          .filter((j) => j.candidate_count > 0 || j.id === Number(jobId))
          .map((j) => ({ id: j.id, title: j.title, candidate_count: j.candidate_count }));
        setJobOptions(options);
      }
    });
  }, [jobId]);

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });
    Promise.all([
      api.GET("/jobs/{job_id}", { params: { path: { job_id: Number(jobId) } } }),
      api.GET("/jobs/{job_id}/reports", { params: { path: { job_id: Number(jobId) } } }),
    ]).then(([jobRes, reportsRes]) => {
      if (cancelled) return;
      if (jobRes.error || !jobRes.data || reportsRes.error || !reportsRes.data) {
        setState({ status: "error" });
        return;
      }
      setState({ status: "ready", jobTitle: jobRes.data.title, items: reportsRes.data });
    });
    return () => {
      cancelled = true;
    };
  }, [jobId, reloadKey]);

  const items = state.status === "ready" ? state.items : [];
  const advanceCount = items.filter((i) => i.decision === "advance").length;
  const rejectCount = items.filter((i) => i.decision === "reject").length;
  const waitingInterviewCount = items.filter((i) => keputusanFor(i).key === "menunggu_wawancara").length;
  const waitingDecisionCount = items.filter((i) => keputusanFor(i).key === "menunggu_keputusan").length;

  const filteredItems = items.filter((item) => {
    if (decisionFilter !== "semua" && keputusanFor(item).key !== decisionFilter) return false;
    if (query.trim() && !item.alias.toLowerCase().includes(query.trim().toLowerCase())) return false;
    return true;
  });
  const sortedItems = [...filteredItems].sort((a, b) => {
    if (sortMode === "score") return (b.match_score ?? -1) - (a.match_score ?? -1);
    return new Date(b.decided_at ?? 0).getTime() - new Date(a.decided_at ?? 0).getTime();
  });

  function handleLihatLaporan(item: ReportListItem) {
    // Gate matches the backend's own rule (routers/report.py::_require_report_ready) — a report
    // can be viewed once the interview is done, even before HR decides, but only once the
    // post-interview LLM chain (through the upskilling plan) has actually finished too.
    if (!item.interview_completed) {
      setBlockedNotice("Kandidat ini belum memulai wawancara.");
      return;
    }
    if (!item.processing_complete) {
      setBlockedNotice(
        "Laporan kandidat ini masih diproses oleh sistem AI (transkripsi, penilaian, dan rencana pengembangan). Silakan coba lagi dalam beberapa menit."
      );
      return;
    }
    navigate(`/jobs/${jobId}/candidates/${item.candidate_id}/report`);
  }

  return (
    <div>
      <TopBar active="laporan" jobId={Number(jobId)} />
      <div className="main wide">
        <div className="pagehead">
          <h1>Laporan Kandidat &middot; {state.status === "ready" ? state.jobTitle : "..."}</h1>
          <p>Ringkasan keputusan HR dan status pengiriman laporan untuk setiap kandidat yang telah diproses</p>
        </div>

        {state.status === "ready" && items.length > 0 && (
          <div className="stat-grid">
            <div className="stat-tile">
              <div className="stat-num">{items.length}</div>
              <div className="stat-label">Total Kandidat</div>
            </div>
            <div className="stat-tile warn">
              <div className="stat-num">{waitingInterviewCount}</div>
              <div className="stat-label">Menunggu Wawancara</div>
            </div>
            <div className="stat-tile">
              <div className="stat-num" style={{ color: "var(--ink-2)" }}>{waitingDecisionCount}</div>
              <div className="stat-label">Menunggu Keputusan HR</div>
            </div>
            <div className="stat-tile">
              <div className="stat-num" style={{ color: "var(--success)" }}>{advanceCount}</div>
              <div className="stat-label">Lanjutkan</div>
            </div>
            <div className="stat-tile">
              <div className="stat-num" style={{ color: "var(--danger)" }}>{rejectCount}</div>
              <div className="stat-label">Tolak</div>
            </div>
          </div>
        )}

        <div className="card" style={{ padding: "14px 18px", marginBottom: 16 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
            {jobOptions.length > 0 && (
              <select
                className="select-control"
                value={jobId}
                onChange={(e) => navigate(`/jobs/${e.target.value}/reports`)}
                style={{ minWidth: 190 }}
                aria-label="Pilih lowongan"
              >
                {jobOptions.map((j) => (
                  <option key={j.id} value={j.id}>
                    {j.title}
                  </option>
                ))}
              </select>
            )}
            <input
              type="text"
              className="text-control"
              placeholder="Cari nama kandidat..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              style={{ flex: "1 1 160px", minWidth: 0 }}
              aria-label="Cari laporan"
            />
            <select
              className="select-control"
              value={decisionFilter}
              onChange={(e) => setDecisionFilter(e.target.value as KeputusanFilter)}
              style={{ minWidth: 190, flexShrink: 0 }}
              aria-label="Filter keputusan"
            >
              <option value="semua">Keputusan: Semua</option>
              <option value="menunggu_wawancara">Keputusan: Menunggu Wawancara</option>
              <option value="menunggu_keputusan">Keputusan: Menunggu Keputusan HR</option>
              <option value="advance">Keputusan: Lanjutkan</option>
              <option value="reject">Keputusan: Tolak</option>
            </select>
            <select
              className="select-control"
              value={sortMode}
              onChange={(e) => setSortMode(e.target.value as typeof sortMode)}
              style={{ minWidth: 170, flexShrink: 0, marginLeft: "auto" }}
              aria-label="Urutkan laporan"
            >
              <option value="date">Urutkan: Tanggal terbaru</option>
              <option value="score">Urutkan: Skor tertinggi</option>
            </select>
          </div>
        </div>

        <div className="card">
          <div style={{ padding: "18px 20px 0" }}>
            <div className="serif" style={{ fontWeight: 700 }}>
              Riwayat Keputusan
            </div>
            <p className="hint" style={{ marginTop: 4 }}>
              Laporan dapat dikirim ulang ke kandidat kapan saja dari halaman detail
            </p>
          </div>

          {state.status === "loading" && <SkeletonLoader rows={4} />}
          {state.status === "error" && (
            <ErrorState message="Gagal memuat daftar laporan." onRetry={() => setReloadKey((k) => k + 1)} />
          )}
          {state.status === "ready" && items.length === 0 && (
            <EmptyState message="Belum ada kandidat untuk lowongan ini." />
          )}
          {state.status === "ready" && items.length > 0 && (
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 150px 170px 110px 140px",
                gap: 16,
                padding: "10px 20px",
                fontSize: "0.72rem",
                fontWeight: 700,
                textTransform: "uppercase",
                letterSpacing: "0.05em",
                color: "var(--muted)",
                borderTop: "1px solid var(--border)",
                borderBottom: "1px solid var(--border)",
              }}
            >
              <span>Kandidat</span>
              <span style={{ textAlign: "center" }}>Skor</span>
              <span style={{ textAlign: "center" }}>Keputusan</span>
              <span style={{ textAlign: "center" }}>Status Kirim</span>
              <span style={{ textAlign: "center" }}>Aksi</span>
            </div>
          )}
          {state.status === "ready" && items.length > 0 && sortedItems.length === 0 && (
            <EmptyState message="Tidak ada laporan yang cocok dengan pencarian/filter." />
          )}
          {state.status === "ready" &&
            sortedItems.map((item) => {
              const scoreOn100 = item.match_score !== null ? Math.round(item.match_score * 100) : null;
              const keputusan = keputusanFor(item);
              return (
                <div
                  key={item.candidate_id}
                  style={{
                    display: "grid",
                    // Fixed column widths so the score bar, badge, and sent-indicator start at the
                    // same x on every row — variable-length labels ("Lanjutkan" vs "Menunggu
                    // Keputusan HR") in a plain flex row would shift everything after them sideways.
                    gridTemplateColumns: "1fr 150px 170px 110px 140px",
                    alignItems: "center",
                    gap: 16,
                    padding: "14px 20px",
                    borderBottom: "1px solid var(--border)",
                  }}
                >
                  <div>
                    <strong>{item.alias}</strong>
                    <div style={{ fontSize: "0.78rem", color: "var(--muted)", marginTop: 2 }}>
                      {item.decided_at
                        ? `Diputuskan ${new Date(item.decided_at).toLocaleDateString("id-ID")}`
                        : item.interview_completed
                          ? item.processing_complete
                            ? "Wawancara selesai"
                            : "Sedang diproses oleh sistem..."
                          : "Belum wawancara"}
                    </div>
                  </div>

                  {scoreOn100 !== null ? (
                    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 8 }}>
                      <div style={{ width: 90, height: 7, borderRadius: "var(--radius-sm)", background: "var(--border)", overflow: "hidden" }}>
                        <div
                          style={{
                            height: "100%",
                            width: `${scoreOn100}%`,
                            background: scoreColor(scoreOn100),
                            borderRadius: "var(--radius-sm)",
                          }}
                        />
                      </div>
                      <span style={{ fontSize: "0.82rem", fontWeight: 700, width: 22, textAlign: "right" }}>
                        {scoreOn100}
                      </span>
                    </div>
                  ) : (
                    <span />
                  )}

                  <div style={{ display: "flex", justifyContent: "center" }}>
                    <Badge tone={keputusan.tone}>{keputusan.label}</Badge>
                  </div>

                  <span className="hint" style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 5 }}>
                    <span
                      style={{
                        width: 7,
                        height: 7,
                        borderRadius: "50%",
                        background: item.report_sent ? "var(--success)" : "var(--muted)",
                        display: "inline-block",
                        flexShrink: 0,
                      }}
                    />
                    {item.report_sent ? "Terkirim" : "Belum dikirim"}
                  </span>

                  <Button variant="secondary" onClick={() => handleLihatLaporan(item)}>
                    Lihat Laporan
                  </Button>
                </div>
              );
            })}
        </div>
      </div>

      {blockedNotice && (
        <Modal title="Belum Bisa Membuka Laporan" onClose={() => setBlockedNotice(null)}>
          <p style={{ fontSize: "0.86rem", color: "var(--ink-2)", lineHeight: 1.6 }}>{blockedNotice}</p>
          <div className="modal-actions">
            <Button variant="ghost" onClick={() => setBlockedNotice(null)}>
              Tutup
            </Button>
          </div>
        </Modal>
      )}
    </div>
  );
}
