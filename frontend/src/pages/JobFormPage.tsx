import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Card } from "../components/Card";
import { Button } from "../components/Button";
import { TextField, TextAreaField } from "../components/FormField";
import { ErrorState } from "../components/ErrorState";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { api } from "../api/client";

type JobFields = {
  title: string;
  responsibilities: string;
  requirements: string;
  qualifications: string;
};

const EMPTY: JobFields = { title: "", responsibilities: "", requirements: "", qualifications: "" };

export function JobFormPage() {
  const navigate = useNavigate();
  const { jobId } = useParams();
  const isEdit = jobId !== undefined;

  const [fields, setFields] = useState<JobFields>(EMPTY);
  const [loading, setLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    if (!isEdit) return;
    api.GET("/jobs/{job_id}", { params: { path: { job_id: Number(jobId) } } }).then(({ data, error: apiError }) => {
      setLoading(false);
      if (apiError || !data) {
        setError("Gagal memuat lowongan.");
        return;
      }
      setFields({
        title: data.title,
        responsibilities: data.responsibilities,
        requirements: data.requirements,
        qualifications: data.qualifications,
      });
    });
  }, [isEdit, jobId]);

  function update(key: keyof JobFields, value: string) {
    setFields((f) => ({ ...f, [key]: value }));
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
    setError(null);

    const { data, error: apiError } = isEdit
      ? await api.PUT("/jobs/{job_id}", { params: { path: { job_id: Number(jobId) } }, body: fields })
      : await api.POST("/jobs", { body: fields });

    setSaving(false);
    if (apiError || !data) {
      setError("Gagal menyimpan lowongan.");
      return;
    }
    navigate("/jobs");
  }

  async function handleDelete() {
    if (!isEdit) return;
    setDeleting(true);
    const { error: apiError } = await api.DELETE("/jobs/{job_id}", { params: { path: { job_id: Number(jobId) } } });
    setDeleting(false);
    if (apiError) {
      setError("Gagal menutup lowongan.");
      return;
    }
    navigate("/jobs");
  }

  if (loading) {
    return <SpinnerWithLabel label="Memuat lowongan..." />;
  }

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", padding: "0 16px" }}>
      <Card>
        <h1>{isEdit ? "Edit Lowongan" : "Buat Lowongan"}</h1>
        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <TextField
            id="title"
            label="Judul Posisi"
            value={fields.title}
            onChange={(e) => update("title", e.target.value)}
          />
          <TextAreaField
            id="responsibilities"
            label="Tanggung Jawab"
            value={fields.responsibilities}
            onChange={(e) => update("responsibilities", e.target.value)}
          />
          <TextAreaField
            id="requirements"
            label="Persyaratan"
            value={fields.requirements}
            onChange={(e) => update("requirements", e.target.value)}
          />
          <TextAreaField
            id="qualifications"
            label="Kualifikasi"
            value={fields.qualifications}
            onChange={(e) => update("qualifications", e.target.value)}
          />

          {validationError && <ErrorState message={validationError} />}
          {error && <ErrorState message={error} />}

          <div style={{ display: "flex", gap: 12 }}>
            <Button type="submit" variant="primary" disabled={saving || deleting}>
              {saving ? "Menyimpan..." : "Simpan"}
            </Button>
            {isEdit && (
              <Button type="button" variant="danger" disabled={saving || deleting} onClick={handleDelete}>
                {deleting ? "Menutup..." : "Tutup Lowongan"}
              </Button>
            )}
          </div>
        </form>
      </Card>
    </div>
  );
}
