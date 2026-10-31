# ETHOS 콘텐츠 운영체계 + 카드뉴스 Codex 킷

이 저장소는 에토스 행정사사무소의 블로그·SNS·홈페이지·카드뉴스 지침을 관리하는 단일 기준본이다. 기존 카드뉴스 제작·렌더·QA 시스템은 그대로 유지한다.

최근 카드 디자인·글쓰기 개선의 적용 범위, 완료 작업, 검증 결과와 남은 일은 [인계인수 문서](HANDOFF.md)에 정리되어 있다. 작업 규칙은 아래 정본 지침을 따른다.

## 콘텐츠 지침 진입점

1. `MANIFEST.md`에서 현재 Active 지침과 적용 순서를 확인한다.
2. `guidelines/core/`의 공통 원칙을 적용한다.
3. 요청에 맞는 `guidelines/channels/` 파일 하나를 선택한다.
4. 주제에 필요한 `guidelines/modules/`만 추가한다.
5. ChatGPT 프로젝트에는 `PROJECT_INSTRUCTIONS.md`의 짧은 부트스트랩만 복사하고, 동일 지침 파일을 중복 업로드하지 않는다.

카드 제작 여부와 채널 패키지는 `docs/card-selection.md`, `docs/channel-packaging.md`에서 정한다. 게시용 한국어는 `docs/language-quality-workflow.md`의 분리된 초안·검증·마케팅·금지 표현·윤문·의미 재검증 순서를 따른다. 자연스러움 점수는 권고지만 윤문과 의미 재검증의 실행 기록은 필수다. 발행 후 개선은 `docs/performance-learning.md`를 따른다.

소재를 새로 발굴할 때에는 `docs/topic-discovery.md`를 먼저 사용한다. 최신 에토스_글감관리표.xlsx가 프로젝트 소스나 첨부 파일로 제공되면 `docs/topic-log-integration.md`도 함께 적용해 발행 중복, 반복 상위 노출, 실제 문의 유입, 갱신 필요성을 확인한다. 신사업 인허가·국제화라는 넓은 브랜드 안에서 분류 경계, 제도 교차, 순서 의존성, 문서 정합성, 반복 관리 가능성이 있는 구체적인 질문을 찾고, 그 뒤 블로그·SNS·카드뉴스 형식으로 나눈다.

블로그를 SNS로 바꿀 때에는 `docs/social-repurposing.md`로 한 질문과 한 행동만 추출하고, `docs/ethical-persuasion.md`로 과장 없는 전환 구조를 점검한다.

GitHub 연결은 자동 동기화로 간주하지 않는다. ChatGPT에서 콘텐츠 작업을 시작할 때마다 `MANIFEST.md`와 필요한 Active 파일을 실제로 조회한다. 연결을 사용할 수 없는 환경에서는 구버전 파일을 임의로 섞지 않는다.

검증:

```bash
python scripts/validate_guidelines.py
```

## Claude Blog 오픈소스 통합 (선택형)

