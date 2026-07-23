import { GapPanel } from "./GapPanel";
import "./ProfileSections.css";

export type KeyStrength = { title: string; description: string };
export type ResumeActionItem = { original: string; improved: string };

export type SkillGapSectionsData = {
  gap_summary: string;
  matched_competencies: string[];
  missing_competencies: string[];
  key_strengths: KeyStrength[];
  // Round-3 follow-up #6 (2026-07-19): "Saran Perbaikan CV (ATS)" removed from display per user
  // request — deferred to be built alongside the (also-deferred) upskilling-plan feature rather
  // than shown now. resume_action_items is still computed/persisted by the backend (see
  // skillgap.py::generate_recommendation_extras); this component just doesn't render it.
  resume_action_items: ResumeActionItem[];
};

// Rendered separately from (and positioned before, inside CvProfileSections's "Ringkasan
// Keahlian" block) the rest of SkillGapSections below — see CvProfileSections's
// `analysisSummary` prop. Title bar uses the same GapPanel-style colored-bar header as Keahlian
// Eksplisit/Sesuai Kebutuhan (on both CandidateDetailPage and the laporan page).
export function AnalysisSummaryCard({
  gapSummary,
  title = "Ringkasan Analisis",
}: {
  gapSummary: string;
  title?: string;
}) {
  return (
    <div className="card profile-section">
      <div className="section-bar-header tone-info">{title}</div>
      <p style={{ fontSize: "0.86rem", color: "var(--ink-2)", lineHeight: 1.7 }}>{gapSummary}</p>
    </div>
  );
}

// Adapted from the Tahap 2 "SkillGap AI" prototype's Agent 4 (Recommendation Report) template —
// Summary Analysis + Market Aligned/High Demand chip grids + Key Strengths — restyled with this
// app's own palette. "Estimasi Waktu Upskilling" is intentionally NOT part of this shared
// component; laporan (ReportPage) renders its own separate section for that. Ringkasan Analisis
// itself is rendered by the caller via AnalysisSummaryCard, positioned inside CvProfileSections.
export function SkillGapSections({ data }: { data: SkillGapSectionsData }) {
  return (
    <>
      <div className="profile-grid-2">
        <GapPanel
          header="Sesuai Kebutuhan"
          items={data.matched_competencies}
          emptyLabel="Belum ada kompetensi yang sesuai."
          tone="success"
        />
        <GapPanel
          header="Kompetensi Belum Terpenuhi"
          items={data.missing_competencies}
          emptyLabel="Tidak ada kesenjangan kompetensi."
          tone="warning"
        />
      </div>

      {data.key_strengths.length > 0 && (
        <div className="card profile-section">
          <div className="section-bar-header tone-gold">Kekuatan Utama</div>
          <div className="profile-list profile-scroll-3">
            {data.key_strengths.map((s, i) => (
              <div className="profile-list-item" key={i}>
                <strong>{s.title}</strong>
                <p style={{ fontSize: "0.82rem" }}>{s.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

    </>
  );
}

// Round 8 follow-up (2026-07-21, user decision): pulled out of SkillGapSections and rendered as
// its own component so ReportPage.tsx can position it AFTER the Wawancara section instead of
// alongside the CV-based Kekuatan Utama — these two are computed from interview performance (see
// skillgap.py::generate_interview_recommendation), not the CV, so they only make sense once the
// interview content above them has already been shown. Side-by-side layout (profile-grid-2),
// matching the Sesuai Kebutuhan/Kompetensi Belum Terpenuhi two-column pattern above.
export function InterviewRecommendationSections({
  interviewKeyStrengths,
  interviewFeedback,
}: {
  interviewKeyStrengths: KeyStrength[];
  interviewFeedback: KeyStrength[];
}) {
  if (interviewKeyStrengths.length === 0 && interviewFeedback.length === 0) return null;

  return (
    <div className="profile-grid-2">
      {interviewKeyStrengths.length > 0 && (
        <div className="card profile-section">
          <div className="section-bar-header tone-info">Kekuatan Utama Wawancara</div>
          <div className="profile-list profile-scroll-3">
            {interviewKeyStrengths.map((s, i) => (
              <div className="profile-list-item" key={i}>
                <strong>{s.title}</strong>
                <p style={{ fontSize: "0.82rem" }}>{s.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {interviewFeedback.length > 0 && (
        <div className="card profile-section">
          <div className="section-bar-header tone-danger">Feedback Wawancara</div>
          <div className="profile-list profile-scroll-3">
            {interviewFeedback.map((s, i) => (
              <div className="profile-list-item" key={i}>
                <strong>{s.title}</strong>
                <p style={{ fontSize: "0.82rem" }}>{s.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
