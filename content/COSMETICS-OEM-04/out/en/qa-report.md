# QA Report

결과: PASS — PNG 생성됨

| 카드 | 유형 | 글자수 | 단어수 | 본문 채움 | 하단 여백 | 결과 |
|---|---|---:|---:|---:|---:|---|
| card_01.html | cover | 211 | 38 | 0.87 | 26 | PASS |
| card_02.html | comparison | 299 | 47 | 0.79 | 26 | PASS |
| card_03.html | concept | 304 | 51 | 0.69 | 26 | PASS |
| card_04.html | checklist | 237 | 45 | 0.88 | 26 | PASS |
| card_05.html | process | 254 | 51 | 0.91 | 26 | PASS |
| card_06.html | comparison | 315 | 50 | 0.75 | 26 | PASS |
| card_07.html | concept | 400 | 66 | 0.97 | 26 | PASS |
| card_08.html | rest | 98 | 16 | 0.4 | 26 | PASS |
| card_09.html | checklist | 311 | 52 | 0.88 | 26 | PASS |
| card_10.html | cta | 345 | 58 | 0.75 | 26 | PASS |

### card_01.html 권고
- main-zone 블록 4 > 권장 3

### card_02.html 권고
- paragraph-lines 5 > 권장 4: 'Tests raw mate'
- paragraph-lines 6 > 권장 4: 'Oversees the c'

### card_07.html 권고
- chars 400 > 권고 340 (문장 압축 또는 카드 분리 검토)
- words 66 > 권고 60 (영문 호흡과 모바일 가독성 확인)

### card_08.html 권고
- content-balance: 본문 묶음 중심 편차 -20% (위 0px / 아래 177px). 문자 정렬이 아니라 묶음 위치를 확인하세요. 의도한 비대칭은 review.md에 기록합니다.
- main-fill 0.40 < 권장 0.4 (여백이 의도적인지 시각 확인)
- headline-lines 4 > 권장 3: 'A Contract Can'
- empty-band 30% > 권장 22% (의도한 여백인지 확인: 관련 요소의 묶음·중앙 위치를 먼저 보고, 간격이나 장식으로 억지로 채우지 않는다)

### card_10.html 권고
- chars 345 > 권고 340 (문장 압축 또는 카드 분리 검토)

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