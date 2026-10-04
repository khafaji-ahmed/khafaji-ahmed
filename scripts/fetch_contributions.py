#!/usr/bin/env python3
"""Fetch the public GitHub contribution calendar without a token."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "profile.json"
OUTPUT_PATH = ROOT / "data" / "contributions.json"
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9-]{1,39}$")
COUNT_PATTERN = re.compile(r"([\d,]+)\s+contributions?", re.IGNORECASE)


class CalendarParser(HTMLParser):
    """Read daily counts from GitHub's day cells and linked tooltips."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.days: dict[str, dict] = {}
        self.tooltip_for: str | None = None
        self.tooltip_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        day_string = values.get("data-date")
        if tag == "td" and day_string:
            try:
                parsed_date = date.fromisoformat(day_string)
                level = max(0, min(4, int(values.get("data-level") or "0")))
            except (ValueError, TypeError):
                return
            self.days[values.get("id") or day_string] = {
                "date": parsed_date.isoformat(),
                "level": level,
                "count": 0,
            }
        elif tag == "tool-tip" and values.get("for"):
            self.tooltip_for = values["for"]
            self.tooltip_text = []

    def handle_data(self, data: str) -> None:
        if self.tooltip_for:
            self.tooltip_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "tool-tip" or not self.tooltip_for:
            return
        day = self.days.get(self.tooltip_for)
        if day:
            match = COUNT_PATTERN.search(" ".join(self.tooltip_text))
            if match:
                day["count"] = int(match.group(1).replace(",", ""))
        self.tooltip_for = None
        self.tooltip_text = []


def contribution_stats(days: list[dict]) -> dict:
    active = {date.fromisoformat(item["date"]) for item in days if item["count"] > 0}

    longest = current = 0
    previous = None
    for current_day in sorted(active):
        current = current + 1 if previous and current_day == previous + timedelta(days=1) else 1
        longest = max(longest, current)
        previous = current_day

    today = date.today()
    cursor = today if today in active else today - timedelta(days=1)
    streak = 0
    while cursor in active:
        streak += 1
        cursor -= timedelta(days=1)

    monthly: dict[str, int] = defaultdict(int)
    for item in days:
        monthly[item["date"][:7]] += item["count"]

    best = max(days, key=lambda item: item["count"], default=None)
    return {
        "current_streak": streak,
        "longest_streak": longest,
        "best_day": best["date"] if best else None,
        "best_day_count": best["count"] if best else 0,
        "monthly": dict(sorted(monthly.items())),
    }


def main() -> None:
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    username = str(profile.get("username") or "").strip()
    if not USERNAME_PATTERN.fullmatch(username) or username.upper() == "YOUR_GITHUB_USERNAME":
        raise SystemExit("Set your GitHub username in profile.json before fetching contributions.")

    url = f"https://github.com/users/{username}/contributions"
    response = requests.get(
        url,
        headers={"User-Agent": "github-profile-readme-art/1.0", "Accept": "text/html"},
        timeout=30,
    )
    response.raise_for_status()

    parser = CalendarParser()
    parser.feed(response.text)
    days = sorted(parser.days.values(), key=lambda item: item["date"])
    if not days:
        raise SystemExit(f"No contribution days found at {url}; GitHub may have changed its page markup.")

    total_match = re.search(r"([\d,]+)\s+contributions?\s+in the last year", response.text, re.IGNORECASE)
    total = int(total_match.group(1).replace(",", "")) if total_match else sum(item["count"] for item in days)
    payload = {
        "username": username,
        "total_last_year": total,
        "days": days,
        "stats": contribution_stats(days),
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(days)} days for @{username}: {total:,} contributions in the last year.")


if __name__ == "__main__":
    main()
