#!/usr/bin/env python3
"""Render a deterministic Instagram fixture and compare it with committed PNG baselines."""

import argparse
import pathlib
import shutil
import sys

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build_cards import build  # noqa: E402


def fixture():
    def card(page, kind, body, bg, headline):
        return {
            "page": page, "type": kind, "bg": bg, "oneMessage": headline,
            "headline": headline, "body": body, "takeaway": "판단 기준을 확인하세요.",
            "sourceTrace": {"heading": "Visual fixture", "evidence": "S"},
        }

    cards = [
        card(1, "cover", ["대상과 문제를 한 문장으로 확인합니다."], "navy", "새로운 서비스를 시작할 때, 어떤 인허가부터 확인해야 할까요?"),
        card(2, "concept", ["서비스 — 실제로 제공하는 기능", "이용자 — 돈을 내거나 책임지는 주체", "수익 — 결제와 정산의 흐름", "공간 — 영업이 이뤄지는 장소"], "cream", "업종명보다 먼저 볼 네 가지"),
        card(3, "process", ["사업 구조를 한 문장으로 정리", "관련 법령과 담당 기관 확인", "서류 사이의 설명 일치 점검", "신청 전 보완 가능성 검토"], "navy", "검토는 이 순서로 진행합니다"),
        card(4, "quote", ["공식 자료", "문구 하나보다 적용 조건과 예외를 함께 읽습니다.", "근거와 판단을 구분합니다."], "cream", "근거는 결론과 함께 읽습니다"),
        card(5, "cta", ["직접 준비 — 사업 구조와 현재 자료 정리", "종합 검토 — 업종 경계·복수 기관·서류 충돌"], "navy", "직접 준비할 범위와 검토가 필요한 상황"),
    ]
    return {
        "language": "ko", "series": "신사업 인허가", "coverLabel": "사업 구조 점검",
        "issue": "No.00", "totalPages": len(cards), "canvasProfile": "portrait",
        "visualFamily": "social-native", "cards": cards,
    }


def render(target):
    html_dir = ROOT / "content" / ".visual-regression" / "ko"
    if html_dir.exists():
        shutil.rmtree(html_dir)
    html_dir.mkdir(parents=True)
    data = fixture()
    for item in data["cards"]:
        (html_dir / f"card_{item['page']:02d}.html").write_text(build(item, data), encoding="utf-8")
    target.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 540, "height": 675}, device_scale_factor=2,
                                      locale="ko-KR", timezone_id="Asia/Seoul", color_scheme="light", reduced_motion="reduce")
        context.route("**/*", lambda route: route.continue_() if route.request.url.startswith("file://") else route.abort())
        for html_file in sorted(html_dir.glob("card_*.html")):
            page = context.new_page()
            page.goto(html_file.resolve().as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.locator(".card").screenshot(path=str(target / f"{html_file.stem}.png"), animations="disabled", caret="hide")
            page.close()
        browser.close()
    shutil.rmtree(html_dir)


def changed_ratio(reference, current, channel_tolerance):
    a, b = Image.open(reference).convert("RGB"), Image.open(current).convert("RGB")
    if a.size != b.size:
        return 1.0
    diff = ImageChops.difference(a, b)
    pixels = diff.get_flattened_data() if hasattr(diff, "get_flattened_data") else diff.getdata()
    changed = sum(1 for px in pixels if max(px) > channel_tolerance)
    return changed / (a.width * a.height)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", default=str(ROOT / "tests" / "visual-baseline"))
    parser.add_argument("--current", default=str(ROOT / "tests" / ".visual-current"))
    parser.add_argument("--update", action="store_true", help="replace the baseline after intentional visual review")
    parser.add_argument("--max-changed-ratio", type=float, default=0.003)
    parser.add_argument("--channel-tolerance", type=int, default=8)
    args = parser.parse_args()
    baseline, current = pathlib.Path(args.baseline), pathlib.Path(args.current)
    render(current)
    if args.update:
        if baseline.exists():
            shutil.rmtree(baseline)
        shutil.copytree(current, baseline)
        print(f"updated visual baseline: {baseline}")
        return 0
    failures = []
    for image in sorted(current.glob("card_*.png")):
        reference = baseline / image.name
        if not reference.exists():
            failures.append(f"missing baseline: {image.name}")
            continue
        ratio = changed_ratio(reference, image, args.channel_tolerance)
        print(f"{image.name}: changed {ratio:.3%}")
        if ratio > args.max_changed_ratio:
            failures.append(f"{image.name}: {ratio:.3%} > {args.max_changed_ratio:.3%}")
    if failures:
        print("FAIL: " + "; ".join(failures))
        return 1
    print("PASS: visual regression")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
