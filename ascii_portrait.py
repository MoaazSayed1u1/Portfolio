"""Compile a reference image into a text-only animated SVG portrait."""

import argparse
import base64
import hashlib
import html
import json
import random
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


CHARACTERS = "  .`',:;i1tfLCG08@"
ROOT = Path(__file__).resolve().parent
# Official brand paths from Simple Icons 16.27.1 (CC0-1.0).
SKILL_ICON_PATHS = json.loads(
    (ROOT / "assets" / "skill-icons.json").read_text(encoding="utf-8-sig")
)
SVG_WIDTH = 2000
SVG_HEIGHT = 2320
PORTRAIT_LEFT = 750
PORTRAIT_TOP = 18
PORTRAIT_WIDTH = 1230
PORTRAIT_COLUMNS = 300
PORTRAIT_ROWS = 525
PORTRAIT_FONT_SIZE = 4.45
PORTRAIT_LINE_HEIGHT = 4.36


def image_rows(image_path):
    image = Image.open(image_path).convert("L")
    image = ImageOps.autocontrast(image, cutoff=1)
    image = ImageEnhance.Contrast(image).enhance(1.22)
    sampled = image.resize(
        (PORTRAIT_COLUMNS, PORTRAIT_ROWS),
        Image.Resampling.LANCZOS,
    )

    output = []
    for y in range(PORTRAIT_ROWS):
        line = []
        for x in range(PORTRAIT_COLUMNS):
            value = sampled.getpixel((x, y))
            normalized = (value / 255) ** 0.78
            index = min(round(normalized * (len(CHARACTERS) - 1)), len(CHARACTERS) - 1)
            line.append(CHARACTERS[index])
        output.append("".join(line))
    return output


def background_streams(digest):
    rng = random.Random(int(digest[:16], 16))
    symbols = ["01", "{}", "[]", "//", "::", "if", "fn", "&&", "||", "<>"]
    streams = []
    for index in range(10):
        x = rng.randint(18, SVG_WIDTH - 30)
        duration = rng.randint(11, 25)
        begin = -rng.randint(0, duration)
        symbol = symbols[index % len(symbols)]
        streams.append(
            f'''<text x="{x}" y="-30" class="stream">{html.escape(symbol)}
  <animate attributeName="y" values="-30;{SVG_HEIGHT + 30}" dur="{duration}s"
    begin="{begin}s" repeatCount="indefinite"/>
</text>'''
        )
    return "\n".join(streams)


def portrait_text(rows):
    """Render every portrait row as one continuous character field."""

    text_rows = []
    for index, row in enumerate(rows):
        y = PORTRAIT_TOP + PORTRAIT_FONT_SIZE + index * PORTRAIT_LINE_HEIGHT
        text_rows.append(
            f'<text x="{PORTRAIT_LEFT}" y="{y:.2f}" '
            f'textLength="{PORTRAIT_WIDTH}" lengthAdjust="spacingAndGlyphs" '
            f'class="portrait">{html.escape(row)}</text>'
        )
    return "".join(text_rows)


def animated_skill_icons(digest):
    """Render recognizable technology marks with lightweight smooth motion."""

    rng = random.Random(int(digest[16:32], 16))
    skills = [
        ("PYTHON", "python"),
        ("PANDAS", "pandas"),
        ("NUMPY", "numpy"),
        ("GIT", "git"),
        ("GITHUB", "github"),
        ("DOCKER", "docker"),
        ("EXCEL", None),
        ("POWER BI", None),
        ("MINITAB", None),
        ("SQL", None),
        ("SCIKIT-LEARN", None),
        ("STREAMLIT", None),
        ("SQLITE", None),
        ("MATPLOTLIB", None),
        ("MQTT / IOT", None),
    ]

    icons = []

    for index, (label, slug) in enumerate(skills):
        column = index % 5
        row = index // 5
        x = 50 + column * 136
        y = 825 + row * 144
        duration = rng.uniform(6.5, 9.5)
        begin = -rng.uniform(0, duration)
        orbit_direction = 360 if index % 2 == 0 else -360
        icon_path = SKILL_ICON_PATHS.get(slug) if slug else None
        # Use official paths where available; otherwise use a compact text mark.
        mark = label.replace(" ", "").replace("/", "").replace("-", "")[:5]
        if icon_path:
            icon_markup = f'<g transform="translate(40.5 15) scale(1.7)"><path d="{icon_path}" class="brand-path"/></g>'
        else:
            icon_markup = f'<text x="61" y="60" text-anchor="middle" class="skill-mark">{html.escape(mark)}</text>'
        icons.append(
            f'''<g transform="translate({x} {y})" aria-label="{label} skill icon">
  <g>
    <rect x="0" y="0" width="122" height="122" rx="3" class="skill-frame"
      stroke-dasharray="11 7"/>
    {icon_markup}
    <g>
      <circle cx="61" cy="8" r="2.7" class="icon-orbit-dot"/>
      <animateTransform attributeName="transform" type="rotate"
        values="0 61 41;{orbit_direction} 61 41" dur="{duration * 0.92:.2f}s"
        begin="{begin:.2f}s" repeatCount="indefinite"/>
    </g>
    <line x1="17" y1="78" x2="105" y2="78" class="skill-rule"/>
    <text x="61" y="104" text-anchor="middle" class="skill-label">{label}</text>
    <animateTransform attributeName="transform" type="translate"
      values="0 0;0 -5;0 0" keyTimes="0;0.5;1" calcMode="spline"
      keySplines="0.42 0 0.58 1;0.42 0 0.58 1" dur="{duration:.2f}s"
      begin="{begin:.2f}s" repeatCount="indefinite"/>
  </g>
</g>'''
        )

    return "\n".join(icons)


