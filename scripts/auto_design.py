#!/usr/bin/env python3
"""card-data JSON → 자유 디자인 HTML 초안(프리셋 A 부품). ChatGPT가 JSON만 올려도 미리보기가 양식집처럼 보이지 않게 한다.

구조: ChatGPT가 card-data(문구·layout·icon·design)를 쓰고 → 이 스크립트가 카드마다 시각 중심이 다른 초안을 만들고
→ Codex가 그 초안을 content/<ID>/<lang>/에 복사해 다듬어 발행본을 만든다(docs/card-codex-production.md).

- 문구는 card-data 그대로 쓴다(카피 잠금과 같은 기준). 숫자·조문을 새로 만들지 않는다.
- 부품 선택은 카드 유형·layout·항목 수·아이콘만 보고 결정론적으로 한다. 같은 부품이 연속되지 않게 일부 유형은 대안을 고른다.
- 표와 흐름(table·flow)처럼 부품이 없는 유형은 None을 돌려주고 호출하는 쪽이 기본 빌더를 쓴다.
- 출력 파일에는 <meta name="ethos-design" content="free">와 <meta name="ethos-auto" content="1">를 단다.
  QA는 자유 디자인 기준(글자 16px 이상, 시각 중심)으로 보고, design_review.py는 "자동 초안"으로 구분한다.

쓰는 법: python scripts/auto_design.py content/<ID> --lang ko --out <dir>   (기본 out: content/<ID>/auto/<lang>)
"""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_cards import esc, icon_path, icon_svg, item_text, label_parts, strip_step_prefix  # noqa: E402

OBJ_DIR = ROOT / "assets" / "illustrations" / "objects"
# 아이콘 이름 → 물건 그림(Phosphor). 표지·인용 카드의 큰 그림으로 쓴다.
OBJECT_FOR = {
    "gavel": "gavel", "scale": "scales", "scales": "scales", "landmark": "bank", "receipt": "receipt",
    "file-text": "file-text", "calendar": "calendar-x", "calendar-x": "calendar-x", "calendar-clock": "calendar-x",
    "truck": "truck", "store": "storefront", "building-2": "building-office", "briefcase": "briefcase",
    "stamp": "stamp", "ban": "prohibit", "circle-dollar-sign": "money", "hourglass": "hourglass-medium",
    "clipboard-check": "clipboard-text", "search": "magnifying-glass", "handshake": "handshake",
}
NEGATIVE_ICONS = {"ban", "x", "x-circle", "circle-x", "octagon-x", "prohibit"}


def obj_svg(name):
    target = OBJECT_FOR.get(name or "")
    path = OBJ_DIR / f"{target}.svg" if target else None
    return path.read_text(encoding="utf-8").strip() if path and path.exists() else ""


def safe_icon(name):
    try:
        return icon_svg(name) if name and icon_path(name) else ""
    except Exception:
        return ""


def _head(depth):
    up = "../" * depth
    return (f'<link rel="stylesheet" href="{up}brand/tokens.css">\n<link rel="stylesheet" href="{up}brand/fonts.css">\n'
            f'<link rel="stylesheet" href="{up}templates/base.css">\n<link rel="stylesheet" href="{up}templates/card-types.css">\n'
            f'<link rel="stylesheet" href="{up}templates/presets/ethos-a.css">')


def _short(text, language, ko, en):
    return len(text) <= (ko if language == "ko" else en)


def cover_main(card, language):
    body = card.get("body", [])
    lede = f'<p class="cv-lede">{esc(item_text(body[0]))}</p>' if body else ""
    promise = f'<p class="cv-promise" data-role="label">{esc(card["promise"])}</p>' if card.get("promise") else ""
    art = ""
    if card.get("coverStyle") == "stat" and card.get("hero"):
        art = (f'<div class="cv-stat" data-focal><span class="cv-stat-b" data-role="label">{esc(card["hero"]["value"])}</span>'
               f'<span class="cv-promise" data-role="label" style="margin:0">{esc(card["hero"]["label"])}</span></div>')
    else:
        for name in card.get("art") or [card.get("icon")]:
            svg = obj_svg(name)
            if svg:
                art = f'<div class="obj-hero" data-decor data-focal style="align-self:center;width:150px;height:150px">{svg}</div>'
                break
    return f'{art}<div class="cv-wrap">{lede}{promise}</div>'


def krows(body, language="ko", focal=True):
    long_key = any(len(label_parts(x)[0]) > (4 if language == "ko" else 10) for x in body)
    rows = []
    for item in body:
        key, text = label_parts(item)
        rows.append(f'<div class="krow"><div class="krow-k">{esc(key)}</div><div class="krow-t">{esc(text)}</div></div>' if key
                    else f'<div class="krow"><div class="krow-t" style="grid-column:1/-1">{esc(text)}</div></div>')
    cls = "krows stack" if long_key else "krows"
    return f'<div class="{cls}"{" data-focal" if focal else ""}>' + "".join(rows) + "</div>"


