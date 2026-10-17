"""Regression tests for read-only im-not-ai GitHub diagnostics."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import im_not_ai_review as review


class ImNotAiReviewTests(unittest.TestCase):
    def test_editorial_candidates_and_valid_prohibition(self):
        self.assertTrue(review.candidates("제조업 서류를 그대로 옮겨서는 안 됩니다."))
        self.assertTrue(review.candidates("여기에 연결됩니다." ) == [])
        self.assertFalse(review.candidates("법에서 금지하는 행위를 해서는 안 됩니다."))
        self.assertFalse(review.candidates("책임판매업 구비서류 목록을 확인합니다."))

    def test_extract_only_public_korean_copy(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            distribution = root / "distribution.md"
            distribution.write_text(
                "## English\nKeep this text\n## Korean\n신청서를 보세요.\nhttps://example.com/a\n## Arabic\n비공개 내용",
                encoding="utf-8",
            )
            self.assertEqual(review.korean_copy(distribution).strip(), "신청서를 보세요.")
            cards = root / "card-data.ko.json"
            cards.write_text(json.dumps({
                "angle": "수정 금지 메타", "cards": [{
                    "headline": "표지", "body": [{"text": "실제 본문"}],
                    "sourceTrace": {"paragraph": "비공개 원문"},
                }]
            }, ensure_ascii=False), encoding="utf-8")
            copy = review.korean_copy(cards)
            self.assertIn("실제 본문", copy)
            self.assertNotIn("비공개 원문", copy)
            self.assertNotIn("수정 금지 메타", copy)

    def test_legacy_distribution_includes_pre_korean_public_captions(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "distribution.md"
            original = (
                "# 배포안\n내부 작성 메모는 보이지 않아야 합니다.\n"
                "## 핵심 문구\n핵심 답부터 읽어 보세요.\n"
                "## 네이버 블로그·카카오톡 채널\n네이버 상담 전에 통지서를 살펴보세요.\n"
                "## SNS 캡션\nSNS에서는 적용해서는 안 됩니다 같은 말을 줄입니다.\n"
                "## 받을 자료(확인표) 문구 — 링크 확인 뒤 게시\n"
                "- 국문: 확인표를 내려받아 보세요.\n"
                "- 영문: English content with 한글 메타 should be excluded.\n"
                "## 해시태그\n#비공개관리태그\n"
                "## 상담 접수 추적\n| 언어 | 채널 |\n| ko | 비공개 접수 메모 |\n"
                "https://example.com/intake?utm_source=private\n"
                "## Korean\n### Alt text\n1. 알트 텍스트에서도 서류를 확인하세요.\n"
                "## English\n### Caption\nEnglish paragraph with 한국어 비공개 노트\n"
                "## Arabic\n### Caption\nعربي 한글 메타\n"
                "## Performance log\n검사하지 않을 성과 기록\n"
            )
            path.write_text(original, encoding="utf-8")
            text = review.korean_copy(path)
            for fragment in (
                "핵심 답부터", "네이버 상담", "SNS에서는 적용해서는 안 됩니다",
                "확인표를 내려받아", "알트 텍스트에서도",
            ):
                self.assertIn(fragment, text)
            for excluded in (
                "내부 작성 메모", "English content", "한글 메타",
                "비공개관리태그", "비공개 접수", "example.com",
                "English paragraph", "성과 기록",
            ):
                self.assertNotIn(excluded, text)
            self.assertEqual(original, path.read_text(encoding="utf-8"))

    def test_real_legacy_distribution_has_all_korean_public_sections(self):
        path = pathlib.Path(__file__).resolve().parents[1] / "content" / "TEST-SUSPENSION-V3" / "distribution.md"
        copy = review.korean_copy(path)
        self.assertIn("영업정지를 과징금으로 바꿀 수 있는지는", copy)
        self.assertIn("영업정지 사전통지를 받은 사업자라면", copy)
        self.assertIn("영업정지 대신 과징금을 내면 끝일까요?", copy)
        self.assertIn("서울특별시행정심판위원회", copy)
        self.assertNotIn("For business owners in Korea", copy)
        self.assertNotIn("TEST-SUSPENSION-V3-kakao-ko", copy)
        self.assertNotIn("해시태그", copy)

    def test_card_extraction_includes_rendered_labels_and_excludes_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "card-data.ko.json"
            data = {
                "language": "ko", "series": "화장품 등록 시리즈",
                "issue": "제3편", "coverLabel": "신규등록 서류",
                "angle": "메타 각도 제외",
                "cards": [
                    {
                        "type": "cover", "headline": "표지 핵심",
                        "coverStyle": "stat",
                        "hero": {"value": "15일", "label": "표지 숫자 설명"},
                        "paths": ["국내 OEM", "해외 수입"],
                        "promise": "끝까지 보면 정리됩니다.",
                        "altCover": {"headline": "대안 표지", "promise": "대안 안내",
                                     "design": "디자인 전용 문구"},
                        "body": ["표지 본문"],
                    },
                    {
                        "type": "table", "headline": "신청서 비교",
                        "head": ["첫 번째 열", "두 번째 열"],
                        "body": [
                            {"key": "증명서는 옮겨서는 안 됩니다.",
                             "text": "실제 담당자 자료를 제출합니다."}
                        ],
                        "oneMessage": "비공개 흐름 정보",
                        "sourceTrace": {"heading": "출처 내부메모"},
                    },
                    {
                        "type": "checklist", "layout": "bars",
                        "headline": "과징금 비교",
                        "body": [{"key": "첫 처분", "display": "6개월", "value": 17,
                                  "text": "막대 설명", "icon": "비공개 아이콘"}],
                        "note": "보충 문구",
                        "takeaway": "검토 결론",
                    },
                ],
            }
            original = json.dumps(data, ensure_ascii=False)
            path.write_text(original, encoding="utf-8")
            copy = review.korean_copy(path)
            for visible in (
                "화장품 등록 시리즈", "제3편", "신규등록 서류",
                "표지 숫자 설명", "15일",
                "대안 표지", "대안 안내", "첫 번째 열", "두 번째 열",
                "증명서는 옮겨서는 안 됩니다.", "실제 담당자 자료",
                "첫 처분", "6개월", "막대 설명", "검토 결론",
            ):
                self.assertIn(visible, copy)
            for private in (
                "메타 각도 제외", "디자인 전용 문구", "비공개 흐름 정보",
                "국내 OEM", "해외 수입", "보충 문구",
                "출처 내부메모", "비공개 아이콘", "17",
            ):
                self.assertNotIn(private, copy)
            self.assertIn("옮겨서는 안 됩니다.", review.candidates(copy)[0])
            self.assertEqual(original, path.read_text(encoding="utf-8"))

    def test_cover_number_picture_variants_do_not_lint_hidden_copy(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "card-data.ko.json"
            card = {
                "type": "cover",
                "headline": "영업등록의 핵심",
                "coverStyle": "stat",
                "hero": {"value": "777", "label": "숨은 숫자 안내"},
                "art": ["truck"],
                "paths": ["사진 갈래 첫째", "사진 갈래 둘째"],
                "body": ["공통 리드"],
                "altCover": {"headline": "대안 표지는 별도 게시", "promise": "대안 안내"},
            }
            data = {"series": "행정처분", "issue": "No.02", "cards": [card]}
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            with patch.object(review.auto_design, "cover_variant", return_value="picture"):
                picture = review.korean_copy(path)
            self.assertIn("사진 갈래 첫째", picture)
            self.assertIn("사진 갈래 둘째", picture)
            self.assertNotIn("숨은 숫자 안내", picture)
            self.assertNotIn("777", picture)
            self.assertIn("대안 표지는 별도 게시", picture)
            with patch.object(review.auto_design, "cover_variant", return_value="number"):
                number = review.korean_copy(path)
            self.assertIn("숨은 숫자 안내", number)
            self.assertIn("777", number)
            self.assertNotIn("사진 갈래 첫째", number)
            self.assertNotIn("사진 갈래 둘째", number)
            with patch.object(review.auto_design, "cover_variant", return_value=None):
                fallback = review.korean_copy(path)
            self.assertIn("숨은 숫자 안내", fallback)
            self.assertNotIn("사진 갈래 첫째", fallback)

    def test_rendered_fields_exclude_hidden_keys_and_notes(self):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "card-data.ko.json"
            cards = [
                {"type": "checklist", "layout": "questions",
                 "headline": "질문 카드",
                 "note": "숨은 체크리스트 주석",
                 "body": [{"key": "보이지 않는 질문 키", "text": "실제 질문"}]},
                {"type": "process", "headline": "순서 카드",
                 "body": [{"key": "숨은 단계 키", "text": "실제 단계"}]},
                {"type": "flow", "headline": "담당 업무 흐름",
                 "note": "표시되는 흐름 주석",
                 "body": [{"key": "노출되는 담당 라벨", "text": "담당자 업무"}]},
                {"type": "checklist", "layout": "bars", "headline": "비교",
                 "body": [{"key": "노출되는 항목", "display": "6개월",
                           "value": 7, "text": "막대 설명"}]},
            ]
            path.write_text(json.dumps({"cards": cards}, ensure_ascii=False), encoding="utf-8")
            copy = review.korean_copy(path)
            for shown in ("실제 질문", "실제 단계", "표시되는 흐름 주석",
                          "노출되는 담당 라벨", "노출되는 항목", "6개월"):
                self.assertIn(shown, copy)
            for hidden in ("숨은 체크리스트 주석", "보이지 않는 질문 키",
                           "숨은 단계 키"):
                self.assertNotIn(hidden, copy)

    def test_upstream_metrics_are_read_only_and_labelled_advisory(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            source = root / "blog.md"
            original = "서류를 옮겨서는 안 됩니다. 책임판매업 신청서에 맞춰 준비합니다.\n"
            source.write_text(original, encoding="utf-8")
            upstream = root / "upstream"
            shim = upstream / "scripts" / "prepare_monolith_input.py"
            shim.parent.mkdir(parents=True)
            shim.write_text("# shim stub for mocked subprocess\n", encoding="utf-8")

            def fake_run(args, **kwargs):
                rd = pathlib.Path(args[args.index("--run-dir") + 1])
                self.assertEqual((rd / "01_input.txt").read_text(encoding="utf-8"), original)
                (rd / "00_metrics.json").write_text(json.dumps({
                    "route_hint": "standard", "risk_band": "medium",
                    "v2_metrics": {"double_passive_count": 1, "antithesis_count": 2},
                }), encoding="utf-8")
                return subprocess.CompletedProcess(args, 0, "", "")

            with patch.object(review.subprocess, "run", side_effect=fake_run):
                result = review.review(source, upstream)
            self.assertIn("route_hint=standard", result)
            self.assertIn("대조 표현 2", result)
            self.assertIn("옮겨서는 안 됩니다", result)
            self.assertEqual(source.read_text(encoding="utf-8"), original)

    def test_missing_upstream_is_not_false_pass(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            source = root / "blog.md"
            source.write_text("적용해서는 안 됩니다.", encoding="utf-8")
            result = review.review(source, root / "missing")
            self.assertIn("정량 검사 미실행", result)
            self.assertNotIn("route_hint=light", result)
            self.assertIn("적용해서는 안 됩니다", result)


if __name__ == "__main__":
    unittest.main()
