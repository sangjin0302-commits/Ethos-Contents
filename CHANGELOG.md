# Changelog

## 2026-10-06 — 카드 디자인 결함 수정

- 크림 카드의 결론 `close` 박스: 그림자 제거(그림자만 있고 안쪽 여백이 없어 글자가 박스 왼쪽 끝에 붙어 보였다). 윗줄 한 줄 스타일로 정리.
- 라벨과 본문 사이 간격 14→22px, 본문(`.rule-copy`) 두께 700→500으로 라벨이 먼저 읽히게 위계 수정.
- 강조 밑줄(`.mark-hl`)을 글자 크기에 비례(두께 `max(2px,.09em)`, 간격 `.24em`)하게 바꿔 두 줄에 걸쳐도 아랫줄과 겹치지 않는다.
- 흐름 박스 설명에 `text-wrap: balance`. 시각 회귀 기준 이미지 3장 갱신(의도한 변경). 스트레스 22건 통과.

## 2026-10-06 — 아이콘 이름 .svg 허용

- ChatGPT가 `icon`에 파일 이름(`scale.svg`)을 확장자까지 써서 스키마가 거부했다. 스키마와 빌더, 출처 점검이 `.svg`가 있든 없든 같은 아이콘으로 받는다(경로 문자는 계속 거부). 시험 결과(TEST-SUSPENSION-V3): 평균 174자, 모든 카드 아이콘, 표지 art, bars, QA 통과.

## 2026-10-06 — 승인 세트 덮어쓰기 복구

- ChatGPT 시험 중 승인 세트 `SUSPENSION-SURCHARGE-04`의 `brief.md`·`card-data.ko.json`·`distribution.md`가 main에 직접 덮어써졌다(6f61598, 2a951d7, 1096069). 승인본(렌더 결과와 같은 버전)으로 되돌렸다. 덮어쓴 버전은 git 기록에 남아 있다.
- 프로젝트 지침: 승인된 세트를 덮어쓰지 않고(새 폴더에 쓰거나 먼저 묻는다) main에 직접 쓰지 않는다. `editorialReview` 단계 값은 `pass`·`pending`만 쓴다.
- 시험 결과(새 카드): 평균 174자, 모든 카드에 아이콘, 표지 art, bars 사용, QA 통과(스키마만 `factCheck: source-lock` 오류).

## 2026-10-06 — ChatGPT 시험 결과 반영

- 실측(SUSPENSION-04 국문 카드, ChatGPT 6분 53초): 평균 보이는 글자 238자(승인본 133자). QA는 카드 10에서 가로 넘침으로 FAIL이었다. 원인은 가운뎃점 묶음이 줄바꿈 없는 18자 덩어리가 된 것이라 v2 세트의 묶음은 14자까지만 줄바꿈을 막는다(승인된 세트의 최장 묶음은 13자라 결과가 바뀌지 않는다).
- 린터: `dense-set`(평균 220자 초과, 글자가 작아짐), `plain-set`·`plain-cover`(icon·art·hero·stats/bars를 거의 안 쓴 세트). 시험본은 표지 art와 icon을 하나도 쓰지 않았다.
- 프로젝트 지침 빠른 경로에 시각 요소 필수와 평균 150~200자 목표 추가.

## 2026-10-06 — 아이콘 전체 세트

- Lucide(ISC) 2130개, Tabler(MIT) 5184개 전체 아웃라인 세트를 보관한다(약 4MB). 기존 파일과 변환(라이선스 주석·class 제거)이 동일함을 확인했다. 추천 목록(용도별)은 README에 유지하고, 없으면 파일 이름으로 찾는다. `scripts/icon_svg.py --search <낱말>` 추가. 이름 충돌 시 Lucide 우선.

## 2026-10-06 — 블로그 경로 분리·막대 비교 카드·Tabler 아이콘

