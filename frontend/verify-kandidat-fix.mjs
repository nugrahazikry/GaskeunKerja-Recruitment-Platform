import { chromium } from "playwright";
const loginRes = await fetch("http://localhost:8000/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email: "hr@gaskeundemo.test", password: "demo12345" }),
});
const { access_token: TOKEN } = await loginRes.json();
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 700 } });
await page.addInitScript((token) => { window.localStorage.setItem("gaskeun_hr_token", token); }, TOKEN);
await page.goto("http://localhost:5173/jobs/16/reports", { waitUntil: "networkidle" });
await page.waitForSelector("text=Riwayat Keputusan", { timeout: 15000 });
await page.waitForTimeout(500);
const nums = await page.locator(".stat-num").allTextContents();
console.log("Laporan stat tiles [Total, Menunggu Wawancara, Menunggu Keputusan HR, Lanjutkan, Tolak]:", nums);
const rows = await page.locator(".card strong").allTextContents();
console.log("Rows shown:", rows.filter(r => r.includes("Kandidat")));
await browser.close();
