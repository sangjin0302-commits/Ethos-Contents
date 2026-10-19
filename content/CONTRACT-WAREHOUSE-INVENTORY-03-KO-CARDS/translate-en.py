import json,pathlib,copy
P=pathlib.Path(__file__).parent
ko=json.loads((P/"card-data.ko.json").read_text(encoding="utf-8"))
M={
"사장님, 계약서만 믿으셨나요?":"Did You Trust the Contract, Business Owner?",
"③":"No. 3",
"비교용 초안 — 사용자 카드 승인 전. 발행 금지":"Draft for comparison — awaiting user card approval. Do not publish.",
"수량 차이가 생겼다면 기록부터 나눠 봅니다.":"When quantities differ, separate the records first.",
"재고 차이의 원인을 찾는 기준":"A way to find the cause of the discrepancy",
"장부의 차이가 곧바로 분실·배상책임은 아닙니다.":"A ledger difference does not by itself prove loss or liability.",
"창고에 맡긴 상품,\\n재고가 다르면 누구 책임일까요?":"Who is responsible when goods stored in a warehouse do not match?",
"창고에 맡긴 상품,\n재고가 다르면 누구 책임일까요?":"Who is responsible when goods stored in a warehouse do not match?",
"예를 들어, 세 숫자가 다르다면":"What if the three numbers do not match?",
"회사 장부":"Company ledger","매입과 판매 등을 반영한 수량":"Quantity reflecting purchases and sales",
"창고 장부":"Warehouse ledger","창고가 입출고를 관리하는 수량":"Quantity managed for warehouse receipts and shipments",
"실사":"Physical count","창고에서 직접 센 수량":"Quantity counted in the warehouse",
"1,200개":"1,200 units","1,150개":"1,150 units","1,130개":"1,130 units",
"50개와 20개의 차이를 따로 확인합니다.":"Check the 50-unit and 20-unit differences separately.",
"50개와 20개, 원인도 다를 수 있습니다":"The 50-unit and 20-unit gaps may have different causes.",
"장부 사이 50개":"50 units between ledgers","출고가 회사 장부에 늦게 반영됐을 수 있습니다. 취소 주문이나 반품 검수 시점도 살펴봅니다.":"A shipment may have been recorded late in the company ledger. Check cancelled orders and the timing of return inspections.",
"장부와 실물 20개":"20 units between the ledger and the count","실사에서 빠진 선반이나 불량품 구역이 있는지 봅니다. 잘못 출고했거나 실제로 잃어버렸을 수도 있습니다.":"Check whether a shelf or defective-goods area was missed. The goods may have been shipped incorrectly or actually lost.",
"같은 기준시각, 상품코드와 수량 단위로 비교합니다.":"Compare them using the same timestamp, product code and unit of count.",
"숫자를 고치기 전, 기록을 맞춰봅니다":"Before changing numbers, reconcile the records.",
"대조할 기록":"Records to compare","확인할 내용":"What to check","입고확정":"Receipt confirmation","창고가 인수한 수량을 확인합니다.":"Confirm the quantity accepted by the warehouse.","출고지시와 인계":"Shipment instruction and handoff","요청과 실제 처리, 택배사 인계를 나눠 봅니다.":"Separate the request, actual processing and courier handoff.","반품 송장과 검수표":"Return waybill and inspection sheet","돌아온 상품과 검수한 내용을 대조합니다.":"Compare returned goods with the inspection record.","실사표와 조정 이력":"Count sheet and adjustment history","누가 왜 수량을 바꿨는지 확인합니다.":"Check who changed the quantity and why.","수정 전 원본을 남기고, 마지막으로 수량이 같았던 때부터 봅니다.":"Keep the original before editing and start from the last time the quantities matched.",
"‘상호 협의’만으로는 기록이 남지 않습니다":"“Mutual discussion” alone leaves no record.","수정 전":"Before","수정 후 방향":"Direction for revision","“수탁자는 위탁물품을 선량하게 보관하고, 재고 차이가 발생하면 당사자 간 협의하여 처리한다.”":"“The custodian shall store the entrusted goods with due care and handle any inventory difference through discussion between the parties.”","입고예정 수량과 검수·확정 수량을 나눠 기록하고, 합의한 경로로 출고합니다. 취소와 반품, 불량품 이동, 재고조정의 사유와 처리시각, 담당자도 남깁니다.":"Record expected, inspected and confirmed receipt quantities separately, and ship through the agreed approval route. Keep the reason, time and person responsible for cancellations, returns, defective-goods movement and inventory adjustments.","당사자가 합의한 업무 방식을 계약서에 구체적으로 적습니다.":"Put the parties’ agreed workflow into specific contract terms.",
"차이가 생겼을 때의 기준도 정합니다":"Set the standard for a discrepancy","같은 기록":"Same records","같은 기준시각의 입출고 기록과 반품·조정 기록, 실사 결과를 대조합니다.":"Compare receipt and shipment records, return and adjustment records, and the count result at the same reference time.","책임 판단":"Liability assessment","멸실 또는 훼손이 인정되면 적용 법령 및 계약에서 정한 기준에 따라 책임과 손해액을 판단합니다.":"If loss or damage is established, assess liability and the amount of loss under applicable law and the contract.","같은 기록으로 원인을 살피고, 실제 손해의 책임을 판단합니다.":"Use the same records to identify the cause, then assess liability for actual loss.","멸실은 물건이 없어지는 것, 훼손은 물건이 손상되는 것입니다. 보관 중 멸실 또는 훼손이 인정돼야 합니다.":"Loss means the goods are gone; damage means they are harmed. Loss or damage during storage must be established.",
"실제로 없어진 물건은 책임을 따집니다":"Liability depends on goods actually missing","적용 관계":"Applicable relationship","타인을 위해 창고에 물건을 보관하는 일을 영업으로 하는 창고업 관계인지 봅니다.":"First determine whether this is a warehouse-business relationship involving storage for another person.","보관 중 사고":"Incident during storage","맡겨둔 물건의 멸실 또는 훼손이 인정되는 경우입니다.":"The entrusted goods must be found lost or damaged.","주의의 증명":"Proof of due care","창고업자 또는 그 사용인이 보관에 주의를 게을리하지 않았음을 증명하지 못하면 책임을 면하지 못합니다.":"The warehouse operator cannot avoid liability unless the operator or its employee proves that due care was exercised in storage.","먼저 맡긴 수량과 인수·출고 내역, 반환할 수 없는 상품을 확인합니다.":"First confirm the entrusted quantity, acceptance and shipment records, and goods that cannot be returned.",
"무단출고도 ‘멸실’에 포함됩니다":"Unauthorized shipment can also count as “loss”","대법원 1981. 12. 22. 선고 80다1609":"Supreme Court, Dec. 22, 1981, 80Da1609","담보로 제공된 생사를 보관하던 사건입니다. 대법원은 상법 제166조의 ‘멸실’에 권한 없는 사람에게 무단으로 출고해 맡긴 사람에게 반환할 수 없게 된 경우도 포함된다고 봤습니다.":"The case concerned silk held as collateral. The Court held that “loss” under Article 166 of the Commercial Act includes unauthorized shipment that makes it impossible to return the goods to the person who entrusted them.","오늘날 풀필먼트 계약과 구조는 다릅니다. 출고 권한과 승인 기록을 살피는 데 참고할 수 있습니다.":"Modern fulfillment contracts have a different structure. The ruling can guide review of shipment authority and approval records.","누가 요청했고 어떤 승인을 거쳐 출고했는지 확인합니다.":"Check who requested the shipment and what approval preceded it.",
"보관과 운송, 사고 난 단계를 나눕니다":"Separate the storage and transport stages","대법원 2019. 7. 10. 선고 2019다213009":"Supreme Court, July 10, 2019, 2019Da213009","대법원은 보관과 물류정보 활용, 항만 하역 등이 포함된 종합물류운영 계약의 핵심 요소를 복합운송으로 보았습니다.":"The Court treated multimodal transport as the core element of a comprehensive logistics operation contract that included storage, logistics-information use and port handling.","특정 계약의 성격과 운송물 손해에 관한 판결입니다. 모든 풀필먼트 계약을 운송계약으로 정한 것은 아닙니다.":"This ruling concerned the character of a specific contract and cargo loss. It did not classify every fulfillment contract as a transport contract.","택배사 인계 전후를 구분해 인계증빙과 운송 기록도 살펴봅니다.":"Separate the period before and after courier handoff, and review handoff proof and transport records.",
"계약서와 기록, 함께 놓고 봅니다":"Review the contract and records together","직접 준비":"Prepare directly","물류대행 계약서, 입출고 내역과 반품·재고조정 내역, 최근 실사표를 준비해 주세요. 같은 시각의 수량부터 맞춰봅니다.":"Prepare the logistics-service contract, receipt and shipment records, return and adjustment records, and the latest count sheet. Start by matching quantities at the same time.","맡길 문서":"Document work to entrust","합의한 입고확정 기준, 출고승인 절차, 실사·조정 방식을 계약 문서에 반영하는 업무입니다. 손해배상 분쟁이나 시효는 필요한 경우 변호사 검토가 필요합니다.":"This work reflects agreed receipt-confirmation standards, shipment approvals, and count and adjustment procedures in contract documents. Damages disputes or limitation periods may require attorney review.","보내 주신 자료로 대조할 기록과 계약서의 빠진 기준을 무료 사전 검토해 드립니다.":"A free preliminary review can identify which records to compare and which standards are missing from the contract."
}
def conv(x):
 if isinstance(x,str):
  return M.get(x,x)
 if isinstance(x,list): return [conv(v) for v in x]
 if isinstance(x,dict): return {k:(v if k in ("sourceTrace","design","compressionNote","paragraph") else conv(v)) for k,v in x.items()}
 return x
