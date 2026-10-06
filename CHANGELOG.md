# Changelog

## 2026-10-06 — 웹사이트 블로그 국·영문 MD

- `docs/website-md-spec.md`: 웹사이트(Admin-system-) 관리자 편집기의 입력 칸(slug·title·excerpt·category·tags, 영문 칸)과 1:1인 YAML 머리말, 공개 페이지 마크다운 변환(remark + remark-html)에 맞춘 본문 규칙(본문 `#` 금지, 마크다운 표 금지, `**` 짝 맞추기, 연락처·추적 링크 금지), 영문 색인 기준(1,200자·180단어 이상, 한글 20자·3% 이하). 웹사이트 저장소 코드를 2026-10-06에 읽어 확인했다.
- `scripts/validate_website_md.py`: 두 파일의 머리말·본문·영문 기준과 국·영 slug·category 일치를 검사한다.
- `content/_TEMPLATE/website.ko.md`, `website.en.md` 양식, `examples/website-md-realtor/` 예시(검사 PASS).
- 프로젝트 지침·AGENTS·웹사이트 채널 지침: "웹사이트·홈페이지·MD" 요청이면 국·영문 MD 두 파일을 함께 낸다.
- 블로그 명세: `**` 금지는 네이버 원고에만 적용, 웹사이트 MD는 별도 규칙.

## 2026-10-06 — 프리셋·피드백 기록·카드 유형 사전·강조·본문 16px

- `templates/presets/ethos-a|b|c.css`: 시범 세트에서 확정한 에토스 프리셋(A 기본: 세리프 제목+Pretendard 본문, B 굵은 타이포, C 크림 여백형). 세트 `design.css`는 프리셋을 불러오고 세트별 조정만 적는다(Kanghyeop/card-news-simple-skill의 프리셋 방식).
- `state/design-feedback.md`: 사용자 디자인 피드백 원문 기록과 반영 내역. 새 세트 디자인 전에 읽고, 반영은 프리셋·가이드로 올린다.
- `docs/card-patterns.md`: 카드 유형 사전(표지·기준·목록·단계·대비·근거·숫자·마무리), 표지 문장 패턴, 카드 위 금지 문구(greeun/card-news-harness 방식을 다시 씀).
- `highlight`: 제목·결론 안의 한 구절을 골드 밑줄로 강조(스키마·빌더·`mark-hl`).
- 자유 디자인 카드 본문 최소 16px(`gates.json` `freeDesignMinPx`, `qa_render.py`가 `ethos-design` 표시 카드에만 적용, 사용자 승인).
- 평가 기준표에 흠 찾기 질문 7개와 독립 평가 원칙 추가.

## 2026-10-06 — 카드 10장 고정, 영문 행정사 번역어 고정

- 카드뉴스는 최대 10장(6~10장)으로 고정. 프로젝트 지침·AGENTS·카드 작성 명세에 명시했다(스키마·게이트는 이미 10장 초과를 오류로 막음).
- 영문에서 행정사는 항상 **Administrative Attorney**, 행정사사무소는 **Administrative Attorney Office**. 영문 표현집·작성 명세·프로젝트 지침에 고정하고, `copy_lint`가 행정사·에토스 사무소를 가리키는 다른 번역어(Korean/licensed administrative agent, scrivener, solicitor, Ethos Administrative Office)를 카드와 캡션에서 경고한다. 다른 나라의 agent·office 같은 일반 표현은 잡지 않는다. 소송·분쟁 대리를 암시하는 문장과 함께 쓰지 않도록 했다.
- 영문 카드 꼬리말을 "Ethos Administrative Attorney Office"로 바꾸고 영문 세트를 다시 렌더했다(QA PASS).

## 2026-10-06 — 공개 카드뉴스 프로젝트 비교 반영

검토한 저장소: chltmdgh522/AutoMakeCardNews(Java 웹 서비스, 구조가 달라 미적용), Giii-sik/card-news-publication-workflow(라이선스 표기 없음, 방식만 참고), Kanghyeop/card-news-simple-skill(ISC), greeun/card-news-harness(MIT, Pretendard OFL). 코드·문서는 복사하지 않고 규칙만 다시 썼다. 폰트만 원본 파일을 OFL 라이선스와 함께 가져왔다.

