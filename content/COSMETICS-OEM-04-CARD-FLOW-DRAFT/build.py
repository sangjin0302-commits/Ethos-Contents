"""Build only four revised cards; preserve six other cards byte-for-byte."""
from pathlib import Path
import json, html

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'COSMETICS-OEM-04-VISUAL-DRAFT'
DATA = json.loads((HERE/'card-data.ko.json').read_text(encoding='utf-8'))
e = html.escape

def emoji(code):
    label = {'1f3ed':'제조업체','1f4c4':'문서','1f512':'영업비밀'}[code]
    return f'<img class="emoji" src="../assets/{code}.svg" alt="{label}" data-decor>'

def row(item, graphic=''):
    text = e(item['text']).replace('. ', '.<br>')
    return f'<div class="item">{graphic}<div><h3>{e(item["key"])}</h3><p>{text}</p></div></div>'

for c in DATA['cards']:
    n = c['page']
    template = (BASE/f'ko/card_{n:02}.html').read_text(encoding='utf-8')
    if n not in (2, 7, 8, 9):
        (HERE/f'ko/card_{n:02}.html').write_bytes((BASE/f'ko/card_{n:02}.html').read_bytes())
        continue
    items = c['body']
    if n == 2:
        main = '<div class="role-rows">'+row(items[0], emoji('1f3ed'))+row(items[1], emoji('1f4c4'))+'</div>'
    elif n == 7:
        main = '<div class="submission">'+row(items[0])+'<div class="exception-group">'+''.join(row(x) for x in items[1:])+'</div></div>'
    elif n == 8:
        main = '<div class="conditions">'+emoji('1f512')+'<div class="condition-list">'+''.join(row(x) for x in items)+'</div></div>'
    else:
        main = '<div class="documents">'+''.join(row(x, emoji('1f4c4')) for x in items)+'</div><p class="doc-note">'+e(c['note']).replace('. ', '.<br>')+'</p>'
    body = f'<div class="body"><div class="z-title" data-zone="title"><h2 class="h2" data-role="headline">{e(c["headline"])}</h2></div><div class="z-main" data-zone="main"><div class="visual-main" data-focal>{main}</div></div><div class="z-take" data-zone="take"><p class="close" data-role="takeaway">{e(c["takeaway"])}</p></div></div>\n'
    start = template.index('  <div class="body">')
    end = template.index('  <div class="ftr">', start)
    template = template[:start] + body + template[end:]
    (HERE/f'ko/card_{n:02}.html').write_text(template, encoding='utf-8')
print('Built four changed cards; six unchanged HTML files preserved')
