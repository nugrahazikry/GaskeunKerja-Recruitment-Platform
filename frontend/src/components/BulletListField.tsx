import { useState } from "react";
import { Button } from "./Button";
import "./FormField.css";
import "./BulletListField.css";

interface Props {
  label: string;
  hint?: string;
  value: string;
  onChange: (value: string) => void;
  /** Skip rendering the visible <label> — for when a wrapping element (e.g. ColorPanel) already
   * shows the field's title as its own header. */
  hideLabel?: boolean;
}

function parseLines(value: string): string[] {
  const lines = value
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .map((line) => (line.startsWith("- ") ? line.slice(2) : line.startsWith("-") ? line.slice(1).trim() : line));
  return lines.length > 0 ? lines : [""];
}

function joinLines(lines: string[]): string {
  return lines
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .map((line) => `- ${line}`)
    .join("\n");
}

/** Block-list editor for bullet-style JD fields (Tanggung Jawab / Kualifikasi / Persyaratan
 * Tambahan) — one row per bullet with add/remove, instead of a free-text textarea. The backend
 * contract is unchanged: still a single "- line\n- line" string, parsed/joined at the edges. */
export function BulletListField({ label, hint, value, onChange, hideLabel }: Props) {
  const [lines, setLines] = useState<string[]>(() => parseLines(value));

  function commit(next: string[]) {
    setLines(next);
    onChange(joinLines(next));
  }

  function updateLine(index: number, text: string) {
    commit(lines.map((l, i) => (i === index ? text : l)));
  }

  function addLine() {
    commit([...lines, ""]);
  }

  function removeLine(index: number) {
    const next = lines.filter((_, i) => i !== index);
    commit(next.length > 0 ? next : [""]);
  }

  return (
    <div className="field bullet-list-field">
      {!hideLabel && <label>{label}</label>}
      <div className="bullet-rows">
        {lines.map((line, i) => (
          <div className="bullet-row" key={i}>
            <span className="bullet-dot" aria-hidden="true">
              &bull;
            </span>
            <input type="text" value={line} onChange={(e) => updateLine(i, e.target.value)} placeholder="Tulis satu poin..." />
            <button type="button" className="bullet-remove" onClick={() => removeLine(i)} aria-label="Hapus poin">
              &times;
            </button>
          </div>
        ))}
      </div>
      <Button type="button" variant="ghost" onClick={addLine}>
        + Tambah poin
      </Button>
      {hint && <div className="hint">{hint}</div>}
    </div>
  );
}
