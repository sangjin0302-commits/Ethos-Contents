#!/usr/bin/env python3
"""Build deterministic ETHOS card HTML files from approved card-data JSON."""

import argparse
import html
import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "icons" / "lucide"
TABLER_DIR = ROOT / "assets" / "icons" / "tabler"
ICON_DIRS = (ICON_DIR, TABLER_DIR)  # Lucide first; Tabler fills the names Lucide lacks
ILLUSTRATION_DIR = ROOT / "assets" / "illustrations"


def esc(value):
    return html.escape(str(value), quote=True)


# 가운뎃점으로 묶인 짧은 낱말("과실·시정", "동기·결과·위반정도")은 한 덩어리로 줄바꿈한다.
# 그렇지 않으면 줄 첫머리에 "·동기와"처럼 가운뎃점이 떨어져 어색하게 읽힌다.
MAX_NOBR = 14
DOT_CHAIN = re.compile(r"[가-힣A-Za-z0-9]{1,8}(?:·[가-힣A-Za-z0-9]{1,8}){1,3}")


def marked(text, highlight):
    """text를 이스케이프하고, card-data highlight와 같은 부분 문자열이 있으면 한 곳만 골드 밑줄로 감싼다."""
    safe = esc(text)
    if highlight and highlight in text:
        h = esc(highlight)
        safe = safe.replace(h, f'<span class="mark-hl">{h}</span>', 1)
    return safe


def keep_dot_chains(markup, cap=None):
    def text(match):
        # v2 세트는 14자를 넘는 묶음에 줄바꿈을 허용한다. 줄바꿈 없는 긴 덩어리는 좁은 칸에서 가로로 넘친다(legacy 세트는 승인본이라 그대로).
        return ">" + DOT_CHAIN.sub(lambda m: f'<span class="nobr">{m.group(0)}</span>' if cap is None or len(m.group(0)) <= cap else m.group(0), match.group(1)) + "<"
    head, sep, rest = markup.partition("<body>")
    body, sep2, tail = rest.partition("<script>")
    return head + sep + re.sub(r">([^<>]+)<", text, body) + sep2 + tail


def icon_path(name):
    """File for an icon name, looked up in Lucide first and then Tabler; None when neither has it."""
    name = re.sub(r"\.svg$", "", str(name))  # ChatGPT often writes "scale.svg"; the name and the file name mean the same icon
    if not re.fullmatch(r"[a-z0-9-]+", name):
        return None
    for folder in ICON_DIRS:
        path = folder / f"{name}.svg"
        if path.is_file():
            return path
    return None


def icon_svg(name):
    """Inline a vendored Lucide or Tabler icon. Size and colour come from CSS, so the file stays untouched."""
    path = icon_path(name)
    if path is None:
        raise ValueError(f"unknown icon {name!r}; add it to {ICON_DIR} or {TABLER_DIR} first")
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
    if kind == "rest":  # 쉼 카드: 결론 한 문장을 크게(자동 디자인이 없을 때의 예비 렌더)
        cap = f'<p class="rest-cap">{esc(item_text(body[0]))}</p>' if body else ""
        return f'<div class="rest-main"><p class="rest-text" data-role="headline">{marked(card["headline"], card.get("highlight"))}</p>{cap}</div>'
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
            if title:
                rows.append(f'<div class="rule-item"><div class="rule-key" data-role="subheading">{esc(title)}</div><div class="rule-copy">{esc(copy)}</div></div>')
            else:  # 라벨 없는 항목은 빈 라벨 칸을 만들지 않고 본문을 전체 폭으로 쓴다
                rows.append(f'<div class="rule-item no-key"><div class="rule-copy">{esc(copy)}</div></div>')
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
        if layout == "bars":
            return bar_rows(body)
        rows = []
        for index, item in enumerate(body, 1):
            key, copy = (item.get("key", ""), item.get("text", "")) if isinstance(item, dict) else ("", item)
            if layout == "stats":
                rows.append(f'<div class="stat-row">{item_icon(item)}<div class="stat-key" data-role="label">{esc(key or index)}</div><div class="stat-copy">{esc(strip_step_prefix(copy))}</div></div>')
                continue
            num = "" if key else " num"  # 키 없는 번호 목록은 번호 칸을 좁게(124px 고정 칸에 숫자 하나만 남던 문제)
            rows.append(f'<div class="threshold{num}"><div class="threshold-key" data-role="label">{esc(key or index)}</div><div class="threshold-copy">{esc(strip_step_prefix(copy))}</div></div>')
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


