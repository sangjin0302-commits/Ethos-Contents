# QA Report

결과: FAIL — PNG 생성 안 됨

| 카드 | 유형 | 글자수 | 단어수 | 본문 채움 | 하단 여백 | 결과 |
|---|---|---:|---:|---:|---:|---|
| card_01.html | cover | 186 | 39 | 1.23 | 26 | FAIL |
| card_02.html | checklist | 261 | 44 | 0.87 | 26 | FAIL |
| card_03.html | comparison | 344 | 66 | 0.91 | 26 | FAIL |
| card_04.html | table | 387 | 66 | 1.15 | 26 | FAIL |
| card_05.html | comparison | 439 | 68 | 1.11 | 26 | FAIL |
| card_06.html | concept | 307 | 59 | 0.81 | 26 | FAIL |
| card_07.html | concept | 428 | 72 | 1.26 | 26 | FAIL |
| card_08.html | quote | 423 | 77 | 1.04 | 26 | FAIL |
| card_09.html | quote | 436 | 73 | 0.99 | 26 | FAIL |
| card_10.html | cta | 490 | 78 | 1.28 | 26 | FAIL |

### card_01.html
- zone-overflow:main
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_02.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_03.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_03.html 권고
- chars 344 > 권고 340 (문장 압축 또는 카드 분리 검토)
- words 66 > 권고 60 (영문 호흡과 모바일 가독성 확인)

### card_04.html
- zone-overflow:main
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_04.html 권고
- chars 387 > 권고 340 (문장 압축 또는 카드 분리 검토)
- words 66 > 권고 60 (영문 호흡과 모바일 가독성 확인)

### card_05.html
- zone-overflow:main
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_05.html 권고
- chars 439 > 강한 경고 340 (문장 압축 또는 카드 분리 검토)
- words 68 > 권고 60 (영문 호흡과 모바일 가독성 확인)
- paragraph-lines 6 > 권장 4: 'Record expecte'

### card_06.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_07.html
- zone-overflow:main
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_07.html 권고
- chars 428 > 강한 경고 340 (문장 압축 또는 카드 분리 검토)
- words 72 > 권고 60 (영문 호흡과 모바일 가독성 확인)

### card_08.html
- zone-overflow:main
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_08.html 권고
- chars 423 > 강한 경고 340 (문장 압축 또는 카드 분리 검토)
- words 77 > 강한 경고 60 (영문 호흡과 모바일 가독성 확인)
- paragraph-lines 6 > 권장 4: 'The case conce'

### card_09.html
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_09.html 권고
- chars 436 > 강한 경고 340 (문장 압축 또는 카드 분리 검토)
- words 73 > 강한 경고 60 (영문 호흡과 모바일 가독성 확인)

### card_10.html
- zone-overflow:main
- frame-drift wordmark.top: 8.0 != 20
- frame-drift section.top: 8.0 != 20

### card_10.html 권고
- chars 490 > 강한 경고 340 (문장 압축 또는 카드 분리 검토)
- words 78 > 강한 경고 60 (영문 호흡과 모바일 가독성 확인)
- paragraph-lines 5 > 권장 4: 'This work refl'

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