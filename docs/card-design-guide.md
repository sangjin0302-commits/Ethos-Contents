# 카드 자유 디자인 가이드 (B 방식 · Codex·Claude용)

카드 HTML을 템플릿 빌더(`scripts/build_cards.py`)로 찍어 내지 않고, 카드마다 내용에 맞춰 직접 디자인하는 방식이다. 브랜드 값·폰트·프레임·QA 게이트는 그대로 지키고 **본문 영역의 레이아웃과 글자 크기만 자유**다.

- 디자인 과정의 바탕: `vendor/anthropic-frontend-design/SKILL.md`(Anthropic `frontend-design`, Apache-2.0). 브랜드가 정해져 있으므로 그 문서의 색·글꼴 선택 부분은 이 가이드가 대신하고, **과정·위계·절제·자기 검토** 부분을 따른다.
- 기준 예시: `examples/free-design-realtor/`(시범 세트, 발행 금지). 시각 기준 `references/golden/game-overseas-en/`.
- 함께 참고한 공개 프로젝트(코드·문서를 복사하지 않고 방식만 가져옴): greeun/card-news-harness(MIT, 한글 타이포·평가 하네스), Kanghyeop/card-news-simple-skill(ISC, 3:1 비율·레퍼런스 흡수·세 방향 시안), Giii-sik/card-news-publication-workflow(라이선스 표기 없음, 와이어프레임·단계별 확인 방식만 참고).

## 1. 역할

| 누가 | 무엇을 |
|---|---|
| ChatGPT | `card-data.ko/en.json`(문구 원본)과 카드별 `design` 한 줄(시각 중심·구도 제안) |
| Codex·Claude | 이 가이드로 `content/<ID>/ko|en/card_NN.html`과 세트 공통 `content/<ID>/design.css`를 직접 디자인 → `qa_render.py`로 렌더 → 축소 시트를 보고 고침 |
| 사람 | 축소 시트와 문구를 보고 승인 |

## 2. 바꾸지 않는 것

- 문구: card-data의 헤드라인·본문·결론·표지 약속을 **글자 그대로** 쓴다(줄바꿈 `<br>`만 허용). 렌더 워크플로가 "카피 잠금"으로 대조해 다르면 실패한다. 문구를 바꾸려면 card-data를 먼저 고치고 다시 승인받는다.
- 프레임: `templates/base.css`의 머리말·꼬리말·골드바 마크업을 그대로 쓴다(`examples/free-design-realtor/ko/card_01.html` 복사). 캔버스 540×675.
- 색: `brand/tokens.css` 변수만. 크림 위 골드는 선·장식(`data-decor`)에만. 그라데이션·이모지·이미지 속 글자 금지.
- 글꼴: `ETHOS Serif`(제목), `ETHOS Sans`(본문), `ETHOS Display`(큰 숫자). 외부 글꼴·네트워크 금지.
- HTML 계약: `docs/html-contract.md`의 `data-zone`(title·main·take), `data-role`, `data-decor`, `data-frame`. 본문 14px 이상, 라벨 12px 이상.
- 파일 맨 위에 `<meta name="ethos-design" content="free">`를 넣는다. 이 표시가 있는 파일만 빌더 대신 그대로 렌더된다.

## 3. 디자인 원칙

1. **위계가 먼저다.** 제목 38~44px, 본문 20~25px, 보조 17~20px. 본문은 제목의 60%를 넘지 않는다. 제목과 본문이 같은 크기로 보이면 실패다.
2. **카드마다 시각 중심은 하나.** 큰 숫자 대비, 실제 순서, 두 기준의 대조, 질문 세 개 중 하나만 주연으로 둔다. 나머지는 조용하게.
3. **구조는 정보다.** 번호는 실제 순서일 때만, 상자는 경계·대조가 필요할 때만 쓴다. 모든 내용을 같은 둥근 상자에 나눠 담지 않는다(frontend-design의 "SaaS 카드 묶음" 경고).
4. **여백은 내용 묶음의 바깥에 둔다.** 채움 비율을 목표로 글자·행간·아이콘을 키우지 않는다. 관련 항목은 일정한 간격으로 묶고 제목과 결론 사이의 가용 영역 중앙에 놓는다. 짧은 카드는 여백을 남겨도 된다. 묶음 안이 벌어져 읽는 순서가 끊기는 것부터 고친다.
5. **결론 띠(bar)는 세트의 40% 이하.** 표지·핵심 판단·마지막 장에만. 나머지는 구분선 한 줄로 끝낸다.
6. **리듬.** 네이비·크림을 번갈아 쓰되, 연속 두 장이 같은 구도가 되지 않게 한다.
7. **줄바꿈을 다듬는다.** 가운뎃점으로 묶인 낱말(`과실·시정`)은 `<span class="nobr">`로 감싸 줄 첫머리에 "·"가 오지 않게 한다. 제목은 의미 단위로 `<br>`을 넣는다(조사 앞에서 끊지 않는다). 영문 제목은 3줄 이내.
8. **중복을 뺀다.** 머리말에 시리즈명이 있으므로 표지에 같은 시리즈명 칩을 또 두지 않는다. 같은 말을 두 번 쓰지 않는다.
9. **흔한 AI 디자인 습관을 피한다:** 제목 속 한 단어만 색 바꾸기, 영문 대문자 라벨, 모든 제목 위의 작은 머리표, 의미 없는 01/02/03, 같은 그림자·같은 둥근 모서리의 상자 반복.

