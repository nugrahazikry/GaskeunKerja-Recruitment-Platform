import createClient from "openapi-fetch";
import type { paths } from "./schema";

export const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export const api = createClient<paths>({ baseUrl: BASE_URL });

const HR_TOKEN_KEY = "gaskeun_hr_token";

export function getHrToken(): string | null {
  return localStorage.getItem(HR_TOKEN_KEY);
}

export function setHrToken(token: string): void {
  localStorage.setItem(HR_TOKEN_KEY, token);
}

export function clearHrToken(): void {
  localStorage.removeItem(HR_TOKEN_KEY);
}

// Round-3 follow-up #12 (2026-07-19, real bug found via live testing): candidate-facing routes
// (/candidate/:id/consent, /candidate/:id/interview) are unauthenticated by design — they use a
// per-candidate `token` query param, not the HR Bearer token, and already have their own "invalid
// link" handling (CandidateTokenGuard -> InvalidLinkPage). The blanket 401 -> HR /login redirect
// below used to fire unconditionally whenever ANY request returned 401 while an HR token happened
// to still be sitting in localStorage — which is exactly what happens when someone opens a
// candidate invite link in the SAME browser they're logged into HR with (the common case while
// testing locally). A candidate page's own unrelated 401 was hijacking navigation away from the
// interview flow into the HR login screen. Scoped the redirect to HR-guarded routes only.
function isCandidateRoute(): boolean {
  return location.pathname.startsWith("/candidate/");
}

api.use({
  onRequest({ request }) {
    const token = getHrToken();
    if (token && !isCandidateRoute()) {
      request.headers.set("Authorization", `Bearer ${token}`);
    }
    return request;
  },
  onResponse({ response }) {
    if (response.status === 401 && getHrToken() && !isCandidateRoute()) {
      clearHrToken();
      if (location.pathname !== "/login") {
        location.href = "/login";
      }
    }
    return response;
  },
});
