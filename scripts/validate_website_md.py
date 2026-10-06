#!/usr/bin/env python3
"""웹사이트 블로그용 국·영문 MD 검사 (docs/website-md-spec.md).

사용: python scripts/validate_website_md.py content/<ID>
머리말 키와 값, 본문 마크다운(제목·표·굵게 짝·링크), 영문 색인 기준을 확인한다.
error는 관리자 입력이나 공개 화면이 깨지는 문제, warn은 다듬을 곳이다.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "copy-rules.json").read_text(encoding="utf-8"))
CATEGORIES = {"visa", "appeal", "contract", "license", "corporate", "other"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CONTACT = re.compile(r"(?:kakao|talk\.naver|t\.me/|mailto:|tel:|@gmail\.com|@naver\.com|010-\d{3,4}-\d{4})", re.IGNORECASE)
TRACKING = re.compile(r"[?&](?:utm_[\w.-]+|oc)=", re.IGNORECASE)


def split_front(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    head, body = text[3:end], text[end + 4:]
    data = {}
    for line in head.strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("["):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = [v.strip().strip("'\"") for v in value.strip("[]").split(",") if v.strip()]
        data[key.strip()] = value.strip("'\"") if isinstance(value, str) else value
    return data, body.lstrip("\n")


def check(path, lang):
    errors, warns = [], []
    text = path.read_text(encoding="utf-8")
    front, body = split_front(text)
    if front is None:
        return {"slug": None, "category": None}, [f"{path.name}: 맨 위 YAML 머리말(---)이 없습니다"], []
    title_key, excerpt_key, tags_key = ("title", "excerpt", "tags") if lang == "ko" else ("titleEn", "excerptEn", "tagsEn")
    for key in ("slug", title_key, excerpt_key, "category", tags_key, "date"):
        if not front.get(key):
            errors.append(f"{path.name}: 머리말 '{key}'가 비어 있습니다")
    slug = str(front.get("slug", ""))
    if slug and (len(slug) > 100 or not SLUG.match(slug) or "-excerpt-" in slug):
        errors.append(f"{path.name}: slug '{slug}'는 영문 소문자·숫자·하이픈 100자 이내여야 합니다")
    if front.get("category") and front["category"] not in CATEGORIES:
        errors.append(f"{path.name}: category는 {sorted(CATEGORIES)} 중 하나여야 합니다")
    excerpt = str(front.get(excerpt_key, ""))
    low, high = (80, 150) if lang == "ko" else (60, 160)
    if excerpt and not low <= len(excerpt) <= high:
        warns.append(f"{path.name}: 요약 {len(excerpt)}자 (권장 {low}~{high}자)")
    raw_tags = front.get(tags_key) or []
    tags = [t.strip() for t in raw_tags.split(",") if t.strip()] if isinstance(raw_tags, str) else [str(t).strip() for t in raw_tags]
    if any("#" in tag for tag in tags):
        errors.append(f"{path.name}: 웹사이트 태그에는 '#'을 쓰지 않습니다. 관리자 칸은 쉼표로 나눈 글자를 그대로 저장하므로 '#'이 태그에 들어갑니다")
    if isinstance(raw_tags, list) and raw_tags:
        warns.append(f"{path.name}: 태그를 배열이 아니라 '태그1, 태그2, 태그3' 한 줄(쉼표 구분)로 쓰세요. 관리자 입력칸과 같은 형식입니다")
    if tags and not 4 <= len(tags) <= 10:
        warns.append(f"{path.name}: 태그 {len(tags)}개 (권장 4~10개)")
    if len(set(tags)) != len(tags):
        warns.append(f"{path.name}: 같은 태그가 두 번 있습니다")

    lines = body.splitlines()
    if any(re.match(r"^#\s", line) for line in lines):
        errors.append(f"{path.name}: 본문에 '# 제목'이 있습니다. 제목은 머리말에만 두고 소제목은 '##'를 쓰세요")
    if any(re.match(r"^\s*\|.*\|\s*$", line) for line in lines) and any(re.match(r"^\s*\|?\s*:?-{3,}", line) for line in lines):
        errors.append(f"{path.name}: 마크다운 표가 있습니다. 웹사이트가 표를 변환하지 않아 글자로 보입니다. 목록으로 바꾸세요")
    if body.count("**") % 2:
        errors.append(f"{path.name}: 짝이 맞지 않는 '**'가 있습니다")
    if CONTACT.search(body):
        errors.append(f"{path.name}: 본문에 연락처·메신저 링크가 있습니다")
    if TRACKING.search(body):
        errors.append(f"{path.name}: 추적값(utm_)이나 API 키(OC=)가 붙은 링크가 있습니다")
    if not any(re.match(r"^##\s", line) for line in lines):
        warns.append(f"{path.name}: '##' 소제목이 없습니다")
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    last = paragraphs[-1] if paragraphs else ""
    # FAQ: 웹사이트 extractFaqPairs는 'Q.' 줄 바로 다음 'A.' 줄만 FAQPage로 넣는다
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    for i, para in enumerate(paras):
        if re.match(r"^(?:[-*]\s*)?\*\*Q[.:]", para) or re.match(r"^[-*]\s+Q[.:]", para):
            warns.append(f"{path.name}: FAQ 질문은 굵게·목록 없이 'Q. '로 시작해야 웹사이트가 인식합니다: {para[:30]}")
        elif re.match(r"^Q[.:]\s", para) and not (i + 1 < len(paras) and re.match(r"^A\.\s", paras[i + 1])):
            warns.append(f"{path.name}: 'Q.' 다음 문단이 'A.'로 시작하지 않아 FAQ로 인식되지 않습니다: {para[:30]}")
    if lang == "ko" and "무료" not in last:
        warns.append(f"{path.name}: 마지막 문단이 무료 검토 안내가 아닙니다")
    if lang == "en":
        if "free" not in last.lower():
            warns.append(f"{path.name}: 마지막 문단이 free review 안내가 아닙니다")
        plain = re.sub(r"[#*>`\-\[\]()!]", " ", body)
        hangul = len(re.findall(r"[가-힣]", plain))
        words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", plain))
        chars = len(plain.strip())
        if len(str(front.get("titleEn", ""))) < 12:
            warns.append(f"{path.name}: 영문 제목이 12자보다 짧습니다")
        if chars < 1200 or words < 180:
            warns.append(f"{path.name}: 영문 본문 {chars}자·{words}단어 (웹사이트 색인 기준 1,200자·180단어 이상)")
        if hangul > 20 or (chars and hangul / chars > 0.03):
            warns.append(f"{path.name}: 영문 본문에 한글 {hangul}자 (기준 20자 이하, 3% 이하)")
        for fixed, banned in RULES.get("style", {}).get("en", {}).get("fixedTerms", {}).items():
            for word in banned:
                if re.search(r"\b" + re.escape(word) + r"s?\b", body + " " + str(front.get("titleEn", "")), re.IGNORECASE):
                    errors.append(f"{path.name}: '{word}' 대신 고정 번역어 '{fixed}'를 쓰세요")
    return front, errors, warns


def hints(folder):
    """윤문 힌트(권고, 결과에 영향 없음): 국문 띄어쓰기(kiwipiepy), 영문 문체(Vale). 도구가 없으면 건너뛴다."""
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import copy_lint
    except Exception:
        return []
    out = []
    for lang in ("ko", "en"):
        path = folder / f"website.{lang}.md"
        if not path.exists():
            continue
        _, body = split_front(path.read_text(encoding="utf-8"))
        if lang == "ko":
            out += [f"{path.name}: 띄어쓰기 '{a}' → '{b}'" for a, b in copy_lint.spacing_suggestions(body)]
        else:
            out += [f"{path.name}:{line} {check}: {message}" for line, check, message in copy_lint.vale_alerts(body)]
    return out


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    folder = pathlib.Path(argv[1])
    errors, warns, fronts = [], [], {}
    for lang in ("ko", "en"):
        path = folder / f"website.{lang}.md"
        if not path.exists():
            errors.append(f"{path} 없음")
            continue
        front, e, w = check(path, lang)
        fronts[lang] = front
        errors += e
        warns += w
    if len(fronts) == 2:
        for key in ("slug", "category"):
            if fronts["ko"].get(key) != fronts["en"].get(key):
                errors.append(f"국·영문 '{key}'가 다릅니다: {fronts['ko'].get(key)} / {fronts['en'].get(key)}")
    for e in errors:
        print("ERROR", e)
    for line in hints(folder):
        print("INFO ", line)
    for w in warns:
        print("WARN ", w)
    print(f"{'FAIL' if errors else 'PASS'}: website md {folder} — error {len(errors)}, warn {len(warns)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
