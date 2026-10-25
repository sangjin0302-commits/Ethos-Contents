# 2026-10-25 — 의미 보조 SVG와 OEM 시각 편집 기본 적용

사용자 요청으로 일괄 이모지 금지를 로컬 SVG 의미 보조 허용으로 변경. 새 카드 초안·직접 디자인·제작 안내에 문서 대조와 법률 조건 묶음 연결. Twemoji v14.0.2 7종·CC BY 4.0 출처 보관, OEM 별도 초안과 실제 렌더 비교 추가. 승인 원고 불변, 게이트·자동 축소 정책 유지. 디자인 고정 지문은 승인된 지침 변경만 갱신.

# Changelog

## 2026-10-24 — Standalone website titles (user-requested policy correction)

- Supersede the website-title rule introduced on 2026-10-23 in c7f9339: omit series names and issue numbers from both `title` and `titleEn`, using concise standalone search questions.
- Keep the full series name and issue in Naver blog titles; retain the existing omission in KakaoTalk Channel and LinkedIn titles.
- Preserve series lineage through existing content IDs, file paths, internal metadata or distribution records. Do not invent website MD frontmatter keys.
- Keep website bodies free of greetings, series tables of contents and direct series links. Do not retroactively change published titles, article bodies, sources or legal content.
- Align the website spec, website channel guide, blog spec, MANIFEST and project instructions; refresh the three affected frozen guideline fingerprints under the user's authorization. No website application code changes.

## 2026-10-23 — Channel-specific series title visibility

- Show the full localized series name and issue in blog and website titles.
- Start KakaoTalk Channel and LinkedIn titles/first lines with the standalone topic instead of a series prefix.
- Keep series lineage in internal content IDs, filenames and distribution records; leave general chat output and other social-channel title rules unchanged.

## 2026-10-23 — 블로그 분량 상한 완화·독자 이해 우선

- 사용자 요청: 법률 설명을 8,000~11,000자에 맞추느라 필요한 사례·조건·문서 대조를 생략하는 문제를 해소. `docs/blog-authoring-spec.md`와 `PROJECT_INSTRUCTIONS.md`에서 8,000~11,000자는 과거의 참고 범위로만 남기고 **고정 상한을 폐지**. 복잡한 칼럼은 12,000~20,000자 이상도 설명 필요에 따라 허용하며 새 글자 수 할당량을 만들지 않음.
- `scripts/copy_lint.py`에서 11,000자 초과 `long-blog` 안내를 제거. 7,000자 미만 `short-blog`는 필수 근거·조건 누락 가능성을 알려주는 비차단 참고 경고로만 보존. `tests/test_copy_lint.py`에 장문이 분량만으로 경고되지 않는 회귀 테스트 추가.
- `docs/language-quality-workflow.md`의 11,000자 길이 맞춤 문구를 중립적인 설명·중복 기준으로 변경.
- `examples/writing/README.md`와 사용자 화장품 ⑦편 샘플의 '19,201자 초과=문제' 판정을 제거. 긴 문장의 설명력과 의미 없는 반복을 분리하고, 사용자가 명함·CTA를 넣으며 생성된 네이버 편집기 흔적을 원고 결함으로 단정하지 않도록 수정. 원본 참고 본문·법률 주장·카드 Source Lock은 보존.
- `state/design-freeze.json`의 고정 SHA-256은 블로그 명세와 프로젝트 지침 두 파일만 갱신. 기존 법률 정확성·무료/유료 CTA·카드 디자인/렌더러·승인 콘텐츠는 변경하지 않음.

## 2026-10-23 — 화장품 표시·광고 ⑦편 사용자 편집 참고 예시

- 사용자가 전체를 통합·편집해 제공한 화장품 패키지·광고 ⑦편을 `examples/writing/samples/cosmetics-label-07-user-edited-20261023.md`에 **문체·서사·서류 대조 참고자료**로 보존. 네이버 에디터의 출처 입력·공백 엔터티·이스케이프만 정리하고 본문 법률 주장·숫자·조건은 임의 수정하지 않음.
- `examples/writing/README.md`에 현실적인 제조·디자인 작업 질문, 5mL/30mL 소용량 비교, 복합원료 2%와 완제품 성분 함량의 차이, 실제 자료 요청과 무료 사전 검토·별도 유료 작성 설명을 선별해 소개.
- `scripts/writing_context.py`의 기존 목적별 최대 3개 예시 중 각 1개를 새로운 ⑦편 문단 예시로 교체. 특정 주제의 법률 결론이 자동으로 다른 글에 적용되지 않도록 정본·검증 경계를 보존.
- 사용자 파일 약 19,201자(편집기 잔여물 포함)의 과도한 분량, 반복된 제조번호·사용기한 설명, 편집기 표시와 누락된 발행용 제목·상담 이미지 등을 보호선으로 기록. 법률 적합성·최종 발행 승인·마케팅 성과를 인증한 것이 아님.
- 기존 `content/` 글·승인 카드·디자인·고정 지침 지문(`state/design-freeze.json`)·MANIFEST는 변경하지 않음.

## 2026-10-23 — 전체 블로그 원고 윤문의 단락별 품질 실행 기준

- 사용자 직접 요청: `docs/blog-authoring-spec.md`의 기존 윤문·의미 재확인 순서에서 **전체 원고를 실제 소제목별/앞뒤 문단 문맥으로 읽는 실행 방법**을 구체화. 단순 문법 교정·낱말 치환에 그치지 않고 질문→근거→조건→자료→다음 행동의 설명과 단락 연결을 살핀다.
- 이미 자연스러운 문단과 승인 원고는 보존하고, 문제가 있는 구간만 국소적으로 편집한다. 추가 단계·강제 수정 개수·점수표·새 도구 호출 의무는 만들지 않는다.
- CI의 형식·인용 확인은 자연스러움/법률 해석 보증과 구분하며, 실제 읽은 본문과 변경한 구간만 검수 완료로 보고한다.
- 사용자가 직접 요청한 고정 지침 변경이므로 `state/design-freeze.json`의 `docs/blog-authoring-spec.md` SHA-256만 기록 갱신. 다른 17개 고정 파일, 콘텐츠, 카드 렌더러·디자인·한도는 불변.

## 2026-10-21 — User-edited paragraph-level blog explanation reference

- Add the user's complete cosmetics functional review/report ⑥ editing sample as a **style reference, not legally approved or publish-ready content**. Remove only editor artifacts, whitespace and a few obvious typos; retain statutory qualifiers and preserve the already merged public article unchanged.
- Add concrete blog writing guidance: show the exact document, compared fields, condition-dependent outcomes and the next action; answer a section's closing question before moving to another legal route; do this in the first full draft, not only after user requests paragraph-by-paragraph repairs.
- Link three selected new examples (opening / argument flow / localized polishing) into the existing `writing_context.py` retrieval path while keeping its maximum of three examples per purpose and its original safety rules.
- Update only the frozen `docs/blog-authoring-spec.md` fingerprint with explicit user-requested change history. No card-design/rendering gates, approved blog, or marketing data changed.

## 2026-10-20 — CI follow-up and measured comparison

- Fix changed-set selection so HTML, CSS and source-only edits actually trigger card rendering without changing locked JSON.
- Fix long Korean/English series headers in both renderers; retain full metadata in a two-line slot without moving the fixed wordmark.
- Reuse existing approved deterministic HTML in CI instead of silently redesigning it; verify exact JSON reconstruction or copy lock, then run hard QA.
- Add regression coverage for design/source changes and removed/non-card folders.
- Record same-browser typography measurements, baseline/current test collection and the unresolved external OASIS certificate failure in `docs/reviews/2026-10-20-ci-followup.md`. Keep TLS validation intact.

## 2026-10-20 — Reader-first card rendering and contextual writing

- User-authorized update: keep design warnings advisory for approved sets; preserve hard QA and fallback-production checks. Remove the icon-count quota and avoid claiming visual approval from HTML heuristics.
- Render proportional bars including zero; preserve tiny values and explicit cover choices. Unordered lists no longer acquire step numbers.
- Production HTML measures overflow without shrinking text; preview fitting is limited to 8% and reported. Improve OEM condition typography and remove decorative checklist numbering while preserving all approved copy.
- Connect selected, exact user-edit examples to drafting commands and the actual polish request. Check argument flow before local sentence edits; preserve approved manuscripts and all legal conditions.
- Separate new language completion status from method, accept historical records without migration, and clear completion metadata when suggestions are applied.
- Add regressions for CI advisory behavior, chart proportions, intent, fitting, metadata and example retrieval. Validation evidence: `docs/reviews/2026-10-20-editorial-refinement.md`.

## 2026-10-18 — OEM editorial hierarchy without copy changes

- Simplified cover chrome, separated responsibility columns, introduced an open change timeline and reserved filled emphasis for the final CTA.
- Grouped English card 7's three exception factors without changing any source words or legal qualifiers; kept 21px body type.
- Added browser assertions for visual hierarchy, legal groups, unshrunk type and headline bounds. Shared renderer, thresholds and prior footer fix remain unchanged.

