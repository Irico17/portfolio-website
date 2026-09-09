import { chromium } from "playwright-core";
import { mkdir } from "node:fs/promises";

const url = process.argv[2] ?? "http://127.0.0.1:4322/portfolio-website/";
await mkdir(".impeccable/review", { recursive: true });
const browser = await chromium.launch({ channel: "chrome", headless: true });

const shots = [
  ["phone", { width: 390, height: 844 }],
  ["phone-full", { width: 390, height: 844 }, true],
  ["tablet", { width: 768, height: 1024 }],
  ["laptop", { width: 1440, height: 900 }],
  ["fullhd", { width: 1920, height: 1080 }],
  ["ultrawide", { width: 2560, height: 1080 }],
  ["short", { width: 1600, height: 720 }],
];

for (const [name, viewport, fullPage] of shots) {
  const context = await browser.newContext({ viewport, reducedMotion: "reduce" });
  const page = await context.newPage();
  await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
  await page.screenshot({
    path: `.impeccable/review/adapt-${name}.png`,
    fullPage: Boolean(fullPage),
  });
  await context.close();
  console.log("wrote", name);
}

await browser.close();
