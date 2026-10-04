#!/usr/bin/env python3
"""Convert source-prepped.png into a self-typing ASCII portrait SVG.

The prepped image is downsampled to a character grid (~100x53) and each
pixel's brightness picks a glyph from a density ramp — sparse characters for
bright areas, dense ones for dark. Two choices keep it clean instead of
noisy: monochrome (one fill color) and high contrast (busy background washes
out to the space glyph, so only the subject prints).

Animation: each row is wrapped in a horizontal clip that wipes left-to-right
(a cursor block rides the wipe edge), staggered top to bottom. The portrait
prints once and freezes — no looping. Pure CSS keyframes inside the SVG, so
GitHub plays it.

Usage: python scripts/make_ascii_svg.py            # reads source-prepped.png
Env:   STATIC=1 emits a frozen frame for local previews.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-prepped.png"
OUT = ROOT / "ahmed-ascii.svg"

# bright (sparse) -> dark (dense); leading space clears the background
RAMP = " .`:-=+*cs#%@"

COLS = 100
CELL_W, CELL_H = 8, 14  # glyph cell; height > width for terminal aspect
FILL = "#c9d1d9"  # monochrome — per-character rainbow is what makes ASCII portraits look like static
FONT_SIZE = CELL_W / 0.6  # monospace advance ≈ 0.6em, so cells tile exactly
CURSOR_COLOR = "#39d353"

STATIC = os.environ.get("STATIC") == "1"


def to_rows(img: Image.Image, cols: int) -> list[str]:
    rgba = img.convert("RGBA")
    alpha = rgba.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value > 8 else 0).getbbox()
    if bbox:
        left, top, right, bottom = bbox
        margin = max(2, round(max(rgba.size) * 0.015))
        rgba = rgba.crop((
            max(0, left - margin),
            max(0, top - margin),
            min(rgba.width, right + margin),
            min(rgba.height, bottom + margin),
        ))
    white = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    img = Image.alpha_composite(white, rgba).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    aspect = img.height / img.width
    # correct for tall terminal glyphs so the portrait isn't stretched
    rows = max(1, round(cols * aspect * (CELL_W / CELL_H)))
    small = img.resize((cols, rows), Image.Resampling.LANCZOS)
    px = np.asarray(small, dtype=np.float32) / 255.0
    idx = ((1.0 - px) * (len(RAMP) - 1)).round().astype(int)
    return ["".join(RAMP[i] for i in row) for row in idx]


def render(rows: list[str]) -> str:
    width = COLS * CELL_W
    height = len(rows) * CELL_H
    row_dur = 450  # ms per row wipe
    row_delay = 70  # ms stagger between rows

    body = []
    for r, text in enumerate(rows):
        delay = r * row_delay
        if STATIC:
            body.append(
                f'<text x="0" y="{r * CELL_H + CELL_H - 3}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
                f'font-size="{FONT_SIZE:.1f}" fill="{FILL}">{text}</text>'
            )
            continue
        # row group clipped to a left-to-right wipe; the cursor rides the wipe edge
        body.append(
            f'<g class="row" style="animation-duration:{row_dur}ms;animation-delay:{delay}ms">'
            f'<text x="0" y="{r * CELL_H + CELL_H - 3}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="{FONT_SIZE:.1f}" fill="{FILL}">{text}</text></g>'
        )
        body.append(
            f'<rect class="cursor" style="animation-duration:{row_dur}ms;animation-delay:{delay}ms" '
            f'x="0" y="{r * CELL_H}" width="5" height="{CELL_H - 2}" fill="{CURSOR_COLOR}"/>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Animated ASCII portrait of Ahmed Khafaji">
<style>
.row {{ clip-path: inset(0 100% 0 0); animation-name: wipe; animation-timing-function: linear; animation-fill-mode: forwards; }}
@keyframes wipe {{ to {{ clip-path: inset(0 0% 0 0); }} }}
.cursor {{ opacity: 0; animation-name: ride, hide; animation-timing-function: linear, step-end; animation-fill-mode: forwards, forwards; }}
@keyframes ride {{ from {{ transform: translateX(0); }} to {{ transform: translateX({width}px); }} }}
@keyframes hide {{ 0%, 99% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
</style>
<rect width="100%" height="100%" fill="#0d1117"/>
{''.join(body)}
</svg>
"""


def main() -> None:
    if not SRC.exists():
        print(f"missing {SRC} — run: python scripts/prep_photo.py <photo>", file=__import__("sys").stderr)
        raise SystemExit(1)
    rows = to_rows(Image.open(SRC), COLS)
    OUT.write_text(render(rows), encoding="utf-8")
    print(f"wrote {OUT} ({len(rows)} rows x {COLS} cols)")


if __name__ == "__main__":
    main()
