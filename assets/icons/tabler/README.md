# Tabler icons (vendored)

- Source: https://github.com/tabler/tabler-icons (`icons/outline/<name>.svg`, @tabler/icons 3.49.0)
- License: MIT (see `LICENSE`)
- Checked: 2026-10-06
- Modification: 도형은 원본 그대로. 첫 줄 `class` 속성만 뺐다(빌더가 `class="ico"`를 넣으므로). 크기·선 굵기·색은 `templates/card-types.css`가 CSS로만 바꾼다.

Lucide에 없는 이름만 모았다. `icon` / `art` / 항목별 `icon`에는 파일 이름(확장자 제외)만 쓰며, 빌더는 Lucide를 먼저 찾고 없으면 Tabler를 찾는다. 사용한 아이콘은 `content/<ID>/assets.md`에 `tabler/<이름>.svg`로 한 줄 기록한다(`copy_lint.py`가 누락을 경고한다).

## 목록 (용도별)

- 기관·자격: building-bank, building-factory, building-skyscraper, certificate, license, file-certificate, id-badge-2, rosette-discount-check, flag-check, home-check
- 서류·계약: contract, writing-sign, file-description, file-invoice, file-time, file-export, file-import, archive, checklist
- 돈: coin, cash, credit-card, report-money
- 숫자·비교: chart-bar, chart-line, chart-pie, report-analytics, trending-up, trending-down, timeline, arrows-split, arrows-exchange, scale-outline
- 기한·절차: calendar-due, calendar-event, clock-hour-3, hourglass-high, door-enter, door-exit
- 사람·체류: users-group, user-search, user-exclamation, user-x, heart-handshake, plane-departure, plane-arrival, world-check, world-www, ticket
- 안내·경고: help-circle, info-circle, bulb, target-arrow, alert-octagon, shield-lock, lock, lock-open, eye, bell, mail, phone, message-circle, device-desktop
