from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.md"


def main() -> int:
    if not MANIFEST.exists():
        print("FAIL: MANIFEST.md가 없습니다.")
        return 1

    text = MANIFEST.read_text(encoding="utf-8")
    candidates = set(re.findall(r"`((?:guidelines|references|docs)/[^`]+\.(?:md|txt))`", text))
    missing = sorted(path for path in candidates if not (ROOT / path).is_file())

    if missing:
        print("FAIL: MANIFEST가 가리키는 파일이 없습니다.")
        for path in missing:
            print(f"- {path}")
        return 1

    required = {
        "guidelines/core/top-level.md",
        "guidelines/core/definitive-style.md",
        "guidelines/channels/blog.md",
        "guidelines/channels/sns.md",
        "guidelines/channels/cardnews.md",
        "docs/card-selection.md",
        "docs/channel-packaging.md",
        "docs/performance-learning.md",
        "docs/asset-policy.md",
        "docs/language-quality-workflow.md",
        "docs/tooling-policy.md",
        "docs/social-repurposing.md",
        "docs/ethical-persuasion.md",
        "docs/topic-discovery.md",
        "docs/topic-log-integration.md",
        "guidelines/modules/human-judgment-positioning.md",
    }
    omitted = sorted(required - candidates)
    if omitted:
        print("FAIL: 필수 활성 지침이 MANIFEST에 없습니다.")
        for path in omitted:
            print(f"- {path}")
        return 1

    print(f"PASS: MANIFEST 경로 {len(candidates)}개를 확인했습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