## 4. 작업 순서 (카드 한 세트)

0. **출발점**: `state/design-feedback.md`(지금까지의 피드백)와 `docs/card-patterns.md`(카드 유형·표지 패턴)를 읽는다. 세트 스타일은 처음부터 쓰지 않고 프리셋에서 출발한다: `content/<ID>/design.css` 첫 줄에 `@import url("../../templates/presets/ethos-a.css");`(기본 A, 굵은 타이포 B, 크림 여백형 C, 마루 부리 명조 제목 + 아이콘 D). 세트에만 필요한 조정을 그 아래에 적는다.
1. **설계 메모**: `design.css` 맨 위 주석에 색 역할, 글자 크기 단계, 카드별 시각 중심 한 줄을 적는다.
2. **검토**: 메모가 어느 세트에나 쓸 수 있는 기본값이면(예: 모든 카드가 상자 두 개) 그 부분을 이 주제에 맞게 바꾼다.
3. **작성**: 카드마다 HTML을 쓴다. 공통 스타일은 `design.css`, 프레임은 복사.
4. **렌더**: `python scripts/qa_render.py --html-dir content/<ID>/ko --source content/<ID>/blog.md --out content/<ID>/out/ko`
5. **디자인 점검**: `python scripts/design_review.py content/<ID>`가 PASS가 될 때까지 시각 중심 종류와 구도를 바꾼다(권고, CI 요약에도 나온다).
6. **자기 검토**: `sheet-270.png`를 보고 ① 제목·본문 위계 ② 빈 띠 ③ 같은 구도 반복 ④ 한 장 한 메시지를 확인한다. 장식 하나를 빼 본다.
7. 영문도 같은 순서로 하되 문장 길이에 맞춰 크기를 다시 정한다(같은 숫자를 복사하지 않는다).

## 5. 기본 빌더와의 관계

- 자유 디자인 HTML이 없는 카드는 렌더 워크플로가 기본 빌더로 만든다. ChatGPT만으로 미리보기가 필요할 때는 빌더 결과를 쓰고, 발행본은 이 가이드로 디자인한다.
- 빌더 결과를 출발점으로 복사해 고쳐도 된다. 그때도 맨 위 메타 표시를 넣는다.

## 6. 글자 체계 (540×675 CSS 기준, PNG는 2배)

참고한 공개 프로젝트의 1080px 기준 값을 절반으로 옮겨 에토스에 맞췄다(greeun/card-news-harness, Giii-sik/card-news-publication-workflow, Kanghyeop/card-news-simple-skill).

| 역할 | 글꼴 | 크기 | 굵기 | 줄 간격 |
|---|---|---:|---:|---:|
| 표지 제목 | ETHOS Serif | 44~50px | 700 | 1.2 |
| 카드 제목 | ETHOS Serif | 36~43px | 700 | 1.25 |
| 큰 숫자 | ETHOS Display 또는 Pretendard 800 | 56~90px | 800~900 | 1.0 |
| 본문 | Pretendard | 21~23px | 500 | 1.55 |
| 라벨·소제목 | Pretendard | 17~20px | 700 | 1.4 |
| 각주·출처 | Pretendard | 16px | 500 | 1.5 |

