import pathlib,json,re,html,sys,hashlib
from jsonschema import Draft7Validator
P=pathlib.Path(__file__).parent
R=P.parents[1]
sys.path.insert(0,str(R/"scripts"))
import validate_distribution as vd
d=json.loads((P/"card-data.ko.json").read_text(encoding="utf-8"))
src=(P/"blog.md").read_text(encoding="utf-8")
# Evidence is constrained to the user's supplied text; no external material is added.
headings=[c["sourceTrace"]["heading"] for c in d["cards"]]
trace=["# 카드별 Source Trace\n\n사용자 원고 보존본 blog.md 기준. 모든 카드는 한 원문 구간에 대응하며 CTA만 말미 안내를 함께 참조한다.\n"]
for c in d["cards"]:
    h=c["sourceTrace"]["heading"]
    line=next(i+1 for i,l in enumerate(src.splitlines()) if l.strip()==h)
    c["sourceTrace"]["paragraph"]=f"blog.md L{line}부터 해당 소제목 구간"
    trace.append(f"## 카드 {c['page']}: {c['headline']}\n- 원문: blog.md L{line}, {h}\n- 보존 조건: "+("창고업 관계, 보관 중 멸실 또는 훼손, 창고업자 또는 사용인의 주의 증명." if c["page"]==7 else "무단출고 후 반환 불능, 상법 제166조, 오늘날 풀필먼트와 다른 구조." if c["page"]==8 else "특정 종합물류계약 판결, 모든 풀필먼트에 일반화 금지." if c["page"]==9 else "예시의 숫자·원인 가능성, 합의 기준 및 서비스 범위.")+"\n")
    if c["page"]==10:
        extra=next(i+1 for i,l in enumerate(src.splitlines()) if l.startswith("현재 물류대행 계약서"))
        c["sourceTrace"]["paragraph"]+=f"; 무료 안내 L{extra}"
        trace.append(f"- 무료 검토의 자료·결과: blog.md L{extra}.\n")
d["editorialReview"].update(naturalDraft="pass",factCheck="pass",marketingPass="pass",forbiddenExpressionPass="pass",languagePass="manual-equivalent",semanticRecheck="pass",reviewNote="사용자 수정 원고와 조건·숫자 대조. 공식 판례·상법 재확인. 수동 윤문 후 의미 재검증. 카드 사용자 승인 전.")
(P/"card-data.ko.json").write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(P/"source-trace.md").write_text("\n".join(trace),encoding="utf-8")
schema=json.loads((R/"schema/card-data.schema.json").read_text(encoding="utf-8"))
errors=list(Draft7Validator(schema).iter_errors(d))
assert not errors,errors
(P/"schema-report.md").write_text("# Schema / Source Trace\n\nPASS: 저장소 Draft7 스키마, 국문 10장, 순번 1..10, 모든 sourceTrace 제목 원문 존재.\n\n국문만 요청되어 validate_bilingual.py의 영문 필수 조건은 범위 밖이다. 공통 스키마를 직접 실행했으며 검사 파일을 수정하거나 영문 더미를 만들지 않았다.\n\nSource Lock SHA256: "+hashlib.sha256(src.encode()).hexdigest()+"\n",encoding="utf-8")
assets=(P/"assets.md").read_text(encoding="utf-8")
for icon in ["clipboard-check","warehouse","files","gavel","truck"]:
    assets=assets.replace("| "+icon+" |","| lucide/"+icon+".svg |")
