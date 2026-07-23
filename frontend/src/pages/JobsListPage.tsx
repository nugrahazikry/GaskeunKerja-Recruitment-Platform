import { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { TopBar } from "../components/TopBar";
import { Button } from "../components/Button";
import { Table } from "../components/Table";
import { Badge } from "../components/Badge";
import { TextField } from "../components/FormField";
import { BulletListField } from "../components/BulletListField";
import { SkeletonLoader } from "../components/SkeletonLoader";
import { ErrorState } from "../components/ErrorState";
import { EmptyState } from "../components/EmptyState";
import { Modal } from "../components/Modal";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { CompetencyEditor } from "../components/CompetencyEditor";
import { ColorPanel } from "../components/ColorPanel";
import { api } from "../api/client";
import { formatRelativeTime } from "../lib/formatRelativeTime";

type Job = {
  id: number;
  company_id: number;
  company_name: string;
  title: string;
  responsibilities: string;
  requirements: string;
  qualifications: string;
  status: string;
  created_at: string;
  candidate_count: number;
  question_status: "none" | "draft" | "approved";
  belum_diundang: number;
  menunggu_wawancara: number;
  selesai_wawancara: number;
  diputuskan: number;
};

type ListState =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; jobs: Job[] };

type JobFields = {
  title: string;
  responsibilities: string;
  requirements: string;
  qualifications: string;
};

const EMPTY: JobFields = { title: "", responsibilities: "", requirements: "", qualifications: "" };

