#!/usr/bin/env python3
"""Copy-quality linter for ETHOS card-data, captions and blog drafts.

gates.json guards layout and fact integrity. This script guards what readers feel:
repeated headline shapes, stacked negations, statute numbers on a phone-sized card,
unexplained jargon, covers that make no promise, and leftover placeholders.
Findings are advisory (warn/info); --strict turns warnings into a failing exit code.
"""

import argparse
import collections
import difflib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "copy-rules.json").read_text(encoding="utf-8"))
GATES = json.loads((ROOT / "gates.json").read_text(encoding="utf-8"))
LIMITS = json.loads((ROOT / "card-limits.json").read_text(encoding="utf-8"))


_KIWI = None


def kiwi():
    """Korean morphological analyser (kiwipiepy, Apache-2.0). Optional: the linter still runs without it."""
    global _KIWI
    if _KIWI is None:
        try:
            from kiwipiepy import Kiwi
            _KIWI = Kiwi()
        except Exception:  # not installed or model missing
            _KIWI = False
    return _KIWI or None


def sentence_ending(text):
    """Final ending morpheme of the last sentence (e.g. 'ᆸ니다', '세요', 'ᆯ까요'), or '명사형' when it ends without one."""
    analyser = kiwi()
    if not analyser or not text.strip():
        return None
    tokens = [t for t in analyser.tokenize(text.strip()) if t.tag not in ("SF", "SP", "SS", "SE", "SO", "SW")]
    if not tokens:
        return None
    endings = [t.form for t in tokens[-3:] if t.tag == "EF"]
    if not endings:
        return "명사형"
    # '-ㅂ니다/-습니다'처럼 받침에 따라 갈리는 같은 어미는 하나로 본다.
    return {"습니다": "ᆸ니다", "습니까": "ᆸ니까"}.get(endings[-1], endings[-1])


FREE_MARK = re.compile(r'<meta\s+name="ethos-design"\s+content="free"', re.IGNORECASE)


def is_free_design(html):
    """자유 디자인(B) 카드 HTML인지. Codex·Claude가 직접 디자인한 파일은 이 메타 태그를 단다."""
    return bool(FREE_MARK.search(html))


def _squash(text):
    import html as _html
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", text, flags=re.S)
    text = _html.unescape(re.sub(r"<[^>]+>", "", text))
    return re.sub(r"\s+", "", text)


def copy_lock(card, html):
    """승인된 card-data 문구가 자유 디자인 HTML에 글자 그대로 들어 있는지. 빠진 문구 목록을 돌려준다.
    레이아웃은 자유지만 문구·숫자·한정어는 card-data가 원본이다."""
    page = _squash(html)
    fields = [card.get("headline", ""), card.get("takeaway", ""), card.get("promise", "")]
    for item in card.get("body", []):
        fields += [item.get("key", ""), item.get("text", "")] if isinstance(item, dict) else [item]
    return [f for f in fields if f and _squash(f) not in page]


STYLE = RULES.get("style", {})


def _noun_plus_ha(left, right, analyser):
    """'제출 할'처럼 명사 뒤에 띄어 쓴 '하다'인지(붙여 써야 함). '해야 할'은 아니다."""
    try:
        lt, rt = analyser.tokenize(left), analyser.tokenize(right)
    except Exception:
        return False
    return bool(lt and rt) and lt[-1].tag.startswith("NN") and rt[0].form == "하" and rt[0].tag in ("XSV", "XSA", "VV")


DEPENDENT = re.compile(r"^(수|것|때|줄|만큼|뿐)(?:[가-힣]{0,3})[.,?!]?$")


def _spacing_pairs(old_words, new_words, analyser):
    """kiwi 제안 가운데 표준 맞춤법과 맞는 두 경우만 남긴다.
    1) 의존 명사 앞 띄우기: '받을수' → '받을 수'
    2) 명사 + '하다' 붙이기: '제출 할' → '제출할'
    kiwi는 '해야 할' → '해야할'처럼 표준과 다른 붙임도 제안하므로 나머지는 버린다."""
    pairs = []
    for word in old_words:
        if not re.search("[가-힣]", word):
            continue
        for k in range(1, len(word)):
            head, tail = word[:k], word[k:]
            last = head[-1]
            # 관형형 어미(받침 ㄴ·ㄹ) 뒤에 붙은 의존 명사만: '받을수', '하는것'
            if "가" <= last <= "힣" and (ord(last) - 0xAC00) % 28 in (4, 8) and DEPENDENT.match(tail):
                if f"{head} {tail}" in " ".join(new_words):
                    pairs.append((word, f"{head} {tail}"))
                    break
    for a, b in zip(old_words, old_words[1:]):
        if a + b in new_words and _noun_plus_ha(a, b, analyser):
            pairs.append((f"{a} {b}", a + b))
    return pairs


