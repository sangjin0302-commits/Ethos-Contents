# ETHOS Active Guidelines Manifest

> 갱신일: 2026-10-25
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
- `guidelines/core/definitive-style.md` — 사실·조건·추론 문체 v1.1, 확인된 결론 우선·근거 없는 양시론 지양
- `guidelines/core/master.md` — 마스터 v7.0, 비충돌 장기 전략에 한정(요약본). 원본 v6.8은 `archive/`에 있으며 적용하지 않는다
- `docs/brand-philosophy.md` — 실제 근거 우선·쉬운 칼럼·의뢰 판단의 공통 정본. 웹사이트 저장소에는 읽기 전용 사본만 둔다

## Active Channels

### 블로그·홈페이지 Editorial Master

- `docs/blog-authoring-spec.md` — 블로그 작성 및 네이버 하단 이미지 링크설정 메모 정본(경로 A 일반·B 심층 조사·C 파생, Hard Gate/Soft Guide, 작성 순서, 최종 3질문). 시리즈명 전체+회차는 네이버 블로그 제목에 표시한다. 홈페이지·웹사이트 관리자 제목(`title`·`titleEn`)과 카카오톡 채널·LinkedIn 제목에는 표시하지 않고 독립 질문을 쓴다. 자연스러운 장면 연결·의미 보조 소제목 이모티콘 기본 활용은 5절을 따른다. 블로그 작업은 이 문서를 먼저 읽는다
- `docs/evidence-gate.md` — 전 매체 근거 선택·검증·재사용 정본. 경로 A/C는 각 명세의 요약과 기존 근거를 재사용하며 B는 이 파일에서 시작한다
- `research/README.md` — 조사 잠금: 시리즈별로 한 번 검증한 법령·판례·통계를 저장해 후속편에서 변경 여부만 확인한다
- `guidelines/channels/blog.md` — 글쓰기 지침 v3.2. 명세에 없는 세부가 필요할 때만 해당 PART를 조회한다

### 비블로그 SNS

- `docs/sns-authoring-spec.md` — SNS 작성 한 장 명세. 카카오톡 채널·LinkedIn 제목은 시리즈명·회차 없이 독립 질문으로 시작한다. SNS 작업은 이 문서를 먼저 읽는다
- `guidelines/channels/sns.md` — 비블로그 SNS 지침 v3.1 (LinkedIn 복사용 일반 텍스트·실제 문단 개행 규칙)
- `guidelines/modules/marketing.md` — SNS 마케팅·영업력 강화 v1.0
- `docs/social-repurposing.md`
- `docs/ethical-persuasion.md`
- `docs/performance-learning.md`

### 웹사이트 변환

- `guidelines/channels/website.md`
- `docs/website-md-spec.md` — 웹사이트 블로그 국·영문 MD 명세(관리자 입력 칸 대응, 시리즈명·회차 없는 독립 질문형 제목, 기존 내부 정보로 시리즈 식별 보존·신규 frontmatter 키 임의 추가 금지, 마크다운 규칙, 영문 색인 기준)
- 원문 작성에는 `guidelines/channels/blog.md`도 함께 적용한다.

### 카드뉴스

- `docs/card-authoring-spec.md` — 카드 JSON 작성 명세. 카드뉴스를 요청받으면 가장 먼저 읽는다(필드 한도·자연스러운 문구 규칙·자가 점검). ChatGPT 초안 단계의 필수 읽기는 이 문서 하나
- `docs/card-codex-production.md` — Codex 전용 카드 제작 명세(초안 검수·윤문·영문·승인·HTML 디자인·렌더·QA). 이하 목록은 Codex 단계 또는 FAIL·판단이 애매할 때만 연다
- `guidelines/channels/cardnews.md`
- `references/ethos-card-design-v3.7.md`
- `references/ethos-card-design-v3.3.md`
- `docs/card-design-guide.md` — 카드 자유 디자인(B 방식) 가이드. Codex·Claude가 카드 HTML을 직접 디자인할 때 적용. 바탕: `vendor/anthropic-frontend-design/`(Apache-2.0)
- `docs/card-patterns.md` — 카드 유형 사전, 표지 문장 패턴, 카드 위 금지 문구, 강조 한 곳
- `state/design-feedback.md` — 사용자 디자인 피드백 원문 기록. 새 세트 디자인 전에 읽는다
- `docs/card-evaluation-rubric.md` — 렌더 후 자기 채점 기준(표지·카피 2배, 가독성·일관성 2배, 흐름, 사실·형식)
- `docs/card-selection.md`
- `docs/channel-packaging.md`
- `docs/performance-learning.md`
- `docs/asset-policy.md` — 의미 보조 로컬 SVG 이모티콘 기본 허용·Twemoji 출처·라이선스 포함

### 게시용 언어·스킬 워크플로

- `guidelines/modules/skill-orchestration.md`
- `docs/marketing-checklist.md` — AI 검색 인용·카피·전환 점검 한 장(marketingskills를 에토스 윤리 원칙에 맞게 걸러 요약, 권고)
- `docs/legal-verification.md` — 사실·법률 검증 체크리스트(확인 기준일, 행정사법 광고·비밀엄수 조항 위치). 게시용 콘텐츠에 공통 적용
- `examples/writing/README.md` — 실제 원고의 고치기 전 → 고친 후 문장 예시. 말투는 규칙보다 이 예시로 잡는다
- `docs/en-legal-glossary.md` — 영문 카드·캡션의 한국 법령 용어 표현집(공식 영문명 아님)
- `docs/language-quality-workflow.md` — 게시용 국문 글·SNS·카드의 자연 초안·분리 검수·최종 윤문·의미 재검증 필수 순서
- `docs/tooling-policy.md`

