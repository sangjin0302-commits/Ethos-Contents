# Writing/design source inventory

ETHOS의 선택형 편집·디자인 어댑터에 대한 출처와 라이선스 기록이다. 활성 운영은 `docs/writing-design-skills.md`와 `.agents/skills/ethos-*/SKILL.md` 중 해당 작업의 파일만 따른다.

## 고정 원본

- RampStack Co.: https://github.com/rampstackco/claude-skills/tree/9b90db257f7395fab76ff9bfcb808456709f6af3 — `content-and-copy`, `art-direction`. MIT 고지는 `LICENSE-rampstack.txt`에 보존했다.
- Alan Ponce (KeroClow): https://github.com/uxKero/anydesign/tree/d81bd8957a21c2d7fba8d2a8f4f60050d09368b5 — AnyDesign. MIT 고지는 `LICENSE-anydesign.txt`에 보존했다.
- 발견 목록: https://github.com/ComposioHQ/awesome-claude-skills/tree/be2a406907dbc61b73e6827ded415c96139d13a2

원본은 각각 `vendor/rampstack-skills`, `vendor/anydesign`의 커밋 고정 서브모듈로 연결한다. 전체 저장소가 연결돼 있어도 활성화한 것은 위 3개 스킬에 대한 ETHOS 어댑터뿐이다. upstream의 다른 스킬·플러그인·hooks·설치 스크립트를 전역 등록하거나 실행하지 않는다. 원본 LICENSE와 상대경로 references는 서브모듈 안에서 그대로 유지한다.

로컬 어댑터는 해당 MIT 방법을 ETHOS 법률·브랜드·승인 조건에 맞게 수정한 파일이며 원본 그대로가 아니다. `sources.json`에는 커밋, 선택 원본 파일의 Git blob SHA, 어댑터 이름과 채택/제외 판단을 기록한다.

Composio의 `content-research-writer`와 `canvas-design`은 원문·예시·코드·폰트를 복사하지 않고, 도입/문단 피드백과 표지의 시각 기획이라는 방법만 ETHOS 문장으로 재구성했다. 목록 저장소 전체에 단일 라이선스가 적용된다고 간주하지 않는다. `brand-guidelines`와 `theme-factory`는 ETHOS 브랜드를 보존하기 위해 자동 적용하지 않는다.
