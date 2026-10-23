# 카드 디자인·자연스러운 글쓰기 개선 인계인수

작성일: 2026-10-21 (KST). 구현·콘텐츠 기준 커밋: `fb61d235fdddf5a68d04ac69c11d7d54bfd61af8`.
이 문서는 작업 이력과 재개 지점이다. 새 작성 규칙의 정본이 아니며, 현재 사용자 요청과 최신 `AGENTS.md`의 작업별 명세를 우선한다.

## 0. 채널별 시리즈 제목 노출 정책 (2026-10-23)

- 블로그와 웹사이트 관리자 제목(`title`·`titleEn`)에는 정식 시리즈명과 회차를 표시한다.
- 카카오톡 채널과 LinkedIn 게시문의 제목·첫 줄에는 시리즈명·회차 머리표를 표시하지 않는다.
- 시리즈 관계는 내부 콘텐츠 ID·파일명·배포 기록으로 유지한다. 일반 채팅 출력과 다른 SNS의 기존 규칙은 이번 변경 대상이 아니다.
- 정본은 `docs/blog-authoring-spec.md`, `docs/website-md-spec.md`, `docs/sns-authoring-spec.md`다.

## 1. 앞으로 만드는 카드에 적용되는 범위

**최신 main의 공통 제작 코드·지침을 사용하는 새 작업에는 공통 개선이 적용된다. OEM 전용 디자인·문구까지 자동으로 복제되지는 않는다.** GitHub 연결만으로 다른 채팅의 구버전 파일이 자동 갱신되는 것은 아니다. 다음 담당자는 최신 main과 해당 명세를 실제로 읽는다.

| 구분 | 완료한 개선 | 다음 카드에서의 적용 |
|---|---|---|
| 공통 렌더러 | 막대 비율 정확화(0 포함), 명시적 표지 의도 반영, 순서 없는 항목의 불필요한 번호 제거 | 해당 공통 빌더를 사용하면 적용. 기존 승인 HTML을 일괄 재생성하지 않음 |
| 공통 가독성 | production 자동 글자 축소 대신 넘침 측정, 긴 헤더의 줄바꿈 처리 | 새 제작 코드 경로에 적용. 넘침은 문구·배치·분할을 검토해 해결 |
| 공통 문체 | 실제 작성 예시를 윤문 입력에 연결, 앞뒤 문맥·독자 행동·구체적 업무 중심 편집, 검수 상태와 방법 분리 | 작성 지침 및 도구 입력에 적용. 자연스러운 글을 자동 보장하는 기능은 아님 |
| 공통 CI | JSON 외 CSS·HTML 변경도 세트 선택, 기존 승인/자유 디자인 HTML 보존 및 카피 잠금 검사 | 해당 변경이 있으면 CI에서 실제 세트 검사 |
| 별도 초안 비교 | 원본 SHA-256 보호, 조건별 원문/국영 카드 발췌 추적, JSON 문량 비교 | `scripts/editorial_compare.py`를 담당자가 실행. 모든 세트에 자동 호출되는 CI 단계는 아직 아님 |
| OEM 전용 | 23~25px 국문 법률 본문, 전용 행·두 갈래·누적 조건 배치, 법률 설명 분할 | `COSMETICS-OEM-04-READABILITY-DRAFT` 안에만 존재. 다른 주제에는 적합성을 보고 선택적으로 재사용 |

공통 지침은 [언어 품질 워크플로](docs/language-quality-workflow.md), 카드 작업 진입점은 [Codex 제작 절차](docs/card-codex-production.md)와 [카드 작성 명세](docs/card-authoring-spec.md). OEM의 글자 크기·구도·카드별 문량을 새 강제 기준으로 승격하지 않는다.

## 2. 완료 이력

| 커밋 | 작업 |
|---|---|
| `779d5c7` | 카드 가독성·문맥을 포함한 글쓰기 개선. 당시 승인 카피 보존 |
| `889775a` | 디자인만 바뀐 세트의 CI 렌더 누락 수정, 측정 결과 기록 |
| `6e9e6f9` | 긴 헤더 정렬과 CI의 기존 승인 레이아웃 보존 |
| `4f78872` | OEM 별도 블로그·국영 카드 초안, 전후 실제 렌더, 법률 감사, 비교 도구·테스트 추가 |
| `fb61d23` | 최종 메타데이터 스키마 수정, 추가 테스트를 CI의 unittest 방식으로 변환 |

글·카드·법률 에이전트 3명이 분담했다. 주 담당자가 HTML/CSS·렌더·전후 비교·통합 검증을 맡았고 카드 에이전트가 실제 이미지도 독립 확인했다. 다음에도 복잡한 작업은 파일 소유 범위를 나누고 최종 통합자가 검토한다. 단순 문서 수정까지 의무적으로 분업하지 않는다.

## 3. 산출물과 원본 보호

