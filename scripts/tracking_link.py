#!/usr/bin/env python3
"""게시물마다 붙일 상담 접수 추적 링크를 만든다.

웹사이트 /intake 는 source·channel·content_id·placement 를 받아 문의에 저장하고
/admin/funnel 에서 채널·글·위치별 문의를 집계한다(Admin-system- 저장소
docs/contracts/public-intake-source-tracking.md). 값이 없어도 접수는 막히지 않는다.

utm_* 는 쓰지 않는다. 위 네 값만으로 집계가 되고, 블로그 본문 검사(copy_lint
tracking-link)와도 충돌하지 않는다. 링크는 카드·본문이 아니라 프로필·링크 스티커·
댓글·강연 QR처럼 본문 밖에 둔다.

사용:
  python scripts/tracking_link.py SUSPENSION-04 --channel instagram linkedin --lang ko en
  python scripts/tracking_link.py SUSPENSION-04 --markdown   # distribution.md 표 행
"""
import argparse
import re
import sys
from urllib.parse import urlencode

BASE = "https://ethosattorney.com/intake"
CHANNELS = {
    # 채널: 기본 링크 위치(placement 앞부분)
    "instagram": "bio",
    "linkedin": "comment",
    "naver_blog": "profile",
    "kakao": "message",
    "threads": "bio",
    "lecture": "qr",
    "email": "signature",
}
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{1,79}$")


def tracking_link(content_id, channel, lang, placement=None):
    if not ID_RE.match(content_id):
        raise ValueError(f"content_id 형식이 아닙니다: {content_id!r} (영문·숫자·-·_ 80자 이내)")
    if channel not in CHANNELS:
        raise ValueError(f"알 수 없는 채널: {channel!r} ({', '.join(CHANNELS)})")
    if lang not in ("ko", "en"):
        raise ValueError(f"언어는 ko 또는 en: {lang!r}")
    spot = placement or CHANNELS[channel]
    query = {"source": "ethos-contents", "channel": channel, "content_id": content_id,
             "placement": f"{spot}-{lang}"}
    return f"{BASE}?{urlencode(query)}"


def tracking_name(content_id, channel, lang):
    return f"{content_id}-{channel}-{lang}"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("content_id")
    parser.add_argument("--channel", nargs="+", default=["instagram", "linkedin"], choices=sorted(CHANNELS))
    parser.add_argument("--lang", nargs="+", default=["ko", "en"], choices=["ko", "en"])
    parser.add_argument("--placement", help="링크 위치를 직접 지정(예: story-sticker)")
    parser.add_argument("--markdown", action="store_true", help="distribution.md Tracking 표 행으로 출력")
    args = parser.parse_args(argv)
    try:
        rows = [(c, l, tracking_name(args.content_id, c, l), tracking_link(args.content_id, c, l, args.placement))
                for c in args.channel for l in args.lang]
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if args.markdown:
        print("\n".join(f"| {c} | {l} |  | {name} | {url} |  |" for c, l, name, url in rows))
    else:
        print("\n".join(f"{name}\t{url}" for _, _, name, url in rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
