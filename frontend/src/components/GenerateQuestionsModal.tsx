import { useState } from "react";
import { Modal } from "./Modal";
import { Button } from "./Button";
import { ErrorState } from "./ErrorState";
import { SpinnerWithLabel } from "./SpinnerWithLabel";

export type ExistingSlot = { label: string; preview: string; checked: boolean };

/** Round-3 follow-up (2026-07-19): lets HR pick exactly which question slots AI should
 * (re)generate — existing slots default UNCHECKED if already filled (so AI never clobbers
 * HR-written content by surprise) and CHECKED if empty; HR can flip any of them.
 *
 * User follow-up (2026-07-19): the "add N new slots" stepper was removed from this modal — that's
 * "+ Tambah Pertanyaan"'s job (a separate, already-existing action), so this modal now does exactly
 * one thing: regenerate the checked slots. When there are no existing questions yet, a plain count
 * picker (1-5) replaces the checkbox list for the initial from-scratch generation. */
export function GenerateQuestionsModal({
  existingSlots,
  busy,
  progress,
  error,
  onCancel,
  onConfirm,
}: {
  existingSlots: ExistingSlot[];
  busy: boolean;
  progress?: { current: number; total: number } | null;
  error?: string | null;
  onCancel: () => void;
  onConfirm: (regenerateIndexes: number[], fromScratchCount: number) => void;
}) {
  const [checked, setChecked] = useState<boolean[]>(existingSlots.map((s) => s.checked));
  const [fromScratchCount, setFromScratchCount] = useState(3);

  const hasExisting = existingSlots.length > 0;
  const total = hasExisting ? checked.filter(Boolean).length : fromScratchCount;

  function toggle(i: number) {
    setChecked((c) => c.map((v, idx) => (idx === i ? !v : v)));
  }

  // Round-3 follow-up (2026-07-19): the modal must not be dismissible (backdrop click, "×", or
  // "Batal") while a generate call is in flight — closing early left the busy/disabled state on
  // the page's own buttons lingering with no visible indication anything was still happening,
  // which read as "the pop-up closed before the AI question was actually created."
  const handleClose = busy ? () => {} : onCancel;

  return (
    <Modal title="Buat Pertanyaan (AI)" onClose={handleClose}>
      {busy ? (
        <div style={{ padding: "24px 0" }}>
          <SpinnerWithLabel
            label={
              progress
                ? `AI sedang membuat pertanyaan ${progress.current} dari ${progress.total}...`
                : "AI sedang membuat pertanyaan..."
            }
          />
        </div>
      ) : (
        <>
          {hasExisting ? (
            <>
              <p className="hint" style={{ marginBottom: 8 }}>
                Pilih pertanyaan mana yang ingin dibuat ulang oleh AI. Yang tidak dicentang akan tetap seperti sekarang.
              </p>
              <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 12 }}>
                {existingSlots.map((slot, i) => (
                  <label key={i} style={{ display: "flex", alignItems: "flex-start", gap: 8, fontSize: "0.84rem" }}>
                    <input type="checkbox" checked={checked[i]} onChange={() => toggle(i)} style={{ marginTop: 3 }} />
                    <span>
                      <strong>{slot.label}</strong>
                      <br />
                      <span style={{ color: "var(--muted)" }}>{slot.preview || "(kosong)"}</span>
                    </span>
                  </label>
                ))}
              </div>
            </>
          ) : (
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 4 }}>
              <label htmlFor="from-scratch-count" style={{ fontSize: "0.84rem", fontWeight: 700 }}>
                Jumlah pertanyaan:
              </label>
              <select
                id="from-scratch-count"
                className="select-control"
                value={fromScratchCount}
                onChange={(e) => setFromScratchCount(Number(e.target.value))}
              >
                {[1, 2, 3, 4, 5].map((n) => (
                  <option key={n} value={n}>
                    {n}
                  </option>
                ))}
              </select>
            </div>
          )}

          {error && <ErrorState message={error} />}
        </>
      )}

      <div className="modal-actions">
        <Button variant="ghost" onClick={onCancel} disabled={busy}>
          Batal
        </Button>
        <Button
          variant="primary"
          disabled={busy || total === 0}
          onClick={() =>
            onConfirm(hasExisting ? checked.flatMap((c, i) => (c ? [i] : [])) : [], hasExisting ? 0 : fromScratchCount)
          }
        >
          {busy ? "Membuat..." : `Buat ${total} Pertanyaan dengan AI`}
        </Button>
      </div>
    </Modal>
  );
}
