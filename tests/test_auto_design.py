import json
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import auto_design  # noqa: E402
import copy_lint  # noqa: E402
import design_review  # noqa: E402


def data(cards, language="ko"):
    return {"language": language, "series": "S", "issue": "No.01", "totalPages": len(cards), "cards": cards}


class AutoDesignTest(unittest.TestCase):
    """JSON-only sets get a preset-A draft with a different focal per card; copy stays verbatim."""

    def test_approved_set_copy_is_verbatim_and_focal_varies(self):
        d = json.loads((ROOT / "content" / "TEST-SUSPENSION-V3" / "card-data.ko.json").read_text(encoding="utf-8"))
        kinds = []
        for card in d["cards"]:
            html = auto_design.build(card, d)
            self.assertIsNotNone(html, card["page"])
            self.assertIn('content="free"', html)
            self.assertIn('name="ethos-auto"', html)
            self.assertEqual(copy_lint.copy_lock(card, html), [], card["page"])
            if card["type"] not in ("cover", "cta"):
                kinds.append(design_review.focal_kind(html))
        self.assertGreaterEqual(len(set(kinds)), 4)

    def test_part_choice(self):
        pick = lambda card, lang="ko": auto_design.main_markup(card, lang)  # noqa: E731
        self.assertIn("versus", pick({"type": "concept", "body": [{"key": "과징금", "text": "a"}, {"key": "과태료", "text": "b"}]}))
        self.assertIn("xlist", pick({"type": "checklist", "icon": "ban", "body": ["a", "b"]}))
        self.assertIn("bars2", pick({"type": "checklist", "layout": "bars", "body": [{"key": "a", "text": "", "value": 2, "display": "2개월"}]}))
        self.assertIn("ico-rows", pick({"type": "comparison", "body": [{"key": "a", "text": "b", "icon": "truck"}, {"key": "c", "text": "d", "icon": "store"}]}))
        self.assertIn("krows stack", pick({"type": "concept", "body": [{"key": "자체등급분류사업자", "text": "a"}] * 4}))
        self.assertIn("steps many", pick({"type": "process", "body": list("abcdef")}))
        self.assertIn("tbl2", pick({"type": "table", "head": ["상황", "처리"], "body": [{"key": "a", "text": "b"}]}))
        self.assertIn("vflow", pick({"type": "flow", "body": [{"key": "a", "text": "b", "icon": "store"}, {"key": "c", "text": "d"}]}))
        self.assertIn("bound", pick({"type": "cta", "body": ["직접 준비: 가", "종합 검토: 나"]}))
        self.assertIn("docs", pick({"type": "cta", "body": ["가", "나", "다"]}))
        self.assertIsNone(pick({"type": "cta", "body": list("abcdefg")}))

    def test_cover_uses_object_art_when_available(self):
        cover = {"page": 1, "type": "cover", "bg": "navy", "headline": "h", "body": ["b"], "art": ["gavel"], "takeaway": "t"}
        self.assertIn("phosphor/gavel", auto_design.build(cover, data([cover])))
        cover['art'] = ['cosmetics-oem']
        for language in ('ko', 'en'):
            html = auto_design.build(cover, data([cover], language))
            self.assertIn('data-asset="ethos/cosmetics-oem"', html)
            self.assertEqual(copy_lint.copy_lock(cover, html), [])

    def test_original_cover_asset_requires_its_real_provenance(self):
        import tempfile
        cover = {"page": 1, "type": "cover", "art": ["cosmetics-oem"]}
        with tempfile.TemporaryDirectory() as directory:
            folder = pathlib.Path(directory)
            report = copy_lint.Report()
            copy_lint.lint_assets(folder, {'ko': data([cover])}, report)
            self.assertTrue(report.findings)
            (folder / 'assets.md').write_text('assets/illustrations/objects/cosmetics-oem.svg', encoding='utf-8')
            report = copy_lint.Report()
            copy_lint.lint_assets(folder, {'ko': data([cover])}, report)
            self.assertFalse(report.findings)

    def test_numbered_checklist_and_fit_state_are_explicit(self):
        card = {"page": 1, "type": "checklist", "layout": "numbered", "bg": "navy",
                "headline": "Four checks", "body": ["first", "second", "third", "fourth"], "takeaway": "Done"}
        html = auto_design.build(card, data([card], "en"), production=True)
        self.assertIn('<div class="docs" data-focal>', html)
        self.assertEqual(html.count('class="doc"'), 4)
        self.assertIn("data-fit-overflow", html)
        self.assertNotIn('name="ethos-auto"', html)

    def test_long_concept_copy_stays_in_full_width_rows(self):
        card = {"type": "concept", "body": [
            {"key": "Duty", "text": "A long legal qualification " * 5, "icon": "scale"},
            {"key": "Exception", "text": "Another long legal qualification " * 5, "icon": "file-search"},
        ]}
        self.assertIn("krows", auto_design.main_markup(card, "en"))
        self.assertNotIn("versus", auto_design.main_markup(card, "en"))
        self.assertNotIn("ico-rows", auto_design.main_markup(card, "en"))

    def test_oem_concept_cards_use_same_layout_in_both_languages(self):
        folder = ROOT / "content" / "COSMETICS-OEM-04"
        for language in ("ko", "en"):
            cards = json.loads((folder / f"card-data.{language}.json").read_text(encoding="utf-8"))
            for page in (3, 7):
                card = cards["cards"][page - 1]
                self.assertIn("krows", auto_design.main_markup(card, language, cards), (language, page))

    def test_oem_first_component_matches_across_languages(self):
        folder = ROOT / "content" / "COSMETICS-OEM-04"
        variants = {}
        for language in ("ko", "en"):
            data_set = json.loads((folder / f"card-data.{language}.json").read_text(encoding="utf-8"))
            variants[language] = [re.search(r'<[^>]+class="([^"]+)', auto_design.main_markup(card, language, data_set)).group(1)
                                  for card in data_set["cards"]]
        self.assertEqual(variants["ko"], variants["en"])

    def test_component_plan_breaks_alternation_and_majority_when_options_exist(self):
        cards = []
        for page in range(1, 7):
            cards.append({"page": page, "type": "comparison", "body": [
                {"key": "A", "text": "alpha", "icon": "store"},
                {"key": "B", "text": "beta", "icon": "truck"},
            ]})
        plan = auto_design.component_plan(data(cards), "ko")
        names = [plan[page][0] for page in range(1, 7)]
        self.assertLessEqual(max(names.count(name) for name in set(names)), len(names) / 2)
        self.assertFalse(any(names[i] == names[i - 2] and names[i - 1] == names[i - 3]
                             for i in range(3, len(names))))


if __name__ == "__main__":
    unittest.main()
