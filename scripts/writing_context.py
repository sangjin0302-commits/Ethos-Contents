#!/usr/bin/env python3
"""Read-only, bounded retrieval of existing ETHOS editing examples. No API calls."""
import argparse
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "writing" / "README.md"
SECTIONS = {
    "opening": ("23-1.", "22-1."),
    "flow": ("21.", "20-2."),
    "polish": ("20-2.", "20-3.", "20-4."),
    "card": ("6.", "10."),
}


def select_examples(purpose, text=None):
    """Return exact sections, including their explanation/protection caveats."""
    text = EXAMPLES.read_text(encoding="utf-8") if text is None else text
    headings = list(re.finditer(r"^(#{2,3}) (.+)$", text, re.M))
    selected = []
    for prefix in SECTIONS[purpose]:
        for i, match in enumerate(headings):
            if match.group(2).startswith(prefix + " "):
                end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
                selected.append({
                    "source": "examples/writing/README.md",
                    "heading": match.group(2),
                    "excerpt": text[match.start():end].strip(),
                })
                break
        else:
            raise ValueError(f"Writing example missing: {prefix}")
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--purpose", choices=SECTIONS, default="polish")
    args = parser.parse_args()
    print("편집 방식 참고용. 예시의 사실·법률 결론은 현재 원고의 근거가 아닙니다.\n")
    for item in select_examples(args.purpose):
        print(item["excerpt"] + "\n")


if __name__ == "__main__":
    main()
