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
- layout-repeat  : 본문 구조가 연속·과반 또는 A-B-A-B로 반복된다.
- visual-thin    : 그림과 명시된 시각 중심이 모두 없을 때 실제 이미지 확인 안내. 개수 할당 없음.

쓰는 법: python scripts/design_review.py content/<ID> [--lang ko|en] [--strict]
"""

import argparse
import collections
import pathlib
import re
import sys

FREE_MARK = re.compile(r'<meta\s+name="ethos-design"\s+content="free"', re.I)
AUTO_MARK = re.compile(r'<meta\s+name="ethos-auto"', re.I)
TYPE_MARK = re.compile(r'data-card-type="([^"]+)"', re.I)
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

    typed = [(name, html, (TYPE_MARK.search(html).group(1).lower() if TYPE_MARK.search(html) else None))
             for name, html in pages]
    if any(kind for _, _, kind in typed):
        body = [(name, html) for name, html, kind in typed if kind not in ("cover", "cta")]
        cover = next((html for _, html, kind in typed if kind == "cover"), pages[0][1])
    else:
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
                             "실제 시트에서 반복이 이해를 돕는지 확인하세요. 같은 구조가 적합하면 유지합니다."))
    counted = collections.Counter(k for k in kinds if k)
    if counted and body:
        kind, n = counted.most_common(1)[0]
        if n > len(body) / 2:
            findings.append(("warn", "focal-repeat", f"시각 중심 '{kind}'이 본문 {len(body)}장 중 {n}장입니다.",
                             "비율만으로 미감을 판단하지 않습니다. 메시지 차이가 실제로 읽히는지 확인하세요."))

    prev = None
    signatures = []
    for name, html in body:
        sig = top_children(_zone(html, "main"))
        signatures.append((name, sig))
        if sig and sig == prev:
            findings.append(("warn", "layout-repeat", f"{name}: 앞 카드와 본문 구조가 같습니다({' + '.join(sig)}).",
                             "연결된 비교라면 같은 구도가 유용할 수 있습니다. 장식용 변주보다 정보 관계를 우선하세요."))
        prev = sig
    counted_layouts = collections.Counter(tuple(sig) for _, sig in signatures if sig)
    if counted_layouts and body:
        signature, n = counted_layouts.most_common(1)[0]
        if n > len(body) / 2:
            findings.append(("warn", "layout-repeat",
                             f"본문 구조 '{' + '.join(signature)}'가 {len(body)}장 중 {n}장입니다.",
                             "같은 정보 관계가 아니라면 표·흐름·강조 구도를 나눠 실제 시트의 리듬을 확인하세요."))
    sig_only = [tuple(sig) for _, sig in signatures if sig]
    for i in range(3, len(sig_only)):
        if sig_only[i] == sig_only[i - 2] and sig_only[i - 1] == sig_only[i - 3] and sig_only[i] != sig_only[i - 1]:
            findings.append(("warn", "layout-repeat", "본문 구조가 A-B-A-B로 교대 반복됩니다.",
                             "정보 관계가 다른 카드 하나를 다른 구도로 바꿔 기계적인 반복을 끊으세요."))
            break

    with_visual = sum(1 for _, html in pages if "<svg" in _zone(html, "main") or "<svg" in _zone(html, "title"))
    if with_visual == 0 and not any(focal_kind(html) for _, html in pages):
        findings.append(("info", "visual-thin", "그림과 명시된 시각 중심이 없습니다.",
                         "실제 축소 이미지를 확인하세요. 타이포그래피·여백으로 메시지가 읽히면 그림을 추가할 필요 없습니다."))
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
            print("HTML 휴리스틱 경고 없음. 미감·가독성은 실제 이미지에서 확인하세요.")
        for level, rule, message, fix in findings:
            warns += level == "warn"
            print(f"{level.upper():4} {rule:14} {message}\n     → {fix}")
    return 1 if args.strict and warns else 0


if __name__ == "__main__":
    sys.exit(main())
