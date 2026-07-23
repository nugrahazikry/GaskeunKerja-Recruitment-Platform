import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { TopBar } from "../components/TopBar";
import { Badge } from "../components/Badge";
import { Button } from "../components/Button";
import { SkeletonLoader } from "../components/SkeletonLoader";
import { ErrorState } from "../components/ErrorState";
import { EmptyState } from "../components/EmptyState";
import { Table } from "../components/Table";
import { api } from "../api/client";

type CompetencyStatus = { competency_name: string; matched: boolean; proficiency: number | null };

type CandidateMatch = {
  candidate_id: number;
  alias: string;
  overall_score: number;
  rank: number;
  competency_breakdown: {
    matched_competencies?: string[];
    missing_competencies?: string[];
    competency_proficiency?: Record<string, number>;
  };
  competency_status: CompetencyStatus[];
  latest_role: string | null;
  invited: boolean;
  interview_completed: boolean;
  decided: boolean;
  cv_url: string | null;
  education_level: string | null;
  major: string | null;
  meets_education: boolean | null;
  has_email: boolean;
  invite_email_sent: boolean;
  skill_gap_ready: boolean;
};

type State =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; candidates: CandidateMatch[] };

// Round 10 follow-up: was folding `decided` into "Selesai Wawancara" (a candidate with an
// hr_decision already always has interview_completed=true too, so the old check never
// distinguished them) — but routers/jobs.py::_pipeline_breakdown already computes a real 4th
// "Sudah Diputuskan" bucket for the Lowongan page's funnel chart. This mirrors that same
// derivation per-candidate instead of inventing a new category, so the two pages agree.
//
// Round 14 follow-up (real bug, user-reported TWICE — first fix used `invited && has_email`,
// still wrong): `invited_at` is set the moment HR opens the invite modal (token generation), and
// `contact_email` can be added/edited long after with no send action happening — neither is
// proof a real invite email went out. The ONLY real signal is `invite_email_sent` (backend:
// candidates.invite_email_sent_at, set exclusively when routers/candidates.py::
// send_candidate_invite_email actually succeeds). Mirrors the identical fix in
// CandidateDetailPage.tsx::pipelineStatusFor().
function statusFor(c: CandidateMatch): { label: string; tone: "neutral" | "warning" | "info" | "success" } {
  if (c.decided) return { label: "Sudah Diputuskan", tone: "success" };
  // 2026-07-22 (user-reported): renamed from "Selesai Wawancara" — this stage means the interview
  // recording is done and processed, but HR hasn't made a decision yet, which "Menunggu Keputusan
  // HR" says explicitly. Matches JobReportsPage.tsx::keputusanFor() and
  // CandidateDetailPage.tsx::pipelineStatusFor(), which already used this label + tone.
  if (c.interview_completed) return { label: "Menunggu Keputusan HR", tone: "warning" };
  if (c.invite_email_sent) return { label: "Menunggu Wawancara", tone: "warning" };
  return { label: "Belum Diundang", tone: "neutral" };
}

function fitLabel(score: number): string {
  const pct = score * 100;
  if (pct >= 75) return "Sangat Cocok";
  if (pct >= 50) return "Cocok";
  return "Kurang Cocok";
}

/** Round-3 follow-up (2026-07-19): replaces the old semantic+graph-boost breakdown — scoring is
 * now entirely derived from the SAME grounded skill-gap analysis shown on Kandidat Detail (no
 * second, disagreeing system). Score = sum of proficiency points (1-3 per matched competency,
 * how strongly the candidate's experience evidences it) out of the max possible (3 per required
 * competency) — so two candidates matching the identical competency set can still score apart if
 * one shows deeper/more senior evidence than the other. */
/** Round 10 follow-up: same "X/Y kompetensi terpenuhi" metric ScoreBreakdown used to show as a
 * small hint under the score number — relocated into a full-width progress bar + caption between
 * the badges row and the competency table, so the coverage is visible at a glance without reading
 * the tooltip. */
