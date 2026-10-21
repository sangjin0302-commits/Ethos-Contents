# 국문 블로그 ⑥편 — 최종 윤문·검수 기록

## 작업 기준
- 대상: `content/COSMETICS-FUNCTIONAL-06/blog.md`, `blog.txt`
- 최신 심사·보고 설명용 원고: `[내 화장품 브랜드를 만들기 전에 알아야 할 인허가 ⑥] 미백·주름개선 화장품 OEM, 기능성화장품 심사가 필요할까요?`
- 2026-10-20: 초안 → 자연스러운 한국어 부분 윤문 → 법률상 서법·숫자·인용 복원 → 공식 원본 검증 게이트 적용.
- 2026-10-20 병합본 MD 10,372자, 네이버 TXT 10,343자. 2026-10-21 제한적 후속 편집안은 MD 10,366자, 네이버 TXT 10,337자.
- MD에서 제목 기호를 제거한 결과와 TXT는 완전히 일치함.
- 무료 사전 검토 CTA 1회, 이미지 영역 1곳(기존 상담 이미지 4장), 후반 3줄 요약, 태그 17개.
- 정식 시리즈명과 회차·중심 질문을 유지. 소제목·사례를 줄여 핵심 법률 조건을 뭉뚱그리지 않음.

## 실제 자동검사
- [GitHub Prose hints](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39375693041): PASS. pinned `im-not-ai v2.3.2` 정량 검사 `standard / medium`.
- MuncheKit: `KO-REGISTER-001` 경고 1건(질문형 제목·예시 대사와 혼재하는 존댓말 어투; 비차단, 최종 맥락 확인); ko-mt-lint 문법 지적 없음.
- [im-not-ai upstream 실제 검증](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39375692732): `prepare_monolith_input.py`와 `verify_gates.py` 실제 실행 후 최종 `exit 0`; 원문 대비 변경률 7.8%; 문장 터치율 39/195(20%); 법률 서법 소실 0건; 숫자·인용·제목 보존 PASS.
- 앞선 upstream 검증에서 소제목 교체 및 법률상 의무·가능성 표현을 지적한 것을 수정하고 재실행해서 통과함.
- 별도 외부 생성형 AI API를 통한 자동 재작성은 미실행. 최종 문장 수정은 `humanize-korean` 규칙 기반의 ChatGPT 직접 부분 윤문.

## 법률 검토 범위
- 「화장품법」 제4조, 시행규칙 제9조·제10조의 심사·보고·자료 제출 면제 차이를 유지.
- 시행규칙 제10조제1항제1호~제3호, 기존 심사 품목의 사업자·제조개발 관계, 기능성 성분·함량, pH 예외와 제형 예외, 대조군 비교실험 요건을 유지.
- 실제 2026-03-09 식약처 공개 회신의 성분·함량 및 사실관계 한정을 보존.
- 심사 목적 선행 제조의 최대 3개 제조단위 특례, 원료목록 보고와 기능성 보고 구분, 수출 전용 예외, 행정사법상 문서 업무 범위와 기술적 시험 경계를 유지.
- [Verify citations](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39375692937): PASS. 그러나 일부 축약 조문·고시 별표·세부 조항에는 수동 확인 권고가 있으므로 법률 실체 해석의 전면 검증을 뜻하지 않음.

## 기타 검사·후속 상태
- [Render cards](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39375692972): PASS.
- PR #67 병합 당시 최종 [Link integrity check](https://github.com/sangjin0302-commits/Ethos-Contents/actions/runs/39376666094)는 두 번째 실행에서 PASS. 첫 실행의 외부 URL 타임아웃은 접근 환경 문제였으며 최종 재검사 결과와 구별한다.
- 원고 자체는 이번 최종 점검에서 추가적인 전면 윤문을 권하지 않음. 형식 경고는 없고, 단 1건의 비차단 문체 참고가 남아 있음.
- 본 리뷰는 발행 승인이나 수임 전환 개선 실증이 아님.
- GitHub [PR #67](https://github.com/sangjin0302-commits/Ethos-Contents/pull/67)은 2026-10-20에 `main`으로 squash 병합 완료(커밋 `f20fbbae7ee594f3166ed2d542406bdd6bc50d6a`). 네이버 블로그 발행은 이 작업에서 진행하지 않았다.
- 2026-10-21 별도 후속 편집안: 도입의 중복 문단 1개 삭제, 실무 문서 작성 설명과 CTA 유료범위의 문서명 구체화, 문서·근거 기록의 과거 PR 상태 정정. 기존 본문 법률상 숫자·조문·핵심 요건·공식 회신·소제목은 유지. 이 후속 편집안은 기존 병합 원본을 소급 덮어쓰지 않고 새 브랜치에서 검토한다.
