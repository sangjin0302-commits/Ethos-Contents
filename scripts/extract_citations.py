#!/usr/bin/env python3
"""Offline citation extractor for ETHOS drafts (no network).

Reads blog.md / website MD / any text file, or a card-data JSON, and lists every
statute article, annex (별표), court case number and administrative-appeal decision
number it cites. The output is a checklist to paste into `citations.md` and to verify
with korean-law-mcp (`legal_analysis` mode `verify_citations`) or by hand on
국가법령정보센터. This script only finds citations; it never says whether they are right.

Scope rules (docs/legal-verification.md "인용 검증"):
- 「법령명」 제N조(의N)(제N항)(제N호), plus unbracketed '…법 제N조' and '같은 법/동법'.
- A bare 제N조 inherits the most recent law name in the same paragraph (blank-line block;
  one card in card-data). Without one it is listed with "법령명 불명" so a person checks it.
- 별표 N, case numbers such as 2023두12345, 대법원 YYYY. M. D. 선고 …, and appeal
  decisions such as 2021경기행심1356 or 서울특별시행정심판위원회 2024-01195.
- English card copy (Article 32 …) is out of scope; the Korean set carries the same facts.
"""

import argparse
import json
import pathlib
import re
import sys

LAW_SUFFIX = r"(?:법|법률|령|규칙|조례|규정|고시|훈령|예규|지침|기준)"
# 「…」 that names a statute. Series titles such as 「사업이 멈추는 행정처분」 do not end with a law suffix.
BRACKET_LAW = re.compile(r"「([^」\n]{1,80}?" + LAW_SUFFIX + r")」(?:\s*(시행령|시행규칙))?")
# Unbracketed '식품위생법 제82조' / '행정사법 시행령 제5조'. Needs an article right after it.
# 마지막 어절만 잡고, 띄어 쓴 정식 제명('개인정보 보호법', '국토의 계획 및 이용에 관한 법률')은 plain_law_title()이 왼쪽으로 넓힌다.
PLAIN_LAW = re.compile(r"(?<![가-힣「])((?:[가-힣]{0,30}?법률|[가-힣]{1,30}?법))(?:\s+(시행령|시행규칙))?(?=\s*제\s*\d+\s*조)")
# 문장 어절(조사로 끝남)이면 제명에 넣지 않는다. 제명 안의 '…의', '…및', '…에 관한', '…과'는 넣는다.
SENTENCE_WORD = re.compile(r"(?:은|는|이|가|을|를|도|만|에서|으로|로|께서|부터|까지|라고|하면|하고|했|합니다|입니다|[.,:;!?)」』])$")
TITLE_WORD = re.compile(r"^[가-힣·]+$")


STOP_WORDS = {"그러나", "그리고", "따라서", "또한", "역시", "다만", "특히", "즉", "이", "그", "이런", "해당", "같은", "현행", "개정", "구"}


def plain_law_title(text, start, last_word):
    """PLAIN_LAW가 잡은 마지막 어절 앞의 어절을 제명으로 붙일지 정한다. 반환: 새 시작 위치.

    - '…법률'로 끝나면 '국토의 계획 및 이용에 관한 법률'처럼 최대 7어절까지 넓힌다.
    - '…법'으로 끝나면 '개인정보 보호법'처럼 짧은 끝 어절(4자 이하)에만 앞 어절 하나를 붙인다.
    문장 어절(조사·어미로 끝남)이나 접속어('그러나', '역시' 등)를 만나면 멈춘다."""
    limit = 7 if last_word.endswith("법률") else (1 if len(last_word) <= 4 else 0)
    offset = max(0, start - 80)
    words = list(re.finditer(r"\S+", text[offset:start]))
    new_start, taken = start, 0
    for w in reversed(words):
        word = w.group()
        if taken >= limit or not TITLE_WORD.match(word) or SENTENCE_WORD.search(word) or word in STOP_WORDS or re.search(r"(?:다면|면|며|고|서|지만)$", word):
            break
        if text[offset + w.end():new_start].strip():
            break
        new_start, taken = offset + w.start(), taken + 1
    return new_start
