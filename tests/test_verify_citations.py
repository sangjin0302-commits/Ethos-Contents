import pathlib
import socket
import sys
import tempfile
import threading
import time
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import verify_citations as vc  # noqa: E402

SAMPLE = """[VERIFIED] == 인용 검증 결과 ==
▶ 법령 인용
✓ 공인중개사법 제39조(업무의 정지) 실존
✓ 공인중개사법 제39조(업무의 정지) 제3항 실존
✗ 행정절차법 제99조 오류
"""

BLOG = "「공인중개사법」 제39조와 같은 법 제39조제3항, 「행정절차법」 제99조, 「공인중개사법 시행규칙」 별표 4를 봅니다.\n"


class ParseTests(unittest.TestCase):
    def test_norm_matches_tool_lines(self):
        self.assertEqual(vc.norm("「공인중개사법」 제39조제3항"), vc.norm("공인중개사법 제39조(업무의 정지) 제3항 실존"))

    def test_table_marks_articles_and_leaves_annex_for_human(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "blog.md"
            path.write_text(BLOG, encoding="utf-8")
            items = vc.extract(path)
        text = vc.table(items, vc.parse_result(SAMPLE), "blog.md", "test", "2026-10-06")
        self.assertIn("| 「공인중개사법」 제39조 | L1 | ✓ |", text)
        self.assertIn("| 「행정절차법」 제99조 | L1 | ✗ |", text)
        self.assertRegex(text, r"별표 4 \| L1 \| ⚠ \|")


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@unittest.skipUnless(__import__("importlib").util.find_spec("mcp"), "mcp SDK 없음")
class FakeServerTests(unittest.TestCase):
    """공식 MCP SDK로 띄운 가짜 서버에 실제 streamable HTTP로 붙어 본다(외부 네트워크 없음)."""

    def test_round_trip_with_fake_server(self):
        from mcp.server.fastmcp import FastMCP

        port = free_port()
        server = FastMCP("fake-law", host="127.0.0.1", port=port, log_level="ERROR")
        seen = {}

        @server.tool()
        def legal_analysis(mode: str, text: str) -> str:
            seen["mode"], seen["text"] = mode, text
            return SAMPLE

        threading.Thread(target=lambda: server.run(transport="streamable-http"), daemon=True).start()
        url = f"http://127.0.0.1:{port}/mcp"
        for _ in range(50):
            try:
                socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
                break
            except OSError:
                time.sleep(0.1)
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "blog.md"
            path.write_text(BLOG, encoding="utf-8")
            results, raw, error = vc.verify(vc.extract(path), url, "test-key")
        self.assertEqual(error, "")
        self.assertEqual(seen["mode"], "verify_citations")
        self.assertIn("「공인중개사법」 제39조", seen["text"])
        self.assertNotIn("별표", seen["text"])  # 별표는 보내지 않는다
        self.assertEqual(results[vc.norm("「공인중개사법」 제39조")][0], "✓")

    def test_unreachable_server_does_not_raise(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "blog.md"
            path.write_text(BLOG, encoding="utf-8")
            results, raw, error = vc.verify(vc.extract(path), f"http://127.0.0.1:{free_port()}/mcp", "")
        self.assertEqual(results, {})
        self.assertTrue(error)


if __name__ == "__main__":
    unittest.main()
