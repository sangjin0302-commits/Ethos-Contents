---
name: ethos-blog
description: ETHOS 공식 콘텐츠 지침을 최우선으로 적용하며 claude-blog 오픈소스의 블로그 작성·SEO/GEO·조사 스킬을 선택적으로 연결한다. 에토스 블로그 작성, 진단, 개요, 리라이팅, 번역 요청에서 사용한다.
argument-hint: "[write|analyze|seo-check|geo|outline|translate|repurpose] [주제 또는 파일]"
user-invocable: true
---

# ETHOS Blog Router

1. 먼저 저장소의 `docs/blog-authoring-spec.md`를 읽고 원고의 A(재사용), B(공식 근거 신규 조사), C(승인 원문 파생) 경로를 정한다. `MANIFEST.md`와 `CLAUDE.md`의 정본 우선순위를 준수한다.
2. 새 법률 쟁점은 `docs/evidence-gate.md`의 원본·판본·확인일을 대조하고 검증되지 않은 법령·판례·기간·사례·성과를 창작하지 않는다. 후속편은 승인된 `research/`와 관련 이전 회차의 실제 본문을 대조한다.
3. 요청과 구체적인 결함에 필요한 경우에만 `vendor/claude-blog/skills/blog/SKILL.md`와 해당 `blog-*` 스킬을 읽는다. 프로젝트의 `/ethos-blog` 명령은 플러그인 `/blog`와 별개다. 원본 플러그인 명령은 서브모듈 초기화 후 `claude --plugin-dir ./vendor/claude-blog`로 세션 로딩했을 때 사용한다.
4. 원본 스킬의 SEO 제안·리뷰 점수·스키마·일반적 CTA가 ETHOS의 법률·광고·업무범위·문체·채널별 명세와 충돌하면 ETHOS를 우선한다. 5-gate 점수는 법률 검증·발행 승인이 아니다.
5. 승인된 `content/<ID>/blog.md`·카드 파일은 보존한다. 새 초안·분석은 별도 파일에서 수행하고, 명시적 승인 없이 자동 수정·외부 API 호출·게시·비공개 데이터 전송을 하지 않는다.
6. 결과를 내기 전에 ETHOS에서 요구하는 사실·법률 확인, 국문 윤문과 의미 재확인, 채널별 파일 형식(블로그 TXT·MD 등)을 지킨다. 원본 분석 스크립트를 실제 실행하지 않았다면 실행했다고 말하지 않는다.

세부 운영: `docs/claude-blog-integration.md`.
