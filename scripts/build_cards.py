#!/usr/bin/env python3
"""Build deterministic ETHOS card HTML files from approved card-data JSON."""

import argparse
import html
import json
import pathlib
import re


def esc(value):
    return html.escape(str(value), quote=True)


def split_label(text):
    if ":" in text:
        label, copy = text.split(":", 1)
        return label.strip(), copy.strip()
    if " — " in text:
        label, copy = text.split(" — ", 1)
        return label.strip(), copy.strip()
    return "", text.strip()


def strip_step_prefix(text):
    """Remove author-supplied list numbers when the layout renders its own."""
    return re.sub(r"^\s*(?:[①②③④⑤⑥⑦⑧⑨⑩]|\d{1,2}[.)]?)\s+", "", str(text)).strip()


def main_markup(card, language):
    body = card.get("body", [])
    page = card["page"]
    kind = card["type"]

    if kind == "cover":
        return f'<div><p class="cover-title" data-role="headline">{esc(card["headline"])}</p><p class="cover-lead">{esc(body[0])}</p></div>'
    if kind == "quote":
        return (f'<div class="authority-panel"><div class="authority-label" data-role="label">{esc(body[0])}</div>'
                f'<div class="authority-text">{esc(body[1])}</div><div class="authority-note" data-role="note">{esc(body[2])}</div></div>')
    if kind == "concept" and len(body) == 4:
        items = []
        for item in body:
            title, copy = split_label(item)
            items.append(f'<div class="quad-item"><div class="qt" data-role="subheading">{esc(title)}</div><div class="qd">{esc(copy)}</div></div>')
        return '<div class="quad">' + ''.join(items) + '</div>'
    if kind == "concept":
        rows = []
        for item in body:
            title, copy = split_label(item)
            rows.append(f'<div class="rule-item"><div class="rule-key" data-role="subheading">{esc(title)}</div><div class="rule-copy">{esc(copy)}</div></div>')
        return '<div class="rule-list">' + ''.join(rows) + '</div>'
    if kind == "comparison":
        cols = []
        for item in body:
            title, copy = split_label(item)
            cols.append(f'<div class="split-col"><div class="split-title" data-role="subheading">{esc(title)}</div><div class="split-copy">{esc(copy)}</div></div>')
        return '<div class="split">' + ''.join(cols) + '</div>'
    if kind == "process":
        items = []
        for index, copy in enumerate(body, 1):
            clean = strip_step_prefix(copy)
            items.append(f'<div class="process-step"><div class="process-num" data-decor>{index:02d}</div><div class="process-copy">{esc(clean)}</div></div>')
        return '<div class="process-steps">' + ''.join(items) + '</div>'
    if kind == "checklist" and page == 6:
        return '<div class="question-grid">' + ''.join(f'<div class="question">{esc(x)}</div>' for x in body) + '</div>'
    if kind == "checklist":
        rows = []
        if page == 8:
            labels = (["1조 원", "1천 건/일", "보고 요구"] if language == "ko"
                      else ["KRW 1tn", "1,000/day", "Report order"])
        else:
            labels = [str(i) for i in range(1, len(body) + 1)]
        for label, copy in zip(labels, body):
            rows.append(f'<div class="threshold"><div class="threshold-key" data-role="label">{esc(label)}</div><div class="threshold-copy">{esc(strip_step_prefix(copy))}</div></div>')
        return '<div class="thresholds">' + ''.join(rows) + '</div>'
    if kind == "cta":
        if len(body) == 2:
            cols = []
            for item in body:
                title, copy = split_label(item)
                cols.append(f'<div class="split-col"><div class="split-title" data-role="subheading">{esc(title)}</div><div class="split-copy">{esc(copy)}</div></div>')
            return '<div class="split">' + ''.join(cols) + '</div>'
        items = []
        for index, copy in enumerate(body, 1):
            clean = strip_step_prefix(copy)
            items.append(f'<div class="six-item"><div class="six-num" data-role="label">{index:02d}</div><div class="six-copy">{esc(clean)}</div></div>')
        return '<div class="six-grid">' + ''.join(items) + '</div>'
    return '<div class="body-text">' + '<br>'.join(esc(x) for x in body) + '</div>'


def build(card, data):
    language = data["language"]
    page = card["page"]
    total = data["totalPages"]
    org = "에토스 행정사사무소" if language == "ko" else "Ethos Administrative Office"
    title = "" if card["type"] == "cover" else f'<div class="kicker-num" data-decor>{page:02d}</div><h2 class="h2" data-role="headline">{esc(card["headline"])}</h2>'
    cover_label = data.get("coverLabel", data["series"])
    chip = f'<span class="chip">{esc(cover_label)}</span>' if card["type"] == "cover" else title
    take = esc(card.get("takeaway", ""))
    take_html = (f'<div class="take" data-role="takeaway">{take}</div>' if page in (1, 4, 7, 10)
                 else f'<div class="editorial-close" data-role="takeaway">{take}</div>')
    # pageTurn remains editorial metadata for checking the story flow.
    # It is intentionally not rendered on the published card.
    page_turn_html = ""
    return f'''<!doctype html>
<html lang="{language}"><head><meta charset="utf-8">
<link rel="stylesheet" href="../../../brand/tokens.css">
<link rel="stylesheet" href="../../../brand/fonts.css">
<link rel="stylesheet" href="../../../templates/base.css">
<link rel="stylesheet" href="../../../templates/card-types.css">
</head><body>
<div class="card {esc(card['bg'])} lang-{language}" data-card-type="{esc(card['type'])}" data-bg="{esc(card['bg'])}" data-page="{page}">
  <div class="gold-top" data-frame="gold-top"></div>
  <div class="hdr"><span class="wm" data-frame="wordmark">ETHOS BRIEF</span><span class="sec" data-frame="section">{esc(data['series'])} · {esc(data['issue'])}</span></div>
  <div class="hl" data-frame="line"></div>
  <div class="body">
    <div class="z-title" data-zone="title">{chip}</div>
    <div class="z-main" data-zone="main">{main_markup(card, language)}</div>
    <div class="z-take" data-zone="take">{take_html}</div>
  </div>
{page_turn_html}
  <div class="ftr"><div class="org" data-frame="org">{org}</div><div class="tagl" data-frame="tagline">LOGOS · PATHOS · ETHOS</div><div class="pg" data-frame="page" aria-hidden="true"></div></div>
  <div class="gold-bottom" data-frame="gold-bottom"></div>
</div></body></html>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("card_data")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    data = json.loads(pathlib.Path(args.card_data).read_text(encoding="utf-8"))
    if not data.get("approvedBy"):
        raise SystemExit("FAIL: card-data has no approvedBy value")
    out = pathlib.Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for card in data["cards"]:
        (out / f"card_{card['page']:02d}.html").write_text(build(card, data), encoding="utf-8")
    print(f"built {len(data['cards'])} cards in {out}")


if __name__ == "__main__":
    main()