## 2026-10-18 — Footer separation and topic-specific OEM cover

- User-requested footer repair: explicit 4px track, aligned fill and 8px clearance below the page label. Browser regression covers both languages and all ten progress values.
- Original cosmetic pump, cream jar and record illustration replaces the generic cover clipboard; reusable generator mapping added.
- English card 7 uses a shorter title and plain-language copy at 21px instead of 19px. All three exception factors, record duty and confidentiality boundary remain; no new legal claims.
- Real PNGs and visual baselines regenerated; approval to publish remains separate.

## 2026-10-18 — 테스트 회귀 수정 및 영문 법률 카드 가독성 마감

- 사용자 요청으로 explicit legacy 세트의 진행 표시를 제외해 승인 HTML 재생성 호환성을 복구했다. 새 세트와 버전 미지정 입력은 진행 표시를 유지한다.
- 법률 도구 통합 테스트의 가짜 서버를 실제 검증기가 소비하는 MCP TextContent 계약으로 명시했다. 네트워크 왕복과 검증 결과 assertion은 그대로 유지한다.
- 영문 OEM 7장 카피는 그대로 두고 상자 패딩을 읽기 폭으로 전환했다. 본문 17→19px, 축소율 1.00 및 넘침 없음의 실제 브라우저 회귀 테스트 추가.
- 이전 프레임 개선에 뒤처진 시각 기준 PNG 5장을 갱신했다. 변경 전후 본문 영역(y=122..1219)의 픽셀 차이가 0임을 확인하고 머리말·꼬리말·진행 표시를 직접 검수했다. 비교 허용치는 유지한다.

## 2026-10-18 — COSMETICS-OEM-04 국·영문 실출력 디자인 마감

- 사용자 요청에 따라 표지·질문·절차·법률 구분·자료 목록·CTA를 세트 전용 디자인으로 통합하고 국·영문 PNG를 직접 검수했다.
- 긴 법률 조건은 좁은 비교 열 대신 세로 패널로 배치하고, 질문 번호의 실제 위치 오류와 영문 자동 분철을 수정했다.
- 제작용 생성 경로, 언어별 구성 회귀 테스트, 실제 글자 축소율·잔여 넘침 QA를 추가했다. 기존 게이트는 완화하지 않았다.
- 20장 출력과 자동 검사 결과, 의도한 쉼 카드 여백 및 밀도 권고는 해당 세트의 review.md에 기록한다. 발행 승인은 별도다.

## 2026-10-18 — 체크리스트 아이콘 시스템 통합

- 판단 질문과 준비 자료 카드의 핵심 아이콘을 공통 크기·내부 여백·선 굵기의 아이콘 플레이트에 배치했다.
- 크림 카드에는 흰색 표면, 네이비 카드에는 딥 네이비 표면을 사용해 배경별 대비를 유지하면서 세트 일관성을 높였다.

## 2026-10-18 — 브랜드 색·표면 토큰 통합

- 금색·네이비 RGB 토큰을 추가하고 반투명 강조선도 정식 브랜드 색에서 파생되도록 통일했다.
- 기본·상승·행동 표면의 그림자 토큰을 추가해 패널별 명도와 깊이가 임의 값으로 흔들리지 않게 했다.

## 2026-10-18 — 핵심 수치 비교 균형 강화

- 전·후 수치 비교에서 한쪽만 박스로 보이던 비대칭을 해소하고 두 값을 같은 높이의 패널로 묶었다.
- 화살표를 패널 중심축에 고정하고 전·후 배경·그림자 차이를 유지해 변화 방향을 더 빠르게 읽게 했다.

## 2026-10-18 — 전 카드 진행 표시 통합

- 모든 카드 생성 경로에 `현재 장 / 전체 장`과 진행 막대를 기본 적용해 캐러셀 위치를 즉시 알 수 있게 했다.
- 금지된 CSS 그라데이션 없이 회색 트랙과 금색 가변 폭을 겹치는 방식으로 진행 막대를 다시 구현했다.

## 2026-10-18 — 본문 정보 카드 일괄 강화

- 법률 근거의 두 층을 흰색 패널과 서로 다른 왼쪽 기준선으로 구분해 법률 상한과 세부 기준의 관계를 빠르게 읽게 했다.
- 판단 질문에는 금색 원형 마커와 얕은 그림자를 추가해 질문 단위의 스캔성을 높였다.
- 준비 자료는 체크박스형 행으로 전환하고 첫 핵심 자료를 별도 강조해 실제 준비 순서를 쉽게 파악하게 했다.

## 2026-10-18 — 절차 카드 타임라인 강화

- 절차형 카드의 번호를 원형 배지로 바꾸고 금색 연결선을 추가해 네 항목이 독립 목록이 아니라 순차 흐름으로 읽히게 했다.
- 텍스트 정렬과 행 간격을 배지 중심에 맞춰 국문·영문의 빠른 훑어보기를 개선했다.

## 2026-10-18 — 비교 카드 판단 영역 분리

- 비교형 카드의 두 판단 영역을 독립 패널로 분리하고 금색·크림색 왼쪽 기준선으로 읽는 순서를 만들었다.
- 단순 구분선을 제거하고 배경 명도와 그림자 차이를 사용해 작은 화면에서도 두 조건이 한 문단처럼 뭉치지 않도록 했다.

## 2026-10-18 — 표지 시각 중심 강화

- 표지 핵심 일러스트를 확대하고 선 굵기·명도·그림자를 보강해 작은 피드 썸네일에서도 주제가 먼저 보이도록 했다.
- 표지의 보조 약속 문구를 얇은 금색 캡슐로 묶어 제목·설명·시리즈 신호의 위계를 분명히 했다.

## 2026-10-18 — CTA 카드 시선 흐름 강화

- CTA 제목 아래에 짧은 금색 기준선을 추가하고, 직접 확인·종합 검토 카드의 왼쪽 강조선을 통일했다.
- 최종 무료 1차 확인 문구를 금색 테두리와 더 강한 그림자로 분리해 마지막 행동이 다른 정보 블록에 묻히지 않도록 했다.

## 2026-10-18 — 모바일 브랜드 프레임 가독성 강화

- 카드가 피드에서 축소되어도 상단 워드마크·섹션명과 하단 사무소명·태그라인을 읽을 수 있도록 글자 크기와 굵기를 소폭 높였다.
- 본문 좌표와 안전영역은 유지해 기존 카드 레이아웃에 영향을 주지 않도록 했다.

## 2026-10-18 — 영문 비교 숫자 단위 줄바꿈 보정

- 영문 전후 비교 카드의 큰 숫자·단위 묶음이 좁은 셀에서도 분리되지 않도록 크기와 줄바꿈 규칙을 보정했다.
- 국문·영문 16장 전수 렌더 시트에서 발견한 `3 month / s` 고립 줄바꿈을 해소했다.

## 2026-10-18 — 국문·영문 카드 디자인 시스템 통합 강화

- 사용자의 전반 강화 요청에 따라 아랍어는 범위에서 제외하고 국문·영문 카드만 대상으로 했다.
- 자유 디자인 HTML·`design.css`·공통 템플릿·브랜드·폰트·아이콘·일러스트 변경도 `Render cards`를 실행하도록 경로를 보강했다.
- 같은 시각 중심과 같은 본문 구조 반복, 그림 부족을 디자인 경고로 승격했다. 실제 승인본은 디자인 경고나 기본 빌더 fallback이 남으면 발행용 QA를 통과하지 못하게 했다. 승인 전 자동 미리보기는 기존처럼 생성한다.
- 렌더 결과에 `render-manifest.json`을 추가해 원본 커밋, card-data·design.css SHA-256, 카드별 free·auto·builder·fallback-builder 모드와 QA 결과를 기록한다.
- 국문 커닝을 안정화하고 영문 본문에는 실제 단어 줄바꿈·optical sizing을 적용했다. 제목은 임의 하이픈을 막고 균형 줄바꿈을 유지했다. 프리셋 A의 CTA는 직접 확인과 종합 검토 경계, 그림자, 결론 띠를 강화했다.
- 디자인 반복 경고와 승인 표시 판별 회귀 테스트를 추가했다. 기존 법률 문구·국영문 카드 JSON·승인 콘텐츠는 변경하지 않았다.
- 사용자 승인에 따른 디자인 고정 지문을 갱신한다.

## 2026-10-17 — 기승전결이 약한 법률 칼럼 예방을 위한 서사선 지침 보강