- 보호 원본: `content/COSMETICS-OEM-04/`. 이번 별도 초안 작업에서 **55개 파일의 SHA-256 일치**, 기준 커밋 대비 폴더 diff 0건 확인.
- 별도 초안: [COSMETICS-OEM-04-READABILITY-DRAFT](content/COSMETICS-OEM-04-READABILITY-DRAFT/).
- [블로그](content/COSMETICS-OEM-04-READABILITY-DRAFT/blog.md): 기존 인물·사례만 사용해 20곳 부분 편집. 숫자·조문·인용 목록과 CTA부터 태그 끝까지 보존. [전후 문장·이유](content/COSMETICS-OEM-04-READABILITY-DRAFT/blog-edit-notes.md).
- 국영 카드 각 10장: 기존 3→새 3·4(검사 생략/남는 의무), 기존 7→새 7·8(제출 원칙/영업비밀 조건). 기존 4·5는 새 5로 통합하고 기존 8의 법정 의무 불변은 새 2 결론으로 이동.
- [전체 실제 렌더 비교](content/COSMETICS-OEM-04-READABILITY-DRAFT/comparison/index.html), [법률 설명 비교 PNG](content/COSMETICS-OEM-04-READABILITY-DRAFT/comparison/legal-before-after.png), [검사 설명 비교 PNG](content/COSMETICS-OEM-04-READABILITY-DRAFT/comparison/testing-before-after.png). HTML 비교는 저장소를 내려받아 로컬 브라우저에서 연다.
- [상세 검수·재현 명령](content/COSMETICS-OEM-04-READABILITY-DRAFT/review.md), [법률 독립 감사](docs/reviews/2026-10-21-oem-legal-audit.md), [조건 추적 JSON](content/COSMETICS-OEM-04-READABILITY-DRAFT/condition-map.json).

**새 OEM 세트는 미승인 비교 초안이다.** `editorialReview`의 실제 완료 단계는 pass지만 `approvedBy`는 없다. 이번 인계 요청으로 승인·발행 상태를 바꾸지 않는다. 보호 원본도 기존 메타데이터 상태를 그대로 보존했다. 비교용 승인 전 렌더는 사용자가 이번 작업에서 명시적으로 요청한 범위이며, 모든 후속 작업의 승인 절차를 없앤 것이 아니다.

## 4. 객관적 측정과 검증 범위

| 지표 | 기존 → 새 초안 |
|---|---|
| 블로그 문자 수(LF, 공백 포함) | 10,241 → 10,399 |
| 블로그 문자 변경률 | 3.76%, SequenceMatcher `autojunk=False` |
| 국문 카드 한 장 최대 JSON 카피 문량 | 234 → 192자, −17.9% |
| 영문 카드 한 장 최대 JSON 카피 문량 | 458 → 410자, −10.5% |
| 국문 카드 전체 JSON 카피 문량 | 1,462 → 1,551자, +6.1% |
| 국문 법률 본문 실제 크기 | 22 → 23~25 CSS px |
| 영문 법률 본문 실제 크기 | 21 → 21~23 CSS px |
| 동일 환경 실제 렌더 | 기존/새 국영 총 40장 하드 QA 통과, 새 20장 자동 축소 없음 |

문량은 공개 JSON 카피 필드의 공백 포함 문자 수이며 필드 사이 연결 문자를 제외한다. 렌더 QA의 공백 제외 수치와 혼용하지 않는다. 전체 카피는 조건을 명시해 증가했고 한 장의 최대 부담은 줄었다. **문량·변경률·QA 통과는 자연스러움·독자 이해도·전환율 개선 점수가 아니다.** 실제 독자 선호나 성과 실험은 하지 않았다.

법률 담당자는 2026-10-21 현행 1차 법령을 확인한 뒤 블로그 L01~L15 및 카드의 해당 주제 범위를 의미 대조했다. 확인 판본·조문·미확인 세부는 법률 감사에 기록했다. AND/OR, 예외 범위, 의무/재량, 무료/유료 구분을 보존했다. CGMP·판매 후 법정 보고 상세 등은 블로그에 남으며 모든 블로그 설명을 카드에 옮긴 것은 아니다. 조건 추적 JSON의 15항목은 법률 감사 L01~L15와 별개다. 정확 발췌의 존재만으로 법률 의미 보존을 판정하지 않는다.

국문은 사실·법률 검토 뒤 설치된 humanize-korean 규칙을 직접 적용하고 의미를 재검증했다. 이번 OEM 작업에서 upstream 전체 파이프라인이나 유료 API를 실행했다고 주장하지 않는다.

## 5. 테스트·원격 CI 확인 결과

아래는 **구현 기준 커밋 fb61d23**의 확인 결과다. 이후 문서 커밋의 실행 결과와 혼동하지 않는다.

