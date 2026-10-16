import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import prose_hints  # noqa: E402


class ProseHintsTests(unittest.TestCase):
    def test_missing_tools_are_skipped_not_failed(self):
        with mock.patch("shutil.which", return_value=None), mock.patch("builtins.print") as out:
            code = prose_hints.main([str(ROOT / "examples" / "free-design-realtor" / "blog.md")])
        self.assertEqual(code, 0)
        self.assertIn("도구 없음", out.call_args[0][0])

    def test_only_korean_distribution_copy_is_extracted(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "distribution.md"
            path.write_text(
                "# Distribution\n## Korean\n### Caption\n관리규정은 회사 업무에 맞게 써야 합니다.\n"
                "### Hook variants\n1. 무엇부터 확인할까요?\n"
                "## English\n### Caption\nEnglish text that should be skipped.\n"
                "## Tracking\nhttps://example.com/intake\n", encoding="utf-8"
            )
            result = prose_hints.korean_prose(path)
            self.assertIn("관리규정은", result)
            self.assertIn("무엇부터", result)
            self.assertNotIn("English text", result)
            self.assertNotIn("example.com", result)

    def test_only_visible_card_fields_are_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "card-data.ko.json"
            sample = {"cards": [
                {"headline": "서류가 맞는지 확인하세요.", "body": [
                    {"key": "담당", "text": "그 자료를 누가 확인할까요?"},
                    "실제 회사에 맞춰 적어야 합니다."
                ], "takeaway": "신청서부터 확인하세요.", "design": "파란색 네모와 이상한 텍스트"},
            ]}
            path.write_text(json.dumps(sample, ensure_ascii=False), encoding="utf-8")
            result = prose_hints.korean_prose(path)
            self.assertIn("그 자료를 누가 확인할까요?", result)
            self.assertIn("신청서부터 확인하세요.", result)
            self.assertNotIn("파란색 네모", result)
            self.assertNotIn("담당", result)

    def test_temporary_copy_is_deleted_and_original_json_is_not_changed(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "card-data.ko.json"
            original = '{"cards":[{"headline":"자료를 확인하세요.","body":["내용"],"takeaway":"결론"}]}'
            path.write_text(original, encoding="utf-8")
            with mock.patch("shutil.which", return_value=None), mock.patch("builtins.print") as printed:
                self.assertEqual(prose_hints.main([str(path)]), 0)
            self.assertEqual(path.read_text(encoding="utf-8"), original)
            self.assertEqual(list(path.parent.glob("prosehints-*/blog.md")), [])
            self.assertIn("card-data.ko.json", printed.call_args[0][0])

    def test_munche_config_keeps_legal_hedges(self):
        import json
        rules = json.loads((ROOT / ".munche.json").read_text(encoding="utf-8"))["rules"]
        self.assertEqual(rules["KO-POSS-001"], "off")  # '~할 수 있다'를 지우라는 규칙은 끈다


if __name__ == "__main__":
    unittest.main()