SAME_LAW = re.compile(r"(?:같은\s*법|동법)(?:\s*(시행령|시행규칙))?(?=\s*(?:제\s*\d+\s*조|별표))")
ARTICLE = re.compile(
    r"제\s*(\d+)\s*조(?:\s*의\s*(\d+))?"
    r"(?:\s*제\s*(\d+)\s*항)?"
    r"(?:\s*제\s*(\d+)\s*호)?"
)
ANNEX = re.compile(r"(?:(시행령|시행규칙)\s*)?\[?별표\s*(\d+)(?:\s*의\s*(\d+))?\]?")

COURT = r"(?:대법원|헌법재판소|[가-힣]{2,8}(?:고등|지방|행정|가정)법원(?:\s*[가-힣]{1,4}지원)?)"
# 법원 사건부호. 'n년' 같은 일반 숫자 표현과 섞이지 않도록 허용 부호만 쓴다.
CASE_CODES = ("헌마|헌바|헌가|헌라|헌사|구합|구단|가합|가단|가소|고합|고단|고정|노|도|두|누|다|나|구|므|스|마|카|후|허|재|모|오|초")
CASE_NO = re.compile(r"(?<![\d-])((?:19|20)\d{2})\s?(" + CASE_CODES + r")\s?(\d{1,6})(?!\d)")
DATED_CASE = re.compile(
    r"(" + COURT + r")\s*((?:19|20)\d{2})\.\s*(\d{1,2})\.\s*(\d{1,2})\.\s*선고\s*"
    r"((?:19|20)\d{2})\s?(" + CASE_CODES + r")\s?(\d{1,6})(?!\d)(?:\s*(판결|결정))?"
)
COURT_BEFORE = re.compile(r"(" + COURT + r")\s*$")
# 2021경기행심1356 처럼 붙여 쓰는 행정심판 사건번호.
APPEAL_COMPACT = re.compile(r"(?<!\d)((?:19|20)\d{2})([가-힣]{0,6}행심)(\d{1,6})(?!\d)")
# 서울특별시행정심판위원회 2024-01195 / 서울행심 2024-01195 / 행심 제2025-40호.
APPEAL_BODY = r"((?:[가-힣]{0,12}행정심판위원회)(?:\s*행심)?|(?:[가-힣]{0,6}행심))"
APPEAL_DASH = re.compile(APPEAL_BODY + r"\s*(?:제\s*)?((?:19|20)\d{2})\s*-\s*(\d{1,6})(?:\s*호)?(?!\d)")


def unknown(hint):
    """법령명을 같은 문단에서 찾지 못한 인용의 표시. 앞 문단 법령은 추정이 아니라 사람이 볼 단서다."""
    return f"(법령명 불명 · 앞 문단: 「{hint}」)" if hint else "(법령명 불명)"


def article_label(match):
    """제28조제5항 형태(법제처 표기)로 정규화한다."""
    jo, ui, hang, ho = match.group(1), match.group(2), match.group(3), match.group(4)
    label = f"제{jo}조" + (f"의{ui}" if ui else "")
    if hang:
        label += f"제{hang}항"
    if ho:
        label += f"제{ho}호"
    return label


def law_title(name, sub):
    name = re.sub(r"\s+", " ", name.strip())
    return f"{name} {sub}" if sub and not name.endswith(sub) else name


class Collector:
    def __init__(self):
        self.items = {}
        self.last_law = ""  # 앞 문단(카드)의 마지막 법령명. 법령명 불명 항목의 힌트로만 쓴다.

    def add(self, key, kind, citation, where, law=""):
        item = self.items.get(key)
        if item is None:
            self.items[key] = {"citation": citation, "kind": kind, "law": law, "locations": [where]}
            return
        if where not in item["locations"]:
            item["locations"].append(where)
        if len(citation) > len(item["citation"]):
            item["citation"] = citation  # 법원명·선고일이 붙은 더 긴 표기를 남긴다

    def results(self):
        return list(self.items.values())


