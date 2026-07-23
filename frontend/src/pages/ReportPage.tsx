import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { TopBar } from "../components/TopBar";
import { Button } from "../components/Button";
import { Badge } from "../components/Badge";
import { Modal } from "../components/Modal";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { ErrorState } from "../components/ErrorState";
import { api } from "../api/client";
import { VideoPlayer } from "../components/VideoPlayer";
import { CvProfileSections, type CvProfileData } from "../components/CvProfileSections";
import { AnalysisSummaryCard, InterviewRecommendationSections, SkillGapSections } from "../components/SkillGapSections";
import { RUBRIC_LABELS, RubricDots } from "../components/RubricDots";
import "./ReportPage.css";

type UpskillingItem = { title: string; description: string };
type UpskillingTiers = { low_effort: UpskillingItem[]; medium_effort: UpskillingItem[]; high_effort: UpskillingItem[] };
type UpskillingSection = {
  kompetensi_belum_terpenuhi: Record<string, UpskillingTiers>;
  area_pengembangan_wawancara: Record<string, UpskillingTiers>;
};
type RubricScore = { criterion_name: string; score: number; rationale: string };
type InterviewAnswer = {
  question_text: string;
  summary_text: string | null;
  transcript_text: string | null;
  video_url: string;
  rubric_scores: RubricScore[];
};
type Report = CvProfileData & {
  candidate_alias: string;
  job_title: string;
  decision: string | null;
  gap_summary: string;
  development_priority: string | null;
  matched_competencies: string[];
  missing_competencies: string[];
  key_strengths: { title: string; description: string }[];
  resume_action_items: { original: string; improved: string }[];
  interview_key_strengths: { title: string; description: string }[];
  interview_feedback: { title: string; description: string }[];
  upskilling_plan: UpskillingSection;
  interview_overall_score: number | null;
  interview_answers: InterviewAnswer[];
};

type State = { status: "loading" } | { status: "error"; message: string } | { status: "ready"; report: Report };

const TIER_LABELS: Record<string, string> = {
  low_effort: "Effort Rendah (Jam/Hari)",
  medium_effort: "Effort Sedang (Minggu)",
  high_effort: "Effort Tinggi (Bulan)",
};
const TIER_ORDER: (keyof UpskillingTiers)[] = ["low_effort", "medium_effort", "high_effort"];

