#!/usr/bin/env python3
"""자유 디자인(B) 카드에 붙여 넣을 Lucide 아이콘 SVG를 출력한다.

사용: python scripts/icon_svg.py calendar-clock [--class cv-ico]
출력에는 data-icon="<이름>"이 붙는다. copy_lint.py가 이 값으로 assets.md 출처 기록을 확인한다.
크기·색·선 굵기는 design.css에서 정한다(색은 brand/tokens.css 변수, stroke는 currentColor).
목록: assets/icons/lucide/README.md
"""
import argparse
import sys

from build_cards import ICON_DIR, icon_svg


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", nargs="?")
    parser.add_argument("--class", dest="cls", default="ico")
    parser.add_argument("--list", action="store_true", help="쓸 수 있는 아이콘 이름")
    args = parser.parse_args(argv)
    if args.list or not args.name:
        print(" ".join(sorted(p.stem for p in ICON_DIR.glob("*.svg"))))
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