- 사용자가 화장품 인허가 ④편을 읽고 지적한 독립 질문 나열·도입 사례 단절·결말의 문제 회수 부족을 이후 새 블로그에서 예방하도록, `docs/blog-authoring-spec.md`와 `guidelines/channels/blog.md`에 중심 질문의 출발·발전·전환·회수에 관한 Soft Guide를 추가했다.
- `docs/content-architecture-system.md`는 홈페이지·SNS·카드·다국어 파생에서도 원문의 판단 흐름과 다음 행동이 유지되도록 요약했고, `examples/writing/README.md`에는 OEM 계약 ④편의 기존 흐름과 권장 재배치 예시를 추가했다.
- 첫 5문단 안의 직접 답, 실제 법령·예외·숫자·판례 근거, 기존 정식 시리즈명, 말미 무료 사전 검토 한 번과 유료 문서 작성 구분을 보존한다. 인물·극적 사건·고정 네 단계·검수 점수표·추가 유료 도구 사용을 강제하지 않는다.
- **사용자 승인에 따른 고정 지문 갱신:** `state/design-freeze.json`의 `docs/blog-authoring-spec.md` SHA-256만 새 원문과 일치하도록 변경 이력을 남겼다. 사용자의 기존 발행 원고와 카드 렌더러·스키마·한도는 변경하지 않았다. 이력은 새 글부터 적용하며 기존 발행 ④편을 자동 수정하지 않는다.
- GitHub Actions의 고정 지문 검사와 링크·회귀 검사를 통과한 뒤 `main`에 반영한다. 검사 실행 여부와 최종 결과는 실제 작업 로그를 따른다.

## 2026-10-17 — 전면 재검토 후 im-not-ai 표지 실제 노출 문구와 검사 연결 보완

- PR #51~#53 병합 이후 코드 리뷰 및 실제 카드 렌더링 분기를 대조해, 숫자(hero)와 그림(art)을 함께 가진 표지는 선택된 디자인에서 보여 주는 문구만 문체 검사하도록 수정했다. auto_design의 회차별 number/picture 선택을 직접 사용하며 다른 표지 문구를 기계적으로 경고하지 않는다.
- 실제 표시되지 않는 카드 유형의 필드도 제외한다. 흐름 카드 이외의 note, 질문 체크리스트·단계 카드의 숨겨진 body.key, 막대가 아닌 카드의 display를 언어 분석에 보내지 않는다. 표 머리글·실제 보이는 항목명·선택적 대안 표지 문구는 유지한다.
- im-not-ai 추출기 또는 Prose hints 공유 추출기의 변경만으로도 Prose hints를 재실행하도록 GitHub Actions 경로를 보완하고, 오래된 워크플로 주석을 정정했다.
- CI에서 패키지 방식과 단독 스크립트 실행 방식 모두 정상적으로 카드 렌더러의 읽기 전용 함수를 불러오도록 import 경로를 수정했다. 자동 디자인이 QA에 실패해 기본 렌더러로 대체되는 경우에는 표지의 숫자 설명도 표시될 수 있으므로 해당 후보를 별도 라벨로 진단한다(기본 그림 표지 문체 지표와 혼합하지 않음).
- 회귀 테스트에 기본/숫자/그림 표지 분기와 숨겨진 필드 구분을 추가했다. 승인된 원고, 자동 카드 렌더러, 고정된 디자인/작성 명세, 디자인 지문, 법률 근거·상품·CTA 범위는 변경하지 않았다.

## 2026-10-17 — PR #51 문체 지침 보강에 따른 design-freeze 지문 갱신

- 사용자가 지적한 `설명해서는 안 됩니다`, `적용해서는 안 됩니다` 등의 집필자용 지시형 표현을 독자용 사실·기준·행동으로 바꾸는 블로그 지침을 사용자 요청에 따라 개정했다.
- PR #51에서 빠졌던 `state/design-freeze.json`의 `docs/blog-authoring-spec.md` SHA-256 지문만 새 원고에 맞춰 갱신하고 변경 이유를 이력에 기록했다. 다른 17개 고정파일과 카드 렌더러·스키마·기존 승인 콘텐츠는 바꾸지 않는다.
- GitHub Actions `test_design_freeze` 실패 원인인 기록 불일치를 바로잡는다. 자동 검사 통과는 실행 결과를 별도로 확인한다.

## 2026-10-17 — PR #52 리뷰 후속: im-not-ai 공개 국문 문구 추출 누락 보완

- scripts/im_not_ai_review.py: 레거시 distribution.md의 '## Korean' 위쪽 '핵심 문구'·'네이버 블로그·카카오톡 채널'·'SNS 캡션' 등 국문 게시 문구도 읽고, 기존 '## Korean' 섹션의 한국어 캡션·alt text와 함께 검사한다. 영문·아랍어·상담 추적표·성과 메모·해시태그·추적 URL은 제외한다.
- 카드 JSON에서는 실제 화면에 나오는 헤더(series, issue, coverLabel), 표 머리글(head), 항목명(body.key), 막대 표기(body.display), 표지 수치·설명(hero), 갈래 텍스트(paths), 대안 표지 문구(altCover)까지 보존해 추출한다. design, sourceTrace, angle, 막대 길이 value 같은 내부 데이터는 제외한다.
- 같은 편집상 누락이 발생하지 않도록 scripts/prose_hints.py의 국문 추출을 im-not-ai와 공유한다. 읽기 전용이며 자동 수정·외부 LLM 호출·법률 검증을 추가하지 않는다.
- tests/test_im_not_ai_review.py, tests/test_prose_hints.py에 구버전 실제 배포안과 렌더 필드, 내부 메타데이터 제외에 관한 회귀 테스트를 보강했다. 기존 승인 콘텐츠·카드 디자인·렌더러·스키마·제품·접수 링크 불변.


## 2026-10-17 — im-not-ai 전체 파이프라인을 에토스 국문 윤문·PR 진단에 연결

- 기존에 동봉된 humanize-korean quick-rules만 적용하던 범위를 확장했다. upstream `epoko77-ai/im-not-ai` v2.3.2 커밋 `b37e0206d31fffd9149bf57168d4d62eb2086bee`를 고정하고 규칙집을 같은 판본으로 갱신했다(MIT).
- 새 repo-scoped Codex 스킬 `.agents/skills/ethos-humanize/SKILL.md`에서 상위 공식 진단·윤문·`verify_gates.py`·필요할 경우 finalize까지 실행하도록 연결했다. 집필자용 금지 지시를 독자에게 필요한 사실·근거·행동으로 바꾸되 실제 법률상의 금지·재량·한정어는 그대로 보존한다.
- GitHub `Prose hints`의 국문 PR 문체 검사에 핀 고정된 상위 정량 shim을 추가하고 `scripts/im_not_ai_review.py`가 참고 지표와 구체적인 어색한 구절 후보를 보고하도록 했다. 원본 글을 자동 수정하거나 별도의 외부 유료 AI API를 호출하지 않는다. 소스 취득 실패는 검사를 통과했다고 하지 않고 미실행으로 기록한다.
- 새 회귀 테스트를 추가했으며 예전 승인 원고와 카드 렌더러·스키마·상품·CTA를 수정하지 않았다. 문체 지표를 AI 작성 탐지, 법률 검증, 실제 게시 승인으로 확대하지 않는다.

## 2026-10-17 — 콘텐츠 산출물 다운로드 파일 기본 전달

- 사용자 요청: 긴 블로그 원고를 채팅에 전부 출력할 때의 로딩 부담을 줄이도록, GitHub 정본에 파일 우선 전달 원칙을 고정했다.
- `PROJECT_INSTRUCTIONS.md` 및 블로그·웹사이트 MD·비블로그 SNS·카드뉴스 빠른 명세에 매체별 실제 파일 이름, 채팅 짧은 링크 안내, 직접 출력 요청 우선, 가짜 파일 링크 금지, GitHub 저장·사용자 발행 승인 분리를 명시했다.
- 블로그는 `.txt`와 `.md` 두 파일, 웹사이트는 기존 `website.ko.md`·`website.en.md`, 카드뉴스는 기존 원본 JSON·브리프·배포안, SNS 완성 게시글은 채널·언어별 `.txt`를 기본으로 한다. 짧은 질문 답변은 채팅으로 제공할 수 있다.
- 법률 검증·문체·CTA·분량·Source Lock·디자인·렌더·가격·상품·접수 규칙은 변경하지 않았다. 고정 문서는 같은 PR에서 SHA-256 지문을 갱신한다. 작성 파일과 GitHub 자동 검사 결과는 작업마다 실제 상태로 보고한다.

## 2026-10-17 — ChatGPT 원고 직접 작성·GitHub 사전검수 경로 확립

- 별도 Codex 전달 없이 ChatGPT가 글 작성·공식 근거 확인·자연어 편집을 맡고, 사용자가 GitHub 검수를 요청한 경우 새 `-DRAFT` 브랜치/PR에 원고를 저장해 기존 `Prose hints`를 확인하도록 블로그 작성 명세에 명확히 했다. 기본 모든 채팅을 자동 공개하거나 승인 원고를 덮어쓰지 않는다.
- GitHub의 `Render cards`처럼 작업 브랜치에 원고를 push하면 별도 Codex나 PR 없이도 `Prose hints`가 실행되도록 했다. PR을 열면 같은 검사가 댓글에 남는다. 결과 아티팩트 `prose-review`와 블로그 `copy_lint.py`의 분량·말미 요약·필수 형식 경고를 함께 제공하되 자연스러움·법률 결론·전환 품질을 자동으로 승인하지 않는다.
- MuncheKit 설치 실패가 ko-mt-lint 설치까지 막지 않도록 설치 단계를 분리했다. 원고 파일은 자동 수정하지 않고 실제 의미 재검증 후 필요한 문장만 고친다.
- 자동 렌더링과 Codex 자유 디자인의 차이를 카드 명세에 명확히 했다. `design`의 자연어 방향은 자동 HTML로 구현하지 않고, 구조화된 `layout`·`icon` 등으로 빠른 미리보기를 만든다. 발행용 자유 디자인은 별도의 카드별 HTML/CSS와 시각 확인이 필요하다.
- 보호: 기존 `content/` 승인 세트·렌더러·CSS·스키마·가격·CTA 주소·Source Lock 불변. 고정된 블로그·카드 명세의 지문은 변경 내용과 함께 갱신한다. 실제 GitHub Actions 실행은 PR을 통해 확인한다.

