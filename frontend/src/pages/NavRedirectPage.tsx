import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { SpinnerWithLabel } from "../components/SpinnerWithLabel";
import { EmptyState } from "../components/EmptyState";
import { TopBar } from "../components/TopBar";
import { api } from "../api/client";

type NavKey = "kandidat" | "laporan";

const DESTINATION_SUFFIX: Record<NavKey, string> = {
  kandidat: "",
  laporan: "/reports",
};

/** "Kandidat" in the top nav has no real cross-job page yet — the app's data is entirely
 * job-scoped (Shortlist, Questions). "Laporan" now has a real destination (JobReportsPage, #15
 * fix — this used to silently alias to the Shortlist page). Resolves the most recently created
 * active job and redirects to its equivalent page, rather than leaving the nav link dead on a
 * same-route no-op.
 *
 * "Wawancara" was removed entirely (2026-07-19, user-requested) — interview questions are now
 * reachable ONLY via "Kelola Pertanyaan" on the Job Detail page, not a global nav redirect. */
export function NavRedirectPage({ target }: { target: NavKey }) {
  const [jobId, setJobId] = useState<number | null | "none">(null);

  useEffect(() => {
    api.GET("/jobs").then(({ data }) => {
      if (!data || data.length === 0) {
        setJobId("none");
        return;
      }
      const active = data.filter((j) => j.status === "active");
      const pool = active.length > 0 ? active : data;
      const mostRecent = [...pool].sort(
        (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      )[0];
      setJobId(mostRecent.id);
    });
  }, []);

  if (jobId === null) {
    return (
      <div>
        <TopBar active={target} />
        <div className="main">
          <SpinnerWithLabel label="Memuat..." />
        </div>
      </div>
    );
  }

  if (jobId === "none") {
    return (
      <div>
        <TopBar active={target} />
        <div className="main">
          <EmptyState message="Belum ada lowongan. Buat lowongan terlebih dahulu untuk melihat halaman ini." />
        </div>
      </div>
    );
  }

  return <Navigate to={`/jobs/${jobId}${DESTINATION_SUFFIX[target]}`} replace />;
}
