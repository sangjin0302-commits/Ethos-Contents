import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import auto_design
import build_cards
import ci_render
import ai_polish
import copy_lint
import writing_context
from jsonschema import Draft7Validator


class EditorialRefinementTests(unittest.TestCase):
    def test_ci_renders_changed_design_and_source_without_json_edits(self):
        for path in ("design.css", "ko/card_01.html", "en/card_07.html",
                     "blog.md", "terms.json", "card-data.ko.json"):
            with self.subTest(path=path), patch.object(
                ci_render.subprocess, "run",
                return_value=subprocess.CompletedProcess(
                    [], 0, f"content/COSMETICS-OEM-04/{path}\n", "")
            ):
                self.assertEqual(ci_render.content_ids(SimpleNamespace(ids=None, changed="base")),
                                 ["COSMETICS-OEM-04"])

    def test_ci_ignores_removed_sets_and_non_card_content(self):
        with patch.object(ci_render.subprocess, "run", return_value=subprocess.CompletedProcess(
            [], 0, "content/removed-set/design.css\ncontent/README.md\n", ""
        )):
            self.assertEqual(ci_render.content_ids(SimpleNamespace(ids=None, changed="base")), [])

    def test_bars_preserve_zero_small_and_equal_values_in_both_renderers(self):
        for renderer in (auto_design.bars, build_cards.bar_rows):
            for values, expected in (([0, 1, 100], [0, 1, 100]), ([0, 0], [0, 0]),
                                     ([4, 4], [100, 100]), ([.001, 100], [.001, 100]),
                                     ([1e-12, 2e-12], [50, 100])):
                html = renderer([{"value": v, "display": f"{v}건"} for v in values])
                widths = [float(x) for x in re.findall(r"width:([\d.e+-]+)%", html)]
                self.assertEqual(widths, expected)
            with self.assertRaises(ValueError):
                renderer([{"value": -1}])

    def test_explicit_cover_intent_is_independent_of_issue(self):
        cover = {"hero": {"value": "6", "label": "months"}, "art": ["gavel"]}
        for issue in ("No.01", "No.02", "special"):
            for style, expected in (("stat", "number"), ("art", "picture")):
                self.assertEqual(auto_design.cover_variant(dict(cover, coverStyle=style), {"issue": issue}), expected)
        panel = dict(cover, coverStyle="panel", illustration="custom-panel")
        self.assertEqual(auto_design.cover_variant(panel, {"issue": "No.01"}), "panel")
        with patch.object(auto_design, "illustration_svg", return_value="<svg>chosen-panel</svg>"):
            markup = auto_design.cover_main(dict(panel, headline="Title", body=[]), "en")
            self.assertIn("chosen-panel", markup)
            self.assertNotIn("phosphor/gavel", markup)

    def test_unordered_cards_never_gain_step_numbers_even_when_repeated(self):
        for kind in ("checklist", "concept", "comparison"):
            cards = [{"page": p, "type": kind, "body": ["first item", "second item"]} for p in range(1, 5)]
            plan = auto_design.component_plan({"cards": cards}, "en")
            self.assertNotIn("steps", [v[0] for v in plan.values()])
        body = build_cards.main_markup({"type": "checklist", "body": ["Alpha", "Beta"]}, "en")
        self.assertNotIn(">1</div>", body)
        self.assertIn("•", body)

    def test_production_does_not_shrink_and_preview_limit_matches_qa(self):
        card = {"page": 1, "type": "concept", "bg": "navy", "headline": "Heading", "body": ["text"]}
        data = {"language": "en", "series": "Series", "issue": "No.01", "totalPages": 1, "cards": [card]}
        production = auto_design.build(card, data, production=True)
        preview = auto_design.build(card, data)
        self.assertNotIn("while(over()", production)
        self.assertIn("scale>0.92", preview)
        self.assertNotIn("0.72", preview)

    def test_approved_ci_does_not_block_advisory_design_warnings(self):
        validator = Draft7Validator(json.loads((ROOT / "schema/card-data.schema.json").read_text(encoding="utf-8")))
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(ci_render.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")), \
                 patch.object(ci_render.build_og, "render", return_value={}), \
                 patch.object(ci_render.design_review, "review", return_value=[("warn", "layout-repeat", "repeat", "review")]):
                ok, summary = ci_render.run_id("COSMETICS-OEM-04", pathlib.Path(tmp), validator)
                self.assertTrue(ok, summary)
                self.assertIn("발행 차단 아님", summary)
            with patch.object(ci_render.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "hard QA failure", "")), \
                 patch.object(ci_render.build_og, "render", return_value={}):
                ok, _ = ci_render.run_id("COSMETICS-OEM-04", pathlib.Path(tmp), validator)
                self.assertFalse(ok)

    def test_new_review_metadata_and_legacy_compatibility(self):
        schema = json.loads((ROOT / "schema/card-data.schema.json").read_text(encoding="utf-8"))
        validator = Draft7Validator(schema)
        original = json.loads((ROOT / "content/COSMETICS-OEM-04/card-data.ko.json").read_text(encoding="utf-8"))
        self.assertEqual(list(validator.iter_errors(original)), [])
        new = json.loads(json.dumps(original))
        new["editorialReview"].update(languagePass="pass", languageMethod="manual-equivalent")
        self.assertEqual(list(validator.iter_errors(new)), [])
        del new["editorialReview"]["languageMethod"]
        self.assertTrue(list(validator.iter_errors(new)))
        new["editorialReview"]["languageMethod"] = "manual-equivalent"
        result = ai_polish.apply_changes(new, {"p1.headline": new["cards"][0]["headline"]})
        self.assertEqual(result["editorialReview"]["languagePass"], "pending")
        self.assertNotIn("languageMethod", result["editorialReview"])
        self.assertNotIn("approvedBy", result)

    def test_selected_examples_are_exact_bounded_and_in_actual_request(self):
        source = writing_context.EXAMPLES.read_text(encoding="utf-8")
        for purpose in writing_context.SECTIONS:
            examples = writing_context.select_examples(purpose)
            self.assertLessEqual(len(examples), 3)
            for item in examples:
                self.assertIn(item["excerpt"], source)
        payload = ai_polish.request_payload([{"context": {"channel": "blog"}}])
        self.assertEqual(payload["editingExamples"], writing_context.select_examples("polish"))
        self.assertIn("자동 적용 금지", payload["exampleUse"])

    def test_approval_gate_checks_method_language_and_pending_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = pathlib.Path(tmp)
            for language, method in (("ko", "humanize-korean"), ("en", "english-localization")):
                data = json.loads((ROOT / f"content/COSMETICS-OEM-04/card-data.{language}.json").read_text(encoding="utf-8"))
                data["editorialReview"].update(languagePass="pass", languageMethod=method)
                (folder / f"card-data.{language}.json").write_text(json.dumps(data), encoding="utf-8")
            command = [sys.executable, str(ROOT / "scripts/validate_bilingual.py"), str(folder)]
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            en = folder / "card-data.en.json"
            data = json.loads(en.read_text(encoding="utf-8"))
            for status, method in (("pass", "humanize-korean"), ("pending", "english-localization")):
                data["editorialReview"].update(languagePass=status, languageMethod=method)
                en.write_text(json.dumps(data), encoding="utf-8")
                result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
                self.assertNotEqual(result.returncode, 0, (status, method))

    def test_zero_bar_is_valid_copy_data(self):
        report = copy_lint.Report()
        copy_lint.lint_bars({"cards": [{"page": 2, "layout": "bars", "body": [
            {"value": 0, "display": "0건"}, {"value": 100, "display": "100건"}]}]}, "ko", report)
        self.assertFalse(report.findings)

    def test_typography_only_copy_has_no_blocking_asset_quota(self):
        report = copy_lint.Report()
        cards = [{"page": p, "type": "cover" if p == 1 else "concept"} for p in range(1, 7)]
        copy_lint.lint_visuals({"cards": cards}, "ko", report)
        self.assertTrue(report.findings)
        self.assertTrue(all(f["level"] == "info" for f in report.findings))
        self.assertNotIn("3분의 1", str(report.findings))


if __name__ == "__main__":
    unittest.main()
