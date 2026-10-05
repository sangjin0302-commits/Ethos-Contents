#!/usr/bin/env python3
"""Copy-quality linter for ETHOS card-data, captions and blog drafts.

gates.json guards layout and fact integrity. This script guards what readers feel:
repeated headline shapes, stacked negations, statute numbers on a phone-sized card,
unexplained jargon, covers that make no promise, and leftover placeholders.
Findings are advisory (warn/info); --strict turns warnings into a failing exit code.
"""

import argparse
import collections
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
        report.add("warn", "question-headlines", f"{tag} cards {q_pages}",
                   f"질문형 헤드라인이 {len(q_pages)}/{len(cards)}장({q_ratio:.0%})입니다. 같은 틀이 반복되면 훅이 아니라 템플릿으로 읽힙니다.",
                   "표지와 한 장 정도만 질문으로 두고 나머지는 단정·대비·숫자형으로 바꾸세요.")
    top_form, top_n = counts.most_common(1)[0]
    if top_n / len(cards) > RULES["headline"]["maxSingleFormShare"] and top_form != "question":
        report.add("warn", "headline-monotony", tag, f"{top_form} 형태가 {top_n}/{len(cards)}장입니다.", "형태를 섞으세요.")

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
        report.add("warn", "negative-framing", f"{tag} cards {neg_pages}",
                   f"제목·결론이 부정문인 카드가 {len(neg_pages)}/{len(cards)}장입니다. 독자는 계속 정정당하는 느낌을 받습니다.",
                   "'~가 아닙니다'를 '~는 이렇게 나뉩니다'처럼 독자가 쓸 수 있는 기준으로 바꾸세요. 법률 한정어는 유지합니다.")

    takeaways = [c["takeaway"] for c in cards if c.get("takeaway")]
    if lang == "ko" and takeaways:
        formal = sum(1 for t in takeaways if re.search(r"니다\.?$", t.strip())) / len(takeaways)
        report.metrics["ko.formal_ending_ratio"] = round(formal, 2)
        if formal > RULES["takeaway"]["maxFormalEndingRatio"]:
            report.add("info", "uniform-endings", tag, f"결론 문장의 {formal:.0%}가 '~니다'로 끝납니다.",
                       "명사형 종결, 짧은 단답, 질문을 섞어 문장 리듬을 바꾸세요.")

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
                       "중간 한 장을 '~하세요', 명사형 종결, 짧은 단답으로 바꿔 리듬을 깨세요.")

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
        has = bool(re.search(RULES["payoff"][lang], card_text(cover), re.IGNORECASE))
        report.metrics[f"{lang}.cover_has_payoff"] = has
        if not has:
            report.add("warn", "cover-payoff", f"{tag} card {cover['page']}", "표지가 끝까지 보면 얻는 것(몇 가지·몇 단계·체크리스트)을 약속하지 않습니다.",
                       "cover.promise에 '출시 전 6가지 질문' 같은 한 줄을 넣으세요.")

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
    if not names:
        return
    path = folder / "assets.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
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
        if not files:
            parser.error(f"no card-data found in {args.target}")
        terms_path = folder / "terms.json"
        terms = json.loads(terms_path.read_text(encoding="utf-8")) if terms_path.exists() else None
        loaded = {}
        for lang, path in files.items():
            loaded[lang] = json.loads(path.read_text(encoding="utf-8"))
            lint_cards(loaded[lang], lang, report, terms)
            lint_limits(loaded[lang], lang, report)
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
