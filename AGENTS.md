# ETHOS 카드뉴스 작업 규칙 (Codex용)

목표: 승인된 블로그 원문 1편 → 카드 6~10장 (정사각 540×540 CSS, PNG 1080×1080).
작업 폴더: `content/<CONTENT_ID>/` (예: `content/GAME-KR-06/`). 이 폴더 밖의 킷 파일은 수정하지 않는다.
카드는 원문의 요약본이 아니라, 원문의 **핵심 판단 구조 하나**를 빨리 이해시키는 시각 콘텐츠다.

## 작업 순서 (건너뛰기 금지)
1. `content/<ID>/blog.md` 를 읽는다. 없으면 만들지 말고 사용자에게 요청한다. (`content/_TEMPLATE/` 를 복사해 폴더를 만든다.)
2. `content/<ID>/brief.md` 작성 (`docs/brief-template.md` 양식): **각도 1개**, 뺄 섹션 목록, Hook 후보 3개, 카드별 한 메시지.
3. `content/<ID>/card-data.json` 작성 (`schema/card-data.schema.json` 준수): 카피 + 카드별 Source Trace.
4. ⛔ **여기서 멈추고 사용자 승인을 받는다.** 승인 전 HTML 작성·렌더 금지. (커밋·PR 은 brief 단계까지만)
5. 승인 후 `content/<ID>/card_NN.html` 생성 (`docs/html-contract.md`, `templates/` 사용).
6. `python scripts/qa_render.py --html-dir content/<ID> --source content/<ID>/blog.md --out content/<ID>/out` 실행.
7. 실패하면 **카드(카피·레이아웃)를 고친다.** `gates.json`, `brand/`, `fonts/` 는 수정 금지.
8. 통과하면 `content/<ID>/out/` (png, sheet-270.png, qa-report.md)를 커밋하고, 사람이 확인할 항목을 PR 설명에 적는다.

## 절대 규칙 (자동 검사 + 사람 확인)
- 원문에 없는 사실·숫자·조문·판례·사례를 넣지 않는다. 숫자·조문은 원문 표기 그대로.
- 원문의 「또는/그리고/~할 수 있다/~해야 할 수 있다」를 단정·기호(+ = ≠)로 바꾸지 않는다. 뜻이 넓어지거나 좁아지면 압축 실패.
- 카드 한 장 = 한 메시지. 결론이 둘이면 카드를 나눈다.
- 글자 크기: 본문 16px↑, 라벨·주석 14px↑, 프레임 12px↑. 위계는 **크기·굵기**로 만들고 색을 흐리게 하지 않는다.
- 블로그 전체를 카드에 압축하지 않는다. 뺀 내용은 `brief.md` 의 OMITTED 에 적는다.
- 폰트는 `fonts/` 파일만 사용. 로드 실패 시 중단(시스템 폰트로 계속하지 않는다). 외부 네트워크 호출 금지.
- 색은 `brand/tokens.css` 변수만. 임의 HEX 금지. 그라데이션·이모지·이미지 생성 텍스트 금지.
- 카드에 연락처·URL·버튼 금지. 마지막 장은 **무료 검토 안내 한 문장**(`docs/editorial.md` §5).
- 이력 소개 문장, About me 카드, "최고/대표/leading" 금지.
- 헤더·푸터·골드바는 `templates/base.css` 프레임 그대로. 카드마다 다시 만들지 않는다.

## 파일 지도
| 경로 | 역할 | 수정 |
|---|---|---|
| `docs/editorial.md` | 카피·Hook·서사·CTA 규칙 | 사람만 |
| `docs/html-contract.md` | 카드 HTML 계약 (data-속성) | 사람만 |
| `brand/tokens.json·css`, `brand/fonts.css`, `fonts/` | 브랜드 값·폰트 | 사람만 |
| `gates.json`, `scripts/qa_render.py` | 검사 기준·실행기 | 사람만 |
| `templates/` | 프레임·카드 유형 CSS·스켈레톤 | 새 유형은 `card-types.css` 에만 추가 |
| `examples/` | 통과하는 예시(good)와 실패하는 예시(bad) | 참고용 |
| `content/<ID>/` (blog.md, brief.md, card-data.json, card_NN.html, out/) | 작업물 | 에이전트 |
| `content/_TEMPLATE/` | 새 작업 폴더 양식 | 복사해서 사용 |

## 완료 정의
qa-report 가 PASS 이고, `humanChecks` 목록을 사용자에게 그대로 전달했을 때. 법령 해석의 정확성은 에이전트가 보증하지 않는다.
