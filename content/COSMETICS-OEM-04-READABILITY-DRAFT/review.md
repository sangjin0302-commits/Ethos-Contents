# OEM readability comparison — 2026-10-21

미승인 비교 초안. 기존 `COSMETICS-OEM-04`의 파일 55개 SHA-256 일치. 승인 원고를 대체하거나 발행하지 않았다. 원본 메타데이터의 승인 상태도 그대로 보존했다.

## 실제 변경

- 블로그 20곳 부분 편집. 명사 중심 설명과 막연한 연결을 주체·행동·다음 질문으로 풀었다. 법률 검토 후 설치된 humanize-korean 규칙을 직접 적용하고 다시 의미를 대조했다. 원본의 숫자·조문·인용 목록과 CTA부터 태그 끝까지 동일하다.
- 기존 3번을 새 3·4번으로 분리: 검사 생략의 두 경로와 위탁 후 남는 의무. 생략 카드 자체에도 잔존 의무를 남겼다.
- 기존 7번을 새 7·8번으로 분리: 제출 의무/동일사업자 예외와 영업비밀의 누적 조건. ‘품질·안전 영향 여부’를 ‘영향 없는 범위’로 명확히 했다.
- 기존 4·5번 자료 흐름을 새 5번으로 통합. 기존 쉼 카드의 법정 의무 불변은 2번 결론으로 이동. 전체 10장 유지.
- 국문 본문 23px를 기본으로 두고 제출 원칙은 25px. 영문 21px, 제출 원칙 23px. 자동 글자 축소 없음. 전용 행·두 갈래·누적 조건 묶음으로 구성했다.

## 비교 수치와 한계

같은 로컬 Chromium에서 기존/새 국영 40장을 540×675 CSS px, 1080×1350 PNG로 렌더했다. 40장 모두 하드 QA 통과. 새 초안 20장의 fitScale은 1.00이다. 실제 시트와 두 분할 비교 이미지는 주 담당자 및 별도 카드 에이전트가 확인했다.

| 측정 | 기존 | 새 초안 | 해석 |
|---|---:|---:|---|
| 블로그 공백 포함 문자 수, LF | 10,241 | 10,399 | +158자; 일괄 축약하지 않음 |
| 블로그 문자 변경률 | — | 3.76% | SequenceMatcher, autojunk=False; 품질 점수 아님 |
| 국문 카드 수 | 10 | 10 | 분할과 반복 통합 병행 |
| 국문 한 장 최대 JSON 카피 문자 수 | 234 | 192 | 17.9% 감소 |
| 영문 한 장 최대 JSON 카피 문자 수 | 458 | 410 | 10.5% 감소 |
| 국문 전체 JSON 카피 문자 수 | 1,462 | 1,551 | 6.1% 증가; 조건 설명 명시 |
| 영문 전체 JSON 카피 문자 수 | 3,181 | 3,372 | 6.0% 증가 |
| 국문 법률 본문 실제 글자 크기 | 22px | 23~25px | +4.5~13.6% |
| 영문 법률 본문 실제 글자 크기 | 21px | 21~23px | 유지~+9.5% |

JSON 문량은 headline/body/takeaway/promise 등 공개 카피 필드의 공백 포함 문자 수이며 필드 사이 연결 문자는 제외했다. 렌더 QA의 공백 제외 글자 수와 혼용하지 않는다. `comparison-metrics.json`과 `comparison/render-comparison.json`이 측정 근거다. 자연스러움·독자 이해도·전환율 개선 비율은 측정하지 않았다.

## 법률 조건과 범위

법률 에이전트가 2026-10-21 현행 1차 법령을 확인하고 블로그 L01~L15를 원문과 독립 대조했다. 국영 카드도 해당 주제 범위에서 의미 재검증 통과. `../../docs/reviews/2026-10-21-oem-legal-audit.md` 참조.

- 검사: 동일사업자 OR (법정 기관 등에 위탁 AND 제조번호별 결과). 별도 검사를 하지 않을 수 있다는 재량과 잔존 의무 보존.
- 자료: 동일사업자 OR (제조업자 설계·개발·생산 AND 품질·안전 영향 없는 범위 AND 상호 계약상 영업비밀). 모든 조건, 범위 한정과 제출하지 않을 수 있다는 표현 보존.
- 변경 약정과 법정 의무, 무료 사전 검토와 유료 작성 구분 보존.
- CGMP, 판매 후 법정 보고 상세 등은 블로그에 보존하며 기존 카드와 같이 카드 범위 밖이다. 블로그의 모든 법률 설명을 카드에 옮겼다고 주장하지 않는다.
- `condition-map.json` 15개 추적 항목은 L01~L15와 별개인 카드 근거 매핑이다. 정확 구절 존재 검사는 의미 검증의 대체가 아니다.

