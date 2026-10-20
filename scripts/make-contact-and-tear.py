"""White torn lip for the desk join, plus collage scraps for phone and email."""
from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "assets" / "plates"
FONTS = Path(r"C:\Windows\Fonts")
CREAM = (236, 232, 226, 255)
TONER = (28, 28, 29, 255)
PINK = (231, 72, 121, 255)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def grain(im: Image.Image, seed: int, amount: int = 22) -> Image.Image:
    rng = random.Random(seed)
    px = im.load()
    w, h = im.size
    for _ in range(max(1, w * h // amount)):
        x, y = rng.randrange(w), rng.randrange(h)
        r, g, b, a = px[x, y]
        if a < 18:
            continue
        j = rng.randint(-28, 28)
        px[x, y] = (
            max(0, min(255, r + j)),
            max(0, min(255, g + j)),
            max(0, min(255, b + j)),
            a,
        )
    return im


def paper_from_dark(src: Image.Image, lift: float = 0.42) -> Image.Image:
    """Keep fibrous paper; punch the dark gap to alpha; lift remaining stock toward cream."""
    im = src.convert("RGBA")
    px = im.load()
    w, h = im.size
    cream = (236, 232, 226)
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            lum = 0.21 * r + 0.72 * g + 0.07 * b
            if lum < 118:
                px[x, y] = (r, g, b, 0)
                continue
            nr = int(r * (1 - lift) + cream[0] * lift)
            ng = int(g * (1 - lift) + cream[1] * lift)
            nb = int(b * (1 - lift) + cream[2] * lift)
            px[x, y] = (nr, ng, nb, 255)
    return im


def torn_mask(w: int, h: int, seed: int, jag: int = 7) -> Image.Image:
    rng = random.Random(seed)
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    pts: list[tuple[int, int]] = []
    step_x = max(4, w // 28)
    step_y = max(4, h // 18)
    for x in range(0, w, step_x):
        pts.append((x, rng.randint(0, jag)))
    pts.append((w - 1, rng.randint(0, jag)))
    for y in range(0, h, step_y):
        pts.append((w - 1 - rng.randint(0, jag), y))
    pts.append((w - 1 - rng.randint(0, jag), h - 1))
    for x in range(w - 1, 0, -step_x):
        pts.append((x, h - 1 - rng.randint(0, jag)))
    pts.append((0, h - 1 - rng.randint(0, jag)))
    for y in range(h - 1, 0, -step_y):
        pts.append((rng.randint(0, jag), y))
    draw.polygon(pts, fill=255)
    return mask.filter(ImageFilter.MaxFilter(3))


def sample_stock(size: tuple[int, int], seed: int) -> Image.Image:
    desk = Image.open(SRC / "desk-sheet.png").convert("RGB")
    dw, dh = desk.size
    tw, th = size
    rng = random.Random(seed)
    # stay on the cream field; the left of desk-sheet is halftone and binder
    x0 = int(dw * 0.28)
    y0 = int(dh * 0.12)
    x1 = int(dw * 0.92)
    y1 = int(dh * 0.88)
    x = x0 + rng.randint(0, max(0, (x1 - x0) - tw))
    y = y0 + rng.randint(0, max(0, (y1 - y0) - th))
    crop = desk.crop((x, y, min(x1, x + tw), min(y1, y + th)))
    if crop.size != size:
        tile = Image.new("RGB", size, (214, 210, 204))
        for yy in range(0, th, crop.size[1]):
            for xx in range(0, tw, crop.size[0]):
                tile.paste(crop, (xx, yy))
        crop = tile
    return ImageEnhance.Brightness(crop).enhance(1.1)


def pink_tape(w: int, max_h: int, seed: int) -> Image.Image:
    rng = random.Random(seed)
    tw, th = int(w * 0.18), max(18, min(max_h, int(w * 0.04)))
    tape = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    body = Image.new("RGBA", (tw, th), PINK)
    body = grain(body, seed, 36)
    mask = torn_mask(tw, th, seed + 4, jag=max(3, th // 6))
    tape.paste(body, (0, 0), mask)
    return tape.rotate(rng.uniform(-18, 22), resample=Image.Resampling.BICUBIC, expand=True)


def stamped_scrap(text: str, seed: int, size: int) -> Image.Image:
    rng = random.Random(seed)
    face_name = "ariblk.ttf" if Path(FONTS / "ariblk.ttf").exists() else "impact.ttf"
    face = font(face_name, size)
    dummy = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    box = dummy.textbbox((0, 0), text, font=face)
    gw, gh = box[2] - box[0], box[3] - box[1]
    pad_x, pad_y = int(size * 0.62), int(size * 0.82)
    tw, th = gw + pad_x * 2, gh + pad_y * 2
    stock = sample_stock((tw, th), seed)
    stock = grain(stock.convert("RGBA"), seed, 30)
    mask = torn_mask(tw, th, seed + 3, jag=max(8, min(tw, th) // 10))
    scrap = Image.new("RGBA", (tw + 10, th + 12), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (tw, th), (20, 16, 14, 78))
    scrap.paste(shadow, (6, 8), mask)
    paper = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    paper.paste(stock, (0, 0), mask)
    draw = ImageDraw.Draw(paper)
    tx = pad_x - box[0] + rng.randint(-2, 2)
    ty = pad_y - box[1] + rng.randint(-3, 3)
    draw.text((tx + 1, ty + 1), text, font=face, fill=(18, 18, 18, 210))
    draw.text((tx, ty), text, font=face, fill=TONER)
    paper = grain(paper, seed + 9, 18)
    scrap.alpha_composite(paper, (0, 0))
    tape = pink_tape(tw, max(18, pad_y // 2), seed + 21)
    # park the tape on a top corner, never across the ink
    ty = rng.randint(0, max(0, pad_y // 5))
    left = rng.randint(8, max(8, int(tw * 0.1)))
    right = max(left, tw - tape.size[0] - 8)
    tx = left if seed % 2 else right
    scrap.alpha_composite(tape, (tx, ty))
    bbox = scrap.getbbox()
    assert bbox
    return scrap.crop(bbox)


def keep_top_sheet(im: Image.Image) -> Image.Image:
    """Drop speckles in the gap; keep only paper connected to the top edge."""
    w, h = im.size
    px = im.load()
    seen = [[False] * w for _ in range(h)]
    stack = [(x, 0) for x in range(w) if px[x, 0][3] > 40]
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h or seen[y][x]:
            continue
        if px[x, y][3] < 40:
            continue
        seen[y][x] = True
        stack.extend(((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))
    for y in range(h):
        for x in range(w):
            if not seen[y][x]:
                px[x, y] = (0, 0, 0, 0)
    return im


def make_tear_lip() -> None:
    torn = keep_top_sheet(paper_from_dark(Image.open(SRC / "scrap-torn.png"), lift=0.55))
    w, h = torn.size
    ridge = torn.crop((0, 0, int(w * 0.82), int(h * 0.3)))
    width = 1720
    height = 150
    scaled = ridge.resize((width + 60, height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas.alpha_composite(scaled, (-30, 0))
    canvas = ImageEnhance.Brightness(canvas).enhance(1.18)
    dest = SRC / "tear-lip.png"
    canvas.save(dest, "PNG")
    print(f"tear-lip {canvas.size}")


def make_contact_scraps() -> None:
    phone = stamped_scrap("900 420 117", 117, 92)
    email = stamped_scrap("arhonalegre@gmail.com", 420, 48)
    phone.save(SRC / "phone-scrap.png", "PNG")
    email.save(SRC / "email-scrap.png", "PNG")
    print(f"phone-scrap {phone.size}")
    print(f"email-scrap {email.size}")


def make_join_sheet() -> None:
    w, h = 1180, 560
    stock = sample_stock((w, h), 91).convert("RGBA")
    stock = grain(stock, 91, 26)
    stock = ImageEnhance.Brightness(stock).enhance(1.14)
    mask = torn_mask(w, h, 77, jag=26)
    canvas = Image.new("RGBA", (w + 12, h + 14), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (w, h), (20, 16, 14, 50))
    canvas.paste(shadow, (8, 10), mask)
    paper = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    paper.paste(stock, (0, 0), mask)
    lip = Image.open(SRC / "tear-lip.png").convert("RGBA").resize((w, int(h * 0.28)), Image.Resampling.LANCZOS)
    paper.alpha_composite(lip, (0, 0))
    canvas.alpha_composite(paper, (0, 0))
    dest = SRC / "join-sheet.png"
    canvas.save(dest, "PNG")
    print(f"join-sheet {canvas.size}")


if __name__ == "__main__":
    make_tear_lip()
    make_join_sheet()
    make_contact_scraps()
