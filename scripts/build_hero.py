#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Sandeep Bazar
# SPDX-License-Identifier: Apache-2.0
"""Generate the animated hero art and star button, one dark file and one light.

A README renders these through GitHub's image proxy, which is a closed context: no font loads, no
script runs, no <foreignObject> lays anything out. So the motion is CSS keyframes inside the file,
the type is generic families only, and every coordinate is computed here rather than by a layout
engine. Motion is dropped wholesale under prefers-reduced-motion.

Usage:  python3 scripts/build_hero.py
"""

from __future__ import annotations

import pathlib
import re

THEMES = {
    "dark": {"bg": "#0b1020", "panel": "#121a30", "edge": "#243154", "ink": "#e8ecf8", "dim": "#93a4c8"},
    "light": {"bg": "#fbfcff", "panel": "#ffffff", "edge": "#dfe6f5", "ink": "#0f1729", "dim": "#5a6b8c"},
}
BLUE, VIOLET, CYAN, GREEN, AMBER = "#3b82f6", "#a78bfa", "#38bdf8", "#22c55e", "#f59e0b"

# Keep each note short: the card is 262 units wide and the monospace fallback is wider per glyph
# than the metric families, so a long line runs under the next card rather than wrapping.
PROJECTS = [
    ("lazy-senior-dev", "three reviewers, in the agent", VIOLET),
    ("ocm-mcp-server", "guardrailed AgentOps, K8s", CYAN),
    ("blogs", "measured, then written", AMBER),
]


def read_stats() -> list[tuple[str, str]]:
    """Read the figures from index.html rather than repeating them here.

    The page is the source of truth for these numbers. Copying them into the art is how a hero ends
    up quoting a headcount the site stopped claiming two edits ago.
    """
    html = (pathlib.Path(__file__).resolve().parent.parent / "index.html").read_text(encoding="utf-8")
    rows = re.findall(r"<dt>([^<]+)</dt><dd>([^<]+)<span>([^<]+)</span></dd>", html)
    out = []
    for label, value, unit in rows:
        unit = unit.strip()
        # "+ engineers" reads as "100+ engineers", not "100 + engineers".
        if unit.startswith("+"):
            value, unit = value.strip() + "+", unit.lstrip("+ ").strip()
        out.append((value.strip(), unit))
    return out[:4]


STATS = read_stats()