def spacing_suggestions(text, limit=8):
    """kiwipiepy space()로 띄어쓰기 교정 후보를 찾는다(오프라인, LLM 아님).

    합성 명사를 띄우는 제안('영업정지' → '영업 정지')은 붙여 써도 맞으므로 버리고,
    의존 명사·보조 용언·'하다' 붙임처럼 실제로 틀리기 쉬운 곳만 돌려준다.
    반환: [(원래 어절, 고친 어절)].
    """
    analyser = kiwi()
    if not analyser:
        return []
    found = []
    for line in text.splitlines():
        line = line.strip()
        if not re.search("[가-힣]", line) or line.startswith(("|", "```", "<")):
            continue
        try:
            fixed = analyser.space(line)
        except Exception:
            continue
        if fixed == line:
            continue
        before, after = line.split(), fixed.split()
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=before, b=after, autojunk=False).get_opcodes():
            if op == "equal":
                continue
            old, new = " ".join(before[i1:i2]), " ".join(after[j1:j2])
            if old.replace(" ", "") != new.replace(" ", ""):
                continue  # 글자가 바뀐 제안은 무시(띄어쓰기만 본다)
            pairs = _spacing_pairs(before[i1:i2], after[j1:j2], analyser)
            found.extend(pairs)
            if len(found) >= limit:
                return found
    return found


def split_sentences(text):
    # Korean prose can contain soft line breaks and unpunctuated sentence endings.
    # Keep the lightweight fallback for environments without the optional model.
    analyser = kiwi() if re.search('[가-힣]', text) else None
    if analyser:
        try:
            return [s.text.strip() for s in analyser.split_into_sents(text) if s.text.strip()]
        except Exception:
            pass
    parts = re.split(r"(?<=[.!?。])\s+|\n+", text)
    return [p.strip() for p in parts if len(p.strip()) > 1]


def style_ko(text, report, where, repeat):
    """반복 접속어·상투 표현·번역투·부정 결론 연속. 모두 info: 윤문할 곳을 알려 줄 뿐 막지 않는다."""
    rules = STYLE.get("ko")
    if not rules or not text.strip():
        return
    sentences = split_sentences(text)
    for pattern, rule, message in (
        (r'먼저[^.!?\n]{1,80}먼저입니다', 'redundant-priority', '같은 문장에서 먼저를 중복해 쓰고 있습니다.'),
        (r'이것도 맞고 저것도 맞|둘 다 맞는 말|양쪽 모두 일리가|어느 쪽이 맞다고 할 수 없',
         'false-balance', '근거 없이 양쪽을 동등하게 놓아 결론을 흐리는지 확인하세요.'),
        (r'[”"]\s*\n\s*(?:는|라는|라고)\s', 'broken-quote-line', '인용문과 뒤의 조사가 줄바꿈으로 떨어져 있습니다.'),
    ):
        if re.search(pattern, text):
            report.add('info', rule, where, message,
                       '확인된 결론부터 쓰고, 결론을 바꾸는 조건만 뒤에 설명하세요. 인용·법률상 한정은 보존합니다.')
    starts = collections.Counter()
    for sentence in sentences:
        for word in rules["connectors"]:
            if re.match(re.escape(word) + r"(?:[ ,]|$)", sentence):
                starts[word] += 1
    for word, n in starts.most_common():
        if n >= repeat:
            report.add("info", "repeated-connector", where, f"문장 첫머리에 '{word}' {n}번.",
                       "절반쯤은 접속어 없이 이어 쓰거나 앞 문장과 합치세요.")
    for group, rule, fix in (("stockPhrases", "stock-phrase", "구체적인 내용으로 바로 말하세요(예: '중요한 것은 X입니다' → 'X부터 보세요')."),
                             ("translationese", "translationese", "우리말 어순으로 풀어 쓰세요(예: '~를 통해' → '~로', '~에 있어서' → '~에서')."),):
        for phrase in rules[group]:
            n = text.count(phrase)
            if n >= repeat:
                report.add("info", rule, where, f"'{phrase}' {n}번.", fix)
    negative = re.compile(RULES["negation"]["ko"])
    flags = [bool(negative.search(s)) or s.rstrip(".").endswith("안 됩니다") for s in sentences]
    if sentences:
        ratio = sum(flags) / len(flags)
        report.metrics[f"{where}.negative_sentence_ratio"] = round(ratio, 2)
        if ratio > rules["maxNegativeSentenceRatio"]:
            report.add("info", "negative-heavy", where, f"부정으로 끝나는 문장이 {ratio:.0%}입니다.",
                       "결론 자리의 '~아닙니다/~안 됩니다'를 독자가 할 일이나 기준으로 바꾸세요(예: '서버 위치로 판단해서는 안 됩니다' → '먼저 볼 것은 누가 제공하느냐입니다').")
    run = best = 0
    for flag in flags:
        run = run + 1 if flag else 0
        best = max(best, run)
    if best >= rules["maxNegativeSentenceRun"]:
        report.add("info", "negative-run", where, f"부정문이 {best}문장 연속 이어집니다.", "가운데 한 문장을 긍정 기준으로 바꾸세요.")
    spacing = spacing_suggestions(text)
    if spacing:
        report.metrics[f"{where}.spacing_suggestions"] = len(spacing)
        sample = ", ".join(f"'{a}'→'{b}'" for a, b in spacing[:5])
        report.add("info", "spacing", where, f"띄어쓰기 교정 후보 {len(spacing)}곳: {sample}",
                   "형태소 분석기(kiwipiepy) 제안입니다. 맞는 것만 고치세요.")