def scan_block(text, where_of, out):
    """One paragraph (or one card). `where_of(offset)` turns a character offset into a location label."""
    taken = []

    def free(start, end):
        return not any(start < e and s < end for s, e in taken)

    # 1) 판례·재결례 번호 (조문 번호와 겹치지 않게 먼저 잡는다)
    for m in DATED_CASE.finditer(text):
        number = f"{m.group(5)}{m.group(6)}{m.group(7)}"
        label = f"{m.group(1)} {m.group(2)}. {m.group(3)}. {m.group(4)}. 선고 {number}" + (f" {m.group(8)}" if m.group(8) else "")
        out.add(("case", number), "case", label, where_of(m.start()))
        taken.append(m.span())
    for m in APPEAL_COMPACT.finditer(text):
        if free(*m.span()):
            number = "".join(m.groups())
            out.add(("appeal", number), "appeal", number, where_of(m.start()))
            taken.append(m.span())
    for m in APPEAL_DASH.finditer(text):
        if free(*m.span()):
            number = f"{m.group(2)}-{m.group(3)}"
            out.add(("appeal", number), "appeal", f"{m.group(1)} {number}", where_of(m.start()))
            taken.append(m.span())
    for m in CASE_NO.finditer(text):
        if not free(*m.span()):
            continue
        number = "".join(m.groups())
        court = COURT_BEFORE.search(text[max(0, m.start() - 20):m.start()])
        label = f"{court.group(1)} {number}" if court else number
        out.add(("case", number), "case", label, where_of(m.start()))
        taken.append(m.span())

    # 2) 법령명 앵커를 위치순으로 모은다
    anchors = []
    for m in BRACKET_LAW.finditer(text):
        anchors.append((m.start(), m.end(), law_title(m.group(1), m.group(2))))
    for m in PLAIN_LAW.finditer(text):
        if free(*m.span()) and not any(s <= m.start() < e for s, e, _ in anchors):
            begin = plain_law_title(text, m.start(1), m.group(1))
            name = re.sub(r"\s+", " ", text[begin:m.end(1)])
            anchors.append((begin, m.end(), law_title(name, m.group(2))))
    anchors.sort()

    def base_law(title):
        return re.sub(r"\s+(시행령|시행규칙)$", "", title)

    def current_law(offset):
        before = [a for a in anchors if a[1] <= offset]
        return before[-1][2] if before else ""

    same_law = []
    for m in SAME_LAW.finditer(text):
        law = current_law(m.start())
        if law:
            same_law.append((m.start(), m.end(), law_title(base_law(law), m.group(1))))
    anchors = sorted(anchors + same_law)

    # 3) 조문
    for m in ARTICLE.finditer(text):
        if not free(*m.span()):
            continue
        label = article_label(m)
        law = current_law(m.start())
        if law:
            citation = f"「{law}」 {label}"
            key = ("article", law, label)
        else:
            citation = f"{label} {unknown(out.last_law)}"
            key = ("article", "?" + out.last_law, label)
        out.add(key, "article", citation, where_of(m.start()), law)
        taken.append(m.span())

    # 4) 별표. 바로 앞의 '시행령/시행규칙'은 같은 문단의 법령명에 붙인다.
    for m in ANNEX.finditer(text):
        if not free(*m.span()):
            continue
        label = f"별표 {m.group(2)}" + (f"의{m.group(3)}" if m.group(3) else "")
        law = current_law(m.start())
        sub = m.group(1)
        if law and sub:
            law = law_title(base_law(law), sub)
        if law and not sub and not re.search(r"(?:령|규칙)$", law):
            # 법률 본문에는 별표가 드물다. 시행령·시행규칙 별표를 줄여 쓴 경우가 많으므로 사람이 정한다.
            citation = f"{label} (「{law}」 또는 그 시행령·시행규칙 — 법령명 확인 필요)"
            out.add(("annex", "?" + law, label), "annex", citation, where_of(m.start()), None)
            taken.append(m.span())
            continue
        if law:
            citation = f"「{law}」 {label}"
        else:
            citation = f"{sub + ' ' if sub else ''}{label} {unknown(out.last_law)}"
        key = ("annex", law, label) if law else ("annex", f"?{out.last_law}|{sub or ''}", label)
        out.add(key, "annex", citation, where_of(m.start()), law)
        taken.append(m.span())

    if anchors:
        out.last_law = base_law(anchors[-1][2])


