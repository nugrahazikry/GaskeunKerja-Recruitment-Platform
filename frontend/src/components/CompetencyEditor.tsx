import { useEffect, useState } from "react";
import { Button } from "./Button";
import { SpinnerWithLabel } from "./SpinnerWithLabel";
import { ErrorState } from "./ErrorState";
import { api } from "../api/client";
import "./CompetencyEditor.css";

type Competency = {
  id: number;
  competency_name: string;
  importance_level: number;
  status: string;
  source: string;
};

/** Shared review/edit panel for a job's required competencies (#4, #7): dismiss (moves to a
 * restorable "recommended" pool, never deletes), add a custom one, restore from the pool. Used
 * both right after job save (inside a Modal, B2) and inline on Job Detail (B3). */
export function CompetencyEditor({ jobId, onDone }: { jobId: number; onDone?: () => void }) {
  const [active, setActive] = useState<Competency[] | null>(null);
  const [dismissed, setDismissed] = useState<Competency[]>([]);
  const [showRecommended, setShowRecommended] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<number | null>(null);
  const [newName, setNewName] = useState("");
  const [adding, setAdding] = useState(false);

  function load() {
    setError(null);
    api
      .GET("/jobs/{job_id}/competencies", {
        params: { path: { job_id: jobId }, query: { include_dismissed: true } },
      })
      .then(({ data, error: apiError }) => {
        if (apiError || !data) {
          setError("Gagal memuat kompetensi.");
          return;
        }
        setActive(data.filter((c) => c.status === "active"));
        // Recommended pool only ever resurfaces AI-suggested competencies — a dismissed custom
        // one (something the HR typed in themselves, then removed) was a mistake, not a
        // recommendation, so it's excluded here even though the row still exists in the DB.
        setDismissed(data.filter((c) => c.status === "dismissed" && c.source === "ai"));
      });
  }

  useEffect(load, [jobId]);

  async function handleDismiss(id: number) {
    setBusyId(id);
    const { error: apiError } = await api.POST("/jobs/{job_id}/competencies/{competency_id}/dismiss", {
      params: { path: { job_id: jobId, competency_id: id } },
    });
    setBusyId(null);
    if (apiError) {
      setError("Gagal menghapus kompetensi.");
      return;
    }
    load();
  }

  async function handleRestore(id: number) {
    setBusyId(id);
    const { error: apiError } = await api.POST("/jobs/{job_id}/competencies/{competency_id}/restore", {
      params: { path: { job_id: jobId, competency_id: id } },
    });
    setBusyId(null);
    if (apiError) {
      setError(
        (apiError as { detail?: string })?.detail ??
          "Gagal memulihkan kompetensi. Mungkin sudah ada kompetensi aktif dengan nama yang sama."
      );
      return;
    }
    load();
  }

  async function handleAdd() {
    if (!newName.trim()) return;
    setAdding(true);
    const { error: apiError } = await api.POST("/jobs/{job_id}/competencies", {
      params: { path: { job_id: jobId } },
      body: { competency_name: newName.trim(), importance_level: 1.0 },
    });
    setAdding(false);
    if (apiError) {
      setError(
        (apiError as { detail?: string })?.detail ??
          "Gagal menambah kompetensi. Mungkin sudah ada kompetensi aktif dengan nama yang sama."
      );
      return;
    }
    setNewName("");
    load();
  }

  if (active === null) {
    return error ? <ErrorState message={error} onRetry={load} /> : <SpinnerWithLabel label="Memuat kompetensi..." />;
  }

  return (
    <div className="competency-editor">
      <p className="hint">
        Tinjau kompetensi wajib yang diekstrak AI. Hapus yang tidak relevan, atau tambahkan sendiri —
        kompetensi yang dihapus tidak hilang, hanya dipindah ke daftar rekomendasi di bawah.
      </p>
      <p className="comp-lock-notice">
        <strong>Peninjauan ini hanya dapat dilakukan satu kali.</strong> Kompetensi yang dikonfirmasi
        di sini akan menjadi acuan tetap untuk seluruh proses analisis kesenjangan keahlian dan
        penilaian kandidat pada lowongan ini, serta tidak dapat diubah kembali setelah lowongan
        disimpan.
      </p>
      {error && <ErrorState message={error} onRetry={load} />}

      <div className="comp-chip-row">
        {active.length === 0 && <span className="hint">Belum ada kompetensi aktif.</span>}
        {active.map((c) => (
          <span className="comp-chip" key={c.id}>
            {c.competency_name}
            <button
              type="button"
              className="comp-chip-remove"
              onClick={() => handleDismiss(c.id)}
              disabled={busyId === c.id}
              aria-label={`Hapus ${c.competency_name}`}
            >
              &times;
            </button>
          </span>
        ))}
      </div>

      <div className="comp-add-row">
        <input
          type="text"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="Tambah kompetensi..."
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              handleAdd();
            }
          }}
        />
        <Button type="button" variant="ghost" onClick={handleAdd} disabled={adding || !newName.trim()}>
          {adding ? "Menambah..." : "+ Tambah"}
        </Button>
      </div>

      {dismissed.length > 0 && (
        <div className="comp-recommended">
          <button type="button" className="comp-recommended-toggle" onClick={() => setShowRecommended((s) => !s)}>
            {showRecommended ? "Sembunyikan" : "Lihat"} Rekomendasi ({dismissed.length})
          </button>
          {showRecommended && (
            <div className="comp-chip-row">
              {dismissed.map((c) => (
                <span className="comp-chip comp-chip-dismissed" key={c.id}>
                  {c.competency_name}
                  <button
                    type="button"
                    className="comp-chip-restore"
                    onClick={() => handleRestore(c.id)}
                    disabled={busyId === c.id}
                    aria-label={`Pulihkan ${c.competency_name}`}
                  >
                    +
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {onDone && (
        <div className="modal-actions" style={{ marginTop: 14 }}>
          <Button variant="primary" onClick={onDone}>
            Selesai
          </Button>
        </div>
      )}
    </div>
  );
}
