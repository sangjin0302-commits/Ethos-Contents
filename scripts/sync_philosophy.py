#!/usr/bin/env python3
"""Build the read-only copy of docs/brand-philosophy.md that is pushed to the website repository.

Ethos-Contents is the source of truth. The copy gets a header naming the source version and commit,
and the sync workflow overwrites it on every change, so hand edits in the copy never survive.
With --dest, exit code 0 means the destination was written (or is already identical).
With --compare, exit code 0 means the candidate is identical and 1 means it differs.
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "docs" / "brand-philosophy.md"


def version_of(text):
    match = re.search(r"^- 버전:\s*(.+)$", text, flags=re.MULTILINE)
    if not match:
        raise SystemExit("FAIL: source has no '- 버전:' line")
    return match.group(1).strip()


def build_copy(source_text, commit):
    version = version_of(source_text)
    header = (f"<!-- 자동 동기화 사본(읽기 전용). 정본: Ethos-Contents docs/brand-philosophy.md · {version} · 커밋 {commit}. "
              "이 파일을 직접 고치지 마세요. 다음 동기화 때 정본으로 덮어씁니다. -->\n\n")
    return header + source_text.lstrip("﻿")


def matches_copy(path, expected):
    candidate = pathlib.Path(path)
    return candidate.exists() and candidate.read_text(encoding="utf-8") == expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--dest", help="path of the copy inside the website repository checkout")
    target.add_argument("--compare", help="candidate copy to compare without writing")
    parser.add_argument("--commit", default="local", help="short commit SHA of the source")
    args = parser.parse_args()
    content = build_copy(pathlib.Path(args.source).read_text(encoding="utf-8"), args.commit)
    if args.compare:
        candidate = pathlib.Path(args.compare)
        if matches_copy(candidate, content):
            print(f"unchanged: {candidate}")
            return 0
        print(f"different: {candidate}")
        return 1
    dest = pathlib.Path(args.dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if matches_copy(dest, content):
        print(f"unchanged: {dest}")
        return 0
    dest.write_text(content, encoding="utf-8", newline="\n")
    print(f"written: {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
