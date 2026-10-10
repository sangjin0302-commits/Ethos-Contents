#!/usr/bin/env python3
"""받을 자료(lead magnet) HTML을 A4 PDF와 PNG(2배)로 렌더한다. 글꼴은 로컬 fonts/만 쓰고 외부 호출은 없다.

쓰는 법: python scripts/render_lead_magnet.py content/<ID>/lead-magnet/checklist.html
출력: 같은 폴더의 checklist.pdf, checklist.png (A4 794×1123 CSS px, PNG는 1588×2246)
넘침 검사: 본문이 시트 밖으로 나가면 실패로 끝낸다.
"""

import os
import pathlib
import sys

from playwright.sync_api import sync_playwright


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    src = pathlib.Path(sys.argv[1]).resolve()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=os.environ.get("CHROMIUM_PATH") or None)
        page = browser.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=2)
        page.goto(src.as_uri())
        page.evaluate("document.fonts.ready")
        loaded = page.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family)")
        overflow = page.evaluate("""() => {
          const s = document.querySelector('.sheet'), r = s.getBoundingClientRect(), bad = [];
          s.querySelectorAll('main, section, footer').forEach(e => { const b = e.getBoundingClientRect();
            if (b.bottom > r.bottom + 0.5 || b.right > r.right + 0.5) bad.push(e.tagName + '.' + e.className); });
          const m = s.querySelector('main').getBoundingClientRect(), f = s.querySelector('footer').getBoundingClientRect();
          if (m.bottom > f.top - 8) bad.push('main overlaps footer');
          return bad; }""")
        page.locator(".sheet").screenshot(path=str(src.with_suffix(".png")))
        page.pdf(path=str(src.with_suffix(".pdf")), format="A4", print_background=True, prefer_css_page_size=True)
        browser.close()
    if not any("Pretendard" in f for f in loaded) or not any("ETHOS Serif" in f for f in loaded):
        print(f"FAIL: 브랜드 글꼴이 로드되지 않았습니다: {sorted(set(loaded))}")
        return 1
    if overflow:
        print(f"FAIL: 넘침 {overflow}")
        return 1
    print(f"PASS: {src.with_suffix('.pdf').name}, {src.with_suffix('.png').name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
