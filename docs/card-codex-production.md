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
카드는 원문의 요약본이 아니라, 원문의 **핵심 판단 구조 하나**를 빨리 이해시키는 시각 콘텐츠다. 중심 질문에 맞는 실제 근거를 승인 원문과 기존 `research/`에서 먼저 확인한다(`docs/brand-philosophy.md`, 새 근거 확인은 `docs/evidence-gate.md`). 새 근거·장면은 원문 보강·검증·승인 후 쓰며 실제 사건에 원문 밖 대화·감정·피해액·결과를 보태지 않는다.

## A. 승인 전 (카피 잠금)

1. `content/<ID>/blog.md`가 없고 사용자가 원문을 붙여 넣었으면 그 텍스트로 만든다. ID가 없으면 날짜와 주제 영문 slug로 제안하되 기존 ID를 덮어쓰지 않는다.
2. ChatGPT 초안(`brief.md`, `card-data.ko.json`)이 있으면 그것에서 시작한다. 없을 때만 `docs/card-authoring-spec.md`와 `docs/card-selection.md`로 직접 만든다(`docs/brief-template.md` 양식).
3. 국문 카피를 사실·법률 검증 → 금지 표현 검사 → `humanize-korean`(`vendor/im-not-ai/quick-rules.md`) 또는 수동 윤문 → 의미 재검증 순서로 편집한다. 고친 곳만 고치고, 숫자·조문·한정어는 원문 그대로 둔다.
4. 영문은 국문 문장 수를 복제하지 않고 독립적으로 현지화하되 사실·한정어·숫자를 보존한다(`docs/en-legal-glossary.md`).
5. `editorialReview`를 실제 완료 상태로 채운다(`pipelineVersion: 2.0`, 완료 상태 `languagePass: pass`, 국문 `languageMethod: humanize-korean|manual-equivalent`, 영문 `languageMethod: english-localization|manual-equivalent`). 하지 않은 단계를 `pass`로 적지 않는다. ChatGPT 최소 JSON에 빠진 제작 메타데이터도 이때 채운다: `canvasProfile: portrait`, `visualFamily: social-native`, `marketing`(brief.md의 독자·질문·CTA 자료·확인 결과), 카드별 `oneMessage`·`sourceTrace`(두 언어가 같은 원문 제목). `marketing_review.py`가 이 필드를 읽으므로 비워 두면 내용과 무관하게 점수가 30점대로 나온다.
6. 점검:
   - `python scripts/copy_lint.py content/<ID> --blog` — 경고를 고친다. 윤문 전후는 `--compare <이전.json> <이후.json>`으로 사실 토큰 보존 확인.
   - `python scripts/validate_bilingual.py content/<ID>` — 하나라도 `pending`이면 승인 요청 금지.
7. ⛔ **여기서 멈추고 사용자 승인을 받는다.** 승인 전 HTML 작성·렌더 금지.

## B. 승인 후 (디자인·렌더)

8. 출발점: `python scripts/auto_design.py content/<ID> --lang ko --out content/<ID>/ko --production`(영문도 같게)로 JSON 기반 초안을 만든 뒤, `<link>`에 `../design.css`를 더하고 `<meta name="ethos-auto">`를 지운 다음 카드마다 다듬는다. `docs/card-design-guide.md`에 따라 `content/<ID>/ko/card_NN.html`과 `en/card_NN.html`을 **카드마다 직접 디자인**한다(세트 공통 스타일은 `content/<ID>/design.css`). 문구는 card-data와 글자 그대로 같고, 맨 위에 `<meta name="ethos-design" content="free">`. 프레임·색·글꼴·HTML 계약(`docs/html-contract.md`)은 그대로. 기준 예시 `examples/free-design-realtor/`. 프리셋 A~D, 아이콘은 `python scripts/icon_svg.py <이름>`. 본문 카드마다 시각 중심(`data-focal`) 하나, `altCover`가 있으면 `<lang>/alt/card_01.html`도.
   - HTML 전에 `wireframe.txt`. 새 시리즈는 세 방향 시안(`scripts/preview_drafts.py`)으로 방향을 고른다. 새 세트 전에 `state/design-feedback.md`를 읽는다. 의미 보조 SVG 이모티콘과 문서 대조·조건 묶음은 `docs/card-design-guide.md`의 시각 편집 기본값을 적용한다.
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
- 색은 `brand/tokens.css` 변수만. 임의 HEX·그라데이션·이미지 생성 텍스트 금지. 의미 보조용 로컬 SVG 이모티콘은 기본 허용한다(`docs/asset-policy.md`). 운영체제 이모지 글꼴·이미지 속 본문은 쓰지 않는다. 프레임·텍스트·도식은 브랜드 색을 유지하고, 출처가 기록된 이모티콘 원본의 고유색만 허용한다.
- 카드에 연락처·URL·버튼 금지. 마지막 장은 **무료 검토 안내 한 문장**(`docs/editorial.md` §5).
- 이력 소개 문장, About me 카드, "최고/대표/leading" 금지.
- 헤더·푸터·골드바는 `templates/base.css` 프레임 그대로. 카드마다 다시 만들지 않는다.

