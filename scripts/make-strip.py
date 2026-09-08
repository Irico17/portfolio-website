"""Build a gray-xerox + day-glo pink band strip at the spec aspect."""
from pathlib import Path
import random

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
W, H = 1844, 308
GRAY = (203, 199, 194)
PINK = (231, 72, 121)


def noisy(base: tuple[int, int, int], amp: int = 14) -> tuple[int, int, int]:
    n = random.randint(-amp, amp)
    return tuple(max(0, min(255, c + n)) for c in base)


def main() -> None:
    random.seed(481103)
    im = Image.new("RGB", (W, H))
    px = im.load()
    y0 = int(H * 0.5)
    y1 = int(H * 0.92)
    for y in range(H):
        jagged = int(3 * ((y % 7) - 3))
        top = y0 + jagged
        bot = y1 + int(2 * ((y % 5) - 2))
        for x in range(W):
            edge = 8 if 18 < x < W - 22 else 0
            if top + edge <= y <= bot - edge:
                px[x, y] = noisy(PINK, 18)
            else:
                px[x, y] = noisy(GRAY, 16)
    for dest in (ROOT / "src" / "assets" / "plates", ROOT / "assets" / "plates"):
        path = dest / "proyecto01-strip.png"
        im.save(path, "PNG")
        print("wrote", path, im.size)


if __name__ == "__main__":
    main()
