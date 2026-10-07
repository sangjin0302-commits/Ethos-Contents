import json
import pathlib
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


if __name__ == "__main__":
    unittest.main()
