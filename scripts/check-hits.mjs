import { chromium } from "playwright-core";
const url = process.argv[2];
const browser = await chromium.launch({ channel: "chrome", headless: true });
const sel = [
  ".r-contacto-stamp", ".r-trabajo-title", ".r-proyecto01-label",
  ".r-proyecto02-label", ".r-camino-title", ".r-skills-title", ".r-skill-cluster",
];
for (const [w, h] of [[390, 844], [768, 1024], [1280, 720], [1920, 1080], [2560, 1080]]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: "reduce" });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  const out = await page.evaluate((sel) => {
    const rows = [];
    for (const s of sel) {
      const el = document.querySelector(s);
      if (!el) { rows.push(`${s}: MISSING`); continue; }
      const r = el.getBoundingClientRect();
      const cx = r.x + r.width / 2, cy = r.y + r.height / 2;
      const hit = document.elementFromPoint(cx, cy);
      const ok = hit && (hit === el || el.contains(hit) || hit.parentElement === el);
      // hit target incl. the ::after expansion
      const a = getComputedStyle(el, "::after");
      const tw = Math.max(r.width, parseFloat(a.width) || 0);
      const th = Math.max(r.height, parseFloat(a.height) || 0);
      rows.push(
        `${s.padEnd(22)} ${Math.round(tw)}x${Math.round(th)}` +
        `${tw < 44 || th < 44 ? "  SMALL" : ""}` +
        `${ok ? "" : "  BLOCKED by " + (hit ? hit.className || hit.tagName : "nothing")}`
      );
    }
    return rows;
  }, sel);
  console.log(`\n== ${w}x${h}`);
  out.forEach((r) => console.log("  " + r));
  await ctx.close();
}
await browser.close();
