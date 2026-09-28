import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


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
        with tempfile.TemporaryDirectory() as tmp:
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
        with tempfile.TemporaryDirectory() as tmp:
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


if __name__ == "__main__":
    unittest.main()
