import type { ReactNode } from "react";
import "./EmptyState.css";

export function EmptyState({ message, action }: { message: string; action?: ReactNode }) {
  return (
    <div className="empty-state">
      <p className="empty-state-message">{message}</p>
      {action}
    </div>
  );
}
