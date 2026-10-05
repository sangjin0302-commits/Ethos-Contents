#!/usr/bin/env python3
"""Render a preview of card-data sets and run every gate, for CI or a quick local check.

The copywriter (ChatGPT or a person) only edits content/<ID>/card-data.{ko,en}.json. This script:
  1. validates the JSON against schema/card-data.schema.json
  2. runs copy_lint (advisory) and builds the HTML with the deterministic builder
  3. runs qa_render.py (hard gates) against the blog, producing PNGs, sheet-270.png and qa-report.md
  4. writes a Markdown summary (to $GITHUB_STEP_SUMMARY in CI) that can be pasted back to the copywriter

A preview render never means approval: `approvedBy` is not required here.
"""

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

from jsonschema import Draft7Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_cards import build  # noqa: E402
import build_og  # noqa: E402
import copy_lint  # noqa: E402

ENV = {**os.environ, "PYTHONUTF8": "1"}


def content_ids(args):
    if args.ids:
        return args.ids
    paths = []
    if args.changed and not re.fullmatch(r"0+", args.changed):
        for base in (args.changed, "origin/main"):
            result = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD", "--", "content"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            if result.returncode == 0:
                paths = result.stdout.splitlines()
                break
    if not paths:
        paths = [str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "content").glob("*/card-data.*.json")]
    ids = sorted({p.split("/")[1] for p in paths if re.match(r"content/[^/]+/card-data\.\w+\.json$", p)})
    return [i for i in ids if not i.startswith(("_", ".")) and (ROOT / "content" / i).is_dir()]


def hard_failures(report_md):
    out, current = [], None
    for line in report_md.splitlines():
        if line.startswith("### "):
            current = None if "권고" in line else line[4:]
        elif current and line.startswith("- "):
            out.append(f"{current}: {line[2:]}")
    return out


def previous_version(base, content_id, lang):
    """card-data at the base commit, or None when the set is new or the base is unknown."""
    if not base or re.fullmatch(r"0+", base):
        return None
    for ref in (base, "origin/main"):
        result = subprocess.run(["git", "show", f"{ref}:content/{content_id}/card-data.{lang}.json"], cwd=ROOT, capture_output=True)
        if result.returncode == 0:
            try:
                return json.loads(result.stdout.decode("utf-8"))
            except json.JSONDecodeError:
                return None
    return None


def compare_section(content_id, base):
    """Fact and hedge changes against the previous version, so an AI rewrite that drops a condition is visible."""
    folder = ROOT / "content" / content_id
    caption = (folder / "distribution.md").read_text(encoding="utf-8") if (folder / "distribution.md").exists() else ""
    lines = []
    for lang in ("ko", "en"):
        path = folder / f"card-data.{lang}.json"
        old = previous_version(base, content_id, lang)
        if old is None or not path.exists():
            continue
        report = copy_lint.Report()
        copy_lint.compare(old, json.loads(path.read_text(encoding="utf-8")), report, caption)
        lines += [f"- `{lang}` {f['message']}" for f in report.findings if f["level"] == "warn"]
    if not lines:
        return ""
    return "\n".join([f"### ⚠️ {content_id}: 이전 버전 대비 사실·한정어 변화", "", *lines,
                      "", "윤문이나 수정 과정에서 바뀐 것이 의도한 것인지 확인하세요. 의도한 변경이면 그대로 두면 됩니다.", ""])


