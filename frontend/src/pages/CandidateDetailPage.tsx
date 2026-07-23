import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { TopBar } from "../components/TopBar";
import { Button } from "../components/Button";
import { Badge } from "../components/Badge";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { ErrorState } from "../components/ErrorState";
import { CvProfileSections, type CvProfileData } from "../components/CvProfileSections";
import { AnalysisSummaryCard, SkillGapSections } from "../components/SkillGapSections";
import { InviteModal } from "../components/InviteModal";
import { Modal } from "../components/Modal";
import { api } from "../api/client";

type SkillGap = {
  gap_summary: string;
  missing_competencies: string[];
  matched_competencies: string[];
  development_priority: string | null;
  key_strengths: { title: string; description: string }[];
  resume_action_items: { original: string; improved: string }[];
  interview_key_strengths: { title: string; description: string }[];
  interview_feedback: { title: string; description: string }[];
};
type CandidateDetail = CvProfileData & {
  candidate_id: number;
  alias: string;
  job_id: number;
  job_title: string;
  match_score: number | null;
  skill_gap: SkillGap | null;
  decision: { decision: string; notes: string | null } | null;
  report_sent: boolean;
  cv_url: string | null;
  contact_email: string | null;
  has_email: boolean;
  meets_education: boolean | null;
  invited: boolean;
  invite_email_sent: boolean;
  answers: unknown[];
};

type PipelineKey = "belum_diundang" | "menunggu_wawancara" | "menunggu_keputusan" | "advance" | "reject";

// Round 13 follow-up (real bug, user-reported): mirrors the same 4-stage pipeline shown on
// Kandidat/Laporan (statusFor()/keputusanFor()) instead of the old binary "no decision yet" /
// "Lanjutkan" badge — the old badge only ever showed nothing or "Lanjutkan", so there was no way
// to see "Menunggu Wawancara" vs "Menunggu Keputusan HR" from this page at all.
//
// Round 14 follow-up (real bug, user-reported, TWICE — first fix used `invited && has_email`,
// which was still wrong): `invited_at` is set the moment HR opens the invite modal (token
// generation), and `contact_email` can be added/edited at any later point via the "Simpan" button
// with no send action happening — neither is proof a real invite email went out. The ONLY real
// signal is `invite_email_sent` (backend: candidates.invite_email_sent_at, set exclusively by
// routers/candidates.py::send_candidate_invite_email after a real send succeeds). "Menunggu
// Wawancara" is gated on that now, not invited/has_email.
function pipelineStatusFor(d: CandidateDetail): { key: PipelineKey; label: string; tone: "neutral" | "warning" | "info" | "success" | "danger" } {
  if (d.decision?.decision === "advance") return { key: "advance", label: "Dilanjutkan", tone: "success" };
  if (d.decision?.decision === "reject") return { key: "reject", label: "Ditolak", tone: "danger" };
  if (d.answers.length > 0) return { key: "menunggu_keputusan", label: "Menunggu Keputusan HR", tone: "warning" };
  if (d.invite_email_sent) return { key: "menunggu_wawancara", label: "Menunggu Wawancara", tone: "neutral" };
  return { key: "belum_diundang", label: "Belum Diundang", tone: "neutral" };
}

type State =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; detail: CandidateDetail };

function fitLabel(score: number): string {
  const pct = score * 100;
  if (pct >= 75) return "Sangat Cocok";
  if (pct >= 50) return "Cocok";
  return "Kurang Cocok";
}

