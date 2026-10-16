#!/usr/bin/env python3
"""국문 원고 윤문 힌트를 외부 오픈소스 린터 두 개로 모은다(권고, LLM 없음, 실패로 치지 않음).

- MuncheKit(MIT, Node): 번역투·생성형 AI 상투 표현·상투적 서두·맺음말·겹말·모호한 강조·문두 접속어.
  설정은 저장소 `.munche.json`(법률 한정어를 지우라는 KO-POSS-001은 끔).
- ko-mt-lint(MIT, Python, `kolint`): LLM 출력의 활용 오류('했는다')·조사 중복 같은 문법 오류(KO0xx, 휴리스틱 KO007 제외).

도구가 설치돼 있지 않으면 그 도구만 건너뛴다. 설치:
  npm i -g github:ongsi2/munchekit#v0.2.0
  pip install git+https://github.com/eorua8801/ko-mt-lint@9f8ba8464350e37d48bd78d8c9c3a4e8f8fc5cb9

사용: python scripts/prose_hints.py content/<ID>/blog.md [다른 파일 …]
지원: website.ko.md, card-data.ko.json(카드에 실제로 보이는 문장만), distribution.md(국문 부분만), caption.ko.md.
파일을 고치지 않으며 외부 문체 도구가 없어도 알려진 부자연스러운 문구를 비차단 힌트로 표시한다.
"""
import contextlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

import copy_lint

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIMIT = 15


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=180, cwd=ROOT)
    except Exception as error:
        return subprocess.CompletedProcess(cmd, 1, "", str(error))


def walk(node, out):
    if isinstance(node, dict):
        if "ruleId" in node:
            out.append(node)
        for value in node.values():
            walk(value, out)
    elif isinstance(node, list):
        for value in node:
            walk(value, out)
    return out


def munche(files):
    exe = shutil.which("munche")
    if not exe:
        return None
    result = run([exe, "lint", *files, "--output", "json"])
    if not result.stdout.strip():
        return [f"MuncheKit 실행 오류: {result.stderr.strip()[:200]}"] if result.stderr.strip() else []
    try:
        items = walk(json.loads(result.stdout or "[]"), [])
    except json.JSONDecodeError:
        return [f"MuncheKit 출력을 읽지 못했습니다: {(result.stderr or result.stdout)[:200]}"]
    lines = []
    for item in items[:LIMIT]:
        excerpt = str(item.get("excerpt") or item.get("text") or "").replace("\n", " ")[:50]
        lines.append(f"`{item['ruleId']}` {item.get('message', '')} — “{excerpt}”")
    if len(items) > LIMIT:
        lines.append(f"…외 {len(items) - LIMIT}건")
    return lines


def kolint(files):
    exe = shutil.which("kolint")
    if not exe:
        return None
    result = run([exe, "check", "--select", "KO0", "--ignore", "KO007", "--format", "json", "--exit-level", "never", *files])
    try:
        data = json.loads(result.stdout or "[]")
    except json.JSONDecodeError:
        return [line for line in result.stdout.splitlines() if " KO0" in line][:LIMIT]
    items = data if isinstance(data, list) else walk(data, [])
    return [f"`{i.get('code') or i.get('rule') or i.get('ruleId')}` {pathlib.Path(str(i.get('location', ''))).name}:{i.get('line', '')} {i.get('message', '')}" for i in items[:LIMIT]]


def korean_prose(path):
    """Return extractable Korean copy or None for an already-plain prose file.

    card-data: only reader-visible Korean copy, not design notes or metadata.
    distribution: Korean section only; exclude English and tracking URLs.
    """
    if path.name == "card-data.ko.json":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return ""
        parts = []
        for card in data.get("cards", []):
            for field in ("headline", "promise", "note", "takeaway"):
                text = card.get(field)
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())
            for item in card.get("body", []):
                text = item.get("text", "") if isinstance(item, dict) else item
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())
        return "\n".join(parts)

    if path.name == "distribution.md":
        lines, active, parts = path.read_text(encoding="utf-8").splitlines(), False, []
        for line in lines:
            if re.fullmatch(r"## Korean[ \t]*", line):
                active = True
                continue
            if active and line.startswith("## "):
                break
            if active and line.strip() and not line.startswith(("### ", "#")):
                parts.append(re.sub(r"https?://\S+", "", line))
        return "\n".join(parts)

    return None


def prepare_sources(paths, stack):
    """Temporary, ignored-on-exit blog.md probes match existing MuncheKit globs."""
    derived, inspected = [], []
    for source in paths:
        data = korean_prose(source)
        if data is None:
            derived.append(str(source))
            inspected.append((source, source.read_text(encoding="utf-8")))
            continue
        if not data.strip() or not re.search(r"[가-힣]", data):
            continue
        # No artifact changes are committed. The existing MuncheKit glob
        # content/**/blog.md also accepts this temporary per-source probe.
        folder = pathlib.Path(stack.enter_context(
            tempfile.TemporaryDirectory(dir=source.parent, prefix="prosehints-")
        ))
        probe = folder / "blog.md"
        probe.write_text(data + "\n", encoding="utf-8")
        derived.append(str(probe))
        inspected.append((source, data))
    return derived, inspected


def main(argv=None):
    files = [pathlib.Path(f) for f in (argv if argv is not None else sys.argv[1:]) if pathlib.Path(f).is_file()]
    if not files:
        print(__doc__)
        return 2
    out = ["#### 윤문 힌트 (오픈소스 린터, 권고)", ""]
    with contextlib.ExitStack() as stack:
        probes, inspected = prepare_sources(files, stack)
        out.append("검사 대상: " + ", ".join(str(source) for source, _ in inspected) if inspected else
                   "검사할 국문 본문이 없습니다.")
        out.append("")
        for original, text in inspected:
            for phrase, suggestion in copy_lint.idiomatic_korean_hints(text):
                out.append(f"- 자연스러운 한국어 ({original}): '{phrase}' — {suggestion}")

            if original.name == "blog.md" and "prosehints-" not in str(original):
                report = copy_lint.Report()
                copy_lint.lint_blog(original, report)
                findings = report.findings
                out.append(f"")
                out.append(f"#### 블로그 발행 전 형식 점검 — {original}")
                out.append(f"")
                if not findings:
                    out.append("- 자동으로 찾은 형식 경고는 없습니다. 실제 법률·근거·독자 이해 검토를 대신하지 않습니다.")
                else:
                    for finding in findings[:30]:
                        label = "형식 확인" if finding["level"] == "warn" else "표현 참고"
                        where = finding.get("where", "blog")
                        out.append(f"- **{label}** `{finding['rule']}` ({where}): {finding['message']}")
                        if finding.get("fix"):
                            out.append(f"  - 참고: {finding['fix']}")
                    if len(findings) > 30:
                        out.append(f"- …추가 {len(findings) - 30}건. 필요한 부분만 확인하세요.")
                out.append("")
        if probes:
            for name, lines in (("MuncheKit 문체", munche(probes)), ("ko-mt-lint 문법", kolint(probes))):
                if lines is None:
                    out.append(f"- {name}: 도구 없음(건너뜀)")
                elif not lines:
                    out.append(f"- {name}: 지적 없음")
                else:
                    out.append(f"- {name} {len(lines)}건")
                    out += [f"  - {line}" for line in lines]
    out.append("")
    out.append("_자동 수정하지 않습니다. 원문과 법률상 주체·조건·의무·재량·숫자·한정어를 보존한 뒤 필요한 표현만 고칩니다._")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