export function JobsListPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { jobId } = useParams();
  const isEdit = jobId !== undefined;

  const [listState, setListState] = useState<ListState>({ status: "loading" });
  const [reloadKey, setReloadKey] = useState(0);

  const [fields, setFields] = useState<JobFields>(EMPTY);
  // Round-3 follow-up #10 (2026-07-19): baseline snapshot of the last SAVED/LOADED field values —
  // compared against `fields` to detect unsaved edits, same "isDirty" pattern already built for
  // QuestionsPage.tsx's draft-questions guard.
  const [savedFields, setSavedFields] = useState<JobFields>(EMPTY);
  const [pendingNav, setPendingNav] = useState<(() => void) | null>(null);
  const [formLoading, setFormLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [savingStage, setSavingStage] = useState<null | "saving" | "extracting">(null);
  const [reviewJobId, setReviewJobId] = useState<number | null>(null);
  const [cancelingReview, setCancelingReview] = useState(false);
  const [hardDeleteModalOpen, setHardDeleteModalOpen] = useState(false);
  const [hardDeleteConfirmText, setHardDeleteConfirmText] = useState("");
  const [hardDeleting, setHardDeleting] = useState(false);
  const [hardDeleteError, setHardDeleteError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<null | "active" | "closed">(null);

  useEffect(() => {
    let cancelled = false;
    setListState({ status: "loading" });
    api.GET("/jobs").then(({ data, error }) => {
      if (cancelled) return;
      if (error || !data) {
        setListState({ status: "error" });
        return;
      }
      setListState({ status: "ready", jobs: data });
    });
    return () => {
      cancelled = true;
    };
  }, [reloadKey]);

  useEffect(() => {
    if (!isEdit) {
      setFields(EMPTY);
      setSavedFields(EMPTY);
      setFormLoading(false);
      return;
    }
    setFormLoading(true);
    api.GET("/jobs/{job_id}", { params: { path: { job_id: Number(jobId) } } }).then(({ data, error: apiError }) => {
      setFormLoading(false);
      if (apiError || !data) {
        setFormError("Gagal memuat lowongan.");
        return;
      }
      const loaded = {
        title: data.title,
        responsibilities: data.responsibilities,
        requirements: data.requirements,
        qualifications: data.qualifications,
      };
      setFields(loaded);
      setSavedFields(loaded);
    });
  }, [isEdit, jobId]);

  function update(key: keyof JobFields, value: string) {
    setFields((f) => ({ ...f, [key]: value }));
  }

  const isDirty = JSON.stringify(fields) !== JSON.stringify(savedFields);

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

  function handleLeaveWithoutSaving() {
    const go = pendingNav;
    setPendingNav(null);
    go?.();
  }

  function validate(): boolean {
    if (!fields.title.trim()) {
      setValidationError("Judul wajib diisi.");
      return false;
    }
    if (!fields.responsibilities.trim() && !fields.requirements.trim()) {
      setValidationError("Isi minimal salah satu: Tanggung Jawab atau Persyaratan.");
      return false;
    }
    setValidationError(null);
    return true;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!validate()) return;
    setSaving(true);
    setFormError(null);
    setSavingStage("saving");

    // UX-only staged label, not real backend phase tracking — save + extract is one atomic
    // backend call, this just gives visible feedback during the wait instead of a blank pause.
    // Round-3 follow-up #9 (2026-07-19): editing an EXISTING job no longer re-extracts
    // competencies at all (see below + backend's update_job) — the "extracting" stage would be
    // misleading here, so it only fires for a fresh create.
    const stageTimer = isEdit ? null : setTimeout(() => setSavingStage("extracting"), 900);

    const { data, error: apiError } = isEdit
      ? await api.PUT("/jobs/{job_id}", { params: { path: { job_id: Number(jobId) } }, body: fields })
      : await api.POST("/jobs", { body: fields });

    if (stageTimer) clearTimeout(stageTimer);
    setSaving(false);
    setSavingStage(null);
    if (apiError || !data) {
      setFormError("Gagal menyimpan lowongan.");
      return;
    }
    setReloadKey((k) => k + 1);
    // Round-3 follow-up #9: the "Tinjau Kompetensi Wajib" review modal (full add/dismiss/restore
    // editing) is now ONLY shown right after a fresh CREATE — an existing job's competencies are
    // locked once candidates may already be scored against them (see JobDetailPage.tsx, which no
    // longer offers any competency-edit entry point at all). Editing a job's text fields no longer
    // reopens this modal or touches competencies.
    if (!isEdit) {
      // Round-3 follow-up #10 (2026-07-19, corrected — first attempt navigated to /edit
      // immediately, which the user explicitly did NOT want: closing the review modal via X
      // should return to THIS form exactly as it was, not jump to the Edit Lowongan page.
      // Navigation to /edit now only happens from the modal's "Selesai" button below. The
      // earlier bug (blank form after X) is fixed differently here: `fields` is simply left as
      // the just-submitted values (never cleared), and `savedFields` is synced to match so the
      // form isn't flagged dirty — closing the modal reveals the same filled form, unchanged.
      setSavedFields(fields);
      setReviewJobId(data.id);
    } else {
      setSavedFields(fields);
    }
  }

  // Round-3 follow-up #10 (2026-07-19, round 3 — user clarified the actual requirement): a job
  // must only really "exist" (show up in the jobs list, count as created) once the user explicitly
  // finishes the competency review via "Selesai" — closing via X means they're backing out of the
  // whole creation, not just dismissing a summary screen. The backend has no "draft" job state, so
  // the only correct way to honor this is to actually roll the creation back: X hard-deletes the
  // job that was just created (reusing the same DELETE /jobs/{id}/permanent endpoint as the
  // Job Detail page's "Hapus Permanen" — safe here since a brand-new job has zero candidates/
  // competency edits to lose). The form stays on-screen with the same filled values afterward, so
  // the user can just click "Simpan & Ekstrak Kompetensi" again if they didn't actually mean to quit.
  async function handleCancelReview() {
    if (reviewJobId === null) return;
    setCancelingReview(true);
    await api.DELETE("/jobs/{job_id}/permanent", { params: { path: { job_id: reviewJobId } } });
    setCancelingReview(false);
    setReviewJobId(null);
    setReloadKey((k) => k + 1);
  }

  async function handleDelete() {
    if (!isEdit) return;
    setDeleting(true);
    const { error: apiError } = await api.DELETE("/jobs/{job_id}", { params: { path: { job_id: Number(jobId) } } });
    setDeleting(false);
    if (apiError) {
      setFormError("Gagal menutup lowongan.");
      return;
    }
    setReloadKey((k) => k + 1);
    navigate("/jobs");
  }

  async function handleHardDelete() {
    if (!isEdit) return;
    setHardDeleting(true);
    setHardDeleteError(null);
    const { error: apiError } = await api.DELETE("/jobs/{job_id}/permanent", {
      params: { path: { job_id: Number(jobId) } },
    });
    setHardDeleting(false);
    if (apiError) {
      setHardDeleteError("Gagal menghapus lowongan secara permanen.");
      return;
    }
    setHardDeleteModalOpen(false);
    // Navigating from /jobs/{id}/edit to /jobs stays on the same JobsListPage component instance
    // (React Router doesn't remount it), and the jobs-list fetch effect only re-runs when
    // reloadKey changes — without this, the just-deleted job kept showing in the stale list until
    // some unrelated reload happened, and clicking it 404'd ("Gagal memuat") since it was already
    // gone from the DB. Same fix pattern already used by the soft-close handler above.
    setReloadKey((k) => k + 1);
    navigate("/jobs");
  }

  const isFormMode = isEdit || location.pathname === "/jobs/new";

  const activeCount = listState.status === "ready" ? listState.jobs.filter((j) => j.status === "active").length : 0;
  const closedCount = listState.status === "ready" ? listState.jobs.filter((j) => j.status !== "active").length : 0;

  function questionStatusPill(status: Job["question_status"]) {
    if (status === "approved") return <Badge tone="info">Disetujui</Badge>;
    if (status === "draft") return <Badge tone="warning">Draf</Badge>;
    return <Badge tone="neutral">Belum dibuat</Badge>;
  }

  const filteredJobs =
    listState.status === "ready"
      ? listState.jobs.filter((j) => {
          if (statusFilter === "active") return j.status === "active";
          if (statusFilter === "closed") return j.status !== "active";
          return true;
        })
      : [];

  const jobsTable = listState.status === "ready" && listState.jobs.length > 0 && (
    <Table
      columns={[
        {
          header: "Judul",
          render: (j: Job) => (
            <strong>
              <a href={`/jobs/${j.id}/detail`} onClick={(e) => { e.preventDefault(); navigate(`/jobs/${j.id}/detail`); }}>
                {j.title}
              </a>
            </strong>
          ),
        },
        {
          header: "Status",
          render: (j: Job) => (
            <Badge tone={j.status === "active" ? "success" : "neutral"}>
              {j.status === "active" ? "Aktif" : "Ditutup"}
            </Badge>
          ),
        },
        {
          header: "Dibuat",
          render: (j: Job) => (
            <span style={{ color: "var(--muted)" }}>{formatRelativeTime(j.created_at)}</span>
          ),
        },
        {
          header: "Kandidat",
          render: (j: Job) => j.candidate_count,
        },
        {
          header: "Pertanyaan",
          render: (j: Job) => questionStatusPill(j.question_status),
        },
        {
          header: "",
          render: (j: Job) => (
            <a href={`/jobs/${j.id}/edit`} onClick={(e) => { e.preventDefault(); navigate(`/jobs/${j.id}/edit`); }}>
              <Button variant="ghost">Edit</Button>
            </a>
          ),
        },
      ]}
      rows={filteredJobs}
      keyField={(j) => j.id}
    />
  );

  if (isFormMode) {
    return (
      <div>
        <TopBar active="lowongan" interceptNav={(href) => guardedNavigate(() => navigate(href))} />
        <div className="main wide">
          <div className="pagehead">
            <h1>{isEdit ? `Edit Lowongan · ${fields.title || "..."}` : "Lowongan Baru"}</h1>
            <p>
              {listState.status === "ready" && listState.jobs.length > 0
                ? listState.jobs[0].company_name
                : "Kelola deskripsi pekerjaan perusahaan Anda"}
              {isEdit ? " · ubah deskripsi pekerjaan ini" : " · buat deskripsi pekerjaan baru"}
            </p>
          </div>

          {listState.status === "ready" && listState.jobs.length > 0 && (
            <div className="card" style={{ padding: "10px 16px", marginBottom: 14 }}>
              <Table
                columns={[
                  {
                    header: "Judul",
                    render: (j: Job) => (
                      <strong style={j.id === Number(jobId) ? { color: "var(--teal)" } : undefined}>
                        {j.title}
                        {j.id === Number(jobId) && " · sedang diedit"}
                      </strong>
                    ),
                  },
                  {
                    header: "Status",
                    render: (j: Job) => (
                      <Badge tone={j.status === "active" ? "success" : "neutral"}>
                        {j.status === "active" ? "Aktif" : "Ditutup"}
                      </Badge>
                    ),
                  },
                  {
                    header: "Dibuat",
                    render: (j: Job) => (
                      <span style={{ color: "var(--muted)" }}>{formatRelativeTime(j.created_at)}</span>
                    ),
                  },
                ]}
                rows={listState.jobs}
                keyField={(j) => j.id}
              />
            </div>
          )}

          <div className="card">
            <div className="serif" style={{ fontWeight: 700, marginBottom: 12 }}>
              Formulir Lowongan
            </div>
            {formLoading ? (
              <SkeletonLoader rows={3} />
            ) : (
              <form onSubmit={handleSubmit}>
                <ColorPanel tone="teal" title="Judul Posisi">
                  <TextField
                    id="title"
                    label="Judul Posisi"
                    hideLabel
                    value={fields.title}
                    onChange={(e) => update("title", e.target.value)}
                  />
                </ColorPanel>
                <ColorPanel tone="teal" title="Tanggung Jawab">
                  <BulletListField
                    label="Tanggung Jawab"
                    hideLabel
                    value={fields.responsibilities}
                    onChange={(v) => update("responsibilities", v)}
                  />
                </ColorPanel>
                <ColorPanel tone="success" title="Persyaratan Tambahan">
                  <BulletListField
                    label="Persyaratan Tambahan"
                    hideLabel
                    hint="Field ini digunakan AI untuk mengekstrak kompetensi wajib secara otomatis."
                    value={fields.requirements}
                    onChange={(v) => update("requirements", v)}
                  />
                </ColorPanel>
                <ColorPanel tone="gold" title="Kualifikasi">
                  <BulletListField
                    label="Kualifikasi"
                    hideLabel
                    value={fields.qualifications}
                    onChange={(v) => update("qualifications", v)}
                  />
                </ColorPanel>

                {validationError && <ErrorState message={validationError} />}
                {formError && <ErrorState message={formError} />}

                <div style={{ display: "flex", gap: 10, marginTop: 4 }}>
                  <Button type="submit" variant="primary" disabled={saving || deleting}>
                    {saving ? "Menyimpan..." : isEdit ? "Simpan Perubahan" : "Simpan & Ekstrak Kompetensi"}
                  </Button>
                  <Button
                    type="button"
                    variant="ghost"
                    disabled={saving || deleting}
                    onClick={() => guardedNavigate(() => navigate(isEdit ? `/jobs/${jobId}/detail` : "/jobs"))}
                  >
                    Batal
                  </Button>
                  {isEdit && (
                    <Button type="button" variant="ghost" disabled={saving || deleting} onClick={handleDelete}>
                      {deleting ? "Menutup..." : "Tutup Lowongan"}
                    </Button>
                  )}
                  {isEdit && (
                    <Button
                      type="button"
                      variant="danger"
                      disabled={saving || deleting}
                      onClick={() => {
                        setHardDeleteConfirmText("");
                        setHardDeleteError(null);
                        setHardDeleteModalOpen(true);
                      }}
                    >
                      Hapus Permanen
                    </Button>
                  )}
                </div>
              </form>
            )}
          </div>
        </div>

        {hardDeleteModalOpen && (
          <Modal title="Hapus Lowongan Permanen" onClose={() => setHardDeleteModalOpen(false)}>
            <p style={{ fontSize: "0.86rem", color: "var(--ink-2)", lineHeight: 1.6 }}>
              Tindakan ini <strong>tidak dapat dibatalkan</strong>. Semua kandidat, jawaban wawancara, skor, dan
              keputusan untuk lowongan <strong>{fields.title}</strong> akan dihapus permanen dari database dan
              penyimpanan berkas — termasuk riwayat audit.
            </p>
            <p className="hint" style={{ marginTop: 10 }}>
              Ketik judul lowongan di atas untuk konfirmasi:
            </p>
            <input
              type="text"
              value={hardDeleteConfirmText}
              onChange={(e) => setHardDeleteConfirmText(e.target.value)}
              placeholder={fields.title}
              style={{
                width: "100%",
                border: "1px solid var(--border)",
                borderRadius: "var(--radius-sm)",
                padding: "8px 10px",
                fontSize: "0.84rem",
                marginTop: 6,
              }}
            />
            {hardDeleteError && <ErrorState message={hardDeleteError} onRetry={handleHardDelete} />}
            <div className="modal-actions" style={{ marginTop: 14 }}>
              <Button variant="ghost" onClick={() => setHardDeleteModalOpen(false)}>
                Batal
              </Button>
              <Button
                variant="danger"
                disabled={hardDeleteConfirmText.trim() !== fields.title.trim() || hardDeleting}
                onClick={handleHardDelete}
              >
                {hardDeleting ? "Menghapus..." : "Hapus Permanen"}
              </Button>
            </div>
          </Modal>
        )}

        {savingStage && (
          <Modal title="Menyimpan Lowongan" onClose={() => {}}>
            <SpinnerWithLabel
              layout="stacked"
              label={
                savingStage === "saving"
                  ? "Menyimpan data lowongan..."
                  : "Mengekstrak kompetensi wajib dengan AI..."
              }
            />
          </Modal>
        )}

        {reviewJobId !== null && (
          <Modal
            title="Tinjau Kompetensi Wajib"
            onClose={() => (cancelingReview ? undefined : handleCancelReview())}
            dismissOnBackdropClick={false}
          >
            {cancelingReview ? (
              <SpinnerWithLabel label="Membatalkan pembuatan lowongan..." />
            ) : (
              <CompetencyEditor
                jobId={reviewJobId}
                onDone={() => {
                  const doneJobId = reviewJobId;
                  setReviewJobId(null);
                  // Round-3 follow-up #10: "Selesai" is the explicit completion action — takes the
                  // user into the job's Edit Lowongan view. Closing via X (onClose above) does NOT
                  // navigate anywhere; it hard-deletes the just-created job and returns to this
                  // same (still-filled) form instead.
                  navigate(`/jobs/${doneJobId}/edit`);
                }}
              />
            )}
          </Modal>
        )}

        {pendingNav && (
          <Modal title="Perubahan Belum Disimpan" onClose={() => setPendingNav(null)}>
            <p style={{ fontSize: "0.86rem", color: "var(--ink-2)", lineHeight: 1.6 }}>
              Anda memiliki perubahan pada formulir lowongan yang belum disimpan. Jika Anda
              melanjutkan ke halaman lain sekarang, perubahan tersebut akan hilang.
            </p>
            <div className="modal-actions">
              <Button variant="ghost" onClick={() => setPendingNav(null)}>
                Lanjutkan Mengisi
              </Button>
              <Button variant="danger" onClick={handleLeaveWithoutSaving}>
                Keluar Tanpa Menyimpan
              </Button>
            </div>
          </Modal>
        )}
      </div>
    );
  }

  return (
    <div>
      <TopBar active="lowongan" />
      <div className="main wide">
        <div className="pagehead">
          <h1>Lowongan</h1>
          <p>
            {listState.status === "ready" && listState.jobs.length > 0
              ? listState.jobs[0].company_name
              : "Kelola deskripsi pekerjaan perusahaan Anda"}
            {" · kelola deskripsi pekerjaan"}
          </p>
        </div>

        {listState.status === "ready" && listState.jobs.length > 0 && (
          <div className="stat-grid" style={{ gridTemplateColumns: "repeat(3, 1fr)" }}>
            <div
              className="stat-tile"
              style={{ cursor: "pointer", outline: statusFilter === null ? "2px solid var(--teal)" : undefined }}
              onClick={() => setStatusFilter(null)}
              title="Tampilkan semua lowongan"
            >
              <div className="stat-num">{listState.jobs.length}</div>
              <div className="stat-label">Total Lowongan</div>
            </div>
            <div
              className="stat-tile"
              style={{ cursor: "pointer", outline: statusFilter === "active" ? "2px solid var(--teal)" : undefined }}
              onClick={() => setStatusFilter(statusFilter === "active" ? null : "active")}
              title="Filter: lowongan aktif"
            >
              <div className="stat-num">{activeCount}</div>
              <div className="stat-label">Aktif</div>
            </div>
            <div
              className="stat-tile"
              style={{ cursor: "pointer", outline: statusFilter === "closed" ? "2px solid var(--teal)" : undefined }}
              onClick={() => setStatusFilter(statusFilter === "closed" ? null : "closed")}
              title="Filter: lowongan ditutup"
            >
              <div className="stat-num">{closedCount}</div>
              <div className="stat-label">Ditutup</div>
            </div>
          </div>
        )}

        {listState.status === "ready" && listState.jobs.length > 0 && (
          <div className="card chart-card" style={{ marginBottom: 16 }}>
            <h3>Alur Kandidat per Lowongan</h3>
            <p className="chart-sub">Sebaran tahap kandidat di tiap lowongan</p>
            {filteredJobs.length === 0 ? (
              <EmptyState message="Tidak ada lowongan dengan status ini." />
            ) : (
              (() => {
                const withTotals = filteredJobs.map((j) => ({
                  job: j,
                  total: j.belum_diundang + j.menunggu_wawancara + j.selesai_wawancara + j.diputuskan,
                }));
                return (
                  <>
                    {[...withTotals]
                      .sort((a, b) => b.total - a.total)
                      .map(({ job: j, total }) => {
                        const segments: [string, number, string][] = [
                          ["s1", j.belum_diundang, "Belum Diundang"],
                          ["s2", j.menunggu_wawancara, "Menunggu Wawancara"],
                          ["s3", j.selesai_wawancara, "Selesai Wawancara"],
                          ["s4", j.diputuskan, "Sudah Diputuskan"],
                        ];
                        return (
                          <div
                            key={j.id}
                            className="lightable"
                            style={{ marginBottom: 16, cursor: "pointer" }}
                            onClick={() => navigate(`/jobs/${j.id}/detail`)}
                          >
                            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.8rem", marginBottom: 5 }}>
                              <strong>{j.title}</strong>
                              <span style={{ color: "var(--muted)" }}>{total} kandidat</span>
                            </div>
                            <div className="pipeline-track" style={{ height: 20 }}>
                              {total === 0 ? (
                                <div className="pseg s1" style={{ flex: 1 }} />
                              ) : (
                                segments.map(([cls, count, label]) =>
                                  count > 0 ? (
                                    <div key={cls} className="pseg-wrap" style={{ flex: count }} data-tooltip={`${label}: ${count} kandidat`}>
                                      <div className={`pseg ${cls}`}>{count}</div>
                                    </div>
                                  ) : null
                                )
                              )}
                            </div>
                          </div>
                        );
                      })}
                    <div className="dec-legend" style={{ marginTop: 6 }}>
                      <span>
                        <i style={{ background: "var(--border)" }} />
                        Belum Diundang
                      </span>
                      <span>
                        <i style={{ background: "var(--gold)" }} />
                        Menunggu Wawancara
                      </span>
                      <span>
                        <i style={{ background: "var(--teal)" }} />
                        Selesai Wawancara
                      </span>
                      <span>
                        <i style={{ background: "var(--success)" }} />
                        Sudah Diputuskan
                      </span>
                    </div>
                  </>
                );
              })()
            )}
          </div>
        )}

        <div className="card">
          {listState.status === "loading" && <SkeletonLoader rows={3} />}
          {listState.status === "error" && (
            <ErrorState message="Gagal memuat daftar lowongan." onRetry={() => setReloadKey((k) => k + 1)} />
          )}
          {listState.status === "ready" && listState.jobs.length === 0 && (
            <EmptyState message="Belum ada lowongan. Buat lowongan pertama Anda." />
          )}
          {listState.status === "ready" && listState.jobs.length > 0 && filteredJobs.length === 0 && (
            <EmptyState message="Tidak ada lowongan dengan status ini." />
          )}
          {filteredJobs.length > 0 && jobsTable}
        </div>

        <Button variant="secondary" onClick={() => navigate("/jobs/new")}>
          + Lowongan Baru
        </Button>
      </div>
    </div>
  );
}
