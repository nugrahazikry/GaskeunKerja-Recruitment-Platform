import "./SpinnerWithLabel.css";

export function SpinnerWithLabel({ label }: { label: string }) {
  return (
    <div className="spinner-with-label" role="status" aria-live="polite">
      <span className="spinner" />
      <span>{label}</span>
    </div>
  );
}
