import pathlib,json,re,html
P=pathlib.Path(__file__).parent;R=P.parents[1]
d=json.loads((P/"card-data.ko.json").read_text(encoding="utf-8"))
E=lambda x:html.escape(x).replace("\n","<br>")
def ico(n):
 s=(R/f"assets/icons/lucide/{n}.svg").read_text(encoding="utf-8")
 s=re.sub(r'<\?xml.*?\?>','',s)
 return s.replace("<svg ",f'<svg data-icon="{n}" ',1)
for c in d["cards"]:
 n=c["page"];p=P/f"ko/card_{n:02}.html";s=p.read_text(encoding="utf-8")
 s=s.replace('<meta name="ethos-auto" content="1">','')
 s=re.sub(r'<style>.*?</style>','<link rel="stylesheet" href="../design.css">',s,flags=re.S)
 s=re.sub(r'<script>.*?</script>','',s,flags=re.S) # explicit sizes; never shrink text automatically
 title=E(c["headline"])
 if n==2: title=title.replace("예를 들어, 세","예를 들어,<br>세")
 if n==3: title=title.replace("50개와 20개, 원인","50개와 20개,<br>원인")
 title=f'<h2 class="h2" data-role="headline">{title}</h2>'
 b=c["body"]
 if n==1:
  main=f'<div class="warehouse-scene" data-focal><div class="scene-warehouse">{ico("warehouse")}</div><div class="scene-ledger">{ico("clipboard-check")}</div></div><div class="cover-copy"><p>{E(b[0])}</p><p class="promise" data-role="note">{E(c["promise"])}</p></div>'
 elif n==2:
  main='<div class="inventory-bars" data-focal>'+''.join(f'<div class="inventory-row"><div class="inventory-label"><b>{E(x["key"])}</b><strong>{E(x["display"])}</strong></div><div class="track"><div class="fill" style="width:{x["value"]/1200*100:.4f}%"></div></div><p>{E(x["text"])}</p></div>' for x in b)+'</div>'
 elif n==3:
  main='<div class="differences" data-focal>'+''.join(f'<section><h3>{E(x["key"])}</h3><p>{E(x["text"])}</p></section>' for x in b)+'</div>'
 elif n==4:
  main=f'<div class="records" data-focal><div class="record-head"><b>{E(c["head"][0])}</b><b>{E(c["head"][1])}</b></div>'+''.join(f'<div class="record-row"><h3>{E(x["key"])}</h3><p>{E(x["text"])}</p></div>' for x in b)+'</div>'
 elif n==5:
  main='<div class="contract-edit" data-focal>'+''.join(f'<section><h3>{E(x["key"])}</h3><p>{E(x["text"])}</p></section>' for x in b)+'</div>'
 elif n==6:
  main='<div class="criteria" data-focal>'+''.join(f'<section><h3>{E(x["key"])}</h3><p>{E(x["text"])}</p></section>' for x in b)+'</div>'
 elif n==7:
  main='<div class="liability" data-focal>'+''.join(f'<section><h3>{E(x["key"])}</h3><p>{E(x["text"])}</p></section>' for x in b)+'</div>'
 elif n in (8,9):
  main=f'<div class="judgment judgment-{n}" data-focal><div class="judgment-source" data-role="note">{E(b[0])}</div><div class="judgment-body">{E(b[1])}</div><div class="judgment-boundary">{E(b[2])}</div></div>'
 else:
  main='<div class="handoff" data-focal>'+''.join(f'<section><h3>{E(x["key"])}</h3><p>{E(x["text"])}</p></section>' for x in b)+'</div>'
 if n==4:
  main=main.replace('<div class="records" data-focal>', '<div class="records" data-focal="records"><div class="record-symbol">'+ico("files")+'</div>')
 if n==8:
  main=main.replace('<div class="judgment judgment-8" data-focal>', '<div class="judgment judgment-8" data-focal="judgment"><div class="case-symbol">'+ico("gavel")+'</div>')
 if n==9:
  main=main.replace('class="judgment judgment-9" data-focal', 'class="transport-case" data-focal="transport"').replace('<div class="judgment-source"', '<div class="transport-symbol">'+ico("truck")+'</div><div class="judgment-source"')
 s=re.sub(r'<div class="z-title" data-zone="title">.*?</div>\s*<div class="z-main" data-zone="main">.*?</div>\s*<div class="z-take"',f'<div class="z-title" data-zone="title">{title}</div>\n<div class="z-main" data-zone="main">{main}</div>\n<div class="z-take"',s,flags=re.S)
 s=s.replace("‘멸실’에",'<span style="white-space:nowrap">‘멸실’에</span>')
 p.write_text(s,encoding="utf-8")
print("10 individually composed HTML cards")
