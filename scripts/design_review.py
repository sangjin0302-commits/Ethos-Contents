#!/usr/bin/env python3
"""카드 세트의 디자인 다양성 점검(권고, 렌더를 막지 않는다).

qa_render.py는 깨짐(넘침·폰트·대비)을 잡는다. 이 스크립트는 "양식집처럼 보이는가"를 HTML만 읽어 본다.
승인 세트 SUSPENSION-SURCHARGE-04가 기본 빌더로만 만들어져 10장이 같은 목록 틀, 아이콘 0개, 작은 숫자로
발행 직전까지 갔던 일을 다시 막기 위해 만들었다(2026-10-07).

검사(모두 권고):
- builder-only   : 자유 디자인 HTML이 하나도 없다(발행본은 docs/card-design-guide.md로 직접 디자인).
- auto-draft     : 자동 디자인 초안만 있다(안내). Codex가 다듬어 발행본으로 만든다.
- cover-plain    : 표지에 그림·큰 숫자 같은 시각 요소가 없다.
- focal-missing  : 본문 카드(표지·마지막 장 제외)에 data-focal이 없다.
- focal-repeat   : 같은 종류의 시각 중심(숫자·그림·막대·아이콘 행·목록·핵심어)이 세 장 연속이거나 세트 절반을 넘는다.
- layout-repeat  : 본문 영역의 구조(직계 자식 클래스)가 같은 카드가 연달아 나온다.
- visual-thin    : 아이콘·그림이 있는 카드가 세트의 3분의 1 미만이다.

쓰는 법: python scripts/design_review.py content/<ID> [--lang ko|en] [--strict]
"""

import argparse
import collections
import pathlib
import re
import sys

FREE_MARK = re.compile(r'<meta\s+name="ethos-design"\s+content="free"', re.I)
AUTO_MARK = re.compile(r'<meta\s+name="ethos-auto"', re.I)
TAG = re.compile(r"<(\w+)([^>]*)>")


def _classes(attrs):
    m = re.search(r'class="([^"]*)"', attrs)
    return m.group(1).split() if m else []


