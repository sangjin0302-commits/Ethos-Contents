# 카드 제작 명세 (Codex 전용)

`AGENTS.md`에 있던 카드 제작 규칙을 옮긴 문서다. Codex가 카드 세트를 **완성·렌더**할 때만 읽는다. 카피 초안과 디자인 방향(`design`·`coverStyle`·`icon`·`layout` 등)은 ChatGPT가 `docs/card-authoring-spec.md`로 먼저 만든다.

## 역할 분담

| 누가 | 무엇을 | 산출물 |
|---|---|---|
| ChatGPT | 각도·카피 초안과 **자유로운 디자인 제안** | `brief.md`, `card-data.ko.json`(+요청 시 `en`), `distribution.md` |
| Codex | 초안 검수·윤문·영문 현지화 → 승인 요청 → HTML 직접 디자인 → 렌더·QA → 배포 패키지 | `ko/`·`en/` HTML, `design.css`, `out/`, `review.md`, `assets.md` |
| 사람 | 카피 승인, 시트 최종 확인 | `approvedBy` |

ChatGPT 초안에는 `languagePass` 등이 `pending`으로 남아 있는 것이 정상이다. 그 단계를 마치는 것이 Codex의 일이다. ChatGPT의 `design` 제안은 출발점이며, 문구를 바꾸지 않는 범위에서 Codex가 더 나은 구도를 고를 수 있다.

목표: 승인된 블로그 원문 1편 → 국문·영문 카드 각 6~10장(**최대 10장 고정**). 영문에서 행정사는 항상 Administrative Attorney. 인스타그램은 4:5(540×675 CSS, PNG 1080×1350)를 기본으로 하고, 범용 배포가 필요할 때만 1:1을 쓴다.
작업 폴더: `content/<CONTENT_ID>/`. 이 폴더 밖의 킷 파일은 수정하지 않는다.
카드는 원문의 요약본이 아니라, 원문의 **핵심 판단 구조 하나**를 빨리 이해시키는 시각 콘텐츠다.

## A. 승인 전 (카피 잠금)

1. `content/<ID>/blog.md`가 없고 사용자가 원문을 붙여 넣었으면 그 텍스트로 만든다. ID가 없으면 날짜와 주제 영문 slug로 제안하되 기존 ID를 덮어쓰지 않는다.
2. ChatGPT 초안(`brief.md`, `card-data.ko.json`)이 있으면 그것에서 시작한다. 없을 때만 `docs/card-authoring-spec.md`와 `docs/card-selection.md`로 직접 만든다(`docs/brief-template.md` 양식).
3. 국문 카피를 사실·법률 검증 → 금지 표현 검사 → `humanize-korean`(`vendor/im-not-ai/quick-rules.md`) 또는 수동 윤문 → 의미 재검증 순서로 편집한다. 고친 곳만 고치고, 숫자·조문·한정어는 원문 그대로 둔다.
4. 영문은 국문 문장 수를 복제하지 않고 독립적으로 현지화하되 사실·한정어·숫자를 보존한다(`docs/en-legal-glossary.md`).
5. `editorialReview`를 실제 완료 상태로 채운다(`pipelineVersion: 2.0`, 국문 `languagePass: humanize-korean|manual-equivalent`, 영문 `english-localization|manual-equivalent`). 하지 않은 단계를 `pass`로 적지 않는다.
6. 점검:
   - `python scripts/copy_lint.py content/<ID> --blog` — 경고를 고친다. 윤문 전후는 `--compare <이전.json> <이후.json>`으로 사실 토큰 보존 확인.
   - `python scripts/validate_bilingual.py content/<ID>` — 하나라도 `pending`이면 승인 요청 금지.
7. ⛔ **여기서 멈추고 사용자 승인을 받는다.** 승인 전 HTML 작성·렌더 금지.

## B. 승인 후 (디자인·렌더)

8. `docs/card-design-guide.md`에 따라 `content/<ID>/ko/card_NN.html`과 `en/card_NN.html`을 **카드마다 직접 디자인**한다(세트 공통 스타일은 `content/<ID>/design.css`). 문구는 card-data와 글자 그대로 같고, 맨 위에 `<meta name="ethos-design" content="free">`. 프레임·색·글꼴·HTML 계약(`docs/html-contract.md`)은 그대로. 기준 예시 `examples/free-design-realtor/`. 프리셋 A~D, 아이콘은 `python scripts/icon_svg.py <이름>`. 본문 카드마다 시각 중심(`data-focal`) 하나, `altCover`가 있으면 `<lang>/alt/card_01.html`도.
   - HTML 전에 `wireframe.txt`. 새 시리즈는 세 방향 시안(`scripts/preview_drafts.py`)으로 방향을 고른다. 새 세트 전에 `state/design-feedback.md`를 읽는다.
