# claude-blog 오픈소스 연동 가이드 (ETHOS)

## 목적과 출처

- 원본: [AgriciDaniel/claude-blog](https://github.com/AgriciDaniel/claude-blog)
- 적용 버전: v2.3.1 (원본 `.claude-plugin/plugin.json` 기준)
- 고정 커밋: `354442348815a7f0327077ad89af2c43cf4b4ab4` (2026-10-14 기준 업스트림 `main`)
- 라이선스: MIT, Copyright (c) 2025-2026 AgriciDaniel. 원본 `LICENSE` 및 `NOTICE`는 서브모듈 내부에 보존된다.
- 배치: `vendor/claude-blog` — Git **submodule**(모드 `160000`)이며 복사된 스냅샷이나 자동 갱신 브랜치가 아니다.

블로그 작성, 재작성, 구조·SEO/GEO 진단, 콘텐츠 전략과 다국어 초안의 **선택형 실행 도구**로 활용한다. 기존 ETHOS 글쓰기 지침, 법률·윤리 검증, 카드뉴스 렌더러, 발행 승인 흐름은 그대로다. 플러그인의 100점 평가·90점 통과·AI 인용 준비도는 내부 품질 휴리스틱일 뿐 **한국 법률 정확성, 실제 검색 순위, AI 인용 성과 또는 발행 승인을 입증하지 않는다.**

## 로컬 최초 실행

새로 클론할 때:

```bash
git clone --recurse-submodules https://github.com/sangjin0302-commits/Ethos-Contents.git
cd Ethos-Contents
```

기존 작업 폴더에서는 저장소 루트에서:

```bash
git submodule update --init vendor/claude-blog
test -f vendor/claude-blog/.claude-plugin/plugin.json
claude --plugin-dir ./vendor/claude-blog
```

Claude Code와 Python 3.11+가 필요하다(기본 설치와 고급 도구·렌더 의존성은 원본 `vendor/claude-blog/docs/INSTALLATION.md` 참고). 마지막 명령은 **해당 세션에서만** 로컬 플러그인을 로드하며 전역 설치·유료 API 활성화·자동 게시를 하지 않는다. 프로젝트 자체에는 `.claude/skills/ethos-blog/SKILL.md`가 있어 `/ethos-blog` 진입점을 제공한다. 로드된 플러그인의 블로그 작업에는 원본의 `/blog` 명령을 사용할 수 있다.

원본의 `install.sh`·`install.ps1`를 무심코 실행하지 않는다. 이 설치 스크립트는 사용자 계정의 `~/.claude` 파일을 변경할 수 있어, 이 저장소에서는 `--plugin-dir`을 기본 경로로 사용한다. 일부 Claude Code 버전은 원본 플러그인 이름 `claude-blog`를 예약 이름으로 경고한다. 원본 `README.md`의 Known Issues를 확인하고, 로딩 여부를 검증한 뒤 사용한다. 오류가 나면 원본 파일을 임의로 덮어쓰지 말고 기록한다.

CI 또는 `git clone`에서 서브모듈을 내려받지 않았다면 GitHub에는 gitlink만 존재한다. 스킬·스크립트 파일이 로컬에서 보이지 않는 것은 정상이며 초기화가 필요하다. 원본 변경은 서브모듈 커밋 핀을 별도 PR에서 검토·수정할 때만 반영한다.

## ETHOS 선행 규칙: 충돌 시 반드시 이 순서

1. 현재 사용자 요청과 `MANIFEST.md`의 Active 지침
2. `docs/blog-authoring-spec.md`: 원고 작업 경로 A(기존 근거), B(새 법률 근거), C(승인 원문 파생); 국문 TXT·MD 납품 및 채널별 규칙
3. `docs/evidence-gate.md`, 승인된 `research/<시리즈>.md`, `docs/legal-verification.md` 및 필요한 채널 명세
4. `docs/tooling-policy.md`와 `docs/language-quality-workflow.md`: 필요한 때만 진단·윤문, 의미 재확인
5. `vendor/claude-blog/skills/`와 해당 파이썬 스크립트: 위 규칙과 충돌하지 않는 기술적 보조 기능에 한함

`Source Lock`: 승인된 `content/<ID>/blog.md`의 주체·범위·문서·조건·예외·수치·기한·인용은 변경하지 않는다. SNS·카드·웹사이트 파생은 승인 원문만 이용한다. 새 사실·판례·법령 정보는 공식 1차 근거와 기준일을 확인한 뒤 원문 보강과 승인을 거친다. 원본 스킬의 일반적인 SEO 최적화·마케팅 CTA·서구권 문체·JSON-LD 제안이 ETHOS 출처·표현·직역·광고 규칙과 충돌하면 적용하지 않는다.

## 추천 매핑

| ETHOS 작업 | 원본에서 필요할 때만 사용하는 도구 | 우선 확인할 ETHOS 파일 |
|---|---|---|
| 새 법률 글 조사·개요 | `blog-brief`, `blog-outline`, `blog-factcheck` | `docs/blog-authoring-spec.md`, `docs/evidence-gate.md` |
| 검증된 국문 원고 SEO/AI 검색 개선 | `blog-analyze`, `blog-seo-check`, `blog-geo` | `docs/blog-authoring-spec.md`, `docs/tooling-policy.md` |
| 콘텐츠 허브·갱신 진단 | `blog-cluster`, `blog-decay`, `blog-cannibalization` | `docs/content-architecture-system.md`, `docs/topic-log-integration.md` |
| 승인 원문 번역·채널 변환 | `blog-translate`, `blog-repurpose` | `docs/website-md-spec.md`, `docs/sns-authoring-spec.md`, 승인 원문 |

원고 자체는 ETHOS 명세대로 만든 뒤 필요할 때만 해당 분석을 추가한다. 도구 결과는 별도 제안·보고서로 남기며 승인본을 직접 덮어쓰지 않는다. 외부 SEO 점수 때문에 자동 재작성하거나 새로운 하드 게이트를 만들지 않는다.

## 외부 처리·보안·발행

- 외부 API(Google, Gemini, NotebookLM, 이미지 생성·텍스트 분석 등), 비공개 자료 전송, 유료 호출, 외부 게시를 기본 실행하지 않는다. 실제 데이터·계정·비용에 관계되는 작업은 사용자 승인과 비밀정보 최소화가 선행돼야 한다.
- 개인정보·상담 기록·수임 문서·비공개 사건 내용은 외부 플러그인, 프롬프트, 원격 API, 공개 GitHub PR 등에 입력하거나 업로드하지 않는다.
- 법률 숫자·조건·인용을 임의 생성하거나, 검증 실패를 툴의 합격 점수로 대체하지 않는다. 인터넷 연결 실패는 자료 진위 확인 성공과 같지 않다.
- 기존 카드 `gates.json`, `brand/`, `templates/`, `scripts/qa_render.py`와 `state/design-freeze.json`, 승인 `content/`는 자동 수정하지 않는다. 필요하면 별도 사용자 요청 및 승인 절차를 따른다.
- 이 변경은 플러그인과의 **저장소 연동**이다. 실제 Claude Code 설치·플러그인 로드·글 작성·CI 통과·서비스 발행을 실행한 것으로 간주하지 않는다.

## 검증

```bash
python scripts/validate_guidelines.py
python -m pytest -q tests/test_claude_blog_integration.py
git ls-files --stage vendor/claude-blog
git submodule status vendor/claude-blog
```

`git ls-files`에 `160000` gitlink와 고정 커밋이 보여야 한다. `git submodule status` 앞에 `-`가 있으면 로컬 미초기화 상태다. 원본의 전체 테스트를 실행하려면 서브모듈 초기화 후 원본 의존성을 별도로 설치해야 하며, ETHOS 검증과 혼동하지 않는다.