def versus(body):
    cols = []
    for item in body[:2]:
        key, text = label_parts(item)
        cols.append(f'<div><div class="vs-k">{esc(key)}</div><div class="vs-t">{esc(text)}</div></div>')
    wide = ""
    if len(body) == 3:
        key, text = label_parts(body[2])
        wide = f'<div class="vs-wide"><div class="vs-wide-k">{esc(key)}</div><div class="vs-wide-t">{esc(text)}</div></div>'
    return f'<div class="versus" data-focal>{"".join(cols)}</div>{wide}'


def ico_rows(body):
    rows = []
    for item in body:
        key, text = label_parts(item)
        icon = safe_icon(item.get("icon")) if isinstance(item, dict) else ""
        rows.append(f'<div class="ico-row"><div class="badge">{icon}</div><div><div class="ico-row-k">{esc(key)}</div>'
                    f'<div class="ico-row-t">{esc(text)}</div></div></div>')
    return '<div class="ico-rows" data-focal>' + "".join(rows) + "</div>"


def quote(card):
    body = card.get("body", [])
    src, text, note = (item_text(x) for x in (body + ["", "", ""])[:3])
    art = obj_svg(card.get("icon"))
    head = (f'<div class="q-head"><div class="q-art" data-decor data-focal>{art}</div><div class="q-src" data-role="label">{esc(src)}</div></div>'
            if art else f'<div class="q-src" data-role="label">{esc(src)}</div>')
    note_html = f'<div class="q-note">{esc(note)}</div>' if note else ""
    focal = "" if art else " data-focal"
    return f'{head}<div class="q-panel"{focal}><div class="q-body">{esc(text)}</div>{note_html}</div>'


def xlist(body):
    x = safe_icon("x")
    items = "".join(f'<div class="xitem">{x}<div>{esc(strip_step_prefix(item_text(t)))}</div></div>' for t in body)
    return f'<div class="xlist" data-focal>{items}</div>'


def steps(body):
    items = "".join(f'<div class="step"><div class="step-n" data-decor>{i}</div><div class="step-t">{esc(strip_step_prefix(item_text(t)))}</div></div>'
                    for i, t in enumerate(body, 1))
    return f'<div class="steps{" many" if len(body) >= 5 else ""}" data-focal>{items}</div>'


def bars(body):
    values = [float(item.get("value", 0) or 0) for item in body]
    top = max(values + [1e-9])
    rows = []
    for item, value in zip(body, values):
        pct = max(value / top * 100, 7.0)
        text = f'<div class="bar2-t">{esc(item.get("text", ""))}</div>' if item.get("text") else ""
        rows.append(f'<div><div class="bar2-head"><span class="bar2-k">{esc(item.get("key", ""))}</span><span class="bar2-v">{esc(item.get("display", ""))}</span></div>'
                    f'<div class="bar2-track"><div class="bar2-fill" style="width:{pct:.0f}%"></div></div>{text}</div>')
    return '<div class="bars2" data-focal>' + "".join(rows) + "</div>"


def stat_rows(body):
    rows = "".join(f'<div class="stat-row"><b>{esc(item.get("key", ""))}</b><span>{esc(item.get("text", ""))}</span></div>'
                   if isinstance(item, dict) else f'<div class="stat-row"><span>{esc(item)}</span></div>' for item in body)
    return f'<div class="stat-rows" data-focal>{rows}</div>'


def asks(body):
    return '<div class="asks" data-focal>' + "".join(f'<div class="ask">{esc(item_text(t))}</div>' for t in body) + "</div>"


def bound(body):
    icons = ["clipboard-check", "scale"]
    cols = []
    for i, item in enumerate(body[:2]):
        key, text = label_parts(item)
        deep = " deep" if i == 1 else ""
        color = "" if deep else ' style="color:var(--ethos-navy)"'
        cols.append(f'<div class="bound-col{deep}"><div class="bound-h"><div class="bound-ico"{color}>{safe_icon(icons[i])}</div>'
                    f'<div class="bound-k">{esc(key)}</div></div><div class="bound-t">{esc(text)}</div></div>')
    return '<div class="bound stack">' + "".join(cols) + "</div>"


def main_markup(card, language):
    """부품 하나를 고른다. 고를 부품이 없으면 None(호출하는 쪽이 기본 빌더를 쓴다)."""
    kind, body = card["type"], card.get("body", [])
    layout = card.get("layout")
    keyed = all(isinstance(x, dict) and x.get("key") for x in body)
    if kind == "cover":
        return cover_main(card, language)
    if kind == "quote" and len(body) >= 2:
        return quote(card)
    if kind == "concept" and keyed and len(body) in (2, 3) and all(_short(x["key"], language, 6, 16) for x in body[:2]):
        return versus(body)
    if kind in ("concept", "comparison") and keyed and all(isinstance(x, dict) and x.get("icon") for x in body):
        return ico_rows(body)
    if kind in ("concept", "comparison"):
        return krows(body, language)
    if kind == "process":
        return steps(body)
    if kind == "checklist":
        if layout == "bars":
            return bars(body)
        if layout == "stats":
            return stat_rows(body)
        if layout == "questions":
            return asks(body)
        if card.get("icon") in NEGATIVE_ICONS:
            return xlist(body)
        return krows(body, language) if keyed else steps(body)
    if kind == "cta" and len(body) == 2 and keyed:
        return bound(body)
    return None


