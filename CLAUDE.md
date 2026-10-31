# ETHOS | Claude Code 프로젝트 지침

이 저장소의 콘텐츠·카드 운영 정본은 `MANIFEST.md`와 해당 Active 명세다. 외부 블로그 플러그인이나 이 문서가 정본을 대체하지 않는다.

- 블로그 작업은 `docs/blog-authoring-spec.md`부터 읽고 A/B/C 경로를 선택한다. 새 법률 근거가 필요한 경우 `docs/evidence-gate.md`의 1차 출처 확인·연구 잠금을 따른다.
- 승인된 원문은 Source Lock이다. 블로그→SNS·카드·웹사이트 변환, 번역, SEO 문장 변경 시 법률 조건·숫자·예외·기한·인용·업무 범위를 보존한다. 승인 원고와 카드 고정 시스템을 자동으로 바꾸지 않는다.
- 국문 게시 원고는 `docs/language-quality-workflow.md`에 따라 자연 초안→사실·법률→마케팅→금지 표현→윤문→의미 재검증 순서로 처리한다. `docs/tooling-policy.md`에 따라 외부 품질 점수는 보조 정보다.
- `vendor/claude-blog`는 고정된 MIT Git 서브모듈이다. `docs/claude-blog-integration.md`를 읽고 명시적 요청에 따라 선택형으로만 사용한다. `.claude/skills/ethos-blog/SKILL.md`는 ETHOS 우선 진입점이다.
- `claude --plugin-dir ./vendor/claude-blog`은 서브모듈 초기화 후 로컬 환경에서만 실행할 수 있다. 미초기화·명령 실패·의존성 미설치를 성공으로 표현하지 않는다.
- 비공개 의뢰인 자료를 외부 API·공개 PR로 전송하거나 자동 게시하지 않는다. 새 API 호출·유료 서비스·원본 덮어쓰기는 사전에 명시적 승인을 받는다.
- 카드 제작은 기존 `AGENTS.md`, `docs/card-codex-production.md` 및 고정 렌더 게이트를 따른다.
