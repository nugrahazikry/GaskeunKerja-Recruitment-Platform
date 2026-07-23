import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { TopBar } from "../components/TopBar";
import { Button } from "../components/Button";
import { Badge } from "../components/Badge";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { ErrorState } from "../components/ErrorState";
import { EmptyState } from "../components/EmptyState";
import { GenerateQuestionsModal } from "../components/GenerateQuestionsModal";
import { Modal } from "../components/Modal";
import { api } from "../api/client";

const MAX_QUESTIONS = 5;
const DEFAULT_QUESTION_DURATION_SECONDS = 120;

type Question = {
  id: number;
  job_id: number;
  question_text: string;
  order_index: number;
  status: string;
  duration_seconds: number;
};

// duration_seconds here is LOCAL-only state for a not-yet-persisted draft (id === null) — once a
// question is saved (real id), its authoritative duration lives in `state.questions` and is edited
// via the immediate-save PATCH endpoint instead (durationFor() below reads from there).
type DraftItem = { id: number | null; question_text: string; order_index: number; duration_seconds: number };

type State =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; questions: Question[] };

export function QuestionsPage() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [jobTitle, setJobTitle] = useState<string>("");
  const [state, setState] = useState<State>({ status: "loading" });
  const [drafts, setDrafts] = useState<DraftItem[]>([]);
  const [busy, setBusy] = useState<null | "generate" | "approve">(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [lastFailedAction, setLastFailedAction] = useState<null | "approve">(null);
  const [reopened, setReopened] = useState(false);
  const [questionDurationBusy, setQuestionDurationBusy] = useState<number | null>(null);
  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [generateError, setGenerateError] = useState<string | null>(null);
  const [generateProgress, setGenerateProgress] = useState<{ current: number; total: number } | null>(null);
  // The last-persisted state — used to detect unsaved edits (dirty check below) and as the
  // rollback target for "discard changes." Set on every successful load/save, never on a purely
  // local edit like typing in a textarea or entering edit mode.
  const [savedDrafts, setSavedDrafts] = useState<DraftItem[]>([]);
  const [pendingNav, setPendingNav] = useState<(() => void) | null>(null);

  useEffect(() => {
    api.GET("/jobs/{job_id}", { params: { path: { job_id: Number(jobId) } } }).then(({ data }) => {
      if (data) setJobTitle(data.title);
    });
  }, [jobId]);

  async function handleQuestionDurationChange(questionId: number, seconds: number) {
    setQuestionDurationBusy(questionId);
    const { data, error } = await api.PATCH("/jobs/{job_id}/questions/{question_id}/duration", {
      params: { path: { job_id: Number(jobId), question_id: questionId } },
      body: { duration_seconds: seconds },
    });
    setQuestionDurationBusy(null);
    if (!error && data && state.status === "ready") {
      setState({
        status: "ready",
        questions: state.questions.map((q) => (q.id === questionId ? { ...q, duration_seconds: seconds } : q)),
      });
    }
  }

  function toDraft(q: Question): DraftItem {
    return { id: q.id, question_text: q.question_text, order_index: q.order_index, duration_seconds: q.duration_seconds };
  }

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
        setDrafts(data.map(toDraft));
        setSavedDrafts(data.map(toDraft));
        setReopened(false);
      });
  }

  useEffect(load, [jobId]);

  const isApproved = !reopened && state.status === "ready" && state.questions.some((q) => q.status === "approved");
  // Drives which draft rows render, so it must reflect LOCAL drafts (unsaved new/AI-generated
  // questions live only in `drafts` until "Setujui & Kunci Pertanyaan"), not state.questions —
  // using state.questions here left a fresh job with 0 saved questions stuck showing the empty
  // state even after adding/generating drafts, since those never touch state.questions.
  const hasQuestions = state.status === "ready" && drafts.length > 0;

  // Only question TEXT/order/id changes count as "unsaved" — duration is saved independently and
  // immediately via PATCH .../duration for already-persisted questions, so it's excluded here.
  const isDirty =
    drafts.length !== savedDrafts.length ||
    drafts.some((d, i) => savedDrafts[i]?.id !== d.id || savedDrafts[i]?.question_text !== d.question_text);

  // Native browser dialog for tab close/refresh/external navigation — cannot be replaced with a
  // custom UI, browsers force their own "leave site?" prompt for this case regardless.
  useEffect(() => {
    function handleBeforeUnload(e: BeforeUnloadEvent) {
      if (isDirty) e.preventDefault();
    }
    window.addEventListener("beforeunload", handleBeforeUnload);
    return () => window.removeEventListener("beforeunload", handleBeforeUnload);
  }, [isDirty]);

  function guardedNavigate(to: () => void) {
    if (isDirty) {
      setPendingNav(() => to);
    } else {
      to();
    }
  }

  async function handleDiscardAndNavigate() {
    setDrafts(savedDrafts);
    setReopened(false);
    const go = pendingNav;
    setPendingNav(null);
    go?.();
  }

  async function handleSaveAndNavigate() {
    const ok = await handleApprove();
    if (!ok) return; // keep the modal's pending nav so the user can retry after seeing the error
    const go = pendingNav;
    setPendingNav(null);
    go?.();
  }

  // Round-3 follow-up (2026-07-19): AI-generated questions are no longer persisted immediately —
  // they only ever get written to the DB at "Setujui & Kunci Pertanyaan" (the PUT+approve call
  // below), same as manually-typed drafts already worked.
  //
  // Generates ONE question at a time, calling the backend once per slot IN ORDER, starting from
  // slot 1 — a real finding: batching all N into one request produced mixed/unrelated questions
  // no matter how the prompt was worded. Each call is seeded with every question generated so far
  // this run (so later questions don't overlap earlier ones), and — critically — with THAT SLOT'S
  // OWN current text as a "hint": a slot HR had already labeled with a topic note (e.g. "QC
  // pengalaman") gets a question built specifically around that note, instead of a generic
  // JD-grounded question with no connection to what HR wrote. The loop runs client-side (not one
  // big backend call) so the modal can show live "pertanyaan X dari Y" progress.
  async function handleGenerateConfirm(regenerateIndexes: number[], fromScratchCount: number) {
    const total = regenerateIndexes.length + fromScratchCount;
    if (total === 0) {
      setShowGenerateModal(false);
      return;
    }

    const slots: { hint: string | null; targetIndex: number | null }[] = regenerateIndexes.map((i) => {
      const text = drafts[i].question_text.trim();
      return { hint: text === "" ? null : text, targetIndex: i };
    });
    for (let k = 0; k < fromScratchCount; k++) {
      slots.push({ hint: null, targetIndex: null }); // targetIndex null = append as a new question
    }

    let contextQuestions = drafts
      .filter((_, i) => !regenerateIndexes.includes(i))
      .map((d) => d.question_text)
      .filter((t) => t.trim() !== "");

    setBusy("generate");
    setGenerateError(null);

    for (let idx = 0; idx < slots.length; idx++) {
      setGenerateProgress({ current: idx + 1, total: slots.length });
      const { data, error } = await api.POST("/jobs/{job_id}/questions/generate", {
        params: { path: { job_id: Number(jobId) } },
        body: { hint: slots[idx].hint, existing_questions: contextQuestions },
      });
      if (error || !data) {
        setBusy(null);
        setGenerateProgress(null);
        setGenerateError((error as { detail?: string } | undefined)?.detail ?? "Gagal membuat pertanyaan.");
        return;
      }

      const targetIndex = slots[idx].targetIndex;
      const text = data.question;
      contextQuestions = [...contextQuestions, text];
      setDrafts((current) => {
        if (targetIndex !== null) {
          return current.map((d, i) => (i === targetIndex ? { ...d, question_text: text } : d));
        }
        return [
          ...current,
          { id: null, question_text: text, order_index: current.length, duration_seconds: DEFAULT_QUESTION_DURATION_SECONDS },
        ];
      });
    }

    setBusy(null);
    setGenerateProgress(null);
    setShowGenerateModal(false);
  }

  function updateDraft(index: number, text: string) {
    setDrafts((d) => d.map((item, i) => (i === index ? { ...item, question_text: text } : item)));
  }

  function updateDraftDuration(index: number, seconds: number) {
    setDrafts((d) => d.map((item, i) => (i === index ? { ...item, duration_seconds: seconds } : item)));
  }

  function addDraft() {
    if (drafts.length >= MAX_QUESTIONS) return;
    setDrafts((d) => [
      ...d,
      { id: null, question_text: "", order_index: d.length, duration_seconds: DEFAULT_QUESTION_DURATION_SECONDS },
    ]);
  }

  function removeDraft(index: number) {
    setDrafts((d) => d.filter((_, i) => i !== index).map((item, i) => ({ ...item, order_index: i })));
  }

  async function handleApprove(): Promise<boolean> {
    setBusy("approve");
    setActionError(null);

    // Entering edit mode (handleEditPertanyaan below) is now purely local — it never calls the
    // backend reopen endpoint immediately, so an approved-then-untouched-then-abandoned edit
    // never leaves the DB in a stuck "draft" state (a real user-reported issue: reopening on
    // click meant navigating away without saving left the questions unapproved until manually
    // re-approved, even if nothing had actually changed). The backend reopen only happens here,
    // right before the save, and only if we're actually coming from that locally-unlocked state.
    if (reopened) {
      const reopenRes = await api.POST("/jobs/{job_id}/questions/reopen", {
        params: { path: { job_id: Number(jobId) } },
      });
      if (reopenRes.error) {
        setBusy(null);
        setActionError("Gagal membuka kembali pertanyaan.");
        setLastFailedAction("approve");
        return false;
      }
    }

    const saveRes = await api.PUT("/jobs/{job_id}/questions", {
      params: { path: { job_id: Number(jobId) } },
      body: { questions: drafts },
    });
    if (saveRes.error || !saveRes.data) {
      setBusy(null);
      setActionError(
        (saveRes.error as { detail?: string } | undefined)?.detail ?? "Gagal menyimpan pertanyaan."
      );
      setLastFailedAction("approve");
      return false;
    }
    const approveRes = await api.POST("/jobs/{job_id}/questions/approve", {
      params: { path: { job_id: Number(jobId) } },
    });
    setBusy(null);
    if (approveRes.error || !approveRes.data) {
      setActionError("Gagal menyetujui pertanyaan.");
      setLastFailedAction("approve");
      setState({ status: "ready", questions: saveRes.data });
      setDrafts(saveRes.data.map(toDraft));
      return false;
    }
    setLastFailedAction(null);
    setReopened(false);
    setState({ status: "ready", questions: approveRes.data });
    setDrafts(approveRes.data.map(toDraft));
    setSavedDrafts(approveRes.data.map(toDraft));
    return true;
  }

  // Purely local: unlocks the editable view for an already-approved question set without touching
  // the backend. The backend only learns about this once "Setujui & Kunci Pertanyaan" is actually
  // clicked (handleApprove calls reopen() first in that case) — see handleApprove's comment above.
  function handleEditPertanyaan() {
    setReopened(true);
  }

  function retryLastAction() {
    if (lastFailedAction === "approve") handleApprove();
  }

  function durationFor(d: DraftItem): number {
    if (d.id === null || state.status !== "ready") return d.duration_seconds;
    return state.questions.find((q) => q.id === d.id)?.duration_seconds ?? d.duration_seconds;
  }

  const canAddOrGenerate = state.status === "ready" && !isApproved;

  return (
    <div>
      <TopBar
        active="wawancara"
        jobId={Number(jobId)}
        interceptNav={(href) => guardedNavigate(() => navigate(href))}
      />
      <div className="main">
        <div className="pagehead" style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}>
          <div>
            <h1>Pertanyaan Wawancara AI</h1>
            <p>{jobTitle || "..."} &middot; ditinjau &amp; disetujui sebelum dikirim ke kandidat</p>
          </div>
          <Button variant="ghost" onClick={() => guardedNavigate(() => navigate("/jobs"))}>
            Kembali ke Daftar Lowongan
          </Button>
        </div>

        {canAddOrGenerate && (
          <div className="card" style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14, flexWrap: "wrap" }}>
            <Button variant="ghost" onClick={addDraft} disabled={busy !== null || drafts.length >= MAX_QUESTIONS}>
              + Tambah Pertanyaan
            </Button>
            <Button variant="primary" onClick={() => setShowGenerateModal(true)} disabled={busy !== null}>
              Buat Pertanyaan (AI)
            </Button>
            <span className="hint">
              Maksimum {MAX_QUESTIONS} pertanyaan. Setiap pertanyaan punya batas waktu jawab sendiri (diatur per
              pertanyaan di bawah) — kandidat direkam video, rekaman berhenti otomatis pada batas waktu tersebut.
            </span>
          </div>
        )}

        {state.status === "ready" && isApproved && (
          <div className="card" style={{ marginBottom: 14 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
              <Badge tone="success">Disetujui</Badge>
              <Button variant="primary" onClick={handleEditPertanyaan} disabled={busy !== null}>
                Edit Pertanyaan
              </Button>
            </div>
            <span className="hint" style={{ display: "block", marginTop: 8 }}>
              Pertanyaan sudah dikunci dan siap dikirim ke kandidat.
            </span>
          </div>
        )}

        {state.status === "loading" && <SpinnerWithLabel label="Memuat pertanyaan..." />}
        {state.status === "error" && <ErrorState message="Gagal memuat pertanyaan." onRetry={load} />}

        {state.status === "ready" && !hasQuestions && (
          <div className="card">
            <EmptyState message="Belum ada pertanyaan wawancara untuk lowongan ini." />
          </div>
        )}

        {state.status === "ready" && hasQuestions && (
          <>
            {reopened && (
              <div className="card" style={{ background: "var(--warning-soft)", borderColor: "var(--warning)", padding: "10px 14px", marginBottom: 14 }}>
                <span style={{ fontSize: "0.8rem", color: "var(--ink-2)" }}>
                  Sedang mengedit pertanyaan yang sudah disetujui &mdash; simpan untuk mengunci ulang dan mengirim ke kandidat.
                </span>
              </div>
            )}
            {drafts.map((d, i) => {
              const duration = durationFor(d);
              const durationBusy = d.id !== null && questionDurationBusy === d.id;
              return (
                <div className="qcard" key={d.id ?? `new-${i}`}>
                  <div className="qn">Pertanyaan {i + 1}</div>
                  <textarea
                    value={d.question_text}
                    disabled={isApproved}
                    onChange={(e) => updateDraft(i, e.target.value)}
                  />
                  <div style={{ marginTop: 8, display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
                    {!isApproved && (
                      <Button variant="danger" onClick={() => removeDraft(i)} disabled={busy !== null}>
                        Hapus
                      </Button>
                    )}
                    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                      <label htmlFor={`duration-${i}`} style={{ fontSize: "0.76rem", color: "var(--muted)" }}>
                        Batas waktu:
                      </label>
                      <select
                        id={`duration-${i}`}
                        className="select-control"
                        value={duration}
                        disabled={isApproved || durationBusy}
                        onChange={(e) =>
                          d.id !== null
                            ? handleQuestionDurationChange(d.id, Number(e.target.value))
                            : updateDraftDuration(i, Number(e.target.value))
                        }
                      >
                        <option value={60}>1 menit</option>
                        <option value={120}>2 menit</option>
                        <option value={180}>3 menit</option>
                      </select>
                    </div>
                  </div>
                </div>
              );
            })}

            {actionError && <ErrorState message={actionError} onRetry={retryLastAction} />}

            {!isApproved && (
              <div style={{ marginTop: 16, display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
                <Button variant="primary" onClick={handleApprove} disabled={busy !== null}>
                  {busy === "approve" ? "Menyetujui..." : "Setujui & Kunci Pertanyaan"}
                </Button>
              </div>
            )}

          </>
        )}
      </div>

      {showGenerateModal && (
        <GenerateQuestionsModal
          existingSlots={drafts.map((d, i) => ({
            label: `Pertanyaan ${i + 1}`,
            preview: d.question_text.slice(0, 80),
            checked: d.question_text.trim() === "",
          }))}
          busy={busy === "generate"}
          progress={generateProgress}
          error={generateError}
          onCancel={() => {
            setShowGenerateModal(false);
            setGenerateError(null);
          }}
          onConfirm={handleGenerateConfirm}
        />
      )}

      {pendingNav && (
        <Modal title="Perubahan Belum Disimpan" onClose={() => (busy ? undefined : setPendingNav(null))}>
          <p>Anda memiliki perubahan pertanyaan yang belum disimpan. Simpan sekarang?</p>
          {actionError && <ErrorState message={actionError} />}
          <div className="modal-actions">
            <Button variant="ghost" onClick={handleDiscardAndNavigate} disabled={busy !== null}>
              Tidak Simpan
            </Button>
            <Button variant="primary" onClick={handleSaveAndNavigate} disabled={busy !== null}>
              {busy === "approve" ? "Menyimpan..." : "Simpan"}
            </Button>
          </div>
        </Modal>
      )}
    </div>
  );
}
