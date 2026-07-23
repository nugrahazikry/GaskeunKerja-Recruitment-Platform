import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { TopBar } from "../components/TopBar";
import { SkeletonLoader } from "../components/SkeletonLoader";
import { ErrorState } from "../components/ErrorState";
import { EmptyState } from "../components/EmptyState";
import { api } from "../api/client";

type PerJobStat = {
  job_id: number;
  title: string;
  status: string;
  candidate_count: number;
  interviewed_count: number;
  decided_count: number;
};

type AttentionItem = {
  type: string;
  label: string;
  job_id: number | null;
  candidate_id: number | null;
};

type ScoreDistribution = {
  bucket_0_40: number;
  bucket_40_60: number;
  bucket_60_80: number;
  bucket_80_100: number;
};

type JobConversion = {
  job_id: number;
  title: string;
  invited_count: number;
  completed_count: number;
};

type CompetencyGap = {
  competency_name: string;
  missing_pct: number;
};

type JobDecisionBreakdown = {
  job_id: number;
  title: string;
  advance_count: number;
  reject_count: number;
  pending_count: number;
};

type DashboardStats = {
  company_name: string;
  active_jobs: number;
  closed_jobs: number;
  total_candidates: number;
  belum_diundang: number;
  menunggu_wawancara: number;
  selesai_wawancara: number;
  decisions_advance: number;
  decisions_reject: number;
  decisions_pending: number;
  reports_sent: number;
  avg_match_score: number | null;
  per_job: PerJobStat[];
  attention: AttentionItem[];
  score_distribution: ScoreDistribution;
  conversion_by_job: JobConversion[];
  competency_gaps: CompetencyGap[];
  decisions_by_job: JobDecisionBreakdown[];
};

type State =
  | { status: "loading" }
  | { status: "error" }
  | { status: "ready"; stats: DashboardStats };

const ATTENTION_ICON: Record<string, string> = {
  undecided: "!",
  no_approved_questions: "?",
  report_not_sent: "✉",
};

const ATTENTION_CLASS: Record<string, string> = {
  undecided: "undecided",
  no_approved_questions: "noquestions",
  report_not_sent: "noreport",
};

