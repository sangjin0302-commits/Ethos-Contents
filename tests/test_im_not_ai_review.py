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
