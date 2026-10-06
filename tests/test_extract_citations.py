import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_citations import extract_card_data, extract_text, markdown_table  # noqa: E402


def citations(text):
    return [item["citation"] for item in extract_text(text)]


class ExtractCitationsTests(unittest.TestCase):
    def test_bare_annex_next_to_act_needs_human(self):
        found = citations("「공인중개사법」 제39조와 별표 4의 기준을 봅니다.")
        self.assertIn("「공인중개사법」 제39조", found)
        self.assertTrue(any("별표 4" in c and "확인 필요" in c for c in found))

    def test_law_and_article(self):
        found = citations("「식품위생법」 제82조는 영업정지를 갈음하는 과징금을 둡니다.")
        self.assertEqual(found, ["「식품위생법」 제82조"])

    def test_article_branch_paragraph_and_item(self):
        found = citations("「폐기물관리법」 제28조 제5항과 「행정사법」 제22조제5호, 「게임산업법」 제31조의2제1항")
        self.assertEqual(found, ["「폐기물관리법」 제28조제5항", "「행정사법」 제22조제5호", "「게임산업법」 제31조의2제1항"])

    def test_bare_article_inherits_law_in_same_paragraph_only(self):
        text = "「식품위생법」 제82조는 제75조 또는 제76조에 따른 처분을 말합니다.\n\n제28조는 다른 문단입니다."
        found = citations(text)
        self.assertIn("「식품위생법」 제75조", found)
        self.assertIn("「식품위생법」 제76조", found)
        self.assertIn("제28조 (법령명 불명 · 앞 문단: 「식품위생법」)", found)

    def test_series_title_is_not_a_law(self):
        found = citations("「사업이 멈추는 행정처분」 시리즈의 제2편입니다. 제3조를 봅니다.")
        self.assertEqual(found, ["제3조 (법령명 불명)"])

    def test_same_act_and_decree(self):
        found = citations("「노인장기요양보험법」 제38조제1항 및 같은 법 시행규칙 제30조")
        self.assertEqual(found, ["「노인장기요양보험법」 제38조제1항", "「노인장기요양보험법 시행규칙」 제30조"])

    def test_annex(self):
        found = citations("「식품위생법 시행령」 제53조와 별표 1을 봅니다.\n\n「건설산업기본법」 등록기준은 시행령 별표 6에 있습니다.")
        self.assertIn("「식품위생법 시행령」 별표 1", found)
        self.assertIn("「건설산업기본법 시행령」 별표 6", found)

    def test_case_numbers(self):
        text = ("대법원 2008. 10. 23. 선고 2008도3970 판결을 봅니다.\n\n"
                "대법원 2008도3970은 같은 사건입니다. 2023두12345도 있습니다.\n\n"
                "국가법령정보센터, 2021경기행심1356(2021. 12. 6.)\n\n"
                "서울특별시행정심판위원회 2024-01195, 2024. 9. 23. 재결")
        items = extract_text(text)
        found = [item["citation"] for item in items]
        self.assertIn("대법원 2008. 10. 23. 선고 2008도3970 판결", found)
        self.assertIn("2023두12345", found)
        self.assertIn("2021경기행심1356", found)
        self.assertIn("서울특별시행정심판위원회 2024-01195", found)
        case = next(item for item in items if "2008도3970" in item["citation"])
        self.assertEqual(case["locations"], ["L1", "L3"])
        # 판례 번호의 숫자가 조문·연도로 다시 잡히지 않는다
        self.assertFalse(any("제" in c for c in found))

    def test_dedupe_keeps_all_locations(self):
        text = "「행정심판법」 제51조\n\n「행정심판법」 제51조를 다시 봅니다.\n「행정심판법」 제51조"
        items = extract_text(text)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["locations"], ["L1", "L3", "L4"])

    def test_card_data_scope_is_one_card(self):
        data = {"cards": [
            {"page": 1, "headline": "「게임산업법」 제21조의5 특례", "sourceTrace": {"paragraph": "「민법」 제750조"}},
            {"page": 2, "body": ["제33조의 표시의무"]},
        ]}
        found = [item["citation"] for item in extract_card_data(data)]
        self.assertEqual(found, ["「게임산업법」 제21조의5", "제33조 (법령명 불명 · 앞 문단: 「게임산업법」)"])

    def test_markdown_table_and_cli(self):
        table = markdown_table(extract_text("「행정사법」 제23조"))
        self.assertIn("| 인용 | 위치(line) | 결과 ✓/✗/⚠ | 확인일 |", table)
        self.assertIn("| 「행정사법」 제23조 | L1 |  |  |", table)
        with tempfile.TemporaryDirectory(prefix="ethos-cite-") as tmp:
            path = pathlib.Path(tmp) / "blog.md"
            path.write_text("「행정사법」 제23조와 제21조", encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "extract_citations.py"), str(path), "--json"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            items = json.loads(result.stdout)
            self.assertEqual([item["citation"] for item in items], ["「행정사법」 제23조", "「행정사법」 제21조"])


if __name__ == "__main__":
    unittest.main()
