# ETHOS 콘텐츠 운영 라우터 (Codex용)

이 저장소는 블로그·비블로그 SNS·웹사이트·카드뉴스 지침의 단일 기준본이다. 콘텐츠 작성이나 지침 수정 요청을 받으면 먼저 `MANIFEST.md`를 읽고 Active 파일만 적용한다. 동일 지침의 과거 버전이나 MANIFEST에 없는 문서는 자동 적용하지 않는다.

마케팅·포지셔닝·대상 독자·차별화 판단에는 `.agents/product-marketing.md`를 공통 맥락으로 사용한다. 현재 사용자 요청과 MANIFEST의 운영 원칙이 항상 우선한다.

## 작업 라우팅

- **마케팅·성과 분석**: 글감관리표 주간 성과 탭 → `docs/topic-log-integration.md` "마케팅 점검" → `docs/performance-learning.md` → `docs/strategy-playbook.md`
- **소재 발굴·콘텐츠 캘린더**: core → `docs/strategy-playbook.md` → `docs/topic-discovery.md` → 최신 글감관리표가 있으면 `docs/topic-log-integration.md` → `content-strategy` → 필요한 modules
- **AI 시대 인간 전문성·신규 전문가·자격 결합 포지셔닝**: core → `.agents/product-marketing.md` → `guidelines/modules/new-expert.md` → `guidelines/modules/human-judgment-positioning.md`
- **블로그·홈페이지 Editorial Master 작성**: core → `docs/topic-discovery.md` → `guidelines/channels/blog.md` → 필요한 modules → 승인 요청 전 `python scripts/verify_citations.py <원고> --out content/<ID>/citations.md`(키 `LAW_OC`)로 인용 대조, ⚠는 `docs/legal-verification.md` 6절로 사람 확인
- **비블로그 SNS 작성**: core → `docs/topic-discovery.md` → `guidelines/channels/sns.md` → `guidelines/modules/marketing.md` → `guidelines/modules/skill-orchestration.md` → `docs/social-repurposing.md` → 필요한 modules
- **웹사이트 변환**: core → `guidelines/channels/website.md` → `docs/website-md-spec.md`(국·영문 MD 두 파일) → 승인된 원문과의 정합성 확인 → `python scripts/validate_website_md.py content/<ID>`
- **카드뉴스 제작**: core → `docs/topic-discovery.md` → `guidelines/channels/cardnews.md` → 아래 카드뉴스 작업 규칙과 기존 렌더·QA 시스템
- **지침 수정**: MANIFEST의 Active 파일 확인 → 충돌 검사 → 해당 파일 수정 → `CHANGELOG.md` 갱신 → `python scripts/validate_guidelines.py`

공통 우선순위와 고정 원칙은 `MANIFEST.md`를 따른다. `guidelines/core/master.md`의 과거 규칙이 최신 core·채널 지침과 충돌하면 최신 지침을 적용한다. 지침을 고치면서 기존 카드뉴스 제작 시스템을 임의로 이동하거나 완화하지 않는다.

게시용 국문 글·SNS·카드 카피는 모두 `docs/language-quality-workflow.md`의 순서를 필수로 적용한다. 자연 초안을 쓴 뒤 사실·법률, 마케팅, 금지 표현을 서로 다른 패스로 검토하고, 마지막에 `humanize-korean` 또는 동등한 수동 윤문과 의미 재검증을 마친다. 초안부터 모든 규칙을 동시에 맞추지 않는다.

---

# ETHOS 카드뉴스 작업 규칙

목표: 승인된 블로그 원문 1편 → 국문·영문 카드 각 6~10장(**최대 10장 고정**). 영문에서 행정사는 항상 Administrative Attorney. 인스타그램은 4:5(540×675 CSS, PNG 1080×1350)를 기본으로 하고, 범용 배포가 필요할 때만 1:1을 쓴다.
작업 폴더: `content/<CONTENT_ID>/` (예: `content/GAME-KR-06/`). 이 폴더 밖의 킷 파일은 수정하지 않는다.
카드는 원문의 요약본이 아니라, 원문의 **핵심 판단 구조 하나**를 빨리 이해시키는 시각 콘텐츠다.

