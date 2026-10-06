#!/usr/bin/env python3
"""세 방향 시안 미리보기: drafts/<A|B|C>/ko/*.html을 PNG로 찍고 방향별로 나란히 붙인 비교 시트를 만든다.

QA 게이트(장수·쪽번호)는 적용하지 않는다. 시안은 방향을 고르는 용도이고, 고른 뒤 전체 세트를 qa_render.py로 검사한다.
사용: python scripts/preview_drafts.py content/<ID>/drafts
"""

import argparse
import os
import pathlib

from PIL import Image
from playwright.sync_api import sync_playwright


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("drafts", help="drafts 폴더 (하위에 A/ko, B/ko, C/ko)")
    args = parser.parse_args()
    root = pathlib.Path(args.drafts)
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=os.environ.get("CHROMIUM_PATH") or None)
        page = browser.new_page(viewport={"width": 540, "height": 675}, device_scale_factor=2)
        page.route("**/*", lambda r: r.continue_() if r.request.url.startswith("file://") else r.abort())
        for variant in sorted(d for d in root.iterdir() if d.is_dir()):
            shots = []
            for html in sorted((variant / "ko").glob("card_*.html")):
                page.goto(html.resolve().as_uri(), wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                png = variant / f"{html.stem}.png"
                page.locator(".card").screenshot(path=str(png))
                shots.append(png)
            if shots:
                rows.append((variant.name, shots))
        browser.close()
    if not rows:
        print("시안 HTML이 없습니다.")
        return 1
    thumb_w, thumb_h, gap = 270, 338, 12
    cols = max(len(shots) for _, shots in rows)
    sheet = Image.new("RGB", (cols * (thumb_w + gap) + gap, len(rows) * (thumb_h + gap) + gap), (128, 128, 128))
    for r, (_, shots) in enumerate(rows):
        for c, png in enumerate(shots):
            img = Image.open(png).convert("RGB").resize((thumb_w, thumb_h))
            sheet.paste(img, (gap + c * (thumb_w + gap), gap + r * (thumb_h + gap)))
    out = root / "drafts-sheet.png"
    sheet.save(out)
    print(f"시안 {len(rows)}개 방향 → {out} (위에서부터 {', '.join(name for name, _ in rows)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
