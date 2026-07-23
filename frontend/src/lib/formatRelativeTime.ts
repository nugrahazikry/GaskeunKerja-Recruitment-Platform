export function formatRelativeTime(isoTimestamp: string): string {
  const then = new Date(isoTimestamp).getTime();
  const now = Date.now();
  const diffSeconds = Math.max(0, Math.floor((now - then) / 1000));

  const minute = 60;
  const hour = 60 * minute;
  const day = 24 * hour;
  const week = 7 * day;
  const month = 30 * day;

  if (diffSeconds < minute) return "baru saja";
  if (diffSeconds < hour) {
    const n = Math.floor(diffSeconds / minute);
    return `${n} menit lalu`;
  }
  if (diffSeconds < day) {
    const n = Math.floor(diffSeconds / hour);
    return `${n} jam lalu`;
  }
  if (diffSeconds < week) {
    const n = Math.floor(diffSeconds / day);
    return `${n} hari lalu`;
  }
  if (diffSeconds < month) {
    const n = Math.floor(diffSeconds / week);
    return `${n} minggu lalu`;
  }
  const n = Math.floor(diffSeconds / month);
  return `${n} bulan lalu`;
}