def syllables(word):
    """영어 음절 수 근사(모음 묶음). 사전 다운로드 없이 오프라인으로 동작한다."""
    word = word.lower().strip(".,;:!?()\"'")
    if not word:
        return 0
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups) - (1 if word.endswith("e") and len(groups) > 1 and not word.endswith("le") else 0)
    return max(1, count)


def flesch_ease(text):
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    if not words:
        return 100.0
    sentences = max(1, len(split_sentences(text)))
    return 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (sum(map(syllables, words)) / len(words))


def fixed_terms_en(texts, report, where):
    """고정 번역어 검사: 행정사·에토스 사무소를 가리키는 다른 번역어만 잡는다.
    다른 나라의 agent·office 같은 일반 표현은 뜻이 다르므로 잡지 않는다."""
    for fixed, banned in STYLE.get("en", {}).get("fixedTerms", {}).items():
        for label, text in texts:
            for word in banned:
                if re.search(r"\b" + re.escape(word) + r"s?\b", text, re.IGNORECASE):
                    report.add("warn", "fixed-term", f"{where} {label}", f"'{word}' 대신 고정 번역어 '{fixed}'를 쓰세요.",
                               "docs/en-legal-glossary.md의 고정 번역어를 따릅니다.")


def style_en(texts, report, where):
    """영문 가독성(Flesch 근사, 오프라인)과 상투·군더더기(proselint, 선택 의존성). 결과는 모두 info다."""
    rules = STYLE.get("en")
    if not rules:
        return
    fixed_terms_en(texts, report, where)
    for label, text in texts:
        words = len(text.split())
        if words < 12:
            continue
        ease = flesch_ease(text)
        per = words / max(1, len(split_sentences(text)))
        if ease < rules["minFleschEase"] or per > rules["maxWordsPerSentence"]:
            report.add("info", "en-readability", f"{where} {label}",
                       f"읽기 쉬움 {ease:.0f}점(Flesch 근사), 문장당 {per:.0f}단어입니다.",
                       "한국 법령 용어를 직역한 명사 덩어리를 풀고 문장을 둘로 나누세요. 사실·한정어는 그대로 둡니다.")
    for label, text in texts:
        for line, check, message in vale_alerts(text.replace("\n", "\n\n"), limit=3):
            report.add("info", "en-vale", f"{where} {label}", f"{check}: {message}")
    try:
        from proselint.checks import __register__
        from proselint.registry import CheckRegistry
        from proselint.tools import LintFile
    except Exception:
        return
    registry = CheckRegistry()
    if not registry.checks:
        registry.register_many(__register__)
    seen = 0
    for label, text in texts:
        for result in LintFile(label, text).lint():
            if seen >= rules["proselintMax"]:
                return
            seen += 1
            item = result.check_result
            report.add("info", "en-style", f"{where} {label}", f"{item.check_path}: {item.message}")


def vale_alerts(text, limit=12):
    """Vale(MIT) 영문 문체 힌트. 설정은 저장소 루트 .vale-en.ini(수동태·한정어 지적은 끔).
    vale 실행 파일이나 패키지(vale sync)가 없으면 빈 목록을 돌려준다. 반환: [(줄, 규칙, 메시지)]."""
    import shutil
    import subprocess
    import tempfile
    exe = shutil.which("vale")
    config = ROOT / ".vale-en.ini"
    if not exe or not config.exists() or not (ROOT / ".vale" / "styles" / "Microsoft").exists() or not text.strip():
        return []
    with tempfile.TemporaryDirectory(prefix="ethos-vale-") as tmp:
        path = pathlib.Path(tmp) / "text.md"
        path.write_text(text, encoding="utf-8")
        try:
            result = subprocess.run([exe, f"--config={config}", "--output=JSON", str(path)],
                                    capture_output=True, text=True, encoding="utf-8", timeout=60)
            data = json.loads(result.stdout or "{}")
        except Exception:
            return []
    alerts = [(a.get("Line", 0), a.get("Check", ""), a.get("Message", "")) for items in data.values() for a in items]
    return sorted(alerts)[:limit]


STYLE_RULES = {"spacing", "en-vale", "legalese", "repeated-connector", "stock-phrase", "translationese", "negative-heavy", "negative-run", "en-readability", "en-style", "false-balance", "redundant-priority", "broken-quote-line", "question-headlines", "headline-monotony", "negative-framing", "cover-payoff", "uniform-endings", "ending-run"}


def style_cards(data, lang, report):
    """카드 세트의 윤문 힌트(info). copy_lint 단독 실행과 Render cards 워크플로가 같은 함수를 쓴다."""
    cards = data.get("cards", [])
    if lang == "ko":
        style_ko("\n".join(text for c in cards for _, text in card_fields(c)), report, "[ko] cards", STYLE.get("ko", {}).get("cardRepeat", 3))
        for c in cards:
            text = "\n".join(t for _, t in card_fields(c))
            hits = [w for w in STYLE.get("ko", {}).get("legalese", []) if w in text]
            if hits:
                report.add("info", "legalese", f"[ko] card {c['page']}", f"법률 문서 말투: {', '.join(hits)}",
                           "말로 한 초안부터 다시 써 보세요(docs/card-authoring-spec.md '두 번에 나눠 쓴다'). 원문 용어가 꼭 필요하면 그대로 둡니다.")
    elif lang == "en":
        style_en([(f"card {c['page']}", "\n".join(text for _, text in card_fields(c))) for c in cards], report, "[en]")


