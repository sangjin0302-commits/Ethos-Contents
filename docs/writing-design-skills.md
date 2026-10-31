# ETHOS 글쓰기·디자인 강화 스킬

> 2026-10-31 사용자 요청으로 채택. 기존 법률·브랜드·승인·카드 렌더 기준은 유지한다.

## 무엇을 언제 쓰는가

| 요청·결함 | 실행할 ETHOS 스킬 | 반영한 원본 | 기존 흐름에 붙이는 위치 |
|---|---|---|---|
| 글쓰기 강화, 도입·반복·문단 연결·결말 편집 | `ethos-editorial` | RampStack `content-and-copy` | 자연 초안 뒤 구조·내용 편집, 최종 윤문·의미 재검증 전 |
| 승인 시안의 장점 추출, 실제 디자인 참고자료 분석 | `ethos-design-reference` | `anydesign` | 실제 자료 관찰 → 기존 brief/design 메모 보강 |
| 카드 표지·대표 이미지·설명 도식의 콘셉트 | `ethos-art-direction` | RampStack `art-direction` | 승인 원문 근거의 시각 브리프 → 카피 승인 → 기존 제작·렌더·QA |

정본 실행 지침은 `.agents/skills/<이름>/SKILL.md`이며 `.claude/skills/<이름>/SKILL.md`는 이를 읽는 얇은 진입점이다. 세 스킬을 모든 작업에 연속 실행하지 않는다. 필요한 하나만 적용하고, 실제 결함이 해소되면 종료한다. 새 블로그 집필·SEO 분석은 기존 `docs/claude-blog-integration.md`를 유지한다. 문장 수준 윤문은 기존 ethos-humanize/im-not-ai 경로와 중복 재작성하지 않는다.

## 적용 우선순위와 보호 범위

현재 사용자 요청과 `MANIFEST.md`의 우선순위, 채널별 빠른 명세, `docs/evidence-gate.md`, `docs/language-quality-workflow.md`, `docs/tooling-policy.md`가 외부 스킬보다 우선한다. 각 원고의 경로 A/B/C와 사람 승인을 그대로 따른다.

Source Lock: 승인 원문의 주체·대상·의무/재량·조건·예외·숫자·기한·인용·서비스 범위는 고정한다. 새 법률 근거나 사례가 필요하면 공식 자료 확인과 원문 보강·승인으로 돌아간다. 외부 스킬의 예시 통계·가상 인용·비용 배수는 근거로 쓰지 않는다. 점수·일반 SEO 길이·최소문자 비율 때문에 조건을 지우거나 원고를 부풀리지 않는다.

좋은 도입·승인 제목·문체는 보존하고 필요한 부분만 고친다. 기존 네이버 TXT·MD 납품과 말미 순서, 웹사이트 frontmatter, SNS별 CTA 예외를 유지한다. 디자인은 `brand/tokens.css`, `brand/fonts.css`, 기존 프레임·템플릿·게이트를 사용한다. 추출한 외부 색·폰트·토큰은 참고 자료이지 정본이 아니다. 원문에 없는 인과·순서를 화살표로 만들지 않는다.

승인 콘텐츠, 공통 카드 렌더러, `gates.json`, `card-limits.json`, 스키마, `state/design-freeze.json`을 자동 변경하지 않는다. 새 초안·분석 메모는 별도 작업물에 남긴다. 새로운 필수 JSON 필드·하드 게이트·점수표·매번 작성해야 하는 보고서를 추가하지 않는다.

## 목록의 나머지 후보 반영

| 후보 | 반영 방식 | 가져오지 않은 부분 |
|---|---|---|
| `content-research-writer` | editorial에 근거를 유지한 도입부 소수 대안, 문단별 주장·근거·전환 피드백을 독자적으로 재구성 | 별도 집필 엔진, 예시 통계·인용, 원문 파일 복사, 무조건 반복 재작성 |
| `canvas-design` | art-direction에 표지·대표 이미지의 시각 중심·공간·최종 시각 검수 방법을 독자적으로 재구성 | 본문 카드 최소문자화, 원문·코드·폰트 복사, 의무 PDF/미학 선언 |
| `brand-guidelines` | 검토 결과와 제외 이유를 기록 | Anthropic 색·Poppins/Lora 글꼴을 ETHOS에 적용하지 않음 |
| `theme-factory` | 기존 ETHOS 프리셋 사용으로 역할을 대체 | 범용 외부 테마와 새 폰트·팔레트 자동 설치 |

