import type { InputHTMLAttributes, TextareaHTMLAttributes } from "react";
import "./FormField.css";

interface BaseProps {
  label: string;
  error?: string;
}

export function TextField({ label, error, id, ...rest }: BaseProps & InputHTMLAttributes<HTMLInputElement>) {
  return (
    <div className="form-field">
      <label htmlFor={id}>{label}</label>
      <input id={id} className={error ? "has-error" : ""} {...rest} />
      {error && <span className="form-field-error">{error}</span>}
    </div>
  );
}

export function TextAreaField({
  label,
  error,
  id,
  ...rest
}: BaseProps & TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <div className="form-field">
      <label htmlFor={id}>{label}</label>
      <textarea id={id} className={error ? "has-error" : ""} rows={4} {...rest} />
      {error && <span className="form-field-error">{error}</span>}
    </div>
  );
}
