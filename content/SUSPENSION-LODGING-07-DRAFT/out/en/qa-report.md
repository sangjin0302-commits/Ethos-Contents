# QA Report

결과: FAIL — PNG 생성 안 됨

| 카드 | 유형 | 글자수 | 단어수 | 본문 채움 | 하단 여백 | 결과 |
|---|---|---:|---:|---:|---:|---|
| card_01.html | cover | 199 | 36 | 0.66 | 26 | FAIL |
| card_02.html | concept | 346 | 62 | 0.81 | 26 | FAIL |
| card_03.html | checklist | 298 | 58 | 0.76 | 26 | FAIL |
| card_04.html | comparison | 357 | 66 | 0.54 | 26 | FAIL |
| card_05.html | flow | 273 | 50 | 0.65 | 26 | FAIL |
| card_06.html | concept | 360 | 63 | 0.82 | 26 | FAIL |
| card_07.html | concept | 346 | 66 | 0.81 | 26 | FAIL |
| card_08.html | rest | 106 | 21 | 0.87 | 26 | FAIL |
| card_09.html | process | 374 | 66 | 0.78 | 26 | FAIL |
| card_10.html | cta | 350 | 64 | 0.62 | 26 | FAIL |

### card_01.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_02.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_02.html 권고
- chars 346 > 권고 340 (문장 압축 또는 카드 분리 검토)
- words 62 > 권고 60 (영문 호흡과 모바일 가독성 확인)

### card_03.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_04.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_04.html 권고
- chars 357 > 권고 340 (문장 압축 또는 카드 분리 검토)
- words 66 > 권고 60 (영문 호흡과 모바일 가독성 확인)
- paragraph-lines 6 > 권장 4: 'Missing online'

### card_05.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_06.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_06.html 권고
- chars 360 > 권고 340 (문장 압축 또는 카드 분리 검토)
- words 63 > 권고 60 (영문 호흡과 모바일 가독성 확인)

### card_07.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_07.html 권고
- chars 346 > 권고 340 (문장 압축 또는 카드 분리 검토)
- words 66 > 권고 60 (영문 호흡과 모바일 가독성 확인)

### card_08.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_08.html 권고
- headline-lines 4 > 권장 3: 'A second citat'

### card_09.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_09.html 권고
- chars 374 > 권고 340 (문장 압축 또는 카드 분리 검토)
- words 66 > 권고 60 (영문 호흡과 모바일 가독성 확인)

### card_10.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_10.html 권고
- chars 350 > 권고 340 (문장 압축 또는 카드 분리 검토)
- words 64 > 권고 60 (영문 호흡과 모바일 가독성 확인)
- paragraph-lines 6 > 권장 4: 'ETHOS Administ'

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