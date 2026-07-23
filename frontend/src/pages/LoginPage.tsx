import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { TextField } from "../components/FormField";
import { ErrorState } from "../components/ErrorState";
import { api, setHrToken } from "../api/client";

export function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const { data, error: apiError } = await api.POST("/auth/login", {
      body: { email, password },
    });
    setLoading(false);
    if (apiError || !data) {
      setError("Email atau password salah.");
      return;
    }
    setHrToken(data.access_token);
    navigate("/dashboard");
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          width: 360,
          background: "var(--surface)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius-md)",
          padding: "32px 30px",
          boxShadow: "0 4px 18px rgba(15, 40, 35, 0.08)",
        }}
      >
        <div style={{ textAlign: "center", marginBottom: 22 }}>
          <div className="brand" style={{ fontSize: "1.25rem" }}>
            Gaskeun<span>Kerja</span>
          </div>
          <p style={{ color: "var(--muted)", fontSize: "0.78rem", margin: "4px 0 0" }}>
            Platform Rekrutmen untuk Bisnis
          </p>
        </div>
        <form onSubmit={handleSubmit}>
          <TextField
            id="email"
            label="Email Perusahaan"
            type="email"
            placeholder="hr@contohsejahtera.co.id"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            id="password"
            label="Kata Sandi"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {error && <ErrorState message={error} />}
          <Button type="submit" variant="primary" block disabled={loading}>
            {loading ? "Memproses..." : "Masuk"}
          </Button>
        </form>
        <p
          className="hint"
          style={{ textAlign: "center", marginTop: 14 }}
        >
          Hanya HR/Recruiter yang memiliki akun. Kandidat mengakses lewat tautan undangan.
        </p>
      </div>
    </div>
  );
}
