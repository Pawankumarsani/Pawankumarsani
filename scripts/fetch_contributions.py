"""Fetch a GitHub contribution calendar and save it as JSON.

Usage:
    python scripts/fetch_contributions.py            # defaults to Pawankumarsani
    python scripts/fetch_contributions.py <username>

Writes data/contributions.json with this shape:

    {
      "username": "Pawankumarsani",
      "fetched_at": "2026-11-18T13:56:24+00:00",
      "total": 123,
      "start": "2025-11-16",
      "end": "2026-11-15",
      "days": [ {"date": "2025-11-16", "count": 0, "level": 0}, ... ]
    }

`level` is GitHub's own 0-4 shade for that day, so the renderer does not have
to recompute bucket thresholds.
"""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

USERNAME = sys.argv[1] if len(sys.argv) > 1 else "Pawankumarsani"

# NOTE the two slashes that matter:
#   https://github.com  +  /users/<name>/contributions
# Concatenating "https://github.com" with the username drops the "/" and DNS
# then tries to resolve the host "github.compawankumarsani".
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"

CELL_RE = re.compile(
    r'<td[^>]*?id="contribution-day-component-(?P<col>\d+)-(?P<row>\d+)"'
    r'[^>]*?data-date="(?P<date>\d{4}-\d{2}-\d{2})"'
    r'[^>]*?data-level="(?P<level>\d)"',
    re.S,
)
# Same attributes can appear in any order, so fall back to a looser pass.
LOOSE_CELL_RE = re.compile(r"<td\b[^>]*>", re.S)
ATTR_RE = {
    "date": re.compile(r'data-date="(\d{4}-\d{2}-\d{2})"'),
    "level": re.compile(r'data-level="(\d)"'),
    "id": re.compile(r'id="contribution-day-component-(\d+)-(\d+)"'),
}
TOOLTIP_RE = re.compile(
    r'<tool-tip[^>]*for="contribution-day-component-(?P<col>\d+)-(?P<row>\d+)"[^>]*>(?P<text>.*?)</tool-tip>',
    re.S,
)
COUNT_RE = re.compile(r"^(?P<n>[\d,]+)\s+contribution")


def fetch(url: str, attempts: int = 3) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; profile-heatmap/1.0)",
        "Accept": "text/html",
    }
    last_error: Exception | None = None
    for i in range(attempts):
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as exc:  # network, DNS, 5xx, 429
            last_error = exc
            if i + 1 < attempts:
                time.sleep(2 * (i + 1))
    raise SystemExit(f"Could not fetch {url}\n  {last_error}")


def parse_counts(html: str) -> dict[tuple[int, int], int]:
    """Map (col,row) -> contribution count, read from the tooltips."""
    counts: dict[tuple[int, int], int] = {}
    for m in TOOLTIP_RE.finditer(html):
        key = (int(m.group("col")), int(m.group("row")))
        text = re.sub(r"<[^>]+>", "", m.group("text")).strip()
        hit = COUNT_RE.match(text)
        counts[key] = int(hit.group("n").replace(",", "")) if hit else 0
    return counts


def parse_days(html: str) -> list[dict]:
    counts = parse_counts(html)
    days: dict[str, dict] = {}

    for tag in LOOSE_CELL_RE.findall(html):
        idm = ATTR_RE["id"].search(tag)
        dm = ATTR_RE["date"].search(tag)
        lm = ATTR_RE["level"].search(tag)
        if not (idm and dm and lm):
            continue
        key = (int(idm.group(1)), int(idm.group(2)))
        days[dm.group(1)] = {
            "date": dm.group(1),
            "count": counts.get(key, 0),
            "level": int(lm.group(1)),
        }

    return [days[d] for d in sorted(days)]


def main() -> None:
    html = fetch(URL)
    days = parse_days(html)
    if not days:
        raise SystemExit(
            "No contribution cells found in the response. GitHub may have "
            "changed its markup or served a rate-limit page."
        )

    payload = {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total": sum(d["count"] for d in days),
        "start": days[0]["date"],
        "end": days[-1]["date"],
        "days": days,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(OUT)  # atomic, so a half-written file never breaks the renderer

    active = sum(1 for d in days if d["count"] > 0)
    print(
        f"{USERNAME}: {payload['total']} contributions over {len(days)} days "
        f"({active} active) {payload['start']} -> {payload['end']}\n"
        f"wrote {OUT}"
    )


if __name__ == "__main__":
    main()
