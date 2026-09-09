import { chromium } from "playwright-core";

const url = process.argv[2];
const browser = await chromium.launch({ channel: "chrome", headless: true });
const sizes = [
  ["phone", 390, 844], ["tablet", 768, 1024], ["laptop", 1440, 900],
  ["fullhd", 1920, 1080], ["ultrawide", 2560, 1080], ["short", 1600, 720],
];

const hot = [
  ".r-nombre-ransom", ".r-tagline", ".r-contacto-stamp", ".r-trabajo-title",
  ".r-proyecto01-label", ".r-proyecto02-label", ".r-camino-title",
  ".r-estudio-block", ".r-rol-block", ".r-skills-title", ".r-skill-cluster",
];

for (const [name, width, height] of sizes) {
  const ctx = await browser.newContext({ viewport: { width, height }, reducedMotion: "reduce" });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
  const report = await page.evaluate((sel) => {
    const boxes = sel.map((s) => {
      const el = document.querySelector(s);
      if (!el) return { s, missing: true };
      const r = el.getBoundingClientRect();
      return { s, x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) };
    });
    const overlaps = [];
    for (let i = 0; i < boxes.length; i++)
      for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i], b = boxes[j];
        if (a.missing || b.missing) continue;
        const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
        const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
        if (ox > 2 && oy > 2) overlaps.push(`${a.s} x ${b.s} (${ox}x${oy})`);
      }
    const offscreen = boxes.filter((b) => !b.missing && (b.x < -4 || b.y < -4 || b.x + b.w > innerWidth + 4));
    const tiny = boxes.filter((b) => !b.missing && (b.w < 40 || b.h < 18));
    // every plate box must match its image's own aspect, or object-fit:fill
    // stretches the scrap
    const stretched = [];
    for (const img of document.querySelectorAll(".board .plate")) {
      if (!img.naturalWidth || !img.offsetParent) continue;
      const box = img.parentElement.getBoundingClientRect();
      if (getComputedStyle(img).objectFit !== "fill") continue;
      const want = img.naturalWidth / img.naturalHeight;
      const got = box.width / box.height;
      if (Math.abs(got - want) / want > 0.03)
        stretched.push(`${img.parentElement.className.split(" ")[0]} ${got.toFixed(2)} vs ${want.toFixed(2)}`);
    }
    return {
      hScroll: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      missing: boxes.filter((b) => b.missing).map((b) => b.s),
      overlaps,
      offscreen: offscreen.map((b) => `${b.s} @${b.x},${b.y} ${b.w}x${b.h}`),
      tiny: tiny.map((b) => `${b.s} ${b.w}x${b.h}`),
      stretched,
      name: boxes.find((b) => b.s === ".r-nombre-ransom"),
    };
  }, hot);
  const nm = report.name;
  console.log(`\n== ${name} ${width}x${height}`);
  console.log("  h-overflow:", report.hScroll);
  console.log("  name box:", nm && `${nm.w}x${nm.h} at ${nm.x},${nm.y} = ${(nm.w / width * 100).toFixed(0)}% of width`);
  if (report.missing.length) console.log("  MISSING:", report.missing.join(", "));
  if (report.overlaps.length) console.log("  OVERLAP:", report.overlaps.join(" | "));
  if (report.offscreen.length) console.log("  OFFSCREEN:", report.offscreen.join(" | "));
  if (report.tiny.length) console.log("  TINY:", report.tiny.join(" | "));
  if (report.stretched.length) console.log("  STRETCHED:", report.stretched.join(" | "));
  if (name === "laptop") {
    await page.click(".r-proyecto01-label");
    const open = await page.evaluate(() => {
      const d = document.getElementById("project-flyer");
      return d && d.open ? document.getElementById("flyer-title").textContent : null;
    });
    console.log("  flyer on Proyecto 01 ->", open);
  }
  await ctx.close();
}
await browser.close();
