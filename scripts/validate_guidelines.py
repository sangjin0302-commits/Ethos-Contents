from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.md"


# 활성 문서에 들어가면 안 되는 것. 보관 문서(archive/)와 콘텐츠 원고(content/)는 검사하지 않는다.
CONTACT_PATTERNS = [
    r"https?://(?:talk\.naver\.com|pf\.kakao\.com|open\.kakao\.com|t\.me)/",
    r"@EthosAdmin",
    r"[A-Za-z0-9._%+-]+@(?:gmail|naver|daum|kakao)\.com",
]
UNSOURCED_STATS = ["Lead Docket", "Epic Attorney Marketing", "Hootsuite", "SaaS Funnel Lab", "월 3,000회"]
RETIRED_RULES = ["모든 글 인라인 CTA 2회", "CTA 3회 상한", "프루프는 모든 글에서 3개소", "매일 전 채널 발행"]
ACTIVE_GLOBS = ["guidelines/**/*.md", "docs/*.md", ".agents/*.md", "README.md", "AGENTS.md", "PROJECT_INSTRUCTIONS.md", "MANIFEST.md"]


def check_active_docs() -> list[str]:
    problems = []
    for pattern in ACTIVE_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(ROOT).as_posix()
            for regex in CONTACT_PATTERNS:
                if re.search(regex, text):
                    problems.append(f"{rel}: 연락처 패턴 {regex}")
            for needle in UNSOURCED_STATS:
                if needle in text:
                    problems.append(f"{rel}: '{needle}'")
            for number, line in enumerate(text.splitlines(), 1):
                # 폐기 사실을 알리는 표·문장(충돌해소표, 폐기 안내)은 허용한다.
                if line.lstrip().startswith("|") or "폐기" in line:
                    continue
                for needle in RETIRED_RULES:
                    if needle in line:
                        problems.append(f"{rel}:{number}: '{needle}'")
    return problems


def check_archive() -> list[str]:
    problems = []
    archive = ROOT / "archive"
    if not archive.is_dir():
        return problems
    for path in sorted(archive.glob("*.md")):
        head = path.read_text(encoding="utf-8")[:400]
        if "보관 문서" not in head:
            problems.append(f"archive/{path.name}: 맨 위에 '보관 문서(비활성)' 경고가 없습니다")
    return problems


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
        "docs/brand-philosophy.md",
        "docs/card-authoring-spec.md",
        "docs/card-selection.md",
        "docs/channel-packaging.md",
        "docs/performance-learning.md",
        "docs/asset-policy.md",
        "docs/language-quality-workflow.md",
        "docs/marketing-checklist.md",
        "docs/tooling-policy.md",
        "docs/social-repurposing.md",
        "docs/ethical-persuasion.md",
        "docs/topic-discovery.md",
        "docs/topic-log-integration.md",
        "guidelines/modules/human-judgment-positioning.md",
        "docs/blog-authoring-spec.md",
        "docs/sns-authoring-spec.md",
        "docs/legal-verification.md",
    }
    omitted = sorted(required - candidates)
    if omitted:
        print("FAIL: 필수 활성 지침이 MANIFEST에 없습니다.")
        for path in omitted:
            print(f"- {path}")
        return 1

    problems = check_active_docs() + check_archive()
    if problems:
        print("FAIL: 활성 문서에 폐기된 규칙·연락처·근거 불명 수치가 남아 있습니다.")
        for line in problems:
            print(f"- {line}")
        return 1

    print(f"PASS: MANIFEST 경로 {len(candidates)}개를 확인했습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
