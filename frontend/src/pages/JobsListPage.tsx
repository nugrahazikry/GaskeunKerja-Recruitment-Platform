import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Card } from "../components/Card";
import { Button } from "../components/Button";
import { Table } from "../components/Table";
import { Badge } from "../components/Badge";
import { SkeletonLoader } from "../components/SkeletonLoader";
import { ErrorState } from "../components/ErrorState";
import { EmptyState } from "../components/EmptyState";
import { api } from "../api/client";

type Job = {
  id: number;
  company_id: number;
  title: string;
  responsibilities: string;
  requirements: string;
  qualifications: string;
  status: string;
};

type State =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; jobs: Job[] };

export function JobsListPage() {
  const [state, setState] = useState<State>({ status: "loading" });
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });
    api.GET("/jobs").then(({ data, error }) => {
      if (cancelled) return;
      if (error || !data) {
        setState({ status: "error" });
        return;
      }
      setState({ status: "ready", jobs: data });
    });
    return () => {
      cancelled = true;
    };
  }, [reloadKey]);

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", padding: "0 16px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <h1>Daftar Lowongan</h1>
        <Link to="/jobs/new">
          <Button variant="primary">+ Buat Lowongan</Button>
        </Link>
      </div>

      <Card>
        {state.status === "loading" && <SkeletonLoader rows={3} />}
        {state.status === "error" && (
          <ErrorState message="Gagal memuat daftar lowongan." onRetry={() => setReloadKey((k) => k + 1)} />
        )}
        {state.status === "ready" && state.jobs.length === 0 && (
          <EmptyState message="Belum ada lowongan. Buat lowongan pertama Anda." />
        )}
        {state.status === "ready" && state.jobs.length > 0 && (
          <Table
            columns={[
              { header: "Judul", render: (j: Job) => <Link to={`/jobs/${j.id}/edit`}>{j.title}</Link> },
              {
                header: "Status",
                render: (j: Job) => (
                  <Badge tone={j.status === "active" ? "success" : "neutral"}>
                    {j.status === "active" ? "Aktif" : "Ditutup"}
                  </Badge>
                ),
              },
            ]}
            rows={state.jobs}
            keyField={(j) => j.id}
          />
        )}
      </Card>
    </div>
  );
}