def take_style_of(card):
    """build_cards.take_style과 같은 기본값: cover·cta·comparison은 bar, 나머지는 close."""
    return card.get("takeStyle") or ("bar" if card.get("type") in ("cover", "cta", "comparison") else "close")


def item_text(item):
    return item.get("text", "") if isinstance(item, dict) else str(item)


def item_key(item):
    return item.get("key", "") if isinstance(item, dict) else ""


def card_fields(card):
    """Every visible string of a card, tagged by role."""
    out = [("headline", card.get("headline", ""))]
    if card.get("promise"):
        out.append(("promise", card["promise"]))
    for item in card.get("body", []):
        if item_key(item):
            out.append(("body", item_key(item)))
        out.append(("body", item_text(item)))
    if card.get("note"):
        out.append(("note", card["note"]))
    out.append(("takeaway", card.get("takeaway", "")))
    return [(role, text) for role, text in out if text]


def card_text(card):
    return " ".join(text for _, text in card_fields(card))


def compact(text):
    return len(re.sub(r"\s+", "", text or ""))


def headline_form(headline, lang):
    text = headline.strip()
    if text.endswith("?") or (lang == "ko" and re.search(r"(까요|나요|습니까)\??$", text)):
        return "question"
    if re.search(r"(가 아니라|이 아니라|보다|대신|말고)" if lang == "ko" else r"\b(not|instead of|rather than|more than|less than|vs\.?)\b|—", text):
        return "contrast"
    if re.search(RULES["payoff"][lang], text) or re.match(r"^\d", text):
        return "number"
    return "assertion"


class Report:
    def __init__(self):
        self.findings = []
        self.metrics = {}

    def add(self, level, rule, where, message, fix=""):
        self.findings.append({"level": level, "rule": rule, "where": where, "message": message, "fix": fix})


