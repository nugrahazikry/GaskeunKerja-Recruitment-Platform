import "./ProfileSections.css";

// Round-3 follow-up #7 (2026-07-19, round 3 — mirrors the reference "Skill gap analysis prod_v1"
// project's .skill-panel/.a4-gap-panel structure exactly, per user instruction to check that
// project's logic directly): a self-contained bordered box with a colored, full-width HEADER BAR
// (like a table's thead) followed by a white body of chip bubbles — not a bare icon+title floating
// over a plain background. Scrolls only once item count exceeds 7 (same threshold as the
// reference's applyTagScrollLimit()), so a short list never reserves empty scroll space.
export function GapPanel({
  header,
  items,
  emptyLabel,
  tone,
}: {
  header: string;
  items: string[];
  emptyLabel: string;
  tone: "success" | "warning" | "info";
}) {
  const scrollable = items.length > 7;
  return (
    <div className={`gap-panel gap-panel-${tone}`}>
      <div className="gap-panel-header">{header}</div>
      <div className={`gap-panel-body${scrollable ? " gap-panel-scrollable" : ""}`}>
        {items.length === 0 ? (
          <p className="hint">{emptyLabel}</p>
        ) : (
          items.map((item) => (
            <span className={`badge badge-${tone}`} key={item}>
              {item}
            </span>
          ))
        )}
      </div>
    </div>
  );
}
