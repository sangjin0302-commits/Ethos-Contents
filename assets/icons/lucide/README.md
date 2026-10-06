# Lucide icons (vendored)

- Source: https://github.com/lucide-icons/lucide (`icons/<name>.svg`)
- License: ISC (see `LICENSE`; the file also carries the MIT notice for the Feather-derived icons)
- Checked: 2026-10-05, 2026-10-06(lucide-static 1.52.0에서 행정·비자·기한 아이콘 37개 추가)
- Modification: 도형은 원본 그대로. lucide-static에서 가져온 파일만 첫 줄 라이선스 주석과 `class` 속성을 뺐다(빌더가 class를 넣으므로). 크기와 선 굵기, 색은 `templates/card-types.css`에서 CSS로만 바꾼다.

카드 `icon` / `art` 필드는 이 폴더의 파일 이름(확장자 제외)만 받는다. 새 아이콘을 추가하면 같은 폴더에 원본 그대로 넣고, 사용한 아이콘은 해당 `content/<ID>/assets.md`에 한 줄씩 기록한다(`docs/asset-policy.md`).

## 목록 (용도별)

- 기한·절차: calendar-clock, calendar-days, clock, hourglass, route, list-checks, clipboard-check
- 서류: file-text, file-check, file-warning, file-search, file-x, file-pen-line, files, folder-open, scroll-text, signature, stamp, receipt
- 사람·체류: id-card, plane, user-check, users, languages, globe, graduation-cap
- 사업·장소: building-2, briefcase-business, store, house, key-round, truck, utensils, landmark, map-pin
- 돈: banknote, hand-coins, calculator
- 판단·경고: scale, gavel, shield-check, badge-check, badge-alert, circle-alert, circle-check, triangle-alert, ban, search, target, lightbulb
- 강연·안내: mic, presentation, message-square-text, book-open-text
