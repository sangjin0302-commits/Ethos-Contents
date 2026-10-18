# COSMETICS OEM 04 카드 디자인 인계

작성일: 2026-10-18. 사용자가 현재 단계에서 작업을 마무리하고, 남은 개선은 다음에 진행하도록 요청했다. 추가 디자인 작업이나 자동 모니터링을 시작하지 않는다.

## 현재 상태

- 최종 디자인 커밋: `53915acd9cfcccdac8d29ab50e5745a39a158877` (`53915ac`), main에 푸시 완료.
- 국문 10장·영문 10장. 아랍어는 작업 대상에서 제외.
- 실제 1080×1350 PNG 20장과 전체 미리보기 저장 완료.
- 이번 최종 수정에서는 `card-data.ko.json`, `card-data.en.json`, `blog.md` 문구를 바꾸지 않았다. 영문 7장은 HTML의 의미 단위 묶음만 추가했다.
- 사용자 발행 승인은 별도다. `approvedBy`의 승인 대기 상태를 임의로 바꾸거나 SNS에 게시하지 않는다.

## 다음 담당자가 먼저 볼 파일

이 파일 기준 상대 경로다.

| 목적 | 파일 |
|---|---|
| 국문 전체 확인 | [out/ko/sheet-270.png](out/ko/sheet-270.png) |
| 영문 전체 확인 | [out/en/sheet-270.png](out/en/sheet-270.png) |
| 원본 PNG | `out/ko/png/card_01.png`부터 `card_10.png`, 영문은 `out/en/png/` |
| 잠긴 문구 | [card-data.ko.json](card-data.ko.json), [card-data.en.json](card-data.en.json) |
| Source Lock | [blog.md](blog.md) |
| 세트 전용 스타일 | [design.css](design.css) |
| 직접 디자인한 HTML | `ko/card_01.html`부터 `card_10.html`, 영문은 `en/` |
| 설계·검수 기록 | [wireframe.txt](wireframe.txt), [review.md](review.md) |
| 최신 제작 규칙 | [카드 작성 명세](../../docs/card-authoring-spec.md), [디자인 가이드](../../docs/card-design-guide.md), [HTML 계약](../../docs/html-contract.md) |
| 기존 평가 기준 | [card-evaluation-rubric.md](../../docs/card-evaluation-rubric.md) |

`review.md`는 작업 이력이 누적된 파일이다. 맨 위의 최신 수정 기록이 아래의 이전 설명보다 우선한다.

## 완료된 개선

1. **푸터 겹침 제거**: 공통 `templates/base.css`에서 숫자와 진행바 사이 8 CSS px 확보. 4px 트랙과 채움 위치 일치. 국·영문 각 1~10장 회귀 검사 추가.
2. **화장품 표지**: 범용 클립보드 대신 펌프 용기·크림 단지·품질기록 SVG 사용. 원본은 `assets/illustrations/objects/cosmetics-oem.svg`. 최신 수정에서는 칩 테두리·장식 밑줄·무거운 결론 박스를 없앴다.
3. **영문 7장**: 본문 21px, 제목 30px 한 줄. 예외의 세 판단 요소를 `.legal-factor`로 구분했다. 설계·개발·생산 방식, 품질·안전 영향, 계약상 영업비밀 범위와 접속사·문장부호를 모두 보존했다.
4. **반복 배치 완화**: 2장은 제조업체와 책임판매업자 책임을 나란히 비교한다. 6장은 변경 전후를 열린 연결선 구조로 표시한다. 3장의 조건 패널과 다른 구도다.
5. **CTA 위계 정리**: 10장 준비자료·우선 검토 설명은 크림 바탕에 네이비 글자. 마지막 무료 사전 검토 안내만 네이비 채움 강조. 새 서비스·성과·처리기간·버튼·연락처는 추가하지 않았다.

## 검증 결과

디자인 커밋 `53915ac` 기준이다. 이 인계 문서만 추가하는 커밋의 검증 결과와 혼동하지 않는다.

- 로컬 전체 테스트: **185 passed**, 실패·건너뜀 없음. 의존성 폐기 예정 API 경고 4개.
- 실제 카드 QA: 국문·영문 모두 PASS. 20장 모두 `fitScale=1.00`, `fitOverflow=0`.
- 카피 검사: WARN 0 / INFO 11. 한영 구조·출처 추적, 배포 자료·자산 출처 검사 통과.
- 공통 시각 회귀: 기준 PNG 5장 변화 0.000%, 통과. 이번에는 기준 이미지를 갱신하지 않았다.
- 장문·최대 분량 스트레스: 카드 조합 14개와 OG 8개, 총 22개 통과.
- GitHub CI 세 작업 모두 성공:
  - [Render cards](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39112223203)
  - [Link integrity check](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39112223206)
  - [Card system regression check](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39112223181)
- 문구 데이터가 바뀌지 않아 해당 커밋에서는 Prose hints 작업이 새로 실행되지 않았다. 이를 네 작업 성공으로 보고하지 않는다.

자동 QA 통과와 시각적 완성도는 다르다. 전체 시트와 수정 카드 원본을 실제로 열어 확인했다. 이 작업에서 외부 법률 원문을 새로 검증한 것은 아니다.

## 남은 개선과 우선순위

아래는 다음 요청 때 검토할 후보이며 현재 실패나 즉시 수정 명령이 아니다. 사용자는 지금 중단을 요청했다.

### 1 영문 2장 모바일 가독성

