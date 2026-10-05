#!/usr/bin/env python3
"""Build deterministic ETHOS card HTML files from approved card-data JSON."""

import argparse
import html
import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "icons" / "lucide"
ILLUSTRATION_DIR = ROOT / "assets" / "illustrations"


def esc(value):
    return html.escape(str(value), quote=True)


def icon_svg(name):
    """Inline a vendored Lucide icon. Size and colour come from CSS, so the file stays untouched."""
    path = ICON_DIR / f"{name}.svg"
    if not re.fullmatch(r"[a-z0-9-]+", str(name)) or not path.is_file():
        raise ValueError(f"unknown icon {name!r}; add it to {ICON_DIR} first")
    svg = path.read_text(encoding="utf-8").strip()
    svg = re.sub(r'\s(?:width|height)="[^"]*"', "", svg, count=2)
    return svg.replace("<svg", '<svg class="ico" aria-hidden="true" focusable="false"', 1)


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


def label_parts(item):
    """Body items are strings ("제목 — 설명") or {"key", "text"} objects; objects win."""
    if isinstance(item, dict):
        return str(item.get("key", "")).strip(), str(item.get("text", "")).strip()
    return split_label(str(item))


def illustration_svg(name):
    """Inline one of our own flat illustrations. Colours come from CSS classes (m/s/f/lm/lf), so each works on navy and cream."""
    path = ILLUSTRATION_DIR / f"{name}.svg"
    if not re.fullmatch(r"[a-z0-9-]+", str(name)) or not path.is_file():
        raise ValueError(f"unknown illustration {name!r}; add it to {ILLUSTRATION_DIR} first")
    return path.read_text(encoding="utf-8").strip().replace("<svg", '<svg class="il" aria-hidden="true" focusable="false" preserveAspectRatio="xMidYMid meet"', 1)


# 본문 글자 수(공백 제외)에 따라 카드를 "비어 보임/보통/빽빽함"으로 나눈다. 비어 보이는 카드는 글자와 패널을 키워 여백을 채운다.
DENSITY_TYPES = {"concept", "comparison", "process", "checklist", "table", "flow", "cta"}
DENSITY_LIMITS = {"ko": (150, 230), "en": (260, 400)}


def body_chars(card):
    total = 0
    for item in card.get("body", []):
        key, text = (item.get("key", ""), item.get("text", "")) if isinstance(item, dict) else ("", str(item))
        total += len(re.sub(r"\s+", "", key + text))
    return total


def density(card, language):
    if card["type"] not in DENSITY_TYPES:
        return ""
    low, mid = DENSITY_LIMITS.get(language, DENSITY_LIMITS["ko"])
    chars = body_chars(card) + 22 * len(card.get("body", []))  # 항목마다 줄 높이가 생기므로 개수도 밀도에 넣는다
    return "low" if chars < low else "mid" if chars < mid else "high"


def item_text(item):
    return item.get("text", "") if isinstance(item, dict) else item


def item_icon(item):
    return f'<span class="ico-wrap" data-decor>{icon_svg(item["icon"])}</span>' if isinstance(item, dict) and item.get("icon") else ""


def split_cols(body):
    cols = []
    for item in body:
        title, copy = label_parts(item)
        cols.append(f'<div class="split-col"><div class="split-title" data-role="subheading">{esc(title)}</div><div class="split-copy">{esc(copy)}</div></div>')
    return cols


# 결론 박스 스타일 기본값. 카드 단위로 takeStyle 을 지정하면 그 값이 우선한다.
TAKE_BAR_TYPES = {"cover", "cta", "comparison"}


def take_style(card):
    return card.get("takeStyle") or ("bar" if card["type"] in TAKE_BAR_TYPES else "close")


def cover_art(icons):
    """Two or three icon discs joined by a dashed line: a small illustration that carries the situation."""
    if not icons:
        return ""
    discs = [f'<span class="art-disc">{icon_svg(name)}</span>' for name in icons]
    return '<div class="cover-art" data-decor aria-hidden="true">' + '<span class="art-link"></span>'.join(discs) + '</div>'