export function CandidateDetailPage() {
  const { jobId, candidateId } = useParams();
  const navigate = useNavigate();
  const [state, setState] = useState<State>({ status: "loading" });
  const [decisionBusy, setDecisionBusy] = useState(false);
  const [decisionError, setDecisionError] = useState<string | null>(null);
  const [inviteModalOpen, setInviteModalOpen] = useState(false);
  const [emailDraft, setEmailDraft] = useState("");
  const [emailBusy, setEmailBusy] = useState(false);
  const [emailError, setEmailError] = useState<string | null>(null);
  const [emptyEmailAlert, setEmptyEmailAlert] = useState(false);

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

  useEffect(() => {
    if (state.status === "ready") {
      setEmailDraft(state.detail.contact_email ?? "");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.status === "ready" ? state.detail.contact_email : null]);

  async function handleSaveEmail() {
    if (!emailDraft.trim()) {
      setEmptyEmailAlert(true);
      return;
    }
    setEmailBusy(true);
    setEmailError(null);
    const { error } = await api.PATCH("/candidates/{candidate_id}/contact-email", {
      params: { path: { candidate_id: Number(candidateId) } },
      body: { contact_email: emailDraft },
    });
    setEmailBusy(false);
    if (error) {
      setEmailError("Gagal menyimpan email.");
      return;
    }
    load();
  }

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

  if (state.status === "loading") {
    return (
      <div>
        <TopBar active="kandidat" jobId={Number(jobId)} />
        <div className="main">
          <SpinnerWithLabel label="Memuat detail kandidat..." />
        </div>
      </div>
    );
  }
  if (state.status === "error") {
    return (
      <div>
        <TopBar active="kandidat" jobId={Number(jobId)} />
        <div className="main">
          <ErrorState message="Gagal memuat detail kandidat." onRetry={load} />
        </div>
      </div>
    );
  }

  const d = state.detail;
  const status = pipelineStatusFor(d);

  return (
    <div>
      <TopBar active="kandidat" jobId={Number(jobId)} />
      <div className="main wide">
        <div className="pagehead" style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}>
          <div>
            <h1>{d.alias}</h1>
            <p>
              {d.job_title}
              {d.match_score !== null && (
                <>
                  {" "}
                  &middot; Skor Kecocokan {Math.round(d.match_score * 100)} &middot; {fitLabel(d.match_score)}
                </>
              )}
            </p>
          </div>
          <Button variant="ghost" onClick={() => navigate(`/jobs/${d.job_id}`)}>
            Kembali ke Kandidat
          </Button>
        </div>

        <div className="card">
          <div
            className="section-bar-header tone-info"
            style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}
          >
            <span>Keputusan</span>
            <Badge tone={status.tone}>{status.label}</Badge>
          </div>

          {/* Round 13 follow-up (real bug, user-reported): a candidate not yet invited to
              interview used to require an explicit "Lanjutkan Kandidat" click — a final-sounding
              decision made purely from the CV, before any interview exists — before the invite
              button even appeared. Inviting to interview IS the forward action pre-interview;
              there's no separate "advance" decision to make until after the interview happens.
              Round 14 follow-up (real bug, user-reported, TWICE): "Lihat CV" always shows if
              cv_url exists, regardless of pipeline stage. "Tolak Kandidat" is available at ANY
              point before a final decision — it must NOT disappear just because an invite email
              got sent or the interview happened; HR can still reject at any of those points.
              "Kirim Undangan Wawancara" only makes sense before the email has actually been sent
              (gated on invite_email_sent specifically, not on pipeline stage as a whole). */}
          <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: 10 }}>
            {d.cv_url && (
              <Button
                variant="success"
                onClick={() => navigate(`/jobs/${d.job_id}/candidates/${candidateId}/cv`)}
              >
                Lihat CV
              </Button>
            )}
            {!d.decision && !d.invite_email_sent && (
              <Button variant="secondary" onClick={() => setInviteModalOpen(true)}>
                Kirim Undangan Wawancara
              </Button>
            )}
            {!d.decision && (
              <Button variant="danger" disabled={decisionBusy} onClick={() => handleDecision("reject")}>
                Tolak Kandidat
              </Button>
            )}
          </div>
          {decisionError && <ErrorState message={decisionError} onRetry={() => handleDecision("reject")} />}
          {/* Round-3 follow-up #11 (2026-07-19): "Kirim Laporan via Email" moved OUT of this card
              — the development report should only be sent once CV analysis AND interview results
              both exist. Sending now lives on the Laporan page itself (ReportPage.tsx), reached
              via "Lihat Laporan"; this card's job is only the pre-interview invite/reject gate. */}

          <hr className="divider" />
          <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: 8 }}>
            <strong style={{ fontSize: "0.82rem", whiteSpace: "nowrap" }}>Email kandidat:</strong>
            <input
              value={emailDraft}
              onChange={(e) => setEmailDraft(e.target.value)}
              placeholder="belum ada email terdeteksi"
              style={{ minWidth: 180 }}
            />
            <Button variant="ghost" disabled={emailBusy} onClick={handleSaveEmail}>
              {emailBusy ? "Menyimpan..." : "Simpan"}
            </Button>
          </div>
          {emailError && <ErrorState message={emailError} onRetry={handleSaveEmail} />}
          {d.decision && !d.has_email && (
            <p className="hint" style={{ marginTop: 8 }}>
              Kandidat belum memiliki email — isi email di atas untuk mengirim undangan wawancara
              atau laporan.
            </p>
          )}
        </div>

        {(d.education_level || d.major) && d.meets_education !== null && (
          <p className="hint" style={{ margin: "0 0 14px" }}>
            Pendidikan: {d.education_level ?? "-"}
            {d.major ? ` — ${d.major}` : ""}
            <span style={{ marginLeft: 8 }}>
              <Badge tone={d.meets_education ? "success" : "warning"}>
                {d.meets_education ? "Memenuhi syarat" : "Belum memenuhi syarat"}
              </Badge>
            </span>
          </p>
        )}

        <CvProfileSections
          data={d}
          analysisSummary={d.skill_gap && <AnalysisSummaryCard gapSummary={d.skill_gap.gap_summary} />}
        />

        {d.skill_gap && <SkillGapSections data={d.skill_gap} />}
      </div>

      {inviteModalOpen && (
        <InviteModal
          candidateId={Number(candidateId)}
          candidateAlias={d.alias}
          alreadyInvited={d.invited}
          onClose={() => setInviteModalOpen(false)}
          onInvited={load}
        />
      )}

      {/* Round 14 follow-up (user-reported): clicking "Simpan" with an empty email field used to
          silently PATCH an empty string with no feedback at all. */}
      {emptyEmailAlert && (
        <Modal title="Email Tidak Boleh Kosong" onClose={() => setEmptyEmailAlert(false)}>
          <p style={{ fontSize: "0.86rem", color: "var(--ink-2)", lineHeight: 1.6 }}>
            Isi alamat email kandidat terlebih dahulu sebelum menyimpan.
          </p>
          <div className="modal-actions">
            <Button variant="primary" onClick={() => setEmptyEmailAlert(false)}>
              Tutup
            </Button>
          </div>
        </Modal>
      )}
    </div>
  );
}
