# ETHOS × Solar Human Proofreader — 선택형 MCP 윤문

원본: https://github.com/SolarLLM/human-proofreader-mcp  
MCP 주소(POST 전용, 일반 GET은 405): `https://human-proofreader-mcp.toy.x.upstage.ai/api/mcp`

이 통합은 외부 저장소의 **코드를 복사하거나 원격 서버를 배포하지 않는다.**
공개 MCP 서버에 클라이언트로 접속하는 선택형 보조 기능이다. 서버가 바뀌면
동작·결과도 바뀔 수 있다. 현재 저장소의 im-not-ai 고정 버전,
Prose hints, 법률 검증, 카드 디자인과 발행 게이트는 그대로 유지한다.

## 언제 사용하나

- 기본: 기존 에토스 명세에 따라 자연 초안을 작성하고 법률 근거를 검증한 후, 어색한 구간만 부분 윤문한다.
- 통독에서 문제가 남으면: Human Proofreader의 `read_through`를 통해 중복 문단·논리 단절·리듬 문제를 **진단만** 한다.
- 표현의 대안이 필요한 짧은 구간이면: `suggest`를 선택적으로 쓴다.
- 전체 윤문을 명시적으로 요청한 경우에 한해: `proofread`를 **보수** 강도로 사용한다. 결과는 제안이며 원문을 자동 교체하지 않는다.
- 수정 전후 점검: 로컬 `local-compare`를 우선 사용한다. 필요할 때 `compare`도 호출할 수 있지만 이 경우 원문과 수정본 모두 외부로 전송된다.

여러 윤문 도구를 무조건 연달아 돌리지 않는다. 통독 소견이 잘못된 법률 단순화나
불필요한 짧은 문장 나열을 권해도 채택하지 않는다. 블로그는 필요한 법률적 깊이와
정확한 주체·조건·예외·근거를 유지한다. 승인된 원문(Source Lock)과 발행 콘텐츠는
새 외부 도구 도입만을 이유로 수정하지 않는다.

## 1. GitHub Actions에서 수동 실행 (Codex 불필요)

PR을 검토·병합한 뒤 저장소의 **Actions → Human proofreader (manual, public drafts only) → Run workflow**로 이동한다.

- `content_path`: 외부에 공개해도 되는 `content/<ID>/blog.md`, `website.ko.md`, `caption.ko.md` 중 하나.
- `mode`: `readability`(정량 분석)·`read_through`(통독 소견)·`proofread`(보수 윤문) 중 선택.
- `confirm_public`: 고객정보·비공개 계약서·상담기록·미공개 사건자료가 없는지 검토하고 외부 전송에 동의한 경우에만 체크.

워크플로는 **수동 실행만** 허용한다. 원고를 변경하거나 PR 댓글을 달지 않는다.
결과는 실행 페이지의 `human-proofreader-report` 아티팩트에서 확인한다(3일 보관).
**공개 저장소의 Actions 로그·아티팩트를 비공개 저장공간으로 간주하지 않는다.**
서버 사용량과 무료 한도는 실행 시점의 실제 서버 응답을 따른다.
MCP 서버가 외부망에서 응답하지 않거나 무료 한도에 도달하면 실패할 수 있다.

## 2. Python CLI로 실행 (Codex 불필요)

표준 라이브러리만 사용하며 Python 3.12 이상을 권장한다.
저장소 루트에서 실행한다.

**네트워크 없는 원고 대조:**

~~~bash
python scripts/human_proofreader_mcp.py --mode local-compare \
  --file content/EXAMPLE-ID/blog.md --after review/blog-polished.md
~~~

이 검사는 외부로 글을 보내지 않는다. 숫자·직접 인용·링크와 법률 한정 표현의
누락·추가, 변경률 30% 초과를 찾아 채택을 보류한다(종료 코드 2).
문자·토큰 정규식 검사이므로 오탐과 미탐이 가능하며 **법률 의미 인증이 아니다.**

**공개해도 되는 원고의 통독만 요청:**

