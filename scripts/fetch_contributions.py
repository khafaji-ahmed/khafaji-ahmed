#!/usr/bin/env python3
"""Scrape the public contribution calendar for a GitHub user.

No API token needed: github.com/users/<username>/contributions serves the
same calendar fragment the profile page uses. Each day cell carries a
data-level (0-4) and a tooltip with the exact count.

Writes data/contributions.json with the raw days plus derived stats
(current streak, longest streak, best day, monthly totals).

Usage: python scripts/fetch_contributions.py
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "khafaji-ahmed"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "contributions.json"


def fetch(username: str) -> str:
    url = f"https://github.com/users/{username}/contributions"
    r = requests.get(url, timeout=30, headers={"User-Agent": "profile-readme-bot/1.0"})
    r.raise_for_status()
    if "ContributionCalendar-day" not in r.text:
        raise RuntimeError("Contribution calendar not found in page — structure may have changed.")
    return r.text


def _streak_ending(by_date: dict[str, int], end: date) -> int:
    """Consecutive active days ending today; falls back to yesterday (today
    may still be 0 early in the day)."""
    for offset in (0, 1):
        d = end - timedelta(days=offset)
        streak = 0
        while by_date.get(d.isoformat(), 0) > 0:
            streak += 1
            d -= timedelta(days=1)
        if streak > 0 or offset == 1:
            return streak
    return 0


def _longest_streak(by_date: dict[str, int]) -> int:
    active = sorted(d for d, c in by_date.items() if c > 0)
    best = cur = 0
    prev = None
    for iso in active:
        d = date.fromisoformat(iso)
        cur = cur + 1 if prev and (d - prev).days == 1 else 1
        best = max(best, cur)
        prev = d
    return best


def parse(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    total_match = re.search(r"([\d,]+)\s+contributions?\s+in the last year", html)
    total = int(total_match.group(1).replace(",", "")) if total_match else None

    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        day_date = td.get("data-date")
        if not day_date:
            continue
        level = int(td.get("data-level", "0"))
        count = 0
        tip = soup.find("tool-tip", attrs={"for": td.get("id")})
        if tip:
            m = re.search(r"(\d+)\s+contribution", tip.get_text())
            if m:
                count = int(m.group(1))
        days.append({"date": day_date, "level": level, "count": count})

    if not days:
        raise RuntimeError("No contribution day cells found.")

    days.sort(key=lambda d: d["date"])
    by_date = {d["date"]: d["count"] for d in days}

    best = max(days, key=lambda d: d["count"])
    monthly: dict[str, int] = defaultdict(int)
    for d in days:
        monthly[d["date"][:7]] += d["count"]

    return {
        "username": USERNAME,
        "total_last_year": total,
        "days": days,
        "stats": {
            "current_streak": _streak_ending(by_date, date.today()),
            "longest_streak": _longest_streak(by_date),
            "best_day": best["date"],
            "best_day_count": best["count"],
            "monthly": dict(sorted(monthly.items())),
        },
    }


def main() -> None:
    data = parse(fetch(USERNAME))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2), encoding="utf-8")
    s = data["stats"]
    print(f"wrote {OUT}  ({len(data['days'])} days)")
    print(
        f"total={data['total_last_year']}  "
        f"current_streak={s['current_streak']}  "
        f"longest={s['longest_streak']}  "
        f"best={s['best_day']} ({s['best_day_count']})"
    )


if __name__ == "__main__":
    main()
