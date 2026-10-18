# COSMETICS-OEM-04 디자인 검수 — 2026-10-18

## Editorial hierarchy revision — four remaining design issues

- All card-data and blog wording remain unchanged. English card 7 adds semantic spans only: the design/development/production model, quality/safety impact and contractual trade-secret scope are individually grouped, with the conjunction and punctuation intact. Copy lock remains mandatory.
- Covers: removed decorative underlines, path-tab rules, promise-chip border and heavy takeaway panel. Product artwork and question dominate; all supporting copy remains visible.
- Card 2: parallel responsibility columns replace stacked boxes. English paragraphs run 5–6 lines at 19px; this is a disclosed line-count advisory, not a reason to shrink type. Both columns retain their complete duties.
- Card 6: an open before/after timeline replaces duplicate rounded panels. Card 3 keeps its conditional panels, so adjacent concepts no longer repeat the same visual structure.
- English card 7: single-line 30px headline releases room for three visible exception factors; 21px body retained without shrinking. Density advisory remains.
- CTA: both preparation and review sections use the cream page, navy text and a quiet separator. Only the final free-review sentence has a navy filled panel. No new service, promise, button or contact information.
- Actual PNGs checked: both language sheets, English 1/2/6/7/10 and Korean 2/10 at full size. Visual hierarchy is clearer; this is not a claim of perfection or an externally validated score. Publication approval remains separate.
- Validation for this revision: 185 tests pass (four dependency deprecation warnings); copy lint has zero warnings and 11 information items; bilingual and distribution checks pass; five shared visual baselines have zero pixel changes. All 20 cards render with fitScale=1.00 and fitOverflow=0. Remote CI is verified after push, separately from this local record.

## Latest revision — footer, cover and English card 7

This section supersedes the earlier cover and card-7 observations below. The earlier review missed a footer defect; automatic QA was not evidence of visual completion.

- Footer: the number has an 8 CSS-pixel gap above a real 4px track. Filled and unfilled sections now share the same baseline. Browser tests inspect pseudo-element geometry for all 20 cards, including 01 and 10.
- Cover: original pump bottle and cream jar connected to a record replace the generic clipboard badge. Both covers retain the approved copy and brand palette.
- English card 7: headline shortened; plain-language verbs; body increased from 19px to 21px. QA counts 400 characters / 66 words versus 444 / 67 previously. Manufacturing and quality records, the design/development/production model, quality and safety impact, contractual trade-secret scope and the non-blanket confidentiality boundary remain. No external legal verification or new factual claim was added in this revision.
- Both language renders pass. Card 7 still carries a density advisory: it is a legal explanation, not a low-text promotional card. The advisory thresholds were not relaxed.
- Revised English wording uses the copy-editing clarity pass; Korean published copy is unchanged. Publication approval remains pending.
- Final local checks: all 20 cards have fitScale=1.00 and fitOverflow=0; 22 stress cases pass; visual regression passes with unchanged tolerances. Five footer baselines were visually checked and refreshed. Bilingual structure/source trace and guideline routes pass. Remote CI is checked separately after push.
- Full test suite: 184 passed, four dependency deprecation warnings, no failures or skips. Copy lint: zero warnings / 11 advisory information items. Distribution and asset provenance validation pass.

국문·영문 각 10장 구현, 실제 PNG 출력, 개별 이미지와 축소 시트 검수 완료. 아랍어는 제외. 사용자 발행 승인은 별도다. 이전의 실제 PNG 확인 없이 제시한 75점·90점대 평가는 폐기한다.

## 결과

- `out/ko/png/`, `out/en/png/`: 1080×1350 PNG 20장.
- `out/ko/sheet-270.png`, `out/en/sheet-270.png`: 전체 미리보기.
- 양쪽 qa-report.json: allPass=true, pngWritten=true. 20장 모두 fitScale=1.00, fitOverflow=0. 자동 축소 없이 출력.
- 한·영 구조·출처 추적, 카피(WARN 0 / INFO 12), 배포 자료, 구조 디자인, 카드 스모크 검사 통과.
- 기존 실패 3건 수정. 전체 테스트 최종 결과는 아래 후속 검증 기록 참조. 로컬 검사와 원격 CI 결과는 구분한다.

