import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { TopBar } from "../components/TopBar";
import { Badge } from "../components/Badge";
import { Button } from "../components/Button";
import { SkeletonLoader } from "../components/SkeletonLoader";
import { ErrorState } from "../components/ErrorState";
import { ColorPanel } from "../components/ColorPanel";
import { api } from "../api/client";
import { formatRelativeTime } from "../lib/formatRelativeTime";

function bulletLines(text: string): string[] {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .map((line) => (line.startsWith("- ") ? line.slice(2) : line.startsWith("-") ? line.slice(1).trim() : line));
}

function BulletDisplay({ text }: { text: string }) {
  const lines = bulletLines(text);
  if (lines.length === 0) return <p className="jd-text">-</p>;
  return (
    <ul className="color-panel-list">
      {lines.map((line, i) => (
        <li key={i}>{line}</li>
      ))}
    </ul>
  );
}

type Job = {
  id: number;
  company_id: number;
  company_name: string;
  title: string;
  responsibilities: string;
  requirements: string;
  qualifications: string;
  status: string;
  created_at: string;
};

type Competency = { id: number; competency_name: string; importance_level: number };

type Question = { id: number; job_id: number; question_text: string; order_index: number; status: string };

type CandidateMatch = {
  candidate_id: number;
  invited: boolean;
  interview_completed: boolean;
  decided: boolean;
};

type State =
  | { status: "loading" }
  | { status: "error" }
  | {
      status: "ready";
      job: Job;
      competencies: Competency[];
      questions: Question[];
      candidates: CandidateMatch[];
    };

function importanceDots(level: number) {
  // importance_level is a float, typically 1-3 in the seeded data — render up to 3 dots.
  const filled = Math.max(1, Math.min(3, Math.round(level)));
  return [1, 2, 3].map((n) => <i key={n} className={n <= filled ? "on" : ""} />);
}

