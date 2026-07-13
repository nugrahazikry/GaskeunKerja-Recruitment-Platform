import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Card } from "../components/Card";
import { Button } from "../components/Button";
import { Badge } from "../components/Badge";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { ErrorState } from "../components/ErrorState";
import { AudioPlayer } from "../components/AudioPlayer";
import { api } from "../api/client";

type RubricScore = { criterion_name: string; score: number; rationale: string };
type AnswerDetail = {
  answer_id: number;
  question_text: string;
  audio_url: string;
  transcript_text: string;
  rubric_scores: RubricScore[];
};
type SkillGap = {
  gap_summary: string;
  missing_competencies: string[];
  development_priority: string | null;
};
type CandidateDetail = {
  candidate_id: number;
  alias: string;
  job_id: number;
  job_title: string;
  skills: string[];
  experience: { role: string; company: string; summary: string; duration: string }[];
  qualifications: string[];
  skill_gap: SkillGap | null;
  answers: AnswerDetail[];
  interview_summary_text: string | null;
  interview_overall_score: number | null;
  decision: { decision: string; notes: string | null } | null;
  has_telegram_link: boolean;
  report_sent: boolean;
};

type State =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; detail: CandidateDetail };

export function CandidateDetailPage() {
  const { candidateId } = useParams();
  const [state, setState] = useState<State>({ status: "loading" });
  const [decisionBusy, setDecisionBusy] = useState(false);
  const [decisionError, setDecisionError] = useState<string | null>(null);
  const [sendBusy, setSendBusy] = useState(false);
  const [sendError, setSendError] = useState<string | null>(null);
  const [sendSuccess, setSendSuccess] = useState(false);

  function load() {
    setState({ status: "loading" });
    api
      .GET("/candidates/{candidate_id}/detail", { params: { path: { candidate_id: Number(candidateId) } } })
      .then(({ data, error }) => {
        if (error || !data) {
          setState({ status: "error" });
          return;
        }
        setState({ status: "ready", detail: data as CandidateDetail });
      });
  }

  useEffect(load, [candidateId]);

  async function handleDecision(decision: "advance" | "reject") {
    setDecisionBusy(true);
    setDecisionError(null);
    const { error } = await api.POST("/decisions", {
      body: { candidate_id: Number(candidateId), decision },
    });
    setDecisionBusy(false);
    if (error) {
      setDecisionError("Gagal menyimpan keputusan.");
      return;
    }
    load();
  }

  async function handleSendReport() {
    setSendBusy(true);
    setSendError(null);
    setSendSuccess(false);
    const { error } = await api.POST("/candidates/{candidate_id}/send-report", {
      params: { path: { candidate_id: Number(candidateId) } },
    });
    setSendBusy(false);
    if (error) {
      setSendError((error as { detail?: string })?.detail ?? "Gagal mengirim laporan.");
      return;
    }
    setSendSuccess(true);
    load();
  }

  if (state.status === "loading") return <SpinnerWithLabel label="Memuat detail kandidat..." />;
  if (state.status === "error") return <ErrorState message="Gagal memuat detail kandidat." onRetry={load} />;

  const d = state.detail;

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", padding: "0 16px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <h1>{d.alias}</h1>
        <Link to={`/jobs/${d.job_id}`}>
          <Button variant="secondary">Kembali ke Kandidat</Button>
        </Link>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        <Card>
          <h2>Profil CV</h2>
          <p>
            <strong>Keahlian:</strong> {d.skills.join(", ") || "-"}
          </p>
          {d.experience.map((exp, i) => (
            <div key={i} style={{ marginTop: 8 }}>
              <strong>
                {exp.role} — {exp.company}
              </strong>
              <p style={{ margin: "2px 0", fontSize: 13, opacity: 0.7 }}>{exp.duration}</p>
              <p style={{ margin: "2px 0" }}>{exp.summary}</p>
            </div>
          ))}
          {d.qualifications.length > 0 && (
            <p style={{ marginTop: 8 }}>
              <strong>Kualifikasi:</strong> {d.qualifications.join("; ")}
            </p>
          )}
        </Card>

        {d.skill_gap && (
          <Card>
            <h2>Analisis Kesenjangan Keahlian</h2>
            <p>{d.skill_gap.gap_summary}</p>
            {d.skill_gap.missing_competencies.length > 0 && (
              <p>
                <strong>Kompetensi yang kurang:</strong>{" "}
                <span style={{ display: "inline-flex", gap: 6, flexWrap: "wrap" }}>
                  {d.skill_gap.missing_competencies.map((c) => (
                    <Badge key={c} tone="warning">
                      {c}
                    </Badge>
                  ))}
                </span>
              </p>
            )}
          </Card>
        )}

        {d.answers.map((a) => (
          <Card key={a.answer_id}>
            <h2>{a.question_text}</h2>
            <AudioPlayer url={a.audio_url} />
            <p style={{ marginTop: 8 }}>
              <strong>Transkrip:</strong> {a.transcript_text}
            </p>
            <div style={{ display: "flex", gap: 8, marginTop: 8, flexWrap: "wrap" }}>
              {a.rubric_scores.map((r) => (
                <Badge key={r.criterion_name} tone="info">
                  {r.criterion_name}: {r.score}/5
                </Badge>
              ))}
            </div>
          </Card>
        ))}

        {d.interview_summary_text && (
          <Card>
            <h2>Ringkasan Wawancara (AI)</h2>
            <p>{d.interview_summary_text}</p>
            {d.interview_overall_score !== null && (
              <p>
                <strong>Skor keseluruhan:</strong> {d.interview_overall_score.toFixed(1)}/5
              </p>
            )}
            <p style={{ fontSize: 13, opacity: 0.6 }}>Catatan: AI hanya memberi rekomendasi, keputusan akhir ada di tangan HR.</p>
          </Card>
        )}

        <Card>
          <h2>Keputusan HR</h2>
          {d.decision ? (
            <Badge tone={d.decision.decision === "advance" ? "success" : "danger"}>
              {d.decision.decision === "advance" ? "Lanjutkan" : "Tolak"}
            </Badge>
          ) : (
            <div style={{ display: "flex", gap: 12 }}>
              <Button variant="primary" disabled={decisionBusy} onClick={() => handleDecision("advance")}>
                Lanjutkan
              </Button>
              <Button variant="danger" disabled={decisionBusy} onClick={() => handleDecision("reject")}>
                Tolak
              </Button>
            </div>
          )}
          {decisionError && <ErrorState message={decisionError} onRetry={() => handleDecision("advance")} />}
        </Card>

        {d.decision && (
          <Card>
            <h2>Kirim Laporan</h2>
            {d.report_sent && !sendSuccess && (
              <Button variant="secondary" disabled>
                Terkirim
              </Button>
            )}
            {!d.report_sent && !d.has_telegram_link && (
              <Button variant="secondary" disabled>
                Kandidat belum menautkan Telegram
              </Button>
            )}
            {!d.report_sent && d.has_telegram_link && (
              <Button variant="primary" disabled={sendBusy} onClick={handleSendReport}>
                {sendBusy ? "Mengirim..." : "Kirim Laporan"}
              </Button>
            )}
            {sendSuccess && <p style={{ color: "var(--color-success)" }}>Laporan berhasil dikirim.</p>}
            {sendError && <ErrorState message={sendError} onRetry={handleSendReport} />}
          </Card>
        )}
      </div>
    </div>
  );
}
