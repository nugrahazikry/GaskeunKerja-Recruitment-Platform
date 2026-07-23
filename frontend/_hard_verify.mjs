import { chromium } from "playwright";
const OUT_DIR = "C:/Users/zikri/AppData/Local/Temp/claude/d--Data-Scientist-Hackathon-DIGDAYA-2026-project-Tahap-3-implementation/c5d122cb-30f1-434a-9843-912491084585/scratchpad";

// Brand new context, cache fully disabled, no reuse of anything
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 900, height: 700 }, bypassCSP: true });
await context.route("**/*", (route) => route.continue());
const page = await context.newPage();
await page.setExtraHTTPHeaders({ "Cache-Control": "no-cache" });

await page.goto("http://localhost:5173/login", { waitUntil: "networkidle" });
await page.fill("#email", "hr@gaskeundemo.test");
await page.fill("#password", "demo12345");
await page.click("button[type=submit]");
await page.waitForURL("**/dashboard", { timeout: 10000 });
await page.waitForSelector("table.jt", { timeout: 10000 });
await page.waitForTimeout(500);

const cell = page.locator("table.jt tbody td.num").first();
const styles = await cell.evaluate((el) => {
  const cs = getComputedStyle(el);
  return { color: cs.color, fontSize: cs.fontSize };
});
console.log("RESULT:", JSON.stringify(styles));

await page.screenshot({ path: `${OUT_DIR}/hard_verify.png`, fullPage: true });
await browser.close();