- `fonts/`: Pretendard Regular·Medium·Bold·ExtraBold(SIL OFL 1.1)와 `LICENSE-Pretendard.txt`. `brand/fonts.css`, `brand/tokens.json`(필수 로드 확인), `gates.json`(허용 글꼴)에 추가했다(사용자 승인). 기존 빌더 카드의 글꼴은 그대로다.
- `docs/card-design-guide.md` 6~9절: 540px 기준 글자 체계, 카드 안 글자 비율 3:1 이내, 한글 자간, 줄바꿈·분량 한도, 카드 위 금지 문구, 와이어프레임·세 방향 시안·레퍼런스 흡수·자기 채점 단계.
- `docs/card-evaluation-rubric.md`: 표지·카피(2배), 가독성·일관성(2배), 흐름, 사실·형식 1~5점 채점과 통과 기준.
- `scripts/preview_drafts.py`: 세 방향 시안을 QA 없이 찍어 비교 시트를 만든다.
- 시범 세트: 본문 Pretendard, 자간, 배경 장식 원 제거, 영문 카드 8장, 와이어프레임·시안(A·B·C)·채점 기록 추가. 국·영문 QA PASS.
- 빌더: 가운뎃점으로 묶인 낱말이 줄 첫머리에서 끊기지 않게 했고(`nobr`), 린터가 가운뎃점 셋 이상 나열한 메모체 문구를 알려 준다.

## 2026-10-06 — 카드 자유 디자인(B 방식)

- 카드 HTML을 템플릿 빌더로 찍지 않고 Codex·Claude가 카드마다 직접 디자인하는 방식을 기본으로 바꿨다. `docs/card-design-guide.md`(위계·시각 중심 하나·빈칸을 글자로 채우기·결론 띠 40% 이하·흔한 AI 디자인 습관 피하기·설계→검토→작성→렌더→자기 검토 순서).
- 바탕 자료로 Anthropic `frontend-design` 스킬(Apache-2.0)을 `vendor/anthropic-frontend-design/`에 원본 그대로 넣었다. 색·글꼴은 에토스 브랜드가 우선한다.
- 직접 디자인한 HTML은 `<meta name="ethos-design" content="free">`로 표시한다. `Render cards`는 이 파일을 빌더 대신 그대로 렌더하고, card-data 문구가 글자 그대로 들어 있는지 **카피 잠금**으로 대조해 다르면 실패시킨다(`copy_lint.copy_lock`). 표시가 없는 카드는 기존 빌더로 만든다.
- card-data 카드에 `design`(시각 중심·구도 한 줄 제안) 필드를 추가했다. ChatGPT가 쓰고 Codex가 출발점으로 쓴다.
- 시범 세트 `examples/free-design-realtor/`(발행 금지, QA PASS).
- 빌더의 자동 맞춤은 본문 글자가 제목의 60%를 넘지 않게 제한했다(제목과 본문이 같은 크기로 보이던 문제).

## 2026-10-06 — 카드 빈칸 자동 맞춤, 발행 위생 검사, ChatGPT 테스트 반영