## 카드별 구현·시각 확인

| 카드 | 결과 |
|---|---|
| 1 | 문서 아이콘·질문·검사/제조번호/기록 관리의 위계 정리. 큰 원형 장식을 줄임. 표지와 9장의 네 항목 수 일치. 영문 different 분철 제거. |
| 2 | 제조업체와 브랜드 회사의 책임을 위아래 독립 패널로 구분. 아이콘과 본문 간격 확인. |
| 3 | 좁은 비교 열 대신 예외와 남는 의무를 세로로 분리. 국문 제목 ‘별도 검사를 생략할 수 있는 경우가 있습니다’로 조건 보존. |
| 4 | 번호가 질문 위에 놓이던 결함 수정. 왼쪽 고정 번호와 세로 질문 패널. 영문 축소 제거. |
| 5 | 네 단계 세로 타임라인. 영문 길이에 맞춰 패널 여백 조정, 글자 축소 없음. |
| 6 | 변경 전후 패널과 문서·갱신 아이콘. 통보·확인 업무가 분리되어 읽힘. |
| 7 | 인용처럼 보이던 형식을 의무·예외·경계의 세 패널로 변경. 전문 조건은 삭제하지 않음. 가장 조밀한 장. |
| 8 | 큰 문장과 법정 의무 강조, 의도적 여백. 정보량 높은 전후 카드 사이의 쉼 역할. |
| 9 | 네 항목에 원형 번호와 구분선. 영문 outsourced의 임의 분철 제거. |
| 10 | 직접 준비 / 우선 검토를 밝은 패널과 네이비 패널로 분리. 마지막 무료 검토 안내를 독립 배치. |

## 기존 기준에 따른 자기 평가

`docs/card-evaluation-rubric.md` 적용. 4는 발행 가능한 디자인 수준이며 사용자 승인·법률 검증·성과 보장을 뜻하지 않는다.

### SET: COSMETICS-OEM-04 (ko)

- C1 표지와 카피: 4/5 — 공장 품질검사 질문과 화장품 시리즈명이 대상·문제를 드러냄. 전문 용어는 원문 의미를 위해 유지.
- C2 가독성과 일관성: 4/5 — 제목·본문 위계, 네이비·크림·골드, 정렬 일치. 전 장 잘림·자동 축소 없음. 7장은 상대적으로 조밀함.
- C3 흐름: 4/5 — 책임 → 예외 → 질문 → 문서 전달 → 변경·영업비밀 → 핵심 구분 → 준비·검토로 연결.
- C4 사실과 형식: 4/5 — 기존 원문의 조건·의무 구분 및 카피 잠금·캔버스 검사 통과. 이번 작업에서 외부 법률 원문을 새로 검증한 것은 아님.

### SET: COSMETICS-OEM-04 (en)

- C1 표지와 카피: 4/5 — 질문형 표지와 Cosmetics Brand Launch 표기로 맥락 제공. 7장 복합어는 길지만 조건 보존.
- C2 가독성과 일관성: 4/5 — 국문과 같은 구조, 영문에 맞춘 간격. 자동 축소·임의 분철 없음. 7장 모바일 읽기 부담은 남음.
- C3 흐름: 4/5 — 국문과 같은 카드 역할·순서. 준비자료와 검토 범위 연결.
- C4 사실과 형식: 4/5 — 같은 sourceTrace, Administrative Attorney 표기, 1080×1350 및 카피 잠금 통과. 번역 법률 용어의 최종 발행 판단은 사용자에게 남김.

## 경고 및 한계

