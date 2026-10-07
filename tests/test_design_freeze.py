import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import design_freeze  # noqa: E402


class DesignFreezeTests(unittest.TestCase):
    """2026-10-07 고정: 렌더러·CSS·게이트·지침은 사용자 승인 없이 바뀌면 안 된다(docs: AGENTS.md '디자인 고정')."""

    def test_frozen_files_match_the_record(self):
        diff, new, gone = design_freeze.changed()
        self.assertEqual((diff, new, gone), ([], [], []),
                         "고정 파일이 바뀌었습니다. 사용자가 요청한 변경이면 python scripts/design_freeze.py --update --note \"이유\"로 기록을 갱신하세요.")

    def test_every_frozen_file_exists(self):
        missing = [p for p in design_freeze.FROZEN if not (ROOT / p).exists()]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