- 세로형(4:5) 캔버스에서 본문이 짧은 카드에 빈 공간이 크게 남던 문제: v2 세트(편집 v2.0 또는 `layoutVersion: "2"`)는 폰트 로드 뒤 본문 **글자 크기만** 남는 높이만큼 키운다(최대 1.6배, 목표 채움 90%, 여백은 그대로). 처음에는 블록 전체를 확대(zoom)했는데 여백까지 함께 커져 눈으로는 여전히 비어 보여 글자만 키우도록 바꿨다. 가로·세로 넘침이 생기면 직전 배율에서 멈춘다.
- 키 없는 번호 목록(`checklist`)의 번호 칸이 124px로 고정돼 숫자 옆이 크게 비던 결함을 고쳤다(`threshold num`, 36px). 표지는 제외. 스펙 스트레스 전 세트와 승인 세트 2개(국·영문) QA PASS, PNG·시트 재생성.
- `copy_lint` 블로그 검사: `utm_…`·`OC=`가 붙은 링크, `**` 마크다운 굵게 표시를 경고한다. 카드: 결론 띠(bar)가 40%를 넘으면 info.
- `marketing_review.py`: 본문 항목이 `{key, text}`일 때 멈추던 오류를 고쳤다(사용자 승인).
- 블로그 작성 명세에 발행 형식(시리즈 제목·인사·목차, 출처 표기, 마크다운 금지), 카드 작성 명세에 가장 강한 숫자는 `stats`, 결론 띠 40% 이하, 얇은 카드 연속 피하기, `marketing` 블록을 추가했다. 예시집에 카드 예시 2쌍 추가.

## 2026-10-06 — 승인 세트 v2 레이아웃 재렌더, 라벨 없는 항목 수정, ChatGPT 테스트 안내

- GAME-OVERSEAS-06, SUSPENSION-SURCHARGE-04에 `layoutVersion: "2"`를 넣어 문구 변경 없이 v2 레이아웃으로 HTML·PNG·시트·QA 보고서를 다시 만들었다(국·영문 QA PASS). 편집 기록은 legacy 그대로다.
- `concept` 항목에 라벨이 없을 때 빈 라벨 칸(92px)이 남아 본문이 오른쪽으로 밀리던 결함을 고쳤다(`rule-item no-key`).
- `Render cards` 요약에 윤문 힌트와 블로그 검사를 포함했다.
- 렌더 스크립트가 `CHROMIUM_PATH` 환경 변수로 브라우저 경로를 받을 수 있다(없으면 기존 동작).
- `docs/chatgpt-test-plan.md`: 개편 후 ChatGPT 통합 테스트 프롬프트·확인 항목·점수표.

## 2026-10-06 — 자연스러움 우선: 예시집·반복 패턴 검사·영문 표현집

- 작성 명세와 법률 검증표를 "다 쓴 뒤 훑는 권고"로 명시하고 반드시 지킬 것을 네 가지(미확인 사실, 경험 창작, 연락처, 숫자·조문·한정어)로 좁혔다.
- `examples/writing/README.md`: 실제 원고에서 뽑은 고치기 전 → 고친 후 8쌍(부정 결론, "따라서" 사슬, "중요한 것은", 번역투, 카드 결론 띠, 카드 위 조문, 영문 직역). 작성 명세·카드 명세·프로젝트 지침 맨 앞에 연결했다.
- `docs/en-legal-glossary.md`: 영문 카드·캡션용 한국 법령 용어 표현집(공식 영문명 아님).
- `copy_lint.py`: 반복 접속어, 상투 표현, 번역투, 부정문 비율·연속(국문 블로그·카드), 영문 가독성(오프라인 Flesch 근사)과 proselint 상투어 표시. 모두 info이며 `--strict`에서도 실패로 치지 않는다. textstat은 실행 중 사전 다운로드가 필요해 쓰지 않았다.
- `layoutVersion: "2"`: legacy 승인 세트도 문구와 편집 기록을 건드리지 않고 v2 레이아웃(밀도 보정·일러스트)으로 다시 렌더할 수 있다.
- requirements에 `proselint==0.16.0`(BSD-3-Clause) 추가.

## 2026-10-06 — 전략 플레이북·받을 자료·유입 출처

- `docs/strategy-playbook.md`: 독자×채널(영문 카드는 LinkedIn 문서형 캐러셀 기본), 여정 단계별 콘텐츠 역할, 받을 자료, 분기 운영, 유입 출처 기록, 웹사이트 저장소 요청 목록. MANIFEST와 AGENTS 소재 발굴 경로에 연결했다.
- `content/_TEMPLATE/lead-magnet-checklist.md`, `lead-magnet-process-map.md`: 승인된 원문만으로 채우는 받을 자료 양식.
- `content/_TEMPLATE/distribution.md`: 게시 링크·추적 이름 표.
- `docs/layout-playbook.md`: 6장 이상 세트에 글이 적은 "쉼" 카드 한 장 이상, 표지 제목 2줄 우선.

