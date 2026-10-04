#!/usr/bin/env python3
"""Build the animated terminal card from profile.json."""

from __future__ import annotations

import json
import os
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
OUT = ROOT / "info-card.svg"

WIDTH = 490
TITLE_H = 34
ROW_H = 30
ROWS = 5
HEIGHT = TITLE_H + ROWS * ROW_H + 18
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
COLORS = ("#39d353", "#58a6ff", "#d2a8ff", "#e3b341", "#f778ba")


def profile_rows() -> list[tuple[str, str]]:
    stack = PROFILE.get("stack", [])
    first = " · ".join(stack[:4])
    second = " · ".join(stack[4:])
    return [
        ("now", str(PROFILE.get("role", ""))),
        ("prev", str(PROFILE.get("previous", ""))),
        ("stack", first),
        ("also", second),
        ("contact", str(PROFILE.get("contact", ""))),
    ]


def main() -> None:
    username = escape(str(PROFILE.get("username", "khafaji-ahmed")))
    static = os.getenv("STATIC") == "1"
    styles = (
        "<style>.title{opacity:1}.cursor{opacity:1}</style>"
        if static
        else '<style>.line{opacity:0;transform:translateY(6px);animation:print .5s cubic-bezier(.2,.7,.3,1) forwards}@keyframes print{to{opacity:1;transform:translateY(0)}}.cursor{animation:blink 1.1s step-end infinite}@keyframes blink{50%{opacity:0}}.title{animation:fade .4s ease forwards;opacity:0}@keyframes fade{to{opacity:1}}</style>'
    )
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{username} terminal profile</title>',
        '<desc id="desc">Role, previous experience, programming languages, tools and LinkedIn contact.</desc>',
        styles,
        '<rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#21262d"/>',
        f'<rect width="100%" height="{TITLE_H}" rx="10" fill="#161b22"/>',
        f'<rect x="0" y="24" width="100%" height="{TITLE_H - 24}" fill="#161b22"/>',
        '<g class="title">',
        '<circle cx="16" cy="17" r="5" fill="#ff5f56"/><circle cx="34" cy="17" r="5" fill="#ffbd2e"/><circle cx="52" cy="17" r="5" fill="#27c93f"/>',
        '<text x="70" y="21" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="12" fill="#8b949e">~/profile — neofetch</text>',
        '</g>',
        '<rect class="cursor" x="222" y="11" width="7" height="14" fill="#39d353"/>',
    ]
    for index, ((key, value), color) in enumerate(zip(profile_rows(), COLORS)):
        y = TITLE_H + 20 + index * ROW_H
        row = (
            f'<rect x="14" y="{y - 11}" width="8" height="8" rx="2" fill="{color}"/>'
            f'<text x="30" y="{y}" font-family="{FONT}" font-size="13" fill="#8b949e">{escape(key)}</text>'
            f'<text x="110" y="{y}" font-family="{FONT}" font-size="13" fill="#e6edf3">{escape(value)}</text>'
        )
        if static:
            parts.append(f'<g>{row}</g>')
        else:
            parts.append(f'<g class="line" style="animation-delay:{150 + index * 130}ms">{row}</g>')
    parts.append("</svg>")
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
