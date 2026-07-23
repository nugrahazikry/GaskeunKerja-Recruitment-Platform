import { useEffect, useState, type MouseEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { clearHrToken } from "../api/client";
import { getLastViewedJob, setLastViewedJob } from "../lib/lastViewedJob";

type NavKey = "dashboard" | "lowongan" | "kandidat" | "wawancara" | "laporan";

/** jobId, when provided (i.e. TopBar is rendered from inside a /jobs/:jobId/* page),
 * keeps Kandidat/Wawancara/Laporan scoped to THAT job instead of jumping to whichever
 * job NavRedirectPage's global "most recent" lookup would otherwise pick — clicking the
 * nav while looking at one job's data should never silently switch you to a different job. */
export function TopBar({
  active,
  jobId,
  hrInitials = "HR",
  interceptNav,
}: {
  active: NavKey;
  jobId?: number;
  hrInitials?: string;
  // Optional: when provided, clicking the brand/nav links calls this with the link's target
  // instead of navigating directly — lets a page with unsaved edits (e.g. QuestionsPage) show its
  // own confirm-before-leaving modal for every way to navigate away, not just an in-page button.
  interceptNav?: (href: string) => void;
}) {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    if (jobId !== undefined) setLastViewedJob(jobId);
  }, [jobId]);

  const fallbackJobId = jobId ?? getLastViewedJob();

  function navLinkProps(href: string) {
    if (!interceptNav) return { to: href };
    return {
      to: href,
      onClick: (e: MouseEvent) => {
        e.preventDefault();
        interceptNav(href);
      },
    };
  }

  function handleLogout() {
    clearHrToken();
    navigate("/login");
  }

  // Round-3 follow-up (2026-07-19, user-requested): "Wawancara" removed from the top nav entirely
  // — interview questions are now reachable ONLY via "Kelola Pertanyaan" on the Job Detail page,
  // never a global nav link (see App.tsx: the /interviews redirect route was removed too).
  //
  // Round 11 follow-up (real bug): a page with no natural job context (e.g. the Lowongan list)
  // used to link Kandidat/Laporan to the generic /candidates and /reports redirect routes, which
  // pick the most recently CREATED active job — not the one you were actually just looking at.
  // fallbackJobId (last-viewed, from localStorage) makes those links point straight at the real
  // job whenever we know one, so leaving and coming back never silently switches jobs.
  const navItems: { key: NavKey; label: string; href: string }[] = fallbackJobId
    ? [
        { key: "dashboard", label: "Dashboard", href: "/dashboard" },
        { key: "lowongan", label: "Lowongan", href: "/jobs" },
        { key: "kandidat", label: "Kandidat", href: `/jobs/${fallbackJobId}` },
        { key: "laporan", label: "Laporan", href: `/jobs/${fallbackJobId}/reports` },
      ]
    : [
        { key: "dashboard", label: "Dashboard", href: "/dashboard" },
        { key: "lowongan", label: "Lowongan", href: "/jobs" },
        { key: "kandidat", label: "Kandidat", href: "/candidates" },
        { key: "laporan", label: "Laporan", href: "/reports" },
      ];

  return (
    <div className="topbar">
      <Link className="brand" {...navLinkProps("/dashboard")}>
        Gaskeun<span>Kerja</span> for Business
      </Link>
      <div className="nav">
        {navItems.map((item) => (
          <Link key={item.key} className={item.key === active ? "on" : ""} {...navLinkProps(item.href)}>
            {item.label}
          </Link>
        ))}
      </div>
      <div style={{ position: "relative" }}>
        <button
          className="hr-avatar"
          style={{ border: "none", cursor: "pointer" }}
          onClick={() => setMenuOpen((v) => !v)}
        >
          {hrInitials}
        </button>
        {menuOpen && (
          <>
            <div
              style={{ position: "fixed", inset: 0, zIndex: 10 }}
              onClick={() => setMenuOpen(false)}
            />
            <div
              className="card"
              style={{
                position: "absolute",
                right: 0,
                top: "calc(100% + 8px)",
                padding: "6px",
                minWidth: 140,
                zIndex: 20,
                marginBottom: 0,
              }}
            >
              <button
                onClick={handleLogout}
                style={{
                  width: "100%",
                  textAlign: "left",
                  background: "none",
                  border: "none",
                  padding: "8px 10px",
                  fontSize: "0.82rem",
                  fontWeight: 600,
                  color: "var(--danger)",
                  cursor: "pointer",
                  borderRadius: 4,
                }}
              >
                Keluar
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
