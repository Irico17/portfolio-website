import { chromium } from "playwright-core";
import { mkdir } from "node:fs/promises";

const url = process.argv[2] ?? "http://127.0.0.1:4323/portfolio-website/";
await mkdir(".impeccable/review/motion", { recursive: true });
const browser = await chromium.launch({ channel: "chrome", headless: true });

for (const motion of ["no-preference", "reduce"]) {
  const ctx = await browser.newContext({
    viewport: { width: 1600, height: 900 },
    reducedMotion: motion === "reduce" ? "reduce" : "no-preference",
  });
  const page = await ctx.newPage();
  // freeze at load so we can step through the paste-up
  await page.addInitScript(() => { document.addEventListener("DOMContentLoaded", () => {}); });
  // wait for the plates to decode first, then rewind the paste-up so the
  // frames show motion and not a half-loaded page
  await page.goto(url, { waitUntil: "networkidle" });

  const list = await page.evaluate(() =>
    document.getAnimations().map((a) => ({
      name: a.animationName,
      target: a.effect?.target?.className?.baseVal ?? String(a.effect?.target?.className ?? ""),
      delay: a.effect?.getTiming().delay,
      dur: a.effect?.getTiming().duration,
      iter: a.effect?.getTiming().iterations,
      state: a.playState,
    }))
  );
  const byName = {};
  for (const a of list) (byName[a.name] ||= []).push(a);
  console.log(`\n== prefers-reduced-motion: ${motion} — ${list.length} animations running`);
  for (const [name, group] of Object.entries(byName)) {
    const delays = group.map((g) => g.delay).sort((a, b) => a - b);
    console.log(
      `   ${name.padEnd(14)} x${String(group.length).padEnd(3)} dur ${group[0].dur}ms  ` +
      `iter ${group[0].iter}  delays ${delays[0]}–${delays[delays.length - 1]}ms  ${group[0].state}`
    );
  }

  if (motion === "no-preference") {
    for (const t of [120, 300, 520, 900]) {
      await page.evaluate((ms) => {
        document.getAnimations().forEach((a) => { a.pause(); a.currentTime = ms; });
      }, t);
      await page.screenshot({ path: `.impeccable/review/motion/t${String(t).padStart(4, "0")}.png` });
    }
    const spin = await page.evaluate(() => {
      const d = document.querySelector(".vinyl-disc");
      return { classes: d?.className, anims: d ? d.getAnimations().map((a) => a.animationName) : [] };
    });
    console.log("   vinilo:", JSON.stringify(spin));
  }
  await ctx.close();
}
await browser.close();
