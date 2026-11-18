import os
import html

STATIC = os.environ.get("STATIC") == "1"

ROWS = [
    ("OS", "AI Engineer · Production RAG & Agents"),
    ("Host", "Lucknow, India (IST)"),
    ("Kernel", "Python · PyTorch · LangChain · LangGraph"),
    ("Memory", "FAISS · ChromaDB · SQLite · MySQL"),
    ("Engine", "Groq · CLIP · Quantization & Serving"),
    ("Uptime", "Multi-Agent Research & Self-Correcting RAG"),
    ("Shell", "Docker · Linux · Git · Streamlit"),
    ("Web", "pawansani.lovable.app"),
    ("Mail", "pawan.sani321@gmail.com"),
]

WIDTH = 490
HEIGHT = 330

svg = [
    f'<svg xmlns="http://w3.org" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
    '<style>',
    '  .bg { fill: #0d1117; stroke: #30363d; stroke-width: 1; }',
    '  .bar { fill: #161b22; }',
    '  .title { font-family: monospace; font-size: 12px; fill: #8b949e; }',
    '  .prompt { font-family: monospace; font-size: 13px; font-weight: bold; fill: #58a6ff; }',
    '  .key { font-family: monospace; font-size: 12.5px; font-weight: bold; fill: #39d353; }',
    '  .val { font-family: monospace; font-size: 12.5px; fill: #c9d1d9; }',
    '  @keyframes fadeSlide {',
    '    from { opacity: 0; transform: translateX(-8px); }',
    '    to { opacity: 1; transform: translateX(0); }',
    '  }',
    '  .row { opacity: 0; animation: fadeSlide 0.35s ease-out forwards; }',
    '  .static { opacity: 1 !important; animation: none !important; }',
    '</style>',
    f'<rect class="bg" width="{WIDTH}" height="{HEIGHT}" rx="8"/>',
    f'<path class="bar" d="M 8 0 H {WIDTH - 8} Q {WIDTH} 0 {WIDTH} 8 V 28 H 0 V 8 Q 0 0 8 0 Z"/>',
    '<circle cx="18" cy="14" r="5" fill="#ff5f56"/>',
    '<circle cx="34" cy="14" r="5" fill="#ffbd2e"/>',
    '<circle cx="50" cy="14" r="5" fill="#27c93f"/>',
    f'<text x="{WIDTH // 2}" y="18" text-anchor="middle" class="title">pawan@github — neofetch</text>',
    '<text x="20" y="54" class="prompt">pawan@github ~ $ neofetch --ai-stack</text>',
]

start_y = 82
line_gap = 24

for i, (k, v) in enumerate(ROWS):
    y = start_y + i * line_gap
    delay = round(0.15 + i * 0.12, 2)
    cls = "row static" if STATIC else "row"
    style = "" if STATIC else f'style="animation-delay: {delay}s;"'
    svg.append(
        f'<g class="{cls}" {style}>'
        f'<text x="20" y="{y}" class="key">{html.escape(k)}:</text>'
        f'<text x="95" y="{y}" class="val">{html.escape(v)}</text>'
        f'</g>'
    )

palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
swatch_y = start_y + len(ROWS) * line_gap + 6
for idx, color in enumerate(palette):
    svg.append(f'<rect x="{20 + idx * 24}" y="{swatch_y}" width="18" height="10" rx="2" fill="{color}"/>')

svg.append('</svg>')

with open("info-card.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))

print("Saved info-card.svg")
