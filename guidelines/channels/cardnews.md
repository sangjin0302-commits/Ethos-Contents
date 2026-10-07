# ETHOS 카드뉴스 채널 라우터 v1.0

카드뉴스 작업은 공통 지침을 적용한 뒤 기존 결정론적 제작 시스템을 그대로 사용한다.

역할 분담: 1~7단계의 카피 초안과 디자인 방향은 ChatGPT가 `docs/card-authoring-spec.md`로, 8단계 이후의 윤문·영문·승인 요청·렌더는 Codex가 `docs/card-codex-production.md`로 한다. 두 명세가 이 문서의 작업용 요약이다.

## 필수 순서

1. 승인된 원문에서 사실·수치·조건·한정어를 Source Lock으로 삼되 원문의 문장 구조까지 복제하지 않는다.
2. `docs/card-selection.md`로 전체 캐러셀·짧은 파생물·제작하지 않음을 선택한다.
3. 소재 발굴 작업이라면 `docs/topic-discovery.md`로 시각화할 충돌·순서·대조관계를 먼저 정한다.
4. 캐러셀 전체의 질문과 답 흐름을 정하고, 국문 카피를 인스타그램에서 사람이 설명하듯 자연스럽게 초안한다.
5. 국문 초안을 Source Lock과 대조해 사실·법률·한정어를 검증한다.
6. 기획·마케팅 기준 `references/ethos-card-design-v3.7.md`로 훅, 저장가치, Proof of Work, Reader Boundary, CTA를 필요한 만큼 보강한다.
7. 경험 창작·과장·공포·직접 연락 유도와 반복되는 보고서식 문장·동일 종결어미를 검사한다.
8. `docs/language-quality-workflow.md`에 따라 국문 카피를 윤문하고 의미를 다시 대조한다. 영문은 국문 문장 수를 복제하지 않고 별도의 현지화 편집과 의미 대조를 거친다.
9. brief와 국·영문 card-data에 편집 단계 완료 상태를 기록한다. 새 세트는 `pipelineVersion: 2.0`과 모든 완료 상태가 확인돼야 사용자 승인 단계로 넘어간다.
10. 사용자 승인을 받은 뒤 `docs/card-codex-production.md`, 결정론적 제작 기준 `references/ethos-card-design-v3.3.md`, `docs/editorial.md`, `docs/layout-playbook.md`, `docs/html-contract.md`, `docs/asset-policy.md`에 따라 렌더한다.
11. QA와 마케팅 검토를 실행하고 축소 시트에서 상하 여백·시선 흐름·영문 밀도를 사람이 확인한다. 마케팅 권고는 사실 정확성을 침해하거나 렌더를 불필요하게 막는 하드 게이트로 바꾸지 않는다.
12. `docs/channel-packaging.md`에 따라 필요한 채널 결과물만 만든다.
13. 발행 후 `docs/performance-learning.md`와 `performance-log.csv`로 실제 반응을 기록한다.

## 공통 콘텐츠 원칙

- 경험담·사례·후기·성과를 창작하지 않는다.
- Authority를 이력 주장보다 판단 과정으로 보여준다.
- 한 장에는 한 메시지만 둔다.
- 희소성은 낯선 업종명보다 시각화 가능한 제도·순서·문서의 충돌로 보여준다.
- AI 시대에 사람의 전문성을 보여줄 때에는 `guidelines/modules/human-judgment-positioning.md`에 따라 사실관계 분기·문서 정합성·절차 순서·직접 확인과 전문가 판단의 경계 중 하나를 시각화한다. 로봇·회로·AI 화면은 장식으로 사용하지 않는다.
- 영문은 국문의 기계적 직역이 아니라 같은 사실 구조를 보존한 독립 편집본으로 쓴다.
- 마지막 장은 독자가 직접 확인할 범위와 종합 검토가 필요한 경계를 보여준 뒤, 주제에 맞는 무료 검토 안내 한 문장으로 끝낸다.
- 연락처·URL·버튼을 카드 본문에 넣지 않는다.

세부 시각 규칙과 수치는 위 문서와 기존 검사 시스템을 단일 기준으로 삼고 이 파일에 중복 기재하지 않는다.