export function DashboardPage() {
  const navigate = useNavigate();
  const [state, setState] = useState<State>({ status: "loading" });
  const [reloadKey, setReloadKey] = useState(0);
  const attnListRef = useRef<HTMLDivElement>(null);
  const [attnCanScrollDown, setAttnCanScrollDown] = useState(false);
  const jobTableRef = useRef<HTMLDivElement>(null);
  const [jobTableCanScrollDown, setJobTableCanScrollDown] = useState(false);

  function checkAttnScroll() {
    const el = attnListRef.current;
    setAttnCanScrollDown(!!el && el.scrollHeight - el.clientHeight - el.scrollTop > 4);
  }

  function checkJobTableScroll() {
    const el = jobTableRef.current;
    setJobTableCanScrollDown(!!el && el.scrollHeight - el.clientHeight - el.scrollTop > 4);
  }

  useEffect(() => {
    checkAttnScroll();
    checkJobTableScroll();
  }, [state]);

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });
    api.GET("/dashboard/stats").then(({ data, error }) => {
      if (cancelled) return;
      if (error || !data) {
        setState({ status: "error" });
        return;
      }
      setState({ status: "ready", stats: data as DashboardStats });
    });
    return () => {
      cancelled = true;
    };
  }, [reloadKey]);

  if (state.status === "loading") {
    return (
      <div className="dashboard-shell">
        <TopBar active="dashboard" />
        <div className="main wide">
          <SkeletonLoader rows={4} />
        </div>
      </div>
    );
  }

  if (state.status === "error") {
    return (
      <div className="dashboard-shell">
        <TopBar active="dashboard" />
        <div className="main wide">
          <ErrorState message="Gagal memuat dashboard." onRetry={() => setReloadKey((k) => k + 1)} />
        </div>
      </div>
    );
  }

  const s = state.stats;
  const totalJobs = s.active_jobs + s.closed_jobs;
  const totalDecided = s.decisions_advance + s.decisions_reject;
  const funnelTotal = Math.max(1, s.belum_diundang + s.menunggu_wawancara + s.selesai_wawancara + totalDecided);

  if (totalJobs === 0) {
    return (
      <div className="dashboard-shell">
        <TopBar active="dashboard" />
        <div className="main wide">
          <div className="pagehead">
            <h1>Dashboard</h1>
            <p>{s.company_name} &middot; ringkasan rekrutmen</p>
          </div>
          <div className="card">
            <EmptyState message="Belum ada lowongan. Buat lowongan pertama Anda untuk mulai melihat ringkasan di sini." />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-shell">
      <TopBar active="dashboard" />
      <div className="main wide">
        <div className="pagehead">
          <h1>Dashboard</h1>
          <p>{s.company_name} &middot; ringkasan rekrutmen</p>
        </div>

        <div className="kpi-grid">
          <div className="kpi-card">
            <div className="kpi-label">Lowongan Aktif</div>
            <div className="kpi-num">{s.active_jobs}</div>
            <div className="kpi-sub">{s.closed_jobs} ditutup</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Total Kandidat</div>
            <div className="kpi-num">{s.total_candidates}</div>
            <div className="kpi-sub">di semua lowongan</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Wawancara Selesai</div>
            <div className="kpi-num">{s.selesai_wawancara + totalDecided}</div>
            <div className="kpi-sub">dari {s.menunggu_wawancara + s.selesai_wawancara + totalDecided} diundang</div>
          </div>
          <div className={`kpi-card${s.decisions_pending > 0 ? " warn" : ""}`}>
            <div className="kpi-label">Keputusan Dibuat</div>
            <div className="kpi-num">{totalDecided}</div>
            <div className="kpi-sub">
              {s.decisions_advance} lanjut &middot; {s.decisions_reject} tolak
            </div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Laporan Terkirim</div>
            <div className="kpi-num">{s.reports_sent}</div>
            <div className="kpi-sub">via Email</div>
          </div>
        </div>

        <div className="ai-card">
          <div className="ai-icon">&#10022;</div>
          <div>
            <h4>AI sedang menganalisis kandidat Anda</h4>
            <p>Skor kecocokan, kesenjangan kompetensi, dan status wawancara diperbarui otomatis setiap ada kandidat baru masuk.</p>
          </div>
          <div className="ai-badge">AI AKTIF</div>
        </div>

        <div className="pipeline-card">
          <div className="pipeline-head">
            <h2>Alur Kandidat</h2>
            <span className="ptotal">{funnelTotal} kandidat dalam proses</span>
          </div>
          <div className="pipeline-stages">
            <div className="pstage s1">
              <div className="pnum">{s.belum_diundang}</div>
              <div className="plabel">Belum Diundang</div>
            </div>
            <div className="pstage s2">
              <div className="pnum">{s.menunggu_wawancara}</div>
              <div className="plabel">Menunggu Wawancara</div>
            </div>
            <div className="pstage s3">
              <div className="pnum">{s.selesai_wawancara}</div>
              <div className="plabel">Selesai Wawancara</div>
            </div>
            <div className="pstage s4">
              <div className="pnum">{totalDecided}</div>
              <div className="plabel">Sudah Diputuskan</div>
            </div>
          </div>
          <div className="pipeline-track">
            <div className="pseg s1" style={{ flex: Math.max(s.belum_diundang, 0.001) }}>
              {s.belum_diundang > 0 && `${Math.round((s.belum_diundang / funnelTotal) * 100)}%`}
            </div>
            <div className="pseg s2" style={{ flex: Math.max(s.menunggu_wawancara, 0.001) }}>
              {s.menunggu_wawancara > 0 && `${Math.round((s.menunggu_wawancara / funnelTotal) * 100)}%`}
            </div>
            <div className="pseg s3" style={{ flex: Math.max(s.selesai_wawancara, 0.001) }}>
              {s.selesai_wawancara > 0 && `${Math.round((s.selesai_wawancara / funnelTotal) * 100)}%`}
            </div>
            <div className="pseg s4" style={{ flex: Math.max(totalDecided, 0.001) }}>
              {totalDecided > 0 && `${Math.round((totalDecided / funnelTotal) * 100)}%`}
            </div>
          </div>
        </div>

        <div className="db-split">
          <div className="panel">
            <div className="panel-head">
              <h3>Ringkasan per Lowongan</h3>
            </div>
            <div className="jt-scroll" ref={jobTableRef} onScroll={checkJobTableScroll}>
              <table className="jt">
                <thead>
                  <tr>
                    <th>Lowongan</th>
                    <th>Status</th>
                    <th className="num">Kandidat</th>
                    <th className="num">Diwawancara</th>
                    <th className="num">Diputuskan</th>
                  </tr>
                </thead>
                <tbody>
                  {s.per_job.map((j) => (
                    <tr
                      key={j.job_id}
                      onClick={() => navigate(`/jobs/${j.job_id}/detail`)}
                    >
                      <td className="jobname">{j.title}</td>
                      <td>
                        <span className={`db-pill ${j.status === "active" ? "db-pill-active" : "db-pill-closed"}`}>
                          {j.status === "active" ? "Aktif" : "Ditutup"}
                        </span>
                      </td>
                      <td className="num">{j.candidate_count}</td>
                      <td className="num">{j.interviewed_count}</td>
                      <td className="num">{j.decided_count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {jobTableCanScrollDown && (
              <button
                type="button"
                className="attn-scroll-btn"
                onClick={() => jobTableRef.current?.scrollBy({ top: 150, behavior: "smooth" })}
                aria-label="Gulir ke bawah untuk melihat lowongan lainnya"
                title="Gulir ke bawah"
              >
                &#9660;
              </button>
            )}
          </div>
          <div className="panel">
            <div className="panel-head">
              <h3>Perlu Perhatian</h3>
            </div>
            {s.attention.length === 0 ? (
              <div className="attn-empty">Tidak ada yang perlu perhatian saat ini.</div>
            ) : (
              <div className="attn-list" ref={attnListRef} onScroll={checkAttnScroll}>
                {s.attention.map((item, i) => {
                  const tone = item.type === "no_approved_questions" ? "warn" : "info";
                  return (
                    <div className={`attn-item ${tone}`} key={i}>
                      <div className="attn-ico">{ATTENTION_ICON[item.type] ?? "!"}</div>
                      <div className="attn-body">
                        <div className="attn-title">
                          {item.type === "no_approved_questions"
                            ? "Pertanyaan belum disetujui"
                            : item.type === "report_not_sent"
                              ? "Laporan belum dikirim"
                              : "Belum ada keputusan"}
                        </div>
                        <div className="attn-desc">{item.label}</div>
                      </div>
                      {item.job_id !== null && (
                        <a
                          className="attn-action"
                          href={`/jobs/${item.job_id}/detail`}
                          onClick={(e) => {
                            e.preventDefault();
                            navigate(`/jobs/${item.job_id}/detail`);
                          }}
                        >
                          Lihat &rarr;
                        </a>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
            {attnCanScrollDown && (
              <button
                type="button"
                className="attn-scroll-btn"
                onClick={() => attnListRef.current?.scrollBy({ top: 150, behavior: "smooth" })}
                aria-label="Gulir ke bawah untuk melihat item lainnya"
                title="Gulir ke bawah"
              >
                &#9660;
              </button>
            )}
          </div>
        </div>

        <div className="chart-grid2">
          <div className="card chart-card">
            <h3>Distribusi Skor Kecocokan</h3>
            <p className="chart-sub">Semua kandidat, semua lowongan aktif &mdash; di mana kualitas pool berada</p>
            {(() => {
              const d = s.score_distribution;
              const max = Math.max(d.bucket_0_40, d.bucket_40_60, d.bucket_60_80, d.bucket_80_100, 1);
              const buckets: [string, number][] = [
                ["0–40", d.bucket_0_40],
                ["40–60", d.bucket_40_60],
                ["60–80", d.bucket_60_80],
                ["80–100", d.bucket_80_100],
              ];
              return buckets.map(([label, count]) => (
                <div className="hbar-row lightable" key={label} title={`${count} kandidat pada rentang skor ${label}`}>
                  <div className="hlabel">{label}</div>
                  <div className="hbar-track">
                    <div className="hbar-fill" style={{ width: `${(count / max) * 100}%` }} />
                  </div>
                  <div className="hval">{count}</div>
                </div>
              ));
            })()}
          </div>

          <div className="card chart-card">
            <h3>Konversi Undangan &rarr; Wawancara</h3>
            <p className="chart-sub">Dari kandidat yang diundang, berapa % menyelesaikan wawancara</p>
            {s.conversion_by_job.length === 0 ? (
              <p style={{ fontSize: "0.82rem", color: "var(--muted)" }}>Belum ada kandidat yang diundang.</p>
            ) : (
              s.conversion_by_job.map((c) => {
                const pct = c.invited_count > 0 ? Math.round((c.completed_count / c.invited_count) * 100) : 0;
                return (
                  <div
                    className="conv-row lightable"
                    key={c.job_id}
                    title={`${c.completed_count} dari ${c.invited_count} diundang menyelesaikan wawancara`}
                  >
                    <div className="conv-head">
                      <span className="cjob">{c.title}</span>
                      <span className="cpct">{pct}%</span>
                    </div>
                    <div className="conv-track">
                      <div className="conv-fill" style={{ width: `${Math.max(pct, 2)}%` }} />
                    </div>
                    <div className="conv-foot">
                      {c.completed_count} dari {c.invited_count} diundang menyelesaikan wawancara
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        <div className="chart-grid2">
          <div className="card chart-card">
            <h3>Kesenjangan Kompetensi Terbanyak</h3>
            <p className="chart-sub">
              Kompetensi wajib yang paling sering &quot;belum terlihat&quot; di kandidat
              {s.per_job.length > 0 && ` — ${[...s.per_job].sort((a, b) => b.candidate_count - a.candidate_count)[0].title}`}
            </p>
            {s.competency_gaps.length === 0 ? (
              <p style={{ fontSize: "0.82rem", color: "var(--muted)" }}>Belum ada data kompetensi.</p>
            ) : (
              s.competency_gaps.map((g) => (
                <div
                  className="gap-row lightable"
                  key={g.competency_name}
                  title={`${Math.round(g.missing_pct)}% kandidat belum menunjukkan "${g.competency_name}"`}
                >
                  <div className="glabel">{g.competency_name}</div>
                  <div className="gap-track">
                    <div className="gap-fill" style={{ width: `${g.missing_pct}%` }} />
                  </div>
                  <div className="gval">{Math.round(g.missing_pct)}%</div>
                </div>
              ))
            )}
          </div>

          <div className="card chart-card">
            <h3>Ringkasan Keputusan per Lowongan</h3>
            <p className="chart-sub">Lanjut vs tolak vs masih menunggu, per lowongan</p>
            {s.decisions_by_job.length === 0 ? (
              <p style={{ fontSize: "0.82rem", color: "var(--muted)" }}>Belum ada keputusan.</p>
            ) : (
              <>
                {s.decisions_by_job.map((d) => {
                  const total = d.advance_count + d.reject_count + d.pending_count || 1;
                  return (
                    <div className="dec-row lightable" key={d.job_id}>
                      <div className="dec-head">{d.title}</div>
                      <div className="dec-stack">
                        {d.advance_count > 0 && (
                          <div
                            className="dec-seg advance"
                            style={{ width: `${(d.advance_count / total) * 100}%` }}
                            title={`${d.advance_count} lanjut — ${d.title}`}
                          >
                            {d.advance_count}
                          </div>
                        )}
                        {d.reject_count > 0 && (
                          <div
                            className="dec-seg reject"
                            style={{ width: `${(d.reject_count / total) * 100}%` }}
                            title={`${d.reject_count} tolak — ${d.title}`}
                          >
                            {d.reject_count}
                          </div>
                        )}
                        {d.pending_count > 0 && (
                          <div
                            className="dec-seg pending"
                            style={{ width: `${(d.pending_count / total) * 100}%` }}
                            title={`${d.pending_count} belum diputuskan — ${d.title}`}
                          >
                            {d.pending_count}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
                <div className="dec-legend">
                  <span>
                    <i style={{ background: "var(--success)" }} />
                    Lanjut
                  </span>
                  <span>
                    <i style={{ background: "var(--danger)" }} />
                    Tolak
                  </span>
                  <span>
                    <i style={{ background: "var(--muted)" }} />
                    Belum diputuskan
                  </span>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