- 블로그 작성 경로를 **A 일반 / B 심층 조사 / C 파생**으로 나눴다(`docs/blog-authoring-spec.md`). 법률 정확성·경험 창작 금지·업무범위·CTA 한 번·숫자 보존·의미 재검증만 Hard Gate, 제목·구조·마케팅 기법은 Soft Guide. 최종 점검은 세 질문(첫 5문단의 답, 구별되는 검토 방식, CTA 없이도 남는 정보)만. 점수로 재작성을 강제하지 않는다.
- 조사 잠금 `research/`: 시리즈별로 한 번 검증한 법령·판례·통계를 저장하고, 후속편은 기준일 이후 변경 여부만 확인한다.
- 프로젝트 지침: 매번 MANIFEST와 전체 지침을 읽지 않고 작업 유형별로 필요한 문서만 읽는다. 순차 6패스를 "자연 초안 → 법률 검증 → 제목·도입·차별점·CTA 편집 → 어색한 문장만 윤문 → 재확인"으로 줄였다.
- 막대 비교 카드: `checklist` `layout:"bars"`(같은 단위 숫자 2~3개, `value`=길이·`display`=보이는 숫자). 린터 `bars-data`·`bars-units`, 스트레스 검증 포함.
- Tabler Icons(MIT) 63개를 `assets/icons/tabler/`에 추가(기관·서류·차트·기한). Lucide에 없는 이름만, 빌더는 Lucide 우선. 출처 기록은 `tabler/<이름>.svg`.

## 2026-10-06 — 카드 정보량 상향·빠른 경로 단순화

- 필드 한도 상향(`card-limits.json` 1.1): 유형별 본문 글자 한도를 1.5배(숫자 목록·CTA 6칸은 1.25배)로 올렸다. 올리기 전에 1.0~2.2배를 렌더로 시험해 최악 조건(줄바꿈 없는 긴 키, 네이비·크림 교차, 국·영문)에서 넘치는 지점을 확인했고, 전체 `spec_stress` 22건이 통과했다. 기존 한도는 안전 여유가 과해 카드가 얇게 나오는 원인이었다. 표 값은 `docs/card-authoring-spec.md`와 같게 갱신.
- 정보량 린트: `thin-set`(카드 평균 보이는 글자가 국문 150자·영문 330자 미만), `thin-cards`(하한 70% 미만 본문 카드 3장 이상). 권고이며 `Render cards`에도 표시. 명세에 "정보량" 절(저장용 카드 한 장, 항목마다 조건·기준·예시) 추가.
- 빠른 경로: 국문 먼저, 영문은 별도 요청. 윤문·재검증 패스를 빼고 검증은 CI(`--compare`, 린터)가 맡는다. 읽는 문서는 명세·철학·블로그 원문 3개로 줄였다.

## 2026-10-06 — 독자 표현·웹사이트 FAQ·대안 표지