function MatchBar({ items }: { items: CompetencyStatus[] }) {
  if (items.length === 0) return null;
  const matchedCount = items.filter((i) => i.matched).length;
  const pct = Math.round((matchedCount / items.length) * 100);
  return (
    <div style={{ margin: "10px 0 12px" }}>
      <div style={{ height: 8, borderRadius: "var(--radius-sm)", background: "var(--border)", overflow: "hidden" }}>
        <div style={{ height: "100%", width: `${pct}%`, background: "var(--success)", borderRadius: "var(--radius-sm)" }} />
      </div>
      <div
        className="hint"
        data-tooltip="Skor = jumlah poin kekuatan bukti (1-3) untuk setiap kompetensi yang terpenuhi, dibagi poin maksimum (3 × jumlah kompetensi wajib). Dua kandidat dengan kompetensi yang sama tetap bisa berbeda skor karena kedalaman pengalaman yang dievaluasi berbeda."
        style={{ marginTop: 4, cursor: "help" }}
      >
        {matchedCount}/{items.length} kompetensi terpenuhi ({pct}%) ⓘ
      </div>
    </div>
  );
}

const PROFICIENCY_LABEL: Record<number, string> = { 1: "Pemula ★", 2: "Menengah ★★", 3: "Mahir ★★★" };

/** Round-3 Task 20: separate eligibility badge — never folded into the numeric match score. */
function EducationBadge({ c }: { c: CandidateMatch }) {
  if (c.meets_education === null) return null;
  return (
    <Badge tone={c.meets_education ? "success" : "warning"}>
      {c.meets_education ? "Memenuhi syarat pendidikan" : "Belum memenuhi syarat pendidikan"}
      {c.education_level ? ` (${c.education_level})` : ""}
    </Badge>
  );
}

const PAGE_SIZE = 5;
const COMPETENCY_PAGE_SIZE = 5;

