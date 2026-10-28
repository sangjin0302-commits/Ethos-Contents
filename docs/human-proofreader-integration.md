# ETHOS × Solar Human Proofreader — 요청부터 결과 회수까지

원본: https://github.com/SolarLLM/human-proofreader-mcp

MCP 설정 주소: `https://human-proofreader-mcp.toy.x.upstage.ai/api/mcp`

상위 서버 소스를 복사하거나 새 서버를 운영하지 않는다. 기존 im-not-ai·Prose hints·법률 의미 검증과 카드 디자인 게이트를 유지하며, 필요한 국문 원고의 통독·윤문 제안에만 사용한다. 설정 파일의 존재와 실제 원고 처리 완료는 구분한다.

## 1. 채팅에서 실행하는 기본 경로 — 담당자는 ChatGPT

사용자가 Solar 실행을 요청하고 현재 GitHub 연결에 파일 쓰기 기능이 있으면, 채팅 컨테이너의 DNS나 `workflow_dispatch` 기능에 의존하지 말고 아래 요청 브랜치 경로를 사용한다. 사용자에게 Actions 버튼을 누르라고 넘기는 것이 기본 경로가 아니다.

1. **실제 입력과 동의 확인**: 현재 대화·첨부·연결 저장소에서 원문을 확보한다. 다른 대화의 원고를 제목이나 글자 수만으로 재구성하지 않는다. 공개 GitHub에 원문·결과를 저장하는 것과 외부 Solar 처리의 동의를 구분한다. 고객정보·상담기록·비공개 사건자료는 올리지 않는다. 미발행 원고의 공개 동의를 추정하지 않는다.
2. **최신 기준 고정**: 커넥터로 최신 main 커밋을 읽는다. 고유 ID는 영문 소문자·숫자·하이픈 3~64자로 만든다. `proofreader/request/<id>` 브랜치를 main 커밋에서 만든다. 운영 개선 PR 브랜치와 원고 요청 브랜치는 구분한다.
3. **원문 잠금과 요청**: `_proofreader/requests/<id>/source.md`에 정확한 UTF-8 원문을 저장하고 그 바이트의 SHA-256을 계산한다. 아래 `request.json`과 함께 한 커밋으로 올리는 것을 권장한다. 두 번 쓰면 source.md를 먼저, request.json을 마지막에 쓴다. main 기준에서 바꾸는 파일은 이 두 개뿐이어야 한다.
4. **실행 확인**: GitHub 커넥터의 쓰기로 push가 발생하면 `Human proofreader request bridge`가 실행된다. 커넥터의 fetch로 해당 브랜치의 Actions 실행과 실제 상태·실행 ID를 확인한다. `fetch_commit_workflow_runs`는 PR 이벤트만 반환할 수 있으므로 push 탐색에 의존하지 않는다.
5. **결과 회수**: 실행 후 같은 요청 브랜치의 `_proofreader/results/<id>/summary.json`을 `fetch_file`로 읽는다. `request_commit`·`source_sha256`·`source_unchanged`가 맡긴 원고와 일치하는지 확인하고 `proposal.md`, `review.md`, `changes.diff`, 필요 시 `report.md`를 실제로 읽는다. 바이너리 아티팩트 다운로드 없이 일반 파일 읽기로 회수할 수 있다.
6. **전달과 채택 구분**: 성공한 교정본도 제안이다. 실제 원문과 바뀐 부분을 보고 주체·조건·예외·의무/재량·출처·서비스 범위를 직접 대조한다. 원문을 덮어쓰거나 카드 Source Lock·발행 승인을 자동 갱신하지 않는다. 파일을 제공할 때는 실제 생성한 경로만 안내한다.

기본 흐름은 **원고 확보 → ChatGPT의 승인 요청 커밋 → GitHub 실행 환경의 Solar 처리 → 분리된 결과 파일 커밋 → ChatGPT의 회수·대조·전달**이다. 실패 시 실제 진행 범위를 보고하며 수동 윤문 결과를 Solar 결과로 표시하지 않는다. 응답 종료 후 백그라운드 작업을 약속하지 않는다.

## 2. 요청 파일 계약

다음은 형식 예시다. SHA와 ID는 실제 값으로 채우고 동의는 사용자 요청에 근거해서만 true로 기록한다.

```json
{
  "version": 1,
  "request_id": "example-20261028-01",
  "base_commit": "실제로 조회한 main의 40자리 커밋 SHA",
  "source_sha256": "source.md 실제 UTF-8 바이트의 SHA-256",
  "consent": {
    "public_repository": true,
    "external_processing": true,
    "no_private_data": true,
    "authorization": "사용자가 승인한 범위와 이번 원고를 식별하는 짧은 기록"
  },
  "mode": "proofread",
  "genre": "블로그",
  "depth": "standard",
  "preserve": ["원문에 실제로 존재하며 그대로 남겨야 하는 문장"],
  "instructions": "어색한 부분만 고치고 제목·인사·목차·CTA·요약·태그와 법률 의미를 유지하세요."
}
```

