#!/usr/bin/env python3
"""Render the landscape share image (1200x630) from a set's cover card.

Blog posts use the cover card as og:image. Social previews are landscape (about 1.91:1), so a square or
portrait cover gets centre-cropped and loses its frame. This builds a dedicated version: the headline and the
office name sit inside a centred safe zone, there is no page number, and nothing important touches the edges.

    python scripts/build_og.py content/<ID> --out ci-out/<ID>/out        # writes og-ko.png and og-en.png
"""

import os
import argparse
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_cards import icon_svg  # noqa: E402

WIDTH, HEIGHT = 1200, 630
SAFE_LEFT, SAFE_RIGHT = 140, 1060
BOTTOM_LIMIT = 560  # content must end above the office-name line
MIN_FONT_PX = 22

CSS = f"""
body {{ margin:0; width:{WIDTH}px; height:{HEIGHT}px; overflow:hidden; background:transparent; }}
.og {{ position:relative; width:{WIDTH}px; height:{HEIGHT}px; overflow:hidden; font-family:"ETHOS Sans"; word-break:keep-all; overflow-wrap:normal; }}
.og.navy {{ background:var(--ethos-navy); color:#FFFFFF; }}
.og.cream {{ background:var(--ethos-cream); color:var(--ethos-navy); }}
.bar {{ position:absolute; left:0; width:{WIDTH}px; height:8px; background:var(--ethos-gold); }}
.bar.top {{ top:0; }} .bar.bottom {{ bottom:0; }}
.ring {{ position:absolute; border-radius:50%; border:2px solid currentColor; opacity:.08; }}
.ring.a {{ right:-130px; top:60px; width:360px; height:360px; }}
.ring.b {{ left:-80px; bottom:110px; width:170px; height:170px; border-color:var(--ethos-gold); opacity:.28; }}
.safe {{ position:absolute; left:{SAFE_LEFT}px; right:{WIDTH - SAFE_RIGHT}px; top:0; bottom:70px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:20px; text-align:center; }}
.discs {{ display:flex; align-items:center; gap:18px; }}
.disc {{ width:68px; height:68px; border-radius:50%; border:2px solid var(--ethos-gold); display:flex; align-items:center; justify-content:center; color:var(--ethos-gold); background:rgba(184,151,42,.14); }}
.cream .disc {{ color:var(--ethos-navy); border-color:var(--ethos-navy); background:rgba(27,43,107,.06); }}
.disc svg {{ width:32px; height:32px; fill:none; stroke:currentColor; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round; }}
.chip {{ border:2px solid var(--ethos-gold); border-radius:30px; padding:7px 22px; font-weight:700; font-size:24px; color:var(--ethos-gold); }}
.cream .chip {{ border-color:var(--ethos-navy); color:var(--ethos-navy); }}
h1 {{ margin:0; font-family:"ETHOS Serif"; font-weight:700; line-height:1.3; text-wrap:balance; }}
.promise {{ margin:0; font-weight:700; font-size:28px; line-height:1.4; color:var(--ethos-gold); }}
.cream .promise {{ color:var(--ethos-navy); }}
.org {{ position:absolute; left:50%; transform:translateX(-50%); white-space:nowrap; bottom:34px; text-align:center; font-family:"ETHOS Serif"; font-weight:700; font-size:24px; line-height:1.2; }}
.org small {{ display:block; margin-top:6px; font-family:"ETHOS Sans"; font-weight:500; font-size:16px; letter-spacing:3px; color:var(--ethos-gold); }}
.cream .org small {{ color:var(--ethos-navy); }}
"""


def headline_size(text, lang):
    """Largest size that keeps the headline within three lines of the safe zone."""
    n = len(text.strip())
    if lang == "ko":
        return 66 if n <= 22 else 58 if n <= 32 else 50 if n <= 42 else 44
    return 62 if n <= 30 else 52 if n <= 46 else 46 if n <= 62 else 40


def cover_of(data):
    for card in data.get("cards", []):
        if card.get("type") == "cover":
            return card
    raise ValueError("card-data has no cover card")