def lint_cards(data, lang, report, terms=None):
    cards = data.get("cards", [])
    tag = f"[{lang}]"
    if not cards:
        return
    forms = [(c["page"], headline_form(c.get("headline", ""), lang)) for c in cards]
    counts = collections.Counter(form for _, form in forms)
    q_pages = [p for p, f in forms if f == "question"]
    q_ratio = len(q_pages) / len(cards)
    report.metrics[f"{lang}.question_headline_ratio"] = round(q_ratio, 2)
    report.metrics[f"{lang}.headline_forms"] = dict(counts)
    if q_ratio > RULES["headline"]["maxQuestionRatio"]:
        report.add("info", "question-headlines", f"{tag} cards {q_pages}",
                   f"질문형 헤드라인이 {len(q_pages)}/{len(cards)}장({q_ratio:.0%})입니다. 같은 틀이 반복되면 훅이 아니라 템플릿으로 읽힙니다.",
                   "질문이 실제 독자 질문이면 유지하세요. 비율을 맞추려고 문장을 바꾸지 않습니다.")
    top_form, top_n = counts.most_common(1)[0]
    if top_n / len(cards) > RULES["headline"]["maxSingleFormShare"] and top_form != "question":
        report.add("info", "headline-monotony", tag, f"{top_form} 형태가 {top_n}/{len(cards)}장입니다.", "소리 내어 읽고 반복감이 있는 곳만 고치세요. 확인된 사실은 단정형을 유지합니다.")

    neg_re = re.compile(RULES["negation"][lang], re.IGNORECASE)

    def negative(text):
        """A claim that ends by denying something. Questions and mid-sentence facts do not count."""
        text = text.strip()
        if not text or text.endswith("?"):
            return False
        return bool(neg_re.search(re.split(r"(?<=[.!?])\s+", text)[-1]))

    neg_pages = [c["page"] for c in cards if negative(c.get("takeaway", "")) or negative(c.get("headline", ""))]
    neg_ratio = len(neg_pages) / len(cards)
    report.metrics[f"{lang}.negative_card_ratio"] = round(neg_ratio, 2)
    if neg_ratio > RULES["takeaway"]["maxNegativeCardRatio"]:
        report.add("info", "negative-framing", f"{tag} cards {neg_pages}",
                   f"제목·결론이 부정문인 카드가 {len(neg_pages)}/{len(cards)}장입니다. 독자는 계속 정정당하는 느낌을 받습니다.",
                   "독자가 쓸 기준을 보강하되, 사실에 맞는 부정 결론은 유지하세요. 억지로 양쪽을 긍정하지 않습니다.")

    takeaways = [c["takeaway"] for c in cards if c.get("takeaway")]
    if lang == "ko" and takeaways:
        formal = sum(1 for t in takeaways if re.search(r"니다\.?$", t.strip())) / len(takeaways)
        report.metrics["ko.formal_ending_ratio"] = round(formal, 2)
        if formal > RULES["takeaway"]["maxFormalEndingRatio"]:
            report.add("info", "uniform-endings", tag, f"결론 문장의 {formal:.0%}가 '~니다'로 끝납니다.",
                       "문장 길이와 반복 동사를 먼저 점검하세요. 어미 비율 때문에 단정·의무·재량을 바꾸지 않습니다.")

    if lang == "ko" and kiwi():
        endings = [(c["page"], sentence_ending(c.get("takeaway", ""))) for c in cards if c.get("takeaway")]
        endings = [(p, e) for p, e in endings if e]
        report.metrics["ko.takeaway_endings"] = dict(collections.Counter(e for _, e in endings))
        run, best, previous = [], [], None
        for page, ending in endings:
            run = run + [page] if ending == previous else [page]
            previous = ending
            if len(run) > len(best):
                best = list(run)
        if len(best) >= RULES["takeaway"].get("maxSameEndingRun", 3):
            report.add("info", "ending-run", f"[ko] cards {best}", f"결론 문장이 {len(best)}장 연속 같은 어미로 끝납니다(형태소 분석).",
                       "반복 동사와 문장 길이를 먼저 다듬으세요. 격식체와 법률상 한정은 유지합니다.")

    if lang == "ko":
        memo = [c["page"] for c in cards if re.search(r"[가-힣]+(?:·[가-힣 ]+){2,}", card_text(c))]
        if memo:
            report.add("info", "memo-style", f"{tag} cards {memo}", "가운뎃점으로 셋 이상 나열한 메모체 문장이 있습니다(예: '과실·시정 노력·동기와 결과 등').",
                       "카드는 말하듯 읽혀야 합니다. 두 개까지만 묶고 나머지는 문장으로 풀거나 항목을 나누세요.")

    bars = [c["page"] for c in cards if c.get("takeaway") and take_style_of(c) == "bar"]
    if len(cards) >= 6 and len(bars) / len(cards) > 0.4:
        report.add("info", "take-bar-share", tag, f"결론 띠(bar)가 {len(bars)}/{len(cards)}장입니다. HTML 계약 권장은 40% 이하입니다.",
                   "결론이 가벼운 카드는 takeStyle을 'close'(구분선 한 줄)로 바꿔 리듬을 만드세요.")

    stat_re = re.compile(RULES["statuteRef"][lang])
    over = []
    for card in cards:
        text = card_text(card) if card["type"] != "quote" else " ".join(t for r, t in card_fields(card) if r != "body" or not re.search(r"\d{4}도\d+", t))
        n = len(stat_re.findall(text))
        if n > RULES["statute"]["maxPerCard"] or (card["type"] == "cover" and n and not RULES["statute"]["coverAllowed"]):
            over.append((card["page"], n))
    report.metrics[f"{lang}.statute_heavy_cards"] = len(over)
    for page, n in over:
        report.add("warn", "statute-density", f"{tag} card {page}", f"조문 번호가 {n}개 있습니다. 모바일 카드에서는 해독하기 어렵습니다.",
                   "카드에는 '무엇이 어떻게 되는지'를 쓰고 조문 번호는 캡션이나 각주로 내리세요.")

    cover = next((c for c in cards if c["type"] == "cover"), None)
    if cover and RULES["cover"]["requirePayoff"]:
        # An explicit payoff need not be a numbered list. Whether it is useful
        # is an editorial judgement, not something a numeral regex can prove.
        promise = cover.get("promise", "").strip()
        has = bool(promise and not any(p.lower() in promise.lower() for p in RULES["placeholders"]))
        has = has or bool(re.search(RULES["payoff"][lang], card_text(cover), re.IGNORECASE))
        report.metrics[f"{lang}.cover_has_payoff"] = has
        if not has:
            report.add("info", "cover-payoff", f"{tag} card {cover['page']}", "표지에서 독자가 얻을 답이 명시됐는지 확인하세요.",
                       "cover.promise에 '내게 필요한 출시 절차를 구분합니다'처럼 구체적인 답을 쓰세요. 숫자는 필수가 아닙니다.")

    if terms:
        seen = set()
        for card in cards:
            fields = [text for _, text in card_fields(card)]
            for text in fields:
                for term in terms.get(lang, []):
                    if term in seen or term.lower() not in text.lower():
                        continue
                    seen.add(term)
                    # 풀이는 같은 카드의 어느 필드에 있어도 된다(제목에 용어, 본문에 풀이).
                    glossed = any(re.search(re.escape(term) + r".{0,40}?(?: — |:|\(|이란|means|is a|refers to)", other, re.IGNORECASE) for other in fields)
                    if not glossed:
                        report.add("warn", "unglossed-term", f"{tag} card {card['page']}",
                                   f"전문용어 '{term}'가 처음 등장하는데 풀이(— · : · 괄호)가 붙어 있지 않습니다.", "첫 등장에 한 줄 풀이를 붙이세요.")

    pattern = re.compile("|".join(re.escape(p) for p in RULES["placeholders"]), re.IGNORECASE)
    for card in cards:
        hit = pattern.search(card_text(card))
        if hit:
            report.add("warn", "placeholder", f"{tag} card {card['page']}", f"자리표시자 '{hit.group(0)}'가 남아 있습니다.", "삭제하거나 실제 값으로 바꾸세요.")


def limit_key(card):
    kind, body = card["type"], card.get("body", [])
    count = len(body)
    if kind == "concept":
        return "concept4" if count == 4 else "concept"
    if kind == "comparison":
        return "comparison3" if count == 3 else "comparison2"
    if kind == "checklist":
        if card.get("layout") == "questions":
            return "questions"
        keyed = card.get("layout") in ("stats", "thresholds") or any(isinstance(x, dict) and x.get("key") for x in body)
        return "stats" if keyed else "numbered"
    if kind == "cta":
        return "cta2" if count == 2 else "cta6"
    return kind if kind in LIMITS["types"] else None


