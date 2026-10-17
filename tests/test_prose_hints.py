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
            self.assertIn("담당", result)  # Rendered subheading is public copy.

    def test_legacy_distribution_and_im_not_ai_scan_the_same_public_text(self):
        legacy = ROOT / "content" / "TEST-SUSPENSION-V3" / "distribution.md"
        copy = prose_hints.korean_prose(legacy)
        self.assertEqual(copy, prose_hints.im_not_ai_review.korean_copy(legacy))
        self.assertIn("영업정지 사전통지를 받은 사업자라면 과징금 액수부터", copy)
        self.assertIn("영업정지 대신 과징금을 내면 끝일까요?", copy)
        self.assertIn("서울특별시행정심판위원회", copy)
        self.assertNotIn("For business owners in Korea", copy)
        self.assertNotIn("TEST-SUSPENSION-V3-kakao-ko", copy)

    def test_share_rendered_card_labels_but_exclude_internal_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "card-data.ko.json"
            path.write_text(json.dumps({
                "series": "화장품 인허가", "issue": "③", "coverLabel": "구비서류",
                "angle": "내부 기획용 설명",
                "cards": [{"type": "table", "headline": "대조표",
                           "head": ["첫 열 제목", "두 번째 열 제목"],
                           "body": [{"key": "왼쪽 항목", "text": "오른쪽 설명"}],
                           "sourceTrace": {"paragraph": "자료 추적용 설명"}}],
            }, ensure_ascii=False), encoding="utf-8")
            result = prose_hints.korean_prose(path)
            for visible in ("화장품 인허가", "구비서류", "첫 열 제목",
                            "두 번째 열 제목", "왼쪽 항목", "오른쪽 설명"):
                self.assertIn(visible, result)
            for internal in ("내부 기획용 설명", "자료 추적용 설명"):
                self.assertNotIn(internal, result)
            self.assertEqual(result, prose_hints.im_not_ai_review.korean_copy(path))

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

    def test_blog_preflight_uses_current_summary_order_and_does_not_edit(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "blog.md"
            content = "\n".join([
                "화장품 책임판매업 등록, 신청서만 내면 될까요?",
                "브랜드를 준비하고 있습니다.",
                "안녕하세요, 행정사 지상진입니다.",
                "신청서뿐 아니라 품질관리규정과 관리자 자격증빙을 준비해야 합니다.",
                "민수 씨의 회사는 국내 OEM 방식으로 제품을 만듭니다.",
                "무료 사전 검토에 현재 가지고 있는 서류 초안을 보내세요.",
                "3줄 요약",
                "1. 신청서 외에 규정도 준비해야 합니다.",
                "2. 관리자는 법정 자격을 갖춰야 합니다.",
                "3. 행정서류 작성 업무를 위임할 수 있습니다.",
                "#화장품 #책임판매업 #관리규정 #행정사"
            ])
            path.write_text(content, encoding="utf-8")
            with mock.patch("shutil.which", return_value=None), mock.patch("builtins.print") as printed:
                self.assertEqual(prose_hints.main([str(path)]), 0)
            report = printed.call_args[0][0]
            self.assertIn("블로그 발행 전 형식 점검", report)
            self.assertNotIn("summary-before-toc", report)
            self.assertNotIn("cta-not-last", report)
            self.assertNotIn("no-end-summary", report)
            self.assertIn("short-blog", report)
            self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_munche_config_keeps_legal_hedges(self):
        import json
        rules = json.loads((ROOT / ".munche.json").read_text(encoding="utf-8"))["rules"]
        self.assertEqual(rules["KO-POSS-001"], "off")  # '~할 수 있다'를 지우라는 규칙은 끈다


if __name__ == "__main__":
    unittest.main()
