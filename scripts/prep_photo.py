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


def main(src: Path, flat_bg: bool, gamma: float = 0.8, white_pct: float = 99.0, clahe: float = 1.0) -> None:
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

    # CLAHE rescues a flat-lit photo, but on an already well-lit 3D render it
    # amplifies soft shading into mottled mid-tone noise that the ASCII ramp
    # turns to static. Blend it in at whatever strength the source needs.
    if clahe > 0:
        equalized = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
        boosted = cv2.addWeighted(gray, 1.0 - clahe, equalized, clahe, 0.0)
    else:
        boosted = gray

    # --- tone mapping -------------------------------------------------------
    # CLAHE alone leaves near-white clothing sitting at mid grey, which the
    # ASCII ramp turns into a wall of `=`/`S` static. Anchor the white point on
    # the *subject* (the background is already pure white and would otherwise
    # dominate any percentile), then lift highlights with gamma so light areas
    # fall on the blank end of the ramp.
    subject = boosted[boosted < 250]
    if subject.size:
        black = float(np.percentile(subject, 1.0))
        white = float(np.percentile(subject, white_pct))
        x = (boosted.astype(np.float32) - black) / max(white - black, 1.0)
        stretched = (np.clip(x, 0.0, 1.0) ** gamma) * 255.0
    else:
        stretched = boosted.astype(np.float32)

    # --- crop to the subject ------------------------------------------------
    mask = stretched < 250
    ys, xs = np.where(mask)
    if xs.size:
        m = int(0.03 * max(stretched.shape))
        stretched = stretched[
            max(0, ys.min() - m) : min(stretched.shape[0], ys.max() + m + 1),
            max(0, xs.min() - m) : min(stretched.shape[1], xs.max() + m + 1),
        ]

    out = src.parent / "source-prepped.png"
    Image.fromarray(stretched.astype(np.uint8)).save(out)
    print(f"wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Prep a photo for the ASCII portrait.")
    p.add_argument("source", type=Path)
    p.add_argument(
        "--flat-bg",
        action="store_true",
        help="key a flat background by colour instead of running rembg",
    )
    p.add_argument(
        "--clahe",
        type=float,
        default=1.0,
        help="strength of CLAHE local contrast, 0 disables it (use 0 for renders "
        "or images that are already well lit; default 1.0)",
    )
    p.add_argument(
        "--white",
        type=float,
        default=99.0,
        help="white point as a percentile of the subject; lower it to push light "
        "clothing onto blank glyphs (default 99)",
    )
    p.add_argument(
        "--gamma",
        type=float,
        default=0.8,
        help="highlight lift, <1 brightens light clothing toward blank glyphs (default 0.8)",
    )
    a = p.parse_args()
    if not a.source.exists():
        print(f"missing {a.source}", file=sys.stderr)
        raise SystemExit(1)
    main(a.source, a.flat_bg, a.gamma, a.white, a.clahe)
