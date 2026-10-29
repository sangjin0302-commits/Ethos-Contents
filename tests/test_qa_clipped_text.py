import pathlib
import sys
import unittest

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from qa_render import JS  # noqa: E402


class ClippedTextTest(unittest.TestCase):
    def test_nested_hidden_panel_is_reported(self):
        html = '''<html><body style="margin:0"><div class="card" style="width:540px;height:675px">
        <div data-zone="main"><div class="panel" style="height:20px;overflow:hidden;line-height:20px">
        First line<br>Second line</div></div></div></body></html>'''
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 540, "height": 675})
            page.set_content(html)
            report = page.evaluate(JS)
            browser.close()
        self.assertIn("clipped-text:panel", report["problems"])


if __name__ == "__main__":
    unittest.main()
