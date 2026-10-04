#!/usr/bin/env python3
"""Render the Rocket NPU project cards in cards/ as light and dark SVGs.

Descriptions and layer labels live in CARDS below. Star counts and languages
come from the GitHub API, so rerunning this keeps them current. Set GH_TOKEN
(or GITHUB_TOKEN) to avoid the unauthenticated rate limit.
"""
import json
import os
import pathlib
import urllib.request
from xml.sax.saxutils import escape

OWNER = "gregordinary"
OUT = pathlib.Path(__file__).resolve().parent.parent / "cards"

# Each description is two lines; keep each under ~50 characters so it fits.
CARDS = [
    ("ggml-rocket", "Framework backend",
     ["Drop-in ggml backend: runs llama.cpp and",
      "whisper.cpp prefill on the RK3588 NPU"]),
    ("rocket-userspace", "Driver",
     ["librocketnpu: userspace driver, matmul and",
      "on-NPU op library for the rocket driver"]),
    ("ort-rocket", "Framework backend",
     ["ONNX Runtime provider for vision transformers:",
      "CLIP/SigLIP, SAM, Depth Anything, RF-DETR"]),
    ("tflite-rocket", "Framework backend",
     ["TensorFlow Lite delegate for NPU object",
      "detection, e.g. in Frigate"]),
    ("rknpu-submit", "Driver · vendor kernel",
     ["Runs the same open NPU stack on a stock",
      "vendor BSP kernel, no reflash needed"]),
    ("patches", "Kernel",
     ["Out-of-tree rocket driver and hardware",
      "video-transcode patch sets"]),
]

# GitHub's own palette, so the cards sit naturally on the profile page.
THEMES = {
    "light": dict(bg="#ffffff", border="#d1d9e0", fg="#1f2328", muted="#59636e",
                  link="#0969da", accent="#bc4c00"),
    "dark": dict(bg="#0d1117", border="#3d444d", fg="#f0f6fc", muted="#9198a1",
                 link="#4493f8", accent="#f0883e"),
}

LANG_COLORS = {"C": "#555555", "C++": "#f34b7d", "Rust": "#dea584",
               "Shell": "#89e051", "Python": "#3572a5"}

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
W, H = 420, 148


def fetch(name):
    req = urllib.request.Request(f"https://api.github.com/repos/{OWNER}/{name}",
                                 headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def card(name, layer, lines, stars, lang, t):
    desc = "".join(
        f'<text x="20" y="{82 + i * 18}" class="d">{escape(line)}</text>'
        for i, line in enumerate(lines))
    lang_row = ""
    if lang:
        lang_row = (f'<circle cx="25" cy="{H - 24}" r="5" fill="{LANG_COLORS.get(lang, t["muted"])}"/>'
                    f'<text x="36" y="{H - 20}" class="m">{escape(lang)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(name)}">
<style>
text {{ font-family: {FONT}; }}
.l {{ font-size: 11px; font-weight: 600; letter-spacing: .08em; fill: {t["accent"]}; }}
.n {{ font-size: 17px; font-weight: 600; fill: {t["link"]}; }}
.d {{ font-size: 13px; fill: {t["fg"]}; }}
.m {{ font-size: 12px; fill: {t["muted"]}; }}
</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" fill="{t["bg"]}" stroke="{t["border"]}"/>
<text x="20" y="30" class="l">{escape(layer.upper())}</text>
{f'<text x="{W - 20}" y="30" class="m" text-anchor="end">★ {stars}</text>' if stars else ""}
<text x="20" y="56" class="n">{escape(name)}</text>
{desc}
{lang_row}
</svg>
'''


def main():
    OUT.mkdir(exist_ok=True)
    for name, layer, lines in CARDS:
        repo = fetch(name)
        for theme, t in THEMES.items():
            svg = card(name, layer, lines, repo["stargazers_count"], repo["language"], t)
            (OUT / f"{name}-{theme}.svg").write_text(svg)


if __name__ == "__main__":
    main()
