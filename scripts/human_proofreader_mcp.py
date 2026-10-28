#!/usr/bin/env python3
"""Optional, consent-gated client for Solar Human Proofreader's HTTP MCP server.

No dependency on Codex or external Python packages. This script never changes
the source manuscript. The local-compare mode never makes a network request.
"""
from __future__ import annotations

import argparse
from collections import Counter
import difflib
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

DEFAULT_URL = "https://human-proofreader-mcp.toy.x.upstage.ai/api/mcp"
PROTOCOL_VERSION = "2025-06-18"
MAX_REMOTE_CHARS = 20_000
MAX_CHANGE = 0.30
QUOTES = re.compile(r'“[^”\n]*”|‘[^’\n]*’|「[^」\n]*」|『[^』\n]*』|"[^"\n]*"')
NUMBERS = re.compile(r"(?<!\d)[+\-−]?\d+(?:[.,]\d+)*(?:%|퍼센트)?")
URLS = re.compile(r"https?://[^\s)>]+")
# Conservative alerts only. Matching counts does NOT prove legal equivalence.
QUALIFIERS = (
    "수 있", "수 없", "하여야", "해야",
    "이하", "이상", "미만", "초과", "또는", "다만", "제외", "면제",
    "한하여", "원칙적으로", "금지", "허용",
)


class ProofreaderError(Exception):
    """A clear, non-secret-bearing error for the command-line client."""


def local_compare(before: str, after: str) -> tuple[bool, str]:
    """Reject obvious ETHOS fact/qualifier drift; never certify legal accuracy."""
    problems = []
    for label, pattern in (
        ("숫자·기한·금액", NUMBERS),
        ("직접 인용", QUOTES),
        ("URL", URLS),
    ):
        original = Counter(pattern.findall(before))
        updated = Counter(pattern.findall(after))
        if original != updated:
            removed = list((original - updated).elements())[:5]
            added = list((updated - original).elements())[:5]
            problems.append(f"{label} 변화: 삭제 {removed!r} / 추가 {added!r}")

    altered = [q for q in QUALIFIERS if before.count(q) != after.count(q)]
    if altered:
        problems.append("법률 한정 표현의 빈도 변화: " + ", ".join(altered))

    change = 1 - difflib.SequenceMatcher(None, before, after).ratio()
    if change > MAX_CHANGE:
        problems.append(f"문자 변경률 {change:.1%} > ETHOS 기준 {MAX_CHANGE:.0%}")

    headline = f"ETHOS 로컬 대조: 변경률 {change:.1%}"
    if problems:
        return False, headline + "\n채택 보류:\n- " + "\n- ".join(problems) + (
            "\n코드의 오탐 가능성을 확인하되, 법률상 주체·조건·의무/재량·예외·"
            "업무범위를 원문과 직접 대조해야 합니다."
        )
    return True, headline + (
        "\n기계적으로 잡히는 변화는 없습니다. 법률상 주체·조건·의무/재량·"
        "예외·서비스 범위는 사람이 별도로 재확인해야 합니다."
    )


def parse_reply(body: bytes, content_type: str, expected_id: int) -> dict:
    """Handle both JSON and MCP Streamable HTTP SSE replies."""
    raw = body.decode("utf-8-sig")
    replies: list[dict] = []
    if "text/event-stream" in content_type:
        for frame in raw.replace("\r\n", "\n").split("\n\n"):
            data = "\n".join(
                line[5:].lstrip() for line in frame.splitlines() if line.startswith("data:")
            )
            if data and data != "[DONE]":
                try:
                    candidate = json.loads(data)
                except json.JSONDecodeError:
                    continue
                if isinstance(candidate, dict):
                    replies.append(candidate)
    else:
        try:
            candidate = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ProofreaderError("MCP 서버의 응답이 유효한 JSON이 아닙니다.") from exc
        if isinstance(candidate, dict):
            replies.append(candidate)

    for payload in replies:
        if payload.get("id") != expected_id:
            continue
        if payload.get("error"):
            message = payload["error"].get("message", "요청 실패")
            raise ProofreaderError(f"MCP 오류: {message}")
        result = payload.get("result")
        if isinstance(result, dict):
            return result
    raise ProofreaderError("MCP 서버에서 해당 요청에 대한 응답을 받지 못했습니다.")