- **한 카드 안에서 가장 큰 글자와 가장 작은 글자의 비율은 3:1 이내**(큰 숫자 카드는 예외). 큰 제목 옆에 작은 글씨가 섞이면 "AI가 만든 PPT"처럼 보인다.
- 한글 자간: 제목 -0.5~-1px, Pretendard 본문 -0.3px. 넓은 자간 라벨은 쓰지 않는다.
- 본문은 Pretendard로 쓴다(로컬 `fonts/`, SIL OFL). 제목은 브랜드 세리프(ETHOS Serif)를 유지한다. 시안에서 전체 Pretendard 방향을 고르면 그 세트는 제목도 Pretendard 800을 쓸 수 있다.
- 텍스트는 왼쪽 정렬과 같은 왼쪽 기준선을 유지한다. **본문 묶음의 세로 중앙 배치와 문자의 가운데 정렬은 다르다.** 표지 그림·단일 숫자는 가로 중앙도 가능하지만 긴 본문은 왼쪽 정렬한다.

## 7. 줄바꿈과 분량

- 제목은 2줄 이내, 본문은 3줄 이내가 기본. 넘치면 문장을 줄이고, 그래도 넘치면 카드를 나눈다. 글자를 줄여 맞추지 않는다.
- 두 줄 제목은 의미 단위로 `<br>`을 넣어 두 줄 길이를 비슷하게 한다. 조사(은·는·이·가·을·를)로 줄이 시작되지 않게 한다. 한 음절만 다음 줄에 남기지 않는다.
- 숫자와 단위를 떼지 않는다("6<br>개월" 금지). 가운뎃점 묶음은 `<span class="nobr">`로 감싼다.
- 대략의 한도(국문): 표지 제목 22자, 카드 제목 28자, 본문 한 덩어리 90자, 대조 한 줄 38자, 큰 숫자 밑 설명 36자.

## 8. 카피 금지 목록 (카드 위)

AI가 쓴 티가 나는 말과 번역투는 쓰지 않는다: "요즘 핫한", "꼭 알아야 할", "여러분", "~할 필요가 있습니다", "~에 대해 알아보겠습니다", "~를 통해", "중요한 것은 ~입니다", "카드뉴스로 알아보는", 느낌표 남발. 대신 독자의 상황과 판단을 바로 말한다(`examples/writing/README.md`).

## 9. 작업 산출물 추가

- **와이어프레임**: HTML을 쓰기 전에 `content/<ID>/wireframe.txt`에 카드마다 ASCII로 구도를 그린다(시각 중심, 정렬, 결론 위치).
- **세 방향 시안**(새 시리즈 첫 세트 또는 사용자가 원할 때): 표지와 본문 한 장을 세 방향(A 브랜드 세리프+Pretendard 본문 / B 전체 Pretendard 굵은 타이포 / C 크림 바탕 여백형)으로 만들어 `content/<ID>/drafts/`에 렌더해 보여 주고 고르게 한다. 고른 방향을 `design.css` 설계 메모에 적는다.
- **레퍼런스 흡수**: 사용자가 닮고 싶은 카드뉴스 캡처를 주면 `references/inspiration/<이름>/`에 두고, 위계·여백·정렬·밀도·장치·말투를 분석해 `references/inspiration/<이름>/notes.md`에 적은 뒤 `design.css`와 이 가이드에 반영한다. 색 체계를 바꾸는 큰 전환은 사용자 확인 후에 한다.
- **평가**: 렌더 후 `docs/card-evaluation-rubric.md`로 스스로 채점해 `content/<ID>/review.md`에 남긴다. 2배 가중 항목(표지·카피, 가독성·일관성)이 4점 미만이면 고친 뒤 다시 렌더한다.

## 10. 프리셋과 피드백으로 진화하기

- 프리셋(`templates/presets/ethos-a|b|c|d.css`)이 세트 사이의 일관성을 만든다. 세트마다 새 스타일을 발명하지 않는다.
- 사용자가 디자인·문구 피드백을 주면 `state/design-feedback.md`에 원문 그대로 적고, 같은 지적이 다시 나오지 않도록 프리셋이나 이 가이드를 고친다. 한 세트에서만 맞는 조정은 그 세트의 `design.css`에만 둔다.
- 사용자가 결과에 충분히 만족한 세트가 나오면 그 세트의 조정을 프리셋으로 올린다.
- 자유 디자인 카드의 본문 글자는 16px 이상이다(QA가 검사한다. 1080px PNG 기준 32px).

## 10-0. 빈칸 점검 (empty-band)

`qa_render.py`가 본문 영역에서 내용 없는 가장 긴 가로 띠를 재서 22%를 넘으면 권고한다(`empty-band`). 빈 띠가 크다는 사실만으로 디자인 실패는 아니다. 배경색 패널이 지표를 낮출 수도 있으므로 실제 글자·그림의 묶음과 축소 시트를 함께 본다.

