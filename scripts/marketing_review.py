#!/usr/bin/env python3
"""Advisory marketing review for a bilingual ETHOS carousel."""

import argparse
import json
import pathlib
import re


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def compact_len(value):
    return len(re.sub(r"\s+", "", value or ""))


def contains_any(text, values):
    folded = (text or "").casefold()
    return any(str(value).casefold() in folded for value in values if value)


def review(data):
    lang = data.get("language", "")
    cards = data.get("cards", [])
    cover = cards[0] if cards else {}
    final = cards[-1] if cards else {}
    marketing = data.get("marketing", {})
    notes, scores = [], {}

    hook = 4 if cover.get("headline") else 0
    limit = 42 if lang == "ko" else 80
    if compact_len(cover.get("headline")) <= limit:
        hook += 6
    else:
        notes.append(f"{lang}: 표지 헤드라인을 {limit}자 안팎에서 다시 검토")
    if any(mark in cover.get("headline", "") for mark in ("?", "？", ":", "—")):
        hook += 4
    else:
        notes.append(f"{lang}: 표지에 질문·대비·구체 상황 중 하나를 더 선명하게")
    hook += 3 if marketing.get("coverIntent") else 0
    hook += 3 if marketing.get("targetReader") else 0
    scores["hook"] = hook

    traced = sum(bool(card.get("sourceTrace", {}).get("heading")) for card in cards)
    trust = 8 if cards and traced == len(cards) else 4 if traced else 0
    trust += 4 if any(card.get("sourceTrace", {}).get("evidence") == "F" for card in cards) else 0
    trust += 4 if any(card.get("type") == "quote" for card in cards) else 0
    all_text = " ".join(str(card) for card in cards)
    hype = ["무조건", "충격", "100%", "최고", "guaranteed", "must know"]
    if not contains_any(all_text, hype):
        trust += 4
    else:
        notes.append(f"{lang}: 과장 표현이 신뢰를 깎지 않는지 확인")
    scores["trust"] = trust

    types = [card.get("type") for card in cards]
    readability = 5 if len(set(types)) >= 4 else 0
    readability += 5 if "checklist" in types and "process" in types else 0
    readability += 5 if all(len(card.get("body", [])) <= 6 for card in cards) else 0
    text_limit = 180 if lang == "ko" else 300
    longest = max((compact_len(card.get("headline", "") + "".join(card.get("body", [])) + card.get("takeaway", "")) for card in cards), default=0)
    if longest <= text_limit:
        readability += 5
    else:
        notes.append(f"{lang}: 가장 긴 카드 {longest}자 — 글자를 줄이기 전에 문장 구조와 중복 표현을 압축하고 축소 시트 확인")
    scores["readability"] = readability

    save = 6 if "checklist" in types else 0
    save += 6 if "process" in types else 0
    save += 4 if marketing.get("saveValue") else 0
    save += 4 if len(final.get("body", [])) >= 2 else 0
    scores["save"] = save

    conversion = 4 if final.get("type") == "cta" else 0
    inputs = marketing.get("ctaInputs", [])
    outcomes = marketing.get("ctaOutcomes", [])
    conversion += 5 if len(inputs) >= 2 else 0
    conversion += 5 if outcomes else 0
    cta_text = " ".join(final.get("body", []) + [final.get("takeaway", "")])
    if contains_any(cta_text, inputs) and contains_any(cta_text, outcomes):
        conversion += 6
    else:
        notes.append(f"{lang}: 마지막 CTA에 실제로 받을 자료와 확인 결과를 한 번씩 명시")
    scores["conversion"] = conversion
    return scores, notes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("content_dir", help="content/<ID> directory")
    parser.add_argument("--out", help="default: content/<ID>/marketing-report.md")
    args = parser.parse_args()
    folder = pathlib.Path(args.content_dir)
    reports = []
    for lang in ("ko", "en"):
        path = folder / f"card-data.{lang}.json"
        if not path.exists():
            raise SystemExit(f"missing: {path}")
        scores, notes = review(load(path))
        reports.append((lang, sum(scores.values()), scores, notes))

    average = round(sum(item[1] for item in reports) / len(reports))
    lines = ["# Marketing Review", "", f"종합 권고 점수: **{average}/100**", "",
             "> 발행을 막지 않는 편집 보조 지표다. 실제 성과 데이터로 조정한다.", "",
             "| 언어 | 훅 | 신뢰 | 가독성 | 저장가치 | 전환 | 합계 |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for lang, total, scores, _ in reports:
        lines.append(f"| {lang} | {scores['hook']} | {scores['trust']} | {scores['readability']} | {scores['save']} | {scores['conversion']} | {total} |")
    all_notes = [note for _, _, _, notes in reports for note in notes]
    lines += ["", "## 권고"] + ([f"- {note}" for note in all_notes] if all_notes else ["- 추가 권고 없음"])
    lines += ["", "## 사람이 확인할 것", "- 표지가 2초 안에 대상과 문제를 전달하는가", "- 체크리스트·프로세스가 실제로 저장할 가치가 있는가", "- CTA의 입력자료와 제공 결과가 실제 서비스 범위와 일치하는가", "- 점수를 올리느라 법률 요건이나 예외를 삭제하지 않았는가", ""]
    out = pathlib.Path(args.out) if args.out else folder / "marketing-report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"marketing review: {average}/100 -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
