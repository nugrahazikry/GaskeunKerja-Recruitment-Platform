import { CandidateTokenGuard } from "../lib/CandidateTokenGuard";
import { Card } from "../components/Card";

export function CandidateInterviewPage() {
  return (
    <CandidateTokenGuard requireConsent={true}>
      {(candidate) =>
        candidate.interview_completed ? (
          <div style={{ maxWidth: 480, margin: "80px auto", padding: "0 16px" }}>
            <Card>
              <h1>Wawancara sudah selesai, terima kasih</h1>
            </Card>
          </div>
        ) : (
          <div style={{ maxWidth: 480, margin: "80px auto", padding: "0 16px" }}>
            <Card>
              <h1>Wawancara — {candidate.job_title}</h1>
              <p>(T6 akan mengisi perekam audio 8-state di sini.)</p>
            </Card>
          </div>
        )
      }
    </CandidateTokenGuard>
  );
}