# 세로형 캔버스에서 본문이 짧으면 빈 공간이 크게 남는다. v2 세트는 폰트 로드 뒤 본문의 글자 크기만
# 남는 높이만큼 키운다(최대 FIT_MAX배, 여백은 그대로). 가로·세로로 넘칠 기미가 있으면 그 직전 배율에서 멈춘다.
# 결정론적이며 외부 호출이 없다.
FIT_MAX = 1.6
FIT_TARGET = 0.9
FIT_SCRIPT = (
    "<script>(function(){var M=%s,T=%s;function fit(){"
    "var m=document.querySelector('.z-main');if(!m)return;var k=[].slice.call(m.children).filter(function(e){return !e.hasAttribute('data-decor')});"
    "if(!k.length)return;var cs=getComputedStyle(m);var a=m.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom);"
    # 글자가 직접 들어 있는 요소만 키운다. 여백·테두리는 그대로 두어 공간이 여백이 아니라 글자로 찬다.
    "var tx=[].slice.call(m.querySelectorAll('*')).filter(function(e){if(e.closest('[data-decor]'))return false;"
    "for(var i=0;i<e.childNodes.length;i++){var n=e.childNodes[i];if(n.nodeType===3&&n.textContent.trim())return true}return false});"
    "var base=tx.map(function(e){var c=getComputedStyle(e);return [parseFloat(c.fontSize),parseFloat(c.lineHeight)]});"
    "function set(z){tx.forEach(function(e,i){e.style.fontSize=(base[i][0]*z)+'px';if(!isNaN(base[i][1]))e.style.lineHeight=(base[i][1]*z)+'px'})}"
    "function used(){var t=k[0].getBoundingClientRect().top,b=k[k.length-1].getBoundingClientRect().bottom;return b-t}"
    "function wide(){var b=document.querySelector('.body')||m;var all=[b].concat([].slice.call(b.querySelectorAll('*')));"
    "for(var i=0;i<all.length;i++){var e=all[i];if(e.clientWidth>0&&e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).display!=='inline')return true}"
    "return m.scrollHeight>m.clientHeight+1}"
    "function ok(){return used()<=a*T&&!wide()}"
    # 위계: 본문 글자는 제목의 60%를 넘지 않는다(제목과 본문이 같은 크기로 보이던 문제).
    "var h=document.querySelector('.z-title .h2');var big=Math.max.apply(null,base.map(function(b){return b[0]}));"
    "if(h){M=Math.min(M,parseFloat(getComputedStyle(h).fontSize)*0.6/big)}if(M<=1)return;"
    "if(!ok())return;var lo=1,hi=M;for(var i=0;i<10;i++){var z=(lo+hi)/2;set(z);if(ok())lo=z;else hi=z}"
    "lo=Math.floor(lo*100)/100;set(lo);m.setAttribute('data-fit',String(lo))}"
    "if(document.fonts&&document.fonts.ready){document.fonts.ready.then(fit)}else{fit()}})();</script>"
) % (FIT_MAX, FIT_TARGET)