export function JobDetailPage() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [state, setState] = useState<State>({ status: "loading" });
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });

    Promise.all([
      api.GET("/jobs/{job_id}", { params: { path: { job_id: Number(jobId) } } }),
      api.GET("/jobs/{job_id}/competencies", { params: { path: { job_id: Number(jobId) } } }),
      api.GET("/jobs/{job_id}/questions", { params: { path: { job_id: Number(jobId) } } }),
      api.GET("/jobs/{job_id}/candidates", { params: { path: { job_id: Number(jobId) } } }),
    ]).then(([jobRes, compRes, questionsRes, candidatesRes]) => {
      if (cancelled) return;
      if (jobRes.error || !jobRes.data) {
        setState({ status: "error" });
        return;
      }
      setState({
        status: "ready",
        job: jobRes.data,
        competencies: (compRes.data as Competency[]) ?? [],
        questions: (questionsRes.data as Question[]) ?? [],
        candidates: (candidatesRes.data as CandidateMatch[]) ?? [],
      });
    });

    return () => {
      cancelled = true;
    };
  }, [jobId, reloadKey]);

  if (state.status === "loading") {
    return (
      <div>
        <TopBar active="lowongan" jobId={Number(jobId)} />
        <div className="main wide">
          <SkeletonLoader rows={4} />
        </div>
      </div>
    );
  }

  if (state.status === "error") {
    return (
      <div>
        <TopBar active="lowongan" jobId={Number(jobId)} />
        <div className="main wide">
          <ErrorState message="Gagal memuat detail lowongan." onRetry={() => setReloadKey((k) => k + 1)} />
        </div>
      </div>
    );
  }

  const { job, competencies, questions, candidates } = state;

  const totalCandidates = candidates.length;
  const invitedCount = candidates.filter((c) => c.invited).length;
  const interviewedCount = candidates.filter((c) => c.interview_completed).length;
  const decidedCount = candidates.filter((c) => c.decided).length;

  const hasQuestions = questions.length > 0;
  const isApproved = questions.some((q) => q.status === "approved");
  const questionsStatusLabel = !hasQuestions ? "Belum dibuat" : isApproved ? "Disetujui" : "Draf";
  const questionsStatusTone = !hasQuestions ? "neutral" : isApproved ? "success" : "warning";

  return (
    <div>
      <TopBar active="lowongan" jobId={Number(jobId)} />
      <div className="main wide">
        <div className="row" style={{ alignItems: "flex-start", marginBottom: 20 }}>
          <div className="pagehead" style={{ marginBottom: 0 }}>
            <h1>{job.title}</h1>
            <p>
              {job.company_name} &middot;{" "}
              <Badge tone={job.status === "active" ? "success" : "neutral"}>
                {job.status === "active" ? "Aktif" : "Ditutup"}
              </Badge>{" "}
              &middot; dibuat {formatRelativeTime(job.created_at)}
            </p>
          </div>
          <Button variant="ghost" onClick={() => navigate(`/jobs/${jobId}/edit`)}>
            Edit Lowongan
          </Button>
        </div>

        <div className="mini-stat-row">
          <div className="mini-stat">
            <div className="mn">{totalCandidates}</div>
            <div className="ml">Total Kandidat</div>
          </div>
          <div className="mini-stat">
            <div className="mn">{invitedCount}</div>
            <div className="ml">Sudah Diundang</div>
          </div>
          <div className="mini-stat">
            <div className="mn">{interviewedCount}</div>
            <div className="ml">Selesai Wawancara</div>
          </div>
          <div className="mini-stat">
            <div className="mn">{decidedCount}</div>
            <div className="ml">Diputuskan</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
          <Button variant="primary" onClick={() => navigate(`/jobs/${jobId}`)}>
            Lihat Kandidat
          </Button>
          <Button variant="secondary" onClick={() => navigate(`/jobs/${jobId}/questions`)}>
            Kelola Pertanyaan
          </Button>
        </div>

        <div className="split3 jd-visuals">
          <div>
            <ColorPanel tone="teal" title="Tanggung Jawab">
              <BulletDisplay text={job.responsibilities} />
            </ColorPanel>
            <ColorPanel tone="success" title="Persyaratan Tambahan">
              <BulletDisplay text={job.requirements} />
            </ColorPanel>
            <ColorPanel tone="gold" title="Kualifikasi">
              <BulletDisplay text={job.qualifications} />
            </ColorPanel>
          </div>
          <div>
            <div className="card">
              <div className="row" style={{ marginBottom: 10 }}>
                <div className="serif" style={{ fontWeight: 700 }}>
                  Pertanyaan Wawancara
                </div>
                <Badge tone={questionsStatusTone}>{questionsStatusLabel}</Badge>
              </div>
              <p style={{ fontSize: "0.8rem", color: "var(--muted)", margin: "0 0 10px" }}>
                {hasQuestions
                  ? `${questions.length} pertanyaan · ${isApproved ? "siap dikirim ke kandidat" : "belum disetujui — kandidat belum bisa diundang"}`
                  : "Belum ada pertanyaan dibuat untuk lowongan ini."}
              </p>
              <Button variant="ghost" block onClick={() => navigate(`/jobs/${jobId}/questions`)}>
                {hasQuestions ? "Tinjau Pertanyaan" : "Buat Pertanyaan"}
              </Button>
            </div>
            <div className="card">
              <div className="row" style={{ marginBottom: 10 }}>
                <div className="serif" style={{ fontWeight: 700 }}>
                  Kompetensi Wajib (diekstrak AI)
                </div>
              </div>
              {competencies.length === 0 ? (
                <p style={{ fontSize: "0.8rem", color: "var(--muted)" }}>Belum ada kompetensi diekstrak.</p>
              ) : (
                <div className="chip-row">
                  {competencies.map((c) => (
                    <span className="chip" key={c.id}>
                      {c.competency_name}
                      <span className="chip-imp">{importanceDots(c.importance_level)}</span>
                    </span>
                  ))}
                </div>
              )}
              <p className="hint" style={{ marginTop: 10 }}>
                Kompetensi wajib dikunci setelah lowongan dibuat, agar analisis kesenjangan
                keahlian kandidat yang sudah dinilai tidak berubah-ubah. Ubah kompetensi hanya
                saat membuat lowongan baru.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