def main_markup(card, language):
    body = card.get("body", [])
    kind = card["type"]

    if kind == "cover":
        promise = f'<p class="cover-promise" data-role="label">{esc(card["promise"])}</p>' if card.get("promise") else ""
        style = card.get("coverStyle")
        if style == "panel" and card.get("illustration"):
            art = f'<div class="cover-panel" data-decor aria-hidden="true">{illustration_svg(card["illustration"])}</div>'
        elif style == "stat" and card.get("hero"):
            art = (f'<div class="cover-hero"><span class="hero-val" data-role="label">{esc(card["hero"]["value"])}</span>'
                   f'<span class="hero-label" data-role="label">{esc(card["hero"]["label"])}</span></div>')
        else:
            art = cover_art(card.get("art"))
        return (f'<div>{art}<p class="cover-title" data-role="headline">{esc(card["headline"])}</p>'
                f'<p class="cover-lead">{esc(item_text(body[0]))}</p>{promise}</div>')
    if kind == "quote":
        return (f'<div class="authority-panel"><div class="authority-label" data-role="label">{esc(item_text(body[0]))}</div>'
                f'<div class="authority-text">{esc(item_text(body[1]))}</div><div class="authority-note" data-role="note">{esc(item_text(body[2]))}</div></div>')
    if kind == "concept" and len(body) == 4:
        items = []
        for item in body:
            title, copy = label_parts(item)
            items.append(f'<div class="quad-item">{item_icon(item)}<div class="qt" data-role="subheading">{esc(title)}</div><div class="qd">{esc(copy)}</div></div>')
        return '<div class="quad">' + ''.join(items) + '</div>'
    if kind == "concept":
        rows = []
        for item in body:
            title, copy = label_parts(item)
            rows.append(f'<div class="rule-item"><div class="rule-key" data-role="subheading">{esc(title)}</div><div class="rule-copy">{esc(copy)}</div></div>')
        return '<div class="rule-list">' + ''.join(rows) + '</div>'
    if kind == "comparison":
        cols = split_cols(body)
        return f'<div class="split split-{len(cols)}">' + ''.join(cols) + '</div>'
    if kind == "process":
        items = []
        for index, copy in enumerate(body, 1):
            clean = strip_step_prefix(item_text(copy))
            items.append(f'<div class="process-step"><div class="process-num" data-decor>{index:02d}</div><div class="process-copy">{esc(clean)}</div></div>')
        return f'<div class="process-steps process-{len(items)}">' + ''.join(items) + '</div>'
    if kind == "checklist":
        layout = card.get("layout") or ("thresholds" if any(isinstance(x, dict) and x.get("key") for x in body) else "numbered")
        if layout == "questions":
            return '<div class="question-grid">' + ''.join(f'<div class="question">{esc(item_text(x))}</div>' for x in body) + '</div>'
        rows = []
        for index, item in enumerate(body, 1):
            key, copy = (item.get("key", ""), item.get("text", "")) if isinstance(item, dict) else ("", item)
            if layout == "stats":
                rows.append(f'<div class="stat-row">{item_icon(item)}<div class="stat-key" data-role="label">{esc(key or index)}</div><div class="stat-copy">{esc(strip_step_prefix(copy))}</div></div>')
                continue
            rows.append(f'<div class="threshold"><div class="threshold-key" data-role="label">{esc(key or index)}</div><div class="threshold-copy">{esc(strip_step_prefix(copy))}</div></div>')
        return f'<div class="{"stat-rows" if layout == "stats" else "thresholds"}">' + ''.join(rows) + '</div>'
    if kind == "flow":
        nodes = []
        for item in body:
            name, copy = label_parts(item)
            nodes.append(f'<div class="flow-node">{item_icon(item)}<div class="flow-name" data-role="subheading">{esc(name)}</div><div class="flow-desc">{esc(copy)}</div></div>')
        chain = '<div class="flow-arrow" data-decor aria-hidden="true"></div>'.join(nodes)
        note = f'<div class="flow-note">{esc(card["note"])}</div>' if card.get("note") else ""
        return f'<div><div class="flow flow-{len(nodes)}">{chain}</div>{note}</div>'
    if kind == "table":
        head = card.get("head") or []
        thead = (f'<div class="tbl-head" data-role="label"><span>{esc(head[0])}</span><span>{esc(head[1])}</span></div>'
                 if len(head) == 2 else "")
        rows = []
        for item in body:
            key, copy = label_parts(item)
            rows.append(f'<div class="tbl-row"><div class="tbl-key" data-role="subheading">{esc(key)}</div><div class="tbl-val">{esc(copy)}</div></div>')
        return f'<div class="tbl">{thead}{"".join(rows)}</div>'
    if kind == "cta":
        if len(body) == 2:
            return '<div class="split">' + ''.join(split_cols(body)) + '</div>'
        items = []
        for index, copy in enumerate(body, 1):
            clean = strip_step_prefix(item_text(copy))
            items.append(f'<div class="six-item"><div class="six-num" data-role="label">{index:02d}</div><div class="six-copy">{esc(clean)}</div></div>')
        return '<div class="six-grid">' + ''.join(items) + '</div>'
    return '<div class="body-text">' + '<br>'.join(esc(item_text(x)) for x in body) + '</div>'


