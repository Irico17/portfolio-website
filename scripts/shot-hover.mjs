import { chromium } from "playwright-core";
import { mkdir } from "node:fs/promises";
const url = process.argv[2] ?? "http://127.0.0.1:4323/portfolio-website/";
await mkdir(".impeccable/review/hover", { recursive: true });
let failed = false;
const browser = await chromium.launch({ channel: "chrome", headless: true });
const ctx = await browser.newContext({ viewport: { width: 1600, height: 900 } });
const page = await ctx.newPage();
await page.goto(url, { waitUntil: "networkidle" });
await page.evaluate(() => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = 2000; }));
for (const sel of [".r-proyecto01-label", ".r-contacto-stamp", ".r-skills-title"]) {
  await page.hover(sel);
  await page.waitForTimeout(320);
  const t = await page.$eval(sel, (el) => getComputedStyle(el).transform);
  // an entrance animation with fill-mode both outranks the hover transition
  // and silently kills every hover; catch that here
  if (t === "none" || t === "matrix(1, 0, 0, 1, 0, 0)") {
    console.log(`FAIL ${sel} does not react to hover (${t})`);
    failed = true;
  } else {
    console.log(`OK   ${sel} -> ${t}`);
  }
  await page.screenshot({ path: `.impeccable/review/hover/${sel.slice(3)}.png` });
}
await browser.close();
if (failed) process.exit(1);
console.log("hover ok");
