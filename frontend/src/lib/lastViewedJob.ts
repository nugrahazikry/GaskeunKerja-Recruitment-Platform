const KEY = "gaskeun_last_job_id";

/** Remembers whichever job's Kandidat/Laporan/Questions page was last viewed, so navigating away
 * (e.g. to the Lowongan list, which has no natural job context) and back doesn't silently switch
 * to a different job — see TopBar.tsx and NavRedirectPage.tsx. Without this, TopBar's Kandidat/
 * Laporan links on a job-less page had no way to know which job you actually meant, and fell back
 * to NavRedirectPage's "most recently CREATED job" guess, which is not the same thing. */
export function setLastViewedJob(jobId: number): void {
  localStorage.setItem(KEY, String(jobId));
}

export function getLastViewedJob(): number | null {
  const raw = localStorage.getItem(KEY);
  return raw ? Number(raw) : null;
}
