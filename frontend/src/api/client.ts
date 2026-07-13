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

api.use({
  onRequest({ request }) {
    const token = getHrToken();
    if (token) {
      request.headers.set("Authorization", `Bearer ${token}`);
    }
    return request;
  },
});
