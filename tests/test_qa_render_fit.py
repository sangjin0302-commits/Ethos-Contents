import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from qa_render import fit_failures  # noqa: E402


def test_fit_threshold_and_remaining_overflow():
    assert fit_failures("1.00", "0") == []
    assert fit_failures("0.92", "0") == []
    assert any("fit-shrink" in x for x in fit_failures("0.88", "0"))
    assert any("fit-overflow" in x for x in fit_failures("1.00", "1"))