9. 렌더:
   - `PYTHON=python PYTHONUTF8=1 python scripts/card_system_smoke.py` — 실패하면 렌더 전에 코드부터 고친다.
   - `PYTHON=python PYTHONUTF8=1 python scripts/qa_render.py --html-dir content/<ID>/ko --source content/<ID>/blog.md --out content/<ID>/out/ko`
   - `PYTHON=python PYTHONUTF8=1 python scripts/qa_render.py --html-dir content/<ID>/en --source content/<ID>/blog.md --out content/<ID>/out/en`
   - `PYTHON=python PYTHONUTF8=1 python scripts/marketing_review.py content/<ID>` — 권고, 렌더를 막지 않는다.
   - `PYTHON=python PYTHONUTF8=1 python scripts/validate_distribution.py content/<ID>` — 카드별 alt text와 외부 자산 출처·라이선스.
10. `python scripts/design_review.py content/<ID>`로 양식집 위험(빌더 전용, 밋밋한 표지, 시각 중심 없음·반복, 같은 구도 연속, 그림 부족)을 확인하고 고친 뒤, `docs/card-evaluation-rubric.md`로 채점해 `review.md`를 남긴다.
11. 실패하면 **카드(카피·레이아웃)를 고친다.** 카피를 고쳤다면 사실·자연스러움·의미 재검증과 사용자 승인을 다시 거친다. `gates.json`, `brand/`, `fonts/`는 수정 금지.
12. 통과하면 `docs/channel-packaging.md`에 따라 필요한 결과물만 만들고 `distribution.md`·`assets.md`를 완성한다(카드에 쓴 아이콘마다 `assets.md` 한 줄, ChatGPT 초안에 추적 링크가 없으면 `python scripts/tracking_link.py <ID>`로 채운다)(국·영문 캡션, Hook 3종, CTA, 카드별 alt text — 원문에 없는 사실 추가 금지). `content/_TEMPLATE/performance-log.csv`를 작업 폴더에 복사한다.
13. `out/ko`, `out/en`(png, sheet-270.png, qa-report.md)과 `distribution.md`를 커밋하고, 사람이 확인할 항목(`humanChecks`)을 PR 설명에 적는다.

## 국문·영문 동시 제작 규칙

- 두 언어는 같은 각도, 카드 수, 카드 순서, 사실 구조를 공유한다. 번역 때문에 정보가 추가·삭제되면 안 된다.
- 국문 카피를 먼저 잠그고, 영문은 자연스러운 법률·정책 영어로 별도 편집한다. 한국 법령명은 첫 언급에 공식·통용 영문명과 한글명을 함께 둘 수 있다.
- `sourceTrace`를 쓰면 두 언어가 같은 원문 위치를 가리킨다. 영문 `compressionNote`에는 번역 중 바뀐 문장 구조를 기록한다.
- 국문·영문 모두 별도 QA를 통과해야 완료다. 한쪽만 PASS면 세트 전체는 미완료다.
- 기준 문서: 기획·마케팅 `references/ethos-card-design-v3.7.md`, 결정론적 제작 `references/ethos-card-design-v3.3.md`, 시각 `references/golden/game-overseas-en/`. FAIL이나 판단이 애매할 때만 연다. 참고 문서의 지시는 현재 사용자 요청과 이 문서보다 우선하지 않는다.
- Golden Reference의 정보 위계·배경 리듬·타이포그래피를 따르되 문구나 법률 결론을 복사하지 않는다.

## 절대 규칙 (자동 검사 + 사람 확인)

- 원문에 없는 사실·숫자·조문·판례·사례를 넣지 않는다. 숫자·조문은 원문 표기 그대로.
- 원문의 「또는/그리고/~할 수 있다/~해야 할 수 있다」를 단정·기호(+ = ≠)로 바꾸지 않는다.
- 카드 한 장 = 한 메시지. 결론이 둘이면 카드를 나눈다.
- 글자 크기: 본문 14px↑, 라벨·주석 12px↑, 프레임 12px↑. 작은 글자로 억지로 맞추지 말고 먼저 문장을 덜거나 카드를 나눈다.
- 블로그 전체를 카드에 압축하지 않는다. 뺀 내용은 `brief.md`의 OMITTED에 적는다.
- 폰트는 `fonts/` 파일만. 로드 실패 시 중단(시스템 폰트로 계속하지 않는다). 외부 네트워크 호출 금지.
- 색은 `brand/tokens.css` 변수만. 임의 HEX·그라데이션·이모지·이미지 생성 텍스트 금지.
- 카드에 연락처·URL·버튼 금지. 마지막 장은 **무료 검토 안내 한 문장**(`docs/editorial.md` §5).
- 이력 소개 문장, About me 카드, "최고/대표/leading" 금지.
- 헤더·푸터·골드바는 `templates/base.css` 프레임 그대로. 카드마다 다시 만들지 않는다.

