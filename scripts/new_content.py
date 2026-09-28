#!/usr/bin/env python3
"""Create a bilingual ETHOS content workspace from a blog supplied by file or stdin."""

import argparse
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{1,63}$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create content/<ID> for Korean and English cards")
    parser.add_argument("--id", required=True, help="2-64 characters: letters, numbers, _ or -")
    parser.add_argument("--source", help="Blog Markdown file. If omitted, read UTF-8 text from stdin")
    args = parser.parse_args()

    if not ID_RE.fullmatch(args.id):
        parser.error("--id must use 2-64 letters, numbers, underscores, or hyphens")

    text = pathlib.Path(args.source).read_text(encoding="utf-8") if args.source else sys.stdin.read()
    if not text.strip():
        parser.error("blog content is empty")

    target = ROOT / "content" / args.id
    if target.exists():
        parser.error(f"refusing to overwrite existing directory: {target}")

    target.mkdir(parents=True)
    (target / "blog.md").write_text(text.rstrip() + "\n", encoding="utf-8")
    shutil.copyfile(ROOT / "content" / "_TEMPLATE" / "brief.md", target / "brief.md")
    shutil.copyfile(ROOT / "content" / "_TEMPLATE" / "distribution.md", target / "distribution.md")
    for language in ("ko", "en"):
        (target / language).mkdir()

    print(f"created: {target}")
    print("next: write brief.md and card-data.ko.json/card-data.en.json, then request copy approval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
