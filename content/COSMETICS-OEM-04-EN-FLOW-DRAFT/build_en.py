"""Localize the adopted Korean free design without changing its source files."""
from pathlib import Path
import json, html

HERE=Path(__file__).resolve().parent
ko=json.loads((HERE/'card-data.ko.json').read_text(encoding='utf-8'))
en=json.loads((HERE/'card-data.en.json').read_text(encoding='utf-8'))
e=html.escape
def visible(c):
    out=[c[k] for k in ['headline','promise','note','takeaway'] if c.get(k)]
    for item in c['body']:
        out.extend([item] if isinstance(item,str) else [item['key'],item['text']])
    return out
for kc,ec in zip(ko['cards'],en['cards']):
    n=kc['page']
    source=(HERE/f'ko/card_{n:02}.html').read_text(encoding='utf-8')
    pairs=sorted(zip(visible(kc),visible(ec)),key=lambda pair:len(pair[0]),reverse=True)
    for old,new in pairs:
        old=e(old); new=e(new)
        if old in source: source=source.replace(old,new)
        elif old.replace('. ','.<br>') in source:
            source=source.replace(old.replace('. ','.<br>'),new if n==7 else new.replace('. ','.<br>'))
        else: raise AssertionError((n,old))
    source=source.replace('lang="ko"','lang="en"').replace('lang-ko','lang-en')
    source=source.replace('화장품 브랜드 인허가 · No.04','Cosmetics Brand Launch · No.04')
    source=source.replace('에토스 행정사사무소','Ethos Administrative Attorney Office')
    for old,new in {'문서':'Document','제조업체':'Manufacturer','영업비밀':'Trade secret','검토':'Review','납품 상자':'Delivery','보유 자료':'Your documents','사양 변경':'Specification change'}.items():
        source=source.replace('alt="'+old+'"','alt="'+new+'"')
    (HERE/f'en/card_{n:02}.html').write_text(source,encoding='utf-8')
print('Built 10 localized English cards; Korean files untouched')
