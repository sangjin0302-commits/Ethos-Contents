#!/usr/bin/env python3
"""자유 디자인(B) 카드에 붙여 넣을 Lucide 아이콘 SVG를 출력한다.

사용: python scripts/icon_svg.py calendar-clock [--class cv-ico]
출력에는 data-icon="<이름>"이 붙는다. copy_lint.py가 이 값으로 assets.md 출처 기록을 확인한다.
크기·색·선 굵기는 design.css에서 정한다(색은 brand/tokens.css 변수, stroke는 currentColor).
목록: assets/icons/lucide/README.md, assets/icons/tabler/README.md
"""
import argparse
import sys

from build_cards import ICON_DIRS, icon_svg


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", nargs="?")
    parser.add_argument("--class", dest="cls", default="ico")
    parser.add_argument("--list", action="store_true", help="쓸 수 있는 아이콘 이름")
    parser.add_argument("--search", help="이름에 이 낱말이 들어간 아이콘만 출력(영문 소문자)")
    args = parser.parse_args(argv)
    if args.search:
        names = sorted({p.stem for folder in ICON_DIRS for p in folder.glob("*.svg") if args.search.lower() in p.stem})
        print(" ".join(names) or "(없음)")
        return 0
    if args.list or not args.name:
        print(" ".join(sorted({p.stem for folder in ICON_DIRS for p in folder.glob("*.svg")})))
        return 0
    try:
        svg = icon_svg(args.name)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(svg.replace('class="ico"', f'class="{args.cls}" data-icon="{args.name}"', 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
