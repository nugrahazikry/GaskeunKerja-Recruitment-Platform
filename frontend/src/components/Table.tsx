import type { ReactNode } from "react";
import "./Table.css";

interface Column<T> {
  header: string;
  render: (row: T) => ReactNode;
}

export function Table<T>({ columns, rows, keyField }: { columns: Column<T>[]; rows: T[]; keyField: (row: T) => string | number }) {
  return (
    <table className="data-table">
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
