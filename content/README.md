# content/

콘텐츠 1편 = 폴더 1개. `content/_TEMPLATE/` 를 복사해 `content/<CONTENT_ID>/` 를 만든다.

```
content/GAME-KR-06/
  blog.md            승인된 원문 (사람이 넣는다)
  brief.md           각도·Hook·카드 계획 (에이전트 작성 → 사람 승인)
  card-data.ko.json  국문 카피 + Source Trace (승인 표시 후 렌더)
  card-data.en.json  영문 카피 + 동일 근거 Source Trace (승인 표시 후 렌더)
  ko/card_01.html …  국문 카드 HTML (에이전트)
  en/card_01.html …  영문 카드 HTML (에이전트)
  distribution.md    국·영문 게시 캡션·Hook·CTA·성과 기록
  assets.md          외부 이미지·아이콘·일러스트 출처와 라이선스 기록
  out/ko/            국문 png/, sheet-270.png, qa-report.md|json
  out/en/            영문 png/, sheet-270.png, qa-report.md|json
```

사용자가 채팅에 원문만 제공한 경우에도 에이전트가 위 구조를 만들고 brief 승인 단계까지 진행한다.
