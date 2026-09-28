# ETHOS 카드뉴스 Codex 킷 v1.0

Codex(또는 다른 코딩 에이전트)가 승인된 블로그 원문에서 카드뉴스를 만들 때 쓰는 지침·검사 세트.
핵심 원칙: **블로그 원문을 한 번 입력하면 같은 사실 구조의 국문·영문 카드를 만들고, 실패하면 빌드가 멈추게 한다.**

## 구성
```
AGENTS.md                  에이전트 진입점 (작업 순서·절대 규칙·중단 조건)
docs/editorial.md          카피·Hook·서사·CTA·Authority
docs/html-contract.md      카드 HTML 계약(data- 속성)
docs/brief-template.md     승인 전 brief.md 양식
brand/ tokens.json|css, fonts.css     브랜드 값 (단일 출처)
fonts/                     로컬 폰트(서브셋 woff2, OFL)
templates/                 프레임·카드 유형 CSS, 카드 스켈레톤
gates.json                 검사 기준(숫자) — 초기 가설
scripts/qa_render.py       게이트 검사 + 통과 시에만 PNG 렌더
schema/card-data.schema.json
examples/                  good(통과) / bad(일부러 위반) 예시
references/                v3.3 참고 지침·승인 Golden Reference·manifest
tests/run_gate_tests.sh    게이트 회귀 테스트
```

## Codex에서 원문만 넣어 시작하기
채팅에 승인된 블로그 원문을 붙여 넣고 “국문·영문 카드뉴스로 만들어줘”라고 요청한다. Codex는 `content/<ID>/blog.md`를 만들고, 공통 brief와 언어별 card-data를 작성한 뒤 카피 승인 단계에서 멈춘다. 승인 후 `ko/`, `en/` HTML과 각각의 PNG·QA 보고서, 게시용 `distribution.md`를 만든다.

## 설치·실행
```
pip install -r requirements.txt && playwright install chromium
bash tests/run_gate_tests.sh                       # 게이트 동작 확인 (good PASS / bad FAIL)
python scripts/qa_render.py --html-dir content/GAME-KR-06 --source content/GAME-KR-06/blog.md --out content/GAME-KR-06/out
```
통과 시 `<--out>/png/`, `<--out>/sheet-270.png`(폰 크기 미리보기), `<--out>/qa-report.md` 생성. 실패 시 PNG 없음, exit 1.
(콘텐츠 작업: `--html-dir content/<ID> --source content/<ID>/blog.md --out content/<ID>/out`)

## GitHub 리포로 쓰기 (권장)
이 폴더 전체를 리포 루트로 올린다(폴더 구조 유지). Codex 클라우드 환경 설정(확인 필요):
- Setup script: `pip install -r requirements.txt && playwright install chromium`
  (에이전트 실행 중에는 인터넷이 막힐 수 있으므로 설치는 setup 단계에서. 폰트는 이미 리포에 들어 있다.)
- 작업 요청 시 `content/<ID>/` 를 지정한다. 결과는 브랜치·PR 로 받는다.

## 프로젝트 폴더에 놓는 위치
이 킷을 Codex 작업 repo 루트에 그대로 두고, 원문을 `source/blog.md` 로 넣는다. Codex 는 루트의 `AGENTS.md` 를 먼저 읽도록 설정한다
(자동으로 읽는지는 사용 중인 Codex 버전에서 확인).

## 자동으로 못 잡는 것 (사람이 확인)
법령 해석의 정확성 · 「또는/그리고」 뉘앙스 보존 · 폰 크기에서의 실제 읽힘 · CTA 문구 · 한 장 한 메시지.
`qa-report.md` 하단 체크리스트에 매번 출력된다.

## 알려진 한계 / 보정 필요
- `gates.json` 의 숫자(글자 수 180, 본문 채움 0.4, 하단 여백 48px 등)는 **초기 가설**이다. 실제 발행 후 성과와 실측으로 보정한다.
- 대비 검사는 단색 배경 기준(그라데이션은 금지). 배경 이미지·사진 카드는 별도 규칙이 필요하다.
- 정사각(540×540)만 지원한다. 4:5 세로가 필요하면 `tokens.json`·`gates.json`·`base.css` 를 함께 바꿔야 한다.
- 예시 카드 3장은 지침 검증용이며, 세트 전체(6~10장) 예시는 `examples/card-data.example.json`(카피 스키마 예시)만 제공한다.
- 아랍어 RTL 은 이 킷에 포함되지 않았다.
