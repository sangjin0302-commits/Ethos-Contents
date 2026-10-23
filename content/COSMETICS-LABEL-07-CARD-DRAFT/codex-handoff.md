# Codex 인계 — 화장품 표시·광고 ⑦편 국문 카드뉴스 JSON → JPEG

> 2026-10-23 사용자 직접 요청: **코덱스가 카드뉴스 JSON을 직접 작성하고 국문 JPEG 이미지까지 한 작업으로 제작**한다. 별도 영문·아랍어 세트는 요청하지 않았다. 작업물은 미발행 검토용이며, **발행 승인과 법률 적합성의 최종 확인을 받았다고 주장하지 않는다.**

## 시작 위치·범위

- 저장소: `sangjin0302-commits/Ethos-Contents`
- 시작 작업 브랜치: `codex/cosmetics-label-07-jpeg-20261023`
- 작업 폴더: `content/COSMETICS-LABEL-07-CARD-DRAFT/`; **이 폴더 밖은 읽기만 하고 수정하지 않는다.**
- 카드 Source Lock 후보: `content/COSMETICS-LABEL-07-CARD-DRAFT/blog.md` (이 브랜치에 이미 생성되어 있음).
- 원본 대조 경로: `examples/writing/samples/cosmetics-label-07-user-edited-20261023.md`의 **'## 사용자 제공 전체 원고 (편집기 잔여물만 정리)' 아래**. 이 사용자 직접 편집본을 기준으로 하며 오래된 PR #71의 `blog.md`로 대체하지 않는다.
- `blog.md`는 원문 문장과 법률 수치·한정어를 유지하고 제목/소제목의 Markdown 서식만 통일한 작업용 잠금본이다. 사용자가 카드 파생을 요청한 원문이지만, 샘플 자체는 전체 법률 검증 완료·공식 게시 승인으로 표시돼 있지 않다.
- 최신 필수 명세: `docs/card-authoring-spec.md` + `docs/card-codex-production.md`; 검증·렌더 필요시에만 그 명세가 가리키는 파일을 추가로 읽는다. 이전 ⑥편의 디자인을 그대로 복사하지 않는다.

## 필수 산출물

```text
content/COSMETICS-LABEL-07-CARD-DRAFT/
  blog.md                          # 기존 사용자 수정본; 법률 오류 발견 시 임의 변경 금지
  codex-handoff.md                 # 이 인계서
  brief.md                         # 중심 질문·스토리보드·채택 근거·OMITTED
  card-data.ko.json                # 국문 6~10장, 가급적 10장, Source Lock
  distribution.md                  # 국문 SNS 캡션·저장 이유·카드 alt text
  assets.md                        # 실제 사용한 아이콘 등 에셋 출처
  wireframe.txt                    # 카드별 배치 방향
  design.css                       # 브랜드 기존 프리셋 상속, 고유 보정
  ko/card_01.html ...              # 본문과 일치하는 카드 HTML
  out/ko/card_01.png ...           # 1080×1350 원본 PNG, QA용
  out/ko/sheet-270.png             # 휴대폰 축소 검토용
  out/ko/qa-report.md              # 렌더 QA
  out/ko/jpeg/card_01.jpg ...      # **사용자가 요청한 최종 전달용 JPEG**
  out/ko/jpeg/cosmetics-label-07-ko-jpegs.zip
  review.md                        # 실제 검수 결과, 발행 전 남은 확인사항
```

필요한 다른 산출물(예: `lead-magnet.md`)은 현재 명세상 정말 요구될 때만 추가한다.

## 카드 기획: 질문을 반복하지 말고 10장에 판단을 분산

**중심 질문:** OEM 크림의 패키지를 인쇄하고 온라인·SNS 광고를 공개하기 전에 어떤 자료를 맞춰야 하나?

권장 10장 역할(카드당 한 메시지; 실제 검증 후 순서·구도 조정 가능):

1. 표지: '미백·주름개선 크림, 인쇄 전에 문구부터 비교하세요' — 제조자료·포장·광고의 세 차이
2. 용기 vs 상자: 1차·2차 포장의 기재사항 차이
3. 5mL 체험용·30mL 여행용: 작은 제품이라도 표시 면제의 대상·범위가 다름(법정 10 이하, 10 초과 50 이하 등 **원문 조건 보존**)
4. 제품명에 성분: 복합원료 2%와 완제품 특정 성분 2%의 차이
5. '2중 기능성' 판단: 원료 두 개만으로는 부족, **두 기능의 심사 또는 보고 내역**
6. 쉼(rest): '공장 자료와 포장 문구가 맞아야 합니다'처럼 앞 판단을 하나로 회수 (새 정보 금지)
7. 광고의 한계: '미백에 도움' vs '기미 치료' — 의약품 오인 광고 구분
8. 시험자료: 원료 시험 vs 완제품 광고 주장 (필요하다면 15일 제출기한은 정확한 근거·주체·기산점 보존)
9. SNS·협찬 광고: 채널·대행사가 달라도 같은 법적 기준 적용; **AI 전문가 오인 광고 규정은 한 장에서 의미를 혼합하게 되면 OMITTED에 남길 것**
10. 저장/CTA: 최종 처방·심사/보고 자료·용기/상자 시안·광고 문안을 대조하고, 에토스의 **무료 사전 확인**과 별도 유료 문서작성·제출 범위를 명확히 구분

