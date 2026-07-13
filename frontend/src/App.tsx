import { Card } from "./components/Card";
import { Button } from "./components/Button";
import { Badge } from "./components/Badge";
import { Table } from "./components/Table";
import { SkeletonLoader } from "./components/SkeletonLoader";
import { ErrorState } from "./components/ErrorState";
import { EmptyState } from "./components/EmptyState";
import { SpinnerWithLabel } from "./components/SpinnerWithLabel";
import { TextField, TextAreaField } from "./components/FormField";

const demoRows = [
  { id: 1, name: "Kandidat WD-14", score: 0.54, tier: "Menunggu wawancara" },
  { id: 2, name: "Kandidat WD-03", score: 0.52, tier: "Belum diundang" },
];

function App() {
  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 32, display: "flex", flexDirection: "column", gap: 24 }}>
      <h1>GaskeunKerja — Design System Preview (T2)</h1>

      <Card>
        <h2>Buttons</h2>
        <div style={{ display: "flex", gap: 12, marginTop: 12 }}>
          <Button variant="primary">Simpan</Button>
          <Button variant="secondary">Batal</Button>
          <Button variant="danger">Hapus</Button>
          <Button variant="primary" disabled>
            Memproses...
          </Button>
        </div>
      </Card>

      <Card>
        <h2>Status Pills</h2>
        <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
          <Badge tone="neutral">Belum diundang</Badge>
          <Badge tone="warning">Menunggu wawancara</Badge>
          <Badge tone="success">Selesai wawancara</Badge>
          <Badge tone="danger">Ditolak</Badge>
          <Badge tone="info">Terkirim</Badge>
        </div>
      </Card>

      <Card>
        <h2>Table</h2>
        <div style={{ marginTop: 12 }}>
          <Table
            columns={[
              { header: "Kandidat", render: (r) => r.name },
              { header: "Skor", render: (r) => r.score.toFixed(2) },
              { header: "Status", render: (r) => <Badge tone="warning">{r.tier}</Badge> },
            ]}
            rows={demoRows}
            keyField={(r) => r.id}
          />
        </div>
      </Card>

      <Card>
        <h2>Form fields</h2>
        <div style={{ marginTop: 12 }}>
          <TextField id="title" label="Judul Posisi" placeholder="Web Developer" />
          <TextAreaField id="resp" label="Tanggung Jawab" placeholder="Membangun aplikasi web..." />
        </div>
      </Card>

      <Card>
        <h2>Cross-cutting states (T9)</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: 16, marginTop: 12 }}>
          <SkeletonLoader rows={2} />
          <ErrorState message="Gagal memuat data. Periksa koneksi Anda." onRetry={() => alert("retry clicked")} />
          <EmptyState message="Belum ada kandidat untuk posisi ini." />
          <SpinnerWithLabel label="Mengunggah audio..." />
        </div>
      </Card>
    </div>
  );
}

export default App;
