# 자유 디자인(B) 시범 세트 — 공인중개사 업무정지

`docs/card-design-guide.md`의 기준 예시다. **발행용이 아니다**(사용자 승인 전 비교용 초안).

- `card-data.ko.json`: 문구 원본(ChatGPT 통합 테스트 산출물, 법령·재결례는 2026-10-06 원문 대조)
- `design.css`: 세트 공통 스타일과 맨 위 설계 메모
- `ko/card_NN.html`: 카드별 직접 디자인. 맨 위 `<meta name="ethos-design" content="free">`
- `out/ko/`: `qa_render.py` 결과(QA PASS)와 `sheet-270.png`

같은 문구를 기본 빌더로 렌더한 결과와 비교하면 차이가 보인다: 제목 40px·본문 23~25px의 위계, 카드마다 다른 구도, 결론 띠 3장.
