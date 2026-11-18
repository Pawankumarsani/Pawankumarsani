"""Render data/contributions.json as a GitHub-style contribution heatmap SVG.

Usage:
    python scripts/render_heatmap_svg.py
    python scripts/render_heatmap_svg.py data/contributions.json assets/contribution-heatmap.svg

The SVG is self-contained (no scripts, no external fonts or images), so it
survives GitHub's image proxy and renders inside a README <img> tag.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "contributions.json"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "assets" / "contribution-heatmap.svg"

# GitHub's dark-mode calendar ramp.
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
BG = "#0d1117"
BORDER = "#30363d"
MUTED = "#8b949e"
TEXT = "#c9d1d9"
ACCENT = "#39d353"

CELL = 11
PITCH = 14
RX = 2.5
GUTTER = 34          # room for Mon / Wed / Fri labels
TOP = 26             # room for month labels
PAD = 16
LEGEND_H = 30

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
FONT = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,"
        "sans-serif")


def load(path: Path) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(
            f"{path} not found — run scripts/fetch_contributions.py first."
        )
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path} is not valid JSON: {exc}")


def render(data: dict) -> str:
    days = data.get("days") or data.get("contributions") or []
    if not days:
        raise SystemExit("No day records in the JSON — nothing to draw.")

    total = data.get("total_contributions", data.get("total"))
    if total is None:
        total = sum(d.get("count", 0) for d in days)

    cells = []
    for d in days:
        iso = d["date"]
        count = d.get("count", d.get("contributionCount", 0))
        level = d.get("level", d.get("contributionLevel", 0))
        level = max(0, min(4, int(level)))
        cells.append((date.fromisoformat(iso), count, level))
    cells.sort()

    first, last = cells[0][0], cells[-1][0]
    start_row = (first.weekday() + 1) % 7          # Sun=0 ... Sat=6
    weeks = ((cells[-1][0] - first).days + start_row) // 7 + 1

    grid_w = weeks * PITCH - (PITCH - CELL)
    width = PAD * 2 + GUTTER + grid_w
    height = PAD + TOP + 7 * PITCH - (PITCH - CELL) + LEGEND_H + PAD

    out: list[str] = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}" '
        f'font-family="{FONT}" role="img" '
        f'aria-label="{total} contributions in the last year">'
    )
    out.append(f"<title>{total} contributions in the last year</title>")
    out.append(
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" '
        f'rx="10" fill="{BG}" stroke="{BORDER}"/>'
    )

    x0 = PAD + GUTTER
    y0 = PAD + TOP

    # Month labels, one per column where the month changes and space allows.
    last_label_col = -99
    for col in range(weeks):
        week_start = first.toordinal() - start_row + col * 7
        d = date.fromordinal(week_start)
        # label the column containing the 1st of a month
        for offset in range(7):
            dd = date.fromordinal(week_start + offset)
            if dd.day == 1:
                if col - last_label_col >= 3:
                    out.append(
                        f'<text x="{x0 + col * PITCH}" y="{PAD + 12}" '
                        f'font-size="10" fill="{MUTED}">'
                        f"{MONTHS[dd.month - 1]}</text>"
                    )
                    last_label_col = col
                break

    # Weekday labels on the left.
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(
            f'<text x="{x0 - 6}" y="{y0 + row * PITCH + CELL - 2}" '
            f'font-size="9" fill="{MUTED}" text-anchor="end">{name}</text>'
        )

    # Day cells.
    for iso_day, count, level in cells:
        idx = (iso_day - first).days + start_row
        col, row = divmod(idx, 7)
        x = x0 + col * PITCH
        y = y0 + row * PITCH
        label = f"{count} contribution{'s' if count != 1 else ''} on " \
                f"{iso_day.strftime('%d %b %Y')}"
        out.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RX}" '
            f'fill="{COLORS[level]}"><title>{label}</title></rect>'
        )

    # Footer: total on the left, Less/More legend on the right.
    fy = y0 + 7 * PITCH + 12
    active = sum(1 for _, c, _ in cells if c > 0)
    out.append(
        f'<text x="{PAD}" y="{fy + 9}" font-size="11" fill="{TEXT}">'
        f'<tspan fill="{ACCENT}" font-weight="600">{total}</tspan> '
        f"contributions in the last year "
        f'<tspan fill="{MUTED}">· {active} active days · '
        f"{first.strftime('%d %b %Y')} – {last.strftime('%d %b %Y')}"
        f"</tspan></text>"
    )

    legend_w = 5 * PITCH + 62
    lx = width - PAD - legend_w
    out.append(
        f'<text x="{lx}" y="{fy + 9}" font-size="10" fill="{MUTED}">Less</text>'
    )
    for i, color in enumerate(COLORS):
        out.append(
            f'<rect x="{lx + 30 + i * PITCH}" y="{fy}" width="{CELL}" '
            f'height="{CELL}" rx="{RX}" fill="{color}" stroke="{BORDER}" '
            f'stroke-opacity="0.6"/>'
        )
    out.append(
        f'<text x="{lx + 30 + 5 * PITCH + 2}" y="{fy + 9}" font-size="10" '
        f'fill="{MUTED}">More</text>'
    )

    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    data = load(SRC)
    svg = render(data)
    DST.parent.mkdir(parents=True, exist_ok=True)
    tmp = DST.with_suffix(".svg.tmp")
    tmp.write_text(svg, encoding="utf-8")
    tmp.replace(DST)
    print(f"wrote {DST} ({len(svg):,} bytes, {svg.count('<rect')} rects)")


if __name__ == "__main__":
    main()