import pathlib
import sys
import unittest
from urllib.parse import parse_qs, urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tracking_link import tracking_link, tracking_name  # noqa: E402


class TrackingLinkTests(unittest.TestCase):
    def test_link_uses_intake_contract_fields(self):
        url = tracking_link("SUSPENSION-04", "instagram", "ko")
        parsed = urlparse(url)
        self.assertEqual(parsed.path, "/intake")
        query = parse_qs(parsed.query)
        self.assertEqual(query["content_id"], ["SUSPENSION-04"])
        self.assertEqual(query["channel"], ["instagram"])
        self.assertEqual(query["placement"], ["bio-ko"])
        self.assertEqual(query["source"], ["ethos-contents"])
        self.assertNotIn("utm_", url)

    def test_custom_placement_and_name(self):
        url = tracking_link("GAME-KR-06", "linkedin", "en", "story-sticker")
        self.assertIn("placement=story-sticker-en", url)
        self.assertEqual(tracking_name("GAME-KR-06", "linkedin", "en"), "GAME-KR-06-linkedin-en")

    def test_rejects_bad_input(self):
        for args in (("bad id", "instagram", "ko"), ("OK-1", "tiktok", "ko"), ("OK-1", "instagram", "ja")):
            with self.assertRaises(ValueError):
                tracking_link(*args)


if __name__ == "__main__":
    unittest.main()