def run_id(content_id, out_root, validator):
    folder = ROOT / "content" / content_id
    lines = [f"## {content_id}", ""]
    ok = True
    blog = folder / "blog.md"
    for lang in ("ko", "en"):
        path = folder / f"card-data.{lang}.json"
        if not path.exists():
            lines.append(f"- `{lang}`: card-data.{lang}.json 없음")
            ok = False
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = [f"{'.'.join(map(str, e.path)) or 'root'}: {e.message[:120]}" for e in sorted(validator.iter_errors(data), key=lambda e: list(e.path))]
        if errors:
            ok = False
            lines += [f"### {lang}: 스키마 오류", *[f"- {e}" for e in errors[:15]], ""]
            continue
        report = copy_lint.Report()
        copy_lint.lint_cards(data, lang, report, json.loads((folder / "terms.json").read_text(encoding="utf-8")) if (folder / "terms.json").exists() else None)
        copy_lint.lint_limits(data, lang, report)
        warns = [f for f in report.findings if f["level"] == "warn"]
        html_dir = out_root / content_id / lang  # depth 3 below the repo root, as the CSS links expect
        html_dir.mkdir(parents=True, exist_ok=True)
        for card in data["cards"]:
            (html_dir / f"card_{card['page']:02d}.html").write_text(build(card, data), encoding="utf-8")
        out_dir = out_root / content_id / "out" / lang
        if not blog.exists():
            lines.append(f"- `{lang}`: blog.md 없음 — 사실 잠금을 확인할 수 없어 QA를 건너뜀")
            ok = False
            continue
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "qa_render.py"), "--html-dir", str(html_dir), "--source", str(blog), "--out", str(out_dir)],
                                capture_output=True, text=True, encoding="utf-8", env=ENV)
        qa_md = (out_dir / "qa-report.md").read_text(encoding="utf-8") if (out_dir / "qa-report.md").exists() else result.stdout + result.stderr
        passed = result.returncode == 0
        ok &= passed
        lines.append(f"### {lang}: QA {'PASS ✅' if passed else 'FAIL ❌'} · 린터 경고 {len(warns)}건")
        if not passed:
            lines += [f"- {item}" for item in hard_failures(qa_md)[:25]] or [f"- ```{qa_md[-600:]}```"]
        for finding in warns[:12]:
            lines.append(f"- 린터 `{finding['rule']}` {finding['where']}: {finding['message']}")
        lines.append("")
    og_items = [(lang, json.loads((folder / f"card-data.{lang}.json").read_text(encoding="utf-8")))
                for lang in ("ko", "en") if (folder / f"card-data.{lang}.json").exists()]
    try:
        og = build_og.render(og_items, out_root / content_id / "out")
    except ValueError as error:  # e.g. the set has no cover card
        og = {lang: [str(error)] for lang, _ in og_items}
    for lang, problems in og.items():
        lines.append(f"- 가로 대표 이미지(1200×630) `og-{lang}.png`: " + ("PASS ✅" if not problems else "FAIL ❌ " + ", ".join(problems)))
        ok &= not problems
    return ok, "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ids", nargs="*", help="content IDs; default is the sets changed since --changed (or all)")
    parser.add_argument("--changed", help="git base SHA/ref used to find changed sets")
    parser.add_argument("--out", default="ci-out", help="work dir; must be exactly one level below the repo root")
    args = parser.parse_args()

    ids = content_ids(args)
    if not ids:
        print("no card-data changes to render")
        return 0
    out_root = ROOT / args.out
    validator = Draft7Validator(json.loads((ROOT / "schema" / "card-data.schema.json").read_text(encoding="utf-8")))
    sections, ok = ["# 카드 미리보기 렌더 (승인 아님)", "", "FAIL이 있으면 해당 카드의 글을 줄이거나 카드를 나눠 JSON만 고치세요. 이 보고서를 그대로 작성자에게 붙여 넣으면 됩니다.", ""], True
    warnings = []
    for content_id in ids:
        passed, text = run_id(content_id, out_root, validator)
        ok &= passed
        sections.append(text)
        changed = compare_section(content_id, args.changed)
        if changed:
            sections.append(changed)
            warnings.append(changed)
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "compare.md").write_text("\n".join(warnings), encoding="utf-8")
    summary = "\n".join(sections)
    print(summary)
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with open(target, "a", encoding="utf-8") as handle:
            handle.write(summary + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
