"""Document wiring checks, not SEO, legal-accuracy or conversion evaluations."""
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
GUIDE = "docs/search-intent-writing.md"
REVIEW = "docs/reviews/2026-10-31-search-writing-factcheck.md"


class SearchIntentWritingTests(unittest.TestCase):
    def setUp(self):
        self.guide = (ROOT / GUIDE).read_text(encoding="utf-8")

    def test_routes_reference_guide(self):
        for name in ("MANIFEST.md", "AGENTS.md", "CLAUDE.md",
                     ".agents/skills/ethos-editorial/SKILL.md"):
            with self.subTest(path=name):
                self.assertIn(GUIDE, (ROOT / name).read_text(encoding="utf-8"))

    def test_preserves_ethos_boundaries(self):
        for token in ("Source Lock", "Traffic / Authority / Revenue", "적합 문의",
                      "3줄 요약", "리멤버", "개인정보", "Soft Guide"):
            with self.subTest(token=token):
                self.assertIn(token, self.guide)

    def test_separates_evidence_and_measurements(self):
        for token in ("검색 결과 미확인", "타인의 매출", "광고주 CPC",
                      "페이지 RPM", "수동 조치", "보장하지 않는다"):
            with self.subTest(token=token):
                self.assertIn(token, self.guide)

    def test_sources_are_primary_and_numbered(self):
        sources = re.findall(r"^(\d+)\. \[[^\]]+\]\((https://[^)]+)\)$",
                             self.guide, flags=re.MULTILINE)
        self.assertEqual([int(n) for n, _ in sources], list(range(1, 11)))
        allowed = {"developers.google.com", "support.google.com",
                   "searchadvisor.naver.com", "help.naver.com", "help.openai.com"}
        for _, url in sources:
            self.assertIn(urlsplit(url).hostname, allowed)

    def test_review_does_not_certify_anecdote(self):
        review = (ROOT / REVIEW).read_text(encoding="utf-8")
        self.assertIn("진위는 확인되지 않았다", review)
        self.assertIn("원본 캡처는 저장소에 복제하지 않는다", review)
        self.assertIn(REVIEW, self.guide)

    def test_no_new_mandatory_tools(self):
        self.assertIn("새 스킬·필수 보고서·점수표·JSON 필드를 만들지 않는다", self.guide)
        self.assertIn("매번 모든 원고에 검색·경쟁 분석을 강제하지 않는다", self.guide)


if __name__ == "__main__":
    unittest.main()
