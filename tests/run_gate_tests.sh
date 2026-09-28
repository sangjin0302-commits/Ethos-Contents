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
$PY scripts/qa_render.py --html-dir examples/cream-gold --source examples/source/blog-excerpt.md --allow-partial --out /tmp/ethos_qa_cream_gold >/dev/null 2>&1
C=$?
CG=$(grep -c 'gold-text-on-cream' /tmp/ethos_qa_cream_gold/qa-report.md || true)
if [ $C -ne 0 ] && [ "$CG" -ge 3 ]; then
  echo "cream-gold : FAIL (기대대로 — 제목·소제목·본문 골드 텍스트를 잡음)"
else
  echo "cream-gold : PASS 또는 다른 실패 (전용 게이트 문제)"
fi
$PY scripts/qa_render.py --html-dir examples/english-thin --source examples/source/blog-excerpt.md --allow-partial --out /tmp/ethos_qa_english_thin >/dev/null 2>&1
E=$?
if [ $E -ne 0 ] && grep -q 'english-weight<700(headline)' /tmp/ethos_qa_english_thin/qa-report.md; then
  echo "english-thin: FAIL (기대대로 — 얇은 영문 제목을 잡음)"
else
  echo "english-thin: PASS 또는 다른 실패 (전용 게이트 문제)"
fi
[ $G -eq 0 ] && [ $B -ne 0 ] && [ $W -eq 0 ] && [ $C -ne 0 ] && [ "$CG" -ge 3 ] && [ $E -ne 0 ] && grep -q 'english-weight<700(headline)' /tmp/ethos_qa_english_thin/qa-report.md && exit 0 || exit 1
