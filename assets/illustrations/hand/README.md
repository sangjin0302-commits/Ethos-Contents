# 손그림 선화 (IRA Design Outline, MIT)

- 원본: IRA Design(Creative Tim) `SVG.zip` → `SVG/Outline/Objects`, `SVG/Outline/Characters`(https://github.com/ira-design/ira-illustrations, `SVG` 브랜치), MIT(`LICENSE-ira.md`), 2026-10-06
- 수정: 색만 바꿨다. 선(#151515·#000)은 `currentColor`, 옅은 면은 `--hand-fill`(기본 골드), 흰 면은 `--hand-paper`. 도형은 그대로. 그라데이션 버전은 브랜드 규칙상 쓰지 않는다.
- 프리셋 A가 배경에 맞춰 색을 정한다: 크림 카드는 네이비 선 + 흰 면, 네이비 카드는 크림 선 + 네이비 면. 면 강조는 골드.

| 종류 | 파일 |
|---|---|
| 물건 | bag, books, calendar, card, coffee-cup, computer, inbox, laptop, phone, pin, table, tag, wallet |
| 인물(크림 카드 전용) | character-1, 2, 3, 5, 8, 12 |

Phosphor 물건(`../objects/`)보다 선이 가늘고 손으로 그린 느낌이라 표지·쉼 카드에 어울린다. 쓰는 법은 `.hand-hero` 안에 SVG를 붙이고 `assets.md`에 `ira/<이름>`과 MIT를 적는다.
