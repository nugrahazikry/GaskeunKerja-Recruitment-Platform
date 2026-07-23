import { useEffect, useRef, useState } from "react";
import { CandidateTokenGuard } from "../lib/CandidateTokenGuard";
import { useVideoRecorder } from "../lib/useVideoRecorder";
import { Card } from "../components/Card";
import { Button } from "../components/Button";
import { ErrorState } from "../components/ErrorState";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { EmptyState } from "../components/EmptyState";
import { CandidateHeader } from "../components/CandidateHeader";
import { api } from "../api/client";

type Question = {
  id: number;
  question_text: string;
  order_index: number;
  duration_seconds: number;
};

function formatElapsed(seconds: number): string {
  const m = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const s = (seconds % 60).toString().padStart(2, "0");
  return `${m}:${s}`;
}

type PendingAnswer = { questionId: number; blob: Blob };

function InterviewFlow({
  candidateId,
  token,
  questions,
}: {
  candidateId: number;
  token: string;
  questions: Question[];
}) {
  const [questionIndex, setQuestionIndex] = useState(0);
  const [completed, setCompleted] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  // Round-3 follow-up #21 (2026-07-19): recorded answers now accumulate here across ALL
  // questions and are only uploaded once, after the LAST question — previously each "Kirim
  // Jawaban" click uploaded immediately and blocked moving to the next question on that upload's
  // network round-trip, which visibly added latency between every single question. Recording is
  // now fully decoupled from saving: the candidate can move through all questions back-to-back,
  // and the (now single, batched) upload wait happens once at the very end instead of N times.
  const [pendingAnswers, setPendingAnswers] = useState<PendingAnswer[]>([]);
  const [uploadProgress, setUploadProgress] = useState<{ done: number; total: number } | null>(null);

  const sessionId = useRef(`web-${Date.now()}`);
  // Each question carries its own HR-set time limit — passing it fresh per render means the
  // recorder auto-stops at the CURRENT question's duration, not a single job-wide value.
  const recorder = useVideoRecorder(questions[questionIndex].duration_seconds);

  async function uploadAllAnswers(answers: PendingAnswer[]) {
    setUploadError(null);
    for (let i = 0; i < answers.length; i++) {
      setUploadProgress({ done: i, total: answers.length });
      const { questionId, blob } = answers[i];
      const formData = new FormData();
      formData.append("question_id", String(questionId));
      formData.append("session", sessionId.current);
      formData.append("token", token);
      formData.append("file", blob, "answer.webm");

      const res = await fetch(
        `${(import.meta.env.VITE_API_BASE_URL as string) ?? "http://localhost:8000"}/candidates/${candidateId}/answers`,
        { method: "POST", body: formData }
      );

      if (!res.ok) {
        setUploadError(
          `Gagal mengirim jawaban ${i + 1} dari ${answers.length}. Silakan coba lagi — jawaban yang sudah terekam tidak hilang.`
        );
        setUploadProgress(null);
        return;
      }
    }
    setUploadProgress(null);
    // 2026-07-22 (user decision): the candidate is released as soon as the video data is
    // confirmed stored — not once the backend's post-interview LLM chain finishes. That chain
    // (transcription/scoring/summary/upskilling plan) now runs fully invisibly in the background;
    // only HR-facing surfaces (Laporan list, report page) wait for it to actually complete.
    setCompleted(true);
  }

  function handleSubmit() {
    if (!recorder.videoBlob) return;
    const question = questions[questionIndex];
    const nextAnswers = [...pendingAnswers, { questionId: question.id, blob: recorder.videoBlob }];
    setPendingAnswers(nextAnswers);
    recorder.reset();

    if (questionIndex + 1 < questions.length) {
      setQuestionIndex((i) => i + 1);
    } else {
      // Last question answered — this is the ONE point where anything actually gets uploaded.
      uploadAllAnswers(nextAnswers);
    }
  }

  if (uploadProgress) {
    return (
      <Card>
        <SpinnerWithLabel
          label={`Mengunggah jawaban ${uploadProgress.done + 1} dari ${uploadProgress.total}...`}
        />
      </Card>
    );
  }

  if (uploadError) {
    return (
      <Card>
        <ErrorState message={uploadError} onRetry={() => uploadAllAnswers(pendingAnswers)} />
      </Card>
    );
  }

  if (completed) {
    return (
      <Card>
        <h1>Wawancara selesai, terima kasih!</h1>
        <p>Jawaban Anda telah dikirim. Tim rekrutmen akan meninjau hasil wawancara Anda.</p>
      </Card>
    );
  }

  const question = questions[questionIndex];

  return (
    <Card>
      <p style={{ opacity: 0.6, marginBottom: 10 }}>
        Pertanyaan {questionIndex + 1} dari {questions.length}
      </p>

      <div
        style={{
          position: "relative",
          width: "100%",
          aspectRatio: "16 / 9",
          background: "#111",
          borderRadius: 12,
          overflow: "hidden",
          marginBottom: 14,
        }}
      >
        {(recorder.state === "previewing" || recorder.state === "countdown" || recorder.state === "recording") && (
          // eslint-disable-next-line jsx-a11y/media-has-caption
          <video
            ref={recorder.previewVideoRef}
            autoPlay
            muted
            playsInline
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        )}
        {recorder.state === "stopped" && recorder.videoUrl && (
          <video controls src={recorder.videoUrl} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        )}
        {recorder.state === "countdown" && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 64,
              fontWeight: 700,
              color: "#fff",
              background: "rgba(0,0,0,0.35)",
            }}
          >
            {recorder.countdown}
          </div>
        )}
        {recorder.state === "recording" && (
          <div
            style={{
              position: "absolute",
              top: 10,
              right: 10,
              background: "rgba(0,0,0,0.6)",
              color: "#fff",
              padding: "4px 10px",
              borderRadius: 999,
              fontSize: 14,
              fontWeight: 700,
              display: "flex",
              alignItems: "center",
              gap: 6,
            }}
          >
            <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#e5484d" }} />
            {formatElapsed(recorder.remainingSeconds)}
          </div>
        )}
        {(recorder.state === "idle" || recorder.state === "requesting-permission" || recorder.state === "denied") && (
          <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", color: "#888" }}>
            Kamera belum aktif
          </div>
        )}
      </div>

      <div className="consent-box" style={{ textAlign: "center", marginBottom: 12, padding: 12 }}>
        <strong style={{ display: "block", fontSize: "1rem", marginBottom: 2 }}>
          Pertanyaan {questionIndex + 1}:
        </strong>
        <span style={{ fontSize: "0.92rem" }}>{question.question_text}</span>
      </div>

      {/* Round-3 follow-up #16 (2026-07-19): "Uji Kamera & Mikrofon" removed from here — the new
          dedicated CandidateCameraTestPage (T17-followup #15) is now the primary check, shown
          once between consent and the first question; repeating it per-question was redundant. */}
      {recorder.state === "idle" && (
        <Button variant="primary" onClick={recorder.startRecording}>
          Mulai Recording
        </Button>
      )}

      {recorder.state === "requesting-permission" && <SpinnerWithLabel label="Meminta izin kamera & mikrofon..." />}

      {recorder.state === "denied" && (
        <ErrorState
          message="Izinkan akses kamera & mikrofon untuk melanjutkan."
          onRetry={recorder.startRecording}
        />
      )}

      {recorder.state === "countdown" && <p style={{ fontSize: "0.85rem", opacity: 0.7 }}>Bersiap merekam...</p>}

      {recorder.state === "recording" && (
        <Button variant="danger" onClick={recorder.stopRecording}>
          Berhenti Rekam
        </Button>
      )}

      {recorder.state === "stopped" && recorder.videoUrl && (
        <div style={{ display: "flex", gap: 12 }}>
          <Button variant="primary" onClick={handleSubmit}>
            {questionIndex + 1 < questions.length ? "Kirim Jawaban" : "Selesai & Kirim Semua Jawaban"}
          </Button>
          <Button variant="secondary" onClick={recorder.reRecord}>
            Rekam Ulang
          </Button>
        </div>
      )}
    </Card>
  );
}

