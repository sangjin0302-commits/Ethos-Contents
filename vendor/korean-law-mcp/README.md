# korean-law-mcp (참조 기록, 코드 미포함)

- Source: https://github.com/chrisryugj/korean-law-mcp
- Commit (HEAD at check): fe834b8947f2b363ed8ddf23be0e497dee360b52 (package.json version 4.15.6)
- Checked: 2026-10-06
- License: MIT, Copyright (c) 2025 Chris (see `LICENSE`, copied unmodified)
- Copied code: none. 이 폴더에는 출처와 라이선스 기록만 둔다. 서버는 원격 주소나 npm 패키지로 쓴다.

## 우리가 쓰는 것

`docs/legal-verification.md` §6 인용 검증 단계에서 법제처 Open API(국가법령정보센터) 대조 도구로만 쓴다.

| 용도 | 도구 (upstream `docs/API.md` 기준) | 입력 |
|---|---|---|
| 조문·판례 인용 실존·제목 대조 | `legal_analysis`, `mode: "verify_citations"` | `text` (필수), `maxCitations` (기본 15) |
| 판례가 이후 변경·폐기됐는지 | `legal_analysis`, `mode: "cite_check"` | `caseNumber` |
| 조문 본문·별표 조회 | `get_law_text`, `get_annexes`, `search_law` | 법령명·조문 |

upstream README에 따르면 v4.4.0부터 `verify_citations`는 `legal_analysis`의 `mode`로 노출되며, 옛 이름으로 직접 호출하거나 `execute_tool`로 부르는 방식도 하위 호환으로 동작한다. 인용 추출은 우리 쪽 `scripts/extract_citations.py`(오프라인)가 하고, 이 도구는 대조만 한다.

## 연결 정보 (upstream README에서 확인한 것)

- 법제처 Open API 인증키(OC): https://open.law.go.kr 에서 무료 발급.
- 로컬 실행: `npm install --ignore-scripts --omit=optional -g korean-law-mcp` 후 명령 `korean-law-mcp`, 환경 변수 `LAW_OC`.
- 원격 주소: `https://mcp.gomdori.app/law` (구 주소 `https://korean-law-mcp.fly.dev/mcp`도 하위 호환).
- 원격 인증키 전달(우선순위): URL `?oc=키` / HTTP 헤더 `apikey: 키`(`law-oc`, `x-api-key`, `Authorization: Bearer`도 허용) / 도구 파라미터 `apiKey`.
- 키 없이 원격 서버를 쓰면 모든 무키 사용자가 공유하는 한도에 걸려 429가 날 수 있다. 본인 키를 헤더로 보내면 이 한도를 거치지 않는다.

## 확인 필요

- ChatGPT 커스텀 커넥터 연결 절차: upstream에는 연결 영상 링크만 있고 글로 된 절차가 없다. 요금제별 사용 가능 여부도 확인 필요.
- Codex CLI 연결: upstream README에 Codex 설정은 없다. `.codex/config.example.toml`은 Codex 소스(`codex-rs/config/src/mcp_types.rs`)의 설정 필드로 작성했고, 실제 연결은 확인 필요.
- Windows에서 전역 설치한 `korean-law-mcp` 명령을 Codex가 그대로 실행하는지(`.cmd` 확장자 필요 여부) 확인 필요.

## 주의

- 인증키를 저장소·원고·`citations.md`에 적지 않는다. `?oc=키`가 붙은 주소는 링크로도 쓰지 않는다(`docs/blog-authoring-spec.md` 발행 형식).
- 도구 결과는 사람이 확인할 근거일 뿐 법령 해석을 보증하지 않는다.
- 갱신할 때는 upstream README·`docs/API.md`를 다시 읽고 Commit·Checked·도구 표를 고친다.
