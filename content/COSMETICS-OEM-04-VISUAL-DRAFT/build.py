"""Render-ready HTML for the Korean OEM visual comparison (no auto-fit)."""
from pathlib import Path
import json, re, html

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'COSMETICS-OEM-04-READABILITY-DRAFT'
d=json.loads((HERE/'card-data.ko.json').read_text(encoding='utf8'))
e=html.escape
def emoji(code,cls=''):
    label={'1f4c4':'문서','1f50d':'검토','1f4e6':'납품 상자','1f3ed':'제조업체','1f4c2':'보유 자료','1f512':'영업비밀','1f504':'사양 변경'}[code]
    return f'<img class="emoji {cls}" src="../assets/{code}.svg" alt="{label}" data-decor>'
def icon(name):
    svg=(HERE/f'assets/{name}.svg').read_text(encoding='utf8')
    return '<span class="line-icon" aria-hidden="true" data-decor>'+svg+'</span>'
def row(item,i=0,graphic='',classes=''):
    if isinstance(item,str): return f'<div class="item {classes}">{graphic}<p>{e(item)}</p></div>'
    return f'<div class="item {classes}">{graphic}<div><h3>{e(item["key"])}</h3><p>{e(item["text"])}</p></div></div>'

for c in d['cards']:
    n=c['page']; items=c['body']
    if n==1:
        main='<div class="cover-scene" data-decor>'+emoji('1f4c4')+emoji('1f50d')+'</div>'
        main+=f'<h1 class="cover-title" data-role="headline">{e(c["headline"])}</h1><p class="lede">{e(items[0])}</p><p class="promise">{e(c["promise"])}</p>'
    elif n==2:
        main='<div class="roles">'+row(items[0],graphic=emoji('1f3ed'))+row(items[1],graphic=icon('building-2'))+'</div>'
    elif n==3:
        main='<div class="routes">'+row(items[0],graphic=icon('building-2'))+row(items[1],graphic=emoji('1f4c4'))+'</div>'
    elif n==4:
        main='<div class="match">'+row(items[0],graphic=emoji('1f4e6'))+'<div class="bridge" data-decor>'+icon('arrow-right')+'</div>'+row(items[1],graphic=emoji('1f50d'))+'</div>'
    elif n==5:
        main='<div class="oem-flow">'+''.join(row(it,graphic=icon(ic)) for it,ic in zip(items,['clipboard-check','file-text','folder-open']))+'</div>'
    elif n==6:
        main='<div class="change">'+row(items[0],graphic=emoji('1f4c4'))+row(items[1],graphic=emoji('1f504'))+'</div>'
    elif n==7:
        main='<div class="principle">'+row(items[0],graphic=icon('file-text'))+'<div class="exceptions">'+''.join(row(it) for it in items[1:])+'</div></div>'
    elif n==8:
        main='<div class="conditions">'+emoji('1f512')+'<div class="condition-list">'+''.join(row(it) for it in items)+'</div></div>'
    elif n==9:
        main='<div class="documents">'+''.join(row(it,graphic=icon('file-text')) for it in items)+'</div><p class="doc-note">'+e(c['note'])+'</p>'
    else:
        main='<div class="contact">'+row(items[0],graphic=emoji('1f4c2'))+row(items[1],graphic=emoji('1f50d'))+'</div>'
    template=(BASE/f'ko/card_{n:02}.html').read_text(encoding='utf8')
    start=template.index('  <div class="body">')
    end=template.index('  <div class="ftr">',start)
    title='' if n==1 else f'<h2 class="h2" data-role="headline">{e(c["headline"])}</h2>'
    take=f'<p class="close" data-role="takeaway">{e(c["takeaway"])}</p>' if c.get('takeaway') else ''
    body=f'  <div class="body"><div class="z-title" data-zone="title">{title}</div><div class="z-main" data-zone="main"><div class="visual-main" data-focal>{main}</div></div><div class="z-take" data-zone="take">{take}</div></div>\n'
    template=template[:start]+body+template[end:]
    template=re.sub(r'<style>.*?</style>','',template,flags=re.S)
    template=re.sub(r'data-card-type="[^"]+"',f'data-card-type="{c["type"]}"',template)
    template=template.replace('card free ','card free visual ')
    (HERE/'ko').mkdir(exist_ok=True)
    (HERE/f'ko/card_{n:02}.html').write_text(template,encoding='utf8')
print('Built 10 Korean draft cards')