- 4:5 세로 카드에서 두 항목 비교는 좌우 두 단보다 **위아래 두 칸**이 높이를 채운다(프리셋 A `.split`).
- 짧은 목록은 고유 높이와 일정한 간격으로 묶고 `.z-main`에서 `justify-content:center`로 놓는다. `flex:1` + `space-evenly`로 항목 사이를 벌려 빈칸을 숨기지 않는다.
- 표지는 부제·약속·그림을 하나의 흐름으로 모은다. 그림을 오른쪽 아래로 밀어 가운데에 구멍을 만들지 않는다.
- `contentBalance`는 실제 텍스트·그림 경계로 위·아래 여백과 중심 편차를 기록한다. `content-balance`는 편차 10% 초과이면서 여백 차가 24px를 넘을 때의 권고이며 발행 차단이 아니다.
- 의도적인 위·아래 배치는 `.z-main`에 `data-content-align="top"` 또는 `"bottom"`을 쓰고 review.md에 이유를 적는다. 선언 없이 중앙이 맞았다고 보고하지 않는다.
- 프레임·제목·결론 위치는 유지하고 본문을 먼저 조정한다. 큰 여백이 의도적이면 남기되, 여백을 줄이려고 원문 내용을 추가하지 않는다.

## 10-0-1. 시각 중심 (data-focal)

표지·마지막 장을 뺀 본문 카드마다 시선이 먼저 가는 요소 하나에 `data-focal`을 단다. 큰 숫자(36px 이상), 핵심어, 큰 아이콘(`.focal-ico`, 108px) 중 하나다. `qa_render.py`가 없거나 작으면 카드별로, 본문 카드의 60% 미만이면 세트 권고로 알린다(`gates.json` `layout.focal`). 목록만 이어지는 세트가 양식집처럼 보이던 문제를 막는다.

- 문구를 새로 만들지 않는다. 이미 있는 숫자·핵심어를 크게 하거나 아이콘을 더한다.
- 같은 방식을 연달아 쓰지 않는다(큰 숫자 → 아이콘 → 핵심어처럼 바꿔 가며).
- 예시: `examples/free-design-realtor/`(2번 핵심어, 3번 단계 숫자, 4번 아이콘, 5번 대비 핵심어, 6번 큰 숫자, 7번 아이콘).

## 10-0-5. 시각 중심 부품 (프리셋 A, 2026-10-07)

카드마다 다른 시각 중심을 고르기 쉽게 프리셋 A에 부품을 더했다. 예시: `content/TEST-SUSPENSION-V3/`(기본 빌더와 비교 `out/ko/before-after.png`). 연속 두 장에 같은 부품을 쓰지 않는다.

| 부품 | 시각 중심 | 맞는 메시지 |
|---|---|---|
| `.cv-duo` | 표지 큰 숫자 두 칸 | 두 사건·두 기간의 결과 대비(라벨은 제목 낱말만) |
| `.krows` + `.krow.hot` | 핵심어 열, 한 줄 네이비 강조 | 확인 항목 3~4개 중 하나가 결정적일 때 |
| `.versus` + `.vs-wide` | 큰 단어 두 개 좌우 대조 | 헷갈리는 두 개념(과징금/과태료) |
| `.q-head` `.q-art` `.q-panel` | 물건 그림 + 인용 패널 | 재결·판례 사례 |
| `.q-hero` | 큰 숫자 하나 | 사례의 결과 기간·금액 |
| `.ico-rows` | 아이콘 배지 행 | 업종·대상별 차이 |
| `.xlist` + `.xitem.hot` | ✕ 목록 | 안 되는 경우·제외 사유 |
| `.bars2` + `.bar2-cut` | 막대 + 끊긴 선·도장(장식) | 감경·변경 같은 같은 단위 숫자 변화 |
| `.stat-rows` | 숫자 행 | 여러 사건 결과 요약 |
| `.bound.stack` + `.bound-h` | 두 상자 + 아이콘 머리줄 | 마지막 장 직접 준비 / 종합 검토 |

- 표지·도장 라벨처럼 숫자·제목 낱말을 다시 쓰는 장식은 `data-decor`를 달고 새 사실을 만들지 않는다.
- 크림 카드의 네이비 상자 안 글자도 QA가 크림 바탕으로 보므로 골드 글자 대신 흰 글자를 쓴다.

## 10-0-2. 대안 표지 (altCover)