def portrait_particles(digest):
    """Move loose terminal fragments around the portrait's face and hands."""

    rng = random.Random(int(digest[32:48], 16))
    symbols = ["0", "1", "{", "}", "/", ";", "+", "<", ">", "::"]
    regions = [
        (820, 170, 1380, 660),
        (900, 540, 1740, 1120),
        (1350, 260, 1950, 980),
        (850, 1160, 1900, 2140),
    ]
    particles = []

    for index in range(12):
        left, top, right, bottom = regions[index % len(regions)]
        x = rng.randint(left, right)
        y = rng.randint(top, bottom)
        dx = rng.randint(-90, 110)
        dy = rng.randint(150, 390)
        bend = rng.randint(-90, 90)
        duration = rng.uniform(9.0, 15.0)
        begin = -rng.uniform(0, duration)
        symbol = symbols[index % len(symbols)]
        particles.append(
            f'''<text x="{x}" y="{y}" class="portrait-particle" opacity="0">{html.escape(symbol)}
  <animateMotion path="M 0 0 C {bend} {dy * 0.32:.1f}, {dx - bend} {dy * 0.68:.1f}, {dx} {dy}"
    dur="{duration:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;0.58;0.32;0"
    keyTimes="0;0.18;0.76;1" dur="{duration:.2f}s" begin="{begin:.2f}s"
    repeatCount="indefinite"/>
</text>'''
        )

    return "\n".join(particles)


def profile_source_text():
    lines = [
        ("name", 52, 132, "Moaaz"),
        ("name", 52, 236, "Sayed"),
        ("role", 56, 304, "INDUSTRIAL ENGINEERING STUDENT"),
        ("tagline", 56, 362, "I TURN INDUSTRIAL PROBLEMS INTO DATA-DRIVEN"),
        ("tagline", 56, 400, "DECISIONS, SYSTEMS, AND IMPROVEMENT."),
        ("muted", 56, 446, "CAPITAL UNIVERSITY  ::  EGYPT  ::  GRAD. JULY 2027"),
        ("section", 52, 522, "01 / About me"),
        ("about", 56, 574, "I’m an Industrial Engineering student focused on"),
        ("about", 56, 612, "manufacturing, supply chain, and data analytics."),
        ("about", 56, 650, "I use Python, statistics, and process improvement"),
        ("about", 56, 702, "to turn operational data into practical decisions."),
        ("about", 56, 740, "Always learning. Always improving."),
        ("section", 52, 802, "02 / Languages and tools"),
        ("section", 52, 1460, "03 / What I think"),
        ("about", 56, 1512, "Good engineering connects people, processes,"),
        ("about", 56, 1550, "data, and technology."),
        ("about", 56, 1602, "I like making complex operations measurable,"),
        ("about", 56, 1640, "visual, and easier to improve."),
        ("about", 56, 1692, "Industry 4.0 is where engineering meets intelligence."),
        ("section", 52, 1770, "04 / Selected work"),
        ("about", 56, 1822, "Predictive Maintenance — NASA C-MAPSS"),
        ("about", 56, 1860, "AI-Driven Smart Factory Decision Support"),
        ("about", 56, 1898, "Productivity Tracker — Streamlit + SQLite"),
        ("about", 56, 1936, "Industrial Time Study & Line Balancing"),
        ("section", 52, 2010, "05 / Principle"),
        ("quote", 56, 2070, "Measure the process."),
        ("quote", 56, 2112, "Understand the problem. Improve the system."),
        ("prompt", 52, 2200, "moaaz@github:~$ open --portfolio"),
        ("output", 52, 2248, "industrial-engineering / data / operations"),
    ]
    return "\n".join(
        f'<text x="{x}" y="{y}" class="{css_class}">{html.escape(text)}</text>'
        for css_class, x, y, text in lines
    )


