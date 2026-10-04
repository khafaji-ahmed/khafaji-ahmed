#!/usr/bin/env python3
"""Hand-author a neofetch-style info card as a self-animating SVG.

A title bar, then colored key/value rows. Each line fades and slides in on
a short stagger so the panel looks like it's printing next to the portrait.
Keep the story here that the contribution graph's numbers can't tell.

Usage: python scripts/make_info_card.py
Env:   STATIC=1 emits a frozen frame (no animation) for local previews.
"""

from __future__ import annotations

import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

# ── edit these rows ────────────────────────────────────────────────────────
CARD = {
    "title": "khafaji-ahmed",
    "subtitle": "~/profile — neofetch",
    "rows": [
        ("role", "Founder & Senior Architect", "#39d353"),
        ("prev", "Senior web & mobile app engineer", "#58a6ff"),
        ("stack", "C · C++ · C# · Python · TypeScript · Swift · React · AWS", "#d2a8ff"),
        ("contact", "linkedin.com/in/ahmed-khafaji", "#f778ba"),
    ],
}
# ───────────────────────────────────────────────────────────────────────────

BG = "#0d1117"
BORDER = "#21262d"
TITLE_BAR = "#161b22"
KEY = "#8b949e"
VALUE = "#e6edf3"
DOT_RED, DOT_YEL, DOT_GRN = "#ff5f56", "#ffbd2e", "#27c93f"

WIDTH = 490
TITLE_H = 34
ROW_H = 30
PAD_B = 18
HEIGHT = TITLE_H + len(CARD["rows"]) * ROW_H + PAD_B
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

STATIC = os.environ.get("STATIC") == "1"


def render() -> str:
    rows = []
    # terminal window dots
    for i, dot in enumerate((DOT_RED, DOT_YEL, DOT_GRN)):
        rows.append(f'<circle cx="{16 + i * 18}" cy="17" r="5" fill="{dot}"/>')
    rows.append(
        f'<text x="{70}" y="21" font-family="{FONT}" font-size="12" fill="{KEY}">{escape(CARD["subtitle"])}</text>'
    )
    # blinking cursor next to the title
    rows.append(
        f'<rect class="cursor" x="{70 + len(CARD["subtitle"]) * 7.2 + 6}" y="11" width="7" height="14" fill="#39d353"/>'
    )

    for i, (key, value, color) in enumerate(CARD["rows"]):
        y = TITLE_H + i * ROW_H + 20
        delay = 150 + i * 130
        rows.append(
            f'<g class="line" style="animation-delay:{delay}ms">'
            f'<rect x="14" y="{y - 11}" width="8" height="8" rx="2" fill="{color}"/>'
            f'<text x="30" y="{y}" font-family="{FONT}" font-size="13" fill="{KEY}">{escape(key)}</text>'
            f'<text x="110" y="{y}" font-family="{FONT}" font-size="13" fill="{VALUE}">{escape(value)}</text>'
            f"</g>"
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="Info card">
<style>
.line {{ opacity: 0; transform: translateY(6px); animation: print .5s cubic-bezier(.2,.7,.3,1) forwards; }}
@keyframes print {{ to {{ opacity: 1; transform: translateY(0); }} }}
.cursor {{ animation: blink 1.1s step-end infinite; }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
.title {{ animation: fade .4s ease forwards; opacity: 0; }}
@keyframes fade {{ to {{ opacity: 1; }} }}
</style>
<rect width="100%" height="100%" rx="10" fill="{BG}" stroke="{BORDER}"/>
<rect width="100%" height="{TITLE_H}" rx="10" fill="{TITLE_BAR}"/>
<rect x="0" y="{TITLE_H - 10}" width="100%" height="10" fill="{TITLE_BAR}"/>
<g class="title">{''.join(rows[:4])}</g>
{''.join(rows[4:])}
</svg>
"""


def main() -> None:
    out = ROOT / "info-card.svg"
    out.write_text(render(), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