card-data 표지에 `altCover`가 있으면 `content/<ID>/<lang>/alt/card_01.html`을 같은 프레임으로 하나 더 디자인한다(CSS 경로는 한 단계 더 위: `../../../../brand/…`, `../../design.css`). 숫자 대비형은 프리셋 A의 `.cv-stat`(큰 숫자 두 개 + 골드 화살표)을 쓴다. 렌더: `python scripts/qa_render.py --html-dir content/<ID>/ko/alt --source content/<ID>/blog.md --allow-partial --out content/<ID>/out/ko/alt`. 예시: `examples/free-design-realtor/ko/alt/`, 비교 이미지 `out/cover-ab.png`.

## 10-0-3. 생활 장면형 표지 (인물 일러스트)

조회가 높았던 글은 독자의 구체 상황을 바로 보여 줬다(글감관리표 마케팅 점검). 표지 Hook이 situation이면 둘 중 하나를 표지 시각 중심으로 크게 둔다.

- **인물**(`assets/illustrations/people/`): **크림 표지에서만**(예시 `drafts/E/`). 제목은 원문의 상황 문장을 그대로. 세트당 한 번.
- **물건**(`assets/illustrations/objects/`, `.obj-hero`): 네이비·크림 어디나(예시 `drafts/F/`, 도장). 처분은 도장·저울, 서류는 file-text, 기한은 calendar-x·hourglass, 비자는 identification-card·airplane-tilt, 가게는 storefront처럼 주제의 물건 하나.

- **손그림 선화**(`assets/illustrations/hand/`, IRA Design MIT, `.hand-hero`): 물건 13종(달력·지갑·카드·노트북·휴대폰 등)과 인물 6종. Phosphor보다 가늘고 손으로 그린 느낌이라 더 자연스럽다. 파란 배경에서는 골드 면이 있는 물건(달력·카드·지갑)이 잘 읽힌다(예시 `drafts/G/`, 달력 = 의견제출 기한). 인물은 크림 카드에서만.

## 10-0-4. 손으로 그은 강조 (Rough Notation, MIT)

제목이나 결론의 핵심 낱말 하나에 손으로 그은 듯한 골드 밑줄·동그라미를 단다. 기계적인 `mark-hl`보다 자연스럽다.

- 강조할 글자를 `<span data-annotate="underline">6개월</span>`로 감싼다(`underline`·`circle`·`box`·`bracket`). 문구는 바뀌지 않으므로 카피 잠금에 영향이 없다.
- 카드 `</body>` 앞에 `<script src="…/vendor/rough-notation/rough-notation.iife.js"></script>`와 `<script src="…/templates/annotate.js"></script>`를 넣는다(로컬 파일, 외부 호출 없음). 모양은 난수를 고정해 렌더마다 같다.
- 카드당 한 곳, 세트에서 두세 장까지. 형광펜(highlight)은 글자 대비를 해쳐 쓰지 않는다.

## 10-1. 아이콘 (Lucide, ISC)

글만 있는 카드에서 시선이 머물 자리가 없을 때 아이콘 하나로 시각 중심을 만든다. 목록은 `assets/icons/lucide/README.md`(기한·서류·체류·사업·돈·판단·강연 등 60여 개).

- 넣는 법: `python scripts/icon_svg.py calendar-clock` 출력(SVG)을 그대로 HTML에 붙인다. `data-icon` 값이 붙어 나오고, `copy_lint.py`가 이 값으로 `assets.md` 출처 기록을 확인한다.
- 크기·색은 `design.css`에서: 색은 `brand/tokens.css` 변수, 선은 `currentColor`. 프리셋 D의 `.ask.has-ico` + `.ico-badge`(원형 배지)를 그대로 써도 된다.
- 한 카드에 아이콘 묶음은 하나(항목별 아이콘 3~4개 또는 큰 아이콘 1개). 아이콘이 정보를 대신하지 않는다. 같은 아이콘을 세트 전체에 반복하지 않는다.
- 아이콘이 의미를 더하지 않으면 넣지 않는다. 큰 제목과 여백만으로 충분한 카드가 더 좋다.

## 11. 독립 평가

같은 대화에서 만들고 바로 채점하면 점수가 후해진다. 가능하면 평가는 다른 세션이나 다른 에이전트가 `docs/card-evaluation-rubric.md`의 흠 찾기 질문으로 한다. 같은 세션에서 할 때는 렌더 PNG를 처음 보는 사람처럼 한 장씩 다시 열어 질문에 답한다.