## 2026-10-16 — 기존 오픈소스 문체 검사 자동 적용 및 오래된 블로그 경고 수정

- 사용자의 직접적인 활용 요청에 맞춰 PR의 `Prose hints`를 블로그·웹사이트·국문 카드 문구·한국어 SNS 캡션과 배포안으로 확대했다. 카드 JSON에서는 보이는 문구만, 배포안에서는 Korean 절만 임시로 추출한다. 원본 파일 자동 변경 없음.
- `copy_lint.py`에서 구식 '3줄 요약을 앞에, 무료 검토 안내로 끝낸다'는 경고를 제거하고 현재 순서(CTA→이미지→말미 3줄 요약→태그)에 맞췄다. 사용자가 실제 지적한 '정하는 일이 여기에 연결됩니다'를 비차단 후보로 잡는 보수적인 규칙과 회귀 테스트를 추가했다.
- 도구가 없는 환경은 건너뛰었다고 표시하며 유료 AI 윤문·API 시크릿·자동 수정은 활성화하지 않았다. 현행 법률 Hard Gate, 사용자가 편집한 원고, 카드 렌더·한도·스키마, 가격·서비스·접수 링크는 불변이다.
- 작업 상세와 자동 검사의 한계를 `docs/language-quality-workflow.md`에 기록했다. 검증은 PR CI에서 별도로 확인한다.
- `humanize-korean`의 E-1 장문 생성 권고가 '쉽고 짧은 법률 문장'과 충돌하는 점을 확인해, 외부 규칙집 원본은 그대로 두고 에토스 AI 윤문 우선 규칙에서 해당 항목을 제외했다. 유료 API 자체는 호출·활성화하지 않았다.

## 2026-10-16 — SNS·카드·웹사이트 빠른 명세에 쉬운 한국어 원칙 적용

- 비블로그 SNS(카카오·LinkedIn·Instagram·Threads·X·숏폼), 카드뉴스, 웹사이트 MD의 개별 빠른 명세에서도 한 문장 한 생각, 자연스러운 동사, 불필요한 연결말 제거를 바로 적용할 수 있도록 보강했다.
- 영문·아랍어 현지화에서는 한국어를 직역하지 않고 자연스러운 해당 언어 표현을 사용하되 법률 조건·숫자·출처·서비스 범위는 보존한다. 카드의 Source Lock·JSON 필드·글자 수·디자인 역할 분담은 불변.
- 블로그의 기존 원고와 승인 콘텐츠, 가격·상품·접수 경로, 렌더러·한도·스키마는 변경하지 않았다. 수정한 카드·웹사이트 명세의 design-freeze 지문만 사용자 요청에 따라 갱신하고 CI에서 검증한다.

## 2026-10-16 — 자연스러운 한국어 문장 예시와 윤문 기준 보강

- 사용자 지적 문장 '정하는 일이 여기에 연결됩니다'를 기준으로 짧기만 한 문장과 자연스러운 한국어의 차이를 블로그 명세·공통 언어 품질 워크플로에 명확히 했다.
- 작성·윤문에서 빈 연결말·불필요한 명사형·어색한 주어와 서술어를 살피고, 독자가 실제로 쓰는 동사로 바꾸도록 했다. 의무·재량·조건·예외를 바꾸지 않는다.
- `examples/writing/README.md`에 전/후 문장과 판단 이유를 추가했다. 새로운 전면 재작성 패스, 문장 길이 제한, 금지어 목록은 만들지 않았다.
- 기존 ③편·승인 콘텐츠·서비스 범위·렌더러·상품·가격·접수 경로는 보호하며, 고정된 블로그 명세 지문만 동일 PR에서 갱신한다.

## 2026-10-16 — 법률을 처음 접하는 독자를 위한 짧고 쉬운 문장 원칙

- 사용자 요청에 따라 공통 철학(v1.6), 블로그 빠른 명세, 전 채널 국문 언어 품질 워크플로에 '한 문장에 한 생각, 답→이유→조건의 순서, 용어 풀이, 짧은 문단'을 명시했다.
- 기존의 '문장을 자르기보다 생각을 연결한다'는 오해 소지가 있는 지시를 '짧게 쓰되 문단은 자연스럽게 잇는다'로 바꿨다. 기계적인 글자 수·문장 수·줄바꿈 규칙과 유치한 문체는 도입하지 않았다.
- 법률 정확성·주체·의무/재량·예외, 8,000~11,000자, 무료 검토 한 번, 승인 콘텐츠·카드 렌더러·상품·가격·접수 주소·Source Lock은 유지한다. 사용자 요청에 따른 블로그 명세의 변경 지문만 기존 방식으로 갱신하고 CI로 확인한다.

## 2026-10-16 — Core 6 고정 목차 오해 해소 및 반복 재작성 방지

- 사용자 요청에 따라 블로그 Core 6을 고정된 소제목·서술 순서가 아닌 완성본의 내용 점검 기준으로 명확히 했다. Traffic·Authority·Revenue의 화살표형 구성 예시는 고정 전개를 유도하지 않는 강조점으로 바꿨다.
- 상위 블로그 지침의 강제 적용 사례 개수를 해소하고, 공식 자료·조건 비교로 충분한 경우 가상 사례를 추가하지 않도록 정합화했다.
- 언어 품질 워크플로와 블로그 명세에 검수 종료 기준을 명확히 했다. 법률·업무범위·필수 형식 문제는 해당 부분에 한정해 수정하고, 선택적 문체 제안만으로 전면 재작성하지 않는다.
- 기존 Hard Gate, 블로그 8,000~11,000자, 승인 콘텐츠·렌더러·가격·접수 경로는 유지한다. 사용자 요청으로 바뀐 고정 파일은 블로그 명세 하나이며 해당 SHA-256 지문을 갱신한다. 명세·디자인 검사는 PR에서 별도 확인한다.

## 2026-10-16 — 실제 근거 우선 원칙과 전 채널 실행 기준 통합

- 최신 main `68db069`와 PR #48 head `39c017d`를 확인하고 기존 브랜치에서 이어서 구현했다. 공통 정본은 `docs/brand-philosophy.md` v1.5, 근거 선택·검증은 `docs/evidence-gate.md`로 구분하고 라우터의 중복 선언을 짧은 연결로 정리했다.
- 초안 전 관련 판결·재결·공식 질의회신·통계·보도·행정자료를 우선 검토하고 설명을 이끄는 데 사용한다. 종류별 의무 개수 없이 검증 법령·공식 안내로 대체하며, 기존 research 재사용과 채택·제외 이유의 최소 기록을 명시했다.
- 블로그·웹사이트·카드·SNS 빠른 명세에서 단독으로 실행할 요약과 기존 최종 3질문을 연결했다. 국·영·아랍어와 모든 새 글·후속편·시리즈·수정본·파생에 적용한다. 실제 사건의 대화·감정·피해액·결과 창작 금지, 예시 뒤 쉬운 설명, 승인 서비스 범위 부재 시 원문 보강·확인·승인, Traffic 글의 유용한 의뢰 판단 설명을 명확히 했다.
- 제거한 충돌: 법령 사이트만 허용하던 블로그 출처 URL 제한(검증된 공식 질의회신·통계 등 실제 출처 허용), 카드/SNS의 낡은 철학 버전 고정, 하나의 글 역할과 의뢰 판단의 양립 모호함, 자동 QA와 사람 확인 기록만으로 카드 완성을 판단하던 문구. 카드의 연속 주장 중복·동일 상자 반복을 피하고 원문 기반 조건·문서 항목·같은 단위 수치만 시각화한다.
- A는 블로그·웹사이트, B는 카드·SNS·제작 지침, C는 기존 미발행 예시집을 분담해 실제 편집했고 A가 통합본을 추가 대조했다. 별도 모델 변경을 주장하지 않는다. 예시집은 시행규칙 제8조·제4조와 식약처 2026-03-30 회답 원문을 직접 읽은 범위 및 판본을 기록했다. 증명서 질문→자격 경로·문서 표기→관할 심사→무료 검토 업무로 연결하고 카드 개요의 역할을 구분했다.
- 검사: MANIFEST 46개 경로, 카드 기본 회귀, 전체 unittest 152개(147 통과·선택 의존 기능 5 skip), git diff --check 통과. 디자인 고정 검사는 전체 테스트에 포함했다. Git Bash의 기존 Windows 접근 오류를 피하여 PowerShell과 명시적 Python 경로·작업 폴더 임시경로/의존성으로 실행했다. 테스트 코드나 기준을 바꾸지 않았다.
- 보호: content/·렌더러·CSS·스키마·한도·상품·가격·접수 주소·승인 상태 불변. 공식 갱신 절차로 PROJECT 및 blog/card/website/evidence 명세 5개 지문만 변경했다. 실제 샘플 카드 JSON·렌더 QA·시각 검토 및 외국어 독립 검수는 미완료 상태로 구분하며 자동 검사가 글의 설득력·법률 해석을 증명한다고 주장하지 않는다.
- 기존 PR에 구현을 반영하며 main 직접 쓰기·병합·발행은 하지 않는다. ChatGPT 프로젝트 설정은 저장소와 별개이며 교체용 문구만 제공한다.

