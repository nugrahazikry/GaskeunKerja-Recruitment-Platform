import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { getHrToken } from "../api/client";

export function HrAuthGuard({ children }: { children: ReactNode }) {
  if (!getHrToken()) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
}
