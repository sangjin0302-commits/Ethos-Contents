# QA Report

결과: FAIL — PNG 생성 안 됨

| 카드 | 유형 | 글자수 | 단어수 | 본문 채움 | 하단 여백 | 결과 |
|---|---|---:|---:|---:|---:|---|
| card_01.html | cover | 88 | 30 | 0.78 | 26 | FAIL |
| card_02.html | comparison | 153 | 50 | 0.44 | 26 | FAIL |
| card_03.html | quote | 187 | 58 | 0.78 | 26 | FAIL |
| card_04.html | checklist | 102 | 31 | 0.52 | 26 | FAIL |
| card_05.html | concept | 150 | 44 | 0.66 | 26 | FAIL |
| card_06.html | concept | 130 | 38 | 0.62 | 26 | FAIL |
| card_07.html | rest | 46 | 16 | 0.75 | 26 | FAIL |
| card_08.html | comparison | 169 | 52 | 0.39 | 26 | FAIL |
| card_09.html | checklist | 142 | 48 | 0.55 | 26 | FAIL |
| card_10.html | cta | 126 | 41 | 0.56 | 26 | FAIL |

### card_01.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_02.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_02.html 권고
- paragraph-lines 5 > 권장 4: '「화장품법 시행규칙」 제1'
- empty-band 22% > 권장 22% (의도한 여백인지 확인: 관련 요소의 묶음·중앙 위치를 먼저 보고, 간격이나 장식으로 억지로 채우지 않는다)

### card_03.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_03.html 권고
- chars 187 > 권고 180 (문장 압축 또는 카드 분리 검토)

### card_04.html
- overflow-x:body
- overflow-x:z-main
- overflow-x:question-grid
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_04.html 권고
- paragraph-lines 6 > 권장 4: '기능성 성분과 함량이 고시'
- paragraph-lines 6 > 권장 4: '성분 조합과 시험방법이 고'

### card_05.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_06.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20
- fact-lock: '06 일' 가 원문에 없음

### card_07.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_07.html 권고
- headline-lines 3 > 권장 2: '결정적인 것은 공장의 말보'

### card_08.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_08.html 권고
- main-fill 0.39 < 권장 0.4 (여백이 의도적인지 시각 확인)
- empty-band 23% > 권장 22% (의도한 여백인지 확인: 관련 요소의 묶음·중앙 위치를 먼저 보고, 간격이나 장식으로 억지로 채우지 않는다)

### card_09.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_10.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

## 사람이 확인할 것 (자동화 불가)
- [ ] 법령·판례 해석이 원문과 일치하는가 (변호사·행정사 최종 확인)
- [ ] sheet-270.png 크기에서 표지가 2초 안에 대상·문제·정보 보상 중 둘 이상을 전달하는가
- [ ] 제목·본문·근거·결론의 위계가 한눈에 구분되는가
- [ ] 상단과 하단의 시각 무게가 한쪽으로 몰리지 않고 여백이 의도적으로 보이는가
- [ ] 영문 카드가 번역문을 밀어 넣은 느낌 없이 자연스러운 호흡으로 읽히는가
- [ ] 세트 전체가 같은 박스 구조를 반복하지 않고 메시지에 맞는 시각 리듬을 갖는가
- [ ] 원문의 또는/그리고/~수 있다 뉘앙스가 카드에서 바뀌지 않았는가
- [ ] 마지막 장 CTA 문구가 마스터 지침의 무료 검토 안내와 일치하는가
- [ ] 카드 한 장이 한 가지 메시지만 전달하는가

게이트 v1.7 · 기준은 초기 가설(instagram-profile-advisory)