import type { ReactNode } from "react";
import "./Table.css";

interface Column<T> {
  header: string;
  render: (row: T) => ReactNode;
  // Optional: fixes this column's width so it doesn't reflow when the table's row set changes
  // (e.g. across pagination) — without this, column widths are auto-sized per render based on
  // whatever content happens to be visible, so paginated content with varying text length shifts
  // the columns page to page.
  width?: string;
}

export function Table<T>({ columns, rows, keyField }: { columns: Column<T>[]; rows: T[]; keyField: (row: T) => string | number }) {
  const hasFixedWidths = columns.some((c) => c.width);
  return (
    <table className="data-table" style={hasFixedWidths ? { tableLayout: "fixed" } : undefined}>
      {hasFixedWidths && (
        <colgroup>
          {columns.map((col, i) => (
            <col key={i} style={{ width: col.width }} />
          ))}
        </colgroup>
      )}
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={col.header}>{col.header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={keyField(row)}>
            {columns.map((col) => (
              <td key={col.header}>{col.render(row)}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
