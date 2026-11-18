from PIL import Image
import html

RAMP = " .`:-=+*cs#%@"
COLS = 80
ROWS = 65
FONT_SIZE = 7
LINE_HEIGHT = 8.5
CHAR_WIDTH = 4.2

img = Image.open("source-prepped.png").convert("L").resize((COLS, ROWS))
pixels = list(img.getdata())

lines = []
for r in range(ROWS):
    row_chars = []
    for c in range(COLS):
        brightness = pixels[r * COLS + c]
        idx = int((255 - brightness) / 256 * len(RAMP))
        idx = max(0, min(len(RAMP) - 1, idx))
        row_chars.append(RAMP[idx])
    lines.append("".join(row_chars))

width = int(COLS * CHAR_WIDTH) + 20
height = int(ROWS * LINE_HEIGHT) + 20

svg_parts = [
    f'<svg xmlns="http://w3.org" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" fill="#0d1117" rx="8"/>',
    '<defs>'
]

for r in range(ROWS):
    delay = round(r * 0.04, 2)
    svg_parts.append(
        f'<clipPath id="clip-{r}"><rect x="10" y="{10 + r * LINE_HEIGHT}" width="0" height="{LINE_HEIGHT + 2}">'
        f'<animate attributeName="width" from="0" to="{width}" dur="0.35s" begin="{delay}s" fill="freeze"/>'
        f'</rect></clipPath>'
    )

svg_parts.append('</defs>')
svg_parts.append(f'<g font-family="monospace" font-size="{FONT_SIZE}" fill="#c9d1d9" xml:space="preserve">')

for r, line in enumerate(lines):
    y = round(10 + (r + 1) * LINE_HEIGHT - 2, 1)
    escaped = html.escape(line)
    svg_parts.append(f'<text x="10" y="{y}" clip-path="url(#clip-{r})">{escaped}</text>')

svg_parts.append('</g></svg>')

with open("pawan-ascii.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg_parts))

print("Saved pawan-ascii.svg")
