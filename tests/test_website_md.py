import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "website-md-realtor"


def run(folder):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_website_md.py"), str(folder)],
                          capture_output=True, text=True, encoding="utf-8")


class WebsiteFaqTests(unittest.TestCase):
    def test_example_faq_passes(self):
        result = run(EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("FAQ", result.stdout)

    def test_bold_or_unpaired_faq_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = pathlib.Path(tmp)
            for name in ("website.ko.md", "website.en.md"):
                shutil.copy(EXAMPLE / name, folder / name)
            ko = folder / "website.ko.md"
            text = ko.read_text(encoding="utf-8")
            text = text.replace("Q. 업무정지 기간은", "**Q.** 업무정지 기간은", 1)
            text = text.replace("A. 기간이 달라질 여지는", "A: 기간이 달라질 여지는", 1)
            ko.write_text(text, encoding="utf-8")
            out = run(folder).stdout
        self.assertIn("굵게·목록 없이", out)
        self.assertIn("'A.'로 시작하지 않아", out)


if __name__ == "__main__":
    unittest.main()
