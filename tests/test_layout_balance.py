"""Measure actual ink, including inside stretched flex wrappers."""
import os
import pathlib
import sys
import unittest
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))
from qa_render import BALANCE_JS, balance_warnings


class LayoutBalanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(headless=True, executable_path=os.environ.get('CHROMIUM_PATH') or None)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def measure(self, align, intent=''):
        page = self.browser.new_page()
        try:
            page.set_content(f'''<div data-zone="main" data-content-align="{intent}"
              style="height:400px;display:flex;flex-direction:column;justify-content:{align}">
              <div style="font:20px/24px sans-serif">Visible copy</div></div>''')
            return page.evaluate(BALANCE_JS)
        finally:
            page.close()

    def test_center_and_declared_asymmetry_do_not_warn(self):
        centered = self.measure('center')
        self.assertLess(abs(centered['offsetRatio']), .02)
        self.assertEqual(balance_warnings(centered), [])
        self.assertEqual(balance_warnings(self.measure('flex-start', 'top')), [])

    def test_unintended_top_heavy_content_warns(self):
        top = self.measure('flex-start')
        self.assertGreater(top['bottomGap'], 300)
        self.assertTrue(balance_warnings(top))

    def test_full_height_wrapper_does_not_hide_top_heavy_text(self):
        page = self.browser.new_page()
        try:
            page.set_content('''<div data-zone="main" style="height:400px">
              <div style="height:100%;font:20px/24px sans-serif">Visible copy</div></div>''')
            self.assertTrue(balance_warnings(page.evaluate(BALANCE_JS)))
        finally:
            page.close()