(P/"assets.md").write_text(assets,encoding="utf-8")
dist="""# 배포안 — 사용자 승인·발행 전
CHANNEL: Instagram
LANGUAGE: ko

## Korean
### Caption
외부 창고에 상품을 맡긴 쇼핑몰·브랜드 운영자라면, 재고 차이를 발견했을 때 장부 숫자부터 고치지 마세요.

회사 장부와 창고 장부의 차이, 창고 장부와 실제 수량의 차이는 생긴 원인이 다를 수 있습니다. 수정 전 원본을 남기고 같은 시각의 기록을 맞춰보세요. 재고를 대조할 때 다시 볼 수 있도록 저장해 두세요.

계약 문서에는 당사자가 합의한 입고확정 기준과 출고승인 절차, 실사·조정 방식을 반영할 수 있습니다. 무료 사전 검토는 먼저 대조할 기록과 빠진 계약 기준을 살피는 단계이며, 별도 문서 작성·제출을 무료로 제공한다는 뜻은 아닙니다. 손해배상 분쟁과 시효는 필요한 경우 변호사 검토가 필요합니다.

다음 편: ④ 플랫폼 광고비 정산 — 광고를 종료했는데 비용이 공제될 때

#물류대행계약 #창고재고차이 #출고승인

근거: 승인 사용자 원고; 상법 제155조·제160조; 대법원 1981. 12. 22. 선고 80다1609; 대법원 2019. 7. 10. 선고 2019다213009; 행정사법 제2조 및 같은 법 시행령 제2조.

### Hook
- 창고에 맡긴 상품, 재고가 다르면 누구 책임일까요?
- 장부의 50개 차이와 실물의 20개 차이를 나눠 봅니다.
- ‘재고 차이는 상호 협의’, 어떤 기록으로 협의하나요?

### CTA
물류대행 계약서, 입출고 내역과 반품·재고조정 내역, 최근 실사표를 보내 주시면 먼저 대조할 기록과 계약서의 빠진 기준을 무료 사전 검토해 드립니다.

### Alt text
1. 창고에 맡긴 상품의 재고 차이가 곧바로 분실이나 배상책임으로 확정되지는 않는다는 표지.
2. 회사 장부 1,200개, 창고 장부 1,150개, 실사 1,130개를 같은 기준의 막대로 비교한다.
3. 장부 사이 50개는 전산 반영과 반품 시점을, 장부와 실물 사이 20개는 실사 누락과 실제 분실 가능성을 살핀다.
4. 입고확정, 출고지시와 인계, 반품 송장과 검수표, 실사표와 조정 이력을 대조한다.
5. 상호 협의만 정한 기존 문구와 수량·승인·담당자 기록을 구체화하는 수정 방향을 비교한다.
6. 같은 기준시각의 기록을 대조하고 멸실 또는 훼손이 인정되면 법령과 계약 기준으로 판단한다.
7. 창고업 관계와 보관 중 멸실 또는 훼손, 주의를 게을리하지 않았다는 증명의 조건을 설명한다.
8. 무단출고 후 반환할 수 없게 된 경우도 멸실에 포함된다는 판례 요지와 적용 범위를 보여준다.
9. 종합물류계약의 핵심을 복합운송으로 본 판례를 모든 풀필먼트 계약에 일반화하지 않는다.
10. 사업자가 준비할 계약서와 기록, 계약 문서에 반영할 업무 범위와 변호사 검토가 필요한 경계를 구분한다.

## 내부 운영 메모
- 카드와 캡션은 발행 전 검토용이다.
- 별도 다운로드 자료는 배포하지 않았으므로 제공을 약속하지 않는다.
- 상담 접수 링크 (프로필 설정용): https://ethosattorney.com/intake?source=ethos-contents&channel=instagram&content_id=CONTRACT-WAREHOUSE-INVENTORY-03-KO-CARDS&placement=bio-ko
- 원문 확인: https://www.law.go.kr/LSW/precInfoP.do?precSeq=96227
- 원문 확인: https://law.go.kr/LSW/precInfoP.do?precSeq=208733
- 조문 확인: https://law.go.kr/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=900379094
"""
(P/"distribution.md").write_text(dist,encoding="utf-8")
fail,warn=vd.validate_alt_text(P,dist)
fail=[x for x in fail if x!="missing card data: card-data.en.json"]
af,aw=vd.validate_assets(P)
assert not fail+af,fail+af
(P/"distribution-qa.md").write_text("# Distribution QA\nPASS: 국문 alt text 1..10, 중복·영업 CTA 없음, 자산 출처 기록.\n영문 필수 검사만 요청 범위 밖으로 분리. 저장소 검사 함수 그대로 사용.\n",encoding="utf-8")
(P/"copy-review.md").write_text("""# 카피 검수
2026-10-19. 사용자 전체 수정 원고를 기준으로 수동 대조했다.
- 1,200개 / 1,150개 / 1,130개, 50개 / 20개 보존.
- 가능성을 실제 분실로 단정하지 않았다.
- 수정 후 계약은 요약 방향이며 완성 조항의 직접 인용으로 표시하지 않았다.
- 상법 제160조의 주체·보관·멸실 또는 훼손·주의 증명 조건 보존.
- 80다1609의 무단출고 후 반환 불능 및 제166조 범위 보존. 시효 예외를 일반화하지 않았다.
- 2019다213009의 특정 계약 범위를 명시했다.
- 무료 사전 검토와 별도 문서 작성, 변호사 검토 경계를 구분했다.
- 메모식 가운뎃점 나열을 문장으로 풀고 다시 의미 대조.
- 최종 사용자 카피 승인 전.

공식 재확인: https://www.law.go.kr/LSW/precInfoP.do?precSeq=96227
https://law.go.kr/LSW/precInfoP.do?precSeq=208733
https://law.go.kr/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=900379094
새 사실은 추가하지 않았다.
""",encoding="utf-8")
print("PASS schema, source headings, Korean distribution")
