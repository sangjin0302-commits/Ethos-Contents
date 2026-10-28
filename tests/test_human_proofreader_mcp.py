"""Regression tests for the optional Human Proofreader MCP bridge (no network calls)."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import human_proofreader_mcp as hp


class LocalGateTests(unittest.TestCase):
    def test_identical_text_passes_but_does_not_certify_law(self):
        ok, report = hp.local_compare("제12조에 따라 신청할 수 있습니다.", "제12조에 따라 신청할 수 있습니다.")
        self.assertTrue(ok)
        self.assertIn("사람이 별도로", report)

    def test_removed_number_is_rejected(self):
        ok, report = hp.local_compare("14일 안에 제출합니다.", "안에 제출합니다.")
        self.assertFalse(ok)
        self.assertIn("숫자", report)

    def test_added_number_is_rejected(self):
        ok, report = hp.local_compare("확인합니다.", "3일 안에 확인합니다.")
        self.assertFalse(ok)
        self.assertIn("추가", report)

    def test_quoted_text_must_survive(self):
        ok, report = hp.local_compare('원문은 "허가할 수 있다"입니다.', '원문은 "허가해야 한다"입니다.')
        self.assertFalse(ok)
        self.assertIn("인용", report)

    def test_legal_qualifier_loss_is_rejected(self):
        ok, report = hp.local_compare("A 또는 B는 제출할 수 있습니다.", "A와 B는 제출합니다.")
        self.assertFalse(ok)
        self.assertIn("한정", report)

    def test_large_rewrite_is_rejected(self):
        ok, report = hp.local_compare("안녕하세요. " * 80, "반갑습니다. " * 80)
        self.assertFalse(ok)
        self.assertIn("30%", report)


class McpProtocolTests(unittest.TestCase):
    def test_decode_json(self):
        raw = json.dumps({"jsonrpc": "2.0", "id": 2, "result": {"content": []}}).encode()
        self.assertEqual(hp.parse_reply(raw, "application/json", 2), {"content": []})

    def test_decode_sse(self):
        text = 'event: message\ndata: {"jsonrpc":"2.0","id":2,"result":{"content":[{"type":"text","text":"OK"}]}}\n\n'
        self.assertEqual(
            hp.parse_reply(text.encode(), "text/event-stream", 2)["content"][0]["text"], "OK"
        )

    def test_decode_error(self):
        raw = b'{"jsonrpc":"2.0","id":1,"error":{"code":-32600,"message":"unsupported"}}'
        with self.assertRaises(hp.ProofreaderError):
            hp.parse_reply(raw, "application/json", 1)

    def test_handshake_and_tool_call(self):
        mock_responses = [
            ({"protocolVersion": "2025-06-18"}, "abc123"),
            ({}, None),
            ({"content": [{"type": "text", "text": "검토 결과"}]}, None),
        ]
        with patch.object(hp, "post_rpc", side_effect=mock_responses) as mocked:
            text = hp.call_remote(hp.DEFAULT_URL, "readability", {"text": "초안"})
        self.assertEqual(text, "검토 결과")
        self.assertEqual(mocked.call_count, 3)
        args = mocked.call_args_list
        self.assertEqual(args[0].args[1]["method"], "initialize")
        self.assertEqual(args[1].args[1]["method"], "notifications/initialized")
        self.assertEqual(args[2].args[1]["params"]["name"], "readability")
        self.assertEqual(args[2].args[2]["Mcp-Session-Id"], "abc123")

    def test_insecure_url_is_rejected_before_network(self):
        with patch.object(hp, "post_rpc") as mocked:
            with self.assertRaises(hp.ProofreaderError):
                hp.call_remote("http://example.com/api/mcp", "usage", {})
        mocked.assert_not_called()

    def test_tool_error_is_not_success(self):
        with patch.object(hp, "post_rpc", side_effect=[
            ({"protocolVersion": "2025-06-18"}, None),
            ({}, None),
            ({"isError": True, "content": [{"type": "text", "text": "한도 초과"}]}, None),
        ]):
            with self.assertRaises(hp.ProofreaderError):
                hp.call_remote(hp.DEFAULT_URL, "read_through", {"text": "글"})


class CliSafetyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.original = Path(self.tmp.name) / "before.md"
        self.after = Path(self.tmp.name) / "after.md"
        self.original.write_text("A 또는 B는 신청할 수 있습니다.", encoding="utf-8")
        self.after.write_text("A 또는 B는 신청할 수 있습니다.", encoding="utf-8")

    def invoke(self, *params):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return hp.main(list(params))

    def test_requires_explicit_external_consent(self):
        with patch.object(hp, "call_remote") as remote:
            result = self.invoke("--mode", "readability", "--file", str(self.original))
        self.assertEqual(result, 2)
        remote.assert_not_called()

    def test_local_compare_does_not_contact_service(self):
        with patch.object(hp, "call_remote") as remote:
            result = self.invoke("--mode", "local-compare", "--file", str(self.original),
                                 "--after", str(self.after))
        self.assertEqual(result, 0)
        remote.assert_not_called()

    def test_external_method_can_be_called_explicitly(self):
        with patch.object(hp, "call_remote", return_value="읽기 결과") as remote:
            result = self.invoke("--mode", "readability", "--file", str(self.original),
                                 "--allow-external")
        self.assertEqual(result, 0)
        self.assertEqual(remote.call_args.args[1], "readability")

    def test_source_file_is_never_overwritten(self):
        with patch.object(hp, "call_remote") as remote:
            result = self.invoke("--mode", "local-compare", "--file", str(self.original),
                                 "--after", str(self.after), "--output", str(self.original))
        self.assertEqual(result, 2)
        self.assertEqual(self.original.read_text(encoding="utf-8"), "A 또는 B는 신청할 수 있습니다.")
        remote.assert_not_called()

    def test_remote_compare_is_still_locally_gated(self):
        self.after.write_text("A와 B는 신청합니다.", encoding="utf-8")
        with patch.object(hp, "call_remote", return_value="✅ 서버 판단 OK"):
            result = self.invoke("--mode", "compare", "--file", str(self.original),
                                 "--after", str(self.after), "--allow-external")
        self.assertEqual(result, 2)

    def test_usage_needs_no_draft_or_external_consent(self):
        with patch.object(hp, "call_remote", return_value="남은 한도"):
            result = self.invoke("--mode", "usage")
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