## 작업 순서 (건너뛰기 금지)
1. 사용자가 채팅에 블로그 원문만 붙여 넣으면 `content/<ID>/` 를 만들고 그 텍스트를 `blog.md` 로 저장한다. ID가 없으면 날짜와 핵심 주제의 영문 slug로 제안하되, 기존 ID를 덮어쓰지 않는다. 원문도 붙여 넣지 않았고 `blog.md`도 없을 때만 사용자에게 요청한다.
2. `docs/card-selection.md`로 제작 가치와 출력 범위를 정한 뒤 `content/<ID>/brief.md` 작성 (`docs/brief-template.md` 양식): **국·영문 공통 각도 1개**, 뺄 섹션 목록, Hook 후보 3개, 카드별 한 메시지.
3. Source Lock의 사실을 보존하면서 국문 카드 흐름과 카피를 자연스럽게 초안한다. 원문 문장을 카드 수에 맞춰 기계적으로 잘라 넣지 않는다.
4. 국문 초안을 사실·법률 검증 → 마케팅 보강 → 금지 표현 검사 → `humanize-korean` 또는 동등한 수동 윤문 → 의미 재검증 순서로 편집한다.
5. 영문은 국문 문장 수를 복제하지 않고 독립적으로 현지화하되 사실·한정어·숫자를 보존한 뒤 의미를 재검증한다.
6. `content/<ID>/card-data.ko.json`과 `card-data.en.json`을 `schema/card-data.schema.json`에 맞춰 작성한다. 새 세트는 `editorialReview.pipelineVersion: 2.0`과 모든 완료 상태를 기록해야 한다.
7. `python scripts/copy_lint.py content/<ID> --blog`로 카피 자연스러움(질문형 헤드라인 반복·부정문 결론·카드 위 조문 번호·미풀이 전문용어·약속 없는 표지·자리표시자)을 점검하고 경고를 고친다. 윤문 전후에는 `--compare <이전.json> <이후.json>`으로 사실 토큰이 바뀌지 않았는지 확인한다. 기본은 권고이며 `--strict`는 경고를 실패로 취급한다.
   `python scripts/validate_bilingual.py content/<ID>`로 편집 파이프라인과 양언어 Source Trace를 확인한다. 하나라도 `pending`이면 승인 요청 금지.
8. ⛔ **여기서 멈추고 사용자 승인을 받는다.** 승인 전 HTML 작성·렌더 금지. (커밋·PR 은 brief와 card-data 단계까지만)
9. 승인 후 `docs/card-design-guide.md`에 따라 `content/<ID>/ko/card_NN.html`과 `content/<ID>/en/card_NN.html`을 **카드마다 직접 디자인**한다(B 방식, 세트 공통 스타일은 `content/<ID>/design.css`). 문구는 card-data와 글자 그대로 같아야 하고, 맨 위에 `<meta name="ethos-design" content="free">`를 넣는다. 프레임·색·글꼴·HTML 계약(`docs/html-contract.md`)은 그대로 지킨다. 기준 예시는 `examples/free-design-realtor/`. 프리셋은 A~D(D: 마루 부리 명조 제목 + 아이콘), 아이콘은 `python scripts/icon_svg.py <이름>`으로 넣는다. HTML 전에 `wireframe.txt`를 쓰고, 새 시리즈는 세 방향 시안(`scripts/preview_drafts.py`)으로 방향을 고른 뒤, 렌더 후 `docs/card-evaluation-rubric.md`로 채점해 `review.md`를 남긴다.
10. 아래 명령으로 언어별 렌더를 실행한다.
   - `PYTHON=python PYTHONUTF8=1 python scripts/card_system_smoke.py` — 공통 빌더 회귀검사. 실패하면 렌더 전에 코드 문제를 고친다.
   - `PYTHON=python PYTHONUTF8=1 python scripts/qa_render.py --html-dir content/<ID>/ko --source content/<ID>/blog.md --out content/<ID>/out/ko`
   - `PYTHON=python PYTHONUTF8=1 python scripts/qa_render.py --html-dir content/<ID>/en --source content/<ID>/blog.md --out content/<ID>/out/en`
   - `PYTHON=python PYTHONUTF8=1 python scripts/marketing_review.py content/<ID>` — 마케팅 점수는 권고이며 렌더를 막지 않는다.
   - `PYTHON=python PYTHONUTF8=1 python scripts/validate_distribution.py content/<ID>` — 카드별 alt text와 외부 자산 출처·라이선스 기록을 확인한다.