- mode는 `readability`, `read_through`, `proofread` 중 선택한다. proofread는 보수 강도로 고정한다. depth는 light 또는 standard이고 기본은 standard다. deep은 이 요청 경로에서 지원하지 않는다.
- 한 요청에는 한 원고만 보낸다. 최대 20,000 UTF-16 코드 단위다. 긴 원고를 임의로 잘라 남은 부분을 누락하지 않는다. 한도를 넘으면 문맥을 보존하는 구간별 요청을 계획하고 전체 검수 범위를 구분한다.
- 좋은 점수를 맞추려고 여러 윤문 도구를 연속으로 전면 재작성시키지 않는다. read_through는 진단이며 교정본을 만들지 않는다.
- preserve의 각 문구는 실제 입력에 있어야 한다. 숫자·조문·인용·핵심 한정어를 가진 문장을 필요에 따라 지정한다. 지정하지 않은 구간의 법률 의미도 대조한다.
- 인증키·별도 외부 URL·실행 명령을 요청 파일에 넣지 않는다. 이 경로는 개인 유료 API 키를 사용하지 않는다. 공개 무료 서비스가 응답하지 않으면 실패로 남긴다.
- 잘못된 ID, 동의 누락, 지문 불일치, symlink 입력, 허용 범위 밖의 파일 변경은 전송 전에 거절한다. 개인정보가 없는지는 작성자가 먼저 확인해야 하며 동의 플래그가 개인정보 자동 검출을 뜻하지 않는다.

## 3. 결과와 완료 기준

결과는 요청 브랜치에만 저장한다. main과 content의 승인 원고에는 쓰지 않는다.

| 파일 | 내용 |
|---|---|
| `summary.json` | 원고·요청 지문, 실행 주소, 상태, 원본 보존과 검사 결과 |
| `original.md` | 실제로 보낸 원문 사본 |
| `report.md` | Solar 원격 도구 원응답 |
| `proposal.md` | proofread 교정 제안. 거절된 제안도 검토 증거로만 보관 |
| `review.md` | 원격 판정 및 ETHOS 숫자·인용·한정어·30% 변경률 대조 |
| `changes.diff` | 원문과 제안의 실제 차이 |

`succeeded`는 요청 처리가 끝났다는 뜻이지 법률 검수·사용자 승인·발행 완료가 아니다. `gate_rejected`는 결과는 왔지만 채택 조건을 충족하지 못했다는 뜻이다. `remote_error`는 외부 처리/응답 단계 실패, `invalid_request`는 전송 전 거절이다. `semantic_review`는 pending, `publication_approved`는 false로 유지한다.

실패·거절도 보고서를 남기며 성공으로 포장하지 않는다. 원격 호출을 무조건 반복하지 않는다. 이미 결과가 기록된 요청을 재실행하면 저장된 결과를 재사용한다. 새 원고나 의도적 재시도는 새 ID로 남긴다. 실행 도중 요청 브랜치가 바뀌면 강제 push하지 않는다.

아티팩트도 7일 보관하지만 **요청 브랜치의 원문과 결과는 자동 삭제되지 않는다.** 공개 브랜치·로그·아티팩트를 비공개 공간으로 취급하지 않는다. 공개 저장에 동의하지 않은 자료는 이 경로를 쓰지 않는다.

## 4. 기존 수동 실행·CLI·Codex 경로

기존 `Human proofreader (manual, public drafts only)` 수동 워크플로는 유지한다. `content/<ID>/blog.md`, `website.ko.md`, `caption.ko.md` 중 공개 가능한 파일을 지정하고 confirm_public에 동의한다. 원고를 수정하지 않으며 결과 아티팩트를 3일 보관한다. 요청 브랜치 방식은 이 수동 워크플로를 강제로 호출하는 것이 아니라 별도의 명시적 요청 트리거다.

Python CLI는 표준 라이브러리만 사용한다. 다음 로컬 대조에는 외부 전송이 없다.

```bash
python scripts/human_proofreader_mcp.py --mode local-compare --file before.md --after after.md
```

공개 가능한 파일의 외부 호출에는 전송 동의를 명시한다.

```bash
python scripts/human_proofreader_mcp.py --mode proofread --file before.md --genre 블로그 --strength 보수 --depth standard --allow-external --output new-report.md
```

기존 CLI의 usage·suggest·compare와 `.codex/config.example.toml` 예시는 유지한다. 개인 BYOK는 별도 동의·비용 확인 후 개인 환경변수에 설정하며 요청 워크플로로 자동 전파하지 않는다. 저장소의 예시 설정만으로 개인 Codex·다른 채팅에 MCP 도구가 자동 등록되지는 않는다.

## 5. 시험 범위와 운영 경계

운영 연결의 검증은 **새 원고 지정 → 실제 호출 → 결과 커밋 → 채팅의 파일 회수 → 원본 지문 확인**까지 해야 한다. 모의 테스트·짧은 고정 샘플·실제 원고 시험을 구분한다. ⑨편 등 원문이 현재 대화나 연결 자료에 없으면 확인하지 못했다고 알리고 대체 내용을 지어내지 않는다.

외부 소견이 `할 수 있다`를 의무로 바꾸라고 하거나 한정어를 약한 표현이라고 지적해도 그대로 채택하지 않는다. ETHOS 법률 의미와 30% 변경률 보호가 상위 기준이다. 모든 길이·모드·향후 서비스 가용성을 보장하지 않으며 서비스 장애와 편집상 거절은 구분한다.