function CompetencyList({ items }: { items: CompetencyStatus[] }) {
  const [compPage, setCompPage] = useState(0);
  const totalCompPages = Math.max(1, Math.ceil(items.length / COMPETENCY_PAGE_SIZE));
  const pageItems = items.slice(compPage * COMPETENCY_PAGE_SIZE, compPage * COMPETENCY_PAGE_SIZE + COMPETENCY_PAGE_SIZE);

  return (
    <div>
      <div style={{ overflowX: "auto" }}>
        <Table
          keyField={(comp) => comp.competency_name}
          rows={pageItems}
          columns={[
            { header: "Kompetensi", width: "45%", render: (comp) => comp.competency_name },
            {
              header: "Level Kompetensi",
              width: "30%",
              render: (comp) =>
                comp.matched ? (comp.proficiency ? PROFICIENCY_LABEL[comp.proficiency] : "—") : "Tidak ada",
            },
            {
              header: "Status",
              width: "25%",
              render: (comp) => (
                <span className={comp.matched ? "ok" : "no"}>{comp.matched ? "Terpenuhi" : "Tidak Terpenuhi"}</span>
              ),
            },
          ]}
        />
      </div>
      {items.length > COMPETENCY_PAGE_SIZE && (
        <div style={{ display: "flex", justifyContent: "center", gap: 4, marginTop: 10 }}>
          {Array.from({ length: totalCompPages }, (_, i) => (
            <button
              key={i}
              onClick={() => setCompPage(i)}
              style={{
                width: 24,
                height: 24,
                borderRadius: "50%",
                border: "1px solid var(--border)",
                background: i === compPage ? "var(--teal)" : "var(--surface)",
                color: i === compPage ? "#fff" : "var(--muted)",
                fontSize: "0.7rem",
                fontWeight: 700,
                cursor: "pointer",
                padding: 0,
              }}
            >
              {i + 1}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

type JobOption = { id: number; title: string; candidate_count: number };

export function ShortlistPage() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [jobTitle, setJobTitle] = useState<string>("");
  const [jobOptions, setJobOptions] = useState<JobOption[]>([]);
  const [state, setState] = useState<State>({ status: "loading" });
  const [reloadKey, setReloadKey] = useState(0);
  const [page, setPage] = useState(0);
  const [query, setQuery] = useState("");
  const [sortMode, setSortMode] = useState<"score" | "name" | "status">("score");

  useEffect(() => {
    api.GET("/jobs/{job_id}", { params: { path: { job_id: Number(jobId) } } }).then(({ data }) => {
      if (data) setJobTitle(data.title);
    });
  }, [jobId]);

  useEffect(() => {
    api.GET("/jobs").then(({ data }) => {
      if (data) {
        // Only offer jobs that already have at least one CV analyzed — otherwise picking one
        // just lands on an empty shortlist. The currently-open job stays selectable regardless,
        // so the dropdown never silently drops its own current value.
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
    api
      .GET("/jobs/{job_id}/candidates", { params: { path: { job_id: Number(jobId) } } })
      .then(({ data, error }) => {
        if (cancelled) return;
        if (error || !data) {
          setState({ status: "error" });
          return;
        }
        setState({ status: "ready", candidates: data as CandidateMatch[] });
        setPage(0);
      });
    return () => {
      cancelled = true;
    };
  }, [jobId, reloadKey]);

  const STATUS_RANK: Record<string, number> = {
    "Sudah Diputuskan": 0,
    "Menunggu Keputusan HR": 1,
    "Menunggu Wawancara": 2,
    "Belum Diundang": 3,
  };

  const filteredCandidates =
    state.status === "ready"
      ? state.candidates.filter((c) => {
          if (!query.trim()) return true;
          const q = query.trim().toLowerCase();
          return c.alias.toLowerCase().includes(q) || (c.latest_role ?? "").toLowerCase().includes(q);
        })
      : [];

  const sortedCandidates = [...filteredCandidates].sort((a, b) => {
    if (sortMode === "name") return a.alias.localeCompare(b.alias);
    if (sortMode === "status") return STATUS_RANK[statusFor(a).label] - STATUS_RANK[statusFor(b).label];
    return b.overall_score - a.overall_score;
  });
  const totalPages = Math.max(1, Math.ceil(sortedCandidates.length / PAGE_SIZE));
  const pageCandidates = sortedCandidates.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE);

  // PERINGKAT is each candidate's fixed rank by score among ALL of this job's candidates — not
  // their position in the currently displayed (possibly re-sorted/filtered/paginated) list. Without
  // this, switching "Urutkan" to Nama A-Z or Status would relabel whoever happens to sort first as
  // "PERINGKAT #1", which is wrong: that label means "highest-scoring candidate," a fixed fact
  // about the candidate, not "wherever they land in the current view."
  const scoreRankById = new Map<number, number>();
  if (state.status === "ready") {
    [...state.candidates]
      .sort((a, b) => b.overall_score - a.overall_score)
      .forEach((c, idx) => scoreRankById.set(c.candidate_id, idx + 1));
  }

  useEffect(() => {
    setPage(0);
  }, [query, sortMode]);

  // Same 4 pipeline stages as the Lowongan page's funnel chart (routers/jobs.py::_pipeline_breakdown),
  // counted client-side via the same mutually-exclusive statusFor() so a candidate lands in exactly
  // one bucket here — unlike that backend endpoint, which additionally increments `diputuskan`
  // without excluding the candidate from `selesai_wawancara` too.
  const statusCounts =
    state.status === "ready"
      ? state.candidates.reduce(
          (acc, c) => {
            acc[statusFor(c).label] = (acc[statusFor(c).label] ?? 0) + 1;
            return acc;
          },
          {} as Record<string, number>
        )
      : {};

  return (
    <div>
      <TopBar active="kandidat" jobId={Number(jobId)} />
      <div className="main wide">
        <div className="pagehead">
          <h1>Kandidat Terseleksi &middot; {jobTitle || "..."}</h1>
          <p>Kandidat yang telah dianalisis AI, diurutkan berdasarkan tingkat kecocokan dengan lowongan</p>
        </div>

        {state.status === "ready" && state.candidates.length > 0 && (
          <div className="stat-grid">
            <div className="stat-tile">
              <div className="stat-num">{state.candidates.length}</div>
              <div className="stat-label">Total Kandidat</div>
            </div>
            <div className="stat-tile">
              <div className="stat-num" style={{ color: "var(--ink-2)" }}>{statusCounts["Belum Diundang"] ?? 0}</div>
              <div className="stat-label">Belum Diundang</div>
            </div>
            <div className="stat-tile warn">
              <div className="stat-num">{statusCounts["Menunggu Wawancara"] ?? 0}</div>
              <div className="stat-label">Menunggu Wawancara</div>
            </div>
            <div className="stat-tile">
              <div className="stat-num">{statusCounts["Menunggu Keputusan HR"] ?? 0}</div>
              <div className="stat-label">Menunggu Keputusan HR</div>
            </div>
            <div className="stat-tile">
              <div className="stat-num" style={{ color: "var(--success)" }}>{statusCounts["Sudah Diputuskan"] ?? 0}</div>
              <div className="stat-label">Sudah Diputuskan</div>
            </div>
          </div>
        )}

        <div className="card" style={{ padding: "14px 18px", marginBottom: 16 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
            {jobOptions.length > 0 && (
              <select
                id="job-picker"
                className="select-control"
                value={jobId}
                onChange={(e) => navigate(`/jobs/${e.target.value}`)}
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
              placeholder="Cari nama kandidat atau peran..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              style={{ flex: "1 1 220px" }}
              aria-label="Cari kandidat"
            />
            <select
              className="select-control"
              value={sortMode}
              onChange={(e) => setSortMode(e.target.value as typeof sortMode)}
              style={{ minWidth: 190 }}
              aria-label="Urutkan kandidat"
            >
              <option value="score">Urutkan: Skor tertinggi</option>
              <option value="name">Urutkan: Nama A-Z</option>
              <option value="status">Urutkan: Status wawancara</option>
            </select>
            <Link to={`/jobs/${jobId}/questions`} style={{ marginLeft: "auto" }}>
              <Button variant="secondary">Pertanyaan Wawancara</Button>
            </Link>
          </div>
        </div>

        {state.status === "ready" && state.candidates.length > 0 && sortedCandidates.length === 0 && (
          <EmptyState message="Tidak ada kandidat yang cocok dengan pencarian." />
        )}

        {state.status === "loading" && <SkeletonLoader rows={4} />}
        {state.status === "error" && (
          <ErrorState message="Gagal memuat kandidat." onRetry={() => setReloadKey((k) => k + 1)} />
        )}
        {state.status === "ready" && state.candidates.length === 0 && (
          <EmptyState message="Belum ada kandidat yang cocok untuk lowongan ini." />
        )}
        {state.status === "ready" &&
          pageCandidates.map((c, i) => {
            const status = statusFor(c);
            const scoreOn100 = Math.round(c.overall_score * 100);
            const overallRank = scoreRankById.get(c.candidate_id) ?? i + 1;
            return (
              <div className="card" key={c.candidate_id}>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
                  <span style={{ fontSize: "0.68rem", color: "var(--muted)", fontWeight: 700 }}>
                    PERINGKAT #{overallRank}
                  </span>
                </div>
                <div className="row">
                  <div>
                    <Link
                      to={`/jobs/${jobId}/candidates/${c.candidate_id}`}
                      style={{ fontWeight: 700, fontSize: "0.95rem", color: "var(--ink)", textDecoration: "none" }}
                    >
                      {c.alias}
                    </Link>
                    <div style={{ color: "var(--gold)", fontSize: "0.78rem", fontWeight: 600, marginTop: 2 }}>
                      {c.latest_role ?? "Belum ada riwayat pekerjaan"}
                    </div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div className="score">{scoreOn100}</div>
                    <div className="score-label">{fitLabel(c.overall_score)}</div>
                  </div>
                </div>

                <div style={{ margin: "10px 0", display: "flex", gap: 8, flexWrap: "wrap" }}>
                  <Badge tone={status.tone}>{status.label}</Badge>
                  <EducationBadge c={c} />
                </div>

                <MatchBar items={c.competency_status} />

                <CompetencyList items={c.competency_status} />

                <div style={{ marginTop: 12, display: "flex", gap: 8 }}>
                  <Link to={`/jobs/${jobId}/candidates/${c.candidate_id}`}>
                    <Button variant="primary">Lihat Detail &amp; Keputusan</Button>
                  </Link>
                </div>
              </div>
            );
          })}

        {state.status === "ready" && sortedCandidates.length > PAGE_SIZE && (
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              gap: 14,
              marginTop: 8,
            }}
          >
            <Button variant="ghost" disabled={page === 0} onClick={() => setPage((p) => p - 1)}>
              &larr; Sebelumnya
            </Button>
            <span style={{ fontSize: "0.8rem", color: "var(--muted)" }}>
              Halaman {page + 1} dari {totalPages} &middot; kandidat {page * PAGE_SIZE + 1}-
              {Math.min((page + 1) * PAGE_SIZE, sortedCandidates.length)} dari {sortedCandidates.length}
            </span>
            <Button
              variant="ghost"
              disabled={page >= totalPages - 1}
              onClick={() => setPage((p) => p + 1)}
            >
              Selanjutnya &rarr;
            </Button>
          </div>
        )}
      </div>

    </div>
  );
}
