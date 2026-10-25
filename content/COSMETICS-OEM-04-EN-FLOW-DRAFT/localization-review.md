# 영문 카드 의미·문체 검토

2026-10-25. 검토 대상: 이 폴더의 `card-data.en.json`, `card-data.ko.json`, `blog.md` 10장 전체. 기준: `docs/en-legal-glossary.md`와 copy-editing의 명료성·말투·구체성·근거·다음 행동. JSON·HTML·기존 원고는 수정하지 않았다. 실제 렌더 검토는 아직 하지 않았다.

영어 법률 용어는 편집용 번역이다. 공식 영문법령 번역 인증이나 이번 검토자의 신규 법령 조사·개별 계약 자문을 뜻하지 않는다. 아래 판정은 확인된 국문 원문과 영문 사이의 의미 대조다.

## 결론

핵심 법률 구분은 대체로 보존됐다. 동일 사업자 또는 적격 기관 등에 위탁한 경우라는 검사 예외, 제출 의무의 별도 예외, 세 조건의 AND, 비용 약정과 법정 의무, 무료 사전 검토와 유료 문서 작성은 구별돼 있다. 새로운 서비스·처리기간·성과·수치를 만들지 않았다.

다만 카드 5의 문서명, 6의 자료 전달·절차, 9의 검사 불일치 표현은 최종 반영 전에 아래처럼 명확히 할 것을 권한다. 카드 7·8의 제한된 범위와 가능 표현은 유지해야 한다.

## 우선 반영할 수정 제안

| 위치 | 현재 | 문제·수정 제안 |
|---|---|---|
| 5 body[1] | `required product standards and quality-control records` | 제품표준서가 기준 자체처럼 읽힌다. 문서라는 점을 명시: `Agree who provides and reviews the required product specification documents and quality-control records, and when.` 제품표준서는 편집용 `product specification document`로 세트 내 용어 기록에 고정하는 편이 낫다. |
| 6 body[1] | `you may agree on advance notice and records, followed by written confirmation ...` | 자료를 전달한 뒤라는 행동이 흐리다. `For changes that may affect quality, you may agree on advance notice and delivery of the relevant records, followed by written confirmation of the change and when it takes effect.` 약정 가능성 `may agree`를 유지한다. |
| 6 takeaway | `Align notice, approval and internal review roles.` | 원문의 통보·승인 **절차**가 모두 역할로 바뀌었다. `Align the notification and approval procedures with the internal reviewer’s role. Further testing depends on the change.` 또는 더 짧게 `Align notification and approval procedures and identify the internal reviewer. Further testing depends on the change.` |
| 9 note | `mismatched test results` | 카드 4의 제조번호 불일치와 혼동할 수 있다. 블로그의 기준과 다른 검사결과라는 맥락을 명확히 한다: `These are examples from the source article. If specifications change, test results differ from the agreed standards, or post-sale inquiries arise, check whom to consult and who handles the records.` |

## 선택적 문체 개선

- 1 body: `Korean domestic OEM`은 이해되지만 명사 나열처럼 들린다. `For OEM production in Korea, the brand receives and manages test results.`가 자연스럽다.
- 1 promise: `Quality checks before you sign`은 검사 자체로 좁혀 읽힐 수 있다. 원문의 품질관리에는 기록·감독도 포함되므로 `Quality control before you sign` 권장.
- 3 body[1]: `legally eligible facility`는 물리적 시험시설에만 초점을 준다. 기관·제조업자 등이라는 범위를 포괄하는 `legally eligible testing provider`가 편집용 표현으로 더 낫다. 예: `For separate businesses, testing must be entrusted to a legally eligible testing provider, with results available for each batch.` 여기서 must는 별도 검사를 생략하려는 경우의 조건이다. 제목과 `Or outsourced testing` 라벨을 함께 유지한다.
- 8 takeaway: 현재도 필요조건은 전달되지만 `may`를 직접 쓰면 국문 가능 표현이 더 선명하다. `Submission may be omitted only where all three apply, and only within that scope. A trade-secret claim is no blanket exemption.`
- 10 body[0]: `test-report delivery guidance`보다 `information on how test reports will be provided`가 자연스럽다. 공간이 부족하면 현행도 의미상 허용 가능하다. 문서가 없는 사람에게 새로 만들어 보내라고 요구하는 뜻이 되지 않게 `you already have`를 유지한다.
- 10 body[1]: `quality rules`를 앞선 `quality-control rules`와 통일한다. `Ethos Administrative Attorney Office`는 고정 표현대로 정확하다.