## 2026-10-06 — 마스터 v7.0 요약본, 작성 명세, 법률 검증

- `guidelines/core/master.md`를 v6.8(약 78KB)에서 v7.0 요약본으로 교체했다. 원본은 `archive/master-v6.8.md`로 옮겨 "보관 문서" 경고를 붙이고 연락처를 가렸다. 폐기 규칙(글마다 인라인 CTA 2회, 정확히 3회 규칙, 매일 전 채널 발행, 비자 허브 45% 고정 비중, 다수 연락처 표기)과 출처 없는 마케팅 통계는 v7.0에 옮기지 않았다.
- v7.0 11절에 구 번호 참조표를 두고, 마스터 번호를 인용하는 하위 모듈 3개(`everyday-topics`, `middle-east-arabic`, `new-practice-exploration`) 맨 위에 해석 안내를 넣었다. 마스터 9 팩트뱅크는 적용 금지로 하고 쓰기 전에 공식 1차 자료로 다시 확인하도록 했다.
- `docs/blog-authoring-spec.md`, `docs/sns-authoring-spec.md`: ChatGPT용 한 장 명세(읽을 파일, 작성 순서, 자가 점검표). "CTA를 지워도 저장할 기준이 남는가" 점검을 넣었다. `PROJECT_INSTRUCTIONS.md`와 MANIFEST에 연결했다.
- `docs/legal-verification.md`: 확인 기준일, 증거 라벨, 행정사법 제22조(제3·4·5호), 제23조, 제15조, 제21조 위치표(2026-10-06 조회).
- `guidelines/modules/skill-orchestration.md`: ChatGPT에 없는 스킬(`humanize-korean`, `content-strategy`, `social`, `copywriting`)의 대체 절차표.
- `docs/performance-learning.md`: 세트 3개마다 유지·변경·보류를 정하는 규칙. `performance-log.csv` 템플릿에 `decision` 열 추가.
- `scripts/validate_guidelines.py`: 활성 문서의 연락처, 출처 없는 통계, 폐기 규칙 잔존과 `archive/` 경고 문구 누락을 검사한다.
- `docs/brand-philosophy.md`는 바꾸지 않았다. 웹사이트 저장소 동기화 PR은 생기지 않는다.

## 2026-10-05 — 가로 대표 이미지

- `scripts/build_og.py`: 표지 카드에서 1200×630 가로 공유 이미지(`og-ko.png`, `og-en.png`)를 만든다. 사이트 글의 `og:image`가 1200×630을 선언하는데 실제 이미지는 1080×1080이나 세로형이라 공유 미리보기에서 가운데만 잘리던 문제를 줄인다. 제목은 가운데 안전 영역에 두고 페이지 번호를 뺀다. 안전 영역 이탈·글자 크기·줄 수를 검사하고 실패하면 PNG를 내지 않는다.
- `ci_render.py`가 세트마다 가로 대표 이미지를 함께 만들어 아티팩트와 요약에 낸다. `spec_stress.py`에 표지 스타일 4종 × 국·영문 8건 시험을 추가했다.

## 2026-10-05 — 체크리스트에서 llms.txt 항목 삭제

- `llms.txt`는 표준이 아니고 효과가 확인되지 않아 마케팅 체크리스트에서 뺐다. 파일이 없어도 사이트에는 문제가 없다.

## 2026-10-05 — 마케팅 체크리스트