def lint_limits(data, lang, report):
    """Per-field length and item-count limits from card-limits.json (verified by scripts/spec_stress.py)."""
    tag = f"[{lang}]"
    H, TK, T = LIMITS["headline"], LIMITS["takeaway"], LIMITS["types"]
    for card in data.get("cards", []):
        page, kind = card["page"], card["type"]

        def over(field, text, limit):
            if text and len(text) > limit:
                # 한도는 가장 빽빽한 글자로 잰 보수적 값이다. 1.5배를 넘을 때만 경고하고, 그 안쪽은 렌더 QA 가 최종 판정한다.
                level = "warn" if len(text) > limit * 1.5 else "info"
                report.add(level, "over-limit", f"{tag} card {page} {field}", f"{len(text)}자 > 한도 {limit}자: {text[:24]}…",
                           "렌더 QA에서 오버플로·빈 공간이 나오면 문장을 줄이거나 카드를 나누세요(card-limits.json).")

        panel = kind == "cover" and card.get("coverStyle") in ("panel", "stat")
        over("headline", card.get("headline", ""), LIMITS["coverPanel"]["headline"][lang] if panel else H[("cover" + lang.capitalize()) if kind == "cover" else lang])
        over("takeaway", card.get("takeaway", ""), TK[lang])
        key = limit_key(card)
        spec = T.get(key) if key else None
        if not spec:
            continue
        body = card.get("body", [])
        low, high = spec["items"]
        if not low <= len(body) <= high:
            report.add("warn", "item-count", f"{tag} card {page}", f"{kind} 항목이 {len(body)}개입니다. 허용 범위는 {low}~{high}개입니다.", "항목 수를 맞추세요.")
        if key == "quote":
            for i, (item, slot) in enumerate(zip(body, spec["slots"])):
                over(f"body[{i}]", item_text(item), slot[lang])
            continue
        if panel:
            over("body[0]", item_text(body[0]) if body else "", LIMITS["coverPanel"]["text"][lang])
        for i, item in enumerate(body):
            if isinstance(item, dict):
                over(f"body[{i}].key", item.get("key", ""), spec.get("key", {}).get(lang, 10**6))
                over(f"body[{i}].text", item.get("text", ""), spec.get("text", {}).get(lang, 10**6))
            else:
                label, copy = (re.split(r"\s—\s|:\s", item, maxsplit=1) + [""])[:2] if re.search(r"\s—\s|:\s", item) else ("", item)
                if label:
                    over(f"body[{i}].key", label, spec.get("key", {}).get(lang, 10**6))
                    over(f"body[{i}].text", copy, spec.get("text", {}).get(lang, 10**6))
                else:
                    over(f"body[{i}]", item, spec.get("text", {}).get(lang, 10**6))
        if kind == "cover":
            over("promise", card.get("promise", ""), spec["promise"][lang])
            hero = card.get("hero") or {}
            over("hero.value", hero.get("value", ""), spec["hero"]["value"][lang])
            over("hero.label", hero.get("label", ""), spec["hero"]["label"][lang])
        if kind == "flow":
            over("note", card.get("note", ""), spec["note"][lang])
        if kind == "table":
            for cell in card.get("head", []):
                over("head", cell, spec["head"][lang])


def used_icons(data):
    names = set()
    for card in data.get("cards", []):
        if card.get("icon"):
            names.add(card["icon"])
        names.update(card.get("art", []))
        names.update(item["icon"] for item in card.get("body", []) if isinstance(item, dict) and item.get("icon"))
    return names


def lint_assets(folder, loaded, report):
    """Every icon drawn on a card must have a provenance row in assets.md (docs/asset-policy.md)."""
    names = set().union(*(used_icons(d) for d in loaded.values())) if loaded else set()
    assets = set()
    for html in list(folder.glob("ko/card_*.html")) + list(folder.glob("en/card_*.html")):
        page = html.read_text(encoding="utf-8")
        names.update(re.findall(r'data-icon="([a-z0-9-]+)"', page))  # 자유 디자인 카드
        assets.update(re.findall(r'data-asset="([a-z0-9-]+/[a-z0-9-]+)"', page))  # 인물(open-peeps)·물건(phosphor) 일러스트
    if not names and not assets:
        return
    path = folder / "assets.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    for asset in sorted(a for a in assets if a not in text):
        report.add("warn", "asset-unrecorded", "assets.md", f"카드에 쓴 일러스트 '{asset}'의 출처 기록이 없습니다.", "assets.md 표에 한 줄 추가하고 EXTERNAL ASSETS: Yes로 두세요.")
    missing = sorted(n for n in names if f"lucide/{n}.svg" not in text)
    report.metrics["icons.used"] = len(names)
    for name in missing:
        report.add("warn", "icon-unrecorded", "assets.md", f"카드에 쓴 아이콘 '{name}'의 출처 기록이 없습니다.", "assets.md 표에 한 줄 추가하고 EXTERNAL ASSETS: Yes로 두세요.")


