# Profile art — setup

Everything in this folder drops straight into your profile repo
(`Pawankumarsani/Pawankumarsani`). Two commands to get it in place, one to
verify, one to publish.

## 1. Extract over the repo root

```powershell
cd E:\PawanKumarSani
Expand-Archive -LiteralPath "<path to this zip>" -DestinationPath . -Force
```

`-Force` overwrites, which is the point: the `pawan-ascii.svg` and
`info-card.svg` already in your repo are the tutorial's files, and they will
never render because their root element says `xmlns="http://w3.org"` instead of
`http://www.w3.org/2000/svg`. Browsers treat every element as unknown and draw
nothing, which is what shows up as a broken-image icon.

## 2. Verify before committing

```powershell
python check_setup.py
```

It checks the SVG namespaces and sizes, that all six script files are present,
both workflows, the JSON data, the README image references and `.gitignore`.
Every line should say PASS. If one says FAIL, the message names the file and
what is wrong with it — do not commit until they are all green.

## 3. Commit

```powershell
git add -A
git status --short          # confirm no .venv/ paths appear
git commit -m "feat: generated SVG art, daily heatmap workflow"
git push
```

## 4. Regenerating the art

Only needed when the inputs change — the SVGs in this folder are already built
from your photo and your live calendar.

```powershell
# portrait (once per photo)
python scripts\prep_photo.py source-photo.jpg data\source-prepped.png
python scripts\make_ascii_svg.py

# info card (when the details change)
python scripts\make_info_card.py

# heatmap (daily, also runs in Actions)
python scripts\fetch_contributions.py
python scripts\render_heatmap_svg.py
```

`prep_photo.py` uses `rembg` and OpenCV when they are installed and falls back
to PIL-only otherwise. Install the portrait extras with
`pip install -r scripts\requirements.txt`; the daily workflow deliberately
installs only `requests` and `beautifulsoup4`.

## 5. First Actions run

The heatmap workflow runs on its cron, but trigger it once by hand to confirm it
commits: **Actions → Update profile art → Run workflow**. For the snake, run
**Actions → Generate Snake → Run workflow** — the first run creates the `output`
branch your README points at, so until then the snake renders as a broken image.
That is expected, not a bug.

## File map

| Path | What it is |
| --- | --- |
| `pawan-ascii.svg` | portrait, 100×89 glyph grid, SMIL row-by-row wipe |
| `info-card.svg` | neofetch panel, staggered fade-in |
| `contrib-heatmap.svg` | 53-week calendar, diagonal reveal, 860×227 |
| `README.md` | terminal-layout profile page |
| `check_setup.py` | the verifier from step 2 |
| `scripts/` | the five generators plus `requirements.txt` |
| `data/contributions.json` | calendar data the heatmap renders |
| `.github/workflows/update-profile-art.yml` | daily heatmap refresh |
| `.github/workflows/snake.yml` | snake animation, 12-hourly |