- `docs/marketing-checklist.md`를 추가하고 MANIFEST에 연결했다. marketingskills(MIT)의 `ai-seo`·`copywriting`·`cro`를 에토스 윤리 원칙에 맞게 걸러 AI 검색 인용, 카피, 전환 점검 목록으로 다시 썼다. 후기·고객 수 나열, 긴급성·희소성, 성과 수치, 경쟁 우위 비교, 인위적 언급 만들기는 원칙과 충돌해 뺐고 그 이유를 표로 남겼다.
- 사이트 확인 결과를 기록했다: AI 크롤러를 막지 않음, 구조화 데이터는 Article·BlogPosting·LegalService 등. 웹사이트 저장소 쪽 조치는 그 저장소에서 결정한다.
- PROJECT_INSTRUCTIONS 빠른 경로의 마지막 단계에 이 체크리스트를 추가했다. 출처 표기와 라이선스는 `vendor/marketingskills/`.

## 2026-10-05 — 자동 윤문 제안·형태소 검사

- `vendor/im-not-ai/quick-rules.md`(MIT, 원본 그대로)와 `scripts/ai_polish.py`를 추가했다. Claude API로 국문 카드 카피의 윤문 제안을 만들고, 사실 토큰·길이·변경률·금지 문구 검사를 통과한 제안만 남긴다. 파일은 `--apply`일 때만 고친다.
- `AI polish suggestions` 워크플로: PR에서 국문 card-data가 바뀌면 제안을 PR 댓글로 남긴다. `ANTHROPIC_API_KEY`가 없으면 건너뛴다.
- `copy_lint.py`에 kiwipiepy 형태소 분석을 붙여, 같은 결론 어미가 4장 이상 이어지면 알려 준다(`-ㅂ니다/-습니다`는 같은 어미로 본다).
- requirements에 `kiwipiepy==0.24.0`, `anthropic==1.11.0`을 고정했다.
- API 없이 쓰는 기본 방식: 프로젝트 지침의 빠른 경로에 humanize-korean 규칙집을 추가해 ChatGPT가 직접 윤문한다. `Render cards` 워크플로가 PR의 card-data를 이전 버전과 비교해 사실 토큰 변화와 한정어 감소(수 있·이하·또는 등)를 PR 댓글로 알린다.

## 2026-10-05 — 밀도 보정·일러스트·표지 변형

- v2.0 세트 한정으로 카드 본문 밀도를 low/mid/high로 나눠, 본문이 짧은 카드는 글자와 패널을 키워 빈 공간을 채운다. legacy 세트는 영향이 없고 승인 세트 4개의 HTML은 그대로 재생성된다.
- `assets/illustrations/`에 자체 제작 평면 일러스트 6종(balance, bridge, calendar, documents, layers, route)을 추가했다. navy·cream 양쪽에서 같은 클래스로 칠해진다.
- 카드 `illustration`(본문이 짧고 제목이 짧을 때만 표시), 표지 `coverStyle`(`art`·`panel`·`stat`)과 `hero`를 추가했다.
- `spec_stress.py`를 v2.0 모드로 돌리고 표지 변형, 짧은 본문, 밀도 경계(low 직전 최대 카드) 세트를 추가했다. 국·영문 7세트 14건이 통과한다.

## 2026-10-05 — ChatGPT 시험 결과 반영

- 실제 ChatGPT 산출물을 파이프라인에 넣어 확인한 결과를 반영했다.
- `concept`(2~3항목) 키 열이 92px 고정이라 `Occupation` 같은 긴 영문 키가 넘치던 결함을 고쳤다(`minmax(92px, max-content)`, 기존 짧은 키의 렌더는 그대로).
- `spec_stress.py`가 키 필드에 줄바꿈 없는 한 단어를 넣어 고정 폭 열을 시험하도록 강화하고, 이로 드러난 키 한도(comparison·stats·flow·table·cta)를 낮췄다.
- `copy_lint.py`: 같은 카드 안에 용어 풀이가 있으면 인정하고, `[미확인]`을 자리표시자로 경고한다.
- 작성 명세에 숫자+단위 원문 일치, `assets.md` 기록, `[미확인]` 해소를 추가했다.

## 2026-10-05 — 철학 동기화 멱등성 수정