## 렌더·문체 권고 처리

- 표지 본문 블록 4개와 국문 하단 53px 여백: 제품 그림·질문·직접 답·읽을 이유를 분리한 의도적 구성. 빈 공간을 장식으로 채우지 않았다.
- 국문 2번 두 열의 5행 문단: 주체 비교 목적, 낱말 분절·가림 없음. 영문은 세로로 바꿔 좁은 열의 긴 문단을 줄였다.
- 영문 6·8·9번 문량 권고 초과: 실제 넘침 없음. 계약상 재량, 누적 조건·범위, 담당자 항목을 지우지 않았다. 모바일 축소 보기에서도 내용을 따라갈 수 있으나 영문 8번은 여전히 설명량이 많다.
- process 유형 권고: 이번 내용은 필수 순서가 아니므로 번호나 절차 유형을 억지로 추가하지 않았다.
- memo-style, 법률상 ‘범위에서’, 의무형 종결 반복: 법정 누적조건·확정적 의무·재량 표현 보존. 정보성 비율을 맞추는 재작성은 하지 않았다.
- 블로그 ‘주문수량’ 띄어쓰기 후보: 의미 오류 아님. 이번 부분윤문 범위 밖의 기존 표기를 유지했다.
- 디자인 린터의 layout-repeat 7건: 공통 첫 클래스 `editorial`을 같은 부품으로 집계한다. 실제로는 주체 두 열, 예외 두 갈래, 의무 행, 자료 체크, 변경 대조, 누적 조건 묶음이 다르다. 실제 이미지 확인 결과 수정이 필요한 반복 결함으로 판단하지 않았다.

전체 회귀 테스트 209개 통과(기존 의존성 deprecation 경고 4개). CI와 동일한 `ci_render.py --ids COSMETICS-OEM-04-READABILITY-DRAFT`도 국영 카드 및 대표 이미지 검사 통과. 자동 통과만으로 디자인·법률 품질이나 발행 승인을 주장하지 않는다.

원격 CI 후속 수정: 최종 메타데이터의 `languageMethod`를 스키마의 `humanize-korean`/`english-localization` 값으로 맞추고, 사용하지 않는 1개짜리 `art` 배열을 제거했다. 공개 문구·렌더에는 변화가 없다. 추가한 비교 도구 테스트 8개는 원격의 표준 `unittest`로 바꿔 pytest 설치 없이도 실행하도록 했다. 수정한 JSON의 스키마 검증과 국영 CI 렌더 재실행이 통과했다. 링크 검사의 별도 실패는 기존 OASIS 주소 2곳의 외부 TLS 인증서 만료이며 해당 출처나 검증 보안 설정을 바꾸지 않았다.

CI 호환 수정 후 `unittest discover` 전체 208개도 로컬에서 통과했다(건너뜀 없음). 앞의 209개는 pytest 수집 기준이며 unittest 수집 수와 구분한다.

## 재현

저장소 루트에서:

```sh
python content/COSMETICS-OEM-04-READABILITY-DRAFT/build_preview.py
python scripts/editorial_compare.py --baseline content/COSMETICS-OEM-04 --draft content/COSMETICS-OEM-04-READABILITY-DRAFT
python scripts/qa_render.py --html-dir content/COSMETICS-OEM-04/ko --source content/COSMETICS-OEM-04/blog.md --out _verification/oem-before/ko
python scripts/qa_render.py --html-dir content/COSMETICS-OEM-04/en --source content/COSMETICS-OEM-04/blog.md --out _verification/oem-before/en
python scripts/qa_render.py --html-dir content/COSMETICS-OEM-04-READABILITY-DRAFT/ko --source content/COSMETICS-OEM-04/blog.md --out content/COSMETICS-OEM-04-READABILITY-DRAFT/out/ko
python scripts/qa_render.py --html-dir content/COSMETICS-OEM-04-READABILITY-DRAFT/en --source content/COSMETICS-OEM-04/blog.md --out content/COSMETICS-OEM-04-READABILITY-DRAFT/out/en
python content/COSMETICS-OEM-04-READABILITY-DRAFT/build_comparison.py
```

향후 별도 초안에서는 수정 전 `editorial_compare.py --initialize`로 원본 해시를 한 번 기록한다. 기존 스냅샷을 갱신해 변경을 숨기지 않는다. 법률·윤문·카드 담당을 나눌 수 있으나 최종 통합자가 실제 문구와 렌더를 함께 확인한다. 검수 통과와 사용자 승인·발행을 분리한다.
