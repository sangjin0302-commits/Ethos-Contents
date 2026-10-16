# ETHOS 콘텐츠 운영 라우터 (Codex용)

이 저장소는 블로그·비블로그 SNS·웹사이트·카드뉴스 지침의 단일 기준본이다. **작업 유형을 고르고 아래 표의 파일만 읽는다.** 표에 없는 문서, 과거 버전, `archive/`, `CHANGELOG.md`는 사용자가 요청하거나 충돌이 의심될 때만 연다. 필요한 파일은 한 번에 함께 읽는다.

## 작업 라우팅

| 작업 | 읽을 파일 (순서대로) |
|---|---|
| 카드뉴스 제작(ChatGPT 초안 → 완성·렌더) | `docs/card-codex-production.md`, `docs/card-authoring-spec.md`, 해당 `content/<ID>/`의 `brief.md`·`card-data.*.json`·`blog.md`. HTML 단계에서 `docs/card-design-guide.md` |
| 블로그·홈페이지 Editorial Master | `docs/blog-authoring-spec.md`(+ 새 법률 주제면 `docs/evidence-gate.md`, 있으면 `research/<시리즈>.md`). 승인 요청 전 `python scripts/verify_citations.py <원고> --out content/<ID>/citations.md`(키 `LAW_OC`), ⚠는 `docs/legal-verification.md` 6절로 사람 확인 |
| 비블로그 SNS | `docs/sns-authoring-spec.md` |
| 웹사이트 변환 | `docs/website-md-spec.md`(국·영문 MD 두 파일) → 승인된 원문과 정합성 확인 → `python scripts/validate_website_md.py content/<ID>` |
| 소재 발굴·콘텐츠 캘린더 | `docs/strategy-playbook.md`, `docs/topic-discovery.md`, 최신 글감관리표가 있으면 `docs/topic-log-integration.md` |
| 마케팅·성과 분석 | 글감관리표 주간 성과 탭, `docs/topic-log-integration.md` "마케팅 점검", `docs/performance-learning.md` |
| AI 시대 인간 전문성·신규 전문가·자격 결합 포지셔닝 | `.agents/product-marketing.md`, `guidelines/modules/new-expert.md`, `guidelines/modules/human-judgment-positioning.md` |
| 지침 수정·충돌 | `MANIFEST.md`의 Active 파일 확인 → 충돌 검사 → 해당 파일 수정 → `CHANGELOG.md` 갱신 → `python scripts/validate_guidelines.py` |

각 명세가 상위 지침(`guidelines/core/`, `guidelines/channels/`)의 요약이다. 명세로 해결되지 않는 세부나 충돌이 있을 때만 원문을 연다. 우선순위는 현재 사용자 요청 → `MANIFEST.md` → 명세 순이다.

새 글·후속편·새 시리즈·수정본과 파생 콘텐츠는 각 빠른 명세의 칼럼형 설명·법률 조건·실제 맡길 작업과 다음 행동을 함께 적용한다. 국문·영문·아랍어의 표현을 현지화해도 근거와 서비스 범위는 같게 유지한다. 조건형 예시와 매체별 적용 확인은 `examples/writing/cross-channel-three-pillars-20261016.md`를 참고하며, 이 검증 샘플을 승인·발행 원문으로 취급하지 않는다.

새 글·후속편·수정본과 모든 매체·언어는 독자의 생각·질문을 법률 근거·조건 비교·자기 적용·실제 맡길 업무로 연결하는 칼럼을 기본으로 한다. 절차 안내를 공통 뼈대로 강제하지 않는다. 다양한 예시 이름·짧은 대화는 문맥에서 예시임을 드러내어 허용하되 필수 공식으로 만들지 않는다. 허구의 실제 상담·수임·후기·성과 주장은 금지한다. 무료 사전 검토와 유료 작성·제출은 구분한다. 세부 정본은 `docs/language-quality-workflow.md`다.

정본은 `docs/language-quality-workflow.md`이며 각 빠른 명세만 읽어도 적용할 수 있게 요약한다. 파생·번역의 새 장면은 원문 보강·의미 검증·승인 후 Source Lock에 포함한다. 국문·영문·아랍어에 같은 원칙을 적용한다.

## 공통 고정 원칙 (모든 작업)

- 원문·1차 자료에 없는 사실·숫자·조문·판례·경험·후기·성과를 만들지 않는다. 숫자·조문·한정어(수 있·이하·또는)는 원문 그대로.
- 확인된 사실은 단정하고, 조건·재량·추론만 한정한다. 근거 없는 양시론으로 결론을 피하지 않는다.
- 서술 본문·카드에 연락처·URL·버튼 금지. 마지막은 주제에 맞는 무료 검토 안내. 네이버 하단 기존 상담 이미지 4개 예외와 별도 링크설정 메모는 `docs/blog-authoring-spec.md` 6-1절을 따른다.
- 이력 과장·"최고/대표/leading" 금지. 영문에서 행정사는 항상 Administrative Attorney.
- 게시용 국문은 `자연 초안 → 사실·법률 → 마케팅 → 금지 표현 → 윤문 → 의미 재검증` 순서(`docs/language-quality-workflow.md`). 초안부터 모든 규칙을 동시에 맞추지 않는다.
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
