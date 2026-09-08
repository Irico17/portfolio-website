import { chromium } from "playwright-core";

const url = process.argv[2] ?? "http://127.0.0.1:4322/";
const out = [];
const fail = (msg) => {
  out.push(`FAIL ${msg}`);
};
const ok = (msg) => {
  out.push(`OK   ${msg}`);
};

const browser = await chromium.launch({ channel: "chrome", headless: true });

async function runViewport(name, viewport, reduced = false) {
  const context = await browser.newContext({
    viewport,
    reducedMotion: reduced ? "reduce" : "no-preference",
  });
  const page = await context.newPage();
  const requests = [];
  page.on("request", (req) => {
    const u = req.url();
    if (u.includes("/capture/") && !u.includes("capture=")) requests.push(u);
  });
  await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
  const title = await page.title();
  if (title.includes("Cristhofer Alegre")) ok(`${name} title`);
  else fail(`${name} title ${title}`);

  const h1 = await page.locator("h1").getAttribute("aria-label").catch(() => null);
  const h1Alt = await page.locator("h1 img").getAttribute("alt").catch(() => null);
  if ((h1Alt || "").includes("Cristhofer Alegre") || (await page.locator("h1").innerText()).includes("Cristhofer")) {
    ok(`${name} name`);
  } else if (h1Alt) ok(`${name} name ${h1Alt}`);
  else fail(`${name} name missing`);

  const skip = page.locator("a.skip");
  await skip.focus();
  const skipBox = await skip.boundingBox();
  if (skipBox && skipBox.y >= 0) ok(`${name} skip visible on focus`);
  else fail(`${name} skip not visible`);
  await skip.press("Enter");
  await page.waitForTimeout(200);
  const hash = new URL(page.url()).hash;
  if (hash === "#trabajo") ok(`${name} skip to #trabajo`);
  else fail(`${name} skip hash ${hash}`);

  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  const focused = await page.evaluate(() => document.activeElement?.getAttribute("href") || document.activeElement?.tagName);
  ok(`${name} tab focus ${focused}`);

  await page.locator("#contacto").scrollIntoViewIfNeeded();
  const contactY = await page.locator("#contacto").evaluate((el) => el.getBoundingClientRect().top);
  if (contactY < viewport.height) ok(`${name} scrolled to contact`);
  else fail(`${name} contact not in view ${contactY}`);

  const linkedin = page.locator('a[href*="linkedin.com/in/cristhoferalegre"]');
  const github = page.locator('a[href*="github.com/Irico17"]');
  if ((await linkedin.count()) >= 1 && (await github.count()) >= 1) ok(`${name} contact links`);
  else fail(`${name} missing contact links`);

  const slots = await page.locator(".project-list li").count();
  if (slots === 10) ok(`${name} 10 project slots`);
  else fail(`${name} slots ${slots}`);

  const lima = await page.getByText("Municipalidad de Lima").count();
  const pucp = await page.getByText("PUCP").count();
  const ibm = await page.getByText("IBM").count();
  if (lima >= 1 && pucp >= 1 && ibm >= 1) ok(`${name} camino facts`);
  else fail(`${name} camino lima=${lima} pucp=${pucp} ibm=${ibm}`);

  const anim = await page.evaluate(() => {
    const el = document.querySelector(".scrap-in");
    if (!el) return "none";
    return getComputedStyle(el).animationName;
  });
  if (reduced) {
    if (anim === "none") ok(`${name} reduced-motion kills slap`);
    else fail(`${name} reduced-motion still animates ${anim}`);
  } else {
    ok(`${name} motion animationName=${anim}`);
  }

  const liveCapture = requests.filter((u) => u.includes("/capture/"));
  if (liveCapture.length === 0) ok(`${name} live path did not fetch /capture/`);
  else fail(`${name} fetched capture ${liveCapture.length}`);

  await page.screenshot({
    path: `.impeccable/review/verify-${name}.png`,
    fullPage: false,
  });
  await context.close();
}

try {
  await runViewport("desktop", { width: 1440, height: 1024 }, false);
  await runViewport("mobile", { width: 390, height: 844 }, false);
  await runViewport("reduced", { width: 1440, height: 1024 }, true);
} finally {
  await browser.close();
}

const failed = out.filter((l) => l.startsWith("FAIL"));
console.log(out.join("\n"));
if (failed.length) {
  console.error(`\n${failed.length} checks failed`);
  process.exit(1);
}
console.log("\nall checks passed");