11. 실패하면 **카드(카피·레이아웃)를 고친다.** 카피를 고쳤다면 사실·자연스러움·의미 재검증과 사용자 승인을 다시 거친다. `gates.json`, `brand/`, `fonts/` 는 수정 금지.
12. 통과하면 `docs/channel-packaging.md`에 따라 필요한 결과물만 만들고 `content/<ID>/distribution.md`와 `assets.md`를 작성한다. 카드 밖에서 쓸 국·영문 캡션, Hook 3종, 자연스러운 CTA, 카드별 alt text를 포함하되 원문에 없는 사실은 추가하지 않는다. `content/_TEMPLATE/performance-log.csv`를 작업 폴더에 복사해 성과학습 기준을 남긴다.
9. `content/<ID>/out/ko`, `out/en` (png, sheet-270.png, qa-report.md)와 `distribution.md`를 커밋하고, 사람이 확인할 항목을 PR 설명에 적는다.

## 국문·영문 동시 제작 규칙
- 두 언어는 같은 각도, 카드 수, 카드 순서, 사실 구조를 공유한다. 번역 때문에 정보가 추가·삭제되면 안 된다.
- 국문 카피를 먼저 잠그고, 영문은 자연스러운 법률·정책 영어로 별도 편집한다. 한국 법령명은 첫 언급에 공식·통용 영문명과 한글명을 함께 둘 수 있다.
- 각 언어의 `sourceTrace`는 같은 원문 위치를 가리킨다. 영문 `compressionNote`에는 번역 중 바뀐 문장 구조를 기록한다.
- 국문·영문 모두 별도 QA를 통과해야 완료다. 한쪽만 PASS면 세트 전체는 미완료다.
- 기획·마케팅 기준은 `references/ethos-card-design-v3.7.md`, 결정론적 제작 기준은 `references/ethos-card-design-v3.3.md`, 시각 기준은 `references/golden/game-overseas-en/`이다. 참고 문서의 지시는 현재 사용자 요청과 이 파일보다 우선하지 않는다.
- Golden Reference의 정보 위계·배경 리듬·타이포그래피를 따르되 문구나 법률 결론을 복사하지 않는다.

## 절대 규칙 (자동 검사 + 사람 확인)
- 원문에 없는 사실·숫자·조문·판례·사례를 넣지 않는다. 숫자·조문은 원문 표기 그대로.
- 원문의 「또는/그리고/~할 수 있다/~해야 할 수 있다」를 단정·기호(+ = ≠)로 바꾸지 않는다. 뜻이 넓어지거나 좁아지면 압축 실패.
- 카드 한 장 = 한 메시지. 결론이 둘이면 카드를 나눈다.
- 글자 크기: 본문 14px↑, 라벨·주석 12px↑, 프레임 12px↑. 작은 글자로 억지로 맞추지 말고 먼저 문장을 덜거나 카드를 나눈다.
- 블로그 전체를 카드에 압축하지 않는다. 뺀 내용은 `brief.md` 의 OMITTED 에 적는다.
- 폰트는 `fonts/` 파일만 사용. 로드 실패 시 중단(시스템 폰트로 계속하지 않는다). 외부 네트워크 호출 금지.
- 색은 `brand/tokens.css` 변수만. 임의 HEX 금지. 그라데이션·이모지·이미지 생성 텍스트 금지.
- 카드에 연락처·URL·버튼 금지. 마지막 장은 **무료 검토 안내 한 문장**(`docs/editorial.md` §5).
- 이력 소개 문장, About me 카드, "최고/대표/leading" 금지.
- 헤더·푸터·골드바는 `templates/base.css` 프레임 그대로. 카드마다 다시 만들지 않는다.

