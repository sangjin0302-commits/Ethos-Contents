#!/usr/bin/env python3
"""카드 디자인·작성 지침 고정(2026-10-07 사용자 결정).

렌더러·CSS·프리셋·게이트·한도·스키마·작성 지침의 지문(sha256)을 state/design-freeze.json에 기록한다.
tests/test_design_freeze.py가 지문을 비교하므로, 이 파일들을 바꾸면 CI가 실패한다.
바꾸려면 사용자가 요청한 변경이어야 하고, 같은 PR에서 이 스크립트로 기록을 갱신하고 CHANGELOG에 이유를 적는다.

    python scripts/design_freeze.py            # 현재 상태와 기록을 비교(바뀐 파일 목록)
    python scripts/design_freeze.py --update   # 사용자가 승인한 변경 뒤에만 기록 갱신

줄바꿈(CRLF/LF) 차이는 무시한다(Windows와 CI가 같은 지문을 얻도록).
"""

import argparse
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECORD = ROOT / "state" / "design-freeze.json"
FROZEN = [
    "templates/base.css",
    "templates/card-types.css",
    "templates/presets/ethos-a.css",
    "templates/annotate.js",
    "scripts/build_cards.py",
    "scripts/auto_design.py",
    "scripts/build_og.py",
    "scripts/qa_render.py",
    "scripts/card_data_fix.py",
    "scripts/tag_rules.py",
    "gates.json",
    "card-limits.json",
    "schema/card-data.schema.json",
    "PROJECT_INSTRUCTIONS.md",
    "docs/card-authoring-spec.md",
    "docs/blog-authoring-spec.md",
    "docs/evidence-gate.md",
    "docs/website-md-spec.md",
]


def fingerprint(path):
    data = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def current():
    return {path: fingerprint(path) for path in FROZEN if (ROOT / path).exists()}


def changed():
    """(바뀐 파일, 기록에 없는 파일, 없어진 파일)."""
    record = json.loads(RECORD.read_text(encoding="utf-8")).get("files", {}) if RECORD.exists() else {}
    now = current()
    diff = sorted(p for p in now if p in record and record[p] != now[p])
    new = sorted(p for p in now if p not in record)
    gone = sorted(p for p in record if p not in now)
    return diff, new, gone


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--update", action="store_true", help="사용자가 승인한 변경 뒤에만 기록을 갱신한다")
    parser.add_argument("--note", default="", help="갱신 이유(기록에 남는다)")
    args = parser.parse_args()
    if args.update:
        old = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.exists() else {}
        history = old.get("history", [])
        if args.note:
            history.append(args.note)
        RECORD.write_text(json.dumps({"frozenOn": old.get("frozenOn", "2026-10-07"), "tag": old.get("tag", "design-freeze-2026-10-07"),
                                      "rule": "이 파일들은 사용자 승인 없이 바꾸지 않는다. 바꾸면 같은 PR에서 --update로 갱신하고 CHANGELOG에 이유를 적는다.",
                                      "files": current(), "history": history}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"updated {RECORD.relative_to(ROOT)} ({len(FROZEN)} files)")
        return 0
    diff, new, gone = changed()
    if not (diff or new or gone):
        print("PASS: 고정된 디자인·지침 파일이 기록과 같습니다")
        return 0
    for label, items in (("바뀜", diff), ("기록 없음", new), ("없어짐", gone)):
        for item in items:
            print(f"FAIL {label}: {item}")
    print("사용자가 요청한 변경이면 python scripts/design_freeze.py --update --note \"이유\" 로 갱신하세요.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
