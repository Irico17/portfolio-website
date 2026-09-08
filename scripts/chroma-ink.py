"""Chroma-key magenta generated inks to alpha PNGs, then crop and decontaminate."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ORIGIN = Path(r"C:\Users\Irico\.cursor\projects\c-Users-Irico-Documents-portfolio-website\assets")
SRC = Path(__file__).resolve().parents[1] / "src" / "assets" / "plates"


def is_key(r: int, g: int, b: int) -> bool:
    magenta = r > 160 and b > 130 and g < 150 and (r - g) > 35
    white = r > 232 and g > 232 and b > 232
    return magenta or white


def chroma(src: Path, name: str, box: tuple[int, int, int, int] | None = None) -> None:
    im = Image.open(src).convert("RGBA")
    if box:
        im = im.crop(box)
    px = im.load()
    w, h = im.size
    kept = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if is_key(r, g, b):
                px[x, y] = (r, g, b, 0)
            else:
                kept += 1
    dest = SRC / name
    im.save(dest, "PNG")
    print(f"{name} {im.size} opaque {kept / (w * h):.0%}")


def decontaminate_toner(im: Image.Image) -> tuple[Image.Image, int]:
    """Drop leftover magenta fringe on black xerox lettering; keep indigo/biro."""
    px = im.load()
    w, h = im.size
    cleared = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            magenta_fringe = r > 48 and b > 36 and g < 110 and (r - g) > 22 and (b - g) > 12
            if magenta_fringe:
                px[x, y] = (0, 0, 0, 0)
                cleared += 1
                continue
            purple_tint = r > g + 18 and b > g + 8 and r > 28 and g < 80
            if purple_tint:
                yv = int(0.21 * r + 0.72 * g + 0.07 * b)
                px[x, y] = (yv, yv, yv, a)
                cleared += 1
    return im, cleared


def crop_opaque(im: Image.Image, pad_ratio: float = 0.03) -> Image.Image:
    bbox = im.getbbox()
    if not bbox:
        return im
    w, h = im.size
    left, top, right, bottom = bbox
    pad_x = max(4, int((right - left) * pad_ratio))
    pad_y = max(4, int((bottom - top) * pad_ratio))
    box = (
        max(0, left - pad_x),
        max(0, top - pad_y),
        min(w, right + pad_x),
        min(h, bottom + pad_y),
    )
    return im.crop(box)


def tighten(name: str, toner: bool = False) -> None:
    path = SRC / name
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a and is_key(r, g, b):
                px[x, y] = (r, g, b, 0)
    cleared = 0
    if toner:
        im, cleared = decontaminate_toner(im)
    im = crop_opaque(im)
    im.save(path, "PNG")
    opaque = sum(1 for p in im.getdata() if p[3] > 20)
    print(f"tighten {name} {im.size} opaque {opaque / (im.size[0] * im.size[1]):.0%} cleared {cleared}")


def main() -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    gens = {
        "trabajo-ink-gen.png": "trabajo-ink.png",
        "contacto-ink-gen.png": "contacto-ink.png",
        "tagline-biro-gen.png": "tagline-biro.png",
        "proyecto02-ink-gen.png": "proyecto02-ink.png",
    }
    if all((ORIGIN / src).exists() for src in gens):
        for src, dest in gens.items():
            chroma(ORIGIN / src, dest)
        scraps = ORIGIN / "contact-scraps-gen.png"
        if scraps.exists():
            img = Image.open(scraps)
            w, h = img.size
            chroma(scraps, "linkedin-scrap.png", (0, 0, w // 2, h))
            chroma(scraps, "github-scrap.png", (w // 2, 0, w, h))
    tighten("trabajo-ink.png", toner=True)
    tighten("contacto-ink.png", toner=True)
    tighten("tagline-biro.png", toner=False)
    tighten("proyecto02-ink.png", toner=False)


if __name__ == "__main__":
    main()
