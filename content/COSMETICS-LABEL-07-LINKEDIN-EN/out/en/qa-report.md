# QA Report

결과: PASS — PNG 생성됨

## 세트 권고
- recommended-type process 없음 (원문에 실제 내용이 없으면 추가하지 않음)
- same-type x3: comparison (연속 권장 2장)

| 카드 | 유형 | 글자수 | 단어수 | 본문 채움 | 하단 여백 | 결과 |
|---|---|---:|---:|---:|---:|---|
| card_01.html | cover | 296 | 49 | 0.76 | 26 | PASS |
| card_02.html | comparison | 345 | 58 | 0.57 | 26 | PASS |
| card_03.html | concept | 317 | 54 | 0.99 | 26 | PASS |
| card_04.html | comparison | 314 | 53 | 0.65 | 26 | PASS |
| card_05.html | comparison | 288 | 45 | 0.75 | 26 | PASS |
| card_06.html | comparison | 275 | 44 | 0.77 | 26 | PASS |
| card_07.html | rest | 182 | 29 | 0.21 | 26 | PASS |
| card_08.html | checklist | 299 | 57 | 0.72 | 26 | PASS |
| card_09.html | table | 303 | 50 | 0.85 | 26 | PASS |
| card_10.html | cta | 375 | 62 | 0.62 | 26 | PASS |

### card_01.html 권고
- words 49 > 권고 48 (영문 호흡과 모바일 가독성 확인)

### card_02.html 권고
- chars 345 > 권고 300 (문장 압축 또는 카드 분리 검토)
- words 58 > 권고 48 (영문 호흡과 모바일 가독성 확인)
- paragraph-lines 5 > 권장 4: 'Product name, '
- paragraph-lines 6 > 권장 4: 'Claims such as'

### card_03.html 권고
- chars 317 > 권고 300 (문장 압축 또는 카드 분리 검토)
- words 54 > 권고 48 (영문 호흡과 모바일 가독성 확인)
- headline-chars 61 > 권장 54

### card_04.html 권고
- chars 314 > 권고 300 (문장 압축 또는 카드 분리 검토)
- words 53 > 권고 48 (영문 호흡과 모바일 가독성 확인)
- paragraph-lines 5 > 권장 4: 'Obtain the fin'
- paragraph-lines 5 > 권장 4: 'Compare produc'

### card_06.html 권고
- paragraph-lines 6 > 권장 4: 'Phrases sugges'

### card_07.html 권고
- main-fill 0.21 < 권장 0.4 (여백이 의도적인지 시각 확인)
- headline-words 10 > 권장 9
- empty-band 25% > 권장 22% (의도한 여백인지 확인: 관련 요소의 묶음·중앙 위치를 먼저 보고, 간격이나 장식으로 억지로 채우지 않는다)

### card_08.html 권고
- words 57 > 권고 48 (영문 호흡과 모바일 가독성 확인)

### card_09.html 권고
- chars 303 > 권고 300 (문장 압축 또는 카드 분리 검토)
- words 50 > 권고 48 (영문 호흡과 모바일 가독성 확인)

### card_10.html 권고
- chars 375 > 권고 300 (문장 압축 또는 카드 분리 검토)
- words 62 > 권고 48 (영문 호흡과 모바일 가독성 확인)
- paragraph-lines 5 > 권장 4: 'Send the final'
- paragraph-lines 7 > 권장 4: 'Ethos Administ'

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

게이트 v1.6 · 기준은 초기 가설(instagram-profile-advisory)