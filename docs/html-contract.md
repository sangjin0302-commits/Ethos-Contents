# 카드 HTML 계약

`scripts/qa_render.py` 는 아래 속성을 읽어 검사한다. 속성이 없으면 검사가 실패한다.

```
<div class="card navy|cream" data-card-type="cover|concept|comparison|process|checklist|quote|cta"
     data-bg="navy|cream" data-page="N">
  frame:  data-frame="gold-top|gold-bottom|wordmark|section|line|org|tagline|page"   ← templates/card.html 그대로
  body :  data-zone="title|main|take"            (title, main 필수 / take 는 결론 바)
  글자  :  data-role="headline|label|note|takeaway"   (없으면 본문: 16px↑)
  장식  :  data-decor      (정보 없는 큰 번호 등. 대비 검사 제외)
  기호  :  data-symbol-ok  (+ = ≠ 사용을 brief.md 에서 승인한 경우만)
</div>
```

- 카드 크기 540×540, 파일명 `card_01.html` … (페이지 순서와 일치). 위치는 `content/<ID>/card_NN.html`,
  CSS 링크는 `templates/card.html` 의 `../../brand/…`, `../../templates/…` 경로 그대로 쓴다(깊이 2단계 고정).
- `main` 존의 직계 자식은 3개 이하. 카드당 글자 수 180자 이하(공백 제외).
- 골드 글씨는 **네이비 계열 배경에서만**. 크림 위 골드는 대비 2.4:1 이라 텍스트 금지(선·장식만).
- 카드 유형은 연속 3장 같으면 안 되고, `takeaway` 바는 세트의 40% 이하.
- 도식 화살표는 인라인 SVG. 이모지 금지.
