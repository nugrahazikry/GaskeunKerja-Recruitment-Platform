import { Card } from "../components/Card";

export function InvalidLinkPage() {
  return (
    <div style={{ maxWidth: 480, margin: "80px auto", padding: "0 16px" }}>
      <Card>
        <h1>Link tidak valid</h1>
        <p>
          Link ini sudah kedaluwarsa atau tidak ditemukan. Silakan hubungi tim rekrutmen
          untuk mendapatkan link baru.
        </p>
      </Card>
    </div>
  );
}