def post_rpc(url: str, payload: dict, headers: dict, expected_id: int | None) -> tuple[dict, str | None]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(url, data=data, method="POST", headers=headers)
    try:
        with urlopen(request, timeout=240) as response:
            body = response.read()
            session_id = response.headers.get("Mcp-Session-Id")
            content_type = response.headers.get("Content-Type", "")
    except HTTPError as exc:
        # Do not echo response bodies; they could include submitted text or keys.
        raise ProofreaderError(f"MCP HTTP 오류 {exc.code}") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise ProofreaderError(f"MCP 연결 실패: {type(exc).__name__}") from exc
    if expected_id is None:
        return {}, session_id
    return parse_reply(body, content_type, expected_id), session_id


def call_remote(url: str, tool: str, arguments: dict) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ProofreaderError("원격 MCP 주소는 사용자정보 없는 HTTPS URL이어야 합니다.")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": PROTOCOL_VERSION,
    }
    if os.environ.get("ETHOS_UPSTAGE_API_KEY"):
        headers["X-Upstage-Api-Key"] = os.environ["ETHOS_UPSTAGE_API_KEY"]
    elif os.environ.get("ETHOS_OPENROUTER_API_KEY"):
        headers["X-OpenRouter-Api-Key"] = os.environ["ETHOS_OPENROUTER_API_KEY"]

    handshake = {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "ethos-human-proofreader", "version": "1.0.0"},
        },
    }
    initialized, session = post_rpc(url, handshake, headers, 1)
    headers["MCP-Protocol-Version"] = initialized.get("protocolVersion", PROTOCOL_VERSION)
    if session:
        headers["Mcp-Session-Id"] = session
    post_rpc(url, {"jsonrpc": "2.0", "method": "notifications/initialized"}, headers, None)
    reply, _ = post_rpc(
        url,
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
         "params": {"name": tool, "arguments": arguments}},
        headers,
        2,
    )
    if reply.get("isError"):
        raise ProofreaderError(
            "서버 도구 오류: " +
            " ".join(item.get("text", "") for item in reply.get("content", [])
                     if item.get("type") == "text")[:300]
        )
    parts = [
        item["text"] for item in reply.get("content", [])
        if item.get("type") == "text" and isinstance(item.get("text"), str)
    ]
    if not parts:
        raise ProofreaderError("MCP 서버가 텍스트 결과를 반환하지 않았습니다.")
    return "\n\n".join(parts)


def extract_polished(report: str) -> str:
    """Extract a proposed manuscript from the upstream report, or fail closed.

    The vendor currently emits a '## 교정본' section ending in a horizontal
    rule. Never infer success if that format changes.
    """
    marker = "\n## 교정본\n\n"
    separator = "\n\n---\n"
    if marker not in report:
        raise ProofreaderError("서버 보고서에서 교정본 구역을 찾지 못했습니다. 자동 채택 금지.")
    section = report.split(marker, 1)[1]
    if separator not in section:
        raise ProofreaderError("서버 보고서의 교정본 구분자가 없습니다. 자동 채택 금지.")
    polished = section.rsplit(separator, 1)[0].strip()
    if not polished:
        raise ProofreaderError("서버가 빈 교정본을 반환했습니다. 자동 채택 금지.")
    return polished


def remote_review_gate(report: str, mode: str) -> tuple[bool, str]:
    """Honor the upstream veto; missing/ambiguous verdicts fail closed.

    For proofread, inspect only the report footer, not manuscript content.
    A recognized non-abort verdict is still not publication approval.
    """
    metadata = report.rsplit("\n\n---\n", 1)[-1] if mode == "proofread" else report
    verdicts = re.findall(r"(?m)^([✅⚠⛔])\ufe0f? \*\*원고 대조 — [^\n]+\*\*\s*$", metadata)
    if len(verdicts) != 1:
        return False, "외부 대조 판정을 확인하지 못해 채택을 보류합니다. 서버 보고서 형식을 확인하세요."
    if verdicts[0] == "⛔" or report.startswith("⛔ **이 교정본은 채택하지 마세요"):
        return False, "외부 교정기가 채택 불가로 판정했습니다. 로컬 대조 결과와 무관하게 채택을 보류합니다."
    if verdicts[0] == "⚠":
        return True, "외부 대조에 경고가 있습니다. 경고의 이유와 법률 의미를 직접 확인해야 합니다."
    return True, "외부 대조에 중단 판정은 없습니다. 발행 승인이나 법률 의미 검증 완료를 뜻하지 않습니다."


