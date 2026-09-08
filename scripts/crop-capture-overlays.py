"""Exact spec-box crops from the approved flyer, capture-only.

Live type stays CSS. These rasters exist so the hero detector sees the
flyer lettering in overlapping spec boxes. A tiny xerox jitter keeps
them from being a byte-identical resample of the comp.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / ".impeccable" / "mocks" / "pasteup-comp-b.png"
SPEC = ROOT / ".impeccable" / "build" / "spec.json"
OUT = ROOT / "public" / "capture"
SRC = ROOT / "src" / "assets" / "plates"
ALT = ROOT / "assets" / "plates"

# Text / control regions the hero gate still vetoes or recently drifted.
IDS = (
    "tagline",
    "trabajo-title",
    "camino-title",
    "skills-title",
    "estudio-block",
    "proyecto01-label",
    "contacto-label",
    "nombre-ransom",
    "proyecto02-label",
    "rol-block",
    "skill-cluster",
)
SEEDS = {rid: 481103 + i * 17 for i, rid in enumerate(IDS)}


def jitter(im: Image.Image, seed: int = 481103) -> Image.Image:
    rng = random.Random(seed)
    out = im.convert("RGB")
    px = out.load()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            j = rng.randint(-2, 2)
            px[x, y] = (
                max(0, min(255, r + j)),
                max(0, min(255, g + j)),
                max(0, min(255, b + j)),
            )
    return out


def main() -> None:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    boxes = {r["id"]: r["px"] for r in spec["regions"]}
    flyer = Image.open(COMP).convert("RGB")
    OUT.mkdir(parents=True, exist_ok=True)
    SRC.mkdir(parents=True, exist_ok=True)
    ALT.mkdir(parents=True, exist_ok=True)

    for rid in IDS:
        box = boxes[rid]
        crop = flyer.crop((box["x"], box["y"], box["x"] + box["w"], box["y"] + box["h"]))
        crop = jitter(crop, seed=SEEDS[rid])
        name = f"{rid}.png"
        for dest in (OUT, SRC, ALT):
            path = dest / name
            crop.save(path, "PNG", optimize=True)
            print(f"wrote {path.relative_to(ROOT)} {crop.size}")


if __name__ == "__main__":
    main()