2열 비교로 책임 차이는 선명해졌지만 영문 본문은 5~6줄이다. 현재 19px이며 축소되지 않는다. 실제 휴대전화 크기로 두 열을 오가며 읽기 편한지 확인한다. 불편하면 두 주체의 관계를 유지한 비대칭 배치나 넓은 행을 비교 시안으로 검토한다. 글자를 줄여 맞추거나 법적 업무 범위를 삭제하지 않는다.

### 2 영문 7장 정보량

400자·66단어로 권고 340자·60단어를 넘는다. 예외 문장의 필드 길이와 소제목 길이 권고도 남아 있다. 현재는 조건을 세 묶음으로 나누고 21px 본문을 유지했다. 더 개선하려면 의미·조건을 보존한 문장 편집안을 먼저 검토한다. 문구 변경이 필요하면 JSON부터 수정하고 HTML 카피 잠금을 다시 확인한다. 장수는 현재 10장이므로 11장으로 단순 추가하지 않는다.

### 3 표지 및 CTA 후속 판단

장식 과잉은 정리됐지만 표지 설명·약속·결론의 의미 중복을 더 줄일 여지는 있다. 이번에는 문구를 그대로 유지했다. 다음에는 사용자가 문구 편집을 원할 때만 검토한다. CTA의 직접 준비와 사전 검토 범위, 무료 검토와 유료 작업 구분을 훼손하지 않는다.

### 4 그대로 남긴 권고

- 표지 main 블록 4개: 권장 3개 초과. 그림·질문·분류·설명이 실제로 읽히는지 기준으로 판단한다.
- 국문 7장 187자: 권고 180자 초과. 조건 삭제 금지.
- 8장: 의도적인 쉼 카드의 여백·줄 수·내용 중심 편차 권고. 수치만 낮추려고 내용이나 장식을 추가하지 않는다.
- 영문 10장 345자: 권고 340자 초과. 준비자료·검토 범위 보존.
- 기타 카피 INFO는 `copy_lint.py` 결과를 참고한다. 권고를 0으로 만드는 것이 목표는 아니다.

## 재시작 시 주의

- 최신 main을 먼저 조회하고 이 인계 이후 변경이 있는지 확인한다. 사용자 파일을 초기화하거나 덮어쓰지 않는다.
- **`auto_design.py --production`을 기존 HTML에 무조건 다시 실행하지 않는다.** 영문 7장의 수동 `.legal-factor` 묶음이 생성기 출력에는 없으므로 사라진다. 자유 디자인 HTML은 현재 저장본이 정본이다. 재생성이 필요하면 별도 임시 위치에 만들고 수동 변경을 비교·이식한다.
- 표지·CTA의 일부 장식 비표시는 CSS에서 처리했다. 텍스트를 숨긴 것이 아니다. 시각 강조를 되살리기 전에 `design.css` 마지막 editorial refinement 구역을 확인한다.
- 공통 프레임·게이트·한도 등 보호 파일 변경은 사용자 요청 범위를 확인하고 디자인 동결 절차를 따른다. 테스트 임계값을 낮춰 통과시키지 않는다.
- 한글 발행 문구를 고치면 프로젝트의 humanize-korean 최종 문체 검토를 적용한다. 새 법률 사실이 필요하면 Source Lock 원문 검증·승인부터 진행한다.
- 80점 평가는 **이번 네 가지 개선 이전 버전**의 자기평가다. 최종 `53915ac`에는 새 점수를 부여하지 않았다. 다음 평가는 실제 PNG와 기존 평가 기준으로 다시 수행한다. 이전 75점·90점대 주장을 재사용하지 않는다.

## 재검증 명령

저장소 루트에서 실행한다. Windows에서는 `PYTHONUTF8=1`을 설정한다. 현재 로컬 환경의 RTK 지침이 유지된다면 명령을 `rtk proxy`로 실행한다.

```powershell
$env:PYTHONUTF8="1"
python -m pytest -q
python scripts/copy_lint.py content/COSMETICS-OEM-04
python scripts/validate_bilingual.py content/COSMETICS-OEM-04
python scripts/validate_distribution.py content/COSMETICS-OEM-04
python scripts/design_review.py content/COSMETICS-OEM-04
python scripts/qa_render.py --html-dir content/COSMETICS-OEM-04/ko --source content/COSMETICS-OEM-04/blog.md --out content/COSMETICS-OEM-04/out/ko
python scripts/qa_render.py --html-dir content/COSMETICS-OEM-04/en --source content/COSMETICS-OEM-04/blog.md --out content/COSMETICS-OEM-04/out/en
python scripts/visual_regression.py
python scripts/spec_stress.py
```

출력 후 축소 시트와 수정 카드 원본을 함께 확인한다. 코드 변경을 푸시하면 해당 커밋 SHA의 CI를 끝까지 확인한다. 과거 커밋의 성공을 새 커밋 성공으로 보고하지 않는다.

## 로컬 전용 파일

인계 시점 로컬의 `_workspace/2026-10-18-001/`, `COSMETICS-OEM-04-design.zip`, `COSMETICS-OEM-04-final-cards.zip`, `marketing-report.md`는 추적되지 않은 파일이다. ZIP은 다운로드 편의용이며 GitHub 인계의 필수 자료가 아니다. 원본 PNG와 QA 보고서는 저장소에 있다. 이 파일들을 최신 정본으로 간주하거나 일괄 커밋·삭제하지 않는다.

## 다음 대화에서 사용할 요청

> 최신 main의 content/COSMETICS-OEM-04/HANDOFF.md를 읽고 이어서 진행해. 우선 영문 2장·7장을 실제 모바일 크기로 재평가하고, 법률 조건과 10장 구성을 유지하는 개선안을 검토해. 변경 전 현재 출력과 비교하고, 변경 후 실제 PNG·테스트·해당 커밋 CI까지 확인해.