def og_html(data, css_prefix="../../../"):
    lang = data.get("language", "ko")
    cover = cover_of(data)
    bg = cover.get("bg", "navy")
    label = data.get("coverLabel") or data.get("series", "")
    headline = cover["headline"]
    discs = ""
    if cover.get("art") and cover.get("coverStyle", "art") == "art":
        discs = '<div class="discs" data-decor>' + "".join(f'<span class="disc">{icon_svg(n)}</span>' for n in cover["art"]) + "</div>"
    promise = f'<p class="promise">{html.escape(cover["promise"])}</p>' if cover.get("promise") else ""
    org = "에토스 행정사사무소" if lang == "ko" else "Ethos Administrative Office"
    size = headline_size(headline, lang)
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<link rel="stylesheet" href="{css_prefix}brand/tokens.css">
<link rel="stylesheet" href="{css_prefix}brand/fonts.css">
<style>{CSS}</style></head><body>
<div class="og {bg}" data-og>
  <div class="bar top"></div><div class="bar bottom"></div>
  <div class="ring a"></div><div class="ring b"></div>
  <div class="safe" data-safe>
    {discs}
    <span class="chip" data-text>{html.escape(label)}</span>
    <h1 data-text style="font-size:{size}px">{html.escape(headline)}</h1>
    {promise}
  </div>
  <div class="org" data-text>{org}<small>LOGOS · PATHOS · ETHOS</small></div>
</div></body></html>"""


CHECK_JS = f"""
() => {{
  const problems = [];
  const root = document.querySelector('[data-og]').getBoundingClientRect();
  const safe = document.querySelector('[data-safe]');
  for (const el of document.querySelectorAll('[data-text], .promise')) {{
    const r = el.getBoundingClientRect();
    const px = parseFloat(getComputedStyle(el).fontSize);
    if (r.left < {SAFE_LEFT - 1} || r.right > {SAFE_RIGHT + 1}) problems.push('outside-safe-x:' + el.textContent.trim().slice(0, 20));
    if (px < {MIN_FONT_PX}) problems.push('font<{MIN_FONT_PX}px:' + el.textContent.trim().slice(0, 20));
    if (el.scrollWidth > el.clientWidth + 1 && el.tagName === 'H1') problems.push('headline-overflow-x');
  }}
  const last = [...safe.children].map(c => c.getBoundingClientRect().bottom).reduce((a, b) => Math.max(a, b), 0);
  if (last > {BOTTOM_LIMIT}) problems.push('content-too-low:' + Math.round(last));
  const first = [...safe.children].map(c => c.getBoundingClientRect().top).reduce((a, b) => Math.min(a, b), 9999);
  if (first < 40) problems.push('content-too-high:' + Math.round(first));
  const h1 = document.querySelector('h1');
  const lines = Math.round(h1.getBoundingClientRect().height / parseFloat(getComputedStyle(h1).lineHeight));
  if (lines > 3) problems.push('headline-lines>3:' + lines);
  return problems;
}}
"""


def render(items, out_dir):
    """items: list of (name, data). Returns {name: [problems]}; PNGs are written only when a name has no problems."""
    from playwright.sync_api import sync_playwright

    work = ROOT / "ci-out" / ".og-work"
    work.mkdir(parents=True, exist_ok=True)
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=os.environ.get("CHROMIUM_PATH") or None)
        context = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1, locale="ko-KR", color_scheme="light", reduced_motion="reduce")
        context.route("**/*", lambda route: route.continue_() if route.request.url.startswith("file://") else route.abort())
        for index, (name, data) in enumerate(items):
            folder = work / f"{index}-{name}"  # depth 3 below the repo root, as the CSS links expect
            folder.mkdir(parents=True, exist_ok=True)
            page_file = folder / "og.html"
            page_file.write_text(og_html(data), encoding="utf-8")
            page = context.new_page()
            page.goto(page_file.resolve().as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            problems = page.evaluate(CHECK_JS)
            results[name] = problems
            if not problems:
                page.locator("[data-og]").screenshot(path=str(out_dir / f"og-{name}.png"), animations="disabled", caret="hide")
            page.close()
        browser.close()
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content_dir")
    parser.add_argument("--out", required=True, help="directory for og-<lang>.png")
    args = parser.parse_args()
    folder = pathlib.Path(args.content_dir)
    items = []
    for lang in ("ko", "en"):
        path = folder / f"card-data.{lang}.json"
        if path.exists():
            items.append((lang, json.loads(path.read_text(encoding="utf-8"))))
    if not items:
        raise SystemExit(f"FAIL: no card-data in {folder}")
    results = render(items, args.out)
    failed = False
    for name, problems in results.items():
        print(f"{'PASS' if not problems else 'FAIL'} og-{name}" + ("" if not problems else ": " + ", ".join(problems)))
        failed |= bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
