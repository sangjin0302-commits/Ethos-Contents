# QA Report

결과: PASS — PNG 생성됨

## 세트 권고
- recommended-type process 없음 (원문에 실제 내용이 없으면 추가하지 않음)

| 카드 | 유형 | 글자수 | 단어수 | 본문 채움 | 하단 여백 | 결과 |
|---|---|---:|---:|---:|---:|---|
| card_01.html | cover | 229 | 38 | 0.86 | 26 | PASS |
| card_02.html | comparison | 309 | 52 | 0.71 | 26 | PASS |
| card_03.html | comparison | 325 | 55 | 0.75 | 26 | PASS |
| card_04.html | concept | 306 | 52 | 1.0 | 26 | PASS |
| card_05.html | comparison | 306 | 51 | 0.65 | 26 | PASS |
| card_06.html | table | 333 | 59 | 0.86 | 26 | PASS |
| card_07.html | concept | 404 | 72 | 0.84 | 26 | PASS |
| card_08.html | rest | 160 | 26 | 0.52 | 26 | PASS |
| card_09.html | checklist | 299 | 55 | 0.51 | 26 | PASS |
| card_10.html | cta | 343 | 59 | 0.95 | 26 | PASS |

### card_02.html 권고
- weak-focal: 시각 중심이 작습니다(글자 0px, 아이콘 1%). 36px 이상 글자나 큰 아이콘으로
- paragraph-lines 5 > 권장 4: 'The cosmetics '

### card_03.html 권고
- weak-focal: 시각 중심이 작습니다(글자 25px, 아이콘 0%). 36px 이상 글자나 큰 아이콘으로

### card_05.html 권고
- weak-focal: 시각 중심이 작습니다(글자 23px, 아이콘 0%). 36px 이상 글자나 큰 아이콘으로

### card_07.html 권고
- chars 404 > 권고 340 (문장 압축 또는 카드 분리 검토)
- words 72 > 권고 60 (영문 호흡과 모바일 가독성 확인)

### card_10.html 권고
- chars 343 > 권고 340 (문장 압축 또는 카드 분리 검토)

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