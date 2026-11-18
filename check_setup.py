"""Verify the profile-art setup before you commit.

    python check_setup.py

Run it from the repo root. It checks the things that actually break a GitHub
profile page — wrong SVG namespace, missing files, a README that points at an
image which isn't there — and prints PASS/FAIL per line. Exit code is 1 if
anything failed.
"""

from __future__ import annotations

import json
import re
import sys
import xml.dom.minidom as minidom
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SVG_NS = "http://www.w3.org/2000/svg"

# file -> (minimum plausible bytes, why)
SVGS = {
    "pawan-ascii.svg": (40_000, "ASCII portrait, ~64 KB"),
    "info-card.svg": (3_000, "neofetch card, ~3.4 KB"),
    "contrib-heatmap.svg": (40_000, "heatmap, ~67 KB"),
}
SCRIPTS = [
    "prep_photo.py",
    "make_ascii_svg.py",
    "make_info_card.py",
    "fetch_contributions.py",
    "render_heatmap_svg.py",
    "requirements.txt",
]
WORKFLOWS = ["update-profile-art.yml", "snake.yml"]

fails = 0
warns = 0


def ok(msg: str) -> None:
    print(f"  PASS  {msg}")


def bad(msg: str) -> None:
    global fails
    fails += 1
    print(f"  FAIL  {msg}")


def warn(msg: str) -> None:
    global warns
    warns += 1
    print(f"  WARN  {msg}")


def check_svgs() -> None:
    print("\nSVG art")
    for name, (min_bytes, note) in SVGS.items():
        p = ROOT / name
        if not p.exists():
            bad(f"{name} is missing ({note})")
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        size = p.stat().st_size
        m = re.search(r'xmlns="([^"]+)"', raw)
        ns = m.group(1) if m else "(none)"
        if ns != SVG_NS:
            bad(f"{name} has xmlns={ns!r} — must be {SVG_NS!r}")
        if size < min_bytes:
            bad(f"{name} is only {size:,} B — expected {note}. That size means "
                f"the old tutorial file, not the generated one")
        try:
            minidom.parseString(raw)
        except Exception as exc:  # noqa: BLE001
            bad(f"{name} is not valid XML: {exc}")
        if ns == SVG_NS and size >= min_bytes:
            ok(f"{name} ({size:,} B, correct namespace)")


def check_scripts() -> None:
    print("\nScripts")
    for name in SCRIPTS:
        p = ROOT / "scripts" / name
        if not p.exists():
            bad(f"scripts/{name} is missing")
            continue
        head = p.read_text(encoding="utf-8", errors="replace")[:400]
        if name.endswith(".py") and not head.lstrip().startswith('"""'):
            warn(f"scripts/{name} has no module docstring — looks like the "
                 f"tutorial version, not the generated one")
    if all((ROOT / "scripts" / n).exists() for n in SCRIPTS):
        ok(f"all {len(SCRIPTS)} script files present")


def check_workflows() -> None:
    print("\nWorkflows")
    for name in WORKFLOWS:
        p = ROOT / ".github" / "workflows" / name
        if not p.exists():
            bad(f".github/workflows/{name} is missing")
        else:
            ok(f"{name}")


def check_data() -> None:
    print("\nData")
    p = ROOT / "data" / "contributions.json"
    if not p.exists():
        bad("data/contributions.json is missing — run scripts/fetch_contributions.py")
        return
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        bad(f"data/contributions.json is not valid JSON: {exc}")
        return
    days = d.get("days") or d.get("contributions") or []
    if not days:
        bad("data/contributions.json has no day records")
    elif "stats" not in d:
        warn("data/contributions.json has no 'stats' block — the heatmap footer "
             "will be blank; re-run fetch_contributions.py")
    else:
        ok(f"{len(days)} days, total {d.get('total')}, "
           f"{d['stats'].get('current_streak')}d current streak")


def check_readme() -> None:
    print("\nREADME")
    p = ROOT / "README.md"
    if not p.exists():
        bad("README.md is missing")
        return
    text = p.read_text(encoding="utf-8", errors="replace")
    for ref, why in (
        ('src="./pawan-ascii.svg"', "portrait"),
        ('src="./info-card.svg"', "info card"),
        ('src="./contrib-heatmap.svg"', "heatmap"),
    ):
        if ref in text:
            ok(f"references the {why}")
        else:
            bad(f"README does not reference the {why} ({ref})")
    if "Contribution Activity" in text:
        warn("README still has the old empty '## Contribution Activity' section")


def check_gitignore() -> None:
    print("\n.gitignore")
    p = ROOT / ".gitignore"
    if not p.exists():
        bad(".gitignore is missing — `git add -A` would commit .venv/")
        return
    text = p.read_text(encoding="utf-8", errors="replace")
    for pat in (".venv", "__pycache__"):
        if pat in text:
            ok(f"ignores {pat}")
        else:
            bad(f"does not ignore {pat}")


def main() -> None:
    print(f"Checking {ROOT}")
    check_svgs()
    check_scripts()
    check_workflows()
    check_data()
    check_readme()
    check_gitignore()

    print()
    if fails:
        print(f"{fails} problem(s) found, {warns} warning(s). Fix the FAILs "
              f"before committing.")
        sys.exit(1)
    print(f"All checks passed ({warns} warning(s)). Safe to commit.")


if __name__ == "__main__":
    main()
