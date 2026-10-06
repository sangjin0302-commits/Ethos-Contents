# 에토스 콘텐츠 전략 플레이북 (한 장)

소재를 고르거나 분기 계획을 세울 때 이 문서로 "누구에게, 어느 단계에서, 무엇을 주고, 무엇을 측정하는지"를 한 번에 맞춘다. 원칙은 `docs/brand-philosophy.md`, 포지셔닝 세부는 `.agents/product-marketing.md`, 소재 발굴은 `docs/topic-discovery.md`가 정본이다.

## 1. 독자 × 채널 맞추기

같은 소재라도 독자가 읽는 곳에 놓아야 전환이 일어난다.

| 독자 | 주로 읽는 곳 | 주 채널 | 보조 |
|---|---|---|---|
| 국내 사업자(처분·인허가 당사자, 대표) | 네이버 검색, 네이버 AI 답변 | 국문 블로그 | 국문 카드(인스타그램·카카오) |
| 외국인 고용기업 담당자 | 네이버·구글 검색 | 국문 블로그 + 홈페이지 | LinkedIn 국문 |
| 한국 진입 해외기업·외국인 창업자 | 구글 검색, LinkedIn | 홈페이지 영문 글 + LinkedIn 영문 | 영문 카드(LinkedIn 문서형 캐러셀) |
| 중동·아랍권 | LinkedIn 아랍어 | `guidelines/modules/middle-east-arabic.md` | — |

- 영문 카드는 인스타그램보다 **LinkedIn 문서형 캐러셀**을 기본 배포처로 삼는다. 영문 카드를 만들 때 `brief.md`에 영문 독자와 배포 채널을 적는다. 적을 수 없으면 영문 세트를 만들지 않는 것도 선택지다(`docs/card-selection.md`).
- 해외 독자를 위한 소재(예: 해외 게임의 한국 출시)는 영문을 원본처럼 설계하고, 국문은 국내 협력사(퍼블리셔·대리인) 관점으로 각도를 바꾼다.

## 2. 여정 단계 × 콘텐츠 역할

| 단계 | 독자의 질문 | 콘텐츠 역할 | 형식 | 다음 행동 |
|---|---|---|---|---|
| 발견 | "이게 나한테 해당되나?" | 상황 하나 + 직접 답 | 카드 표지·SNS 한 줄·블로그 첫 화면 | 저장·프로필 확인 |
| 이해 | "무엇부터 확인하지?" | 확인 순서·구분 기준 | 블로그 본문·카드 2~6장 | 관련 글·시리즈 다음 편 |
| 신뢰 | "이 사람은 어떻게 판단하지?" | 판단 과정 공개(Proof of Work) | 판례·재결례 해설, 서류 대조 예시 | 받을 자료 |
| 결정 | "내 경우는?" | 직접 확인 범위 vs 검토 경계 | 글 후반·마지막 카드 | 무료 검토 |

한 글·한 세트는 주 단계 하나를 맡는다. 시리즈(예: 「사업이 멈추는 행정처분」 12편)는 단계를 나눠 맡을 수 있는 가장 좋은 구조다. 시리즈 1편은 발견, 중간 편은 이해·신뢰, 마지막 편은 결정에 무게를 둔다.

## 3. 받을 자료 (Proof of Work를 손에 쥐여 주기)

무료 검토 CTA 앞에 독자가 먼저 가져갈 수 있는 자료를 둔다. 양식은 `content/_TEMPLATE/lead-magnet-checklist.md`, `lead-magnet-process-map.md`.

- 내용은 그 주제의 승인된 원문에서만 채운다. 원문에 없는 항목을 만들지 않는다.
- 자료는 "독자가 혼자 할 수 있는 범위"까지 완결돼야 한다. 핵심을 빼고 연락을 유도하지 않는다.
- 자료 끝에는 원문과 같은 무료 검토 안내 한 문장만 둔다. 연락처·접수 경로는 웹사이트 운영정책을 따른다.

## 3-1. 성과 자료

분기 운영의 전체 추세와 주제·시리즈 판단은 글감관리표(에토스_글감관리표.xlsx) 주간 성과 탭으로 보충한다. 계산 지표는 `docs/topic-log-integration.md` "마케팅 점검". 세트별 유지·변경·보류 결정은 여전히 각 세트의 `performance-log.csv`와 Primary Objective로 한다(`docs/performance-learning.md`).

## 4. 분기 운영

1. **분기 시작**: 글감관리표로 시리즈 1~2개를 정한다. 시리즈마다 주 독자, 주 채널, 받을 자료 하나를 정한다.
2. **매 편**: `brief.md`에 여정 단계와 Primary Objective를 하나 적는다.
3. **세트 3개마다**: `docs/performance-learning.md`의 결정 규칙(유지·변경·보류)을 적용한다.
4. **분기 말**: 무료 검토 요청이 어느 글·카드에서 왔는지(유입 출처) 집계하고, 다음 분기 시리즈를 고른다. 유입 출처를 모르면 결정할 수 없으므로 5절을 먼저 갖춘다.

## 5. 유입 출처 기록

- 모든 `distribution.md`에 게시 링크와 추적 이름(`content_id-채널-언어`, 예: `SUSPENSION-SURCHARGE-04-instagram-ko`)을 적는다.
- 상담 접수 링크는 `python scripts/tracking_link.py <ID> --channel … --lang …`으로 만든다. 스크립트를 못 쓰면 이 형식으로 직접 쓴다: `https://ethosattorney.com/intake?source=ethos-contents&channel=<instagram|linkedin|naver_blog|kakao|threads|lecture|email>&content_id=<ID>&placement=<위치>-<ko|en>`(위치 기본값: instagram·threads `bio`, linkedin `comment`, naver_blog `profile`, kakao `message`, lecture `qr`, email `signature`). 웹사이트 `/intake`가 `source=ethos-contents`, `channel`, `content_id`, `placement`(위치-언어)를 문의와 함께 저장하고, 관리자 `/admin/funnel`이 채널·글·위치별 문의·상담·수임을 집계한다(웹사이트 저장소 `docs/contracts/public-intake-source-tracking.md`, 2026-10-06 확인). 값이 없어도 접수는 막히지 않는다.
- 링크는 카드·본문에 넣지 않는다. 인스타그램 프로필·스토리 링크 스티커, LinkedIn 첫 댓글, 강연 QR처럼 본문 밖에 둔다. 웹사이트 글의 상담 버튼은 이미 `channel=blog`, `content_id=<slug>`를 보낸다.
- 분기 말 집계는 `/admin/funnel`의 content_id별 문의를 글감관리표 "유입글"보다 우선한다. 추적 링크 없이 온 문의만 접수 때 물어 시트에 적는다.

## 6. 웹사이트 저장소에 요청할 항목 (이 저장소에서 고치지 않는다)

- 접수 폼에 "어떤 글·카드를 보고 오셨나요?" 선택 항목
- `FAQPage` 구조화 데이터 검토, 깨진 글 슬러그 정리, 글마다 같은 저자 표기
- 받을 자료(체크리스트·절차 맵) 게시 위치

## 7. 점검 질문 (분기 계획을 확정하기 전)

- [ ] 각 시리즈의 주 독자가 실제로 읽는 채널에 원본을 놓았는가
- [ ] 시리즈 안에서 발견 → 이해 → 신뢰 → 결정 순서가 보이는가
- [ ] 받을 자료가 CTA 없이도 쓸모 있는가
- [ ] 유입 출처를 집계할 방법이 있는가
- [ ] 영문 세트는 독자와 배포처가 정해져 있는가
