#!/usr/bin/env python3
"""Render worst-case-within-limits cards for every component and run the real QA gates.

card-limits.json is the contract given to the copywriter (docs/card-authoring-spec.md).
If a limit lets an overflowing card through, this script fails, so the contract stays honest.
"""

import json
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_cards import build  # noqa: E402

LIMITS = json.loads((ROOT / "card-limits.json").read_text(encoding="utf-8"))
WORK = ROOT / "content" / ".spec-stress"
T = LIMITS["types"]

WORDS = {
    "ko": ["서비스", "구조를", "먼저", "정하고", "절차의", "주체를", "확인해야", "합니다", "게임의", "유통과"],
    "en": ["service", "structure", "decides", "which", "duties", "apply", "before", "launch", "partners", "review"],
}


def fill(n, lang):
    """Space-separated filler of exactly n characters, so the layout sees realistic line breaks."""
    out, i = "", 0
    while len(out) < n:
        out += ("" if not out else " ") + WORDS[lang][i % len(WORDS[lang])]
        i += 1
    out = out[:n].rstrip()
    return out + ("가" if lang == "ko" else "a") * (n - len(out))


def token(n, lang):
    """One unbroken word of exactly n characters: the worst case for fixed-width key columns (keep-all never wraps it)."""
    return "가" * n if lang == "ko" else ("Occupation" * 4)[:n]


def card(page, kind, bg, lang, body, headline=None, **extra):
    h = LIMITS["headline"]
    if headline is None:
        panel = kind == "cover" and extra.get("coverStyle") in ("panel", "stat")
        headline = fill(LIMITS["coverPanel"]["headline"][lang] if panel else h[("cover" + lang.capitalize()) if kind == "cover" else lang], lang)
    data = {"page": page, "type": kind, "bg": bg, "oneMessage": "m", "headline": headline, "body": body,
            "takeaway": fill(LIMITS["takeaway"][lang], lang), "sourceTrace": {"heading": "h", "evidence": "S"}}
    data.update(extra)
    return data


def items(spec, lang, count, keyed=True):
    return [({"key": token(spec["key"][lang], lang), "text": fill(spec["text"][lang], lang)} if keyed
             else fill(spec["text"][lang], lang)) for _ in range(count)]


def bar_items(spec, lang, count):
    """Rows for layout:bars: the longest label, text and display allowed, with values that span the full bar range."""

    return [{"key": token(spec["key"][lang], lang), "text": fill(spec["text"][lang], lang), "value": 6 - i * 2 if i < 3 else 1,
             "display": "6" * spec["display"][lang]} for i in range(count)]


def with_icon(rows):
    return [dict(row, icon="check") for row in rows]