def lint_polarity(ko, en, report):
    """Catch question headlines whose yes/no direction flips between languages."""
    for kc, ec in zip(ko.get("cards", []), en.get("cards", [])):
        kh, eh = kc.get("headline", ""), ec.get("headline", "")
        ko_neg = re.search(r"없어도|않아도|안 해도|필요 없", kh)
        en_pos = re.search(r"\b(need|must|require|requires)\b", eh, re.IGNORECASE) and not re.search(r"\b(without|no |not need|need not)\b", eh, re.IGNORECASE)
        if ko_neg and en_pos and kh.strip().endswith("?"):
            report.add("warn", "bilingual-polarity", f"card {kc['page']}", f"국문은 '없어도 되나'를 묻고 영문은 '필요한가'를 묻습니다: {kh} / {eh}",
                       "질문의 방향을 일치시키거나 의도적으로 바꿨다면 compressionNote에 기록하세요.")


def lint_distribution(folder, lang_blocks, report, brief_text=""):
    if not lang_blocks:
        return
    wants_save = bool(re.search(r"PRIMARY OBJECTIVE:\s*저장", brief_text))
    for lang, caption in lang_blocks.items():
        placeholder = re.search("|".join(re.escape(p) for p in RULES["placeholders"]), caption, re.IGNORECASE)
        if placeholder:
            report.add("warn", "placeholder", f"[{lang}] caption", f"캡션에 '{placeholder.group(0)}'가 남아 있습니다.")
        if wants_save and not re.search(RULES["saveCue"][lang], caption, re.IGNORECASE):
            report.add("info", "no-save-cue", f"[{lang}] caption", "주 목표가 '저장'인데 캡션에 저장할 이유를 알려 주는 문장이 없습니다.",
                       "'출시 점검할 때 다시 보세요'처럼 한 줄을 넣으세요. CTA는 하나만 유지합니다.")
        if lang == "en":
            fixed_terms_en([("caption", caption)], report, "[en]")
        elif lang == "ko":
            style_ko(caption, report, '[ko] caption', STYLE.get('ko', {}).get('cardRepeat', 3))


def parse_captions(path):
    text = path.read_text(encoding="utf-8")
    blocks = {}
    for lang, heading in (("ko", "## Korean"), ("en", "## English")):
        if heading in text:
            part = text.split(heading, 1)[1]
            part = re.split(r"\n## ", part)[0]
            match = re.search(r"### Caption\s+(.*?)(?:\n### |\Z)", part, re.DOTALL)
            if match:
                blocks[lang] = match.group(1).strip()
    return blocks


def lint_blog(path, report):
    text = path.read_text(encoding="utf-8")
    pattern = re.compile("|".join(re.escape(p) for p in RULES["placeholders"]), re.IGNORECASE)
    lines = text.splitlines()
    hits = [i + 1 for i, line in enumerate(lines) if pattern.search(line)]
    report.metrics["blog.placeholders"] = len(hits)
    if hits:
        report.add("warn", "placeholder", "blog", f"자리표시자가 {len(hits)}곳({', '.join(map(str, hits[:8]))}행…)에 남아 있습니다.", "발행 전에 모두 출처로 바꾸거나 삭제하세요.")
    orphans = [i + 1 for i, line in enumerate(lines) if re.match(r"^[가-힣]에서 ", line.strip()) and i > 0 and len(lines[i - 1].strip()) < 60]
    for n in orphans[:3]:
        report.add("info", "suspect-fragment", f"blog line {n}", f"문장이 조사부터 시작합니다(앞 글자가 빠졌을 수 있음): {lines[n - 1].strip()[:30]}")
    tracked = [i + 1 for i, line in enumerate(lines) if re.search(r"[?&](?:utm_[\w.-]+|oc)=", line, re.IGNORECASE)]
    if tracked:
        report.add("warn", "tracking-link", "blog", f"추적값(utm_…)이나 API 키(OC=)가 붙은 링크가 {len(tracked)}곳({', '.join(map(str, tracked[:5]))}행)에 있습니다.",
                   "링크를 빼고 '국가법령정보센터, 사건번호·의결일'처럼 출처 이름만 쓰세요.")
    bold = [i + 1 for i, line in enumerate(lines) if "**" in line]
    if bold:
        report.add("warn", "markdown-bold", "blog", f"'**' 굵게 표시가 {len(bold)}곳({', '.join(map(str, bold[:5]))}행)에 남아 있습니다.",
                   "네이버·홈페이지에 붙이면 별표가 그대로 보입니다. 지우고 필요하면 편집기에서 굵게 하세요.")
    style_ko(text, report, "blog", STYLE.get("ko", {}).get("blogRepeat", 5))


def protected_tokens(data):
    """Fact-bearing tokens (statutes, case numbers, amounts, dates). Earlier patterns win; overlapping matches are dropped."""
    patterns = [RULES["statuteRef"]["ko"], RULES["statuteRef"]["en"], r"\d{4}(?:도|Do)\d+"]
    patterns += GATES["content"]["factLock"]["patterns"]
    patterns += [r"「[^」]+」", r"\d{4}년\s*\d{1,2}월\s*\d{1,2}일", r"KRW\s?[\d.,]+\s?(?:tn|trillion|million|billion)?", r"\d[\d,]{3,}"]
    tokens = collections.Counter()
    for card in data.get("cards", []):
        text = card_text(card)
        taken = []
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                if any(match.start() < end and start < match.end() for start, end in taken):
                    continue
                taken.append((match.start(), match.end()))
                tokens[re.sub(r"\s+", "", match.group(0))] += 1
    return tokens


