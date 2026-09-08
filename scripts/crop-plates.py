"""Crop 16:9 generated plates to each region's aspect so object-fit:cover fills the spec box."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = Path(r"C:\Users\Irico\.cursor\projects\c-Users-Irico-Documents-portfolio-website\assets")
SRC = ROOT / "src" / "assets" / "plates"
ALT = ROOT / "assets" / "plates"

TARGETS = {
    "paper-ground": (308, 204),
    "contacto-stamp": (922, 614),
    "trabajo-sheet": (2073, 768),
    "proyecto01-strip": (1844, 308),
    "camino-card": (1612, 460),
    "skills-scrap": (1152, 460),
}


def is_pink(r: int, g: int, b: int) -> bool:
    return r > 160 and g < 150 and b > 60 and (r - g) > 35


def pink_bbox(im: Image.Image) -> tuple[int, int, int, int] | None:
    px = im.load()
    w, h = im.size
    minx, miny, maxx, maxy = w, h, 0, 0
    found = False
    step = 2
    for y in range(0, h, step):
        for x in range(0, w, step):
            r, g, b = px[x, y][:3]
            if is_pink(r, g, b):
                found = True
                if x < minx:
                    minx = x
                if y < miny:
                    miny = y
                if x > maxx:
                    maxx = x
                if y > maxy:
                    maxy = y
    if not found:
        return None
    return (max(0, minx - 8), max(0, miny - 8), min(w, maxx + 8), min(h, maxy + 8))


def cover_crop(im: Image.Image, tw: int, th: int, focus: tuple[float, float] | None = None) -> Image.Image:
    w, h = im.size
    target_ratio = tw / th
    src_ratio = w / h
    if src_ratio > target_ratio:
        nw = int(h * target_ratio)
        nh = h
    else:
        nw = w
        nh = int(w / target_ratio)
    if focus:
        cx = int(w * focus[0])
        cy = int(h * focus[1])
    else:
        cx, cy = w // 2, h // 2
    x0 = max(0, min(w - nw, cx - nw // 2))
    y0 = max(0, min(h - nh, cy - nh // 2))
    crop = im.crop((x0, y0, x0 + nw, y0 + nh))
    return crop.resize((tw, th), Image.Resampling.LANCZOS)


def process(name: str, tw: int, th: int) -> None:
    src = ORIGIN / f"{name}.png"
    if not src.exists():
        src = SRC / f"{name}.png"
    im = Image.open(src).convert("RGB")
    if name in {"proyecto01-strip", "contacto-stamp"}:
        box = pink_bbox(im)
        if box:
            x0, y0, x1, y1 = box
            if name == "proyecto01-strip":
                # Keep gray xerox around the pink so the region is not a solid magenta slab.
                pad_x = int((x1 - x0) * 0.35)
                pad_y = int((y1 - y0) * 0.55)
                x0 = max(0, x0 - pad_x)
                x1 = min(im.width, x1 + pad_x)
                y0 = max(0, y0 - pad_y)
                y1 = min(im.height, y1 + pad_y)
                piece = im.crop((x0, y0, x1, y1))
            else:
                pad = 40
                piece = im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))
            out = cover_crop(piece, tw, th)
        else:
            out = cover_crop(im, tw, th)
    elif name == "paper-ground":
        out = cover_crop(im, tw, th, focus=(0.25, 0.4))
    elif name == "camino-card":
        out = cover_crop(im, tw, th, focus=(0.38, 0.62))
    elif name == "skills-scrap":
        out = cover_crop(im, tw, th, focus=(0.62, 0.38))
    else:
        out = cover_crop(im, tw, th, focus=(0.45, 0.45))
    for dest in (SRC, ALT):
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / f"{name}.png"
        out.save(path, "PNG")
        print(f"wrote {path.relative_to(ROOT)} {out.size}")


def main() -> None:
    for name, size in TARGETS.items():
        process(name, *size)


if __name__ == "__main__":
    main()