en=conv(ko)
en["contentId"]="CONTRACT-WAREHOUSE-INVENTORY-03-KO-CARDS";en["language"]="en";en["series"]="Did You Trust the Contract, Business Owner?";en["issue"]="No. 3";en["approvedBy"]="Draft for comparison — awaiting user card approval. Do not publish."
en["marketing"]={"targetReader":"Shop and brand operators using an outside warehouse","readerQuestion":"Does the warehouse have to pay for every difference between the ledger and physical count?","practicalPayoff":"Separate the two gaps and identify the standards to put in the contract.","coverIntent":"A question about warehouse inventory discrepancies and responsibility","saveValue":"A record checklist to revisit when inventory differs","ctaInputs":["Logistics-service contract","Receipt, shipment, return and adjustment records","Latest physical count sheet"],"ctaOutcomes":["Records to compare first","Missing receipt, shipment-approval and count standards in the contract"],"performanceHypothesis":"Test whether separating the number gaps improves saves"}
en["editorialReview"]["languagePass"]="english-localization";en["editorialReview"]["reviewNote"]="Localized into clear legal English while preserving Korean-law conditions, numbers, case scope and service boundaries. Awaiting user card approval."
short={"50 units between ledgers":"50-unit ledger gap","20 units between the ledger and the count":"20-unit physical gap","Shipment instruction and handoff":"Shipment and handoff","Return waybill and inspection sheet":"Return and inspection","Count sheet and adjustment history":"Count and adjustments","Direction for revision":"Revision direction","Document work to entrust":"Document work"}
def shorten(x):
 if isinstance(x,str): return short.get(x,x)
 if isinstance(x,list): return [shorten(v) for v in x]
 if isinstance(x,dict): return {k:shorten(v) if k not in ("sourceTrace","design","compressionNote","paragraph") else v for k,v in x.items()}
 return x
en=shorten(en)
(P/"card-data.en.json").write_text(json.dumps(en,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

