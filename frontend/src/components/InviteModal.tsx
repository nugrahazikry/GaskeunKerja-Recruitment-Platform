import { useEffect, useState } from "react";
import { Modal } from "./Modal";
import { Button } from "./Button";
import { SpinnerWithLabel } from "./SpinnerWithLabel";
import { ErrorState } from "./ErrorState";
import { api } from "../api/client";

export function InviteModal({
  candidateId,
  alreadyInvited,
  onClose,
  onInvited,
}: {
  candidateId: number;
  alreadyInvited: boolean;
  onClose: () => void;
  onInvited: () => void;
}) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [link, setLink] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [reloadKey, setReloadKey] = useState(0);

  function buildLink(token: string) {
    return `${window.location.origin}/candidate/${candidateId}/interview?token=${token}`;
  }

  useEffect(() => {
    setLoading(true);
    setError(null);

    if (alreadyInvited) {
      // Re-view: read the existing token, never regenerate it (would break an already-shared link)
      api.GET("/candidates/{candidate_id}", { params: { path: { candidate_id: candidateId } } }).then(
        ({ data, error: apiError }) => {
          setLoading(false);
          if (apiError || !data || !data.token) {
            setError("Gagal memuat link undangan.");
            return;
          }
          setLink(buildLink(data.token));
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
          onInvited();
        }
      );
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [candidateId, alreadyInvited, reloadKey]);

  async function handleCopy() {
    if (!link) return;
    await navigator.clipboard.writeText(link);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <Modal title={alreadyInvited ? "Link Undangan" : "Undang ke Interview"} onClose={onClose}>
      {loading && <SpinnerWithLabel label="Memuat link undangan..." />}
      {error && <ErrorState message={error} onRetry={() => setReloadKey((k) => k + 1)} />}
      {!loading && link && (
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <p>Bagikan link ini ke kandidat secara manual (misalnya via WhatsApp atau email):</p>
          <div
            style={{
              padding: 12,
              background: "var(--color-paper)",
              border: "1px solid var(--color-border)",
              borderRadius: "var(--radius-sm)",
              wordBreak: "break-all",
              fontSize: 13,
            }}
          >
            {link}
          </div>
          <Button variant="primary" onClick={handleCopy}>
            {copied ? "Tersalin!" : "Salin Link"}
          </Button>
        </div>
      )}
    </Modal>
  );
}
