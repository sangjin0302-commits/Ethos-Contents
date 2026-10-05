#!/usr/bin/env python3
"""Build the read-only copy of docs/brand-philosophy.md that is pushed to the website repository.

Ethos-Contents is the source of truth. The copy gets a header naming the source version and commit,
and the sync workflow overwrites it on every change, so hand edits in the copy never survive.
Exit code 0 means the destination was written (or is already identical); the path is printed.
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--dest", required=True, help="path of the copy inside the website repository checkout")
    parser.add_argument("--commit", default="local", help="short commit SHA of the source")
    args = parser.parse_args()
    content = build_copy(pathlib.Path(args.source).read_text(encoding="utf-8"), args.commit)
    dest = pathlib.Path(args.dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.read_text(encoding="utf-8") == content:
        print(f"unchanged: {dest}")
        return 0
    dest.write_text(content, encoding="utf-8", newline="\n")
    print(f"written: {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
