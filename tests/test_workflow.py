import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from marketing_review import density_penalty, review  # noqa: E402
from ci_render import publish_candidate  # noqa: E402


class WorkflowTests(unittest.TestCase):
    def test_publish_candidate_excludes_preview_labels(self):
        self.assertTrue(publish_candidate({"approvedBy": "홍길동 2026-10-18"}))
        self.assertFalse(publish_candidate({"approvedBy": "비교용 초안 — 사용자 승인 전. 발행 금지"}))
        self.assertFalse(publish_candidate({}))

    def test_bilingual_validator(self):
        cards = []
        for page in range(1, 7):
            cards.append({
                "page": page,
                "type": "cover" if page == 1 else "concept",
                "bg": "navy" if page % 2 else "cream",
                "oneMessage": f"message {page}",
                "headline": f"headline {page}",
                "sourceTrace": {"heading": "Source A", "evidence": "F"},
            })
        base = {"contentId": "TEST-01", "series": "Test", "issue": "No.01", "totalPages": 6,
                "angle": "One angle", "canvasProfile": "portrait", "visualFamily": "social-native",
                "cards": cards}
        with tempfile.TemporaryDirectory(prefix="ethos-test-") as tmp:
            folder = pathlib.Path(tmp)
            for language in ("ko", "en"):
                language_pass = "humanize-korean" if language == "ko" else "english-localization"
                editorial_review = {
                    "pipelineVersion": "2.0",
                    "naturalDraft": "pass",
                    "factCheck": "pass",
                    "marketingPass": "pass",
                    "forbiddenExpressionPass": "pass",
                    "languagePass": language_pass,
                    "semanticRecheck": "pass",
                }
                item = dict(base, language=language, editorialReview=editorial_review)
                (folder / f"card-data.{language}.json").write_text(
                    json.dumps(item, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "validate_bilingual.py"), str(folder)],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_marketing_review_is_advisory(self):
        cards = []
        for page in range(1, 7):
            cards.append({
                "page": page,
                "type": "cover" if page == 1 else "concept",
                "headline": f"headline {page}",
                "body": ["body"],
                "takeaway": "takeaway",
                "sourceTrace": {"heading": "Source A", "evidence": "F"},
            })
        with tempfile.TemporaryDirectory(prefix="ethos-test-") as tmp:
            folder = pathlib.Path(tmp)
            for language in ("ko", "en"):
                item = {"language": language, "cards": cards}
                (folder / f"card-data.{language}.json").write_text(
                    json.dumps(item, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "marketing_review.py"), str(folder)],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = (folder / "marketing-report.md").read_text(encoding="utf-8")
            self.assertIn("발행을 막지 않는 편집 보조 지표", report)

    def test_hook_punctuation_does_not_raise_score(self):
        def item(headline):
            cards = [{
                "page": 1,
                "type": "cover",
                "headline": headline,
                "oneMessage": "one",
                "body": ["body"],
                "takeaway": "takeaway",
                "sourceTrace": {"heading": "source", "evidence": "F"},
            }]
            return {
                "language": "ko",
                "marketing": {
                    "targetReader": "reader",
                    "readerQuestion": "question",
                    "coverIntent": "intent",
                    "practicalPayoff": "payoff",
                    "saveValue": "save",
                },
                "cards": cards,
            }

        plain, _ = review(item("같은 내용의 표지"))
        punctuated, _ = review(item("같은 내용의 표지?"))
        self.assertEqual(plain["hook"], punctuated["hook"])

    def test_english_density_warning_reduces_score(self):
        compact_cards = [{"page": page, "headline": "Clear question", "body": ["Short answer."], "takeaway": "Next step."}
                         for page in range(1, 7)]
        dense_copy = "This sentence deliberately repeats enough detail to make a mobile card difficult to scan quickly. " * 8
        dense_cards = [{"page": page, "headline": "A long English headline for a dense card", "body": [dense_copy], "takeaway": dense_copy}
                       for page in range(1, 7)]

        compact_penalty, _ = density_penalty(compact_cards, "en")
        dense_penalty, dense_notes = density_penalty(dense_cards, "en")

        self.assertEqual(compact_penalty, 0)
        self.assertGreater(dense_penalty, 0)
        self.assertTrue(dense_notes)

    def test_distribution_validator_checks_alt_and_assets(self):
        with tempfile.TemporaryDirectory(prefix="ethos-test-") as tmp:
            folder = pathlib.Path(tmp)
            for language in ("ko", "en"):
                (folder / f"card-data.{language}.json").write_text(
                    json.dumps({"totalPages": 2, "cards": [{}, {}]}), encoding="utf-8")
            (folder / "assets.md").write_text(
                "# Asset provenance\n\nEXTERNAL ASSETS: No\n", encoding="utf-8")
            (folder / "distribution.md").write_text(
                "## Korean\n\n### Alt text\n\n1. 첫 카드 설명\n2. 둘째 카드 설명\n\n"
                "## English\n\n### Alt text\n\n1. First card description\n2. Second card description\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "validate_distribution.py"), str(folder)],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_bilingual_validator_blocks_incomplete_editorial_pipeline(self):
        cards = [{
            "page": page,
            "type": "cover" if page == 1 else "concept",
            "bg": "navy" if page % 2 else "cream",
            "oneMessage": f"message {page}",
            "headline": f"headline {page}",
            "sourceTrace": {"heading": "Source A", "evidence": "F"},
        } for page in range(1, 7)]
        base = {
            "contentId": "TEST-02", "series": "Test", "issue": "No.02",
            "totalPages": 6, "angle": "One angle", "canvasProfile": "portrait",
            "visualFamily": "social-native", "cards": cards,
        }
        with tempfile.TemporaryDirectory(prefix="ethos-test-") as tmp:
            folder = pathlib.Path(tmp)
            for language in ("ko", "en"):
                review = {
                    "pipelineVersion": "2.0", "naturalDraft": "pass",
                    "factCheck": "pass", "marketingPass": "pass",
                    "forbiddenExpressionPass": "pass",
                    "languagePass": "pending", "semanticRecheck": "pending",
                }
                item = dict(base, language=language, editorialReview=review)
                (folder / f"card-data.{language}.json").write_text(
                    json.dumps(item, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "validate_bilingual.py"), str(folder)],
                capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("semanticRecheck", result.stdout)


if __name__ == "__main__":
    unittest.main()