- 원고 전체의 법령·모든 예외를 다 넣으려고 10장을 과밀하게 만들지 않는다. 생략한 법률적 세부 사항은 `brief.md`의 `OMITTED`에 적는다.
- 원고의 수치·인용·'또는/이하/초과/할 수 있다/정당한 사유'를 단순화하다 의미를 바꾸지 않는다. 표시·광고 효능과 기술적 시험·행정사 업무범위를 혼동하지 않는다.
- 가상 인물 민수 씨는 원고의 설명 인물로만 사용. 실제 고객·후기·성과로 표현 금지.
- 표지 `art`는 원고의 상자·용기·상세페이지에 맞는 기존 허용 아이콘을 조합. 번호 큰 `hero`는 원고에 있는 강한 숫자가 아닌 한 억지로 넣지 않는다.
- 카드 한 장에 한 메시지, 카드 글자 한도·줄바꿈·금지 표현, 시리즈 정식명·회차 유지. 원문에 없는 숫자·사건·서비스 추가 금지. 최종 CTA는 한 번만.

## 진행 순서

1. 현재 `main` 명세와 준비한 `blog.md`를 확인하고 원문이 구버전 PR #71이 아닌지 검증한다. 원고·법령 근거 중 **해당 카드 주장의 법적 의미**를 현행 공식 자료와 대조하되, 본문 밖 새로운 법률 사실을 카드에 직접 추가하지 않는다. 오류가 발견되면 필요한 원문 보강·사용자 승인이 남았음을 `review.md`에 기록한다. 중요한 미확인 주장으로 JPEG를 확정하지 않는다.
2. `brief.md` → `card-data.ko.json` → `distribution.md`를 **Codex가 직접 작성**한다. JSON에는 `contentId: "COSMETICS-LABEL-07-CARD-DRAFT"`, `language: "ko"`, 정식 `series`, `issue: "No.07"`, `editorialReview`를 명시한다. `approvedBy`는 사용자 카드 문구 승인 전에는 **'비교용 초안 — 사용자 승인 전. 발행 금지'**로 둔다. 아직 수행하지 않은 검증에 `pass`를 쓰지 않는다.
3. 중간에 JSON 파일만 만들고 멈추지 않는다. 이번 사용자는 **JSON과 JPEG 미리보기 제작을 한 번에 명시적으로 요청**했다. 명세의 사용자 카피 승인 단계는 발행 승인을 위한 게이트로 유지하되, 승인 전에는 비발행용 **자동 미리보기 렌더 경로(`scripts/ci_render.py`)**를 우선 사용하고 JPEG로 변환한다. 자유 디자인 발행용 HTML을 승인 전 작성·확정하는 행위는 명세의 승인 규칙을 위반하지 않도록 구분한다. 사용자가 카드 문구를 승인한 뒤 자유 디자인 HTML·최종 렌더를 진행할 경우 그 상태를 분리해 보고한다. **미리보기 JPEG를 발행 승인된 최종 카드라고 표기하지 않는다.**
4. Preview/QA 명령은 저장소에서 확인한 실제 CLI를 사용한다. 예:
   - `python scripts/ci_render.py --ids COSMETICS-LABEL-07-CARD-DRAFT --out ci-out` (JSON 검증·자동 디자인·PNG)
   - 사용자 카드 문구 승인 후 자유디자인은 `python scripts/auto_design.py content/COSMETICS-LABEL-07-CARD-DRAFT --lang ko --out content/COSMETICS-LABEL-07-CARD-DRAFT/ko --production`으로 출발하고, 카드별로 편집
   - `python scripts/qa_render.py --html-dir content/COSMETICS-LABEL-07-CARD-DRAFT/ko --source content/COSMETICS-LABEL-07-CARD-DRAFT/blog.md --out content/COSMETICS-LABEL-07-CARD-DRAFT/out/ko` (QA)
   - `python scripts/design_review.py content/COSMETICS-LABEL-07-CARD-DRAFT`, `python scripts/marketing_review.py content/COSMETICS-LABEL-07-CARD-DRAFT`, `python scripts/validate_distribution.py content/COSMETICS-LABEL-07-CARD-DRAFT`
   명령과 실제 출력 폴더는 `--help`/스크립트를 확인해 유효한 옵션만 실행한다.
5. **JPEG 변환**: QA가 PASS인 1080×1350 PNG를 이용해 Pillow로 `RGB` 변환 후 `JPEG quality=95, subsampling=0, optimize=True`로 동일 크기 개별 `card_NN.jpg` 생성. 카드는 JPEG 생성 후 다시 눈으로 읽어 압축으로 인한 글자 깨짐·잘림이 없는지 확인한다. 총 장수·각 1080×1350·RGB·파일 정상 열림을 검증한 후 ZIP 생성. **PNG는 QA 원본으로 보존**, JPEG를 전달용으로 우선 제공.
6. 이미지의 시각 검토를 수행하고 `sheet-270.png`와 `review.md`에 미완료/완료를 구분한다. 코드/색/폰트/QA 게이트는 변경하지 않는다. `content/COSMETICS-LABEL-07-CARD-DRAFT/`만 변경하며 작업 브랜치에 커밋·PR 생성. 이미 승인된 `content/`·`main`은 사용자 허락 없이 덮어쓰거나 병합하지 않는다.

## 최종 보고 형식

- 작성된 카드 장수 및 `card-data.ko.json` 위치
- 실제로 완성된 **JPEG 개별 파일·ZIP** 위치와 열기/다운로드 가능한 링크. 이미지/파일이 만들어지지 않았으면 완료라고 말하지 않는다.
- PNG, 축소 시트, QA 결과, 실패/경고와 미해결 법률·카피·최종 인간 검토 항목
- PR 링크와 변경된 파일 경로. `approvedBy` 상태와 실제 완료 상태를 솔직하게 기재.
