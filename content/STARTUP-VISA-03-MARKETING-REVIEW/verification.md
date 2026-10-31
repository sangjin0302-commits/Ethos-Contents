# 내부 검수 메모 — 2026-10-31

본 폴더는 **비발행 검토용**이며 승인된 `content/` Source Lock을 대체하지 않습니다.

## 확인된 근거
- 국가법령정보센터 「출입국관리법」 제17조제1항, 제20조, 제24조제1항 (2026-10-02 시행): https://www.law.go.kr/법령/출입국관리법
- 한국생산성본부 글로벌창업이민센터 OASIS: https://www.oasisvisa.com/kor/process.html (D-10-2 기술창업 준비활동·영리활동 불허)
- 교육부 Study in Korea: https://studyinkorea.go.kr/ko/work/aboutForeignerEmploymentSystem.do (준비 활동 예시)
- 대법원 2016. 7. 14. 선고 2015두48846 판결: https://www.law.go.kr/LSW/precInfoP.do?evtNo=2015%EB%91%9048846 (변경허가의 효력과 재량; D-10-2 판매 사건은 아님)

## 검증 잔여
- 무료 베타테스트·시범운영 실비의 구체적 허용범위는 2026-10-19 법무부 체류관리지침 전문을 직접 대조하지 못함. 포괄적인 허용·금지 단정 금지.
- 네이버 이미지와 실제 CTA 링크 표시 상태 검증 필요.

## 실제 도구 사용
- GitHub `main`과 ETHOS 최신 블로그·검색의도·편집·im-not-ai 명세: 조회함.
- Claude Blog 고정 업스트림의 analyze/SEO/GEO/factcheck/rewrite SKILL: 읽고 **방법을 수동 적용**함. Claude Code CLI/원본 파이썬 스크립트 자체는 실행하지 못함.
- ETHOS Editorial·im-not-ai Quick Rules: 수동 윤문. Solar Proofreader: 미실행.
- 로컬 자체 형식점검: 통과(8,073자, CTA 1회, 기존 상담 이미지 자리 4개, 태그 18개). 이는 GitHub CI 결과가 아님.
