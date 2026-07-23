import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { CandidateTokenGuard } from "../lib/CandidateTokenGuard";
import { CandidateHeader } from "../components/CandidateHeader";
import { Button } from "../components/Button";
import { ErrorState } from "../components/ErrorState";
import { api } from "../api/client";

const CONSENT_TEXT_VERSION = "v1";

function ConsentFlow({
  candidateId,
  candidateAlias,
  token,
}: {
  candidateId: number;
  candidateAlias: string;
  token: string;
}) {
  const navigate = useNavigate();
  const [checked, setChecked] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Round-3 follow-up #16 (2026-07-19): the old flow showed an extra "Terima kasih, siap memulai
  // wawancara?" confirmation screen requiring a SECOND click before moving on — user wants
  // consent to go straight into the camera-test step (T17-followup #15) with no intermediate
  // screen. Navigating directly here removes that redundant click.
  async function handleSubmit() {
    setSubmitting(true);
    setError(null);
    const { error: apiError } = await api.POST("/candidates/{candidate_id}/consent", {
      params: { path: { candidate_id: candidateId } },
      body: { token, consent_text_version: CONSENT_TEXT_VERSION },
    });
    setSubmitting(false);
    if (apiError) {
      setError("Gagal menyimpan persetujuan. Silakan coba lagi.");
      return;
    }
    navigate(`/candidate/${candidateId}/camera-test?token=${token}`);
  }

  return (
    <div className="main" style={{ maxWidth: 520, paddingTop: 44 }}>
      <div className="pagehead" style={{ textAlign: "center" }}>
        <h1>Selamat datang, {candidateAlias}</h1>
        <p>Anda diundang untuk mengikuti proses wawancara AI kami</p>
      </div>

      <div className="consent-box">
        Sebelum memulai wawancara, kami memerlukan persetujuan Anda untuk memproses data pribadi
        (CV, rekaman audio, dan transkrip wawancara) sesuai dengan UU Perlindungan Data Pribadi
        (PDP). Data hanya digunakan untuk proses seleksi ini dan laporan pengembangan diri Anda.
      </div>
      <label className="checkline">
        <input type="checkbox" checked={checked} onChange={(e) => setChecked(e.target.checked)} />
        <span>Saya membaca dan menyetujui pemrosesan data di atas.</span>
      </label>
      {error && <ErrorState message={error} onRetry={handleSubmit} />}
      <Button variant="primary" block disabled={!checked || submitting} onClick={handleSubmit}>
        {submitting ? "Menyimpan..." : "Lanjutkan"}
      </Button>
    </div>
  );
}

export function CandidateConsentPage() {
  return (
    <CandidateTokenGuard requireConsent={false}>
      {(candidate, token) => (
        <div>
          <CandidateHeader step="Langkah 1 dari 3" />
          <ConsentFlow candidateId={candidate.id} candidateAlias={candidate.alias} token={token} />
        </div>
      )}
    </CandidateTokenGuard>
  );
}
