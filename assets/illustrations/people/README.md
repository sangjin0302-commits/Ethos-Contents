# 인물 장면 일러스트 (Open Peeps, CC0)

- 원작: Open Peeps, Pablo Stanley (https://www.openpeeps.com/), CC0 1.0(저작권 표시 의무 없음)
- 추출: npm `@opeepsfun/open-peeps` 1.0.6(MIT, React 컴포넌트)을 React 18 `renderToStaticMarkup`으로 SVG로 렌더, 2026-10-06
- 수정: 색만 바꿨다. 선은 크림, 피부는 네이비, 상의는 골드, 종이·컵·화면은 흰색이고 모두 `var(--ethos-*)` 토큰이다. 원본의 브랜드 밖 색(분홍·갈색·은색)은 가까운 브랜드 색으로 바꿨다. 도형은 원본 그대로.

| 파일 | 장면 | 어울리는 표지 |
|---|---|---|
| `notice-worried.svg` | 서류를 들고 걱정하는 사람 | 사전통지·처분서를 받은 상황 |
| `explaining.svg` | 손짓하며 설명하는 사람 | 절차 안내·상담 |
| `online-filing.svg` | 노트북으로 신청하는 사람 | 온라인 신고·등록 |
| `owner-calm.svg` | 컵을 든 차분한 사람 | 영업 중인 사장님·일상 장면 |
| `pointing-guide.svg` | 위를 가리키는 사람 | 기준·체크리스트 안내 |

쓰는 법: SVG를 카드 HTML에 그대로 붙이고(색은 CSS 토큰이라 배경에 맞게 따라간다) `content/<ID>/assets.md`에 `open-peeps/<파일 이름>` 한 줄을 적는다. 표지의 생활 장면에만 쓰고, 실제 고객·사건처럼 보이게 하지 않는다(`docs/asset-policy.md`). 예시: `examples/free-design-realtor/drafts/E/`.

새 장면을 더 만들려면 위 npm 패키지의 `Effigy`(body·head·face·accessory 조합)를 같은 방식으로 렌더하고 색을 토큰으로 바꾼다.
