import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Card } from "../components/Card";
import { Button } from "../components/Button";
import { TextField } from "../components/FormField";
import { Badge } from "../components/Badge";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { ErrorState } from "../components/ErrorState";
import { EmptyState } from "../components/EmptyState";
import { api } from "../api/client";

type Question = {
  id: number;
  job_id: number;
  question_text: string;
  order_index: number;
  status: string;
};

type DraftItem = { id: number | null; question_text: string; order_index: number };

type State =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; questions: Question[] };

export function QuestionsPage() {
  const { jobId } = useParams();
  const [state, setState] = useState<State>({ status: "loading" });
  const [drafts, setDrafts] = useState<DraftItem[]>([]);
  const [busy, setBusy] = useState<null | "generate" | "save" | "approve">(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [lastFailedAction, setLastFailedAction] = useState<null | "generate" | "save" | "approve">(null);

  function load() {
    setState({ status: "loading" });
    api
      .GET("/jobs/{job_id}/questions", { params: { path: { job_id: Number(jobId) } } })
      .then(({ data, error }) => {
        if (error || !data) {
          setState({ status: "error" });
          return;
        }
        setState({ status: "ready", questions: data });
        setDrafts(data.map((q) => ({ id: q.id, question_text: q.question_text, order_index: q.order_index })));
      });
  }

  useEffect(load, [jobId]);

  const isApproved = state.status === "ready" && state.questions.some((q) => q.status === "approved");
  const hasQuestions = state.status === "ready" && state.questions.length > 0;

  async function handleGenerate() {
    setBusy("generate");
    setActionError(null);
    const { data, error } = await api.POST("/jobs/{job_id}/questions/generate", {
      params: { path: { job_id: Number(jobId) } },
    });
    setBusy(null);
    if (error || !data) {
      setActionError("Gagal membuat pertanyaan.");
      setLastFailedAction("generate");
      return;
    }
    setLastFailedAction(null);
    setState({ status: "ready", questions: data });
    setDrafts(data.map((q) => ({ id: q.id, question_text: q.question_text, order_index: q.order_index })));
  }

  function updateDraft(index: number, text: string) {
    setDrafts((d) => d.map((item, i) => (i === index ? { ...item, question_text: text } : item)));
  }

  function addDraft() {
    setDrafts((d) => [...d, { id: null, question_text: "", order_index: d.length }]);
  }

  function removeDraft(index: number) {
    setDrafts((d) => d.filter((_, i) => i !== index).map((item, i) => ({ ...item, order_index: i })));
  }

  async function handleSave() {
    setBusy("save");
    setActionError(null);
    const { data, error } = await api.PUT("/jobs/{job_id}/questions", {
      params: { path: { job_id: Number(jobId) } },
      body: { questions: drafts },
    });
    setBusy(null);
    if (error || !data) {
      setActionError("Gagal menyimpan pertanyaan.");
      setLastFailedAction("save");
      return;
    }
    setLastFailedAction(null);
    setState({ status: "ready", questions: data });
    setDrafts(data.map((q) => ({ id: q.id, question_text: q.question_text, order_index: q.order_index })));
  }

  async function handleApprove() {
    setBusy("approve");
    setActionError(null);
    const { data, error } = await api.POST("/jobs/{job_id}/questions/approve", {
      params: { path: { job_id: Number(jobId) } },
    });
    setBusy(null);
    if (error || !data) {
      setActionError("Gagal menyetujui pertanyaan.");
      setLastFailedAction("approve");
      return;
    }
    setLastFailedAction(null);
    setState({ status: "ready", questions: data });
  }

  function retryLastAction() {
    if (lastFailedAction === "generate") handleGenerate();
    else if (lastFailedAction === "save") handleSave();
    else if (lastFailedAction === "approve") handleApprove();
  }

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", padding: "0 16px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <h1>Pertanyaan Wawancara</h1>
        <Link to={`/jobs/${jobId}`}>
          <Button variant="secondary">Kembali ke Kandidat</Button>
        </Link>
      </div>

      <Card>
        {state.status === "loading" && <SpinnerWithLabel label="Memuat pertanyaan..." />}
        {state.status === "error" && (
          <ErrorState message="Gagal memuat pertanyaan." onRetry={load} />
        )}

        {state.status === "ready" && !hasQuestions && (
          <>
            <EmptyState message="Belum ada pertanyaan wawancara untuk lowongan ini." />
            <div style={{ marginTop: 12 }}>
              <Button variant="primary" onClick={handleGenerate} disabled={busy === "generate"}>
                {busy === "generate" ? "Membuat..." : "Buat Pertanyaan (AI)"}
              </Button>
            </div>
          </>
        )}

        {state.status === "ready" && hasQuestions && (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {isApproved && <Badge tone="success">Disetujui</Badge>}
            {!isApproved && <Badge tone="warning">Draf</Badge>}

            {drafts.map((d, i) => (
              <div key={d.id ?? `new-${i}`} style={{ display: "flex", gap: 8, alignItems: "flex-end" }}>
                <div style={{ flex: 1 }}>
                  <TextField
                    id={`q-${i}`}
                    label={`Pertanyaan ${i + 1}`}
                    value={d.question_text}
                    disabled={isApproved}
                    onChange={(e) => updateDraft(i, e.target.value)}
                  />
                </div>
                {!isApproved && (
                  <Button variant="danger" onClick={() => removeDraft(i)} disabled={busy !== null}>
                    Hapus
                  </Button>
                )}
              </div>
            ))}

            {actionError && <ErrorState message={actionError} onRetry={retryLastAction} />}

            {!isApproved && (
              <div style={{ display: "flex", gap: 12 }}>
                <Button variant="secondary" onClick={addDraft} disabled={busy !== null}>
                  + Tambah Pertanyaan
                </Button>
                <Button variant="primary" onClick={handleSave} disabled={busy !== null}>
                  {busy === "save" ? "Menyimpan..." : "Simpan Perubahan"}
                </Button>
                <Button variant="primary" onClick={handleApprove} disabled={busy !== null}>
                  {busy === "approve" ? "Menyetujui..." : "Setujui Pertanyaan"}
                </Button>
              </div>
            )}
          </div>
        )}
      </Card>
    </div>
  );
}
