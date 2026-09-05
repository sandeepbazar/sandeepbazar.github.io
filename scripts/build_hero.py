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
  <text x="24" y="282" class="mono xs" fill="{t['dim']}">OPEN SOURCE · APACHE-2.0 · EVERY CLAIM MEASURED AND PUBLISHED</text>
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


def main() -> None:
    out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "hero"
    out.mkdir(parents=True, exist_ok=True)
    for name in THEMES:
        (out / f"hero-{name}.svg").write_text(hero(name), encoding="utf-8")
        (out / f"star-{name}.svg").write_text(star_button(name), encoding="utf-8")
    print(f"wrote {2 * len(THEMES)} animated files -> assets/hero")


if __name__ == "__main__":
    main()
