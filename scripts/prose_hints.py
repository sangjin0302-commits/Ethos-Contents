#!/usr/bin/env python3
"""국문 원고 윤문 힌트를 외부 오픈소스 린터 두 개로 모은다(권고, LLM 없음, 실패로 치지 않음).

- MuncheKit(MIT, Node): 번역투·생성형 AI 상투 표현·상투적 서두·맺음말·겹말·모호한 강조·문두 접속어.
  설정은 저장소 `.munche.json`(법률 한정어를 지우라는 KO-POSS-001은 끔).
- ko-mt-lint(MIT, Python, `kolint`): LLM 출력의 활용 오류('했는다')·조사 중복 같은 문법 오류(KO0xx, 휴리스틱 KO007 제외).

도구가 설치돼 있지 않으면 그 도구만 건너뛴다. 설치:
  npm i -g github:ongsi2/munchekit#v0.2.0
  pip install git+https://github.com/eorua8801/ko-mt-lint@9f8ba8464350e37d48bd78d8c9c3a4e8f8fc5cb9

사용: python scripts/prose_hints.py content/<ID>/blog.md [다른 파일 …]
"""
import json
import pathlib
import shutil
import subprocess
import sys

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


def main(argv=None):
    files = [str(pathlib.Path(f)) for f in (argv if argv is not None else sys.argv[1:]) if pathlib.Path(f).is_file()]
    if not files:
        print(__doc__)
        return 2
    out = ["#### 윤문 힌트 (오픈소스 린터, 권고)", ""]
    for name, lines in (("MuncheKit 문체", munche(files)), ("ko-mt-lint 문법", kolint(files))):
        if lines is None:
            out.append(f"- {name}: 도구 없음(건너뜀)")
        elif not lines:
            out.append(f"- {name}: 지적 없음")
        else:
            out.append(f"- {name} {len(lines)}건")
            out += [f"  - {line}" for line in lines]
    out.append("")
    out.append("_사실·숫자·한정어(수 있·이하·또는)는 이 힌트로 바꾸지 않는다._")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