[claude-blog](https://github.com/AgriciDaniel/claude-blog) v2.3.1을 MIT 라이선스의 Git 서브모듈 `vendor/claude-blog/`로 연결했다. 블로그 조사·SEO/GEO 진단·개요·다국어 작성용 보조 엔진이며, **에토스의 법률 검증·Source Lock·한국어 문체·채널별 산출물·승인 규칙을 대체하지 않는다.** 기존 카드 렌더·QA와 승인 원고는 변경하지 않는다.

```bash
git submodule update --init vendor/claude-blog
claude --plugin-dir ./vendor/claude-blog
```

Claude Code의 프로젝트용 `/ethos-blog` 스킬도 `.claude/skills/ethos-blog/SKILL.md`에 제공한다. 서브모듈을 초기화하지 않으면 원본 스킬·스크립트를 실행할 수 없으며, GitHub 연결만으로 자동 설치·실행되는 것은 아니다. 자세한 사용법, 원본 커밋, 라이선스, 외부 API·개인정보 제한은 [연동 안내](docs/claude-blog-integration.md)를 따른다.

## 선택형 한국어 통독·윤문 (Human Proofreader MCP)

기존 `im-not-ai` 및 `Prose hints`를 유지하며, 문단 흐름·반복 설명 진단이 필요한 공개용 국문 원고에만 Solar Human Proofreader를 선택적으로 사용한다. **Codex 토큰 없이도** 표준 Python CLI 또는 동의를 받는 수동 GitHub Action으로 실행할 수 있다. 외부 전송·보수 교정·원문 대조·변경률 30% 기준과 법률 의미 재검증은 [사용 안내](docs/human-proofreader-integration.md)를 따른다. 자동 원고 수정·PR 댓글·발행은 하지 않는다.

---

# 카드뉴스 Codex 킷 v1.0

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
scripts/validate_distribution.py  카드별 alt text·외부 자산 출처 검사
schema/card-data.schema.json
examples/                  good(통과) / bad(일부러 위반) 예시
references/                v3.7 운용지침·v3.3 제작표준·승인 Golden Reference·manifest
tests/run_gate_tests.sh    게이트 회귀 테스트
```

## Codex에서 원문만 넣어 시작하기
채팅에 승인된 블로그 원문을 붙여 넣고 “국문·영문 카드뉴스로 만들어줘”라고 요청한다. Codex는 `content/<ID>/blog.md`를 만들고, 공통 brief와 언어별 card-data를 작성한 뒤 카피 승인 단계에서 멈춘다. 승인 후 `ko/`, `en/` HTML과 각각의 PNG·QA 보고서, 게시용 `distribution.md`를 만든다.

파일로 받은 원문은 아래처럼 작업 폴더를 먼저 만들 수 있다.

```bash
PYTHON=python PYTHONUTF8=1 python scripts/new_content.py --id GAME-2026-01 --source blog.md
PYTHON=python PYTHONUTF8=1 python scripts/validate_bilingual.py content/GAME-2026-01
PYTHON=python PYTHONUTF8=1 python scripts/marketing_review.py content/GAME-2026-01
PYTHON=python PYTHONUTF8=1 python scripts/validate_distribution.py content/GAME-2026-01
```

미감과 마케팅 점수는 렌더를 막는 절대 규칙이 아니라 권고다. `references/ethos-card-design-v3.7.md`, `docs/layout-playbook.md`와 Golden Reference를 기준으로 구도를 고르고, 사실·폰트·프레임·오버플로 같은 무결성 검사만 하드 게이트로 유지한다. 카드 유형 수나 `checklist`·`process` 사용 여부만으로 합격·실패를 정하지 않는다.

## 오픈소스 구성

- Playwright: 고정 Chromium 환경에서 HTML/CSS 카드 렌더
- Pillow: PNG 크기 확인, 축소 시트, 시각 회귀 비교
- JSON Schema / jsonschema: 국·영문 카드 데이터 구조 검사
- lychee-action: 문서와 출처 URL의 정기 무결성 검사
- Vale: 에토스 전용 금지 표현·직접 연락 유도 표현의 비차단 검사
- CSpell: 영문 카드·캡션의 선택적 오탈자 검사

재현 가능한 결과를 위해 검증한 버전을 `requirements.txt`에 고정한다. 별도 디자인 프레임워크는 넣지 않는다. 프레임워크 기본 컴포넌트가 ETHOS의 편집 디자인을 획일화할 수 있기 때문이다.

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
- 1:1과 인스타그램 4:5를 지원한다. 한 세트에서는 한 비율만 사용한다.
- 예시 카드 3장은 지침 검증용이며, 세트 전체(6~10장) 예시는 `examples/card-data.example.json`(카피 스키마 예시)만 제공한다.
- 아랍어 RTL 은 이 킷에 포함되지 않았다.
