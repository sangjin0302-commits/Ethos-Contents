# im-not-ai (에토스 고정 버전 연동)

- 원본: https://github.com/epoko77-ai/im-not-ai
- 고정 커밋: `b37e0206d31fffd9149bf57168d4d62eb2086bee` (2026-10-12, v2.3.2)
- 동봉한 규칙집: `skills/humanize-korean/references/quick-rules.md`의 원문을 `quick-rules.md`에 보존
- 라이선스: MIT (`LICENSE` 참조; Copyright (c) 2026 epoko77-ai)

## 사용 범위

1. `scripts/ai_polish.py`는 동봉된 quick-rules를 선택적 Claude API 윤문 제안의 규칙집으로 사용한다. 유료 API는 별도 설정·요청 전 자동 호출하지 않는다.
2. GitHub `Prose hints`는 PR의 국문 발행 문장에 대해 고정 커밋의 `scripts/prepare_monolith_input.py`를 작업 중 임시 체크아웃해 정량 문체 지표만 산출한다. `scripts/im_not_ai_review.py`가 비차단 참고 힌트를 작성한다. 체크아웃 실패 시 검사 미실행으로 남긴다.
3. Codex에서 추가 윤문이 필요하면 저장소 범위 스킬 `.agents/skills/ethos-humanize/SKILL.md`에 따라 고정 커밋을 임시로 가져오고 상위 Codex 공식 `humanize-korean` 전체 경로(진단·윤문·`verify_gates.py`)를 에토스 보호 규칙 아래에서 실행한다.

외부 소스가 업데이트돼도 자동 업그레이드하지 않는다. 업그레이드할 때는 고정 커밋·라이선스·GitHub Actions의 안전성·법률 문장 회귀 테스트를 함께 확인한다. 문체 검사와 의미 검증, 사람이 승인하는 발행을 구별한다.