추천 목록을 전부 자동 설치한다는 의미가 아니라, 각 후보의 채택·제한·제외 판단까지 반영한 구성이다. Composio 목록 자체를 하나의 허가된 배포물로 취급하지 않는다. 원문을 복사한 것은 별도 고지를 함께 둔 두 MIT 라이선스 파일뿐이고, 핵심 원본은 커밋 고정 gitlink로 연결했다. 어댑터는 해당 방법을 ETHOS에 맞게 수정했다.

## 사용과 초기화

ETHOS 어댑터 본문은 저장소에 들어 있으므로 원본 체크아웃 없이도 적용할 수 있다. 상세 원본 references와 AnyDesign 도구가 필요한 경우에만 저장소 루트에서 초기화한다.

```bash
git submodule update --init -- vendor/rampstack-skills vendor/anydesign
python scripts/check_writing_design_sources.py --require-checkout
```

이 명령은 원본을 고정 커밋으로 가져오고 선택 원본 파일의 지문을 확인한다. 플러그인 전역 설치, upstream installer/hooks 실행, 유료 API 설정, 원고 전송, 이미지 제작을 하지 않는다. 원본 상세 기능을 사용하기 전 실제 코드·의존성·입출력과 권한을 검토한다. AnyDesign의 '소스를 읽지 말고 실행' 지시는 이 저장소에서 채택하지 않는다. 미초기화 상태를 원본 설치·실행 완료라고 말하지 않는다.

Claude Code의 프로젝트 스킬 진입점:

```text
/ethos-editorial <원고 경로와 편집 요청>
/ethos-design-reference <실제 참고 이미지 또는 HTML 경로>
/ethos-art-direction <승인 원고·brief와 표지 기획 요청>
```

Codex는 `AGENTS.md`의 해당 작업 행과 `.agents/skills/` 정본을 따른다. 다른 도구에서 파일을 읽는 것은 호스트에 플러그인이 자동 설치된다는 뜻이 아니다. GitHub 연결만으로 자동 실행되지 않는다. 새 스킬이 보이지 않으면 호스트가 최신 저장소의 프로젝트 스킬을 읽었는지 확인하고, 로딩 여부를 검증하지 않은 상태에서 실행됐다고 하지 않는다.

## 출처와 보안

커밋·선택 파일 지문은 `vendor/writing-design/sources.json`, 저작권 고지는 `vendor/writing-design/README.md`와 두 LICENSE 파일에 있다. RampStack와 AnyDesign의 원본 LICENSE·references는 서브모듈에도 보존한다. 자동 업데이트하지 않으며 핀 변경은 별도 검토·테스트·PR로 처리한다.

원본 전체 저장소의 다른 스킬은 자동 활성화하지 않는다. 비공개 상담자료·사건자료·개인정보를 공개 PR·원격 디자인 분석·외부 LLM에 전송하지 않는다. URL 캡처·Figma·이미지 API 등은 실제 요청 범위와 연결 권한을 확인한다. 유료 호출·외부 업로드·발행은 별도 명시적 승인 없이 하지 않는다. 참고 화면이 없거나 접근 실패했으면 관찰을 지어내지 않는다.

## 검증과 한계

```bash
python scripts/check_writing_design_sources.py
python -m unittest discover -s tests -p "test_writing_design_skills.py"
python scripts/validate_guidelines.py
```

기본 검사는 gitlink·URL·고정 SHA와 어댑터 연결을 확인하며 원본 미초기화는 허용한다. `--require-checkout`은 초기화된 커밋·LICENSE와 선택된 3개 SKILL.md의 Git blob SHA도 확인한다. 이것은 원본 전체 스크립트의 보안 감사나 Claude Code/Codex 세션의 실제 호출, 문장·디자인 품질 개선을 증명하는 테스트가 아니다. 실제 품질은 같은 승인 원고·브랜드 조건의 전후 결과와 실제 렌더로 비교한다.

변경 기록: `docs/changes/2026-10-31-writing-design-skills.md`.
