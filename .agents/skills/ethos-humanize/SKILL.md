---
name: ethos-humanize
description: ETHOS 국문 블로그·SNS·카드의 어색한 AI 문장을 점검하고, 필요할 때 pinned im-not-ai v2.3.2 전체 진단·윤문·검증을 실행한다. '문체 자연스럽게', '적용해서는 안 됩니다 같은 어투 수정', 'im-not-ai 적용', 'humanize 강화' 요청에 사용한다.
---

# ETHOS × im-not-ai: 문체 진단과 필요한 부분만 윤문

## 범위와 기준

- 최신 에토스 채널 명세 및 원문(Source Lock), 법률상 주체·의무/재량·조건·예외·수치·날짜·조문·인용·서비스 범위가 상위 기준이다. 먼저 기존 사실 검증을 마친다.
- 이 스킬은 기존 quick-rules 한 장을 읽는 경로보다 넓은 **im-not-ai 공식 Codex 전체 파이프라인**(정량 사전 진단 → light/standard/heavy 윤문 → 결정적 게이트 → 필요한 경우 finalize)을 연결한다.
- 글이 이미 자연스러우면 유지한다. 다수의 어색한 문장이 있거나 사용자가 문체 문제를 직접 지적했다면, 상위 shim의 route_hint에만 의존하지 않고 문맥을 확인해 정밀 검토한다.
- '적용해서는 안 됩니다', '옮겨서는 안 됩니다', '설명해서는 안 됩니다'는 무조건 금지어가 아니다. 작성자용 검수 지시가 새어 나온 문장인지 확인하고, 독자용 사실·근거·실제 확인 행동으로 고친다. **실제 법정 금지는 반드시 남긴다.**

## 고정 버전 설치 없이 임시 체크아웃

원본 출처: https://github.com/epoko77-ai/im-not-ai
고정 커밋: b37e0206d31fffd9149bf57168d4d62eb2086bee (v2.3.2, MIT)

이 저장소의 AGENTS.md에서 이 스킬로 들어오면 다음과 같이 외부 임시 폴더에 체크아웃한다. 기존 사용자의 GitHub 저장소·전역 Codex 스킬 설치·API 시크릿을 변경하지 않는다.

    IM_NOT_AI_ROOT="$(mktemp -d)"
    git -C "$IM_NOT_AI_ROOT" init -q
    git -C "$IM_NOT_AI_ROOT" remote add origin https://github.com/epoko77-ai/im-not-ai.git
    git -C "$IM_NOT_AI_ROOT" fetch -q --depth=1 origin b37e0206d31fffd9149bf57168d4d62eb2086bee
    git -C "$IM_NOT_AI_ROOT" checkout -q --detach FETCH_HEAD
    test "$(git -C "$IM_NOT_AI_ROOT" rev-parse HEAD)" = "b37e0206d31fffd9149bf57168d4d62eb2086bee"

체크아웃이 불가능하면 **전체 im-not-ai를 실행했다고 말하지 않는다.** 기존 ETHOS 문체 규칙으로 부분 윤문하고 미실행 범위를 기록한다. 무단으로 다른 버전으로 대체하지 않는다.

## 전체 실행

1. 먼저 실제 원고 파일과 원문을 보호한다. 기존 승인 콘텐츠를 덮어쓰지 말고 신규 초안 또는 분리된 수정본에서 작업한다. 원문 제목·인사·시리즈 목차·CTA·네이버 상담 이미지 자리·말미 요약·태그를 유지한다.
2. 다음 원본 스킬을 읽고 그 지침의 CLI·role 계약을 실행한다. 경로를 짐작하지 말고 실제로 체크아웃한 위치에서 찾는다.
   - "$IM_NOT_AI_ROOT/codex/skills/humanize-korean/SKILL.md"
   - "$IM_NOT_AI_ROOT/skills/humanize-korean/references/quick-rules.md"
   - 필요하면 "diagnosis-rules.md", "references/roles/{diagnostician,monolith,finalizer}.md"
3. 진단 전용이면 해당 버전의 "skills/humanize-scan/SKILL.md"를 참고한다. 단, 이 스캔은 상위의 6가지 구조 신호만 보는 **선별 검사**이고 한국어 문체의 전부를 판정하지 않는다.
4. 원고에 반복된 지시형 부정문, 문어체 명사화, 추상 연결어, 정보 없는 '검토가 필요합니다'가 있으면 필요한 문단을 **법률 독자용 평서문**으로 고친다. 법률의 금지 자체나 '수 있다' 같은 법정 한정은 완화·삭제하지 않는다.
5. 사용자가 정밀 윤문을 요청하거나 어색한 문장이 전반에 반복되는 경우 공식 "--strict" heavy 경로를 사용한다. 그렇지 않으면 상위 shim의 route_hint를 따른다. 15,000자 이하는 임의로 청킹하지 않는다.
6. 상위 "scripts/verify_gates.py"로 원문과 수정본을 검증한다. 강제 중단(exit 2) 또는 검사 오류(exit 3)는 채택하지 않는다. 경고(exit 1)도 근거 및 수정 문장을 직접 다시 본다. 이 게이트가 숫자·법률 의미를 전부 보장하지는 않으므로, 별도로 원고의 조문·숫자·한정어·주체·재량·예외·서비스 범위를 대조한다.
7. 기존 quick-rules의 E-1 '100자 이상 장문 생성'은 ETHOS 칼럼에서 **미적용**. 숫자를 맞추려고 문장을 늘리거나 C-8 대구를 기계적으로 몰살하지 않는다. 전개·일상 예시·전문적인 근거를 희생해서 문장을 짧게 만들지 않는다. 사람이 실제로 쓴 듯한 자연스러움과 법률 정확성 두 조건을 모두 충족한다.
8. 수정한 부분만 반영하고, **사용자의 PR 승인·main 병합·발행을 자동 수행하지 않는다.** 상위 요약 주석(HUMANIZE-SUMMARY)은 내부 검수 메모로 분리하여 네이버 공개 본문에 남기지 않는다.

## GitHub PR 자동 진단과의 차이

- GitHub Actions의 "Prose hints"는 pinned 상위 "prepare_monolith_input.py"로 국문 원고를 **읽기 전용으로 점검**하고 참고 지표·어색한 표현 후보를 PR 댓글에 남긴다. 자동 재작성/유료 API 호출이 아니다.
- 이 스킬은 Codex 작업에서 실제 윤문이 필요한 때에만 **원문 → 수정본 → 게이트**까지 수행한다. 모델·API를 실행하지 않았다면 전체 윤문 완료라고 기록하지 않는다.
- GitHub의 정량 점수는 법률 글의 완성도나 AI 작성 여부를 판정하는 근거가 아니다.

관련 운영정책: docs/language-quality-workflow.md, docs/tooling-policy.md.