def _zone(html, name):
    """data-zone="<name>" 요소의 안쪽 HTML(같은 태그 깊이를 세어 닫는 태그를 찾는다)."""
    m = re.search(rf'<(\w+)[^>]*data-zone="{name}"[^>]*>', html)
    if not m:
        return ""
    tag, start, depth = m.group(1), m.end(), 1
    for t in re.finditer(rf"<(/?){tag}\b[^>]*>", html[start:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return html[start:start + t.start()]
    return html[start:]


def top_children(inner):
    """본문 영역 직계 자식들의 대표 클래스(첫 클래스). 구조 반복 판단에 쓴다."""
    out, depth = [], 0
    for m in re.finditer(r"<(/?)(\w+)([^>]*?)(/?)>", inner):
        closing, tag, attrs, selfclose = m.groups()
        if tag.lower() in ("br", "img", "path", "circle", "rect", "line", "polygon", "polyline", "ellipse") or selfclose:
            continue
        if closing:
            depth -= 1
            continue
        if depth == 0:
            cls = _classes(attrs)
            out.append(cls[0] if cls else tag.lower())
        depth += 1
    return tuple(out)


def focal_kind(html):
    """data-focal 요소의 종류: picture(그림 하나) · number(숫자) · chart(막대) · icons(아이콘 행) · list(행 목록) · keyword(글자·대조)."""
    m = re.search(r"<(\w+)([^>]*\bdata-focal\b[^>]*)>", html)
    if not m:
        return None
    tag, start, depth = m.group(1), m.end(), 1
    inner = html[start:]
    for t in re.finditer(rf"<(/?){tag}\b[^>]*>", inner):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            inner = inner[:t.start()]
            break
    text = re.sub(r"<[^>]+>", " ", re.sub(r"<svg.*?</svg>", " ", inner, flags=re.S))
    text = re.sub(r"\s+", " ", text).strip()
    svgs = inner.count("<svg")
    if svgs and len(text) < 12:
        return "picture"
    units = r"(?:일|개월|년|원|%|배|건|명|days?|weeks?|months?|mo|years?|yrs?|won|KRW|times|cases)"
    if re.search(r"\d", text) and re.fullmatch(rf"[\d.,→~\s-]+{units}?(?:[\s\d.,→~-]*{units})?[\s\d.,→~가-힣-]{{0,12}}", text, re.I):
        return "number"
    if re.search(r"width:\s*\d+(?:\.\d+)?%", inner):
        return "chart"
    if svgs >= 2:
        return "icons"
    if len(top_children(inner)) >= 3:
        return "list"
    return "keyword"


def review(folder, lang):
    html_dir = folder / lang
    files = sorted(html_dir.glob("card_*.html"))
    findings = []
    if not files:
        return [("info", "no-html", f"{lang}/card_*.html이 없습니다. 기본 빌더 미리보기만 있는 세트입니다.",
                 "발행본은 docs/card-design-guide.md로 카드마다 직접 디자인하세요.")]
    pages = [(f.name, f.read_text(encoding="utf-8")) for f in files]
    free = [name for name, html in pages if FREE_MARK.search(html)]
    auto = [name for name, html in pages if AUTO_MARK.search(html)]
    if free and len(auto) == len(free):
        findings.append(("info", "auto-draft", f"자동 디자인 초안입니다({len(auto)}장, scripts/auto_design.py).",
                         "발행본은 Codex가 content/<ID>/<lang>/로 복사해 카드마다 다듬으세요(docs/card-codex-production.md)."))
    if not free:
        findings.append(("warn", "builder-only", "자유 디자인 HTML이 없습니다(전부 기본 빌더).",
                         "기본 빌더는 미리보기용입니다. 발행본은 카드마다 직접 디자인하세요(docs/card-design-guide.md)."))

    body = pages[1:-1] if len(pages) > 2 else []
    cover = pages[0][1]
    if not re.search(r"<svg|data-focal|cv-stat|cv-duo|obj-hero|hand-hero|cv-art", _zone(cover, "main")):
        findings.append(("warn", "cover-plain", "표지 본문에 그림·큰 숫자가 없습니다.",
                         "큰 숫자 대비(.cv-duo/.cv-stat)나 주제 물건 그림(.obj-hero)으로 2초 안에 멈추게 하세요. JSON만 있다면 표지에 art(예: [\"gavel\"]) 또는 coverStyle:\"stat\"+hero를 넣으면 자동 디자인이 그린다."))

    kinds = []
    for name, html in body:
        kind = focal_kind(html)
        kinds.append(kind)
        if kind is None and free:
            findings.append(("warn", "focal-missing", f"{name}: data-focal이 없습니다.",
                             "큰 숫자·그림·핵심어 중 하나를 시각 중심으로 크게 두세요(가이드 10-0-1)."))
    if not free and body:
        missing = sum(1 for k in kinds if k is None)
        if missing:
            findings.append(("warn", "focal-missing", f"본문 {len(body)}장 중 {missing}장에 data-focal이 없습니다.",
                             "큰 숫자·그림·핵심어 중 하나를 시각 중심으로 크게 두세요(가이드 10-0-1)."))
    run = 1
    for i in range(1, len(kinds)):
        run = run + 1 if kinds[i] and kinds[i] == kinds[i - 1] else 1
        if run == 3:
            findings.append(("warn", "focal-repeat", f"{body[i][0]}: 시각 중심 '{kinds[i]}'이 세 장 연속입니다.",
                             "숫자 → 그림 → 핵심어 → 막대·아이콘 행처럼 바꿔 가며 쓰세요."))
    counted = collections.Counter(k for k in kinds if k)
    if counted and body:
        kind, n = counted.most_common(1)[0]
        if n > len(body) / 2:
            findings.append(("warn", "focal-repeat", f"시각 중심 '{kind}'이 본문 {len(body)}장 중 {n}장입니다.",
                             "한 종류가 절반을 넘으면 넘기는 재미가 줄어듭니다."))

    prev = None
    for name, html in body:
        sig = top_children(_zone(html, "main"))
        if sig and sig == prev:
            findings.append(("warn", "layout-repeat", f"{name}: 앞 카드와 본문 구조가 같습니다({' + '.join(sig)}).",
                             "연속 두 장이 같은 구도가 되지 않게 하세요(가이드 3-6)."))
        prev = sig

    with_visual = sum(1 for _, html in pages if "<svg" in _zone(html, "main") or "<svg" in _zone(html, "title"))
    if with_visual * 3 < len(pages):
        findings.append(("warn", "visual-thin", f"아이콘·그림이 있는 카드가 {with_visual}/{len(pages)}장입니다.",
                         "세트의 3분의 1 이상에 의미 있는 아이콘이나 그림을 두세요(python scripts/icon_svg.py <이름>)."))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", help="content/<ID>")
    parser.add_argument("--lang", nargs="*", default=["ko", "en"])
    parser.add_argument("--strict", action="store_true", help="warn이 있으면 실패로 끝낸다")
    args = parser.parse_args()
    folder = pathlib.Path(args.folder)
    warns = 0
    for lang in args.lang:
        if not (folder / lang).exists() and not (folder / f"card-data.{lang}.json").exists():
            continue
        findings = review(folder, lang)
        print(f"## design review [{lang}] {folder.name}")
        if not findings:
            print("PASS: 시각 중심·구도·그림이 고르게 섞여 있습니다.")
        for level, rule, message, fix in findings:
            warns += level == "warn"
            print(f"{level.upper():4} {rule:14} {message}\n     → {fix}")
    return 1 if args.strict and warns else 0


if __name__ == "__main__":
    sys.exit(main())
