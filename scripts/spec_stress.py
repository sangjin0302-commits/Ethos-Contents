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
        headline = fill(h[("cover" + lang.capitalize()) if kind == "cover" else lang], lang)
    data = {"page": page, "type": kind, "bg": bg, "oneMessage": "m", "headline": headline, "body": body,
            "takeaway": fill(LIMITS["takeaway"][lang], lang), "sourceTrace": {"heading": "h", "evidence": "S"}}
    data.update(extra)
    return data


def items(spec, lang, count, keyed=True):
    return [({"key": token(spec["key"][lang], lang), "text": fill(spec["text"][lang], lang)} if keyed
             else fill(spec["text"][lang], lang)) for _ in range(count)]


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
    ]
    swapped = [dict(c, bg="cream" if c["bg"] == "navy" else "navy") for c in max_limits]
    swapped_variants = [dict(c, bg="cream" if c["bg"] == "navy" else "navy") for c in variants]
    return {"max-limits": max_limits, "variants": variants, "max-limits-swapped": swapped, "variants-swapped": swapped_variants}


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
                    "canvasProfile": "portrait", "visualFamily": "social-native", "cards": cards, "coverLabel": "Spec"}
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
    if not os.environ.get("SPEC_STRESS_KEEP"):
        shutil.rmtree(WORK, ignore_errors=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
