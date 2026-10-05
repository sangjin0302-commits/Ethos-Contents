#!/usr/bin/env python3
"""Validate carousel alt text and external-asset provenance records."""

import argparse
import json
import pathlib
import re
import sys


LANGUAGE_HEADINGS = {"ko": "Korean", "en": "English"}
CTA_TERMS = {
    "ko": ("무료 검토", "문의", "연락", "상담 신청"),
    "en": ("free review", "contact us", "send a dm", "book a call"),
}


def extract_alt_section(text, heading):
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$.*?^###\s+Alt text\s*$\s*(.*?)(?=^###\s+|^##\s+|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def numbered_items(section):
    items = []
    for line in section.splitlines():
        match = re.match(r"^\s*(\d+)[.)]\s+(.+?)\s*$", line)
        if match:
            items.append((int(match.group(1)), match.group(2)))
    return items


def validate_alt_text(folder, distribution):
    failures, warnings = [], []
    for language, heading in LANGUAGE_HEADINGS.items():
        data_path = folder / f"card-data.{language}.json"
        if not data_path.exists():
            failures.append(f"missing card data: {data_path.name}")
            continue
        data = json.loads(data_path.read_text(encoding="utf-8"))
        expected = int(data.get("totalPages", len(data.get("cards", []))))
        section = extract_alt_section(distribution, heading)
        template_markers = ("카드 수만큼", "Write one numbered alt text item")
        if not section or section in {"-", "1."} or any(marker in section for marker in template_markers):
            failures.append(f"{language}: Alt text section is empty")
            continue
        items = numbered_items(section)
        if items:
            numbers = [number for number, _ in items]
            if numbers != list(range(1, expected + 1)):
                failures.append(f"{language}: per-card alt text must be numbered 1..{expected}")
            copies = [copy.casefold().strip() for _, copy in items]
            if len(copies) != len(set(copies)):
                failures.append(f"{language}: duplicate per-card alt text")
        else:
            warnings.append(f"{language}: carousel-summary alt text used; per-card alt text is recommended")
            copies = [section.casefold()]
        if any(term in " ".join(copies) for term in CTA_TERMS[language]):
            failures.append(f"{language}: alt text must describe content, not contain a sales CTA")
    return failures, warnings


def validate_assets(folder):
    path = folder / "assets.md"
    if not path.exists():
        return ["missing assets.md provenance record"], []
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^EXTERNAL ASSETS:\s*(Yes|No)\s*$", text, flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        return ["assets.md must declare EXTERNAL ASSETS: Yes or No"], []
    if match.group(1).casefold() == "no":
        return [], []

    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|") or re.match(r"^\s*\|?\s*-+", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and cells[0].casefold() not in {"asset", "자산"}:
            rows.append(cells)
    if not rows:
        return ["assets.md declares external assets but has no records"], []
    failures = []
    for index, cells in enumerate(rows, 1):
        if len(cells) < 6 or any(not value for value in cells[:6]):
            failures.append(f"assets.md row {index}: asset, source URL, creator, license, checked date, modification are required")
        elif not re.match(r"https?://", cells[1]):
            failures.append(f"assets.md row {index}: source URL must be http(s)")
        elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[4]):
            failures.append(f"assets.md row {index}: checked date must use YYYY-MM-DD")
    return failures, []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("content_dir", help="content/<ID> directory")
    args = parser.parse_args()
    folder = pathlib.Path(args.content_dir)
    distribution_path = folder / "distribution.md"
    if not distribution_path.exists():
        raise SystemExit("FAIL: missing distribution.md")

    failures, warnings = validate_alt_text(folder, distribution_path.read_text(encoding="utf-8"))
    asset_failures, asset_warnings = validate_assets(folder)
    failures.extend(asset_failures)
    warnings.extend(asset_warnings)
    for warning in warnings:
        print(f"WARN: {warning}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("PASS: distribution alt text and asset provenance")
    return 0


if __name__ == "__main__":
    sys.exit(main())
