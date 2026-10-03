import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from marketing_review import review  # noqa: E402


class WorkflowTests(unittest.TestCase):
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
                "angle": "One angle", "cards": cards}
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".test-") as tmp:
            folder = pathlib.Path(tmp)
            for language in ("ko", "en"):
                item = dict(base, language=language)
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
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".test-") as tmp:
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


if __name__ == "__main__":
    unittest.main()
