"""Rebuild strip, stamp, and paper-ground so object-fit:cover matches the spec boxes."""
from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "assets" / "plates"
ALT = ROOT / "assets" / "plates"


def save_both(im: Image.Image, name: str) -> None:
    for dest in (SRC, ALT):
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / name
        im.save(path, "PNG")
        print(f"wrote {path.relative_to(ROOT)} {im.size}")


def sample_paper(src: Image.Image, size: tuple[int, int]) -> Image.Image:
    w, h = src.size
    tw, th = size
    x = max(0, (w - tw) // 3)
    y = max(0, (h - th) // 4)
    crop = src.crop((x, y, min(w, x + tw), min(h, y + th)))
    if crop.size != size:
        tile = Image.new("RGB", size, (210, 206, 202))
        for yy in range(0, th, crop.size[1]):
            for xx in range(0, tw, crop.size[0]):
                tile.paste(crop, (xx, yy))
        return tile
    return crop


def jitter_poly(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], rng: random.Random) -> list[tuple[int, int]]:
    x0, y0, x1, y1 = box
    pts: list[tuple[int, int]] = []
    for t in range(18):
        x = x0 + int((x1 - x0) * t / 17)
        y = y0 + rng.randint(-10, 12)
        pts.append((x, y))
    for t in range(6):
        x = x1 + rng.randint(-8, 10)
        y = y0 + int((y1 - y0) * t / 5)
        pts.append((x, y))
    for t in range(18):
        x = x1 - int((x1 - x0) * t / 17)
        y = y1 + rng.randint(-12, 10)
        pts.append((x, y))
    for t in range(6):
        x = x0 + rng.randint(-10, 8)
        y = y1 - int((y1 - y0) * t / 5)
        pts.append((x, y))
    return pts


def rebuild_strip() -> None:
    trabajo = Image.open(SRC / "trabajo-sheet.png").convert("RGB")
    old = Image.open(SRC / "proyecto01-strip.png").convert("RGB")
    tw, th = 1844, 308
    paper = sample_paper(trabajo, (tw, th))
    paper = ImageEnhance.Color(paper).enhance(0.15)
    # Pull pink fiber from the existing plate's right side.
    pink_src = old.crop((int(old.width * 0.62), 0, old.width, old.height)).resize((tw, th), Image.Resampling.LANCZOS)
    band = Image.new("RGB", (tw, th), (210, 206, 202))
    band.paste(paper)
    mask = Image.new("L", (tw, th), 0)
    mdraw = ImageDraw.Draw(mask)
    rng = random.Random(481103)
    y0, y1 = int(th * 0.08), int(th * 0.92)
    x0, x1 = int(tw * 0.02), int(tw * 0.96)
    poly = jitter_poly(mdraw, (x0, y0, x1, y1), rng)
    mdraw.polygon(poly, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    tinted = ImageEnhance.Color(pink_src).enhance(1.35)
    overlay = Image.new("RGB", (tw, th), (231, 72, 121))
    overlay = Image.blend(overlay, tinted, 0.35)
    band = Image.composite(overlay, band, mask)
    grain = ImageEnhance.Contrast(paper).enhance(1.4).convert("L").resize((tw, th))
    band = Image.composite(ImageEnhance.Contrast(band).enhance(1.08), band, grain.point(lambda p: 18 if p < 90 else 0))
    save_both(band, "proyecto01-strip.png")


def rebuild_stamp() -> None:
    trabajo = Image.open(SRC / "trabajo-sheet.png").convert("RGB")
    tw, th = 922, 614
    paper = sample_paper(trabajo, (tw, th))
    paper = ImageEnhance.Color(paper).enhance(0.2)
    draw = ImageDraw.Draw(paper)
    rng = random.Random(17)
    # Small rotated rectangle in the label zone (lower 2/3, not filling the plate).
    cx, cy = int(tw * 0.46), int(th * 0.58)
    rw, rh = int(tw * 0.42), int(th * 0.22)
    stamp = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(stamp)
    box = [cx - rw // 2, cy - rh // 2, cx + rw // 2, cy + rh // 2]
    for i in range(5):
        inset = i
        color = (220, 55, 110, 210 - i * 18)
        sdraw.rectangle(
            [box[0] + inset, box[1] + inset, box[2] - inset, box[3] - inset],
            outline=color,
            width=3,
        )
    # Distress: punch holes in the ink.
    px = stamp.load()
    for _ in range(900):
        x = rng.randint(box[0], box[2])
        y = rng.randint(box[1], box[3])
        if px[x, y][3] > 0:
            px[x, y] = (0, 0, 0, 0)
    stamp = stamp.rotate(-7, resample=Image.Resampling.BICUBIC, center=(cx, cy))
    paper = paper.convert("RGBA")
    paper.alpha_composite(stamp)
    save_both(paper.convert("RGB"), "contacto-stamp.png")


def rebuild_paper() -> None:
    trabajo = Image.open(SRC / "trabajo-sheet.png").convert("RGB")
    camino = Image.open(SRC / "camino-card.png").convert("RGB")
    skills = Image.open(SRC / "skills-scrap.png").convert("RGB")
    tw, th = 308, 204
    light = sample_paper(trabajo, (tw, th))
    dark = camino.crop((camino.width - tw, 0, camino.width, th))
    if dark.size != (tw, th):
        dark = dark.resize((tw, th), Image.Resampling.LANCZOS)
    check = skills.crop((skills.width - 80, skills.height - 70, skills.width, skills.height)).resize((90, 70), Image.Resampling.NEAREST)
    mixed = Image.new("RGB", (tw, th))
    lp = light.load()
    dp = dark.load()
    mp = mixed.load()
    rng = random.Random(8)
    for y in range(th):
        tear = int(tw * 0.46 + 18 * ((y % 17) / 8.5 - 1) + rng.randint(-3, 3))
        for x in range(tw):
            if x > tear:
                r, g, b = dp[x, y]
                mp[x, y] = (min(r, 48), min(g, 48), min(b, 52))
            else:
                mp[x, y] = lp[x, y]
    mixed.paste(check, (tw - check.size[0], th - check.size[1]))
    save_both(mixed, "paper-ground.png")


if __name__ == "__main__":
    rebuild_strip()
    rebuild_stamp()
    rebuild_paper()
