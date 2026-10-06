import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import reader_phrases as rp  # noqa: E402


class ReaderPhrasesTests(unittest.TestCase):
    def test_search_console_and_naver_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            gsc = pathlib.Path(tmp) / "Queries.csv"
            gsc.write_text("Top queries,Clicks,Impressions,CTR,Position\n"
                           "공인중개사 업무정지 감경,3,400,0.75%,8\n"
                           "업무정지 6개월 줄어들 수 있나,1,120,0.8%,9\n"
                           "010-1234-5678 상담,1,90,1%,3\n", encoding="utf-8-sig")
            naver = pathlib.Path(tmp) / "naver.csv"
            naver.write_text("검색어,노출수,클릭수\n공인중개사 업무정지 감경,100,2\n에어비앤비 오피스텔 영업신고 방법,300,4\n", encoding="cp949")
            questions = pathlib.Path(tmp) / "q.txt"
            questions.write_text("사전통지 받았는데 의견서 꼭 내야 하나요?\n홍길동 hong@example.com 문의\n", encoding="utf-8")
            rows = rp.read_csv(gsc) + rp.read_csv(naver)
            text = rp.build(rows, questions.read_text(encoding="utf-8").splitlines(), ["Queries.csv"], "2026-10-06")
        self.assertIn("| 공인중개사 업무정지 감경 | 500 | 5 |", text)  # 두 출처 합산
        self.assertIn("- 업무정지 6개월 줄어들 수 있나", text)  # 질문형
        self.assertIn("에어비앤비 오피스텔 영업신고 방법", text)
        self.assertNotIn("010-1234-5678", text)  # 개인정보 줄은 버린다
        self.assertNotIn("hong@example.com", text)
        self.assertIn("사전통지 받았는데 의견서 꼭 내야 하나요?", text)

    def test_missing_query_column_is_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = pathlib.Path(tmp) / "bad.csv"
            bad.write_text("a,b\n1,2\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                rp.read_csv(bad)


if __name__ == "__main__":
    unittest.main()