## 10장 의미 대조

| 카드 | 확인한 의미 | 판정 |
|---|---|---|
| 1 | 국내 OEM 범위, 공장 검사 뒤 브랜드의 검사결과 수령·관리 | 보존. 문체·promise 범위 명료화 권장 |
| 2 | 제조업체 시험·제조/품질 기록 작성 보관; 책임판매업자의 수탁자 감독·배치별 결과 수령 관리; 비용 분담으로 법정 의무 이전 불가 | 보존. `responsible distributor`는 이 글의 브랜드 역할을 가리키며 모든 브랜드가 법적으로 같은 지위라는 일반화는 피함 |
| 3 | 동일 사업자 **또는** 별개 사업자의 법정 적격 위탁+각 배치 결과; 별도 검사 생략 가능; 감독·기록·최종 품질 의무 잔존 | OR/AND 및 가능성 보존. `facility`보다 `testing provider` 권장 |
| 4 | 제품명만이 아니라 납품 배치번호 확인; 그 배치 결과 대조; 제품명만 있으면 배치 기록 요청 | 보존. 표제는 메일/상자 장면을 압축했지만 핵심 행동은 본문에 남음 |
| 5 | 검사 주체·배치 결과 확인; 문서의 제공·검토 주체와 시점; 회사 규정에 따른 보관; 수령과 적합성 판단 구별 | 의미 보존. 제품표준서가 **문서**임을 명시할 필요 |
| 6 | 승인 샘플·사양·용기·포장·시험기준 문서화; 품질 영향 가능 변경의 사전 통보→자료 전달→서면 확인을 약정할 수 있음; 추가 시험은 내용에 따라 판단 | 약정 가능성 보존. 전달 행동과 통보/승인 절차를 명확히 수정 권장 |
| 7 | 제조업자의 필요한 품질정보 제출; 동일 사업자 예외; 별개 사업자 설계/개발/생산+품질/안전관리 영향 없음+양측 계약상 영업비밀 모두; 법정 범위에서 생략 가능 | 보존. `all three`, `and`, `may`, `only within` 유지. 8번을 보지 않아도 조건이 남음 |
| 8 | 영업비밀 예외의 세 조건 모두, 품질·안전관리 영향 없는 범위, 상호 계약, 일괄 제외 금지 | 보존. takeaway에 `may`를 직접 유지하면 더 명료 |
| 9 | 문서 3개의 예시 인용 의미; 변경/검사 불일치/판매 후 문의의 협의·자료 담당자; 문서 간 담당·전달 시점 연결 | 인용 의미 보존. 실제 고객 문서나 법정 서식으로 바꾸지 않음. `mismatched`는 기준 불일치로 명확화 권장 |
| 10 | 보유 자료로 무료 사전 검토; 검사 담당·배치 결과 전달·문서 담당·추가 합의 검토; 계약/문서 작성은 별도 범위·비용의 유료 서비스 | 보존. 시험 수행·기술적 적합성 보증·분쟁 대리를 암시하지 않음 |

## 용어·강도 확인

- 제조번호: `batch number`, 제조번호별 결과: `results for each batch`. 카드 4에서 batch number를 명시해 다른 카드의 batch 표현과 연결된다.
- 책임판매업자: `responsible distributor`, 책임판매관리자: `responsible sales manager`. 사업자와 담당자를 서로 바꾸지 않았다. 두 표현은 국문 원문상의 서로 다른 지위이며 공식 번역 인증은 아니다. 용어 기록에 구분을 남기고 임의로 모두 distributor 또는 manager로 통일하지 않는다.
- 관리·감독: `oversees`/`oversight`; 제조·품질관리 기록: `manufacturing and quality-control records`. 기술적 검사 보증으로 확대되지 않았다.
- 자료 제출 생략: `submission may be omitted`; 별도 검사 생략: `skip a separate test`. 서로 다른 예외가 구분된다.
- `must design, develop and produce`는 예외를 적용하기 위한 조건을 뜻한다. 모든 제조업자가 언제나 세 업무를 해야 한다는 일반 의무로 떼어 쓰지 않는다.
- `Administrative Attorney Office`는 필수 고정 표현 준수. lawyer/attorney-at-law·court representation으로 확대하지 않았다.

위 내용은 최초 JSON 검토 기록이다. 아래 최종 재검토에서 반영 상태와 실제 화면을 구분한다.