def extract_text(text):
    out = Collector()
    lines = text.splitlines()
    block, start = [], 0
    for index, line in enumerate(lines + [""]):
        if line.strip():
            if not block:
                start = index
            block.append(line)
            continue
        if block:
            joined = "\n".join(block)
            starts = [0]
            for piece in block[:-1]:
                starts.append(starts[-1] + len(piece) + 1)
            first = start

            def where_of(offset, starts=starts, first=first):
                row = max(i for i, s in enumerate(starts) if s <= offset)
                return f"L{first + row + 1}"

            scan_block(joined, where_of, out)
            block = []
    return out.results()


def card_strings(value, path):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, list):
        for i, item in enumerate(value):
            yield from card_strings(item, f"{path}[{i}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in ("sourceTrace", "editorialReview", "pageTurn"):
                continue  # 편집 메타데이터는 게시 문구가 아니다
            yield from card_strings(item, f"{path}.{key}" if path else key)


def extract_card_data(data):
    out = Collector()
    for index, card in enumerate(data.get("cards", [])):
        page = card.get("page", index + 1)
        parts = list(card_strings(card, ""))
        joined, offsets = "", []
        for path, value in parts:
            offsets.append((len(joined), path))
            joined += value + "\n"

        def where_of(offset, offsets=offsets, page=page):
            path = [p for s, p in offsets if s <= offset][-1]
            return f"card {page} {path}"

        scan_block(joined, where_of, out)
    return out.results()


def extract(path):
    path = pathlib.Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return extract_card_data(json.loads(text))
    return extract_text(text)


def markdown_table(items, source=""):
    rows = [
        f"<!-- extract_citations.py {source} | 결과: ✓ 일치 · ✗ 없음/불일치 · ⚠ 확인 불가·법령명 불명 -->",
        "| 인용 | 위치(line) | 결과 ✓/✗/⚠ | 확인일 |",
        "|---|---|---|---|",
    ]
    for item in items:
        where = ", ".join(item["locations"][:6]) + (" …" if len(item["locations"]) > 6 else "")
        rows.append(f"| {item['citation']} | {where} |  |  |")
    return "\n".join(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description="원고·card-data에서 법령·조문·별표·판례·재결 인용을 뽑아 확인표를 만든다 (오프라인).")
    parser.add_argument("path", help="blog.md, 웹사이트 MD, 텍스트 파일 또는 card-data.*.json")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--json", action="store_true", help="JSON으로 출력")
    group.add_argument("--plain", action="store_true", help="한 줄에 인용 하나 (verify_citations의 text 입력용)")
    args = parser.parse_args(argv)
    path = pathlib.Path(args.path)
    if not path.is_file():
        print(f"파일이 없습니다: {path}", file=sys.stderr)
        return 2
    items = extract(path)
    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
    elif args.plain:
        # 법령명 불명 항목은 도구가 엉뚱한 법령으로 판정하지 않도록 빼고, 사람이 볼 목록으로 따로 알린다.
        print("\n".join(item["citation"] for item in items if item["law"] or item["kind"] in ("case", "appeal")))
        unresolved = [item["citation"] for item in items if not item["law"] and item["kind"] in ("article", "annex")]
        if unresolved:
            print(f"[사람 확인] 법령명 불명 {len(unresolved)}건: " + "; ".join(unresolved), file=sys.stderr)
    else:
        print(markdown_table(items, path.as_posix()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