- 표지 블록 4개: 아이콘·질문·요약·다음 장 안내 역할이 구분되며 겹침 없어 유지.
- 7장 국문 187자, 영문 444자·67단어: 예외 조건을 지워 경고만 없애지 않음. 후속 마감에서 영문 본문 17→19px로 확대하고 상자 대신 소제목과 구분선으로 재배치했다. 자동 축소 없음. 글자 수 권고는 보존한다.
- 8장 중심 편차·줄 수·빈 띠 경고: 실제 PNG의 큰 문장은 가운데 영역에 놓인다. 쉼 카드의 의도적 여백으로 유지. 측정 경고는 삭제·완화하지 않음.
- 영문 10장 345자: 자료·검토·무료 안내가 구별되고 잘림 없어 유지.
- 표지 문서 아이콘은 의미를 전달하지만 독자적인 화장품 제품 비주얼은 아니다. 완벽함이나 독자 반응은 보장하지 않는다.

두 번 더 보기: 표지 대상·문제 식별 가능, 질문·설명·저장 목록의 역할 구분, 의도 없는 내용 쏠림 없음, 제목·본문 위계 구분, 같은 배치 세 장 연속 없음, 새 사건·수치·서비스 추가 없음, 영문 사무소 명칭 유지. 수정한 영문 분철과 국문 질문 번호는 재렌더 후 다시 확인했다.

## 이전 전체 테스트 실패 3건 — 수정 완료

1. `test_copy_lint.py::FinalPolishTests::test_progress_marker_on_new_sets_only`: 기존 빌더가 legacy에도 진행 표시를 붙여 기대값과 충돌.
2. `test_copy_lint.py::CommittedSetsStayIdentical::test_rebuild_matches_committed_html`: 저장 카드와 재생성 HTML의 진행 표시 차이.
3. `test_verify_citations.py::FakeServerTests::test_round_trip_with_fake_server`: 설치된 MCP/Pydantic의 반환 모델 생성 오류.

후속 사용자 요청에 따라 빌더에서 explicit legacy의 승인 HTML을 보존하도록 수정했다. 버전 미지정 새 입력의 진행 표시는 유지하고 회귀 assertion을 추가했다. MCP 테스트는 실제 소비하는 TextContent를 명시하도록 structured_output=False를 사용했다. 검증 결과·실제 HTTP 왕복 assertion은 유지했다. 기존 발행 HTML과 테스트 임계값은 바꾸지 않았다.

영문 7장 실출력과 전체 축소 시트를 다시 확인했다. 같은 법률 문구가 더 넓은 행에서 19px로 읽히며 fitScale=1.00, fitOverflow=0이다. 이 조건은 실제 브라우저 회귀 테스트로 고정한다.

후속 검증: 전체 pytest 182 passed, 4 warnings(의존성 폐기 예정 API 안내). 실패·건너뛴 테스트 없음. 카드 스모크·지침 경로·한영 구조·배포 자료·디자인 검사 통과. 시각 회귀 5장 모두 픽셀 변화 0.000%로 통과. 기준 이미지 갱신 전 본문 영역 y=122..1219의 차이가 0임을 확인했고, 차이가 난 머리말·꼬리말·진행 표시를 직접 검수했다. 임계값을 완화하지 않았다.

장문·최대 분량 스트레스 검사: 한영 카드 조합 14개와 공유 이미지(OG) 8개, 총 22개 모두 PASS. 최종 변경의 원격 CI 실행 결과는 이 로컬 검수 기록과 별도다.

## 문체 및 발행

copy-editing으로 국문 3장 제목의 조건성을 정리. humanize-korean 최종 검토: 추가 변경 0%, B, 자체검증 6/6. A·D·G·I 탐지 0→0. ‘생략할 수 있는 경우’는 법률 한정이라 유지. 기록은 `_workspace/2026-10-18-002/final.md`. 스킬상 B 이하 정밀 검증은 Claude Code 정밀 모드(3콜) 권장.

approvedBy는 사용자 발행 승인 전 유지. 후속 요청에 따라 코드·디자인·검수 결과를 커밋·푸시한다. SNS 게시 승인을 뜻하지 않는다.
