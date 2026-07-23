import { useNavigate } from "react-router-dom";
import { CandidateTokenGuard } from "../lib/CandidateTokenGuard";
import { CandidateHeader } from "../components/CandidateHeader";
import { useVideoRecorder } from "../lib/useVideoRecorder";
import { Card } from "../components/Card";
import { Button } from "../components/Button";
import { ErrorState } from "../components/ErrorState";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";

// Round-3 follow-up #17 (2026-07-19): a live "heartbeat"-style bar visualizer driven by the
// mic's real audio level (useVideoRecorder's Web Audio AnalyserNode) — a static camera preview
// alone gives no confirmation the microphone is actually picking up sound; this gives the
// candidate visual proof their voice registers before they commit to a timed answer.
// Per-bar sensitivity multipliers, symmetric around the center bar — center bars react most
// strongly (tallest swing), outer bars less, for a natural-looking pulse rather than uniform bars.
const METER_BAR_WEIGHTS = [0.35, 0.55, 0.75, 0.9, 1, 0.9, 0.75, 0.55, 0.35];

function AudioLevelMeter({ level }: { level: number }) {
  return (
    <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "center", gap: 4, height: 40 }}>
      {METER_BAR_WEIGHTS.map((weight, i) => {
        const heightPct = 12 + level * weight * 0.88;
        return (
          <div
            key={i}
            style={{
              width: 6,
              height: `${Math.min(100, heightPct)}%`,
              minHeight: 4,
              borderRadius: 3,
              background: level > 4 ? "var(--teal)" : "var(--border)",
              transition: "height 90ms ease-out, background 150ms ease-out",
            }}
          />
        );
      })}
    </div>
  );
}

// Round-3 follow-up #15 (2026-07-19): dedicated step between consent and the interview questions
// so a candidate confirms their camera/mic actually work BEFORE seeing any question — the
// per-question "Uji Kamera & Mikrofon" button on CandidateInterviewPage stays as a secondary
// safety net, this page is the primary, always-shown check.
function CameraTestFlow({ candidateId, token }: { candidateId: number; token: string }) {
  const navigate = useNavigate();
  // durationSeconds is irrelevant here — this hook instance only ever uses startPreview(), never
  // startRecording()/beginCapture(), so no answer-timer is ever started.
  const recorder = useVideoRecorder(0);

  return (
    <div className="main" style={{ maxWidth: 680, paddingTop: 32 }}>
      <div className="pagehead" style={{ textAlign: "center" }}>
        <h1>Uji Kamera &amp; Mikrofon</h1>
        <p>Pastikan kamera dan mikrofon Anda berfungsi dengan baik sebelum memulai wawancara.</p>
      </div>
      <Card>
        <div
          style={{
            position: "relative",
            width: "100%",
            aspectRatio: "16 / 9",
            background: "#111",
            borderRadius: 12,
            overflow: "hidden",
            marginBottom: 16,
          }}
        >
          {recorder.state === "previewing" && (
            // eslint-disable-next-line jsx-a11y/media-has-caption
            <video
              ref={recorder.previewVideoRef}
              autoPlay
              muted
              playsInline
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            />
          )}
          {recorder.state !== "previewing" && (
            <div
              style={{
                position: "absolute",
                inset: 0,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#888",
              }}
            >
              Kamera belum aktif
            </div>
          )}
        </div>

        {recorder.state === "previewing" && (
          <div style={{ marginBottom: 12 }}>
            <p className="hint" style={{ textAlign: "center", marginBottom: 6 }}>
              Level mikrofon — coba bicara untuk memastikan suara Anda terekam:
            </p>
            <AudioLevelMeter level={recorder.audioLevel} />
          </div>
        )}

        {recorder.state === "idle" && (
          <Button variant="primary" block onClick={recorder.startPreview}>
            Uji Kamera &amp; Mikrofon
          </Button>
        )}

        {recorder.state === "requesting-permission" && (
          <SpinnerWithLabel label="Meminta izin kamera & mikrofon..." />
        )}

        {recorder.state === "denied" && (
          <ErrorState
            message="Izinkan akses kamera & mikrofon untuk melanjutkan."
            onRetry={recorder.startPreview}
          />
        )}

        {recorder.state === "previewing" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <p className="hint" style={{ textAlign: "center" }}>
              Kamera &amp; mikrofon aktif. Periksa gambar dan suara Anda di atas.
            </p>
            <Button
              variant="primary"
              block
              onClick={() => navigate(`/candidate/${candidateId}/interview?token=${token}`)}
            >
              Lanjutkan ke Wawancara
            </Button>
          </div>
        )}
      </Card>
    </div>
  );
}

export function CandidateCameraTestPage() {
  return (
    <CandidateTokenGuard requireConsent={true}>
      {(candidate, token) => (
        <div>
          <CandidateHeader step="Langkah 2 dari 3" />
          <CameraTestFlow candidateId={candidate.id} token={token} />
        </div>
      )}
    </CandidateTokenGuard>
  );
}
