#!/usr/bin/env python3
"""One-time photo prep for the ASCII portrait.

A flatly-lit face converts to a dark, unreadable blob, so before the ASCII
conversion the photo is:

1. background-removed (rembg) so the subject is isolated,
2. contrast-boosted with OpenCV CLAHE — this gives a flat face real
   highlights and shadows,
3. composited onto pure white so the background maps to the blank end of
   the ASCII ramp (white -> spaces).

Output: source-prepped.png (grayscale) next to the input.

Usage: python scripts/prep_photo.py source-photo.jpg
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def main(src: Path) -> None:
    img = Image.open(src).convert("RGB")

    cut = remove(img)  # RGBA with transparent background
    rgba = np.array(cut)
    alpha = rgba[..., 3:4].astype(np.float32) / 255.0
    rgb = rgba[..., :3].astype(np.float32)
    on_white = (rgb * alpha + 255.0 * (1 - alpha)).astype(np.uint8)

    gray = cv2.cvtColor(on_white, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    boosted = clahe.apply(gray)

    out = src.parent / "source-prepped.png"
    Image.fromarray(boosted).save(out)
    print(f"wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python scripts/prep_photo.py source-photo.jpg", file=sys.stderr)
        raise SystemExit(1)
    main(Path(sys.argv[1]))
