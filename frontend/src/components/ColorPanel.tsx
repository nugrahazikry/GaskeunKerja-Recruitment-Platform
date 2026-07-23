import type { ReactNode } from "react";
import "./ColorPanel.css";

type Tone = "teal" | "gold" | "success";

/** Shared colored panel — colored header bar + body. Used for both the read-only JD text display
 * (Job Detail) and the JD create/edit form (JobsListPage) so the same visual language shows up in
 * both places. */
export function ColorPanel({ tone, title, children }: { tone: Tone; title: string; children: ReactNode }) {
  return (
    <div className={`color-panel color-panel-${tone}`}>
      <div className="color-panel-header">{title}</div>
      <div className="color-panel-body">{children}</div>
    </div>
  );
}