- 더 자연스러운 시각 요소: IRA Design(MIT) 손그림 선화 물건 13종·인물 6종(`assets/illustrations/hand/`, 토큰 색, 선 굵기 2.4px 고정)과 Rough Notation(MIT) 손으로 그은 밑줄·동그라미(`vendor/rough-notation/`, `templates/annotate.js`, 난수 고정). 시안 E 수정(차분한 표정·단색 상의·부제 삭제·밑줄), F 서류+도장 장면, G 손그림 달력+밑줄. 가이드 10-0-3·10-0-4절.
- 생활 장면형 표지: Open Peeps(CC0) 인물 5종을 브랜드 색 토큰으로 바꿔 `assets/illustrations/people/`에 넣었다. 사용자 피드백으로 **크림 표지에서만** 쓴다. 시안 E(크림, 사전통지서를 든 사장님). 네이비용으로 Phosphor duotone(MIT) 물건 그림 30종 `assets/illustrations/objects/`(선은 배경 반대색, 면은 골드)과 시안 F(도장). 크림 표지 글자는 네이비(프리셋 A). `copy_lint.py`가 `data-asset` 출처 기록 누락을 경고. 가이드 10-0-3절, 자산 정책.
- 국문 문체 오픈소스: `scripts/prose_hints.py`와 `Prose hints` 워크플로. MuncheKit v0.2.0(MIT, `.munche.json`)이 번역투·생성형 상투 대구·명사화·겹말·근거 없는 강조·문두 접속어를, ko-mt-lint(MIT, 커밋 고정)가 LLM 초안의 활용 오류·조사 중복을 원고 PR 댓글로 알린다. 법률 한정어를 지우라는 KO-POSS-001과 잡음 규칙(KO-PARA·KO-END)은 끔. 기존 블로그 3편 실측 12건. 상투 표현 목록에 "도움이 되셨기를", "결론적으로" 등 추가.
- 리뷰 반영: 표지 시험은 같은 채널·시간대의 연속 세트에서만 비교(다르면 "비교 불가"), 상담 질문의 전화번호(공백·점·+82)도 제외, FAQ 답은 `A. `만 인정, 프리셋 A 흰색을 토큰(`--ethos-white`)으로.
- 독자 표현: `scripts/reader_phrases.py`가 Search Console·네이버 서치어드바이저 검색어 CSV와 상담 질문(익명)을 모아 `state/reader-language.md`(질문형 검색어, 노출 상위, 제목을 바꿔 볼 검색어, 주제 낱말)를 만든다. 전화·이메일·주민번호 형태 줄은 버린다. 블로그 명세·성과학습·프로젝트 지침이 제목·첫 문장·FAQ 질문에 이 표현을 쓰게 한다. 웹사이트 문의 내보내기에는 본문이 없어 검색어를 기본 자료로 삼았다.
- 웹사이트 FAQ: 웹사이트가 본문의 `Q.`/`A.` 문단을 FAQPage 구조화 데이터로 자동 변환한다(Admin-system `extractFaqPairs`, `faq_schema_auto` 기본 켜짐). `docs/website-md-spec.md` 7절을 이 형식으로 바꾸고, `validate_website_md.py`가 굵게·목록 Q나 짝 없는 Q를 경고. 예시 MD에 FAQ 2쌍.
- 대안 표지: 표지 카드 `altCover`(Hook 유형 situation·question·contrast·number) → `<lang>/alt/card_01.html`. `Render cards`가 카피 잠금과 QA를 따로 보고, 성과학습 "표지 시험"과 배포 양식 "Cover test"로 비교. 프리셋 A `.cv-stat`(큰 숫자 대비). 예시 국·영 대안 표지(6개월 → 3개월)와 `out/cover-ab.png`.

## 2026-10-06 — 오픈소스 보강: 인용 검증·띄어쓰기·영문 문체·아이콘·명조 제목·마케팅 스킬