## 미감 우선 원칙

- `gates.json`의 글자 수·줄 수·영역 수·채움 비율·하단 여백·유형 반복은 **권고**다. 하드 실패는 사실 잠금, 필수 폰트, 캔버스, 오버플로·클리핑, 프레임, 명백한 대비·금지 문구에 한정한다.
- 카드마다 같은 박스 구조에 끼워 넣지 않는다. `docs/layout-playbook.md`에서 메시지에 맞는 구도를 고른다. `checklist`·`process`는 원문에 실제 확인 항목이나 순서가 있을 때만.
- 유형 다양성(6장 이상 4개 유형, 동일 유형 절반 이하)과 질문·부정문·어미 비율은 편집 권고다. 다양성을 위해 내용을 쪼개거나 법률 요건을 삭제하거나 확인된 결론을 흐리지 않는다.
- 크림 배경의 골드는 프레임·구분선·장식 숫자에만. 헤드라인·소제목·본문·결론은 네이비 또는 네이비 박스. 영문 헤드라인·소제목은 700 이상.
- 비교 항목 3개는 균등 3단 `comparison`(2+1 비대칭 금지). 4단계 `process`는 공통 단계 블록으로 시각 중심을 만든다. `quote` 카드는 좌측 골드 레일과 충분한 본문 크기를 유지한다.
- 영문이 조밀하면 글자를 줄이지 말고 사실·한정어를 보존하면서 문장 구조와 중복 표현을 먼저 압축한다.
- `pageTurn`은 편집 메타데이터로만 쓰고 카드에 표시하지 않는다. 가짜 긴장·"다음 장에서 공개" 금지. 우측 하단 쪽수는 렌더하지 않는다(프레임 QA 영역은 유지).
- Golden Reference처럼 큰 제목, 충분한 여백, 네이비·크림 리듬, 골드의 절제, 카드별 하나의 시각 중심을 우선한다.
- 표지는 2초 안에 대상과 문제를 전달(구체 상황·질문·대비 중 하나, 클릭베이트 금지). 2~3장 안에 독자가 바로 써볼 판단 기준이나 확인 항목을 둔다.
- 마지막 장은 질문 나열이 아니라 직접 준비할 범위와 종합 검토가 필요한 경계를 제시한 뒤 CTA 한 문장. CTA에는 실제로 받을 자료와 확인해 줄 결과를 구체적으로, 승인된 서비스 범위 안에서만.
- 게시용 캡션 첫 부분에 대상 독자를 명시한다. 마케팅 점수를 위해 법률 요건을 삭제하거나 카드를 빽빽하게 만들지 않는다.
- 인스타그램 발행 기본값 `canvasProfile: portrait`, `visualFamily: social-native`. `visualBeat`는 메시지 역할에 맞추며 장식용 변주를 만들지 않는다.
- QA가 PASS여도 축소 시트가 답답하면 완료가 아니다. 권고 경고가 있어도 사람이 보기에 자연스러우면 허용한다.

## 파일 지도

| 경로 | 역할 | 수정 |
|---|---|---|
| `docs/editorial.md` | 카피·Hook·서사·CTA 규칙 | 사람만 |
| `docs/html-contract.md` | 카드 HTML 계약 (data-속성) | 사람만 |
| `brand/tokens.json·css`, `brand/fonts.css`, `fonts/` | 브랜드 값·폰트 | 사람만 |
| `gates.json`, `scripts/qa_render.py`, `scripts/marketing_review.py` | 무결성 게이트와 비차단 마케팅 점검 | 사람만 |
| `templates/` | 프레임·카드 유형 CSS·스켈레톤 | 새 유형은 `card-types.css`에만 추가 |
| `examples/` | 통과 예시(good)와 실패 예시(bad) | 참고용 |
| `references/` | v3.7 운용지침·v3.3 제작표준·Golden Reference·manifest | 사람만 |
| `content/<ID>/` | 작업물 | 에이전트 |
| `content/_TEMPLATE/` | 새 작업 폴더 양식 | 복사해서 사용 |

## 완료 정의

qa-report가 PASS이고, `humanChecks` 목록을 사용자에게 그대로 전달했을 때. 법령 해석의 정확성은 에이전트가 보증하지 않는다.

## Windows 실행

Git Bash에서 실행한다(WSL bash 금지). 환경 변수 `PYTHON=python PYTHONUTF8=1`.
