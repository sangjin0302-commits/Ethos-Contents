import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import design_review  # noqa: E402

FREE = '<meta name="ethos-design" content="free">'


def card(main, free=True):
    return (f'<html><head>{FREE if free else ""}</head><body><div class="card">'
            f'<div class="z-title" data-zone="title"><h2>제목</h2></div>'
            f'<div class="z-main" data-zone="main">{main}</div>'
            f'<div class="z-take" data-zone="take"><div class="close">결론</div></div></div></body></html>')


SVG = '<svg viewBox="0 0 1 1"><path d="M0 0"/></svg>'


class DesignReviewTest(unittest.TestCase):
    """Advisory checks that catch template-looking sets (same list frame, no focal, no pictures)."""

    def run_set(self, mains, free=True):
        with tempfile.TemporaryDirectory() as tmp:
            folder = pathlib.Path(tmp)
            (folder / "ko").mkdir()
            for i, main in enumerate(mains, 1):
                (folder / "ko" / f"card_{i:02d}.html").write_text(card(main, free), encoding="utf-8")
            return {rule for _, rule, _, _ in design_review.review(folder, "ko")}

    def test_builder_only_plain_set_is_flagged(self):
        rules = self.run_set(['<div class="list"><p>a</p><p>b</p><p>c</p></div>'] * 6, free=False)
        self.assertTrue({"builder-only", "cover-plain", "focal-missing", "visual-thin"} <= rules)

    def test_varied_set_passes(self):
        mains = [
            f'<div class="cv-duo" data-focal><b>15일</b></div>',
            '<div class="krows" data-focal><div>a</div><div>b</div><div>c</div></div>',
            f'<div class="q-art" data-focal>{SVG}</div><div class="q-panel">인용</div>',
            '<div class="q-hero" data-focal>1.5개월</div>',
            f'<div class="ico-rows" data-focal><div>{SVG}음식점 설명 문장</div><div>{SVG}폐기물</div></div>',
            '<div class="bars2" data-focal><div style="width:50%"></div></div>',
            f'<div class="bound"><div>{SVG}상자</div></div>',
        ]
        self.assertEqual(self.run_set(mains), set())

    def test_same_focal_three_in_a_row_and_same_layout(self):
        mains = ['<div class="cv-duo" data-focal><b>1</b></div>'] + ['<div class="hero" data-focal>3개월</div>'] * 4 + ['<div>끝</div>']
        rules = self.run_set(mains)
        self.assertIn("focal-repeat", rules)
        self.assertIn("layout-repeat", rules)

    def test_focal_kinds(self):
        self.assertEqual(design_review.focal_kind(f'<div data-focal>{SVG}</div>'), "picture")
        self.assertEqual(design_review.focal_kind('<b data-focal>2→1개월</b>'), "number")
        self.assertEqual(design_review.focal_kind('<div data-focal><div style="width:40%"></div></div>'), "chart")


if __name__ == "__main__":
    unittest.main()