- 리서치: 인용 검증 단계 추가. `docs/legal-verification.md` 6절(korean-law-mcp `verify_citations` 또는 국가법령정보센터 수동 확인, `citations.md` ✓/✗/⚠ 기록), 오프라인 인용 추출기 `scripts/extract_citations.py`와 테스트, `vendor/korean-law-mcp/`(MIT 출처 기록), `.codex/config.example.toml`(인증키는 `LAW_OC` 환경 변수).
- 국문 윤문: `copy_lint.py`가 kiwipiepy로 띄어쓰기 교정 후보를 알려 준다(`spacing`, info). 표준과 맞는 두 경우(의존 명사 띄우기, 명사+하다 붙이기)만 남기고 합성어 분리·비표준 붙임 제안은 버린다.
- 영문 윤문: Vale(MIT) `.vale-en.ini`(Microsoft·write-good·proselint, 수동태·한정어 지적은 끔). `copy_lint.py`(`en-vale`)와 `validate_website_md.py`(INFO)가 힌트를 보여 주고, `Render cards` 워크플로가 설치한다. 기존 국문 금지 표현용 `.vale.ini`는 그대로.
- 디자인: Lucide 아이콘 37개 추가(기한·서류·체류·사업·돈·강연, 총 61개, 용도별 목록), 자유 디자인 카드용 `scripts/icon_svg.py`(`data-icon`으로 출처 기록 확인). 마루 부리(MaruBuri, OFL) 제목체와 프리셋 D(`templates/presets/ethos-d.css`, 명조 제목 + 아이콘 배지), 시안 D. 카드 디자인 가이드 10-1절.
- 마케팅: `docs/marketing-checklist.md`에 marketingskills(MIT)의 `lead-magnets`·`marketing-psychology`·`schema`를 에토스 윤리 원칙으로 걸러 받을 자료 설계(4절), 윤리적 심리 원리(5절), 웹사이트 구조화 데이터(6절)를 권고로 추가. `docs/website-md-spec.md` 7절 FAQ 후보.
- 웹사이트 MD 예시: 콜론이 든 영문 제목을 따옴표로 감쌌다(YAML 파서 호환).
- 빈칸: `qa_render.py`가 본문의 가장 긴 빈 가로 띠를 재서 22%를 넘으면 권고(`empty-band`, `gates.json` `layout.maxEmptyBand`). 프리셋 A의 두 항목 비교를 위아래 배치로, 표지 일러스트 340px·제목 43px. 예시 세트 국문 빈 띠 최대 36% → 21%(표지 32→21%, 5번 36→11%). 가이드 10-0절.
- 시각 중심: 본문 카드마다 `data-focal` 하나(36px 이상 글자 또는 큰 아이콘). `qa_render.py`가 카드별(no-focal·weak-focal)과 세트(본문 카드 60% 미만) 권고. 예시 세트 0/6 → 6/6장, 마무리 카드 상자를 위아래로 바꿔 줄바꿈 정리. 가이드 10-0-1절, 브리프에 시각 중심 칸.
- 카드 문구 두 단계: 말로 한 초안 → 카드로 줄이기(`docs/card-authoring-spec.md`, 브리프 칸, 프로젝트 지침). `copy_lint.py` `legalese`(카드의 법률 문서 말투, info).
- 인용 자동 대조: `scripts/verify_citations.py`(공식 MCP Python SDK로 korean-law-mcp 호출, 별표·재결은 ⚠로 사람 확인)와 `Verify citations` 워크플로(원고 PR에 결과 댓글, 시크릿 `LAW_OC` 선택). ChatGPT 커넥터 없이도 GitHub에 올리면 대조된다.

## 2026-10-06 — 상담 접수 추적 링크

- `scripts/tracking_link.py`: content_id·채널·언어별 `/intake` 추적 링크(source·channel·content_id·placement)를 만든다. 웹사이트 `/admin/funnel`이 이 값으로 글·채널·위치별 문의를 집계한다. utm_는 쓰지 않는다.
- `distribution.md` 양식에 추적 링크 열, 전략 플레이북 5절·6절, 글감관리표 마케팅 점검(관리자 집계를 "유입글"보다 우선), 프로젝트 지침에 링크 형식.
- 마케팅 점검: 출처 미상 문의 분리, 시리즈 매핑이 있을 때만 시리즈 성과 계산, 세트별 결정은 `performance-log.csv` 유지.

## 2026-10-06 — 글감관리표로 마케팅 점검

- `docs/topic-log-integration.md`에 "마케팅 점검" 절: 주간 성과 탭으로 조회 추세, 문의 전환, 문의 유입 주제, 조회 상위 주제, 관심과 문의의 어긋남, 시리즈 성과, AI 인용 증가를 계산하고 "다음 4주에 바꿀 것"으로 끝낸다. 표에 추가하면 좋은 열(문의별 content_id·유입 채널, 카드 저장 수)을 적었다.
- 프로젝트 지침·AGENTS·전략 플레이북: 마케팅·성과 분석 요청은 글감관리표 주간 성과 탭을 기준 자료로 쓴다.

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
