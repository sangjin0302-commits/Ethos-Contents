# ETHOS 콘텐츠 운영 라우터 (Codex용)

이 저장소는 블로그·비블로그 SNS·웹사이트·카드뉴스 지침의 단일 기준본이다. **작업 유형을 고르고 아래 표의 파일만 읽는다.** 표에 없는 문서, 과거 버전, `archive/`, `CHANGELOG.md`는 사용자가 요청하거나 충돌이 의심될 때만 연다. 필요한 파일은 한 번에 함께 읽는다.

## 작업 라우팅

| 작업 | 읽을 파일 (순서대로) |
|---|---|
| Claude Blog 스킬 사용(명시 요청 또는 보조 진단) | `docs/blog-authoring-spec.md` → `docs/claude-blog-integration.md` → 필요한 `vendor/claude-blog/skills/` 파일만 확인. ETHOS 규칙과 Source Lock이 우선이며 외부 API·자동 발행은 승인 없이 실행하지 않음 |
| 카드뉴스 제작(ChatGPT 초안 → 완성·렌더) | `docs/card-codex-production.md`, `docs/card-authoring-spec.md`, 해당 `content/<ID>/`의 `brief.md`·`card-data.*.json`·`blog.md`. HTML 단계에서 `docs/card-design-guide.md` |
| 블로그·홈페이지 Editorial Master | `docs/blog-authoring-spec.md`(+ 새 법률 주제면 `docs/evidence-gate.md`, 있으면 `research/<시리즈>.md`). 승인 요청 전 `python scripts/verify_citations.py <원고> --out content/<ID>/citations.md`(키 `LAW_OC`), ⚠는 `docs/legal-verification.md` 6절로 사람 확인 |
| 블로그·국문 파생물 문체 개선(독자에게 어색한 어투, AI 티, humanize 요청) | 채널 명세와 실제 원고를 먼저 읽고 `.agents/skills/ethos-humanize/SKILL.md`의 ETHOS 보호 조건을 적용. 필요할 때 고정된 im-not-ai 전체 진단·윤문·검증 실행. 원문 승인 보호 |
| 사용자가 Solar 실제 실행을 요청 | `docs/human-proofreader-integration.md` → 실제 입력·공개 저장/외부 처리 동의 확인 → 요청 브랜치 제출 → 결과 파일 회수·대조. 컨테이너 DNS나 workflow_dispatch 부재만으로 사용자에게 실행을 넘기지 않는다 |
| 비블로그 SNS | `docs/sns-authoring-spec.md` |
| 웹사이트 변환 | `docs/website-md-spec.md`(국·영문 MD 두 파일) → 승인된 원문과 정합성 확인 → `python scripts/validate_website_md.py content/<ID>` |
| 소재 발굴·콘텐츠 캘린더 | `docs/strategy-playbook.md`, `docs/topic-discovery.md`, 최신 글감관리표가 있으면 `docs/topic-log-integration.md` |
| 고객 언어 분석·내부링크 허브·상담준비 자료 | `docs/topic-log-integration.md` "고객 언어 환류", `docs/content-architecture-system.md` "허브·스포크 내부링크", `docs/strategy-playbook.md` "문의 후 상담준비 자료" |
| 마케팅·성과 분석 | 글감관리표 주간 성과 탭, `docs/topic-log-integration.md` "마케팅 점검", `docs/performance-learning.md` |
| AI 시대 인간 전문성·신규 전문가·자격 결합 포지셔닝 | `.agents/product-marketing.md`, `guidelines/modules/new-expert.md`, `guidelines/modules/human-judgment-positioning.md` |
| 지침 수정·충돌 | `MANIFEST.md`의 Active 파일 확인 → 충돌 검사 → 해당 파일 수정 → `CHANGELOG.md` 갱신 → `python scripts/validate_guidelines.py` |

각 명세가 상위 지침(`guidelines/core/`, `guidelines/channels/`)의 요약이다. 명세로 해결되지 않는 세부나 충돌이 있을 때만 원문을 연다. 우선순위는 현재 사용자 요청 → `MANIFEST.md` → 명세 순이다.

새 글·후속편·새 시리즈·수정본과 파생 콘텐츠는 각 빠른 명세의 칼럼형 설명·법률 조건·실제 맡길 작업과 다음 행동을 함께 적용한다. 국문·영문·아랍어의 표현을 현지화해도 근거와 서비스 범위는 같게 유지한다. 조건형 예시와 매체별 적용 확인은 `examples/writing/cross-channel-three-pillars-20261016.md`를 참고하며, 이 검증 샘플을 승인·발행 원문으로 취급하지 않는다.

