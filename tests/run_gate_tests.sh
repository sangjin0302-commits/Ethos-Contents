#!/usr/bin/env bash
# 게이트 회귀 테스트: good 예시는 통과, bad 예시는 반드시 실패해야 한다.
set -u
cd "$(dirname "$0")/.."
PY=${PYTHON:-python3}
$PY scripts/qa_render.py --html-dir examples/html --source examples/source/blog-excerpt.md --allow-partial --out /tmp/ethos_qa_good >/dev/null 2>&1
G=$?
$PY scripts/qa_render.py --html-dir examples/bad  --source examples/source/blog-excerpt.md --allow-partial --out /tmp/ethos_qa_bad  >/dev/null 2>&1
B=$?
[ $G -eq 0 ] && echo "good examples: PASS (기대대로)" || echo "good examples: FAIL (게이트 또는 예시 깨짐)"
[ $B -ne 0 ] && echo "bad example : FAIL (기대대로 — 게이트가 위반을 잡음)" || echo "bad example : PASS (게이트가 안 잡음 — 문제)"
$PY -m unittest discover -s tests -p 'test_workflow.py'
W=$?
[ $G -eq 0 ] && [ $B -ne 0 ] && [ $W -eq 0 ] && exit 0 || exit 1