## 수정 후 의미·문체 재검토

2026-10-25, 영문 JSON 전체 재독 및 국문 기준 대조. 5번 `product specification documents`, 6번 `delivery of relevant records`와 notification/approval procedures, 9번 `results that differ from agreed standards` 반영을 확인했다. 1번 국내 OEM 설명·품질관리 표현, 3번 eligible testing provider, 8번 may와 only within, 10번 quality-control rules 통일도 반영됐다.

7번은 `Manufacturer’s duty` 라벨 아래 명령문으로 제출 의무의 주체를 명시한다. `Separate businesses: all three` 아래 제조업자의 설계·개발·생산, 품질/안전관리 영향 없음, 상호 계약상 영업비밀이라는 세 문장을 배치했다. 이 문장들은 해당 예외의 조건으로 읽히며 모든 제조업자에게 일반적으로 적용되는 새 의무를 만들지 않는다. 동일 사업자 예외와 `Submission may be omitted only within the statutory exception’s scope` 결론도 유지됐다. 단독 발췌 시 조건 라벨·결론을 제거하지 않는다.

9번 `Illustrative wording`은 예시라는 의미를 보존한다. ‘원문에서 가져온’이라는 내부 출처 설명은 생략됐으나 실제 고객 문서로 표시하지 않았고 세 인용의 의미도 그대로다. 10번 `test-report delivery guidance`는 다소 압축된 표현이나 제출할 수 있는 보유 자료를 뜻하므로 현재 의미상 허용한다.

**내부 의미·현지화 검토 판정: 통과.** 새 사실·서비스·법률 조건 삭제는 확인하지 못했다. 공식 번역 인증·사용자 채택·발행 승인은 아니다. 국문 blog.md 및 JSON은 수정하지 않았다.

## 실제 렌더 확인과 남은 한계

`out/en/png/card_01.png`부터 `card_10.png`까지 개별 PNG 10개와 `out/en/sheet-270.png`를 실제 열었다. QA 보고서의 10/10 PASS를 확인했으며 영문 문서·상자·이모지·제목·본문 구분이 보인다. 7번은 장식을 덜고 폭을 확보했고 9번은 문서 3개와 설명을 분리했다. 시각 확인을 자동 QA 통과로 대신하지 않았다.

- 7번은 449자/72단어, 본문 채움 1.0으로 밀도가 높다. 첫 라벨과 제목 사이, 마지막 조건과 결론 사이 간격도 좁다. 누락이나 잘림은 보이지 않지만 빠르게 훑기보다 집중해서 읽어야 하는 카드다. 범위·세 조건을 다음 장에만 숨기거나 글자를 더 줄여 해결하지 않는다.
- 6·8·9·10번에도 분량 권고 경고가 남는다. 특히 9번의 문서 인용은 좁은 열에서 여러 줄이고 설명도 5줄이므로 실제 휴대전화에서 읽기 확인이 필요하다.
- 첫 시각 확인 당시 8번 결론 `apply`와 9번 결론 `timing`에 자동 하이픈으로 단어가 갈라지는 모습이 있었다. 주 담당자에게 영문 자동 하이픈 해제·단어 단위 줄바꿈 및 최종 시트 재생성을 요청했다. 이 항목의 해결 여부는 후속 렌더 확인 기록으로 판정한다.
- 표지 하단 여백은 문구·그림을 한 묶음으로 읽게 하는 구성이라 그 자체를 실패로 보지 않는다. `concept` 3장 연속 경고도 실제 7·8·9번 배치가 서로 달라 기계적으로 감점하지 않는다.

문체는 국문의 기계적 직역보다 자연스럽고 필요한 행동이 분명하다. 다만 법률 정보 밀도가 사라진 것은 아니며 실제 독자 이해도·저장률·문의 전환은 측정하지 않았다. 사용자 결과 확인 전 커밋·푸시·발행을 승인한 것으로 취급하지 않는다.


## 담당 에이전트 후속 조치 확인
주 에이전트가 영문 전체 hyphens:none을 적용하고 최종 PNG를 재확인했다. 9번 timing 분할 제거. 7번 제목을 Sharing quality records로 압축해 제목과 본문 사이 공간을 확보했다. 최종 QA 기준 7번 439자/69단어, 본문 채움 0.90. 본문 법률 조건은 그대로이며 고밀도 권고는 남는다. 내부 검수 완료이며 사용자 승인 대기.