def bar_rows(body):
    """Proportional bars for 2-3 quantities that share a unit. `value` sets the length only; `display` is the number the reader sees."""
    values = [float(item.get("value", 0) or 0) for item in body]
    top = max(values + [1e-9])
    rows = []
    for item, value in zip(body, values):
        pct = max(value / top * 100, 7.0) if value > 0 else 7.0  # a visible stub, so the smallest value never disappears
        copy = strip_step_prefix(item.get("text", ""))
        rows.append(f'<div class="bar-row"><div class="bar-head"><span class="bar-key" data-role="label">{esc(item.get("key", ""))}</span>'
                    f'<span class="bar-val" data-role="label">{esc(item.get("display", ""))}</span></div>'
                    f'<div class="bar-track" data-decor><div class="bar-fill" style="width:{pct:.1f}%"></div></div>'
                    + (f'<div class="bar-copy">{esc(copy)}</div>' if copy else "") + '</div>')
    return '<div class="bar-rows">' + ''.join(rows) + '</div>'


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
    # 편집 파이프라인 v2.0 세트, 또는 문구는 그대로 두고 레이아웃만 v2로 켠 legacy 세트(layoutVersion "2")
    auto = (data.get("editorialReview") or {}).get("pipelineVersion") == "2.0" or data.get("layoutVersion") == "2"
    dens = density(card, language) if auto else ""
    beat = visual_beat(card)
    if beat not in ("calm", "bold", "evidence", "toolkit"):
        raise ValueError(f"unsupported visualBeat: {beat}")
    org = "에토스 행정사사무소" if language == "ko" else "Ethos Administrative Attorney Office"
    title = "" if card["type"] in ("cover", "rest") else f'<div class="kicker-num" data-decor>{page:02d}</div><h2 class="h2" data-role="headline">{marked(card["headline"], card.get("highlight"))}</h2>'
    cover_label = data.get("coverLabel", data["series"])
    # v2 세트: 칩이 헤더의 시리즈 이름과 같으면 같은 글자가 두 번 보이므로 칩을 뺀다(회차 주제는 coverLabel로 따로 준다).
    # 표지 변경은 새로 쓰는 v2.0 세트에만 적용한다(layoutVersion으로 레이아웃만 켠 승인 세트는 표지를 그대로 둔다).
    new_cover = (data.get("editorialReview") or {}).get("pipelineVersion") == "2.0"
    same_as_header = new_cover and cover_label.strip() == str(data["series"]).strip()
    # v2.0 세트: 오른쪽 아래 페이지 칸에 넘김 표시(막대 + 03 / 10). 칸의 위치·크기는 그대로라 프레임 검사에 영향이 없다.
    progress_style = f' style="--progress:{min(page, total) / max(total, 1) * 100:.0f}%"'
    progress_attr = f' data-progress="{page:02d} / {total:02d}"'
    chip = ("" if same_as_header else f'<span class="chip">{esc(cover_label)}</span>') if card["type"] == "cover" else title
    badge = ""
    if card.get("icon") and card["type"] != "cover":
        badge = f'<span class="card-icon" data-decor aria-hidden="true">{icon_svg(card["icon"])}</span>'
        chip += badge
    il_block = ""
    if card.get("illustration") and card["type"] != "cover" and dens == "low" and len(card.get("headline", "")) <= (24 if language == "ko" else 36):
        il_block = f'<div class="il-wrap" data-decor aria-hidden="true">{illustration_svg(card["illustration"])}</div>'
    take = marked(card.get("takeaway", ""), card.get("highlight") if card.get("highlight", "") not in card.get("headline", "") else None)
    take_html = (f'<div class="take" data-role="takeaway">{take}</div>' if take_style(card) == "bar"
                 else f'<div class="editorial-close" data-role="takeaway">{take}</div>')
    # pageTurn remains editorial metadata for checking the story flow.
    # It is intentionally not rendered on the published card.
    page_turn_html = ""
    fit_script = FIT_SCRIPT if auto and card["type"] != "cover" else ""
    return keep_dot_chains(f'''<!doctype html>
<html lang="{language}"><head><meta charset="utf-8">
<link rel="stylesheet" href="../../../brand/tokens.css">
<link rel="stylesheet" href="../../../brand/fonts.css">
<link rel="stylesheet" href="../../../templates/base.css">
<link rel="stylesheet" href="../../../templates/card-types.css">
</head><body>
<div class="card {esc(card['bg'])} lang-{language} canvas-{canvas} family-{family} beat-{beat} pace-{'a' if page % 2 else 'b'}{' has-icon' if badge else ''}{' cover-v2' if new_cover and card['type'] == 'cover' else ''}{(' dens-' + dens) if dens in ('low', 'mid') else ''}"{progress_style} data-card-type="{esc(card['type'])}" data-bg="{esc(card['bg'])}" data-page="{page}" data-canvas="{canvas}" data-visual-family="{family}">
  <div class="gold-top" data-frame="gold-top"></div>
  <div class="hdr"><span class="wm" data-frame="wordmark">ETHOS BRIEF</span><span class="sec" data-frame="section">{esc(data['series'])} · {esc(data['issue'])}</span></div>
  <div class="hl" data-frame="line"></div>
  <div class="body">
    <div class="z-title" data-zone="title">{chip}</div>
    <div class="z-main" data-zone="main">{il_block}{main_markup(card, language)}</div>
    <div class="z-take" data-zone="take">{take_html}</div>
  </div>
{page_turn_html}
  <div class="ftr"><div class="org" data-frame="org">{org}</div><div class="tagl" data-frame="tagline">LOGOS · PATHOS · ETHOS</div><div class="pg" data-frame="page" aria-hidden="true"{progress_attr}></div></div>
  <div class="gold-bottom" data-frame="gold-bottom"></div>
</div>{fit_script}</body></html>''', MAX_NOBR if auto else None)


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
