"""Live xerox/collage inks for hero labels that were still CSS type."""
from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "assets" / "plates"
PUBLIC = ROOT / "public" / "plates"
FONTS = Path(r"C:\Windows\Fonts")
CREAM = (235, 230, 223, 255)
TONER = (35, 36, 36, 255)
PINK = (231, 72, 121, 255)
HOT_TYPE = (247, 238, 242, 255)
PAPER = (210, 206, 202, 255)
INK = (25, 25, 26, 255)
BIRO = (42, 69, 128, 255)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def crop_ink(im: Image.Image, pad: int = 6) -> Image.Image:
    bbox = im.getbbox()
    if not bbox:
        return im
    left, top, right, bottom = bbox
    return im.crop(
        (
            max(0, left - pad),
            max(0, top - pad),
            min(im.size[0], right + pad),
            min(im.size[1], bottom + pad),
        )
    )


def save(im: Image.Image, name: str) -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    im = crop_ink(im)
    png = SRC / f"{name}.png"
    webp = PUBLIC / f"{name}.webp"
    im.save(png, "PNG")
    im.save(webp, "WEBP", quality=86, method=6)
    print(f"{name} {im.size}")


def grain(im: Image.Image, seed: int, amount: int = 22) -> Image.Image:
    rng = random.Random(seed)
    px = im.load()
    w, h = im.size
    for _ in range(max(1, w * h // amount)):
        x, y = rng.randrange(w), rng.randrange(h)
        r, g, b, a = px[x, y]
        if a < 18:
            continue
        j = rng.randint(-38, 38)
        px[x, y] = (
            max(0, min(255, r + j)),
            max(0, min(255, g + j)),
            max(0, min(255, b + j)),
            a,
        )
    return im


def torn_mask(w: int, h: int, seed: int, jag: int = 7) -> Image.Image:
    rng = random.Random(seed)
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    pts: list[tuple[int, int]] = []
    for x in range(0, w, max(4, w // 28)):
        pts.append((x, rng.randint(0, jag)))
    pts.append((w - 1, rng.randint(0, jag)))
    for y in range(0, h, max(4, h // 18)):
        pts.append((w - 1 - rng.randint(0, jag), y))
    pts.append((w - 1 - rng.randint(0, jag), h - 1))
    for x in range(w - 1, 0, -max(4, w // 28)):
        pts.append((x, h - 1 - rng.randint(0, jag)))
    pts.append((0, h - 1 - rng.randint(0, jag)))
    for y in range(h - 1, 0, -max(4, h // 18)):
        pts.append((rng.randint(0, jag), y))
    draw.polygon(pts, fill=255)
    return mask.filter(ImageFilter.MaxFilter(3))


def paper_tile(w: int, h: int, fill: tuple[int, int, int, int], seed: int) -> Image.Image:
    tile = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    body = Image.new("RGBA", (w, h), fill)
    body = grain(body, seed, 28)
    mask = torn_mask(w, h, seed + 3, jag=max(4, min(w, h) // 9))
    tile.paste(body, (0, 0), mask)
    shadow = Image.new("RGBA", (w + 6, h + 6), (0, 0, 0, 0))
    sh = Image.new("RGBA", (w, h), (20, 16, 14, 70))
    shadow.paste(sh, (3, 4), mask)
    shadow.alpha_composite(tile, (0, 0))
    return shadow


def cut_word(
    text: str,
    faces: list[str],
    size: int,
    seed: int,
    hot_at: int | None = None,
    invert_at: tuple[int, ...] = (),
) -> Image.Image:
    rng = random.Random(seed)
    letters = [ch for ch in text]
    tiles: list[Image.Image] = []
    for i, ch in enumerate(letters):
        face = font(faces[i % len(faces)], size)
        dummy = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        box = dummy.textbbox((0, 0), ch, font=face)
        gw, gh = box[2] - box[0], box[3] - box[1]
        pad_x, pad_y = int(size * 0.18), int(size * 0.16)
        tw, th = gw + pad_x * 2, gh + pad_y * 2
        if i == hot_at:
            fill, ink = PINK, HOT_TYPE
        elif i in invert_at:
            fill, ink = TONER, PAPER
        else:
            fill, ink = CREAM, TONER
        tile = paper_tile(tw, th, fill, seed + i * 17)
        draw = ImageDraw.Draw(tile)
        draw.text((pad_x - box[0], pad_y - box[1] + rng.randint(-2, 2)), ch, font=face, fill=ink)
        rot = rng.uniform(-3.4, 3.2)
        tiles.append(tile.rotate(rot, resample=Image.Resampling.BICUBIC, expand=True))

    gap = int(size * 0.06)
    width = sum(t.size[0] for t in tiles) - gap * (len(tiles) - 1) + 16
    height = max(t.size[1] for t in tiles) + 18
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = 6
    for tile in tiles:
        y = (height - tile.size[1]) // 2 + rng.randint(-3, 3)
        canvas.alpha_composite(tile, (x, max(0, y)))
        x += tile.size[0] - gap
    return grain(canvas, seed, 40)


def typed_ink(
    text: str,
    box: tuple[int, int],
    size: int,
    seed: int,
    underline: bool = False,
    face_name: str = "courbd.ttf",
    fill: tuple[int, int, int, int] = INK,
) -> Image.Image:
    w, h = box
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rng = random.Random(seed)
    x, y = 10, max(6, (h - size) // 3)
    for ch in text:
        face = font(face_name, size + rng.randint(-2, 3))
        glyph = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glyph)
        gd.text((8, 8), ch, font=face, fill=fill)
        glyph = glyph.rotate(rng.uniform(-2.8, 2.8), resample=Image.Resampling.BICUBIC, expand=True)
        im.alpha_composite(glyph, (x, max(0, y + rng.randint(-4, 4))))
        adv = ImageDraw.Draw(Image.new("RGBA", (8, 8))).textbbox((0, 0), ch, font=face)
        x += (adv[2] - adv[0]) + rng.randint(0, 4)
    draw = ImageDraw.Draw(im)
    if underline:
        y2 = y + size + 8
        draw.line((12, y2, min(w - 12, x + 8), y2 + rng.randint(-1, 2)), fill=fill, width=4)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=90, threshold=2))
    return grain(im, seed, 12)


def typed_scrap(
    text: str,
    size: int,
    seed: int,
    underline: bool = False,
    biro: bool = False,
) -> Image.Image:
    dummy = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    face = font("courbd.ttf", size)
    box = dummy.textbbox((0, 0), text, font=face)
    tw, th = box[2] - box[0], box[3] - box[1]
    pad_x, pad_y = 28, 22
    paper = paper_tile(tw + pad_x * 2, th + pad_y * 2 + (18 if underline else 0), CREAM, seed)
    ink = typed_ink(text, paper.size, size, seed + 9, underline=underline and not biro)
    paper.alpha_composite(ink, (0, 0))
    if biro:
        draw = ImageDraw.Draw(paper)
        y = pad_y + th + 8
        draw.line((pad_x, y, paper.size[0] - pad_x, y + 2), fill=BIRO, width=3)
    return grain(paper, seed, 32)


def dash(draw: ImageDraw.ImageDraw, y: int, x0: int, x1: int, fill: tuple[int, int, int, int]) -> None:
    x = x0
    on = True
    while x < x1:
        nx = min(x1, x + (9 if on else 6))
        if on:
            draw.line((x, y, nx, y + 1), fill=fill, width=3)
        x = nx
        on = not on


def form_block(label: str, value: str, seed: int) -> Image.Image:
    scrap = paper_tile(420, 210, CREAM, seed)
    draw = ImageDraw.Draw(scrap)
    head = font("courbd.ttf", 36)
    body = font("courbd.ttf", 44)
    draw.text((22, 18), label.upper(), font=head, fill=INK)
    dash(draw, 64, 22, 360, INK)
    draw.text((22, 78), value, font=body, fill=INK)
    dash(draw, 148, 22, 300, INK)
    return grain(scrap, seed, 20)


def tape_strip(im: Image.Image, seed: int) -> Image.Image:
    rng = random.Random(seed)
    w, h = im.size
    tw, th = int(w * 0.42), max(18, int(h * 0.18))
    tape = Image.new("RGBA", (tw, th), (236, 230, 210, 110))
    tape = grain(tape, seed, 50)
    tape = ImageEnhance.Brightness(tape).enhance(1.08)
    rot = rng.uniform(-8, 9)
    tape = tape.rotate(rot, resample=Image.Resampling.BICUBIC, expand=True)
    x = (w - tape.size[0]) // 2 + rng.randint(-12, 12)
    im.alpha_composite(tape, (max(0, x), max(0, rng.randint(2, 8))))
    return im


def main() -> None:
    skills = cut_word(
        "SKILLS",
        ["ariblk.ttf", "timesbd.ttf", "impact.ttf", "georgiab.ttf", "ariblk.ttf", "timesbd.ttf"],
        92,
        4811,
        hot_at=1,
        invert_at=(0, 4),
    )
    skills = tape_strip(skills, 17)
    save(skills, "skills-ink")

    camino = typed_scrap("CAMINO", 72, 902, underline=True)
    save(camino, "camino-ink")

    p01 = typed_scrap("PROYECTO 01", 78, 55, underline=False)
    save(p01, "proyecto01-ink")

    p02 = typed_scrap("PROYECTO 02", 64, 88, underline=True)
    save(p02, "proyecto02-scrap")

    cluster = typed_scrap("Skill cluster", 48, 330, biro=True)
    save(cluster, "cluster-ink")

    estudio = form_block("Estudio", "PUCP", 12)
    save(estudio, "estudio-ink")

    rol = form_block("Rol", "IBM", 44)
    save(rol, "rol-ink")


if __name__ == "__main__":
    main()