def render_svg(rows, digest):
    inter_data = base64.b64encode(
        (ROOT / "assets" / "fonts" / "inter-latin.woff2").read_bytes()
    ).decode("ascii")
    playfair_data = base64.b64encode(
        (ROOT / "assets" / "fonts" / "playfair-display-latin.woff2").read_bytes()
    ).decode("ascii")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" aria-labelledby="title desc" xml:space="preserve">
<title id="title">Aashish Thakuri terminal profile</title>
<desc id="desc">An expanded developer profile with animated skill symbols beside a living high-density character portrait reconstructed entirely from terminal glyphs.</desc>
<style>
  @font-face {{ font-family: "Profile Sans"; src: url(data:font/woff2;base64,{inter_data}) format("woff2"); font-weight: 100 900; }}
  @font-face {{ font-family: "Profile Serif"; src: url(data:font/woff2;base64,{playfair_data}) format("woff2"); font-weight: 400 900; }}
  text {{ font-family: "Cascadia Mono", Consolas, "Courier New", monospace; letter-spacing: 0; white-space: pre; }}
  .portrait {{ fill: #f0f0ec; font-size: {PORTRAIT_FONT_SIZE}px; font-weight: 700; }}
  .stream {{ fill: #777772; font-size: 9px; opacity: 0.13; }}
  .portrait-particle {{ fill: #f2f2ed; font-size: 14px; font-weight: 700; }}
  .prompt {{ fill: #aaa9a3; font-size: 17px; }}
  .name {{ font-family: "Profile Serif", Georgia, serif; fill: #f5f5f0; font-size: 106px; font-weight: 700; }}
  .role {{ font-family: "Profile Sans", Arial, sans-serif; fill: #f0f0eb; font-size: 30px; font-weight: 800; }}
  .tagline {{ font-family: "Profile Sans", Arial, sans-serif; fill: #d8d8d2; font-size: 22px; font-weight: 750; }}
  .muted {{ fill: #777772; font-size: 15px; }}
  .section {{ font-family: "Profile Serif", Georgia, serif; fill: #f0f0eb; font-size: 32px; font-weight: 700; }}
  .about {{ font-family: "Profile Sans", Arial, sans-serif; fill: #d5d5cf; font-size: 19px; font-weight: 450; }}
  .quote {{ font-family: "Profile Serif", Georgia, serif; fill: #edede7; font-size: 28px; font-style: italic; }}
  .output {{ font-family: "Profile Sans", Arial, sans-serif; fill: #eeeeea; font-size: 21px; font-weight: 700; }}
  .skill-frame {{ fill: #050505; stroke: #5f5f5a; stroke-width: 1.5; }}
  .skill-rule {{ stroke: #4a4a46; stroke-width: 1; }}
  .brand-path {{ fill: #f3f3ee; }}
  .icon-orbit-dot {{ fill: #ffffff; }}
  .skill-label {{ font-family: "Profile Sans", Arial, sans-serif; fill: #cfcfc9; font-size: 12px; font-weight: 750; }}
</style>
<rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="#000000"/>
<rect x="18" y="18" width="{SVG_WIDTH - 36}" height="{SVG_HEIGHT - 36}" fill="none" stroke="#30302e" stroke-width="1"/>
<g aria-label="slow falling code behind the portrait">
{background_streams(digest)}
</g>
<line x1="730" y1="48" x2="730" y2="2272" stroke="#343432" stroke-width="1"/>
<g aria-label="profile identity and capabilities written as terminal source">
{profile_source_text()}
{animated_skill_icons(digest)}
</g>
<g aria-label="portrait reconstructed from terminal characters">
  <g aria-label="the complete high-density terminal portrait">
    {portrait_text(rows)}
  </g>
  <g aria-label="terminal fragments moving around the living portrait">
    {portrait_particles(digest)}
  </g>
</g>
</svg>
'''


def compile_portrait(input_path, output_path):
    source = Path(input_path).read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    rows = image_rows(input_path)
    svg = render_svg(rows, digest)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(svg, encoding="utf-8", newline="\n")
    return len(rows), digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows, digest = compile_portrait(args.input, args.output)
    print(f"Compiled {rows} rows of live ASCII portrait")
    print(f"Source SHA-256: {digest}")


if __name__ == "__main__":
    main()