def visual_beat(card):
    """Use an explicit beat when provided; otherwise choose a restrained semantic default."""
    if card.get("visualBeat"):
        return card["visualBeat"]
    return {
        "cover": "bold", "quote": "evidence", "process": "toolkit",
        "checklist": "toolkit", "cta": "bold",
    }.get(card["type"], "calm")


def build(card, data):
    language = data["language"]
    page = card["page"]
    total = data["totalPages"]
    canvas = data.get("canvasProfile", "portrait")
    family = data.get("visualFamily", "social-native")
    if canvas not in ("square", "portrait"):
        raise ValueError(f"unsupported canvasProfile: {canvas}")
    if family not in ("editorial", "social-native"):
        raise ValueError(f"unsupported visualFamily: {family}")
    auto = (data.get("editorialReview") or {}).get("pipelineVersion") == "2.0"
    dens = density(card, language) if auto else ""
    beat = visual_beat(card)
    if beat not in ("calm", "bold", "evidence", "toolkit"):
        raise ValueError(f"unsupported visualBeat: {beat}")
    org = "에토스 행정사사무소" if language == "ko" else "Ethos Administrative Office"
    title = "" if card["type"] == "cover" else f'<div class="kicker-num" data-decor>{page:02d}</div><h2 class="h2" data-role="headline">{esc(card["headline"])}</h2>'
    cover_label = data.get("coverLabel", data["series"])
    chip = f'<span class="chip">{esc(cover_label)}</span>' if card["type"] == "cover" else title
    badge = ""
    if card.get("icon") and card["type"] != "cover":
        badge = f'<span class="card-icon" data-decor aria-hidden="true">{icon_svg(card["icon"])}</span>'
        chip += badge
    il_block = ""
    if card.get("illustration") and card["type"] != "cover" and dens == "low" and len(card.get("headline", "")) <= (24 if language == "ko" else 36):
        il_block = f'<div class="il-wrap" data-decor aria-hidden="true">{illustration_svg(card["illustration"])}</div>'
    take = esc(card.get("takeaway", ""))
    take_html = (f'<div class="take" data-role="takeaway">{take}</div>' if take_style(card) == "bar"
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
<div class="card {esc(card['bg'])} lang-{language} canvas-{canvas} family-{family} beat-{beat} pace-{'a' if page % 2 else 'b'}{' has-icon' if badge else ''}{(' dens-' + dens) if dens in ('low', 'mid') else ''}" data-card-type="{esc(card['type'])}" data-bg="{esc(card['bg'])}" data-page="{page}" data-canvas="{canvas}" data-visual-family="{family}">
  <div class="gold-top" data-frame="gold-top"></div>
  <div class="hdr"><span class="wm" data-frame="wordmark">ETHOS BRIEF</span><span class="sec" data-frame="section">{esc(data['series'])} · {esc(data['issue'])}</span></div>
  <div class="hl" data-frame="line"></div>
  <div class="body">
    <div class="z-title" data-zone="title">{chip}</div>
    <div class="z-main" data-zone="main">{il_block}{main_markup(card, language)}</div>
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
