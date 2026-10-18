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

    def test_oem_english_legal_card_keeps_readable_type_without_shrinking(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        page = self.browser.new_page()
        try:
            page.goto((root / 'content/COSMETICS-OEM-04/en/card_07.html').as_uri())
            page.evaluate('document.fonts.ready')
            page.wait_for_function("document.querySelector('.z-main').hasAttribute('data-fit')")
            main = page.locator('.z-main')
            self.assertEqual(main.get_attribute('data-fit'), '1.00')
            self.assertEqual(main.get_attribute('data-fit-overflow'), '0')
            sizes = page.locator('.krow-t').evaluate_all(
                '(nodes) => nodes.map(n => parseFloat(getComputedStyle(n).fontSize))')
            self.assertEqual(len(sizes), 3)
            self.assertTrue(all(size >= 21 for size in sizes), sizes)
            self.assertTrue(main.evaluate('(n) => n.scrollHeight <= n.clientHeight + 1'))
        finally:
            page.close()

    def test_oem_footer_number_and_progress_have_separate_rows(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        page = self.browser.new_page()
        try:
            for lang in ('ko', 'en'):
                for number in range(1, 11):
                    with self.subTest(lang=lang, page=number):
                        page.goto((root / f'content/COSMETICS-OEM-04/{lang}/card_{number:02d}.html').as_uri())
                        page.evaluate('document.fonts.ready')
                        values = page.locator('.pg[data-progress]').evaluate('''n => {
                            const track = n.getBoundingClientRect();
                            const label = getComputedStyle(n, '::before');
                            const fill = getComputedStyle(n, '::after');
                            return {
                                gap: -(parseFloat(label.top) + parseFloat(label.lineHeight)),
                                height: track.height,
                                fillHeight: parseFloat(fill.height),
                                fillBottom: parseFloat(fill.bottom),
                                fraction: parseFloat(fill.width) / track.width,
                                content: label.content
                            };
                        }''')
                        self.assertGreaterEqual(values['gap'], 8)
                        self.assertEqual(values['height'], values['fillHeight'])
                        self.assertEqual(values['fillBottom'], 0)
                        self.assertAlmostEqual(values['fraction'], number / 10, places=2)
                        self.assertIn(f'{number:02d} / 10', values['content'])
        finally:
            page.close()

    def test_oem_editorial_hierarchy_and_legal_groups(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        page = self.browser.new_page()
        try:
            for lang in ('ko', 'en'):
                for number in (1, 2, 6, 7, 10):
                    with self.subTest(lang=lang, page=number):
                        page.goto((root / f'content/COSMETICS-OEM-04/{lang}/card_{number:02d}.html').as_uri())
                        page.evaluate('document.fonts.ready')
                        page.wait_for_function("document.querySelector('.z-main').hasAttribute('data-fit')")
                        self.assertEqual(page.locator('.z-main').get_attribute('data-fit'), '1.00')
                        self.assertEqual(page.locator('.z-main').get_attribute('data-fit-overflow'), '0')
                        if number == 1:
                            self.assertEqual(page.locator('.cv-promise').evaluate('(n) => getComputedStyle(n).borderTopWidth'), '0px')
                            self.assertEqual(page.locator('.take').evaluate('(n) => getComputedStyle(n).backgroundColor'), 'rgba(0, 0, 0, 0)')
                        if number == 2:
                            boxes = page.locator('.ico-row').evaluate_all('(nodes) => nodes.map(n => { const r=n.getBoundingClientRect(); return {x:r.x,y:r.y}; })')
                            self.assertAlmostEqual(boxes[0]['y'], boxes[1]['y'], delta=1)
                            self.assertGreater(boxes[1]['x'], boxes[0]['x'] + 200)
                        if number == 6:
                            self.assertEqual(page.locator('.ico-row').first.evaluate('(n) => getComputedStyle(n).boxShadow'), 'none')
                        if number == 7 and lang == 'en':
                            factors = page.locator('.legal-factor').all_text_contents()
                            self.assertEqual(factors, [
                                'This depends on the design, development and production model,',
                                'quality and safety impact,',
                                'and trade-secret scope in the contract.'
                            ])
                            self.assertTrue(page.locator('.h2').evaluate('(n) => n.scrollWidth <= n.clientWidth + 1'))
                        if number == 10:
                            colors = page.locator('.bound-col').evaluate_all('(nodes) => nodes.map(n => getComputedStyle(n).backgroundColor)')
                            self.assertEqual(colors, ['rgba(0, 0, 0, 0)'] * 2)
                            self.assertNotEqual(page.locator('.take').evaluate('(n) => getComputedStyle(n).backgroundColor'), 'rgba(0, 0, 0, 0)')
        finally:
            page.close()
