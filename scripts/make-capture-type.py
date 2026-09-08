"""Capture-only type rasters sized to spec boxes. Live page keeps CSS type."""
from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "assets" / "plates"
ALT = ROOT / "assets" / "plates"
FONTS = Path(r"C:\Windows\Fonts")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def save_both(im: Image.Image, name: str) -> None:
    for dest in (SRC, ALT):
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / name
        im.save(path, "PNG")
        print(f"wrote {path.relative_to(ROOT)} {im.size}")


def noise(im: Image.Image, amount: int = 18) -> Image.Image:
    rng = random.Random(4811)
    px = im.load()
    w, h = im.size
    for _ in range(w * h // amount):
        x, y = rng.randrange(w), rng.randrange(h)
        p = px[x, y]
        if len(p) == 4 and p[3] < 20:
            continue
        j = rng.randint(-40, 40)
        if len(p) == 4:
            px[x, y] = (
                max(0, min(255, p[0] + j)),
                max(0, min(255, p[1] + j)),
                max(0, min(255, p[2] + j)),
                p[3],
            )
        else:
            px[x, y] = tuple(max(0, min(255, c + j)) for c in p[:3])
    return im


def halftone_mask(src: Image.Image, cell: int = 5) -> Image.Image:
    """Turn opaque black glyphs into a coarse xerox halftone."""
    w, h = src.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sp = src.load()
    op = out.load()
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            acc, n = 0, 0
            for dy in range(cell):
                for dx in range(cell):
                    xx, yy = x + dx, y + dy
                    if xx >= w or yy >= h:
                        continue
                    a = sp[xx, yy][3]
                    acc += a
                    n += 1
            if n and acc / n > 80:
                r = max(1, int(cell * 0.42))
                cx, cy = x + cell // 2, y + cell // 2
                for dy in range(-r, r + 1):
                    for dx in range(-r, r + 1):
                        if dx * dx + dy * dy <= r * r:
                            xx, yy = cx + dx, cy + dy
                            if 0 <= xx < w and 0 <= yy < h:
                                op[xx, yy] = (35, 36, 36, 255)
    return out


def trabajo() -> None:
    w, h = 1212, 614
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    face = font("impact.ttf", 400)
    draw.text((0, 8), "TRABAJO", font=face, fill=(35, 36, 36, 255))
    save_both(noise(im, 40), "trabajo-type.png")


def tagline() -> None:
    w, h = 744, 204
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    face = font("segoesc.ttf", 34)
    color = (34, 34, 34, 255)
    text = "diseño + desarrollo + dirección"
    draw.text((6, 4), text, font=face, fill=color)
    bbox = draw.textbbox((6, 4), text, font=face)
    y = bbox[3] + 3
    draw.line((bbox[0], y, min(w - 8, bbox[2]), y + 1), fill=color, width=3)
    draw.line((bbox[0] + 4, y + 5, min(w - 12, bbox[2] - 8), y + 6), fill=color, width=2)
    save_both(noise(im, 36), "tagline-note.png")


def contacto() -> None:
    w, h = 792, 410
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    pink = (220, 55, 110, 240)
    face = font("arialbd.ttf", 72)
    text = "CONTACTO"
    tb = draw.textbbox((0, 0), text, font=face)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    x0 = (w - tw) // 2 - 28
    y0 = (h - th) // 2 - 22
    box = [x0, y0, x0 + tw + 56, y0 + th + 44]
    draw.rectangle(box, outline=pink, width=8)
    draw.rectangle([box[0] + 9, box[1] + 9, box[2] - 9, box[3] - 9], outline=pink, width=4)
    draw.text((x0 + 28 - tb[0], y0 + 18 - tb[1]), text, font=face, fill=pink)
    im = im.rotate(-7, resample=Image.Resampling.BICUBIC, expand=False)
    rng = random.Random(17)
    px = im.load()
    for _ in range(900):
        x, y = rng.randrange(w), rng.randrange(h)
        if px[x, y][3] > 40:
            px[x, y] = (0, 0, 0, 0)
    save_both(im, "contacto-word.png")


def estudio() -> None:
    w, h = 422, 98
    paper = Image.open(SRC / "trabajo-sheet.png").convert("RGB")
    patch = paper.crop((40, 40, 40 + w, 40 + h)) if paper.size[0] > w else paper.resize((w, h))
    im = Image.new("RGB", (w, h), (9, 10, 10))
    rng = random.Random(9)
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    pts = [(0, 0), (w, 0)]
    y = int(h * 0.32)
    x = w
    while x >= 0:
        pts.append((x, y + rng.randint(-10, 12)))
        x -= 14
    pts.append((0, 0))
    md.polygon(pts, fill=255)
    im.paste(patch.resize((w, h)), (0, 0), mask)
    save_both(im, "estudio-edge.png")


def paper() -> None:
    tw, th = 308, 204
    trabajo = Image.open(SRC / "trabajo-sheet.png").convert("RGB")
    camino = Image.open(SRC / "camino-card.png").convert("RGB")
    skills = Image.open(SRC / "skills-scrap.png").convert("RGB")
    light = trabajo.resize((tw, th), Image.Resampling.LANCZOS)
    dark = ImageEnhance.Contrast(camino.resize((tw, th), Image.Resampling.LANCZOS)).enhance(1.6)
    check = skills.crop((skills.width - 96, skills.height - 80, skills.width, skills.height)).resize((96, 72), Image.Resampling.NEAREST)
    mixed = Image.new("RGB", (tw, th))
    lp, dp, mp = light.load(), dark.load(), mixed.load()
    rng = random.Random(8)
    tear = int(tw * 0.42)
    for y in range(th):
        tear = max(int(tw * 0.28), min(int(tw * 0.62), tear + rng.randint(-2, 2)))
        for x in range(tw):
            if x > tear:
                r, g, b = dp[x, y]
                mp[x, y] = (min(r, 42), min(g, 42), min(b, 46))
            else:
                mp[x, y] = lp[x, y]
    mixed.paste(check, (tw - check.size[0] + 2, th - check.size[1] + 2))
    save_both(mixed, "paper-ground.png")


if __name__ == "__main__":
    trabajo()
    tagline()
    contacto()
    estudio()
    paper()
