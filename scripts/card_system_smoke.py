#!/usr/bin/env python3
"""Fast, dependency-free regression checks for the reusable card builder."""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_cards import build  # noqa: E402


def card(page, kind, body, *, bg="navy", headline="Headline", page_turn="Internal next step"):
    return {
        "page": page,
        "type": kind,
        "bg": bg,
        "oneMessage": "One message",
        "headline": headline,
        "body": body,
        "takeaway": "Takeaway",
        "pageTurn": page_turn,
        "sourceTrace": {"heading": "Source", "evidence": "F"},
    }


def assert_contains(markup, value, label):
    if value not in markup:
        raise AssertionError(f"{label}: missing {value!r}")


def assert_not_contains(markup, value, label):
    if value in markup:
        raise AssertionError(f"{label}: unexpected {value!r}")


def main():
    cards = [
        card(1, "cover", ["Lead"], headline="Cover headline"),
        card(2, "checklist", ["① First", "2 Second"], bg="cream"),
        card(3, "quote", ["Authority", "Finding", "Note"]),
        card(4, "comparison", ["A — Alpha", "B — Beta", "C — Gamma"], bg="cream"),
        card(5, "process", ["1 First", "02 Second", "③ Third", "4. Fourth"]),
        card(6, "concept", ["Rule — Copy", "Limit — Copy"], bg="cream"),
        card(7, "cta", ["1 Facts", "2 Law", "3 Period", "4 Option", "5 Value"]),
    ]
    data = {
        "language": "ko",
        "canvasProfile": "portrait",
        "visualFamily": "social-native",
        "series": "Regression Series",
        "coverLabel": "Content-specific label",
        "issue": "No.99",
        "totalPages": len(cards),
    }
    rendered = [build(item, data) for item in cards]
    joined = "\n".join(rendered)

    assert_contains(rendered[0], "Content-specific label", "cover label")
    assert_not_contains(joined, "Overseas Game Launch", "hard-coded topic")
    assert_not_contains(joined, "Internal next step", "pageTurn visibility")
    assert_contains(rendered[0], 'data-progress="01 / 07"', "page count visibility")
    assert_contains(rendered[1], '<div class="kicker-num" data-decor>02</div>', "page number")
    assert_contains(rendered[3], 'class="split split-3"', "three-item comparison")
    assert_contains(rendered[4], 'class="process-steps process-4"', "four-step process")
    for duplicate in (">① First<", ">2 Second<", ">1 First<", ">02 Second<", ">③ Third<", ">4. Fourth<"):
        assert_not_contains(joined, duplicate, "duplicate step prefix")
    assert_contains(rendered[6], "Facts", "CTA step copy")
    assert_not_contains(rendered[6], ">1 Facts<", "CTA duplicate step prefix")
    assert_contains(rendered[0], 'data-frame="page" aria-hidden="true" data-progress="01 / 07"', "progress page frame")
    assert_contains(rendered[0], 'canvas-portrait family-social-native beat-bold pace-a', "Instagram profile classes")
    assert_contains(rendered[1], 'beat-toolkit pace-b', "semantic visual beat")
    assert_contains(rendered[0], 'data-canvas="portrait"', "canvas metadata")

    default_data = {key: value for key, value in data.items() if key not in ("canvasProfile", "visualFamily")}
    default_markup = build(cards[0], default_data)
    assert_contains(default_markup, 'canvas-portrait family-social-native', "Instagram defaults")

    print("PASS: reusable card builder regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