// Round 9 follow-up (2026-07-21, user-provided mockup): "Estimasi Waktu Upskilling" grouped by
// competency/area first (one distinct scrollable box per skill), tiers nested inside each box —
// replaces the earlier tier-first layout where the same skill name repeated across every tier's
// card. Colors adapted to this app's existing info/danger tokens rather than the mockup's literal
// blue gradient, to stay consistent with the rest of the report page's palette.
function UpskillingSkillGrid({
  section,
  tone,
}: {
  section: Record<string, UpskillingTiers>;
  tone: "info" | "danger";
}) {
  return (
    <div className="upskilling-grid">
      {Object.entries(section).map(([name, tiers]) => (
        <div className="upskilling-skill-card" key={name}>
          <div className={`upskilling-skill-badge tone-${tone}`}>{name}</div>
          <div className={`upskilling-skill-body tone-${tone}`}>
            {TIER_ORDER.filter((tier) => tiers[tier]?.length).map((tier) => (
              <div className="upskilling-tier-group" key={tier}>
                <div className={`upskilling-tier-label tone-${tone} tier-${tier}`}>{TIER_LABELS[tier]}</div>
                <div className="upskilling-tier-items">
                  {tiers[tier].map((item, i) => (
                    <div className="upskilling-item-card" key={i}>
                      <strong>{item.title}</strong>
                      <p>{item.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export function ReportPage() {
  const { jobId, candidateId } = useParams();
  const navigate = useNavigate();
  const [state, setState] = useState<State>({ status: "loading" });
  // 2026-07-22 (user-requested): "Ambil Keputusan" replaces the old standalone "Kirim Laporan via
  // Email" button (moved off ReportPdfPage.tsx) — a two-step flow (choose Lanjutkan/Tolak/Batal,
  // then confirm) that records the decision AND sends the combined decision+report email in one
  // action, right from the report itself instead of a separate page.
  const [choiceModalOpen, setChoiceModalOpen] = useState(false);
  const [pendingDecision, setPendingDecision] = useState<"advance" | "reject" | null>(null);
  const [decisionBusy, setDecisionBusy] = useState(false);
  const [decisionError, setDecisionError] = useState<string | null>(null);

  function load() {
    setState({ status: "loading" });
    api
      .GET("/candidates/{candidate_id}/report", { params: { path: { candidate_id: Number(candidateId) } } })
      .then(({ data, error }) => {
        if (error || !data) {
          setState({
            status: "error",
            message: (error as { detail?: string } | undefined)?.detail ?? "Gagal memuat laporan.",
          });
          return;
        }
        setState({ status: "ready", report: data as Report });
      });
  }

  useEffect(load, [candidateId]);

  function chooseDecision(decision: "advance" | "reject") {
    setPendingDecision(decision);
    setChoiceModalOpen(false);
  }

  async function handleConfirmDecision() {
    if (!pendingDecision) return;
    setDecisionBusy(true);
    setDecisionError(null);

    const { error: decisionErr } = await api.POST("/decisions", {
      body: { candidate_id: Number(candidateId), decision: pendingDecision },
    });
    if (decisionErr) {
      setDecisionBusy(false);
      setDecisionError("Gagal menyimpan keputusan.");
      return;
    }

    const { error: sendErr } = await api.POST("/candidates/{candidate_id}/send-report", {
      params: { path: { candidate_id: Number(candidateId) } },
    });
    setDecisionBusy(false);
    if (sendErr) {
      setDecisionError(
        (sendErr as { detail?: string })?.detail ?? "Keputusan tersimpan, tetapi gagal mengirim email ke kandidat."
      );
      return;
    }

    setPendingDecision(null);
    load();
  }

  if (state.status === "loading") {
    return (
      <div>
        <TopBar active="laporan" jobId={Number(jobId)} />
        <div className="main">
          <SpinnerWithLabel label="Memuat laporan..." />
        </div>
      </div>
    );
  }

  if (state.status === "error") {
    return (
      <div>
        <TopBar active="laporan" jobId={Number(jobId)} />
        <div className="main">
          <ErrorState message={state.message} onRetry={load} />
        </div>
      </div>
    );
  }

  const r = state.report;

  return (
    <div>
      <TopBar active="laporan" jobId={Number(jobId)} />
      <div className="main wide report-page">
        <div className="pagehead">
          <h1 style={{ textTransform: "uppercase" }}>
            Laporan Feedback CV dan Wawancara &middot; {r.candidate_alias}
          </h1>
          <p style={{ textTransform: "uppercase" }}>{r.job_title}</p>
          <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
            <Button
              variant="secondary"
              onClick={() => navigate(`/jobs/${jobId}/candidates/${candidateId}/report/pdf`)}
            >
              Lihat Laporan
            </Button>
            <Button variant="ghost" onClick={() => navigate(`/jobs/${jobId}/reports`)}>
              Kembali ke Daftar Laporan
            </Button>
            {r.decision === null && (
              <Button variant="primary" onClick={() => setChoiceModalOpen(true)}>
                Ambil Keputusan
              </Button>
            )}
            {r.decision === "advance" && <Badge tone="success">Dilanjutkan</Badge>}
            {r.decision === "reject" && <Badge tone="danger">Ditolak</Badge>}
          </div>
        </div>

        <CvProfileSections
          data={r}
          showCvDetails={false}
          showSkillsTitle={false}
          analysisSummary={<AnalysisSummaryCard gapSummary={r.gap_summary} title="Ringkasan Analisis Keahlian" />}
        />

        <SkillGapSections
          data={{
            gap_summary: r.gap_summary,
            matched_competencies: r.matched_competencies,
            missing_competencies: r.missing_competencies,
            key_strengths: r.key_strengths,
            resume_action_items: r.resume_action_items,
          }}
        />

        {r.resume_action_items.length > 0 && (
          <div className="card profile-section">
            <div className="section-bar-header tone-gold">Saran Perbaikan CV (ATS)</div>
            <div className="ats-table-wrap">
              <table className="ats-table">
                <thead>
                  <tr>
                    <th>Kalimat Asli di CV</th>
                    <th>Saran Perbaikan Kalimat</th>
                  </tr>
                </thead>
                <tbody>
                  {r.resume_action_items.map((item, i) => (
                    <tr key={i}>
                      <td>{item.original}</td>
                      <td>{item.improved}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {r.interview_answers.length > 0 && (
          <div className="card">
            <div className="section-bar-header tone-info">Wawancara</div>
            <div className="report-interview-scroll" style={{ display: "flex", flexDirection: "column", gap: 32 }}>
              {r.interview_answers.map((a, i) => (
                <div key={i}>
                  <div className="report-question-box">
                    <div className="report-question-label">Pertanyaan {i + 1}</div>
                    <div className="report-question-text">{a.question_text}</div>
                  </div>
                  <VideoPlayer url={a.video_url} frameClassName="report-video-frame" />
                  {a.rubric_scores.length > 0 && (
                    <div className="rubric-table-wrap" style={{ marginTop: 10 }}>
                      <table className="rubric-table">
                        <thead>
                          <tr>
                            <th>Aspek</th>
                            <th>Deskripsi</th>
                            <th>Skor</th>
                          </tr>
                        </thead>
                        <tbody>
                          {a.rubric_scores.map((r) => (
                            <tr key={r.criterion_name}>
                              <td>{RUBRIC_LABELS[r.criterion_name] ?? r.criterion_name}</td>
                              <td>{r.rationale}</td>
                              <td>
                                <RubricDots score={r.score} />
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                  {(a.transcript_text || a.summary_text) && (
                    <div className="answer-summary-table-wrap" style={{ marginTop: 10 }}>
                      <table className="answer-summary-table">
                        <tbody>
                          {a.transcript_text && (
                            <tr>
                              <td className="answer-summary-label">Transkrip Asli</td>
                              <td>{a.transcript_text}</td>
                            </tr>
                          )}
                          {a.summary_text && (
                            <tr>
                              <td className="answer-summary-label">Ringkasan AI</td>
                              <td>{a.summary_text}</td>
                            </tr>
                          )}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        <InterviewRecommendationSections
          interviewKeyStrengths={r.interview_key_strengths}
          interviewFeedback={r.interview_feedback}
        />

        {Object.keys(r.upskilling_plan.kompetensi_belum_terpenuhi).length === 0 &&
        Object.keys(r.upskilling_plan.area_pengembangan_wawancara).length === 0 ? (
          <div className="card">
            <div className="serif" style={{ fontWeight: 700, marginBottom: 10 }}>
              Estimasi Waktu Upskilling
            </div>
            <p className="hint">Tidak ada rencana upskilling — tidak ada kesenjangan kompetensi.</p>
          </div>
        ) : (
          <>
            {Object.keys(r.upskilling_plan.kompetensi_belum_terpenuhi).length > 0 && (
              <div className="card profile-section">
                <div className="section-bar-header tone-danger">
                  Estimasi Waktu Upskilling &middot; Kompetensi Belum Terpenuhi
                </div>
                <UpskillingSkillGrid section={r.upskilling_plan.kompetensi_belum_terpenuhi} tone="danger" />
              </div>
            )}

            {Object.keys(r.upskilling_plan.area_pengembangan_wawancara).length > 0 && (
              <div className="card profile-section">
                <div className="section-bar-header tone-danger">
                  Estimasi Waktu Upskilling &middot; Area Pengembangan Wawancara
                </div>
                <UpskillingSkillGrid section={r.upskilling_plan.area_pengembangan_wawancara} tone="danger" />
              </div>
            )}
          </>
        )}
      </div>

      {choiceModalOpen && (
        <Modal title="Ambil Keputusan" onClose={() => setChoiceModalOpen(false)}>
          <p style={{ fontSize: "0.86rem", color: "var(--ink-2)", lineHeight: 1.6 }}>
            Pilih keputusan untuk {r.candidate_alias}. Keputusan dan laporan pengembangan akan
            dikirim ke kandidat via email.
          </p>
          <div className="modal-actions">
            <Button variant="ghost" onClick={() => setChoiceModalOpen(false)}>
              Batal
            </Button>
            <Button variant="danger" onClick={() => chooseDecision("reject")}>
              Tolak
            </Button>
            <Button variant="success" onClick={() => chooseDecision("advance")}>
              Lanjutkan
            </Button>
          </div>
        </Modal>
      )}

      {pendingDecision && (
        <Modal
          title="Apakah Anda Yakin?"
          onClose={() => (!decisionBusy ? setPendingDecision(null) : undefined)}
          dismissOnBackdropClick={!decisionBusy}
        >
          <p style={{ fontSize: "0.86rem", color: "var(--ink-2)", lineHeight: 1.6 }}>
            Kandidat akan ditandai sebagai{" "}
            <strong>{pendingDecision === "advance" ? "Dilanjutkan" : "Ditolak"}</strong>, dan
            keputusan ini beserta laporan pengembangan akan langsung dikirim ke kandidat via email.
            Tindakan ini tidak dapat dibatalkan.
          </p>
          {decisionError && <ErrorState message={decisionError} onRetry={handleConfirmDecision} />}
          <div className="modal-actions">
            <Button variant="ghost" disabled={decisionBusy} onClick={() => setPendingDecision(null)}>
              Batal
            </Button>
            <Button variant="primary" disabled={decisionBusy} onClick={handleConfirmDecision}>
              {decisionBusy ? "Mengirim..." : "Kirim Keputusan dan Laporan"}
            </Button>
          </div>
        </Modal>
      )}
    </div>
  );
}
