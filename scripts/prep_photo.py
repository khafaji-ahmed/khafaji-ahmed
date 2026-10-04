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

Usage:
    python scripts/prep_photo.py source-photo.jpg          # rembg background removal
    python scripts/prep_photo.py source-photo.jpg --flat-bg
                                                             # key the flat background by
                                                             # colour instead (fast, no model
                                                             # download — good for 3D avatars)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def key_flat_bg(img: Image.Image, tol: int = 40) -> np.ndarray:
    """Composite a flat-colour background to white without rembg.

    Uses the median border pixel as the background colour, then whites out
    everything within `tol`. Fast and artefact-free for studio/3D renders,
    where the backdrop is a single flat tone.
    """
    rgb = np.array(img.convert("RGB")).astype(np.float32)
    border = np.concatenate(
        [rgb[0, :, :], rgb[-1, :, :], rgb[:, 0, :], rgb[:, -1, :]], axis=0
    )
    bg = np.median(border, axis=0)
    dist = np.linalg.norm(rgb - bg, axis=2)
    mask = (dist < tol)[..., None]
    return np.where(mask, 255.0, rgb).astype(np.uint8)


def main(src: Path, flat_bg: bool) -> None:
    img = Image.open(src).convert("RGB")

    if flat_bg:
        on_white = key_flat_bg(img)
    else:
        from rembg import remove  # lazy: only needed for the rembg path

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
    p = argparse.ArgumentParser(description="Prep a photo for the ASCII portrait.")
    p.add_argument("source", type=Path)
    p.add_argument(
        "--flat-bg",
        action="store_true",
        help="key a flat background by colour instead of running rembg",
    )
    a = p.parse_args()
    if not a.source.exists():
        print(f"missing {a.source}", file=sys.stderr)
        raise SystemExit(1)
    main(a.source, a.flat_bg)
