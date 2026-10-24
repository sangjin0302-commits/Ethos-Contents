## COSMETICS-LABEL-07-CARD-DRAFT

- `ko`: 자동 디자인 초안 10장(`scripts/auto_design.py`). Codex가 `content/<ID>/ko/`로 복사해 다듬으면 발행본
### ko: QA PASS ✅ · 린터 경고 1건
- 린터 `so-many-therefore` blog: 문장 첫머리 '따라서'가 4번입니다.
- 윤문 힌트(권고, `examples/writing/README.md` 참고) 7건:
  - `headline-monotony` [ko]: assertion 형태가 8/10장입니다.
  - `legalese` [ko] card 7: 법률 문서 말투: 범위에서
  - `repeated-connector` blog: 문장 첫머리에 '다만' 7번.
  - `repeated-connector` blog: 문장 첫머리에 '따라서' 7번.
  - `repeated-connector` blog: 문장 첫머리에 '특히' 5번.
  - `stock-phrase` blog: '살펴보겠습니다' 6번.
  - `stock-phrase` blog: '필요가 있습니다' 5번.
- 디자인 점검(권고, `scripts/design_review.py`) 6건:
  - `auto-draft` 자동 디자인 초안입니다(10장, scripts/auto_design.py). → 발행본은 Codex가 content/<ID>/<lang>/로 복사해 카드마다 다듬으세요(docs/card-codex-production.md).
  - `focal-repeat` card_04.html: 시각 중심 'keyword'이 세 장 연속입니다. → 실제 시트에서 반복이 이해를 돕는지 확인하세요. 같은 구조가 적합하면 유지합니다.
  - `focal-repeat` card_08.html: 시각 중심 'keyword'이 세 장 연속입니다. → 실제 시트에서 반복이 이해를 돕는지 확인하세요. 같은 구조가 적합하면 유지합니다.
  - `focal-repeat` 시각 중심 'keyword'이 본문 8장 중 6장입니다. → 비율만으로 미감을 판단하지 않습니다. 메시지 차이가 실제로 읽히는지 확인하세요.
  - `layout-repeat` card_03.html: 앞 카드와 본문 구조가 같습니다(krows). → 연결된 비교라면 같은 구도가 유용할 수 있습니다. 장식용 변주보다 정보 관계를 우선하세요.
  - `layout-repeat` card_08.html: 앞 카드와 본문 구조가 같습니다(krows). → 연결된 비교라면 같은 구도가 유용할 수 있습니다. 장식용 변주보다 정보 관계를 우선하세요.
- `ko` 디자인 권고 5건 — 실제 이미지를 보고 판단; 발행 차단 아님

- `en`: card-data.en.json 없음 — 초안 폴더라 안내만 합니다(승인 전 영문 필요)
- 가로 대표 이미지(1200×630) `og-ko.png`: PASS ✅