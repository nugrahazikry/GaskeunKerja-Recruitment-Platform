import { useEffect, useState } from "react";
import { BASE_URL, getHrToken } from "../api/client";
import { SpinnerWithLabel } from "./SpinnerWithLabel";
import { ErrorState } from "./ErrorState";

export function AudioPlayer({ url }: { url: string }) {
  const [state, setState] = useState<"loading" | "error" | "ready">("loading");
  const [objectUrl, setObjectUrl] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    let currentObjectUrl: string | null = null;
    setState("loading");

    fetch(`${BASE_URL}${url}`, { headers: { Authorization: `Bearer ${getHrToken()}` } })
      .then((res) => {
        if (!res.ok) throw new Error("failed");
        return res.blob();
      })
      .then((blob) => {
        if (cancelled) return;
        currentObjectUrl = URL.createObjectURL(blob);
        setObjectUrl(currentObjectUrl);
        setState("ready");
      })
      .catch(() => {
        if (!cancelled) setState("error");
      });

    return () => {
      cancelled = true;
      if (currentObjectUrl) URL.revokeObjectURL(currentObjectUrl);
    };
  }, [url, reloadKey]);

  if (state === "loading") return <SpinnerWithLabel label="Memuat audio..." />;
  if (state === "error") {
    return <ErrorState message="Gagal memuat audio." onRetry={() => setReloadKey((k) => k + 1)} />;
  }
  return <audio controls src={objectUrl!} style={{ width: "100%" }} />;
}
