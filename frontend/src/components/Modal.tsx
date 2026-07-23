import type { ReactNode } from "react";
import "./Modal.css";

export function Modal({
  title,
  onClose,
  children,
  dismissOnBackdropClick = true,
}: {
  title: string;
  onClose: () => void;
  children: ReactNode;
  // Round-3 follow-up #10 (2026-07-19): some modals (e.g. "Tinjau Kompetensi Wajib") hold
  // meaningful in-progress review state — an accidental click just outside the panel shouldn't
  // silently dismiss it. Defaults to true (unchanged behavior) so every other existing Modal
  // usage in the app is unaffected; only the X button and any explicit action button close it
  // when this is set to false.
  dismissOnBackdropClick?: boolean;
}) {
  return (
    <div className="modal-backdrop" onClick={dismissOnBackdropClick ? onClose : undefined}>
      <div className="modal-panel" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="modal-close" onClick={onClose} aria-label="Tutup">
            ×
          </button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
}