function InterviewLoader({ candidateId, token }: { candidateId: number; token: string }) {
  const [state, setState] = useState<
    { status: "loading" } | { status: "error" } | { status: "ready"; questions: Question[] }
  >({ status: "loading" });
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    setState({ status: "loading" });
    api
      .GET("/candidates/{candidate_id}/questions", { params: { path: { candidate_id: candidateId }, query: { token } } })
      .then(({ data, error }) => {
        if (error || !data) {
          setState({ status: "error" });
          return;
        }
        setState({ status: "ready", questions: data });
      });
  }, [candidateId, token, reloadKey]);

  if (state.status === "error") {
    return <ErrorState message="Gagal memuat pertanyaan wawancara." onRetry={() => setReloadKey((k) => k + 1)} />;
  }
  if (state.status === "loading") {
    return <SpinnerWithLabel label="Memuat pertanyaan..." />;
  }
  if (state.questions.length === 0) {
    return <EmptyState message="Belum ada pertanyaan wawancara yang disetujui untuk posisi ini." />;
  }

  return <InterviewFlow candidateId={candidateId} token={token} questions={state.questions} />;
}

export function CandidateInterviewPage() {
  return (
    <CandidateTokenGuard requireConsent={true}>
      {(candidate, token) => (
        <div>
          <CandidateHeader step="Langkah 3 dari 3" />
          {candidate.interview_completed ? (
            <div className="main" style={{ maxWidth: 680, paddingTop: 32 }}>
              <Card>
                <h1>Wawancara selesai, terima kasih!</h1>
                <p>Jawaban Anda telah dikirim. Tim rekrutmen akan meninjau hasil wawancara Anda.</p>
              </Card>
            </div>
          ) : (
            <div className="main" style={{ maxWidth: 680, paddingTop: 32 }}>
              <InterviewLoader candidateId={candidate.id} token={token} />
            </div>
          )}
        </div>
      )}
    </CandidateTokenGuard>
  );
}
