import "./SpinnerWithLabel.css";

/** layout="stacked" puts the spinner above the label (used for prominent modal/full-area loading
 * states); default "inline" keeps the spinner beside the label (compact, used everywhere else). */
export function SpinnerWithLabel({ label, layout = "inline" }: { label: string; layout?: "inline" | "stacked" }) {
  return (
    <div className={`spinner-with-label spinner-with-label-${layout}`} role="status" aria-live="polite">
      <span className="spinner" />
      <span>{label}</span>
    </div>
  );
}