~~~bash
python scripts/human_proofreader_mcp.py --mode read_through \
  --file content/EXAMPLE-ID/blog.md --allow-external
~~~

**외부 교정 제안 요청:**

~~~bash
python scripts/human_proofreader_mcp.py --mode proofread \
  --file content/EXAMPLE-ID/blog.md --genre 블로그 --strength 보수 \
  --depth standard --allow-external
~~~

**수정본을 외부 비교기에 보내기:**

~~~bash
python scripts/human_proofreader_mcp.py --mode compare \
  --file content/EXAMPLE-ID/blog.md --after review/blog-polished.md --allow-external
~~~

`--mode usage`는 원고 없이 무료 한도만 확인한다. `readability`도 서버를 거치므로
원고를 보낼 때는 `--allow-external`이 필요하다. 보고서를 저장하려면
`--output <새 파일 경로>`를 지정한다. CLI는 원문과 기존 파일을 덮어쓰지 않는다.

MCP 서버의 공개 무료 제공 조건은 변경될 수 있다. BYOK가 필요하면 Git Bash 환경
변수 `ETHOS_UPSTAGE_API_KEY` 또는 `ETHOS_OPENROUTER_API_KEY`를 **저장소 밖에서**
설정한다. API 키를 명령줄 인자나 커밋 파일에 넣지 않는다.
자체 운영 HTTPS 서버를 쓰는 경우 `ETHOS_PROOFREADER_MCP_URL`로 주소를 변경할 수
있으나 그 서버에 원문이 전달된다는 점은 동일하다.

## 3. Codex MCP 설정 예시 (선택)

`.codex/config.example.toml`의 `[mcp_servers.human_proofreader]` 예시를
개인 `~/.codex/config.toml`에 복사하면 Codex MCP 도구로도 호출할 수 있다.
**저장소에 설정 예시를 추가해도 개인 Codex나 ChatGPT에 자동 등록되는 것은 아니다.**

사용 가능한 도구:
`read_through`, `readability`, `proofread`, `compare`, `suggest`, `usage`.
CLI는 도구 호출 이름과 동일한 `--mode`를 제공하고, `local-compare`만 에토스
측 오프라인 게이트다.

## 4. 법률 원고 채택 관문

1. 근거 확인과 법률 초안이 먼저다. 윤문 도구 출력은 새로운 법률 근거가 아니다.
2. 교정 원고의 출처·조문·숫자·날짜·직접 인용·URL·주체·조건·예외·재량·금지·서비스 범위를 원문 및 공식 근거와 대조한다.
3. **에토스의 변경률 30% 이하 기준**을 적용한다. Solar 서버의 50% 중단 기준이 이를 대체하지 않는다.
4. 서버가 `✅`를 반환해도 자동 채택하지 않는다. 누락된 숫자를 원격 게이트가 관찰 항목으로만 처리할 수 있으며, 의미가 달라진 법률 표현을 놓칠 수도 있다.
5. 기존 승인 원고와 카드뉴스 Source Lock을 덮어쓰지 않고, 수정한 곳만 별도 초안에 반영해 필요한 법률 의미·채널 형식 검사를 다시 한다.
6. 사용자 승인 없이는 PR 병합, 카드 승인, 발행을 하지 않는다. ChatGPT가 해당 MCP를 실제 호출하지 않은 경우 실행했다고 보고하지 않는다.

## 5. 경계 및 검증

- 이 통합의 **로컬 테스트**는 HTTP 응답 파싱·초기화·옵트인·원문 보호·로컬 비교를 모의 응답으로 검증한다. 외부 Solar 모델 품질이나 현재 공개 서버의 실사용 성공을 인증하지 않는다.
- 원격 서비스의 라이선스·요금·운영정책은 상위 저장소와 서비스 제공자의 최신 안내를 확인한다. ETHOS 저장소는 상위 소스코드를 포함하지 않는다.
- 외부 서버를 이용할 수 없는 경우에는 기존 ETHOS 수동 윤문, im-not-ai, Prose hints로 정상 작업을 이어간다.