- 열린 `sync/brand-philosophy` 브랜치의 사본이 이미 같은 경우 새 커밋과 강제 푸시를 만들지 않도록 했다.
- `scripts/sync_philosophy.py`에 쓰기 없는 정확 비교 모드를 추가하고 회귀 테스트를 보강했다.

## 2026-10-05 — 철학 사본 자동 동기화

- `scripts/sync_philosophy.py`와 `Sync brand philosophy` 워크플로를 추가했다. `docs/brand-philosophy.md`가 main에 머지되면 웹사이트 저장소 `docs/contracts/brand-philosophy.md`에 읽기 전용 사본을 덮어쓰는 PR을 연다. `ADMIN_SYSTEM_SYNC_TOKEN` 시크릿이 없으면 건너뛴다.
- `docs/brand-philosophy.md` v1.1: 7절을 자동 동기화 방식으로 바꿨다.

## 2026-10-05 — 마케팅 철학 공유본, 홈페이지 칼럼 경로 수정

- `docs/brand-philosophy.md`를 추가하고 MANIFEST Active Core에 연결했다. 이 저장소가 철학의 정본이며 웹사이트 저장소에는 읽기 전용 사본만 둔다. 글자 수 한도·린터·렌더 같은 제작 규칙은 공유 대상이 아니다. 무료 검토·유료 상담의 범위, 가격, 접수 경로는 웹사이트 저장소 운영정책이 정본임을 명시했다.
- `master.md`의 홈페이지 칼럼 주소를 `/column (예정)`에서 실제 경로 `/blog`로 고쳐 링크 검사 404를 없앴다.

## 2026-10-05 — 카드 작성 명세·자동 렌더·한도 검증

- `docs/card-authoring-spec.md`: ChatGPT가 카드 JSON만 쓰도록 하는 한 장 명세(필드 한도, 문구 규칙, 자가 점검표). MANIFEST 카드뉴스 첫 항목과 프로젝트 지침에 연결했다.
- `card-limits.json` + `scripts/spec_stress.py`: 모든 카드 유형을 한도의 최대치로 렌더해 실제 QA 게이트 통과를 확인한다(navy/cream 반전 포함). 이 검사로 표지·질문 그리드·6항목 CTA가 한쪽 배경에서 대비 실패하던 CSS 결함을 찾아 고쳤다.
- `scripts/ci_render.py`와 `Render cards` 워크플로: card-data 변경 시 스키마 검증, 린터, 렌더, QA를 돌리고 PNG·시트를 아티팩트로, 결과를 작업 요약으로 낸다. 승인 렌더가 아니라 미리보기다.
- `copy_lint.py`에 한도 초과 규칙을 추가했다. 한도의 1.5배 이내는 info, 초과는 warn이다(렌더 QA가 최종 판정).
- `card-system-check` 워크플로의 `PYTHONUTF8` 누락(Windows cp1252로 한글 출력이 실패)을 고치고 한도 검증을 추가했다.
- cream 위 `concept` 4칸이 카드 테두리 없이 글자만 떠 있던 스타일을 흰 카드로 바꿨다. 시각 회귀 기준 `card_02.png`를 의도적으로 갱신했다.

## 2026-10-05 — 아이콘·표지 삽화·stats 행

- `assets/icons/lucide/`에 Lucide 아이콘 25종(ISC, 원본 그대로)과 LICENSE를 추가했다. 카드의 `icon`, 표지 `art`, 항목별 `icon`을 빌더가 인라인 SVG로 렌더한다. 알 수 없는 이름이나 경로 문자는 렌더 중단.
- `checklist.layout: "stats"`(큰 숫자 행)를 추가했다.
- `copy_lint.py`가 카드에 쓴 아이콘의 `assets.md` 출처 기록 누락을 경고한다.
- `gates.json`은 바꾸지 않았다. 아이콘·도형은 기존 게이트(그라데이션·이모지 금지, 대비, 폰트 크기)를 그대로 통과한다.

## 2026-10-05 — 카피 린터·데이터 구동 렌더러·flow/table 컴포넌트