# 법률 문장의 한정어. 윤문 전후로 하나라도 줄면 의미가 넓어지거나 좁아질 수 있다.
HEDGES = ("수 있", "해야", "않으면", "아니면", "또는", "그리고", "이하", "이상", "초과", "미만", "원칙적으로", "일정", "경우")


def hedge_counts(data):
    text = " ".join(card_text(card) for card in data.get("cards", []))
    return collections.Counter({h: text.count(h) for h in HEDGES if text.count(h)})


def compare(old, new, report, moved_to=""):
    """Diff fact tokens between two card-data files. Tokens that left the cards but live in `moved_to` (e.g. the caption) are info only."""
    a, b = protected_tokens(old), protected_tokens(new)
    removed = sorted((a - b).elements())
    added = sorted((b - a).elements())
    moved_flat = re.sub(r"\s+", "", moved_to)
    report.metrics["protected.removed"] = removed
    report.metrics["protected.added"] = added
    for token in sorted(set(removed)):
        left = removed.count(token)
        if token and token in moved_flat:
            report.add("info", "protected-moved", "compare", f"카드에서 빠졌지만 캡션에 남아 있습니다: {token} ×{left}")
        else:
            report.add("warn", "protected-removed", "compare", f"기존에 있던 사실 토큰이 사라졌습니다: {token} ×{left}", "의도한 삭제인지, 다른 곳으로 옮겼는지 확인하세요.")
    for token in sorted(set(added)):
        report.add("warn", "protected-added", "compare", f"기존에 없던 사실 토큰이 생겼습니다: {token} ×{added.count(token)}", "원문·1차 자료에서 근거를 확인하세요.")
    lost = hedge_counts(old) - hedge_counts(new)
    report.metrics["hedges.lost"] = dict(lost)
    for hedge, n in sorted(lost.items()):
        report.add("warn", "hedge-removed", "compare", f"한정어 '{hedge}'가 {n}회 줄었습니다.", "윤문하면서 '~할 수 있다', '이하', '또는' 같은 조건이 빠지지 않았는지 확인하세요.")


def resolve(arg):
    path = pathlib.Path(arg)
    if path.is_dir():
        return path, {lang: path / f"card-data.{lang}.json" for lang in ("ko", "en") if (path / f"card-data.{lang}.json").exists()}
    match = re.search(r"card-data\.(\w+)\.json$", path.name)
    return path.parent, {(match.group(1) if match else "ko"): path}


def print_report(report, label):
    print(f"== copy_lint: {label}")
    for level in ("warn", "info"):
        for f in [x for x in report.findings if x["level"] == level]:
            print(f"{level.upper():4} {f['rule']:18} {f['where']}\n     {f['message']}" + (f"\n     → {f['fix']}" if f["fix"] else ""))
    warns = sum(1 for f in report.findings if f["level"] == "warn")
    infos = len(report.findings) - warns
    print(f"-- {warns} warn / {infos} info")
    return warns


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", help="content/<ID> directory or a card-data.<lang>.json")
    parser.add_argument("--blog", action="store_true", help="also lint blog.md in the folder")
    parser.add_argument("--compare", nargs=2, metavar=("OLD", "NEW"), help="protected-token diff of two card-data files")
    parser.add_argument("--strict", action="store_true", help="exit 1 when any warn exists")
    parser.add_argument("--json", help="write metrics and findings to this path")
    args = parser.parse_args()
    report = Report()

    if args.compare:
        old, new = (json.loads(pathlib.Path(p).read_text(encoding="utf-8")) for p in args.compare)
        dist = pathlib.Path(args.compare[1]).parent / "distribution.md"
        compare(old, new, report, dist.read_text(encoding="utf-8") if dist.exists() else "")
        label = " vs ".join(args.compare)
    else:
        if not args.target:
            parser.error("target is required unless --compare is used")
        folder, files = resolve(args.target)
        if not files and not (args.blog and (folder / 'blog.md').exists()):
            parser.error(f"no card-data found in {args.target}")
        terms_path = folder / "terms.json"
        terms = json.loads(terms_path.read_text(encoding="utf-8")) if terms_path.exists() else None
        loaded = {}
        for lang, path in files.items():
            loaded[lang] = json.loads(path.read_text(encoding="utf-8"))
            lint_cards(loaded[lang], lang, report, terms)
            lint_limits(loaded[lang], lang, report)
        for lang, data in loaded.items():
            style_cards(data, lang, report)
        if "ko" in loaded and "en" in loaded:
            lint_polarity(loaded["ko"], loaded["en"], report)
        lint_assets(folder, loaded, report)
        dist = folder / "distribution.md"
        if dist.exists():
            brief = folder / "brief.md"
            lint_distribution(folder, parse_captions(dist), report, brief.read_text(encoding="utf-8") if brief.exists() else "")
        if args.blog and (folder / "blog.md").exists():
            lint_blog(folder / "blog.md", report)
        label = str(args.target)

    warns = print_report(report, label)
    if args.json:
        pathlib.Path(args.json).write_text(json.dumps({"metrics": report.metrics, "findings": report.findings}, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1 if (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
