# 세 방향 시안 (예시)

표지와 본문 한 장을 세 방향으로 만들어 비교한 예시다. `python scripts/preview_drafts.py <drafts 폴더>`가 `drafts-sheet.png`(위에서부터 A·B·C·D)를 만든다. 시안은 QA 게이트를 거치지 않고, 고른 방향으로 전체 세트를 만든 뒤 `qa_render.py`로 검사한다.

- A: 브랜드 세리프 제목 + Pretendard 본문 (시범 세트 채택)
- B: 제목까지 Pretendard 800, 굵은 타이포
- C: 모든 카드 크림 바탕 여백형, 상자 대신 선
- F: 기본 표지 + 물건 그림(도장, `assets/illustrations/objects/stamp.svg`, Phosphor MIT). 네이비 배경용
- E: 생활 장면형 표지(크림 배경 전용). 제목은 원문 첫 문장("업무정지 6개월 사전통지서를 받았습니다"), 인물은 `assets/illustrations/people/`(Open Peeps CC0, 브랜드 색). 인물 5종 미리보기 `people-sheet.png`(위 네이비, 아래 크림)
- D: 마루 부리(MaruBuri) 명조 제목 + 항목 아이콘 배지(`templates/presets/ethos-d.css`). 아이콘은 `scripts/icon_svg.py`로 넣었다