def sets(lang):
    max_limits = [
        card(1, "cover", "navy", lang, [fill(T["cover"]["text"][lang], lang)], promise=fill(T["cover"]["promise"][lang], lang), art=["server", "landmark", "globe"]),
        card(2, "quote", "cream", lang, [fill(slot[lang], lang) for slot in T["quote"]["slots"]], icon="scale"),
        card(3, "concept", "navy", lang, items(T["concept4"], lang, 4), icon="layers"),
        card(4, "flow", "cream", lang, with_icon(items(T["flow"], lang, T["flow"]["items"][1])), note=fill(T["flow"]["note"][lang], lang), icon="route"),
        card(5, "comparison", "navy", lang, items(T["comparison2"], lang, 2)),
        card(6, "checklist", "cream", lang, with_icon(items(T["stats"], lang, 3)), layout="stats", icon="badge-check"),
        card(7, "table", "navy", lang, items(T["table"], lang, T["table"]["items"][1]), head=[fill(T["table"]["head"][lang], lang)] * 2, icon="list-checks"),
        card(8, "process", "cream", lang, items(T["process"], lang, 4, keyed=False)),
        card(9, "checklist", "navy", lang, items(T["questions"], lang, 3, keyed=False), layout="questions"),
        card(10, "cta", "cream", lang, items(T["cta2"], lang, 2)),
    ]
    variants = [
        card(1, "cover", "cream", lang, [fill(T["cover"]["text"][lang], lang)]),
        card(2, "concept", "navy", lang, items(T["concept"], lang, 3)),
        card(3, "comparison", "cream", lang, items(T["comparison3"], lang, 3)),
        card(4, "flow", "navy", lang, items(T["flow"], lang, 3), note=fill(T["flow"]["note"][lang], lang)),
        card(5, "checklist", "cream", lang, items(T["numbered"], lang, 4, keyed=False)),
        card(6, "checklist", "navy", lang, items(T["stats"], lang, 2)),
        card(7, "table", "cream", lang, items(T["table"], lang, 3), head=["a", "b"]),
        card(8, "process", "navy", lang, items(T["process"], lang, 4, keyed=False)),
        card(9, "cta", "cream", lang, items(T["cta6"], lang, 6, keyed=False)),
        card(10, "checklist", "navy", lang, bar_items(T["bars"], lang, 3), layout="bars"),
        card(11, "checklist", "cream", lang, bar_items(T["bars"], lang, 2), layout="bars"),
        card(12, "rest", "navy", lang, [fill(T["rest"]["text"][lang], lang)]),
    ]
    swapped = [dict(c, bg="cream" if c["bg"] == "navy" else "navy") for c in max_limits]
    swapped_variants = [dict(c, bg="cream" if c["bg"] == "navy" else "navy") for c in variants]
    cp = LIMITS["coverPanel"]["text"][lang]
    covers = [
        card(1, "cover", "navy", lang, [fill(cp, lang)], promise=fill(T["cover"]["promise"][lang], lang), coverStyle="panel", illustration="documents"),
        card(2, "cover", "cream", lang, [fill(cp, lang)], promise=fill(T["cover"]["promise"][lang], lang), coverStyle="panel", illustration="bridge"),
        card(3, "cover", "navy", lang, [fill(cp, lang)], promise=fill(T["cover"]["promise"][lang], lang), coverStyle="stat", hero={"value": "6" * T["cover"]["hero"]["value"][lang], "label": fill(T["cover"]["hero"]["label"][lang], lang)}),
        card(4, "cover", "cream", lang, [fill(cp, lang)], promise=fill(T["cover"]["promise"][lang], lang), coverStyle="stat", hero={"value": "6" * T["cover"]["hero"]["value"][lang], "label": fill(T["cover"]["hero"]["label"][lang], lang)}),
        card(5, "comparison", "cream", lang, items(T["comparison2"], lang, 2), illustration="route"),
        card(6, "flow", "navy", lang, with_icon(items(T["flow"], lang, 4)), note=fill(T["flow"]["note"][lang], lang), illustration="layers"),
        card(7, "table", "cream", lang, items(T["table"], lang, T["table"]["items"][1]), head=["a", "b"], illustration="calendar"),
        card(8, "checklist", "navy", lang, items(T["questions"], lang, 3, keyed=False), layout="questions", illustration="balance"),
    ]
    low = [  # 짧은 본문: 밀도 보정이 글자와 패널을 키워도 넘치지 않아야 한다
        card(1, "comparison", "navy", lang, [{"key": "가" if lang == "ko" else "A", "text": "가나" if lang == "ko" else "ab"}] * 2),
        card(2, "concept", "cream", lang, [{"key": "가" if lang == "ko" else "A", "text": "가나" if lang == "ko" else "ab"}] * 3, illustration="documents"),
        card(3, "table", "navy", lang, [{"key": "가" if lang == "ko" else "A", "text": "가나" if lang == "ko" else "ab"}] * 2, head=["a", "b"]),
        card(4, "process", "cream", lang, ["가나" if lang == "ko" else "ab"] * 4),
        card(5, "checklist", "navy", lang, ["가나" if lang == "ko" else "ab"] * 3, layout="questions", illustration="route"),
        card(6, "cta", "cream", lang, [{"key": "가" if lang == "ko" else "A", "text": "가나" if lang == "ko" else "ab"}] * 2),
        card(7, "flow", "navy", lang, [{"key": "가" if lang == "ko" else "A", "text": "가나" if lang == "ko" else "ab"}] * 3, illustration="bridge"),
        card(8, "checklist", "cream", lang, [{"key": "가" if lang == "ko" else "A", "text": "", "value": 6, "display": "6"}, {"key": "나" if lang == "ko" else "B", "text": "", "value": 3, "display": "3"}], layout="bars"),
    ]
    import build_cards as bc

    def boundary(kind, bg, n, keyed, kcap=99, **extra):
        """Content sized just under the 'low' density threshold: the largest card that still gets the enlarged type."""
        budget = bc.DENSITY_LIMITS[lang][0] - 1 - 22 * n
        per = max(budget // n, 2)
        if keyed:
            klen = min(max(per // 3, 1), kcap)
            body = [{"key": token(klen, lang), "text": fill(max(per - klen, 1), lang)} for _ in range(n)]
        else:
            body = [fill(per, lang) for _ in range(n)]
        return card(0, kind, bg, lang, body, **extra)

    KC = {name: spec["key"][lang] for name, spec in T.items() if "key" in spec}
    edge = [
        boundary("comparison", "navy", 2, True, kcap=KC["comparison2"]), boundary("comparison", "cream", 3, True, kcap=KC["comparison3"]), boundary("concept", "navy", 4, True, kcap=KC["concept4"]),
        boundary("concept", "cream", 3, True, kcap=KC["concept"]), boundary("table", "navy", 5, True, kcap=KC["table"], head=["a", "b"]), boundary("flow", "cream", 4, True, kcap=KC["flow"], note=fill(T["flow"]["note"][lang], lang)),
        boundary("process", "navy", 4, False), boundary("checklist", "cream", 3, False, layout="questions"), boundary("checklist", "navy", 3, True, kcap=KC["stats"], layout="stats"),
        boundary("checklist", "cream", 4, False), boundary("cta", "navy", 2, True, kcap=KC["cta2"]), boundary("cta", "cream", 6, False),
    ]
    for i, c in enumerate(edge, 1):
        c["page"] = i
    return {"edge-of-low": edge, "max-limits": max_limits, "variants": variants, "max-limits-swapped": swapped, "variants-swapped": swapped_variants, "covers": covers, "low-density": low}


def hard_failures(report):
    """Lines under a '### card_NN.html' heading that are not advisory ('권고') sections."""
    out, current = [], None
    for line in report.splitlines():
        if line.startswith("### "):
            current = None if "권고" in line else line[4:]
        elif current and line.startswith("- "):
            out.append(f"{current}: {line[2:]}")
    return out


def main():
    if WORK.exists():
        shutil.rmtree(WORK)
    failed = []
    for lang in ("ko", "en"):
        for name, cards in sets(lang).items():
            data = {"language": lang, "series": "Spec", "issue": "No.00", "totalPages": len(cards),
                    "canvasProfile": "portrait", "visualFamily": "social-native", "cards": cards, "coverLabel": "Spec", "editorialReview": {"pipelineVersion": "2.0"}}
            html_dir = WORK / f"{name}-{lang}"  # depth 3 below the repo root, as the CSS links expect
            html_dir.mkdir(parents=True)
            for item in cards:
                (html_dir / f"card_{item['page']:02d}.html").write_text(build(item, data), encoding="utf-8")
            source = WORK / f"{name}-{lang}.md"
            source.write_text("stress", encoding="utf-8")
            out = WORK / "out" / f"{name}-{lang}"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "qa_render.py"), "--html-dir", str(html_dir), "--source", str(source), "--out", str(out), "--allow-partial"],
                capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})
            report = (out / "qa-report.md").read_text(encoding="utf-8") if (out / "qa-report.md").exists() else result.stdout + result.stderr
            print(f"{'PASS' if result.returncode == 0 else 'FAIL'} {name}/{lang}")
            if result.returncode != 0:
                failed.append(f"{name}/{lang}")
                for line in hard_failures(report):
                    print(f"   {line}")
    failed += og_stress()
    if not os.environ.get("SPEC_STRESS_KEEP"):
        shutil.rmtree(WORK, ignore_errors=True)
    return 1 if failed else 0


def og_stress():
    """Landscape share image at the longest allowed cover headline, every cover style and both backgrounds."""
    import build_og

    failed = []
    for lang in ("ko", "en"):
        for style, bg in (("art", "navy"), ("art", "cream"), ("panel", "navy"), ("stat", "cream")):
            cover = card(1, "cover", bg, lang, [fill(T["cover"]["text"][lang], lang)], promise=fill(T["cover"]["promise"][lang], lang), coverStyle=style)
            if style == "art":
                cover["art"] = ["server", "landmark", "globe"]
            data = {"language": lang, "series": "Spec", "coverLabel": "Spec", "cards": [cover]}
            name = f"{lang}-{style}-{bg}"
            problems = build_og.render([(name, data)], WORK / "og-out")[name]
            print(f"{'PASS' if not problems else 'FAIL'} og/{name}" + ("" if not problems else ": " + ", ".join(problems)))
            if problems:
                failed.append(f"og/{name}")
    return failed


if __name__ == "__main__":
    sys.exit(main())
