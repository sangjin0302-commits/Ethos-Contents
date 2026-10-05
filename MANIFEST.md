# ETHOS Active Guidelines Manifest

> 갱신일: 2026-10-05
> 원칙: 이 문서에 Active로 지정된 파일만 운영 지침으로 적용한다. 저장소의 다른 문서와 과거 버전은 참고자료일 뿐 자동 적용하지 않는다.

## 적용 우선순위

1. 현재 대화에서 사용자가 직접 한 요청
2. ChatGPT 프로젝트의 짧은 부트스트랩 지침
3. 이 `MANIFEST.md`
4. `guidelines/core/top-level.md`
5. `guidelines/core/definitive-style.md`
6. 요청 채널의 최신 지침
7. 주제와 작업에 필요한 모듈
8. `guidelines/core/master.md`의 비충돌 장기 전략

같은 층에서 충돌하면 더 구체적인 규칙을 적용한다. 그래도 해결되지 않으면 임의로 섞지 말고 사용자에게 충돌을 알린다.

## Active Core

- `guidelines/core/top-level.md` — ChatGPT 최상위 운용지침 v3.2
- `guidelines/core/definitive-style.md` — 사실·조건·추론 문체 v1.0
- `guidelines/core/master.md` — 마스터 v6.8, 비충돌 장기 전략에 한정
- `docs/brand-philosophy.md` — 마케팅 철학 공유본(정본). 웹사이트 저장소에는 읽기 전용 사본만 둔다

## Active Channels

### 블로그·홈페이지 Editorial Master

- `guidelines/channels/blog.md` — 글쓰기 지침 v3.1

### 비블로그 SNS

- `guidelines/channels/sns.md` — 비블로그 SNS 지침 v3.0
- `guidelines/modules/marketing.md` — SNS 마케팅·영업력 강화 v1.0
- `docs/social-repurposing.md`
- `docs/ethical-persuasion.md`
- `docs/performance-learning.md`

### 웹사이트 변환

- `guidelines/channels/website.md`
- 원문 작성에는 `guidelines/channels/blog.md`도 함께 적용한다.

### 카드뉴스

- `docs/card-authoring-spec.md` — 카드 JSON 작성 명세. 카드뉴스를 요청받으면 가장 먼저 읽는다(필드 한도·자연스러운 문구 규칙·자가 점검)
- `guidelines/channels/cardnews.md`
- `references/ethos-card-design-v3.7.md`
- `references/ethos-card-design-v3.3.md`
- `docs/card-selection.md`
- `docs/channel-packaging.md`
- `docs/performance-learning.md`
- `docs/asset-policy.md`

### 게시용 언어·스킬 워크플로

- `guidelines/modules/skill-orchestration.md`
- `docs/marketing-checklist.md` — AI 검색 인용·카피·전환 점검 한 장(marketingskills를 에토스 윤리 원칙에 맞게 걸러 요약, 권고)
- `docs/language-quality-workflow.md` — 게시용 국문 글·SNS·카드의 자연 초안·분리 검수·최종 윤문·의미 재검증 필수 순서
- `docs/tooling-policy.md`

### 공통 소재 발굴

- `docs/topic-discovery.md` — 흔하지 않으면서 판단·전환 가치가 있는 글·SNS·카드뉴스 소재 발굴
- `docs/topic-log-integration.md` — 글감관리표의 발행 이력·반복 관심·문의 유입을 소재 선정에 반영

## Active Modules

필요한 모듈만 선택한다. 모든 모듈을 모든 글에 강제하지 않는다.

- `guidelines/modules/new-expert.md` — 신규 전문가의 Proof of Work·CTA Specificity·Emerging Social Proof·Revenue Cluster
- `guidelines/modules/human-judgment-positioning.md` — AI 시대에도 필요한 사람의 사실판단·문서 정합성·절차 설계·책임을 증명하는 작업 자산
- `guidelines/modules/international-business.md` — 사회 변화형 신사업 인허가·국제화·향후 외국어 번역행정사 확장
- `guidelines/modules/middle-east-arabic.md` — 중동·아랍 소재와 현지화
- `guidelines/modules/everyday-topics.md` — 일상 소재 발굴
- `guidelines/modules/new-practice-exploration.md` — 신규 업역 탐색
- `guidelines/modules/skill-orchestration.md` — ChatGPT 콘텐츠 스킬 사용과 충돌 방지. 게시용 콘텐츠에 공통 적용

소재를 정하거나 콘텐츠 캘린더를 만들 때에는 채널과 관계없이 `docs/topic-discovery.md`를 함께 적용한다.

AI 시대의 전문성, 신규 전문가 신뢰, 자격 결합 또는 다른 전문자격사와의 역할 구분이 주제에 포함되면 `guidelines/modules/human-judgment-positioning.md`를 적용한다. 이때 `.agents/product-marketing.md`는 포지셔닝 맥락으로만 사용하며 상위 지침을 대체하지 않는다.

## 공통 고정 원칙

- 경험하지 않은 상담·수임·후기·성과를 창작하지 않는다.
- 확인된 사실은 단정하고, 조건·재량·추론만 정확히 한정한다.
- Authority Demonstrate를 유지하되 이력과 권위를 과장하지 않는다.
- 필요한 글에서는 실제 검토 순서나 대조관계를 Proof of Work로 보여준다.
- 본문 후반부에는 독자가 직접 처리할 범위와 전문가 검토가 필요한 상황을 구분한다.
- 영업 문단은 업무와 자연스럽게 연결해 한 번만 쓴다.
- 본문에 연락처·카카오톡·텔레그램·이메일 링크를 직접 넣지 않는다.
- 발행용 콘텐츠의 마지막 문장은 해당 주제에서 무엇을 확인하는지 구체화한 무료 검토 안내로 끝낸다.
- 정확성·법률 의미·원본 정합성을 마케팅 점수보다 우선한다.
- 자연스러움은 선택 장식이 아니다. 게시용 한국어는 자연 초안과 분리된 검수·윤문·의미 재검증을 완료한다.

## 비활성 문서

- 동일 지침의 v3.1 이하 최상위 버전
- 블로그 v3.0 이하
- 비블로그 SNS v2.3 이하
- 카드뉴스 v3.6 이하
- 위 Active 파일과 충돌하는 고정 발행 빈도·복수 CTA·직접 연락처 규칙

비활성 문서는 기록 보존 외의 목적으로 적용하지 않는다.
