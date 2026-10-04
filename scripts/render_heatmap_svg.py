#!/usr/bin/env python3
"""Render data/contributions.json as an animated 53-week heatmap SVG.

Classic GitHub calendar: rounded boxes on a green ramp, revealed with a
diagonal line-after-line slide-down (CSS keyframes that play once on load,
then freeze — no looping). Includes a Less->More legend and a stats footer.

Usage: python scripts/render_heatmap_svg.py
Env:   STATIC=1 emits a frozen frame (no animation) for local previews.
"""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "contributions.json").read_text(encoding="utf-8"))

# none -> brightest (index 5 is a neon accent reserved for the best day)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BG = "#0d1117"
BORDER = "#21262d"
TEXT_DIM = "#7d8590"
TEXT_BRIGHT = "#e6edf3"

CELL = 10
GAP = 3
PITCH = CELL + GAP
GUTTER_L = 30  # weekday labels
GUTTER_T = 22  # month labels
FOOTER_H = 66

STATIC = os.environ.get("STATIC") == "1"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def layout(days: list[dict]) -> list[dict]:
    """Attach grid coordinates: column = week, row = weekday (0=Sunday)."""
    first = date.fromisoformat(days[0]["date"])
    out = []
    for d in days:
        dt = date.fromisoformat(d["date"])
        col = (dt - first).days // 7
        row = (dt.weekday() + 1) % 7  # Sunday-first
        out.append({**d, "col": col, "row": row})
    return out


def month_labels(cells: list[dict]) -> list[tuple[int, str]]:
    """Label a column when the month of its earliest day changes."""
    labels = []
    prev_month = None
    by_col: dict[int, list[dict]] = {}
    for c in cells:
        by_col.setdefault(c["col"], []).append(c)
    for col in sorted(by_col):
        month = int(min(by_col[col], key=lambda c: c["date"])["date"][5:7])
        if month != prev_month:
            labels.append((col, MONTHS[month - 1]))
            prev_month = month
    # avoid collisions: keep labels at least 3 columns apart
    kept = []
    for col, name in labels:
        if not kept or col - kept[-1][0] >= 3:
            kept.append((col, name))
    return kept


def fmt_count(n: int) -> str:
    return f"{n:,}"


def render() -> str:
    cells = layout(DATA["days"])
    stats = DATA["stats"]
    max_col = max(c["col"] for c in cells)
    best_iso = stats["best_day"]

    grid_w = (max_col + 1) * PITCH
    width = GUTTER_L + grid_w + 14
    grid_h = 7 * PITCH
    height = GUTTER_T + grid_h + FOOTER_H
    legend_w = 118
    legend_x = width - legend_w - 10

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="Contribution heatmap">',
        "<style>",
        ".day { opacity: 0; transform: translateY(-7px); animation: drop .4s cubic-bezier(.2,.7,.3,1) forwards; }",
        "@keyframes drop { to { opacity: 1; transform: translateY(0); } }",
        ".fadein { opacity: 0; animation: fade .6s ease forwards; }",
        "@keyframes fade { to { opacity: 1; } }",
        "</style>",
        f'<rect width="100%" height="100%" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        # header + legend
        f'<text class="fadein" x="12" y="15" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="11" fill="{TEXT_DIM}">{DATA["username"]} — contributions</text>',
        f'<g class="fadein" style="animation-delay:.35s">',
        f'<text x="{legend_x}" y="15" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="10" fill="{TEXT_DIM}">Less</text>',
    ]
    for i in range(5):
        parts.append(
            f'<rect x="{legend_x + 34 + i * 15}" y="6" width="10" height="10" rx="2" fill="{PALETTE[i + 1]}"/>'
        )
    parts.append(
        f'<text x="{legend_x + 34 + 5 * 15 + 4}" y="15" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="10" fill="{TEXT_DIM}">More</text></g>'
    )

    # month labels
    for col, name in month_labels(cells):
        parts.append(
            f'<text class="fadein" style="animation-delay:.2s" x="{GUTTER_L + col * PITCH}" y="{GUTTER_T - 8}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="9" fill="{TEXT_DIM}">{name}</text>'
        )

    # weekday labels
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        parts.append(
            f'<text class="fadein" style="animation-delay:.2s" x="0" y="{GUTTER_T + row * PITCH + CELL - 1}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="9" fill="{TEXT_DIM}">{name}</text>'
        )

    # day cells — diagonal stagger, plays once then freezes
    for c in cells:
        x = GUTTER_L + c["col"] * PITCH
        y = GUTTER_T + c["row"] * PITCH
        fill = PALETTE[5] if c["date"] == best_iso else PALETTE[min(c["level"], 4)]
        delay = (c["col"] + c["row"]) * 14
        cls = "day" if not STATIC else ""
        style = f' style="animation-delay:{delay}ms"' if not STATIC else ""
        parts.append(
            f'<rect class="{cls}"{style} x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{fill}">'
            f'<title>{c["date"]}: {c["count"]} contributions</title></rect>'
        )

    # stats footer
    best_dt = date.fromisoformat(best_iso)
    best_fmt = best_dt.strftime("%b %-d, %Y")
    footer_y = GUTTER_T + grid_h + 26
    parts.append(
        f'<text class="fadein" style="animation-delay:.5s" x="12" y="{footer_y}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" fill="{TEXT_BRIGHT}">'
        f'{fmt_count(DATA["total_last_year"])} contributions in the last year</text>'
    )
    parts.append(
        f'<text class="fadein" style="animation-delay:.6s" x="12" y="{footer_y + 22}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" fill="{TEXT_DIM}">'
        f'current streak {stats["current_streak"]} days  ·  longest {stats["longest_streak"]} days  ·  '
        f'best day {best_fmt} ({stats["best_day_count"]})  ·  neon box = best day</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    out = ROOT / "contrib-heatmap.svg"
    out.write_text(render(), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