def hero(name: str) -> str:
    t, w, h = THEMES[name], 880, 300

    cards = "".join(f'''
    <g class="card c{i}">
      <rect x="{24 + i * 278}" y="112" width="262" height="86" rx="13" fill="{t['panel']}" stroke="{t['edge']}"/>
      <circle cx="{46 + i * 278}" cy="140" r="12" fill="{col}" opacity=".18"/>
      <circle class="ping" cx="{46 + i * 278}" cy="140" r="4.5" fill="{col}"/>
      <text x="{68 + i * 278}" y="145" class="sans b" fill="{t['ink']}">{proj}</text>
      <text x="{40 + i * 278}" y="172" class="mono xs" fill="{t['dim']}">{note}</text>
      <rect class="bar" x="{40 + i * 278}" y="184" width="230" height="3" rx="2" fill="{col}" opacity=".55"/>
    </g>''' for i, (proj, note, col) in enumerate(PROJECTS))

    stats = "".join(f'''
    <g class="stat s{i}">
      <text x="{40 + i * 212}" y="252" class="mono num" fill="{t['ink']}">{n}</text>
      <text x="{40 + i * 212 + len(n) * 15 + 8}" y="252" class="mono xs" fill="{t['dim']}">{label}</text>
    </g>''' for i, (n, label) in enumerate(STATS))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Sandeep Bazar: platform infrastructure and applied AI. Three open-source projects, and the numbers behind fourteen years at IBM.">
  <style>
    .mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
    .sans{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
    .b{{font-size:14px;font-weight:700}}.xs{{font-size:9.5px;letter-spacing:.07em}}
    .num{{font-size:21px;font-weight:700}}.cap{{font-size:10px;font-weight:700;letter-spacing:.2em}}
    @keyframes rise{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
    @keyframes ping{{0%,100%{{opacity:.3;r:3.6}}50%{{opacity:1;r:5.6}}}}
    @keyframes grow{{0%{{transform:scaleX(.06);opacity:.3}}60%,100%{{transform:scaleX(1);opacity:.85}}}}
    @keyframes glow{{0%,100%{{opacity:.18}}50%{{opacity:.4}}}}
    @keyframes fade{{0%{{opacity:0;transform:translateY(5px)}}100%{{opacity:1;transform:translateY(0)}}}}
    .card{{animation:rise 5s ease-in-out infinite}}.c1{{animation-delay:.45s}}.c2{{animation-delay:.9s}}
    .ping{{animation:ping 2.2s ease-in-out infinite}}
    .bar{{animation:grow 3.6s ease-in-out infinite;transform-origin:left center}}
    .c1 .bar{{animation-delay:.4s}}.c2 .bar{{animation-delay:.8s}}
    .glow{{animation:glow 4.4s ease-in-out infinite}}
    .stat{{animation:fade .7s ease-out both}}
    .s1{{animation-delay:.15s}}.s2{{animation-delay:.3s}}.s3{{animation-delay:.45s}}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
  </style>
  <defs><radialGradient id="g-{name}">
    <stop offset="0%" stop-color="{BLUE}" stop-opacity=".34"/>
    <stop offset="60%" stop-color="{BLUE}" stop-opacity=".10"/>
    <stop offset="100%" stop-color="{BLUE}" stop-opacity="0"/></radialGradient></defs>
  <rect width="{w}" height="{h}" rx="18" fill="{t['bg']}"/>
  <circle class="glow" cx="440" cy="60" r="230" fill="url(#g-{name})"/>
  <text x="24" y="36" class="mono cap" fill="{t['dim']}">SANDEEP BAZAR · PLATFORM INFRASTRUCTURE &amp; APPLIED AI</text>
  <text x="24" y="72" class="sans" font-size="24" font-weight="700" fill="{t['ink']}">I build the teams that build</text>
  <text x="24" y="98" class="sans" font-size="24" font-weight="700" fill="{BLUE}">infrastructure people trust.</text>
  {cards}
  <line x1="24" y1="218" x2="856" y2="218" stroke="{t['edge']}"/>
  {stats}
  <text x="24" y="282" class="mono xs" fill="{t['dim']}">EVERY CLAIM MEASURED AND PUBLISHED</text>
</svg>'''


def star_button(name: str) -> str:
    """A cursor travels in, presses, and the star fills, all off one clock so the star never
    lights before the click that causes it."""
    t, w, h = THEMES[name], 132, 34
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Star this repository on GitHub">
  <style>
    .mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:11.5px;font-weight:700}}
    @keyframes cur{{0%{{transform:translate(34px,26px);opacity:0}}12%{{opacity:1}}30%,38%{{transform:translate(12px,13px)}}
      44%{{transform:translate(12px,15px)}}58%{{transform:translate(12px,13px)}}80%{{transform:translate(12px,13px);opacity:1}}
      92%,100%{{transform:translate(34px,26px);opacity:0}}}}
    @keyframes press{{0%,38%,58%,100%{{transform:scale(1)}}46%{{transform:scale(.94)}}}}
    @keyframes fill{{0%,44%{{fill:none;stroke-width:1.6}}52%,88%{{fill:#f5b301;stroke-width:0}}96%,100%{{fill:none;stroke-width:1.6}}}}
    @keyframes pop{{0%,44%{{transform:scale(1)}}54%{{transform:scale(1.28)}}64%,100%{{transform:scale(1)}}}}
    @keyframes tick{{0%,52%{{opacity:0}}62%,86%{{opacity:1}}94%,100%{{opacity:0}}}}
    .btn{{animation:press 5s ease-in-out infinite;transform-origin:50% 50%}}
    .star{{animation:fill 5s ease-in-out infinite,pop 5s ease-in-out infinite;transform-origin:center;transform-box:fill-box}}
    .cur{{animation:cur 5s ease-in-out infinite}}.n{{animation:tick 5s ease-in-out infinite}}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.star{{fill:#f5b301;stroke-width:0}}.n{{opacity:1}}}}
  </style>
  <g class="btn">
    <rect x=".8" y=".8" width="{w - 1.6}" height="{h - 1.6}" rx="9" fill="{t['panel']}" stroke="{t['edge']}"/>
    <path class="star" d="M20 8.2 l3.3 6.7 7.4 1.1 -5.35 5.2 1.26 7.35 -6.61-3.47 -6.61 3.47 1.26-7.35 -5.35-5.2 7.4-1.1 z"
          fill="none" stroke="#f5b301" stroke-width="1.6" stroke-linejoin="round"/>
    <text x="42" y="22" class="mono" fill="{t['ink']}">Star</text>
    <g class="n"><rect x="{w - 42}" y="9" width="32" height="16" rx="5" fill="#f5b301" opacity=".16"/>
      <text x="{w - 26}" y="21" text-anchor="middle" class="mono" fill="#d69a00">+1</text></g>
  </g>
  <g class="cur"><path d="M0 0 L0 13.5 L3.6 10.4 L6.1 15.6 L8.4 14.5 L5.9 9.4 L10.6 9.1 Z"
     fill="{t['ink']}" stroke="{t['bg']}" stroke-width="1.1"/></g>
</svg>'''


# One compact strip per project, drawn to say what the thing is rather than to decorate the card.
# Each carries three short facts; keep them under about twenty characters, because the monospace
# fallback is wider per glyph than the metric families and a long line runs off the panel.
# The second line says what the thing is, never what it is licensed as. A licence stated in a
# drawing has to be redrawn to stay true, and a stale one is a false claim; the repository is where
# that lives.
STRIPS = {
    "blogs": ("Writing", AMBER, "page", "LONG-FORM NOTES · NO TRACKER",
              ["markdown in", "static site out", "no database"]),
    "lazy-senior-dev": ("lazy-senior-dev", VIOLET, "gate", "REVIEWS THE CHANGE BEFORE IT LANDS",
                        ["3 personas", "14 agents", "every claim measured"]),
    "ocm-mcp-server": ("ocm-mcp-server", CYAN, "shield", "AGENTOPS FOR KUBERNETES FLEETS",
                       ["reads free", "writes signed", "all traced"]),
    "ai-roadmap-365": ("365 Days of AI Mastery", BLUE, "ring", "ONE LESSON AND ONE LAB A DAY",
                       ["9 courses", "365 labs", "real output"]),
    "ibm-fusion-mcp-server": ("ibm-fusion-mcp-server", GREEN, "fleet", "FLEET OPERATIONS FOR IBM FUSION",
                              ["fleet ops", "data resilience", "MCP"]),
}


def motif(kind: str, col: str, t: dict[str, str]) -> str:
    if kind == "page":
        return f"""<g class="bob">
      <rect x="-22" y="-26" width="44" height="52" rx="5" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="2"/>
      <g stroke="{col}" stroke-width="2.4" stroke-linecap="round" opacity=".8">
        <path class="ln l0" d="M-13 -13 h26"/><path class="ln l1" d="M-13 -4 h26"/>
        <path class="ln l2" d="M-13 5 h20"/><path class="ln l3" d="M-13 14 h14"/>
      </g>
      <rect class="caret" x="6" y="9" width="2.4" height="11" fill="{col}"/>
    </g>"""
    if kind == "gate":
        return f"""<g class="bob">
      <rect x="-26" y="-20" width="30" height="40" rx="5" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="2"/>
      <path class="bar-l" d="M10 -22 v44" stroke="{col}" stroke-width="4" stroke-linecap="round"/>
      <circle class="ping" cx="22" cy="0" r="4" fill="{col}"/>
    </g>"""
    if kind == "shield":
        return f"""<g class="bob">
      <circle class="ring" r="26" fill="none" stroke="{col}" stroke-width="2"/>
      <path d="M0 -26 L23 -17 V3 C23 17 12 24 0 29 C-12 24 -23 17 -23 3 V-17 Z" fill="{col}"
            fill-opacity=".16" stroke="{col}" stroke-width="2.2" stroke-linejoin="round"/>
      <g class="shackle"><path d="M-7 2 v-5 a7 7 0 0 1 14 0 v5" fill="none" stroke="{t['ink']}"
         stroke-width="2.2" stroke-linecap="round" opacity=".85"/></g>
      <rect x="-8.5" y="2" width="17" height="12" rx="3" fill="{t['ink']}" opacity=".85"/>
    </g>"""
    if kind == "ring":
        return f"""<g class="bob">
      <circle r="24" fill="none" stroke="{t['edge']}" stroke-width="6"/>
      <circle class="arc" r="24" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round"
              stroke-dasharray="150.8" transform="rotate(-90)"/>
      <text y="5" text-anchor="middle" class="mono" font-size="14" font-weight="700" fill="{t['ink']}">365</text>
    </g>"""
    return f"""<g class="bob">
      <circle r="7" fill="{col}"/>
      <g class="sp"><circle cx="26" cy="0" r="5" fill="{col}" opacity=".85"/>
        <circle cx="-13" cy="22" r="5" fill="{col}" opacity=".6"/>
        <circle cx="-13" cy="-22" r="5" fill="{col}" opacity=".45"/></g>
      <circle r="26" fill="none" stroke="{col}" stroke-width="1.6" opacity=".4" stroke-dasharray="4 6"/>
    </g>"""


def project_strip(key: str, theme_name: str) -> str:
    title, col, kind, subtitle, facts = STRIPS[key]
    t, w, h = THEMES[theme_name], 640, 132
    chips = "".join(f"""
    <g class="chip c{i}">
      <rect x="{116 + i * 172}" y="86" width="160" height="26" rx="8" fill="{t['panel']}" stroke="{t['edge']}"/>
      <circle cx="{132 + i * 172}" cy="99" r="3.6" fill="{col}"/>
      <text x="{144 + i * 172}" y="103" class="mono xs" fill="{t['dim']}">{f}</text>
    </g>""" for i, f in enumerate(facts))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
  <style>
    .mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
    .sans{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
    .xs{{font-size:9.5px;letter-spacing:.05em}}
    @keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
    @keyframes ping{{0%,100%{{opacity:.3;r:3.4}}50%{{opacity:1;r:5.2}}}}
    @keyframes ring{{0%{{opacity:.6;transform:scale(.76)}}70%,100%{{opacity:0;transform:scale(1.22)}}}}
    @keyframes shut{{0%,42%{{transform:translateY(-6px)}}54%,100%{{transform:translateY(0)}}}}
    @keyframes arc{{from{{stroke-dashoffset:150.8}}to{{stroke-dashoffset:0}}}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    @keyframes caret{{0%,45%{{opacity:1}}55%,100%{{opacity:0}}}}
    @keyframes draw{{from{{opacity:0;transform:translateX(-5px)}}to{{opacity:.8;transform:translateX(0)}}}}
    @keyframes fade{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
    @keyframes glow{{0%,100%{{opacity:.16}}50%{{opacity:.34}}}}
    .bob{{animation:bob 3.6s ease-in-out infinite}}
    .ping{{animation:ping 2s ease-in-out infinite}}
    .ring{{animation:ring 2.8s ease-out infinite;transform-origin:0 0}}
    .shackle{{animation:shut 4.2s ease-in-out infinite}}
    .arc{{animation:arc 2.6s cubic-bezier(.22,.9,.3,1) both}}
    .sp{{animation:spin 12s linear infinite;transform-origin:0 0}}
    .caret{{animation:caret 1.1s step-end infinite}}
    .ln{{animation:draw .7s ease-out both}}
    .l1{{animation-delay:.12s}}.l2{{animation-delay:.24s}}.l3{{animation-delay:.36s}}
    .chip{{animation:fade 4.2s ease-in-out infinite}}.c1{{animation-delay:1.4s}}.c2{{animation-delay:2.8s}}
    .glow{{animation:glow 4.4s ease-in-out infinite}}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.arc{{stroke-dashoffset:0}}.ln{{opacity:.8}}}}
  </style>
  <defs><radialGradient id="s-{key}-{theme_name}">
    <stop offset="0%" stop-color="{col}" stop-opacity=".34"/>
    <stop offset="100%" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>
  <rect width="{w}" height="{h}" rx="14" fill="{t['bg']}"/>
  <circle class="glow" cx="58" cy="52" r="76" fill="url(#s-{key}-{theme_name})"/>
  <g transform="translate(58 52)">{motif(kind, col, t)}</g>
  <text x="116" y="46" class="sans" font-size="17" font-weight="700" fill="{t['ink']}">{title}</text>
  <text x="116" y="66" class="mono xs" fill="{t['dim']}">{subtitle}</text>
  {chips}
</svg>"""


def main() -> None:
    out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "hero"
    out.mkdir(parents=True, exist_ok=True)
    for name in THEMES:
        (out / f"hero-{name}.svg").write_text(hero(name), encoding="utf-8")
        (out / f"star-{name}.svg").write_text(star_button(name), encoding="utf-8")
        for key in STRIPS:
            (out / f"{key}-{name}.svg").write_text(project_strip(key, name), encoding="utf-8")
    print(f"wrote {(2 + len(STRIPS)) * len(THEMES)} animated files -> assets/hero")


if __name__ == "__main__":
    main()