- `scripts/copy_lint.py`와 `copy-rules.json`을 추가했다. 질문형 헤드라인 반복, 부정문 결론, 카드 위 조문 번호, 미풀이 전문용어, 약속 없는 표지, 국·영문 질문 방향 반전, 캡션 저장 이유, 자리표시자를 검사하고, `--compare`로 윤문 전후의 조문·판례·금액·날짜 토큰 변화를 확인한다. 기본은 권고이며 `--strict`로 실패 처리할 수 있다.
- `scripts/build_cards.py`에서 `page == 6`/`page == 8`/`page in (1, 4, 7, 10)` 하드코딩을 제거했다. 체크리스트 모양은 `layout`·`key`, 결론 스타일은 `takeStyle`로 정한다. 기존 승인 세트 4개는 필드만 명시해 HTML이 바이트 단위로 같게 재생성되며 `tests/test_copy_lint.py`가 이를 잠근다.
- `flow`, `table` 카드 유형과 `cover.promise` 필드를 추가했다. card-data 스키마의 `body` 항목은 문자열 또는 `{key, text}`를 허용한다.
- `scripts/visual_regression.py` 고정 입력에 `takeStyle`을 명시해 기준 PNG를 그대로 유지했다.
- GAME-OVERSEAS-06의 새 코드 기준 비교용 초안을 `content/GAME-OVERSEAS-06-V2-DRAFT/`에 두었다. 사실 확인과 사용자 승인 전이므로 발행하지 않는다.

## 2026-10-05 — 글·SNS·카드 자연스러움 파이프라인 강제

- 게시용 국문 콘텐츠의 순서를 자연 초안 → 사실·법률 검증 → 마케팅 보강 → 금지 표현 검사 → 자연스러움 윤문 → 의미 재검증으로 통일했다.
- `humanize-korean`을 선택 권고가 아니라 게시 전 필수 편집 단계로 바꾸고, 사용할 수 없을 때에는 동등한 수동 검수를 기록하도록 했다.
- 카드뉴스는 Source Lock으로 사실을 보호하되 원문 문장 구조를 복제하지 않도록 분리했다.
- 새 card-data에 `editorialReview.pipelineVersion: 2.0`과 단계별 완료 기록을 필수화하고, 미완료 상태에서는 양언어 검증이 실패하도록 했다.
- 기존 승인 세트에는 검수를 소급해 꾸미지 않고 `legacy-unrecorded`로 표시했다.
- 동일 종결어미·보고서식 문장·기계적 질문 구조 반복을 카드 자연스러움 검수 항목에 추가했다.

## 2026-10-05 — 글감관리표 연동·카드 가독성·배포 검증 보강

- Instagram 기본 출력을 portrait + social-native로 고정하고 card-data 스키마에서도 두 값을 필수화했다.
- 정사각형으로 남아 있던 단일 레이아웃 값을 프로필별 캔버스 설정으로 바꿨다.
- 국문은 글자 수, 영문은 글자 수·단어 수·실제 줄 수를 함께 보는 밀도 경고를 추가했다.
- 마케팅 점수가 밀도 경고를 내면서도 100점이 되던 문제를 수정해 과밀 카드 수와 강한 경고에 따라 가독성 점수를 차감한다.
- 카드별 alt text와 외부 자산의 원본 URL·제작자·라이선스·확인일·수정 여부를 검사하는 validate_distribution.py와 assets.md 양식을 추가했다.
- Vale 에토스 전용 비차단 규칙과 영문 전용 CSpell 설정을 추가하고, LanguageTool을 한국어 검사기로 사용하지 않도록 정리했다.
- brief에 근거 확인일·갱신 조건·재검토일·상위 허브·이전/다음 콘텐츠·CTA 경로를 추가했다.
- 에토스_글감관리표.xlsx의 발행 이력·반복 상위 노출·실제 문의 유입·갱신 필요·포트폴리오 공백을 소재 선정에 반영하는 운영 지침을 추가했다.

## 2026-10-04 — AI 시대 인간 전문성·자격 결합 포지셔닝