# 본문이 넘치면 본문 글자만 4%씩 줄인다(16px 아래로는 줄이지 않는다). 그래도 넘치면 QA가 알려 주고 호출하는 쪽이 빌더로 되돌린다.
FIT_DOWN = (
    "<script>(function(){function fit(){var m=document.querySelector('.z-main');if(!m)return;"
    "var tx=[].slice.call(m.querySelectorAll('*')).filter(function(e){if(e.closest('[data-decor]')||e.closest('svg'))return false;"
    "for(var i=0;i<e.childNodes.length;i++){var n=e.childNodes[i];if(n.nodeType===3&&n.textContent.trim())return true}return false});"
    "var base=tx.map(function(e){return parseFloat(getComputedStyle(e).fontSize)});"
    "function over(){if(m.scrollHeight>m.clientHeight+1)return true;var all=m.querySelectorAll('*');"
    "for(var i=0;i<all.length;i++){var e=all[i];if(e.clientWidth>0&&e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).display!=='inline')return true}return false}"
    "for(var z=1;over()&&z>0.7;z-=0.04){tx.forEach(function(e,i){e.style.fontSize=Math.max(16,base[i]*z)+'px'})}"
    "m.setAttribute('data-fit',z.toFixed(2))}"
    "if(document.fonts&&document.fonts.ready){document.fonts.ready.then(fit)}else{fit()}})();</script>"
)


def build(card, data, depth=3):
    """자유 디자인 HTML 한 장. 부품이 없으면 None."""
    language = data["language"]
    main = main_markup(card, language)
    if main is None:
        return None
    page, bg = card["page"], card["bg"]
    org = "에토스 행정사사무소" if language == "ko" else "Ethos Administrative Attorney Office"
    if card["type"] == "cover":
        title = f'<p class="cv-title" data-role="headline">{esc(card["headline"])}</p>'
    else:
        title = f'<h2 class="h2" data-role="headline">{esc(card["headline"])}</h2>'
    style = card.get("takeStyle") or ("bar" if card["type"] in ("cover", "cta") else "close")
    take = card.get("takeaway", "")
    take_html = (f'<div class="take" data-role="takeaway">{esc(take)}</div>' if style == "bar"
                 else f'<div class="close" data-role="takeaway">{esc(take)}</div>') if take else ""
    return f"""<!doctype html>
<html lang="{language}"><head><meta charset="utf-8"><meta name="ethos-design" content="free"><meta name="ethos-auto" content="1">
{_head(depth)}
<style>.card.free .h2{{font-size:{35 if language == "ko" else 32}px;line-height:1.24}} .cv-title{{font-size:{38 if language == "ko" else 34}px}}</style>
</head><body>
<div class="card free {esc(bg)} lang-{language} canvas-portrait family-social-native" data-card-type="{esc(card['type'])}" data-bg="{esc(bg)}" data-page="{page}" data-canvas="portrait" data-visual-family="social-native">
  <div class="gold-top" data-frame="gold-top"></div>
  <div class="hdr"><span class="wm" data-frame="wordmark">ETHOS BRIEF</span><span class="sec" data-frame="section">{esc(data['series'])} · {esc(data['issue'])}</span></div>
  <div class="hl" data-frame="line"></div>
  <div class="body">
    <div class="z-title" data-zone="title">{title}</div>
    <div class="z-main" data-zone="main">{main}</div>
    <div class="z-take" data-zone="take">{take_html}</div>
  </div>
  <div class="ftr"><div class="org" data-frame="org">{org}</div><div class="tagl" data-frame="tagline">LOGOS · PATHOS · ETHOS</div><div class="pg" data-frame="page" aria-hidden="true"></div></div>
  <div class="gold-bottom" data-frame="gold-bottom"></div>
</div>""" + FIT_DOWN + """</body></html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", help="content/<ID>")
    parser.add_argument("--lang", default="ko")
    parser.add_argument("--out", help="출력 폴더(저장소 루트에서 3단계 깊이여야 CSS 경로가 맞는다)")
    args = parser.parse_args()
    folder = pathlib.Path(args.folder)
    data = json.loads((folder / f"card-data.{args.lang}.json").read_text(encoding="utf-8"))
    out = pathlib.Path(args.out) if args.out else folder / "auto" / args.lang
    depth = len(out.resolve().relative_to(ROOT).parts)
    out.mkdir(parents=True, exist_ok=True)
    made, skipped = 0, []
    for card in data["cards"]:
        html = build(card, data, depth)
        if html is None:
            skipped.append(card["page"])
            continue
        (out / f"card_{card['page']:02d}.html").write_text(html, encoding="utf-8")
        made += 1
    print(f"auto design: {made} cards -> {out}" + (f" (기본 빌더 필요: {skipped})" if skipped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
