#!/usr/bin/env python3
"""원고의 법령 인용을 korean-law-mcp(MIT)로 대조해 citations.md 표를 채운다.

ChatGPT는 저장소 코드를 실행하지 못하므로, 이 스크립트는 GitHub Actions(`Verify citations`)와
Codex·로컬에서 돌린다. 인용 목록은 extract_citations.py(오프라인)로 뽑고, 조문은 원격 MCP 서버의
`legal_analysis`(mode `verify_citations`)로 대조한다. 별표와 재결번호는 이 도구가 판정하지 않으므로
⚠로 남겨 사람이 확인한다(docs/legal-verification.md 6절).

사용:
  LAW_OC=<법제처 Open API 키> python scripts/verify_citations.py content/<ID>/blog.md
  python scripts/verify_citations.py content/<ID>/blog.md --out content/<ID>/citations.md

키가 없거나 서버에 닿지 못해도 실패로 끝내지 않는다(작성을 막지 않는다). --strict 일 때만 ✗가 있으면 1을 돌려준다.
"""
import argparse
import asyncio
import datetime
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extract_citations import extract  # noqa: E402

DEFAULT_URL = "https://mcp.gomdori.app/law"
BATCH = 15  # 서버 기본 maxCitations
MARKS = {"✓": "✓", "✗": "✗", "⌛": "✗", "⚠": "⚠"}


def norm(text):
    """'「공인중개사법」 제39조제3항'과 '공인중개사법 제39조(업무의 정지) 제3항 실존'을 같은 키로 만든다."""
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"(실존|오류|폐지|확인\s*필요|없음|불일치|미확인).*$", "", text.strip())
    return re.sub(r"[\s「」『』·,]", "", text)


def parse_result(output):
    """도구 출력에서 '✓ 법령 조문 …' 줄을 {키: (표시, 원문 줄)}로 모은다."""
    found = {}
    for line in output.splitlines():
        line = line.strip()
        if line[:1] in MARKS:
            found[norm(line[1:])] = (MARKS[line[:1]], line[1:].strip())
    return found


async def call_tool(url, key, text):
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    headers = {"apikey": key} if key else {}
    async with streamablehttp_client(url, headers=headers, timeout=60) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("legal_analysis", {"mode": "verify_citations", "text": text})
            return "\n".join(getattr(part, "text", "") for part in result.content)


def verify(items, url, key):
    """법령명이 정해진 조문만 보낸다. 반환: ({키: (표시, 줄)}, 원문 출력 목록, 오류 문자열)."""
    targets = [i["citation"] for i in items if i["kind"] == "article" and i["law"]]
    results, raw = {}, []
    for start in range(0, len(targets), BATCH):
        chunk = "\n".join(targets[start:start + BATCH])
        try:
            output = asyncio.run(call_tool(url, key, chunk))
        except Exception as error:  # 네트워크·인증·한도 초과: 작성을 막지 않는다
            return results, raw, f"{type(error).__name__}: {error}"
        raw.append(output)
        results.update(parse_result(output))
    return results, raw, ""


def table(items, results, source, method, today):
    rows = [f"<!-- verify_citations.py {source} | 확인 방법: {method} -->",
            "| 인용 | 위치(line) | 결과 ✓/✗/⚠ | 확인일 | 비고 |", "|---|---|---|---|---|"]
    for item in items:
        where = ", ".join(item["locations"][:6]) + (" …" if len(item["locations"]) > 6 else "")
        mark, note = "", ""
        if item["kind"] == "article" and item["law"]:
            hit = results.get(norm(item["citation"]))
            if hit:
                mark, note = hit[0], hit[1]
            elif results:
                mark, note = "⚠", "도구 결과에 없음(수동 확인)"
        elif item["kind"] == "annex":
            mark, note = "⚠", "별표는 도구가 판정하지 않음(get_annexes 또는 수동)"
        elif not item["law"] and item["kind"] == "article":
            mark, note = "⚠", "법령명 불명(사람이 법령 특정)"
        else:
            mark, note = "⚠", "판례·재결번호는 수동 또는 cite_check"
        rows.append(f"| {item['citation']} | {where} | {mark} | {today if mark in ('✓', '✗') else ''} | {note} |")
    return "\n".join(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path")
    parser.add_argument("--url", default=os.environ.get("LAW_MCP_URL", DEFAULT_URL))
    parser.add_argument("--out", help="citations.md로 저장(없으면 화면 출력)")
    parser.add_argument("--strict", action="store_true", help="✗가 있으면 종료 코드 1")
    args = parser.parse_args(argv)
    path = pathlib.Path(args.path)
    if not path.is_file():
        print(f"파일이 없습니다: {path}", file=sys.stderr)
        return 2
    items = extract(path)
    key = os.environ.get("LAW_OC", "").strip()
    results, _, error = verify(items, args.url, key) if items else ({}, [], "")
    today = datetime.date.today().isoformat()
    method = "korean-law-mcp verify_citations" if results else "자동 대조 실패 — 수동: 국가법령정보센터"
    text = table(items, results, path.as_posix(), method, today)
    if error:
        text += f"\n\n> 자동 대조를 하지 못했습니다({error}). 키(LAW_OC)·네트워크를 확인하거나 국가법령정보센터에서 직접 확인하세요."
    elif not key:
        text += "\n\n> LAW_OC 키 없이 공용 한도로 조회했습니다. 429가 나면 키를 등록하세요."
    if args.out:
        pathlib.Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"저장: {args.out}")
    print(text)
    bad = sum(1 for line in text.splitlines() if "| ✗ |" in line)
    return 1 if args.strict and bad else 0


if __name__ == "__main__":
    sys.exit(main())
