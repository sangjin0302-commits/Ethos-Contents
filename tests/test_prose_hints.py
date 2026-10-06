import pathlib
import sys
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

    def test_munche_config_keeps_legal_hedges(self):
        import json
        rules = json.loads((ROOT / ".munche.json").read_text(encoding="utf-8"))["rules"]
        self.assertEqual(rules["KO-POSS-001"], "off")  # '~할 수 있다'를 지우라는 규칙은 끈다


if __name__ == "__main__":
    unittest.main()
