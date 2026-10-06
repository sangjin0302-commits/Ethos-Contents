# Lucide icons (vendored)

- Source: https://github.com/lucide-icons/lucide (`icons/<name>.svg`)
- License: ISC (see `LICENSE`; the file also carries the MIT notice for the Feather-derived icons)
- Checked: 2026-10-05, 2026-10-06(lucide-static 1.52.0에서 전체 세트로 확장)
- Modification: 도형은 원본 그대로. lucide-static에서 가져온 파일만 첫 줄 라이선스 주석과 `class` 속성을 뺐다(빌더가 class를 넣으므로). 크기와 선 굵기, 색은 `templates/card-types.css`에서 CSS로만 바꾼다.

카드 `icon` / `art` 필드는 이 폴더의 파일 이름(확장자 제외)만 받는다. 새 아이콘을 추가하면 같은 폴더에 원본 그대로 넣고, 사용한 아이콘은 해당 `content/<ID>/assets.md`에 한 줄씩 기록한다(`docs/asset-policy.md`).

## 전체 세트

이 폴더에는 해당 버전의 **전체 아이콘**이 들어 있다. 아래 "추천 목록"은 법률·행정 콘텐츠에서 자주 쓰는 이름을 용도별로 고른 것이며, 목록에 없어도 파일이 있으면 `icon`에 쓸 수 있다. 고를 때는 ① 추천 목록 ② 의미가 분명한 이름(다른 뜻으로 읽히지 않는 것) 순으로 정한다. 장식이 아니라 항목의 뜻을 돕는 아이콘만 쓰고, 한 세트에서 Lucide와 Tabler를 섞어도 선 굵기·크기는 CSS가 같게 맞춘다.

## 추천 목록 (용도별)

- 기한·절차: calendar-clock, calendar-days, clock, hourglass, route, list-checks, clipboard-check
- 서류: file-text, file-check, file-warning, file-search, file-x, file-pen-line, files, folder-open, scroll-text, signature, stamp, receipt
- 사람·체류: id-card, plane, user-check, users, languages, globe, graduation-cap
- 사업·장소: building-2, briefcase-business, store, house, key-round, truck, utensils, landmark, map-pin
- 돈: banknote, hand-coins, calculator
- 판단·경고: scale, gavel, shield-check, badge-check, badge-alert, circle-alert, circle-check, triangle-alert, ban, search, target, lightbulb
- 강연·안내: mic, presentation, message-square-text, book-open-text