- 로컬 pytest 수집 209개 통과(기존 의존성 deprecation 경고 4개). CI 호환 수정 후 unittest 전체 208개 통과, 건너뜀 없음. 수집 방식 차이를 구분한다.
- `design_freeze.py` 통과. 고정된 공통 디자인·지침 파일의 지문 일치.
- [원격 카드 회귀 통과](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39508871826).
- [원격 카드 렌더 통과](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39508871620).
- [원격 문체 힌트 실행 통과](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39508871643). 문체의 자동 품질 인증을 뜻하지 않는다.
- [링크 검사 실패](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39508871628): `research/STARTUP-VISA-D10-2-D8-4.md`의 기존 OASIS 주소 2곳, 외부 사이트 TLS 인증서 만료. OEM 새 링크 오류는 아니며 인증서 검증 완화나 검사 제외로 숨기지 않았다.

첫 푸시에서 발견된 오류는 수정 완료: `languageMethod` 자유 문자열을 허용 enum으로 변경, 사용하지 않는 1개짜리 `art` 배열 제거, pytest 의존 테스트를 unittest로 전환. 공개 카피·비교 이미지에는 변화 없음.

## 6. 남은 일과 재개 순서

| 우선 | 남은 일 | 처리 기준·종료 조건 |
|---|---|---|
| 발행 전 | OEM 초안에 대한 사용자의 채택·수정·발행 결정 | 현재는 미승인 유지. 명시적 결정 뒤에만 승인 상태와 발행 절차 진행 |
| 발행할 경우 | 채널별 캡션·alt text·배포안 등 발행 패키지 준비 | 최신 채널 명세와 Source Lock으로 작성·검증. 비교 초안을 그대로 게시한 것으로 취급하지 않음 |
| 운영 결함 | OASIS 외부 인증서 만료 | 사이트 복구 후 재검사하거나 동일 공식 자료의 유효한 대체 주소를 실제 확인. 임의 URL 교체·TLS 우회 금지 |
| 선택적 개선 | 영문 8번의 많은 설명량, 국문 2번 두 열의 줄바꿈 | 현재 넘침·가림 없음. 독자 피드백이나 구체적인 가독성 문제가 있을 때 해당 부분만 개선. 조건 삭제·전면 재작성 불필요 |
| 향후 성과 확인 | 실제 독자 이해·저장·문의 품질 | 발행·측정이 승인되면 기존 성과 학습 절차 사용. 아직 개선율을 주장하지 않음 |

공통 컴포넌트로 OEM 디자인을 추가하거나 비교 도구를 모든 CI에 자동 연결하는 작업은 이번에 하지 않았다. 실제 다른 주제에서 재사용 필요가 확인되면 별도 범위로 검토한다. 기존 카드 전체 재렌더·자동 윤문·예약 발행·주기 모니터링도 설정하지 않았다.

## 7. 다음 담당자 시작 방법

1. 최신 main과 `AGENTS.md`의 해당 작업 경로를 확인한다. 이 인계 파일은 상태 요약으로 사용한다.
2. 새 카드라면 승인된 해당 블로그를 Source Lock으로 사용한다. OEM 사실·사례·서비스를 다른 주제에 복사하지 않는다.
3. 기존 원고 개선 비교라면 별도 폴더를 만들고 **수정 전에** 해시 스냅샷을 만든다. `condition-map.json`은 OEM 예시의 구조를 참고하되 현재 원문과 새 카드를 실제로 대조해 작성한다.

```bash
python scripts/editorial_compare.py --baseline content/<원본ID> --draft content/<초안ID> --initialize
python scripts/editorial_compare.py --baseline content/<원본ID> --draft content/<초안ID>
python scripts/ci_render.py --ids <초안ID>
python -m unittest discover -s tests -p "test_*.py"
```

Windows에서는 `PYTHONUTF8=1`을 설정한다. 로컬 환경에 RTK 규칙이 있으면 명령 앞에 `rtk proxy`를 붙인다. 위 비교 명령은 초안의 언어별 JSON과 조건 매핑을 읽으며 원본 해시 스냅샷을 덮어쓰지 않는다.

4. 법률 확인 → 필요한 문장 윤문 → 의미 재대조 → 같은 환경의 실제 렌더 비교 순서로 진행한다. 조건을 나눌 때 한 장만 공유해도 면제·선택 조건으로 오독되지 않는지 확인한다.
5. 검수 기록은 실제 완료 상태와 방법을 구분한다. 새 `languagePass`는 pass/pending, 완료 방법은 스키마의 `humanize-korean`/`manual-equivalent`/`english-localization` 중 실제 방법으로 기록한다. 자세한 방법은 검수 메모에 쓴다.
6. 새 원고·기존 승인본·검수 기록을 구분해 커밋하고, 푸시한 정확한 커밋의 CI 결과를 확인한다. 자동 QA와 실제 디자인 완성, 편집 완료와 사용자 승인을 구분한다.
