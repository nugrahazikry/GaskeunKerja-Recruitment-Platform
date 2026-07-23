import type { ButtonHTMLAttributes } from "react";
import "./Button.css";

type Variant = "primary" | "secondary" | "danger" | "ghost" | "info" | "success";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  block?: boolean;
}

export function Button({ variant = "primary", block, className, ...rest }: ButtonProps) {
  const classes = ["btn", `btn-${variant}`, block ? "btn-block" : "", className ?? ""]
    .filter(Boolean)
    .join(" ");
  return <button className={classes} {...rest} />;
}
