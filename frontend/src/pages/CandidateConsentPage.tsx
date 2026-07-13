import { CandidateTokenGuard } from "../lib/CandidateTokenGuard";
import { Card } from "../components/Card";

export function CandidateConsentPage() {
  return (
    <CandidateTokenGuard requireConsent={false}>
      {(candidate, token) => (
        <div style={{ maxWidth: 480, margin: "80px auto", padding: "0 16px" }}>
          <Card>
            <h1>Persetujuan</h1>
            <p>
              Lowongan: <strong>{candidate.job_title}</strong>
            </p>
            <p>(T8 akan mengisi checkbox persetujuan + tautan Telegram di sini.)</p>
            <p style={{ fontSize: 12, opacity: 0.6 }}>token: {token}</p>
          </Card>
        </div>
      )}
    </CandidateTokenGuard>
  );
}
