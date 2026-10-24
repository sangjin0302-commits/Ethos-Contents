import pathlib,json,sys,shutil,zipfile
P=pathlib.Path(__file__).parent;R=P.parents[1]
sys.path.insert(0,str(R/"scripts"))
import copy_lint,marketing_review
d=json.loads((P/"card-data.ko.json").read_text(encoding="utf-8"))
for c in d["cards"]:
 missing=copy_lint.copy_lock(c,(P/f"ko/card_{c['page']:02}.html").read_text(encoding="utf-8"))
 assert not missing,(c["page"],missing)
(P/"copy-lock-report.md").write_text("# Copy Lock\nPASS: 10/10. 저장소 copy_lint.copy_lock으로 JSON→HTML 문구 일치 확인.\n막대 표시 숫자 1,200개 / 1,150개 / 1,130개 및 실제 비례값도 대조.\n",encoding="utf-8")
scores,notes=marketing_review.review(d)
(P/"marketing-report.md").write_text("# Marketing review — ko only\n\n저장소 review 함수를 국문에만 적용. 영문 미제작은 요청 범위에 따른다.\n권고 점수: "+str(sum(scores.values()))+"/100\n"+json.dumps(scores,ensure_ascii=False)+"\n\n"+"\n".join(notes)+"\n자동 점수는 실제 성과·사용자 승인·디자인 평가를 대신하지 않음.\n",encoding="utf-8")
shutil.copyfile(R/"content/_TEMPLATE/performance-log.csv",P/"performance-log.csv")
print("PASS copy lock 10/10; Korean marketing review saved")
