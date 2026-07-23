import type { InputHTMLAttributes, TextareaHTMLAttributes } from "react";
import "./FormField.css";

interface BaseProps {
  label: string;
  error?: string;
  hint?: string;
  /** Skip rendering the visible <label> — for when a wrapping element (e.g. ColorPanel) already
   * shows the field's title as its own header, so the label wouldn't need to repeat. */
  hideLabel?: boolean;
}

export function TextField({
  label,
  error,
  hint,
  hideLabel,
  id,
  ...rest
}: BaseProps & InputHTMLAttributes<HTMLInputElement>) {
  return (
    <div className="field">
      {!hideLabel && <label htmlFor={id}>{label}</label>}
      <input id={id} className={error ? "has-error" : ""} {...rest} />
      {hint && <div className="hint">{hint}</div>}
      {error && <span className="field-error">{error}</span>}
    </div>
  );
}

export function TextAreaField({
  label,
  error,
  hint,
  id,
  ...rest
}: BaseProps & TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <textarea id={id} className={error ? "has-error" : ""} rows={4} {...rest} />
      {hint && <div className="hint">{hint}</div>}
      {error && <span className="field-error">{error}</span>}
    </div>
  );
}
