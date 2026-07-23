import type { ReactNode } from "react";
import { GapPanel } from "./GapPanel";
import "./ProfileSections.css";

type ExperienceItem = {
  role: string;
  company: string | null;
  duration: string | null;
  summary: string;
  bullets?: string[];
  tags?: string[];
};
type EducationHistoryItem = { degree: string; institution: string; period: string | null; gpa: string | null };
type Certification = { name: string; issuer: string | null };
type FeaturedProject = { name: string; description: string; url: string | null };
type OrganizationExperienceItem = { role: string; organization: string; period: string | null; description: string };

export type CvProfileData = {
  cv_summary: string | null;
  skills: string[];
  skills_implicit: string[];
  experience: ExperienceItem[];
  qualifications: string[];
  education_level: string | null;
  major: string | null;
  education_history: EducationHistoryItem[];
  certifications: Certification[];
  featured_projects: FeaturedProject[];
  organization_experience: OrganizationExperienceItem[];
};

// Adapted from the Tahap 2 "SkillGap AI" prototype's Agent 1 (CV Parsing) / Agent 2 (Skills
// Specialization) visual template — sectioned cards with a colored icon-square header, restyled
// with this app's own teal/gold/success/warning palette (tokens.css) instead of the original's
// blue/purple/pink, so it stays visually consistent with the rest of the product.
export function CvProfileSections({
  data,
  analysisSummary,
  showCvDetails = true,
  showSkillsTitle = true,
}: {
  data: CvProfileData;
  // Injected here (rather than owned by this component) so the caller can pass the skill-gap
  // analysis card — data this component doesn't have — while still landing it between the
  // "Ringkasan Keahlian" title and the Keahlian Eksplisit/Tersirat grid, per the requested layout.
  analysisSummary?: ReactNode;
  // Laporan (ReportPage) drops the raw CV cards (Ringkasan CV/Pengalaman Kerja/Pendidikan/
  // Sertifikasi/Proyek/Organisasi) and keeps only the Ringkasan Keahlian block — that section's
  // own plain title is also dropped there since analysisSummary's card title now serves as the
  // section header in its place. CandidateDetailPage keeps both (all defaults true).
  showCvDetails?: boolean;
  showSkillsTitle?: boolean;
}) {
  return (
    <>
      {showCvDetails && data.cv_summary && (
        <div className="card profile-section">
          <div className="section-bar-header tone-info">Ringkasan CV</div>
          <p className="profile-section-sub" style={{ marginBottom: 8 }}>
            Riwayat kerja, pendidikan, dan proyek yang diekstrak dari CV.
          </p>
          <blockquote className="profile-summary-quote">{data.cv_summary}</blockquote>
        </div>
      )}

      {showCvDetails && data.experience.length > 0 && (
        <div className="card profile-section">
          <div className="section-bar-header tone-info">Pengalaman Kerja</div>
          <div className="profile-list profile-scroll-2">
            {data.experience.map((exp, i) => (
              <div className="profile-list-item" key={i}>
                <div className="profile-experience-row">
                  <strong>{exp.role}</strong>
                  {exp.duration && (
                    <span className="badge badge-info" style={{ flexShrink: 0 }}>
                      {exp.duration}
                    </span>
                  )}
                </div>
                {exp.company && (
                  <p className="hint" style={{ margin: "2px 0" }}>
                    {exp.company}
                  </p>
                )}
                {exp.bullets && exp.bullets.length > 0 ? (
                  <ul className="profile-bullet-list">
                    {exp.bullets.map((b, bi) => (
                      <li key={bi}>{b}</li>
                    ))}
                  </ul>
                ) : (
                  <p style={{ margin: "4px 0", fontSize: "0.86rem" }}>{exp.summary}</p>
                )}
                {exp.tags && exp.tags.length > 0 && (
                  <div className="chip-row" style={{ marginTop: 6 }}>
                    {exp.tags.map((t) => (
                      <span className="badge badge-info" key={t}>
                        {t}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {showCvDetails && (
        <div className="profile-grid-2">
          <div className="card profile-section">
            <div className="section-bar-header tone-gold">Pendidikan</div>
            {data.education_history.length === 0 ? (
              data.education_level ? (
                <p style={{ fontSize: "0.86rem" }}>
                  {data.education_level}
                  {data.major ? ` — ${data.major}` : ""}
                </p>
              ) : (
                <p className="hint">Belum ada data pendidikan.</p>
              )
            ) : (
              <div className="profile-list profile-scroll-2-small">
                {data.education_history.map((e, i) => (
                  <div className="profile-list-item" key={i}>
                    <strong>{e.degree}</strong>
                    <p className="hint" style={{ margin: "2px 0 0" }}>
                      {[e.institution, e.period, e.gpa ? `GPA ${e.gpa}` : null].filter(Boolean).join(" · ")}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
          <div className="card profile-section">
            <div className="section-bar-header tone-gold">Sertifikasi</div>
            {data.certifications.length === 0 ? (
              <p className="hint">Tidak ada sertifikasi tercatat.</p>
            ) : (
              <div className="profile-list profile-scroll-2-small">
                {data.certifications.map((c, i) => (
                  <div className="profile-list-item" key={i}>
                    <strong>{c.name}</strong>
                    {c.issuer && <p className="hint">{c.issuer}</p>}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {showCvDetails && (
        <div className="profile-grid-2">
          <div className="card profile-section">
            <div className="section-bar-header tone-success">Proyek Unggulan</div>
            {data.featured_projects.length === 0 ? (
              <p className="hint">Tidak ada proyek tercatat.</p>
            ) : (
              <div className="profile-list profile-scroll-2-small">
                {data.featured_projects.map((p, i) => (
                  <div className="profile-list-item" key={i}>
                    <strong>{p.name}</strong>
                    <p style={{ fontSize: "0.82rem" }}>{p.description}</p>
                    {p.url && (
                      <a href={p.url} target="_blank" rel="noreferrer" style={{ fontSize: "0.78rem" }}>
                        Lihat proyek
                      </a>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
          <div className="card profile-section">
            <div className="section-bar-header tone-danger">Pengalaman Organisasi</div>
            {data.organization_experience.length === 0 ? (
              <p className="hint">Tidak ada data organisasi.</p>
            ) : (
              <div className="profile-list profile-scroll-2-small">
                {data.organization_experience.map((o, i) => (
                  <div className="profile-list-item" key={i}>
                    <strong>
                      {o.role} — {o.organization}
                    </strong>
                    {o.period && <p className="hint">{o.period}</p>}
                    <p style={{ fontSize: "0.82rem" }}>{o.description}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      <div>
        {showSkillsTitle && (
          <div className="serif profile-section-title" style={{ marginBottom: 10 }}>
            Ringkasan Keahlian
          </div>
        )}
        {analysisSummary}
        <div className="profile-grid-2">
          <GapPanel header="Keahlian Eksplisit" items={data.skills} emptyLabel="Tidak ada." tone="info" />
          <GapPanel
            header="Keahlian Tersirat"
            items={data.skills_implicit}
            emptyLabel="Tidak ada."
            tone="success"
          />
        </div>
      </div>
    </>
  );
}
