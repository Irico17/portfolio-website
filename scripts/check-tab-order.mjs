import { chromium } from "playwright-core";
const browser = await chromium.launch({ channel: "chrome", headless: true });
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: "reduce" });
  const page = await ctx.newPage();
  await page.goto(process.argv[2], { waitUntil: "networkidle" });
  const order = [];
  for (let i = 0; i < 9; i++) {
    await page.keyboard.press("Tab");
    order.push(await page.evaluate(() => {
      const el = document.activeElement;
      if (!el) return "?";
      const label = el.getAttribute("aria-label") || el.querySelector(".sr-only")?.textContent || el.textContent?.trim().slice(0, 18);
      const r = el.getBoundingClientRect();
      return `${label} (y=${Math.round(r.y)})`;
    }));
  }
  console.log(`\n== tab order @ ${w}x${h}`);
  order.forEach((o, i) => console.log(`  ${i + 1}. ${o}`));
  await ctx.close();
}
await browser.close();
