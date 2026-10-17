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

import auto_design

UPSTREAM_COMMIT = "b37e0206d31fffd9149bf57168d4d62eb2086bee"
UPSTREAM_VERSION = "2.3.2"
MAX_CHARS = 200_000
EDITORIAL_INSTRUCTION = re.compile(
    r"(?:적용해서는|옮겨서는|설명해서는|결론내려서는|끝내서는)\s*안\s*됩니다"
)
ABSTRACT_LINK = re.compile(
    r"(?:정하는|확인하는|검토하는|준비하는)\s+일이\s+(?:여기에|이와|그와)\s+연결됩니다"
)


# The established distribution template uses "## Korean". Older series put
# publishable Korean captions before that heading; metadata/tracking sections
# must remain excluded even if they contain Hangul.
_LEGACY_PUBLIC_HEADING = re.compile(
    r"^(?:핵심\s*문구|네이버\s*블로그(?:[·/\s]+카카오톡\s*채널)?|"
    r"카카오톡\s*채널|SNS\s*캡션|인스타그램\s*캡션|"
    r"받을\s*자료(?:\([^)]*\))?\s*문구)(?:\s|$|—)",
    re.IGNORECASE,
)


def _append_copy(parts: list[str], value: object) -> None:
    """Add visible text only. Never walk whole JSON (design/trace are private)."""
    if isinstance(value, str) and value.strip():
        parts.append(value.strip())


def _body_key_visible(card: dict, body: list) -> bool:
    """Mirror keyed-content layouts; metadata keys are not public copy."""
    kind = card.get("type")
    if kind in ("cover", "rest", "quote", "process"):
        return False
    if kind == "checklist":
        layout = card.get("layout")
        if layout == "questions":
            return False
        # Auto-design renders unkeyed negative checklists as xlist/steps,
        # both of which use item_text and omit mixed-in keys.
        if not layout and card.get("icon") in auto_design.NEGATIVE_ICONS:
            keyed = bool(body) and all(
                isinstance(x, dict) and x.get("key") for x in body
            )
            if not keyed:
                return False
    if kind == "cta" and len(body) >= 3:
        return False
    return True


def _card_copy(data: dict) -> str:
    """Extract words visible in ETHOS builders, not all editorial JSON.

    auto_design.cover_variant determines the actual picture vs number path.
    An alternate A/B cover is separately publishable copy, so its headline
    and promise remain reviewable even though it is not the primary cover.
    The actual renderer can later fall back after QA; final visual approval
    and legal verification remain separate from these advisory hints.
    """
    parts: list[str] = []
    for key in ("series", "issue", "coverLabel"):
        _append_copy(parts, data.get(key))

    for card in data.get("cards", []):
        kind = card.get("type")
        body = card.get("body", [])
        for key in ("headline", "promise", "takeaway"):
            _append_copy(parts, card.get(key))
        if kind == "flow":
            _append_copy(parts, card.get("note"))
        if kind == "table":
            for title in card.get("head", []):
                _append_copy(parts, title)

        if kind == "cover":
            # The auto-designed cover chooses number for odd issues and
            # picture for even ones when it can render both. A hidden hero
            # or picture-path caption must not produce a language warning.
            variant = auto_design.cover_variant(card, data)
            if variant == "number" or (
                variant is None and card.get("coverStyle") == "stat"
                and card.get("hero")
            ):
                for key in ("value", "label"):
                    _append_copy(parts, card["hero"].get(key))
            elif variant == "picture" and len(card.get("paths") or []) >= 2:
                for label in card["paths"][:4]:
                    _append_copy(parts, label)
            if isinstance(card.get("altCover"), dict):
                for key in ("headline", "promise"):
                    _append_copy(parts, card["altCover"].get(key))

        if kind == "rest" and len(card.get("paths") or []) >= 2:
            for label in card["paths"][:4]:
                _append_copy(parts, label)

        for idx, item in enumerate(body):
            # These card types render only one paragraph; quote renders three.
            if kind in ("cover", "rest") and idx:
                break
            if kind == "quote" and idx >= 3:
                break
            if isinstance(item, dict):
                if _body_key_visible(card, body):
                    _append_copy(parts, item.get("key"))
                if kind == "checklist" and card.get("layout") == "bars":
                    _append_copy(parts, item.get("display"))
                _append_copy(parts, item.get("text"))
            else:
                _append_copy(parts, item)
    return "\n".join(parts)


def _distribution_copy(text: str) -> str:
    """Collect published Korean sections in both legacy and current layouts.

    The older layout has public captions in '핵심 문구', '네이버 블로그·카카오톡
    채널', and 'SNS 캡션' *before* the later '## Korean' alt-text section.
    Never treat a tracking table, English/Arabic section or internal notes
    as publishable copy, even when metadata contains Korean words.
    """
    parts: list[str] = []
    active = False
    in_fence = False
    for line in text.splitlines():
        top_heading = re.match(r"^##\s+(.+?)\s*$", line)
        if top_heading:
            title = top_heading.group(1).strip()
            active = title.casefold() in ("korean", "한국어", "국문") or bool(
                _LEGACY_PUBLIC_HEADING.match(title)
            )
            in_fence = False
            continue

        stripped = line.strip()
        if stripped.startswith((chr(96) * 3, "~" * 3)):
            if active:
                in_fence = not in_fence
            continue
        if not active or in_fence or not stripped:
            continue
        # Section labels, hashtags, statistics tables and links are not prose.
        if stripped.startswith(("#", "|", "http://", "https://", "<")):
            continue
        if re.match(r"^(?:[-*]\s*)?(?:영문|English|아랍어|Arabic)\s*:", stripped, re.I):
            continue
        stripped = re.sub(r"^[-*]\s*(?:국문|한국어)\s*:\s*", "", stripped)
        stripped = re.sub(r"https?://\S+", "", stripped).strip()
        if re.search(r"[가-힣]", stripped):
            parts.append(stripped)
    return "\n".join(parts)


def korean_copy(path: pathlib.Path) -> str:
    """Extract only reader-visible Korean for the supported PR source types."""
    text = path.read_text(encoding="utf-8")
    if path.name == "card-data.ko.json":
        return _card_copy(json.loads(text))
    if path.name == "distribution.md":
        return _distribution_copy(text)
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