## 미감 우선 원칙

- 발행용 `--production`은 본문 글자 크기를 자동 축소하지 않고 넘침만 측정한다. 미리보기 축소도 최대 8%이며 QA에 실제 배율을 남긴다. 넘침은 배치부터 고치고, 문구 변경이 필요하면 별도 승인한다.
- 디자인 휴리스틱 경고는 승인본에서도 CI 실패 사유가 아니다. 자동 빌더로 되돌린 미완성 발행본과 사실·폰트·캔버스·오버플로 같은 하드 실패는 계속 차단한다. 아이콘 개수나 유형 비율을 채우기 위해 장식을 추가하지 않는다.
- 제목·본문·결론의 중복은 초안 편집에서 정리한다. 승인된 문구가 들어 있는 결론 영역을 CSS로 감추거나 자동 삭제하지 않는다.

- `gates.json`의 글자 수·줄 수·영역 수·채움 비율·하단 여백·유형 반복은 **권고**다. 하드 실패는 사실 잠금, 필수 폰트, 캔버스, 오버플로·클리핑, 프레임, 명백한 대비·금지 문구에 한정한다.
- 연속 카드가 같은 주장을 되풀이하면 합치거나 덜어 낸다. 원문에 있는 조건 차이·문서 항목·동일 단위 수치로 판단의 차이를 시각화하며 숫자를 창작하지 않는다. 카드마다 같은 말풍선·상자·아이콘 구도에 끼워 넣지 않는다. `docs/layout-playbook.md`에서 메시지에 맞는 구도를 고른다. `checklist`·`process`는 원문에 실제 확인 항목이나 순서가 있을 때만.
- 유형 다양성(6장 이상 4개 유형, 동일 유형 절반 이하)과 질문·부정문·어미 비율은 편집 권고다. 다양성을 위해 내용을 쪼개거나 법률 요건을 삭제하거나 확인된 결론을 흐리지 않는다.
- 크림 배경의 골드는 프레임·구분선·장식 숫자에만. 헤드라인·소제목·본문·결론은 네이비 또는 네이비 박스. 영문 헤드라인·소제목은 700 이상.
- 비교 항목 3개는 균등 3단 `comparison`(2+1 비대칭 금지). 4단계 `process`는 공통 단계 블록으로 시각 중심을 만든다. `quote` 카드는 좌측 골드 레일과 충분한 본문 크기를 유지한다.
- 영문이 조밀하면 글자를 줄이지 말고 사실·한정어를 보존하면서 문장 구조와 중복 표현을 먼저 압축한다.
- `pageTurn`은 편집 메타데이터로만 쓰고 카드에 표시하지 않는다. 가짜 긴장·"다음 장에서 공개" 금지. 우측 하단 쪽수는 렌더하지 않는다(프레임 QA 영역은 유지).
- Golden Reference처럼 큰 제목, 충분한 여백, 네이비·크림 리듬, 골드의 절제, 카드별 하나의 시각 중심을 우선한다.
- 표지는 2초 안에 대상과 문제를 전달(구체 상황·질문·대비 중 하나, 클릭베이트 금지). 2~3장 안에 독자가 바로 써볼 판단 기준이나 확인 항목을 둔다.
- 마지막 장은 질문 나열이 아니라 직접 준비할 범위와 종합 검토가 필요한 경계를 제시한 뒤 CTA 한 문장. CTA에는 실제로 받을 자료와 확인해 줄 결과를 구체적으로, 승인된 서비스 범위 안에서만.
- 받을 자료(`content/<ID>/lead-magnet.md`)를 배포할 때는 `lead-magnet/checklist.html`(A4, 브랜드 글꼴·색, 연락처·URL 없음)로 디자인하고 `python scripts/render_lead_magnet.py content/<ID>/lead-magnet/checklist.html`로 PDF·PNG를 만든다. 글꼴 미로드·넘침이면 FAIL. 예시: `content/TEST-SUSPENSION-V3/lead-magnet/`.
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

