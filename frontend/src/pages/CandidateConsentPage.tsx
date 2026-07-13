import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { CandidateTokenGuard } from "../lib/CandidateTokenGuard";
import { Card } from "../components/Card";
import { Button } from "../components/Button";
import { ErrorState } from "../components/ErrorState";
import { api } from "../api/client";

const CONSENT_TEXT_VERSION = "v1";
const BOT_USERNAME = import.meta.env.VITE_TELEGRAM_BOT_USERNAME as string;

function ConsentFlow({
  candidateId,
  token,
  hasTelegramLink,
}: {
  candidateId: number;
  token: string;
  hasTelegramLink: boolean;
}) {
  const navigate = useNavigate();
  const [checked, setChecked] = useState(false);
  const [consentGiven, setConsentGiven] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [telegramLinked, setTelegramLinked] = useState(hasTelegramLink);
  const [checkingStatus, setCheckingStatus] = useState(false);
  const [notYetLinkedMessage, setNotYetLinkedMessage] = useState(false);

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
    setConsentGiven(true);
  }

  async function handleCheckStatus() {
    setCheckingStatus(true);
    setNotYetLinkedMessage(false);
    const { data } = await api.GET("/candidates/{candidate_id}/self", {
      params: { path: { candidate_id: candidateId }, query: { token } },
    });
    setCheckingStatus(false);
    if (data?.has_telegram_link) {
      setTelegramLinked(true);
    } else {
      setNotYetLinkedMessage(true);
    }
  }

  const showTelegramStep = consentGiven || telegramLinked;

  return (
    <Card>
      <h1>Persetujuan Data</h1>
      <p>
        Sebelum memulai wawancara, kami memerlukan persetujuan Anda untuk memproses data pribadi
        (CV, rekaman audio, dan transkrip wawancara) sesuai dengan UU Perlindungan Data Pribadi
        (PDP). Data Anda hanya akan digunakan untuk proses rekrutmen ini.
      </p>

      {!showTelegramStep && (
        <>
          <label style={{ display: "flex", gap: 8, alignItems: "flex-start", marginTop: 16 }}>
            <input type="checkbox" checked={checked} onChange={(e) => setChecked(e.target.checked)} />
            <span>Saya menyetujui pemrosesan data pribadi saya untuk keperluan rekrutmen ini.</span>
          </label>
          {error && <ErrorState message={error} onRetry={handleSubmit} />}
          <div style={{ marginTop: 16 }}>
            <Button variant="primary" disabled={!checked || submitting} onClick={handleSubmit}>
              {submitting ? "Menyimpan..." : "Setuju dan Lanjutkan"}
            </Button>
          </div>
        </>
      )}

      {showTelegramStep && !telegramLinked && (
        <div style={{ marginTop: 16 }}>
          <p>
            Terima kasih. Untuk menerima hasil wawancara Anda, tautan Telegram <strong>wajib</strong>{" "}
            dilakukan sebelum memulai wawancara — ini adalah satu-satunya cara kami mengirimkan hasil
            Anda.
          </p>
          <div style={{ display: "flex", gap: 12, marginTop: 12 }}>
            <a href={`https://t.me/${BOT_USERNAME}?start=${token}`} target="_blank" rel="noopener noreferrer">
              <Button variant="primary">Tautkan Telegram</Button>
            </a>
            <Button variant="secondary" disabled={checkingStatus} onClick={handleCheckStatus}>
              {checkingStatus ? "Memeriksa..." : "Sudah tautkan? Cek status"}
            </Button>
          </div>
          {notYetLinkedMessage && (
            <p style={{ marginTop: 8, color: "var(--color-warning)" }}>
              Belum terdeteksi. Pastikan Anda sudah menekan "Start" di Telegram, lalu coba lagi.
            </p>
          )}
        </div>
      )}

      {showTelegramStep && telegramLinked && (
        <div style={{ marginTop: 16 }}>
          <p>Telegram berhasil ditautkan. Anda siap memulai wawancara.</p>
          <Button variant="primary" onClick={() => navigate(`/candidate/${candidateId}/interview?token=${token}`)}>
            Mulai Wawancara
          </Button>
        </div>
      )}
    </Card>
  );
}

export function CandidateConsentPage() {
  return (
    <CandidateTokenGuard requireConsent={false}>
      {(candidate, token) => (
        <div style={{ maxWidth: 520, margin: "80px auto", padding: "0 16px" }}>
          <ConsentFlow candidateId={candidate.id} token={token} hasTelegramLink={candidate.has_telegram_link} />
        </div>
      )}
    </CandidateTokenGuard>
  );
}