## 2026-10-16 — PR #48 칼럼형 지침 구현 및 최종 대조

- PR #48의 실제 시작 head는 `6e90aeca3a27ff7dfffd58571f8f01bcafb84019`(작업지시서만 변경)이었고, 이전 보고의 `8a36e15`는 원격 저장소에서 조회되지 않았다. 본 브랜치에서 누락된 구현을 수행했다.
- 독자 질문·오해 → 근거와 조건 비교 → 자기 적용 → 실제 맡길 업무를 연결하는 법률 칼럼을 공통 기본값으로 구현했다. 이름·대화는 선택이며 신청 순서나 장면·조문·CTA를 반복 공식으로 강제하지 않는다. 가상 예시 허용과 허구의 실제 상담·수임·후기·성과 및 기관 인용 창작 금지를 구분했다.
- 블로그·카드·SNS·웹사이트 빠른 명세, 공통 문체·철학·구조, AGENTS/MANIFEST/프로젝트 지침을 정합화했다. 상위 문체·근거잠금·법률 검증과 SNS 재가공·마케팅 보조 지침의 실제 충돌 문구만 수정했다. 국문·영문·아랍어, 후속편·시리즈·수정본·모든 파생에 적용한다.
- 요약을 말미로 옮기고 공개 독립 확인일을 제외했다. 내부 확인일·판본과 실제 시행일·판결일, 웹사이트 관리용 날짜는 보존했다. 무료 사전 검토와 유료 작성·제출을 구분하고 기존 CTA 수·순서·주소를 유지했다.
- 미발행 비교 샘플의 블로그 도입·중간 설명, 카드 8장·카카오·웹사이트와 EN/AR 장면 대응을 보강했다. 다른 짧은 SNS는 이름을 강제하지 않는 예로 유지했다. 새 장면은 보강 원문의 승인 대기 범위에 속하며 실제 파생·발행 승인을 받은 자료가 아니다. ③편 실제 원고, 구체 유료 상품 범위는 입력에 없어 창작하지 않았다.
- A(블로그·웹사이트)와 B(카드·SNS)가 실제 병렬 편집했고 C가 통합본을 읽어 검증했다. C가 찾은 웹 샘플 요약 위치·Story Hook 일괄 금지·복잡한 구조에만 예시 허용·보조자료 확인일 충돌을 수정했다. 모델 설정은 상위 설정 상속이며 별도 빠른 모델 배정을 주장하지 않는다.
- 검사: `git diff --check`, MANIFEST 46개 경로, 디자인 고정 2 tests, 카드 기본 회귀 통과. 전체 `unittest` 152개 실행, 147개 통과·5개 선택 의존 기능 skip. 최초 pytest 미설치, 임시 디렉터리 권한 및 jsonschema/playwright 누락 오류는 작업 폴더 의존성·임시경로와 실행 권한으로 해결한 뒤 재검사했다. Git Bash는 Windows 접근 오류로 사용할 수 없어 PowerShell에서 명시적 Python 경로로 실행했다. 검사 코드·임계값은 변경하지 않았다.
- 보호 확인: content/·렌더러·CSS·스키마·카드 한도·가격·접수 경로 변경 없음. 기존 URL 문자열 보존 확인. 고정 지문은 사용자 요청 대상 PROJECT_INSTRUCTIONS, 블로그·카드·웹사이트·근거잠금 명세 5개만 갱신했다.
- 편집 적합성은 샘플 직접 대조로 판단했고 문의율·수임 성과를 검증했다고 주장하지 않는다. 외부 법률·외국어 독립 검수, 발행용 카드 렌더는 이번 완료 범위가 아니다. main 직접 쓰기·병합·발행은 하지 않는다. 웹사이트 철학 사본의 동기화는 기존 병합 후 PR 절차로 남긴다.

## 2026-10-16 — 전 매체 이야기·법률 조건·실제 업무 연결

- 기존 인계 지시서에 따라 블로그·웹사이트·언어 품질·카드·SNS 빠른 명세를 최소 보강하고 AGENTS/MANIFEST에 후속편·새 시리즈·국영아 공통 적용을 연결했다. 조건형 예시, 자료와 실제 작업, 무료 검토와 유료 작업의 구분을 명시했다.
- `examples/writing/cross-channel-three-pillars-20261016.md`에 저장소 테스트 원문 기반 미발행 비교 샘플을 작성했다. 원문 검수 상태와 법률·번역의 외부 재검증 한계는 그대로 남긴다.
- 기존 블로그 지문 불일치는 aef8607·d41f9d2의 조건형 예시/CTA 보존 변경 뒤 기록이 갱신되지 않아 발생했다. 해당 변경은 이번 인계 지시서의 보존 대상과 일치함을 확인했다. 이번 허용된 블로그·카드·웹사이트 명세 3개만 고정 지문을 갱신하며 다른 고정 파일은 변경하지 않는다.
- 승인·예약 콘텐츠, 상품·가격·접수 주소, 렌더러·CSS·스키마·글자 한도·검사 기준은 유지했다. 병합·발행은 수행하지 않는다.

## 2026-10-15 — 매체별 독자 이해 원칙 2차 보강

- 공통 전략 `docs/content-architecture-system.md`에 '사실·법률 의미는 동일, 매체 표현은 다르게' 원칙과 독자별 설명 깊이를 반영했다. 새로운 고정 점수·글자 수·사례 개수는 만들지 않았다.
- `docs/sns-authoring-spec.md`에 카카오·LinkedIn·Instagram 캡션·Threads 및 영문·아랍어별 이해 중심 구성 가이드를 넣었다. 매 SNS 작업 때 방대한 상위 지침을 일괄 조회하도록 요구하던 규칙은 현재 프로젝트의 빠른 조회 경로로 정합화했다.
- `docs/card-authoring-spec.md`에 Source Lock 범위 안의 상황·조건 대조·확인 행동 중심 카드 원칙을 추가했다. ChatGPT/Codex/사람 역할, JSON 골격, 디자인·글자 제한은 불변.
- `docs/website-md-spec.md`에 국·영문 독자의 검색 질문·직접 답·적용 조건·선택적 FAQ를 연결하는 편집 원칙을 추가했다. 홈페이지 서비스의 가격·상품·접수 정책은 웹사이트 저장소가 정본.
- `examples/writing/README.md`에 동일한 설명용 가상 상황을 6개 매체별로 표현하는 미발행 예시를 추가했다. 새 법률 판단·가상 수임·허위 성과는 추가하지 않았다.
- 사용자 요청에 따라 고정 작성명세 2개(`docs/card-authoring-spec.md`, `docs/website-md-spec.md`)만 `state/design-freeze.json` 해시를 갱신하고 이력을 기록했다. 기존 승인 세트·예약 화장품 세트·렌더·시트·웹사이트 코드는 변경하지 않았다.

## 2026-10-15 — 사용자 요청: 독자 이해 중심의 생활 밀착형 글쓰기

- `docs/blog-authoring-spec.md`에 독자 상황 → 직접 답 → 쉬운 풀이·가상 사례 → 공식 근거·판단 기준 → 확인할 자료·절차를 권장하는 Soft Guide를 추가했다. 법률 Hard Gate·기존 도입 순서·8,000~11,000자·후반 무료 검토 1회는 유지했다.
- `examples/writing/README.md`에 생활 장면, 전문용어 풀이, 서류 대조, 다음 행동을 보여 주는 가상 구성 예시 네 가지를 추가하고 실제 사례와 구분했다.
- `docs/content-architecture-system.md`와 `docs/language-quality-workflow.md`에서 역할별 이해 방식과 신규 초안의 사례 작성/법률 검증/최종 윤문 단계를 구분했다.
- `docs/brand-philosophy.md`를 v1.2로 개정해 독자의 언어로 설명하는 브랜드 목소리를 추가했다. 웹사이트 저장소 사본은 이 저장소 main 병합 후 동기화 PR에서 별도 검토한다.
- `guidelines/modules/everyday-topics.md`의 과거 표본·고정 편성 비중을 현행 마케팅 성과나 필수 발행 규칙으로 사용하지 않도록 안내했다.
- 사용자 요청에 따른 작성 명세 수정분만 `state/design-freeze.json`의 지문과 이력에 반영했다. 카드 렌더러·법률 범위·CTA 경로·기존 승인 콘텐츠·예약 시리즈는 변경하지 않았다.


