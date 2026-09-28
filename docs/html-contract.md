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

- 카드 크기 540×540, 파일명 `card_01.html` … (페이지 순서와 일치). 국·영문 위치는 각각
  `content/<ID>/ko/card_NN.html`, `content/<ID>/en/card_NN.html`이다.
- 언어 폴더에서는 CSS 링크를 `../../../brand/…`, `../../../templates/…`로 쓴다(깊이 3단계 고정).
- `main` 존의 직계 자식은 3개 이하. 카드당 글자 수 180자 이하(공백 제외).
- 골드 글씨는 **네이비 계열 배경에서만**. 크림 위 골드는 대비 2.4:1 이라 텍스트 금지(선·장식만).
- 크림 카드의 비장식 골드 텍스트는 크기와 무관하게 QA 하드 실패다. 결론은 네이비 텍스트 또는 네이비 박스를 사용한다.
- 영문 헤드라인과 소제목은 700 이상의 웨이트를 사용한다.
- 카드 유형은 연속 3장 같으면 안 되고, `takeaway` 바는 세트의 40% 이하.
- 6장 이상 세트는 원문 근거가 있는 한 `checklist`와 `process`를 각각 최소 1장 포함한다.
- 6장 이상 세트는 최소 4개 유형을 사용하고, 단일 유형이 전체의 절반을 넘지 않는다.
- 도식 화살표는 인라인 SVG. 이모지 금지.
