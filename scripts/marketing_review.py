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
        hook += 4
    else:
        notes.append(f"{lang}: 표지 헤드라인을 {limit}자 안팎에서 다시 검토")
    hook += 4 if marketing.get("targetReader") else 0
    hook += 4 if marketing.get("readerQuestion") else 0
    hook += 4 if marketing.get("coverIntent") else 0
    if not marketing.get("targetReader") or not marketing.get("readerQuestion"):
        notes.append(f"{lang}: 표지 기호보다 대상 독자와 해결할 질문을 먼저 명시")
    scores["hook"] = hook

    traced = sum(bool(card.get("sourceTrace", {}).get("heading")) for card in cards)
    evidenced = sum(bool(card.get("sourceTrace", {}).get("evidence")) for card in cards)
    trust = 5 if cards and traced == len(cards) else 3 if traced else 0
    trust += 4 if cards and evidenced == len(cards) else 2 if evidenced else 0
    trust += 3 if any(card.get("sourceTrace", {}).get("evidence") == "F" for card in cards) else 0
    trust += 3 if cards and all(card.get("sourceTrace") for card in cards) else 0
    all_text = " ".join(str(card) for card in cards)
    hype = ["무조건", "충격", "100%", "최고", "guaranteed", "must know"]
    if not contains_any(all_text, hype):
        trust += 3
    else:
        notes.append(f"{lang}: 과장 표현이 신뢰를 깎지 않는지 확인")
    if any(card.get("type") in ("process", "quote") for card in cards):
        trust += 2
    else:
        notes.append(f"{lang}: 실제 검토 순서나 공식 근거를 보여주는 Proof of Work 장면을 검토")
    scores["trust"] = min(trust, 20)

    types = [card.get("type") for card in cards]
    readability = 8 if cards and all(card.get("oneMessage") for card in cards) else 0
    readability += 4 if cards and all(card.get("headline") for card in cards) else 0
    readability += 4 if cards and all(len(card.get("body", [])) <= 6 for card in cards) else 0
    text_limit = 180 if lang == "ko" else 300
    longest = max((compact_len(card.get("headline", "") + "".join(card.get("body", [])) + card.get("takeaway", "")) for card in cards), default=0)
    if longest > text_limit:
        notes.append(f"{lang}: 가장 긴 카드 {longest}자 — 글자를 줄이기 전에 문장 구조와 중복 표현을 압축하고 축소 시트 확인")
    readability += 2 if len(set(types)) >= 3 else 0
    if len(set(types)) < 3:
        notes.append(f"{lang}: 카드 유형 반복이 의도적인지 축소 시트에서 확인")
    if data.get("canvasProfile") == "portrait" and data.get("visualFamily") == "social-native":
        readability += 2
    else:
        notes.append(f"{lang}: Instagram 발행이면 portrait + social-native 프로필 사용")
    scores["readability"] = min(readability, 20)

    utility = 6 if marketing.get("practicalPayoff") else 0
    utility += 4 if marketing.get("saveValue") else 0
    takeaway_count = sum(bool(card.get("takeaway")) for card in cards)
    utility += 4 if cards and takeaway_count >= max(1, len(cards) // 2) else 0
    utility += 2 if len(final.get("body", [])) >= 2 else 0
    early_payoff = any(card.get("oneMessage") and len(card.get("body", [])) >= 2 for card in cards[1:3])
    utility += 4 if early_payoff else 0
    if not early_payoff:
        notes.append(f"{lang}: 2~3장 안에 바로 써볼 판단 기준이나 확인 항목 배치")
    if not marketing.get("practicalPayoff"):
        notes.append(f"{lang}: 끝까지 읽으면 판단·준비할 수 있는 실용적 보상을 명시")
    scores["utility"] = min(utility, 20)

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
             "| 언어 | 훅 | 신뢰 | 가독성 | 실용성 | 전환 | 합계 |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for lang, total, scores, _ in reports:
        lines.append(f"| {lang} | {scores['hook']} | {scores['trust']} | {scores['readability']} | {scores['utility']} | {scores['conversion']} | {total} |")
    all_notes = [note for _, _, _, notes in reports for note in notes]
    lines += ["", "## 권고"] + ([f"- {note}" for note in all_notes] if all_notes else ["- 추가 권고 없음"])
    lines += ["", "## 사람이 확인할 것", "- 표지가 2초 안에 대상·문제·정보 보상 중 둘 이상을 전달하는가", "- 특정 카드 유형이 없어도 다시 볼 판단 기준이나 준비 정보가 있는가", "- CTA의 입력자료와 제공 결과가 실제 서비스 범위와 일치하는가", "- 점수를 올리느라 법률 요건이나 예외를 삭제하지 않았는가", "- 실제 저장·공유·무료 검토 요청 데이터가 자동 점수와 다르면 실제 데이터를 우선했는가", ""]
    out = pathlib.Path(args.out) if args.out else folder / "marketing-report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"marketing review: {average}/100 -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