## 2026-10-14 — 사용자 승인: 마케팅 운영 기준 정합화

- 블로그 검색 질문을 제목 앞에 두고 기존 상황→인사→3줄 요약, 8,000~11,000자와 법률 검증을 유지했다. 하단 CTA 1영역·기존 이미지 4개·온라인 우선은 그대로다.
- `docs/blog-authoring-spec.md` 6-1절을 별도 배너 링크설정 메모 정본으로 삼았다. `naver_blog/profile`과 `footer-ko`를 구분하고 확인된 기존 글 ID·승인 상품 ID만 목적지에 사용한다. 원시 추적 URL·API 키의 본문 노출을 허용하지 않는다.
- `docs/topic-log-integration.md`에 기존 기록 재사용, 승인 상품 연결 참조, 미입력과 0 구분, 채널·기간이 맞는 문의 참고율, 실제 URL·별도 승인 게이트를 정합화했다. 내부 문의·미공개 성과 데이터는 저장소에 복제하지 않는다.
- 기존 웹 안내가 Revenue 역할을 충족하면 새 네이버 판매 글·페이지를 요구하지 않도록 전략문서의 중복 규칙을 참조로 바꿨다. 검색수요와 실제 문의를 함께 보고 최근 90일로 운영 모드를 재평가하며 제휴 후보는 제외한다.
- 사용자 승인된 작성 지침 변경에 한해 `scripts/design_freeze.py --update --note`로 고정 기록을 갱신했다. 기존 main에서 불일치했던 블로그 명세와 이번에 변경한 프로젝트 지침만 지문이 달라지며 다른 고정파일은 유지한다.
- 가격·법률 업무범위·예약 화장품·`content/` 승인 세트·시트·웹사이트 코드는 변경하지 않았다.

## 2026-10-10 — 받을 자료 디자인본, 블로그 윤문

- TEST-SUSPENSION-V3 받을 자료를 A4 한 장으로 디자인(`lead-magnet/checklist.html` → `checklist.pdf`·`checklist.png`). 문구는 `lead-magnet.md`와 같고 연락처·URL 없음. 읽는 순서대로 1 표시할 것 → 2 모아 둘 자료 → 3 네 가지 순서 → 4 막히는 경우 → 5 알아 둘 것.
- `scripts/render_lead_magnet.py`: HTML을 A4 PDF·2배 PNG로 렌더하고 브랜드 글꼴 미로드·시트 넘침·본문과 꼬리말 겹침이면 FAIL.
- TEST-SUSPENSION-V3 `blog.md` 윤문: 문두 접속어·"~에 대한"·긴 문장·막연한 강조를 줄였다. 숫자·조문·한정어는 그대로.
- 같은 글 앞부분을 새 순서로: 제목 → 독자 상황 한 줄 → 인사 → 3줄 요약(본문 결론만) → 시리즈 목차(끝에서 앞으로 옮김) → 본문.
- `copy_lint.py` `late-answer`: 목차 앞에 '요약'이 있으면 알리지 않는다(명세 11절 순서와 충돌하던 안내 정리).

## 2026-10-07 — 디자인·지침 고정

- 사용자 요청으로 카드 렌더러·CSS·프리셋·게이트·한도·스키마·작성 지침 18개 파일을 고정했다(`state/design-freeze.json`, `scripts/design_freeze.py`, `tests/test_design_freeze.py`). 바꾸면 CI가 실패하고, 승인된 변경만 `--update`로 기록을 갱신한다. 태그 `design-freeze-2026-10-07`.
- 시험 폴더 `TEST-COHABITATION-CONTRACT`·`TEST-COHABITATION-V2`를 지웠다. `TEST-SUSPENSION-V3`는 자유 디자인 기준 예시로 테스트·디자인 가이드가 참조하므로 남겼다.

## 2026-10-07 — 메모체·결론 띠 비율을 필수로

- 동거 계약서 시험에서 카드 점수를 깎은 두 가지(가운뎃점 셋 이상 나열 5/9장, 결론 띠 4/9장)를 지침·명세에서 필수로 올리고, 린터 `memo-style`·`take-bar-share`를 안내에서 경고로 바꿨다(`Render cards` 요약의 린터 경고에 나온다).

## 2026-10-07 — 실제 시험(동거 계약서) 반영

- 시험 결과: 글 앞부분 순서·3줄 요약·"따라서" 1번·태그 17개·제목 27자 준수, 카드는 표지 hero·paths·highlight와 쉼 카드·결론 끝맺음 5/9 준수, QA 통과. 걸린 시간 약 10분(글+카드+배포안 함께).
- 블로그 분량이 4,223자로 승인 글(약 1만 자)의 40%였다. 지침에 분량 기준(공백 포함 8,000~11,000자)을 넣고 7,000자 미만이면 린터 `short-blog` 경고.
- `scripts/card_data_fix.py`: `Render cards`가 흔한 형식 실수(table body를 {head, rows}로 씀, 아이콘 .svg, 단계 값 오류)를 렌더 전에 바로잡고 보고서에 적는다. 저장소 JSON은 그대로.
- 린터 `suspect-fragment` 오탐 수정: 앞 줄이 문장 끝이나 목록 항목이면 알리지 않는다.

## 2026-10-07 — 마무리 8가지(카드 구도·넘김 표시·결론 리듬·글 앞부분)

- 자동 디자인: 세트 전체를 보고 부품을 정해 같은 부품이 세 장 연속되지 않게 한다(`component_plan`). key가 있는 항목은 key를 그리는 부품끼리만 바꿔 카피 잠금을 지킨다.
- 넘김 표시: 오른쪽 아래 페이지 칸에 진행 막대와 "03 / 10"(자동 디자인 전부, 기본 빌더는 v2.0 세트만). 칸의 위치·크기는 그대로라 프레임 검사와 승인 세트 HTML이 바뀌지 않는다.
- 카드 지침: 결론 3장 이상은 "~니다"가 아닌 끝맺음, 본문 항목은 한 문장.
- 글 지침: 제목 30자 안팎 → 독자 상황 한 줄 → 인사 → 3줄 요약 → 목차 → 본문(인사말은 유지, 사용자 결정 A). 필수: "따라서" 3번까지, 쉼표 목록 금지. 린터 `greeting-first`·`no-summary`(안내), `comma-list`·`so-many-therefore`(경고). 웹사이트 MD에 `> 3줄 요약`, 제목 30자 안팎.

## 2026-10-07 — 표지·쉼 카드 시안 회전

- 사용자가 고른 시안 4종을 정식 부품으로: 표지 A(큰 숫자)·B(물건 그림+갈래 칸), 쉼 카드 1(큰 따옴표)·2(손 동그라미). `auto_design.py`가 회차 번호로 번갈아 고른다(표지: 홀수 A·짝수 B, 재료가 하나면 그것. 쉼 카드: 회차+세트 안 순서로 교대). 시안 C(손그림 인물)·쉼 카드 3(먼저/나중 대비)은 쓰지 않는다.
- 새 카드 유형 `rest`(스키마·한도·기본 빌더 예비 렌더·스트레스), 새 선택 필드 `paths`(표지 B·쉼 카드의 갈래). 프리셋 A에 `.cv5`·`.cvb-*`·`.rest-*` 부품. 손 밑줄·동그라미는 Rough Notation(기존 벤더).
- 명세·지침: 표지에 hero·art·paths·highlight를 함께 주기, 쉼 카드 세트당 1장.

## 2026-10-07 — 표지 다듬기와 표지 린트

- 기본 빌더(v2.0 세트만): 헤더와 같은 표지 칩을 그리지 않고, 표지 내용을 위에 붙이지 않고 가운데 두며 제목을 키웠다. 2행 막대 카드는 막대·숫자를 키워 빈 공간을 줄였다. `layoutVersion`으로 레이아웃만 켠 승인 세트(GAME-OVERSEAS-06)는 표지가 그대로다(회귀 테스트로 확인).
- 린터 `cover-number`(표지에 숫자가 있으면 큰 숫자 표지 권고), `cover-object`(art에 자동 디자인이 그릴 큰 그림이 없음), `cover-art-repeat`(다른 회차와 같은 표지 그림). `auto_design.py`가 `scale.svg`처럼 확장자가 붙은 아이콘도 큰 그림으로 찾는다.
- 지침·명세: 표지 고르는 순서, 큰 그림이 있는 아이콘 목록, `coverLabel`은 이번 회 주제로, 카드당 조문 번호 1개(나머지는 캡션 `근거:` 줄).

## 2026-10-07 — 전환 장치(실제 기한·보낼 것→받을 결과·받을 자료·저장·다음 편)

