#!/usr/bin/env python3
"""Build an animated, color-halftone ASCII portrait from source-prepped.png.

The character grid is kept legible over a low-opacity color sample of the same
cell. The tint carries the avatar's soft facial shading, while the contrasting
characters retain the terminal/ASCII look at GitHub's small display size.

Usage: python scripts/make_ascii_svg.py
Env:   STATIC=1 emits a frozen frame for local previews.
"""

from __future__ import annotations

import os
from html import escape
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-prepped.png"
OUT = ROOT / "ahmed-ascii.svg"

COLS = 84
CELL_W, CELL_H = 8, 14
FONT_FAMILY = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
FONT_SIZE = CELL_W / 0.6
RAMP = " .:-=+*#%@"  # sparse to dense
BACKGROUND = "#0d1117"
LIGHT_INK = "#f0f3f6"
DARK_INK = "#10151c"
TILE_OPACITY = 0.70
INK_OPACITY = 0.55
CURSOR_COLOR = "#39d353"
STATIC = os.environ.get("STATIC") == "1"


def sample_grid(img: Image.Image, cols: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rgba = img.convert("RGBA")
    alpha = rgba.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value > 48 else 0).getbbox()
    if bbox:
        left, top, right, bottom = bbox
        margin = max(8, round(max(rgba.size) * 0.015))
        rgba = rgba.crop((
            max(0, left - margin),
            max(0, top - margin),
            min(rgba.width, right + margin),
            min(rgba.height, bottom + margin),
        ))

    aspect = rgba.height / rgba.width
    rows = max(1, round(cols * aspect * (CELL_W / CELL_H)))
    small = rgba.resize((cols, rows), Image.Resampling.LANCZOS)
    pixels = np.asarray(small, dtype=np.float32)
    rgb = pixels[:, :, :3]
    coverage = pixels[:, :, 3] / 255.0
    luminance = (
        0.2126 * rgb[:, :, 0]
        + 0.7152 * rgb[:, :, 1]
        + 0.0722 * rgb[:, :, 2]
    )
    return rgb, coverage, luminance


def row_art(
    row: int,
    rgb: np.ndarray,
    coverage: np.ndarray,
    luminance: np.ndarray,
) -> str:
    rects: list[str] = []
    runs: list[str] = []
    active_color: str | None = None
    run = ""

    for col in range(rgb.shape[1]):
        alpha = float(coverage[row, col])
        value = float(luminance[row, col])

        if alpha >= 0.12:
            color = tuple(int(channel) for channel in np.clip(np.rint(rgb[row, col]), 0, 255))
            tile_color = "#%02x%02x%02x" % color
            rects.append(
                f'<rect x="{col * CELL_W}" y="{row * CELL_H}" '
                f'width="{CELL_W + 0.2}" height="{CELL_H + 0.2}" '
                f'fill="{tile_color}" fill-opacity="{alpha * TILE_OPACITY:.3f}"/>'
            )
            glyph_index = round((1.0 - value / 255.0) * (len(RAMP) - 1))
            glyph = RAMP[glyph_index]
            ink = LIGHT_INK if value < 112 else DARK_INK
        else:
            # Preserve empty cells explicitly; SVG otherwise collapses runs of spaces.
            glyph = " "
            ink = LIGHT_INK

        if ink != active_color and run:
            runs.append(f'<tspan fill="{active_color}">{escape(run)}</tspan>')
            run = ""
        active_color = ink
        run += glyph

    if run:
        runs.append(f'<tspan fill="{active_color}">{escape(run)}</tspan>')

    baseline = row * CELL_H + CELL_H - 3
    text = (
        f'<text xml:space="preserve" x="0" y="{baseline}" '
        f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE:.1f}" '
        f'fill-opacity="{INK_OPACITY}">' + "".join(runs) + "</text>"
    )
    return "".join(rects) + text


def render(rgb: np.ndarray, coverage: np.ndarray, luminance: np.ndarray) -> str:
    rows, cols = coverage.shape
    width = cols * CELL_W
    height = rows * CELL_H
    row_duration = 450
    row_stagger = 70
    body: list[str] = []

    for row in range(rows):
        art = row_art(row, rgb, coverage, luminance)
        if STATIC:
            body.append(f'<g>{art}</g>')
            continue

        delay = row * row_stagger
        body.append(
            f'<g class="row" style="animation-duration:{row_duration}ms;'
            f'animation-delay:{delay}ms">{art}</g>'
        )
        body.append(
            f'<rect class="cursor" style="animation-duration:{row_duration}ms;'
            f'animation-delay:{delay}ms" x="0" y="{row * CELL_H}" '
            f'width="5" height="{CELL_H - 2}" fill="{CURSOR_COLOR}"/>'
        )

    animation = "" if STATIC else f"""
<style>
.row {{ clip-path: inset(0 100% 0 0); animation-name: wipe; animation-timing-function: linear; animation-fill-mode: forwards; }}
@keyframes wipe {{ to {{ clip-path: inset(0 0% 0 0); }} }}
.cursor {{ opacity: 0; animation-name: ride, hide; animation-timing-function: linear, step-end; animation-fill-mode: forwards, forwards; }}
@keyframes ride {{ from {{ transform: translateX(0); }} to {{ transform: translateX({width}px); }} }}
@keyframes hide {{ 0%, 99% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
</style>
"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Animated ASCII portrait of Ahmed Khafaji">
{animation}<rect width="100%" height="100%" fill="{BACKGROUND}"/>
{''.join(body)}
</svg>
"""


def main() -> None:
    if not SRC.exists():
        print(f"missing {SRC} — run: python scripts/prep_photo.py <photo>", file=__import__("sys").stderr)
        raise SystemExit(1)
    image = Image.open(SRC)
    rgb, coverage, luminance = sample_grid(image, COLS)
    OUT.write_text(render(rgb, coverage, luminance), encoding="utf-8")
    print(f"wrote {OUT} ({coverage.shape[0]} rows x {COLS} cols)")


if __name__ == "__main__":
    main()
