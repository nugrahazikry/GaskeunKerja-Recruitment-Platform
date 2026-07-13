import { useEffect, useRef, useState } from "react";
import { CandidateTokenGuard } from "../lib/CandidateTokenGuard";
import { useAudioRecorder } from "../lib/useAudioRecorder";
import { Card } from "../components/Card";
import { Button } from "../components/Button";
import { ErrorState } from "../components/ErrorState";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { EmptyState } from "../components/EmptyState";
import { api } from "../api/client";

type Question = {
  id: number;
  question_text: string;
  order_index: number;
};

function formatElapsed(seconds: number): string {
  const m = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const s = (seconds % 60).toString().padStart(2, "0");
  return `${m}:${s}`;
}

function InterviewFlow({ candidateId, token }: { candidateId: number; token: string }) {
  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [loadError, setLoadError] = useState(false);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [completed, setCompleted] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [submitBlockedMessage, setSubmitBlockedMessage] = useState<string | null>(null);

  const sessionId = useRef(`web-${Date.now()}`);
  const recorder = useAudioRecorder();

  useEffect(() => {
    api
      .GET("/candidates/{candidate_id}/questions", { params: { path: { candidate_id: candidateId }, query: { token } } })
      .then(({ data, error }) => {
        if (error || !data) {
          setLoadError(true);
          return;
        }
        setQuestions(data);
      });
  }, [candidateId, token]);

  async function handleSubmit() {
    if (!recorder.audioBlob || recorder.elapsedSeconds === 0) {
      setSubmitBlockedMessage("Rekaman kosong tidak dapat dikirim. Silakan rekam jawaban Anda.");
      return;
    }
    setSubmitBlockedMessage(null);
    setUploadError(null);
    recorder.setState("uploading");

    const question = questions![questionIndex];
    const formData = new FormData();
    formData.append("question_id", String(question.id));
    formData.append("session", sessionId.current);
    formData.append("token", token);
    formData.append("file", recorder.audioBlob, "answer.webm");

    const res = await fetch(
      `${(import.meta.env.VITE_API_BASE_URL as string) ?? "http://localhost:8000"}/candidates/${candidateId}/answers`,
      { method: "POST", body: formData }
    );

    if (!res.ok) {
      setUploadError("Gagal mengirim jawaban. Silakan coba lagi.");
      recorder.setState("stopped");
      return;
    }

    recorder.reset();
    if (questionIndex + 1 < questions!.length) {
      setQuestionIndex((i) => i + 1);
    } else {
      setCompleted(true);
    }
  }

  if (loadError) {
    return <ErrorState message="Gagal memuat pertanyaan wawancara." />;
  }
  if (!questions) {
    return <SpinnerWithLabel label="Memuat pertanyaan..." />;
  }
  if (questions.length === 0) {
    return <EmptyState message="Belum ada pertanyaan wawancara yang disetujui untuk posisi ini." />;
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
      <p style={{ opacity: 0.6 }}>
        Pertanyaan {questionIndex + 1} dari {questions.length}
      </p>
      <h1>{question.question_text}</h1>

      {recorder.state === "idle" && (
        <Button variant="primary" onClick={recorder.startRecording}>
          Mulai Rekam
        </Button>
      )}

      {recorder.state === "requesting-permission" && <SpinnerWithLabel label="Meminta izin mikrofon..." />}

      {recorder.state === "denied" && (
        <ErrorState
          message="Izinkan akses mikrofon untuk melanjutkan."
          onRetry={recorder.startRecording}
        />
      )}

      {recorder.state === "recording" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <p style={{ fontSize: 32, fontWeight: 700 }}>{formatElapsed(recorder.elapsedSeconds)}</p>
          <Button variant="danger" onClick={recorder.stopRecording}>
            Berhenti Rekam
          </Button>
        </div>
      )}

      {recorder.state === "stopped" && recorder.audioUrl && (
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <audio controls src={recorder.audioUrl} />
          {submitBlockedMessage && <ErrorState message={submitBlockedMessage} />}
          {uploadError && <ErrorState message={uploadError} onRetry={handleSubmit} />}
          <div style={{ display: "flex", gap: 12 }}>
            <Button variant="secondary" onClick={recorder.reRecord}>
              Rekam Ulang
            </Button>
            <Button variant="primary" onClick={handleSubmit}>
              Kirim Jawaban
            </Button>
          </div>
        </div>
      )}

      {recorder.state === "uploading" && <SpinnerWithLabel label="Mengunggah jawaban..." />}
    </Card>
  );
}

export function CandidateInterviewPage() {
  return (
    <CandidateTokenGuard requireConsent={true}>
      {(candidate, token) =>
        candidate.interview_completed ? (
          <div style={{ maxWidth: 480, margin: "80px auto", padding: "0 16px" }}>
            <Card>
              <h1>Wawancara sudah selesai, terima kasih</h1>
            </Card>
          </div>
        ) : (
          <div style={{ maxWidth: 480, margin: "80px auto", padding: "0 16px" }}>
            <InterviewFlow candidateId={candidate.id} token={token} />
          </div>
        )
      }
    </CandidateTokenGuard>
  );
}