- 원칙 안에서 문의로 이어지게: 꾸며낸 긴장 금지, CTA 마지막 한 번, 카드·본문 연락처 금지는 그대로.
- TEST-SUSPENSION-V3: 블로그에 의견제출기한 단락(행정절차법 제21조 제1항 제6호·제3항, korean-law-mcp로 2026-10-07 원문 확인). 마지막 장 CTA를 "의견제출기한 전, 사전통지서와 과거 처분서로 전환 가능 여부와 대응 방향을 무료로 검토해 드립니다"로(결과는 brief의 승인 범위, 회신 기간은 미확인이라 쓰지 않음). 캡션에 기한·저장 신호·다음 편, 받을 자료 `lead-magnet.md`(사전통지서 확인표, 원문 내용만).
- `copy_lint.py`: 배포안에 저장 신호(`no-save-cue`)·다음 편(`no-next-episode`)·받을 자료(`no-lead-magnet`)가 없으면 안내.
- 명세: `card-authoring-spec.md` "전환 장치" 절, `blog-authoring-spec.md` 머리 안내. `strategy-playbook.md` 6절에 웹사이트 요청(접수 폼 첨부 칸, 받을 자료 페이지) 추가.

## 2026-10-07 — 카드 분량 기준 통일(승인본 실측)

- 문제: 명세는 영문 세트 평균 330자 **이상**, QA(`gates.json`)는 영문 카드 300자·48단어 **이하**를 권해 동시에 맞출 수 없었다. 국문도 명세 하한 150자가 승인본 평균(133~165자)보다 높았다. 승인본 영문 세트조차 카드의 22~78%가 권고에 걸렸다.
- 사용자 위임으로 승인본 실측(SUSPENSION-SURCHARGE-04·GAME-OVERSEAS-06·시범 세트)에 맞춰 정했다.
  - `gates.json` 1.7: 영문 카드 권고 340자·60단어, 강한 경고 420자·72단어(이전 300·48 / 380·64). 국문 180·240은 그대로.
  - `card-limits.json`: 세트 평균 하한 국문 130·영문 280(이전 150·330), 상한 국문 210·영문 440(이전 220·450).
  - 명세·프로젝트 지침: 목표 국문 150~190자, 영문 300~400자. 영문은 국문의 약 2.2배가 정상.
- 모든 기준은 권고이며 렌더를 막지 않는다(하드 실패 조건은 바꾸지 않았다).
- `Render cards` 워크플로가 `gates.json`·`card-limits.json` 변경에도 돌도록 했다(바뀐 세트가 없으면 전체 세트를 새 기준으로 미리보기). 승인 세트의 커밋된 `out/` QA 보고서는 승인 당시(v1.6) 기록이라 다시 쓰지 않았다.

## 2026-10-07 — 남은 개선 마무리(표·흐름 부품, 표지 그림, 밀도, 성과 기록)

- 자동 디자인: 표(`.tbl2`, 5행 이상 압축), 세로 흐름(`.vflow`, 아이콘 배지+화살표+메모), 마지막 장 3~6개 목록(`.docs`) 부품. 문자열 항목("제목: 설명")은 구분 기호를 남겨 원문 그대로 보이게 했다. GAME-OVERSEAS-06-V2-DRAFT의 표 2장·흐름 1장이 자동 디자인으로 나온다.
- `ci_render.py`: 자동 초안이 QA를 깨면 실패한 카드만 기본 빌더로 되돌리고, 그래도 실패할 때만 전체를 되돌린다.
- GAME-OVERSEAS-06-V2-DRAFT 표지에 `art: laptop, store` 추가. 승인 세트 두 개에도 넣었다가 되돌렸다: 승인 세트는 card-data로 다시 빌드한 결과가 커밋된 발행 HTML과 같아야 한다는 테스트(`CommittedSetsStayIdentical`)가 있고, 발행된 표지를 바꾸려면 다시 승인이 필요하다.
- TEST-SUSPENSION-V3 밀도: 국문 10장 권고 해소, 영문 4·7·10장 압축(사실·한정어 비교 경고 0). `performance-log.csv` 준비(표지 Hook A/B 변수 기록).
- 미해결 기준 충돌: `gates.json` 영문 권고(카드당 300자·48단어)와 `card-authoring-spec.md`의 영문 평균 330자 이상 권장이 동시에 맞지 않는다. `gates.json`은 사람만 고치는 파일이라 그대로 두었다.

## 2026-10-07 — 자동 디자인: ChatGPT JSON만으로 강화된 미리보기

- 운영 구조(사용자 확인): ChatGPT가 card-data JSON을 쓰고 Codex가 나머지를 실현한다. 그런데 JSON만 올린 세트의 CI 미리보기는 기본 빌더라 같은 목록 틀이었다.
- `scripts/auto_design.py`(신규): card-data의 유형·layout·항목 수·아이콘으로 프리셋 A 부품을 골라 카드마다 시각 중심이 다른 자유 디자인 초안을 만든다. 문구는 그대로(카피 잠금 통과), 넘치면 본문 글자만 16px까지 줄이고, 표·흐름처럼 부품이 없는 카드는 기본 빌더.
- `ci_render.py`: 손으로 디자인한 HTML이 없는 카드는 자동 초안으로 렌더하고, QA가 실패하면 그 카드만 기본 빌더로 되돌려 다시 렌더한다. 기본 빌더·시각 회귀 기준은 바꾸지 않았다.
- 승인 세트 SUSPENSION-SURCHARGE-04·GAME-OVERSEAS-06과 TEST-SUSPENSION-V3의 JSON만으로 국·영문 6세트 모두 자동 초안 QA PASS.
- 프리셋 A: 핵심어 행·질문 패널의 네이비 변형, 순서 행의 크림 변형, 긴 핵심어 위아래 쌓기(`.krows.stack`), 5단계 이상 순서 압축(`.steps.many`).
- `design_review.py`: 자동 초안만 있으면 `auto-draft` 안내, 표지 그림이 없으면 JSON에 `art`·`hero`를 넣으라고 안내. 명세(`card-authoring-spec.md`)에 "JSON 필드 → 자동 디자인 결과" 표, Codex 8단계는 자동 초안에서 시작.

## 2026-10-07 — 카드 디자인 강화: 시각 중심 부품, 디자인 점검기

- 원인: 승인 세트 SUSPENSION-SURCHARGE-04·GAME-OVERSEAS-06이 기본 빌더로만 만들어져 10장이 같은 목록 틀, 아이콘·그림 0장, `data-focal` 0장이었다. QA는 깨짐만 보고 "양식집처럼 보이는가"는 보지 않았다.
- `scripts/design_review.py`(신규, 권고): 빌더 전용(`builder-only`), 밋밋한 표지(`cover-plain`), 시각 중심 없음(`focal-missing`), 같은 종류 시각 중심 세 장 연속·절반 초과(`focal-repeat`, 숫자·그림·막대·아이콘 행·목록·핵심어로 분류), 같은 본문 구조 연속(`layout-repeat`), 그림 있는 카드 3분의 1 미만(`visual-thin`). `ci_render.py` 요약에 함께 나온다. 승인 세트 두 개는 경고 4종, 시범 세트와 새 세트는 PASS.
- 프리셋 A에 부품 10종 추가(`.cv-duo`, `.krows`, `.versus`, `.q-head/.q-panel/.q-hero`, `.ico-rows`, `.xlist`, `.bars2`, `.stat-rows`, `.bound.stack`). 기존 부품은 바꾸지 않았다. 가이드 10-0-5에 부품별 맞는 메시지 표.
- 영문 세트: `card-data.en.json`(용어는 docs/en-legal-glossary.md, 숫자·한정어 국문과 동일, validate_bilingual PASS), 영문 10장+대안 표지 자유 디자인, QA PASS. 프리셋 A에 새 부품의 영문 크기 규칙과 밑줄 낱말 줄바꿈 방지(`[data-annotate]{white-space:nowrap}`)를 더했다. 배포안 영문 캡션·Hook 3종·alt text.
- 제작 메타데이터: ChatGPT 최소 JSON에는 `marketing`·`oneMessage`·`sourceTrace`·`canvasProfile`이 없어 `marketing_review.py`가 30/100을 냈다(내용과 무관). Codex 제작 단계에서 brief.md로 채우도록 `card-codex-production.md` 5단계에 명시. 채운 뒤 국문 99·영문 94(영문 밀도 권고 남음).
- TEST-SUSPENSION-V3: 카피 승인 반영(`approvedBy`, `languagePass: manual-equivalent`) 후 국문 10장과 대안 표지를 자유 디자인으로 제작. QA PASS(1차 렌더 넘침 6장 → 0), 디자인 점검 PASS, 비교 이미지 `out/ko/before-after.png`, `wireframe.txt`·`review.md`·`assets.md`·배포안 alt text 추가. 영문 세트는 아래 항목.

## 2026-10-07 — 린터: 답 먼저·CTA 마지막·추적 링크·붙여 쓴 태그 반복