def read_source(value: str | None, arg_name: str) -> tuple[Path, str]:
    if not value:
        raise ProofreaderError(f"{arg_name} 경로가 필요합니다.")
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise ProofreaderError(f"파일이 없습니다: {value}")
    return path, path.read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=(
        "readability", "read_through", "proofread", "compare",
        "suggest", "usage", "local-compare"), required=True)
    parser.add_argument("--file", help="UTF-8 원본 파일 (업로드 시 전문이 외부로 전송됨)")
    parser.add_argument("--after", help="compare/local-compare에서 비교할 UTF-8 교정본")
    parser.add_argument("--allow-external", action="store_true",
                        help="비공개·개인정보가 없는 원고라는 점을 확인한 후 외부 전송 승인")
    parser.add_argument("--output", help="보고서를 새 파일로 저장 (기존 파일 덮어쓰기 금지)")
    parser.add_argument("--genre", default="블로그",
                        choices=("칼럼", "리포트", "블로그", "뉴스레터", "공적", "에세이", "자동"))
    parser.add_argument("--strength", choices=("보수", "기본", "적극"), default="보수")
    parser.add_argument("--depth", choices=("light", "standard", "deep", "auto"), default="standard")
    parser.add_argument("--audience", default="한국어 비전문가 독자")
    parser.add_argument("--instructions", default="")
    parser.add_argument("--preserve", action="append", default=[], help="원형 보존 문장 (반복 가능)")
    parser.add_argument("--context", default="", help="suggest 앞뒤 문맥")
    parser.add_argument("--count", type=int, choices=(2, 3, 4, 5), default=3)
    args = parser.parse_args(argv)

    try:
        paths: list[Path] = []
        original = ""
        if args.mode != "usage":
            src, original = read_source(args.file, "--file")
            paths.append(src)
        after = ""
        if args.mode in ("compare", "local-compare"):
            dst, after = read_source(args.after, "--after")
            paths.append(dst)

        if args.output:
            destination = Path(args.output).expanduser().resolve()
            if destination in paths or destination.exists():
                raise ProofreaderError("보고서 경로가 원본/교정본 또는 기존 파일과 겹쳐 저장하지 않았습니다.")

        if args.mode == "local-compare":
            accepted, report = local_compare(original, after)
            exit_code = 0 if accepted else 2
        else:
            if args.mode != "usage" and not args.allow_external:
                raise ProofreaderError(
                    "외부 전송을 차단했습니다. 민감정보·비공개 원고가 없는지 확인한 뒤 "
                    "--allow-external을 명시하세요."
                )
            if len(original) > MAX_REMOTE_CHARS and args.mode not in ("compare", "readability"):
                raise ProofreaderError(f"원고가 {MAX_REMOTE_CHARS:,}자를 넘습니다. 절 단위로 나누세요.")
            if args.mode == "suggest" and len(original) > 2_000:
                raise ProofreaderError("suggest는 2,000자 이하여야 합니다.")
            arguments: dict = {}
            if args.mode in ("readability", "read_through", "proofread", "suggest"):
                arguments["text"] = original
            if args.mode in ("read_through", "proofread"):
                arguments["genre"] = args.genre
            if args.mode == "proofread":
                arguments.update(strength=args.strength, depth=args.depth,
                                 audience=args.audience, instructions=args.instructions,
                                 preserve=args.preserve)
            if args.mode == "suggest":
                arguments.update(context=args.context, count=args.count)
            if args.mode == "compare":
                arguments.update(before=original, after=after, preserve=args.preserve)
            url = os.environ.get("ETHOS_PROOFREADER_MCP_URL", DEFAULT_URL)
            report = call_remote(url, args.mode, arguments)
            exit_code = 0
            if args.mode in ("proofread", "compare"):
                proposed = extract_polished(report) if args.mode == "proofread" else after
                accepted, local_report = local_compare(original, proposed)
                remote_ok, remote_note = remote_review_gate(report, args.mode)
                report += "\n\n---\n\n" + remote_note + "\n\n" + local_report
                exit_code = 0 if accepted and remote_ok else 2

        if args.output:
            # Exclusive creation also protects files created during the network call.
            with destination.open("x", encoding="utf-8") as handle:
                handle.write(report + "\n")
            print(f"보고서 작성: {destination}")
        else:
            print(report)
        return exit_code
    except (ProofreaderError, UnicodeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