### 공통 소재 발굴·전략

- `docs/strategy-playbook.md` — 독자×채널, 기존 웹 안내 우선·Revenue 역할 충족 판단 정본, 분기 운영과 유입 출처
- `docs/early-stage-growth-playbook.md` — 발견·검증 단계의 고객확보·문의전환·AI 활용 실행(연차 고정 및 제휴 후보 발굴 제외)
- `docs/sustainable-growth-system.md` — 개업 초기부터 성장기 이후까지 이어지는 검색수요 증거 카드, 운영 모드, 월·분기·연간 성장 루프 정본
- `docs/ai-fast-product-pricing-system.md` — AI 보조 정형상품의 가격 하한·처리기한·자격 게이트와 일반행정사+영어 외국어번역행정사 결합상품 활성화 정본
- `docs/content-architecture-system.md` — Traffic·Authority·Revenue 역할별 글 구조, 채널별 전개, 내부 연결과 성과 진단 정본

- `docs/topic-discovery.md` — 흔하지 않으면서 판단·전환 가치가 있는 글·SNS·카드뉴스 소재 발굴
- `docs/topic-log-integration.md` — 시트 기록 재사용·안정 식별자·발행 및 승인 게이트·성과 계산·내부 데이터 비공개 정본

### 영업 운영 정본

- `docs/strategy-playbook.md` — 콘텐츠·CTA·유입 추적 정본
- `docs/early-stage-growth-playbook.md` — 개업 초기 실행과 1인 사무소 영업 운영체계 정본
- `docs/sustainable-growth-system.md` — 장기 운영 모드와 매출 편중 위험 정본
- `docs/ai-fast-product-pricing-system.md` — 정형·저위험 업무의 고정가·신속처리, 결합상품 범위, 실제시간 기반 가격 재검증 정본
- `docs/topic-log-integration.md`, `docs/performance-learning.md` — 콘텐츠·영업 성과 기록과 학습 정본

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

공통 작성 원칙의 정본은 `docs/brand-philosophy.md`, 근거 선택·검증은 `docs/evidence-gate.md`, 실행 순서·윤문은 `docs/language-quality-workflow.md`다. 각 빠른 명세는 실제 근거를 초안 전에 검토하고 질문·쉬운 설명·의뢰 판단을 연결하도록 요약한다. 파생·번역은 승인 원문의 근거·조건·사례·서비스 범위를 보존한다. 새 근거·장면은 원문 보강·검증·승인 후 사용한다.

## 공통 고정 원칙

- 새 글·후속편·새 시리즈·수정본 및 모든 파생 매체에서 자연스러운 칼럼형 설명, 법률 근거·조건·예외, 실제 맡길 업무와 다음 행동을 함께 살린다. 국문·영문·아랍어는 표현을 현지화하되 의미와 서비스 범위를 유지한다. 각 채널의 빠른 명세에 요약된 기준으로 적용한다.
- 경험하지 않은 상담·수임·후기·성과를 창작하지 않는다.
- 확인된 사실은 단정하고, 조건·재량·추론만 정확히 한정한다.
- 근거가 확보된 질문에는 명확히 답한다. 근거 없는 양시론·양비론을 구성상의 균형으로 사용하지 않는다.
- Authority Demonstrate를 유지하되 이력과 권위를 과장하지 않는다.
- 필요한 글에서는 실제 검토 순서나 대조관계를 Proof of Work로 보여준다.
- 본문 후반부에는 독자가 직접 처리할 범위와 전문가 검토가 필요한 상황을 구분한다.
- 영업 문단은 업무와 자연스럽게 연결해 한 번만 쓴다.
- 네이버 블로그의 서술 본문에는 연락처·상담 링크를 반복 삽입하지 않는다. 예외적으로 글의 마지막 무료 검토 안내 바로 아래에 기존 링크형 상담 이미지 4개(온라인 접수·카카오톡·이메일·텔레그램)를 하나의 CTA 영역으로 둘 수 있다. 온라인 접수를 대표 경로로 먼저 배치하고 나머지는 보조 선택지로 묶는다. SNS·카드 본문 링크 규칙은 별도로 유지한다.
- 발행용 블로그는 칼럼 본문 뒤에 받을 자료와 확인 내용을 구체화한 무료 검토 안내 → 기존 상담 이미지 4개 → 3줄 요약 → 태그 순으로 마친다. 요약에는 새 주장이나 두 번째 CTA를 넣지 않는다. 이미지 4개는 하나의 목적(무료 검토 요청)을 위한 접수 수단이지 영업 문단 4회가 아니다.
- 정확성·법률 의미·원본 정합성을 마케팅 점수보다 우선한다.
- 자연스러움은 선택 장식이 아니다. 게시용 한국어는 자연 초안과 분리된 검수·윤문·의미 재검증을 완료한다.

## 비활성 문서

- `archive/` 아래 모든 파일(마스터 v6.8 원본 포함). 기록 보존용이며 검색에 걸려도 적용하지 않는다.

- 동일 지침의 v3.1 이하 최상위 버전
- 블로그 v3.0 이하
- 비블로그 SNS v2.3 이하
- 카드뉴스 v3.6 이하
- 위 Active 파일과 충돌하는 고정 발행 빈도·복수 CTA·직접 연락처 규칙

비활성 문서는 기록 보존 외의 목적으로 적용하지 않는다.
