import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))
from ci_render import stage_local_assets


class LocalAssetsTest(unittest.TestCase):
    def test_authored_relative_image_survives_staging(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            source, destination = root / 'content', root / 'ci-out'
            image = source / 'assets' / 'nested' / 'document.svg'
            image.parent.mkdir(parents=True)
            image.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"/>')
            html = destination / 'ko' / 'card_01.html'
            html.parent.mkdir(parents=True)
            html.write_text('<img src="../assets/nested/document.svg">')
            stage_local_assets(source, destination)
            self.assertEqual((html.parent / '../assets/nested/document.svg').read_bytes(), image.read_bytes())
            image.write_bytes(b'<svg/>')
            stage_local_assets(source, destination)
            self.assertEqual((destination / 'assets/nested/document.svg').read_bytes(), b'<svg/>')

    def test_no_local_assets_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            stage_local_assets(root / 'content', root / 'ci-out')
            self.assertFalse((root / 'ci-out/assets').exists())