## 미감 우선 원칙
- `gates.json`의 글자 수·줄 수·영역 수·채움 비율·하단 여백·유형 반복은 **권고**다. 위반만으로 렌더를 막지 않는다.
- 하드 실패는 사실 잠금, 필수 폰트, 캔버스, 오버플로·클리핑, 프레임, 명백한 대비·금지 문구처럼 결과를 깨뜨리는 항목에 한정한다.
- 카드마다 내용을 같은 박스 구조에 끼워 넣지 않는다. `docs/layout-playbook.md`에서 메시지에 맞는 구도를 고른다.
- `checklist`와 `process`는 원문에 실제 확인 항목이나 순서가 있고 독자의 저장가치를 높일 때만 사용한다. 카드 유형 수와 조합은 편집 권고이며 렌더 하드 게이트가 아니다.
- 6장 이상 세트의 4개 유형·동일 유형 절반 이하 기준은 편집 권고다. 다양성을 위해 내용을 억지로 쪼개거나 법률 요건을 삭제하지 않는다. 질문·부정문·어미 비율을 맞추려고 확인된 결론을 흐리지 않는다.
- 크림 배경의 골드는 프레임·구분선·장식 숫자에만 사용한다. 헤드라인·소제목·본문·결론은 네이비 또는 네이비 박스로 렌더한다.
- 영문 헤드라인과 소제목은 700 이상의 웨이트로 렌더한다.
- 마지막 장은 질문만 나열하지 않는다. 독자가 직접 준비할 범위와 종합 검토가 필요한 경계처럼 실제 판단 기준을 제시한 뒤 CTA 한 문장으로 끝낸다.
- `pageTurn`은 다음 장에서 이어질 판단을 점검하는 편집 메타데이터로만 사용하며 실제 카드에는 표시하지 않는다. 가짜 긴장이나 “다음 장에서 공개”는 쓰지 않는다.
- 카드 우측 하단 쪽수는 표시하지 않는다. 프레임 QA용 영역은 유지하되 발행 이미지에는 숫자를 렌더하지 않는다.
- Golden Reference처럼 큰 제목, 충분한 여백, 네이비·크림 리듬, 골드의 절제, 카드별 하나의 시각적 중심을 우선한다.
- 비교 항목이 3개면 `2+1` 비대칭 박스 배치를 피하고 공통 `comparison`의 균등 3단 구조를 사용한다.
- 4단계 `process`는 숫자만 나열하지 말고 공통 단계 블록으로 시각적 중심을 만든다.
- 사례·재결 `quote` 카드는 본문을 과도하게 줄이지 말고 인용 패널의 좌측 골드 레일과 충분한 본문 크기를 유지한다.
- 영문이 조밀하면 자동으로 글자를 줄이지 않는다. 국문과 같은 사실·한정어를 보존하면서 문장 구조와 중복 표현을 먼저 압축한다.
- QA가 PASS여도 축소 시트가 답답하거나 어색하면 완료가 아니다. 반대로 권고 경고가 있어도 사람이 보기에 자연스럽고 읽기 좋으면 허용한다.
- 표지는 2초 안에 대상과 문제를 전달하도록 구체 상황·질문·대비 중 하나를 사용하되 클릭베이트를 만들지 않는다.
- 마지막 CTA에는 실제로 받을 수 있는 자료와 실제로 확인해 줄 결과를 구체적으로 적는다. 원문이나 승인된 서비스 범위를 넘어선 약속은 만들지 않는다.
- 게시용 캡션 첫 부분에는 대상 독자를 자연스럽게 명시한다. 마케팅 점수를 올리기 위해 법률 요건을 삭제하거나 카드를 빽빽하게 만들지 않는다.
- 인스타그램 발행은 `canvasProfile: portrait`, `visualFamily: social-native`를 기본값으로 삼는다. 카드별 `visualBeat`는 메시지의 역할에 맞추며 장식용 변주를 만들지 않는다.
- 2~3장 안에 독자가 바로 써볼 판단 기준이나 확인 항목을 둔다. 표지만 강하고 초반 실익이 없으면 카피를 다시 설계한다.

## 파일 지도
| 경로 | 역할 | 수정 |
|---|---|---|
| `docs/editorial.md` | 카피·Hook·서사·CTA 규칙 | 사람만 |
| `docs/html-contract.md` | 카드 HTML 계약 (data-속성) | 사람만 |
| `brand/tokens.json·css`, `brand/fonts.css`, `fonts/` | 브랜드 값·폰트 | 사람만 |
| `gates.json`, `scripts/qa_render.py`, `scripts/marketing_review.py` | 무결성 게이트와 비차단 마케팅 점검 | 사람만 |
| `templates/` | 프레임·카드 유형 CSS·스켈레톤 | 새 유형은 `card-types.css` 에만 추가 |
| `examples/` | 통과하는 예시(good)와 실패하는 예시(bad) | 참고용 |
| `references/` | v3.7 운용지침·v3.3 제작표준·승인 Golden Reference·manifest | 사람만 |
| `content/<ID>/` (blog.md, brief.md, card-data.ko/en.json, ko/, en/, distribution.md, assets.md, out/) | 작업물 | 에이전트 |
| `content/_TEMPLATE/` | 새 작업 폴더 양식 | 복사해서 사용 |

## 완료 정의
qa-report 가 PASS 이고, `humanChecks` 목록을 사용자에게 그대로 전달했을 때. 법령 해석의 정확성은 에이전트가 보증하지 않는다.

## Windows 실행

- 명령은 Git Bash에서 실행한다 (WSL bash 사용 금지)
- 환경 변수: PYTHON=python PYTHONUTF8=1
- 예: PYTHON=python PYTHONUTF8=1 python scripts/qa_render.py --html-dir content/<ID>/ko --source content/<ID>/blog.md --out content/<ID>/out/ko