공통 작성 원칙의 정본은 `docs/brand-philosophy.md`, 근거 선택·검증은 `docs/evidence-gate.md`, 실행 순서·윤문은 `docs/language-quality-workflow.md`다. 각 빠른 명세는 실제 근거를 초안 전에 검토하고 질문·쉬운 설명·의뢰 판단을 연결하도록 요약한다. 파생·번역은 승인 원문의 근거·조건·사례·서비스 범위를 보존한다. 새 근거·장면은 원문 보강·검증·승인 후 사용한다.

## 공통 고정 원칙 (모든 작업)

- 원문·1차 자료에 없는 사실·숫자·조문·판례·경험·후기·성과를 만들지 않는다. 숫자·조문·한정어(수 있·이하·또는)는 원문 그대로.
- 확인된 사실은 단정하고, 조건·재량·추론만 한정한다. 근거 없는 양시론으로 결론을 피하지 않는다.
- 서술 본문·카드에 연락처·URL·버튼 금지. 마지막은 주제에 맞는 무료 검토 안내. 네이버 하단 기존 상담 이미지 4개 예외와 별도 링크설정 메모는 `docs/blog-authoring-spec.md` 6-1절을 따른다.
- 이력 과장·"최고/대표/leading" 금지. 영문에서 행정사는 항상 Administrative Attorney.
- 게시용 국문은 `자연 초안 → 사실·법률 → 마케팅 → 금지 표현 → 윤문 → 의미 재검증` 순서(`docs/language-quality-workflow.md`). 초안부터 모든 규칙을 동시에 맞추지 않는다.
- 국문 원고가 GitHub PR에 올라오면 `Prose hints`가 `im-not-ai` 고정 버전의 정량 문체 진단을 참고용으로 출력한다. 실제 윤문 요청은 `.agents/skills/ethos-humanize/SKILL.md`에 따라 임시 체크아웃한 upstream 전체 경로를 쓴다. 정량 진단을 AI 검증·법률 검증으로 오해하지 않는다.
- 선택적 Human Proofreader MCP는 문단 흐름의 추가 진단이나 사용자 요청 시에만 사용한다(`docs/human-proofreader-integration.md`). 기존 경로를 대체하지 않는다. 외부 전송은 공개 가능 원고에 명시적 동의가 있을 때만 하며 원본을 덮어쓰지 않는다. Codex 없이도 독립 CLI·수동 GitHub Action·명시적 요청 브랜치로 실행할 수 있다. 채팅에서 실행까지 맡긴 경우 실제 원고를 지정하고 교정본·대조 보고서를 회수해야 하며 고정 테스트 재실행으로 대체하지 않는다.
- 기존 카드뉴스 제작 시스템(`gates.json`, `brand/`, `fonts/`, `templates/`, `scripts/qa_render.py`)을 임의로 옮기거나 완화하지 않는다.

## 디자인 고정 (2026-10-07, 태그 `design-freeze-2026-10-07`)

카드 렌더러·CSS·프리셋·게이트·한도·스키마와 작성 지침(`PROJECT_INSTRUCTIONS.md`, 카드·블로그·웹사이트 명세, `docs/evidence-gate.md`)은 사용자 결정으로 고정됐다. 목록과 지문은 `state/design-freeze.json`, 검사는 `tests/test_design_freeze.py`(CI).

- 사용자가 요청하지 않은 변경은 하지 않는다. 카드 세트(`content/<ID>/`)의 HTML·`design.css`는 고정 대상이 아니므로 평소처럼 디자인한다.
- 사용자가 요청한 변경이면 같은 PR에서 `python scripts/design_freeze.py --update --note "이유"`로 기록을 갱신하고 `CHANGELOG.md`에 이유를 적는다.
- 되돌리기: `git checkout design-freeze-2026-10-07 -- <파일>`.

## 카드뉴스 역할 분담

ChatGPT가 카피 초안과 디자인 방향(`design`·`coverStyle`·`icon`·`layout`)을 JSON으로 자유롭게 제안하고, Codex가 검수·윤문·영문·승인 요청·HTML 디자인·렌더·QA를 맡는다. ChatGPT 초안의 `pending` 단계는 정상이며 Codex가 마친다. 승인 전 HTML 작성·렌더 금지. 세부는 `docs/card-codex-production.md`.

## Windows 실행

Git Bash에서 실행한다(WSL bash 금지). 환경 변수 `PYTHON=python PYTHONUTF8=1`.