- 일반행정사와 향후 적법하게 활성화된 외국어번역행정사의 결합 가치를 다른 전문자격사와의 우열이 아니라 행정절차와 외국문서의 연결 능력으로 정의했다.
- AI 활용을 홍보하지 않고 사실관계 파악, 문서 정합성, 절차 설계, 설명, 책임과 대응으로 인간 전문성을 증명하는 공통 모듈을 추가했다.
- 글·SNS·카드뉴스 brief에서 일반정보만으로 해결되지 않는 이유와 사람이 보여줄 판단 증거를 정하도록 했다.
- 신규 전문가의 경험 부족은 허위 후기나 권위 표현이 아니라 최신성·작업 양식·검증 기록으로 보완하도록 했다.
- 마케팅 스킬이 공통으로 참조할 `.agents/product-marketing.md`를 추가했다.

## 2026-10-04 — 희소·전환형 소재 발굴 체계

- 신사업 인허가·국제화 브랜드를 좁히지 않으면서 흔하지 않은 소재를 찾는 공통 가이드를 추가했다.
- 외국인 고용기업, 외국인·외국기업 사업 인허가, 복합 행정문제를 브랜드명이 아니라 우선 탐색할 소재군으로 재정의했다.
- 글·SNS·카드뉴스가 분류 경계, 제도 교차, 순서 의존성, 문서 정합성, 반복성, 국제화 마찰을 공통 신호로 사용하도록 연결했다.
- Entry·Core·Composite·Recurring B2B 분류는 발행을 막는 점수가 아니라 콘텐츠 포트폴리오와 성과학습용 내부 표지로 한정했다.

## 2026-10-04

### Added — 카드뉴스·SNS 회수 보강

- 카드 제작 대상 선별과 전체·짧은 파생물 구분
- Instagram·LinkedIn·카카오·블로그/홈페이지 채널별 패키징
- Revenue Cluster·구매 단계·적합 문의까지 보는 성과학습과 CSV 템플릿
- Visual Family 편집 언어와 사진·삽화·비상주 사무실 자산 정책
- `humanize-korean` 보호·변경률·롤백 절차와 마케팅 스킬 최소 선택 원칙
- 현재 오픈소스 도구와 신규 도구의 비차단 채택 기준
- 블로그 원문에서 SNS 콘텐츠 단위를 추출하는 채널별 재가공 규칙
- 상호성·권위·선택 단순화·행동 부담 감소를 활용하는 윤리적 설득 원칙
- 카드뉴스와 일반 SNS를 분리한 성과로그 템플릿

### Changed — 카드뉴스·SNS 회수 보강

- 스킬 연계지침을 v1.1로 갱신하고 카드뉴스 v3.5.1·v3.6 참조를 v3.7 MANIFEST 라우팅으로 교정
- SNS 마케팅 모듈의 프로젝트 중복 업로드 안내를 GitHub 단일 기준본 방식으로 교체
- 자연스러움·마케팅 검토와 성과 지표를 비차단 권고로 유지

### Added

- GitHub 지침 단일 기준본을 위한 `MANIFEST.md`
- 블로그·SNS·웹사이트·카드뉴스 채널별 지침 라우팅
- 신규 전문가, 신사업 인허가·국제화, 중동·아랍, 일상 소재, 신규 업역, 스킬 연계 모듈
- 확인된 사실과 추론을 구분하는 단정형 문체 규칙
- ChatGPT 프로젝트에 복사할 최소 부트스트랩 지침

### Changed

- 저장소의 역할을 카드뉴스 전용 킷에서 전체 콘텐츠 운영체계로 확장
- 마스터 v6.8은 최신 채널 지침과 충돌하지 않는 장기 전략에 한정
- `단정 대신 여지`를 `확인된 사실은 단정하고 불확실성만 한정`으로 교정
- 구버전·중복 지침을 MANIFEST에서 비활성화

### Preserved

- 기존 카드뉴스 렌더링·QA·브랜드·폰트·템플릿 경로
- Source Lock, 사용자 승인, 국·영문 별도 QA 절차