- `copy_lint.py --blog`: 글 앞 15% 안에 원문자 목록이 5줄 이상 연달아 있으면 `late-answer`(INFO, 시리즈 목차가 답을 늦춤), 태그를 뺀 마지막 문단에 "무료 검토"가 없으면 `cta-not-last`(WARN).
- `copy_lint.py`: `distribution.md`에 상담 접수 추적 링크(`intake?source=ethos-contents`)가 없으면 `no-intake-link`(WARN), 해시태그 같은 낱말 3개 초과는 `dist-tags`(INFO). 캡션 양식과 관계없이 검사한다.
- `tag_rules.py`: 네이버 태그는 띄어쓰기가 없어(`#영업정지과징금`) 기존 검사가 반복을 못 잡았다. 3자 이상 공통 조각도 같은 낱말로 센다(승인 세트에서 '영업정지' 12개를 새로 잡음).
- `ci_render.py`: `TEST-`·`-DRAFT` 폴더에 국문만 있으면 영문 누락을 실패 대신 안내로 처리(지침의 "국문 먼저" 흐름과 CI 불일치 해소, 저장소 주인 승인). 승인 전 `validate_bilingual.py`는 그대로 두 언어를 요구한다.
- TEST-SUSPENSION-V3 개선: 표지를 사례 대비형으로(질문형은 `altCover`), 과징금·과태료 구분을 3장으로 당김, 4장 조문 번호 4개 → 0개(캡션 근거 줄로), 금액 상한 카드를 세 사건 비교 카드로 바꾸고 OMITTED에 기록, 부산 사례 결론을 "첫 청구에서 방향 결정"으로. 블로그는 시리즈 목차를 CTA 앞으로 옮기고 "출처 입력" 10곳 삭제, "따라서" 11 → 4, 태그 22 → 17개, 배포안에 추적 링크와 시리즈 연결 추가.

## 2026-10-07 — 카드 역할 분담(ChatGPT 초안·디자인 제안 / Codex 제작), AGENTS.md 경량화

- 원인: 지침끼리 서로 다른 지시를 해서 모델이 충돌을 풀려고 문서를 더 열었다. `AGENTS.md`는 "먼저 MANIFEST", 프로젝트 지침은 "MANIFEST 읽지 않음"이었고, 카드 명세는 "윤문 패스 안 돌림·`languagePass: pending`"인데 `AGENTS.md`·`validate_bilingual.py`는 pending이면 실패였다. `design` 필드는 같은 명세 안에서 "쓰지 않는다"와 "카드마다 쓴다"가 함께 있었다.
- 역할 확정: ChatGPT는 카피 초안과 디자인 방향(`design`·`coverStyle`·`icon`·`layout`)을 자유롭게 제안하고(`design` 권장 필드로 변경), 윤문·영문·승인 요청·HTML 디자인·렌더·QA는 Codex가 한다. 초안의 `pending`은 정상이며 `validate_bilingual.py`는 Codex가 승인 직전에만 돌리는 관문(검사 기준은 바꾸지 않음).
- `AGENTS.md` 15.8KB → 약 4KB: 라우터 표와 공통 원칙만 남기고, 카드 제작 규칙은 `docs/card-codex-production.md`(신규, Codex 전용)로 옮겼다. 단계 번호 오류(12 다음 9) 수정, 중복 문장 압축. 규칙 내용은 삭제하지 않았다.
- 시험 세트(TEST-SUSPENSION-V3)에서 "지정 파일 외 조회 금지" 때문에 배포안 추적 링크가 빠졌고, 초안 단계에 없는 `assets.md` 때문에 경고 12건이 났다. 추적 링크 형식을 프로젝트 지침에 직접 넣고, `assets.md`는 Codex 단계로 옮겼다.
- `card-authoring-spec.md`: 필수 읽기를 "이 문서 + blog.md"로 고정하고 나머지 참조 문서는 FAIL·요청 때만. `blog-authoring-spec.md`: 상위 문서는 해결되지 않는 충돌일 때만 연다. MANIFEST 카드 목록에 Codex 전용 문서와 읽는 시점 표시.

## 2026-10-07 — 쓰기 가능 폴더 규칙 명확화

- 지침이 "main에 직접 쓰지 않는다"였지만 실제로는 시험 폴더에 직접 올리는 것이 편해서, `TEST-` 시작 또는 `-DRAFT` 끝 폴더에만 직접 쓰기를 허용하고 승인 세트·그 밖의 폴더는 계속 쓰기 금지로 명시했다. 시험 3 결과: 4분, JSON 3.9천 자, 평균 179자, QA 통과.

## 2026-10-07 — 태그 다양성 규칙

- ChatGPT 시험 두 건에서 태그가 `행정사`·`변호사` 계열 변형으로 몰렸다(블로그 18개 중 두 낱말이 각 4개, 웹사이트 8개 중 62%). 명세 10절에 5가지 묶음(핵심어·제도명·독자 검색어 4개 이상·상황·절차어 3개 이상)과 "같은 낱말은 3개까지" 규칙을 넣었다.
- `scripts/tag_rules.py`: 블로그 `#태그`와 웹사이트 쉼표 태그를 같은 기준으로 점검(개수, 중복, 낱말 쏠림). `copy_lint.py`는 `blog.md` 끝 태그를, `validate_website_md.py`는 머리말 태그를 안내한다. 안내이며 발행을 막지 않는다.

## 2026-10-06 — 태그 규칙, 카드 JSON 최소 필드

- 블로그 태그: 네이버 `blog.md` 끝에 `#태그` 12~20개를 다양하게(핵심어·제도명·독자 검색어·표기 변형·상황·절차어). 웹사이트 태그는 `#` 없이 쉼표로만 구분한 한 줄 4~10개. 웹사이트 관리자 편집기(`blog-editor.tsx`)가 태그를 쉼표로 나눠 입력한 글자 그대로 저장하므로 `#`을 붙이면 태그에 `#`이 들어간다. 검사기가 `#`을 오류, 배열 표기를 안내로 알린다.
- 카드 JSON 최소 필드: 렌더·검사에 쓰이지 않던 `angle`·`canvasProfile`·`visualFamily`·`marketing` 블록·카드별 `oneMessage`·`sourceTrace`·`design`을 필수에서 뺐다(스키마). 시험 세트로 측정하니 JSON 출력이 39% 줄었고 스키마·린트·렌더·QA를 그대로 통과한다. 기존 세트의 필드는 그대로 유효하다. 프로젝트 지침과 명세의 JSON 골격, `brief.md` 10줄 이내 규칙 반영.

## 2026-10-06 — ChatGPT 글쓰기 로딩 시간 단축

- 원인: 새 법률 주제 한 편에 약 108KB(MANIFEST·top-level 30KB·blog.md 44KB 등)를 파일마다 따로 조회했고, 프로젝트 지침(10.8KB)이 매 대화에 붙었다. 지침 18행이 "블로그는 blog.md를 적용"이라고 해서 가벼운 경로를 만들어도 큰 파일을 읽게 됐고, 카드에는 영문을 동시에 쓰라는 문장이 남아 국문 우선과 충돌했다.
- `docs/evidence-gate.md`(약 5KB)로 경로 B의 근거 규칙을 한 파일에 모았다(top-level 4절·definitive-style·legal-verification 발췌, 원문 우선). 경로 B 읽기: 약 108KB → 약 16KB(명세 11KB + 근거 요약 5KB), 경로 A: 약 14KB → 약 11KB(명세 한 파일, 브랜드 핵심을 명세에 요약).
- 프로젝트 지침을 요청 유형별 읽을 파일 표 중심으로 다시 써서 10.8KB → 5.3KB, 충돌 문장 제거, "필요한 파일은 한 번에 함께 요청" 규칙 추가.

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

## 2026-10-18 — 보조 프리셋·시각 회귀 게이트 마감

- 프리셋 B를 굵은 타이포·각진 패널 중심의 강한 정보형으로 정리하고 영문 크기를 별도 보정했습니다.
- 프리셋 C를 크림 단색·선 중심의 절제형으로 통일해 A 프리셋의 그림자와 어두운 패널이 새지 않게 했습니다.
- 프리셋 D에 에디토리얼 제목선·영문 세리프 보정·평면 패널 규칙을 더했습니다.
- 기존 PNG 기준선은 새 디자인 렌더를 승인한 뒤 갱신하도록 보존했습니다.
- 시각 회귀 렌더를 격리 프로세스로 실행하고 45초 제한·브라우저 단계별 15초 제한·임시 파일 정리를 추가해 무한 대기를 막았습니다.
## 2026-10-18 — 화장품 OEM 카드뉴스 실전 제작

- 승인 블로그 `COSMETICS-OEM-04`를 Source Lock으로 국문·영문 10장 카드 데이터와 배포 문구를 만들었습니다.
- 제조·검사·기록의 흐름이 보이도록 표지, 책임 비교, 질문형 체크리스트, 영업비밀 근거 카드와 저장용 최종 체크리스트를 전용 CSS로 마감했습니다.
- `auto_design.py --production`을 추가해 수동 마감 CSS를 연결한 발행 후보 HTML에서는 자동 초안 표식을 제거할 수 있게 했습니다.
- 개념 대조·절차 타임라인·쉼 카드·저장용 체크리스트·CTA에 서로 다른 시각 리듬을 적용해 문서형 반복을 줄였습니다.
- 긴 시리즈명 대신 카드용 `headerLabel`을 표시해 540px 화면에서도 헤더와 회차가 겹치지 않도록 했습니다.
