#!/usr/bin/env python3
"""Read-only im-not-ai diagnostics for ETHOS PRs.

The pinned upstream shim computes quantitative style signals locally (no LLM).
This adapter only emits non-blocking hints; it never edits or uploads an article.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile

UPSTREAM_COMMIT = "b37e0206d31fffd9149bf57168d4d62eb2086bee"
UPSTREAM_VERSION = "2.3.2"
MAX_CHARS = 200_000
EDITORIAL_INSTRUCTION = re.compile(
    r"(?:적용해서는|옮겨서는|설명해서는|결론내려서는|끝내서는)\s*안\s*됩니다"
)
ABSTRACT_LINK = re.compile(
    r"(?:정하는|확인하는|검토하는|준비하는)\s+일이\s+(?:여기에|이와|그와)\s+연결됩니다"
)


def korean_copy(path: pathlib.Path) -> str:
    """Use only reader-visible Korean from cards or distribution files."""
    text = path.read_text(encoding="utf-8")
    if path.name == "card-data.ko.json":
        data = json.loads(text)
        parts = []
        for card in data.get("cards", []):
            for key in ("headline", "promise", "note", "takeaway"):
                if isinstance(card.get(key), str):
                    parts.append(card[key])
            for item in card.get("body", []):
                s = item.get("text", "") if isinstance(item, dict) else item
                if isinstance(s, str):
                    parts.append(s)
        return "\n".join(parts)
    if path.name == "distribution.md":
        lines, active, parts = text.splitlines(), False, []
        for line in lines:
            if re.fullmatch(r"## Korean[ \t]*", line):
                active = True
                continue
            if active and line.startswith("## "):
                break
            if active and line.strip() and not line.startswith(("#", "### ")):
                parts.append(re.sub(r"https?://\S+", "", line))
        return "\n".join(parts)
    return text


def candidates(text: str, limit: int = 4) -> list[str]:
    """Advisory examples only: real legal prohibitions must be preserved."""
    matches: list[str] = []
    for pattern in (EDITORIAL_INSTRUCTION, ABSTRACT_LINK):
        for match in pattern.finditer(text):
            left = max(text.rfind("\n", 0, match.start()) + 1, match.start() - 65)
            right_nl = text.find("\n", match.end())
            right = min(len(text), match.end() + 65,
                        right_nl if right_nl >= 0 else len(text))
            excerpt = text[left:right].strip()
            if excerpt not in matches:
                matches.append(excerpt.replace(chr(96), "'"))
            if len(matches) >= limit:
                return matches
    return matches


def metrics(upstream: pathlib.Path, text: str) -> tuple[dict | None, str | None]:
    shim = upstream / "scripts" / "prepare_monolith_input.py"
    if not shim.is_file():
        return None, "고정 버전 im-not-ai 실행 파일을 찾지 못했습니다"
    try:
        with tempfile.TemporaryDirectory(prefix="ethos-im-not-ai-") as tmp:
            run_dir = pathlib.Path(tmp)
            (run_dir / "01_input.txt").write_text(text, encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(shim), "--run-dir", str(run_dir),
                 "--genre", "blog", "--no-sanitize"],
                cwd=upstream, capture_output=True, text=True,
                encoding="utf-8", timeout=90, check=False,
            )
            report = run_dir / "00_metrics.json"
            if completed.returncode != 0 or not report.is_file():
                detail = run_dir / "00_metrics.error"
                info = detail.read_text(encoding="utf-8") if detail.is_file() else completed.stderr
                return None, ("상위 진단 실행 실패: " + info.splitlines()[0][:150]) if info.strip() else "상위 진단 결과 없음"
            return json.loads(report.read_text(encoding="utf-8")), None
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        return None, f"상위 진단을 실행하지 못했습니다: {type(error).__name__}"


def review(path: pathlib.Path, upstream: pathlib.Path) -> str:
    if not path.is_file():
        return f"- {path}: 파일을 찾지 못해 건너뜀"
    try:
        text = korean_copy(path)
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        return f"- {path}: 읽기/추출 실패 ({type(error).__name__})"
    if len(text) > MAX_CHARS:
        return f"- {path}: {MAX_CHARS:,}자 초과로 전체 스캔 생략"
    if not re.search(r"[가-힣]", text):
        return f"- {path}: 국문 본문 없음"
    data, issue = metrics(upstream, text)
    lines = [f"**{path}**"]
    if data:
        route = data.get("route_hint") or "미산출"
        band = data.get("risk_band") or "미산출"
        lines.append(f"- 상위 정량 지표: route_hint={route}, risk_band={band} (법률 글 기준의 품질·AI 작성 판정이 아님)")
        v2 = data.get("v2_metrics") or {}
        keys = (
            ("double_passive_count", "중복 피동"),
            ("double_particle_count", "이중 조사"),
            ("have_make_literal_count", "영어식 경동사"),
            ("antithesis_count", "대조 표현"),
        )
        available = [f"{label} {v2[key]}" for key, label in keys if key in v2]
        if available:
            lines.append("- 참고 신호: " + ", ".join(available))
    else:
        lines.append(f"- im-not-ai 정량 검사 미실행: {issue or '원인 미상'}")
    hits = candidates(text)
    if hits:
        lines.append("- 독자용 설명으로 바꿀지 검토할 문구(법률상 실제 금지·주의는 유지):")
        for hit in hits:
            lines.append(f"  - {hit[:150]}")
    else:
        lines.append("- 집필자용 금지형 문구 및 추상 연결 표현의 지정 패턴은 감지되지 않았습니다.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Non-blocking im-not-ai style diagnostics for Korean ETHOS content")
    parser.add_argument("--upstream-root", required=True, type=pathlib.Path)
    parser.add_argument("files", nargs="+", type=pathlib.Path)
    args = parser.parse_args(argv)
    print(f"\n#### im-not-ai v{UPSTREAM_VERSION} 정량 문체 참고 (상위 고정 커밋 {UPSTREAM_COMMIT[:12]})")
    print("자동 윤문·법률 검증·AI 작성 판정이 아닙니다. 다른 스킬/API 호출이나 파일 수정은 수행하지 않습니다.\n")
    for path in args.files:
        print(review(path, args.upstream_root))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