문구 개요, JSON 초안, 렌더·자동 QA, 실제 이미지 시각 검토의 완료 여부를 각각 보고한다. 렌더 결과의 개별 카드와 축소 시트를 실제 열어 확인하고 `review.md`에 결과를 남긴 뒤, qa-report PASS와 남은 `humanChecks`를 사용자에게 전달한다. 시각 검토를 하지 못했다면 그 단계는 미완료다. 자동 QA PASS는 디자인 품질·법률 검증·사람의 최종 승인을 대신하지 않는다. 이 상태 구분은 기존 검수의 보고 기준이며 새 점수표나 별도 검수 패스를 추가하지 않는다.

## Windows 실행

Git Bash에서 실행한다(WSL bash 금지). 환경 변수 `PYTHON=python PYTHONUTF8=1`.

## 채택된 문장·배치 개선의 적용

새 세트의 문체 편집에는 `docs/card-authoring-spec.md`의 ‘문장 호흡과 읽기 폭’, 직접 디자인에는 `docs/card-design-guide.md`의 ‘문장 호흡에 맞춘 배치’를 적용한다. 역할·행동을 문장으로 풀고 법률 조건을 보존한 뒤, 좁은 열과 넓은 행 등 실제 배치를 비교한다. JSON과 HTML 카피는 일치해야 한다.

기존 승인본 개선은 별도 초안과 원본 해시로 진행하고 이전/개선 렌더를 같은 환경에서 만든다. 국문만 요청된 비교는 국문 범위로 보고하며 영문·전체 배포 완료로 확대하지 않는다. 사용자 채택·커밋/병합 허가·실제 발행 상태도 따로 기록한다. OEM CARD-FLOW의 개선 원칙은 새 작업에 적용하지만 기존 승인 콘텐츠를 자동 재작성하지 않는다.

## 영문 CARD-FLOW 재사용

영문 제작은 작성 명세의 ‘영문 문장·배치 적용’과 디자인 가이드의 ‘영문 읽기 폭과 줄바꿈’을 함께 적용한다. 이는 Codex 직접 제작의 기본 편집 규칙이며 JSON 자동 미리보기가 자연어 design 지시를 자동 구현한다는 뜻은 아니다.

최신 국문과 영문을 카드별로 대조해 주체·의무/재량·AND/OR·범위·문서명·서비스 범위를 기록한다. 예외 적용에 필요한 조건을 다음 장에만 숨기지 않는다. JSON 구조 검증은 의미 검증을 대신하지 않는다. 실제 검수가 끝난 뒤 languagePass와 english-localization 방법을 기록한다.

같은 브라우저·크기·폰트 환경에서 전후 영문을 렌더하고 개별 PNG·축소 시트를 확인한다. 언어별 CSS 수정 후 국문 원본 보존도 확인한다. 문구 구성이 달라진 장은 순수 디자인 비교와 구별한다. 원본 해시, 실제 문구 표시, 넘침·자동 축소 여부, 자산 로드, 남은 밀도 권고를 review.md에 남긴다. 사용자 채택은 approval.md에 따로 기록하고 발행 여부와 구별한다.
