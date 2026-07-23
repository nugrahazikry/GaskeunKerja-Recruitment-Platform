import { useEffect, useState } from "react";
import { Modal } from "./Modal";
import { Button } from "./Button";
import { SpinnerWithLabel } from "./SpinnerWithLabel";
import { ErrorState } from "./ErrorState";
import { api } from "../api/client";

export function InviteModal({
  candidateId,
  candidateAlias,
  alreadyInvited,
  onClose,
  onInvited,
}: {
  candidateId: number;
  candidateAlias?: string;
  alreadyInvited: boolean;
  onClose: () => void;
  onInvited: () => void;
}) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [link, setLink] = useState<string | null>(null);
  const [contactEmail, setContactEmail] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);
  const [emailBusy, setEmailBusy] = useState(false);
  const [emailError, setEmailError] = useState<string | null>(null);
  const [emailSent, setEmailSent] = useState(false);
  const [showNoEmailAlert, setShowNoEmailAlert] = useState(false);
  const [showSendConfirm, setShowSendConfirm] = useState(false);
  // Round-3 follow-up #13 (2026-07-19, real bug found via live testing): the "already invited"
  // view used to silently show whatever token was on file, even a LONG-expired one (72h TTL) —
  // the candidate got a dead "Link tidak valid" page with no indication from the HR side that
  // the link had simply expired, and no way to fix it without leaving this modal.
  const [expired, setExpired] = useState(false);
  const [regenerating, setRegenerating] = useState(false);

  // Round-3 follow-up #14 (2026-07-19, real bug found via live testing): used to point straight
  // at /interview — CandidateTokenGuard's requireConsent redirect only fires if has_consent is
  // still false, so once a candidate had EVER consented (e.g. from earlier testing), a freshly
  // regenerated invite link silently skipped consent entirely. User wants every invite link to
  // always land on consent first, every time — pointing here instead of /interview does that
  // unconditionally; consent page's own "Mulai Wawancara" button forwards to /interview after.
  function buildLink(token: string) {
    return `${window.location.origin}/candidate/${candidateId}/consent?token=${token}`;
  }

  useEffect(() => {
    setLoading(true);
    setError(null);
    setExpired(false);

    if (alreadyInvited) {
      // Re-view: read the existing token, never regenerate it (would break an already-shared link)
      // — UNLESS it's expired, in which case there's nothing valid left to preserve; the UI below
      // offers an explicit "Buat Link Baru" action for that case instead of silently regenerating.
      api.GET("/candidates/{candidate_id}", { params: { path: { candidate_id: candidateId } } }).then(
        ({ data, error: apiError }) => {
          setLoading(false);
          if (apiError || !data || !data.token) {
            setError("Gagal memuat link undangan.");
            return;
          }
          if (data.token_expires_at && new Date(data.token_expires_at) < new Date()) {
            setExpired(true);
            setContactEmail(data.contact_email ?? null);
            return;
          }
          setLink(buildLink(data.token));
          setContactEmail(data.contact_email ?? null);
        }
      );
    } else {
      api.POST("/candidates/{candidate_id}/invite", { params: { path: { candidate_id: candidateId } } }).then(
        ({ data, error: apiError }) => {
          setLoading(false);
          if (apiError || !data) {
            setError(
              (apiError as { detail?: string } | undefined)?.detail ??
                "Gagal mengundang kandidat. Pastikan pertanyaan wawancara sudah disetujui."
            );
            return;
          }
          setLink(buildLink(data.token));
          setContactEmail(data.contact_email ?? null);
          onInvited();
        }
      );
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [candidateId, alreadyInvited, reloadKey]);

  async function handleRegenerate() {
    setRegenerating(true);
    setError(null);
    const { data, error: apiError } = await api.POST("/candidates/{candidate_id}/invite", {
      params: { path: { candidate_id: candidateId } },
    });
    setRegenerating(false);
    if (apiError || !data) {
      setError(
        (apiError as { detail?: string } | undefined)?.detail ??
          "Gagal membuat link baru. Pastikan pertanyaan wawancara sudah disetujui."
      );
      return;
    }
    setExpired(false);
    setLink(buildLink(data.token));
    onInvited();
  }

  function handleSendEmailClick() {
    if (!contactEmail) {
      setShowNoEmailAlert(true);
      return;
    }
    setShowSendConfirm(true);
  }

  async function handleSendEmail() {
    if (!link) return;
    setShowSendConfirm(false);
    setEmailBusy(true);
    setEmailError(null);
    setEmailSent(false);
    const { error: apiError } = await api.POST("/candidates/{candidate_id}/send-invite-email", {
      params: { path: { candidate_id: candidateId } },
      body: { invite_link: link },
    });
    setEmailBusy(false);
    if (apiError) {
      setEmailError((apiError as { detail?: string })?.detail ?? "Gagal mengirim email undangan.");
      return;
    }
    setEmailSent(true);
  }

  const title = alreadyInvited
    ? `Link Undangan ${candidateAlias ?? "Kandidat"}`.trim()
    : `Undang ${candidateAlias ?? "Kandidat"}`.trim();

  return (
    <Modal title={title} onClose={onClose}>
      {loading && <SpinnerWithLabel label="Memuat link undangan..." />}
      {error && <ErrorState message={error} onRetry={() => setReloadKey((k) => k + 1)} />}
      {!loading && !error && expired && (
        <>
          <p style={{ color: "var(--danger)", fontSize: "0.86rem", lineHeight: 1.6 }}>
            Link undangan sebelumnya untuk kandidat ini sudah kedaluwarsa (berlaku 72 jam sejak
            dibuat). Kandidat akan melihat halaman "Link tidak valid" jika membuka link lama
            tersebut. Buat link baru untuk melanjutkan.
          </p>
          <div className="modal-actions">
            <Button variant="ghost" onClick={onClose}>
              Tutup
            </Button>
            <Button variant="primary" disabled={regenerating} onClick={handleRegenerate}>
              {regenerating ? "Membuat..." : "Buat Link Baru"}
            </Button>
          </div>
        </>
      )}
      {!loading && link && (
        <>
          <p>
            Tautan unik untuk kandidat mengisi consent dan mengikuti wawancara AI. Tautan ini berlaku 72
            jam.
          </p>
          <div className="link-box">
            <input readOnly value={link} onFocus={(e) => e.target.select()} />
          </div>
          <p className="hint" style={{ marginTop: 8 }}>
            Kandidat menerima tautan ini secara manual (salin &amp; kirim sendiri), atau otomatis lewat email
            jika alamat email kandidat sudah terdeteksi dari CV.
          </p>
          {contactEmail && (
            <p className="hint" style={{ marginTop: 4 }}>
              Email kandidat terdeteksi: <strong>{contactEmail}</strong>
            </p>
          )}
          {emailSent && (
            <p style={{ color: "var(--success)", fontSize: "0.84rem", marginTop: 4 }}>
              Email undangan berhasil dikirim.
            </p>
          )}
          {emailError && <p style={{ color: "var(--danger)", fontSize: "0.84rem", marginTop: 4 }}>{emailError}</p>}
          <div className="modal-actions">
            <Button variant="ghost" onClick={onClose}>
              Tutup
            </Button>
            <Button variant="primary" disabled={emailBusy} onClick={handleSendEmailClick}>
              {emailBusy ? "Mengirim..." : "Kirim via Email"}
            </Button>
          </div>
        </>
      )}

      {showNoEmailAlert && (
        <Modal title="Email Kandidat Belum Ada" onClose={() => setShowNoEmailAlert(false)}>
          <p>Kandidat ini belum memiliki alamat email. Isi email kandidat terlebih dahulu sebelum mengirim undangan lewat email.</p>
          <div className="modal-actions">
            <Button variant="primary" onClick={() => setShowNoEmailAlert(false)}>
              Mengerti
            </Button>
          </div>
        </Modal>
      )}

      {showSendConfirm && (
        <Modal title="Kirim Undangan?" onClose={() => setShowSendConfirm(false)}>
          <p>
            Apakah Anda yakin ingin mengirim undangan wawancara ke email kandidat ini
            {contactEmail ? <> (<strong>{contactEmail}</strong>)</> : null}?
          </p>
          <div className="modal-actions">
            <Button variant="ghost" onClick={() => setShowSendConfirm(false)}>
              Batal
            </Button>
            <Button variant="primary" onClick={handleSendEmail}>
              Kirim
            </Button>
          </div>
        </Modal>
      )}
    </Modal>
  );
}
