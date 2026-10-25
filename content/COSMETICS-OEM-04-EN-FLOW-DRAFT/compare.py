"""Same-browser English comparison and pixel-level Korean preservation check."""
from pathlib import Path
import hashlib, json, re, html
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OLD=HERE.parent/'COSMETICS-OEM-04-READABILITY-DRAFT'
KO=HERE.parent/'COSMETICS-OEM-04-CARD-FLOW-DRAFT'
e=html.escape
norm=lambda s:re.sub(r'\s+','',s)
def strings(c):
    result=[c[k] for k in ['headline','promise','note','takeaway'] if c.get(k)]
    for it in c['body']:
        result.extend([it] if isinstance(it,str) else [it['key'],it['text']])
    return result
def write(path,value):
    p=HERE/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value,encoding='utf-8')

old=json.loads((OLD/'card-data.en.json').read_text(encoding='utf-8'))
new=json.loads((HERE/'card-data.en.json').read_text(encoding='utf-8'))
ko=json.loads((HERE/'card-data.ko.json').read_text(encoding='utf-8'))
originalko=json.loads((KO/'card-data.ko.json').read_text(encoding='utf-8'))
assert ko['cards']==originalko['cards']
assert (HERE/'blog.md').read_bytes()==(KO/'blog.md').read_bytes()
hashes=json.loads((HERE/'source-hashes.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in hashes.items())
for k,c in zip(ko['cards'],new['cards']):
    for field in ['page','type','bg','sourceTrace']: assert k[field]==c[field],(c['page'],field)

checks=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':540,'height':675},device_scale_factor=2)
    page.route('http://**',lambda r:r.abort());page.route('https://**',lambda r:r.abort())
    for label,folder,lang,data in [('before',OLD,'en',old),('after',HERE,'en',new),('ko',HERE,'ko',ko),('ko-baseline',KO,'ko',originalko)]:
        (HERE/f'comparison/{label}').mkdir(parents=True,exist_ok=True)
        for card in data['cards']:
            n=card['page']
            page.goto((folder/f'{lang}/card_{n:02}.html').as_uri(),wait_until='load')
            page.evaluate('document.fonts.ready')
            page.wait_for_function("document.querySelector('.z-main').hasAttribute('data-fit')")
            text=norm(page.locator('.body').inner_text())
            assert all(norm(s) in text for s in strings(card)),(label,n,'copy')
            assert page.locator('.z-main').get_attribute('data-fit')=='1.00'
            assert page.locator('.z-main').get_attribute('data-fit-overflow')=='0',(label,n,'overflow')
            assert page.locator('img').evaluate_all('(xs)=>xs.every(x=>x.complete&&x.naturalWidth>0)')
            if label=='after': assert not re.search('[가-힣]',page.locator('.card').inner_text())
            fonts=page.locator('.item p, .copy-text, .doc-note').evaluate_all('(xs)=>xs.map(x=>parseFloat(getComputedStyle(x).fontSize))')
            page.locator('.card').screenshot(path=str(HERE/f'comparison/{label}/card_{n:02}.png'))
            checks.append({'version':label,'page':n,'allJsonCopyVisible':True,'assetsLoaded':True,'overflow':False,'scale':1,'bodyMinCssPx':min(fonts) if fonts else None})
    version=browser.version;browser.close()
for n in range(1,11):
    a=Image.open(HERE/f'comparison/ko/card_{n:02}.png').convert('RGB')
    b=Image.open(HERE/f'comparison/ko-baseline/card_{n:02}.png').convert('RGB')
    assert ImageChops.difference(a,b).getbbox() is None,('Korean pixel change',n)
    if n in [2,4,7,8,9,10]:
        a=Image.open(HERE/f'comparison/before/card_{n:02}.png').convert('RGB')
        b=Image.open(HERE/f'comparison/after/card_{n:02}.png').convert('RGB')
        pair=Image.new('RGB',(2184,1350),'white');pair.paste(a,(0,0));pair.paste(b,(1104,0))
        pair.save(HERE/f'comparison/card-{n:02}-before-after.png')

sections=[]
for a,b,k in zip(old['cards'],new['cards'],ko['cards']):
    n=b['page']
    note='구성도 최신 국문에 맞춰 변경했습니다. 이전과 같은 문구의 디자인만 비교하는 장이 아닙니다.' if n in [4,7,9] else ''
    rows=''.join('<tr><td>'+e(x)+'</td><td>'+e(y)+'</td></tr>' for x,y in zip(strings(k),strings(b)))
    sections.append(f'<section id="card-{n}"><h2>Card {n} · {e(b["headline"])}</h2><p>{note}</p><div class="pair"><figure><figcaption>기존 영문 READABILITY</figcaption><img src="before/card_{n:02}.png" alt="Before card {n}"></figure><figure><figcaption>최신 CARD-FLOW 영문 초안</figcaption><img src="after/card_{n:02}.png" alt="After card {n}"></figure></div><details><summary>최신 국문과 문구 대조</summary><table><tr><th>국문 기준</th><th>영문 현지화</th></tr>{rows}</table><img class="ko" src="ko/card_{n:02}.png" alt="Korean reference card {n}"></details></section>')
write('comparison/index.html','''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OEM 영문 CARD-FLOW 전후 비교</title><style>
body{margin:0;background:#f5f0e8;color:#1b2a67;font-family:system-ui,sans-serif}main{max-width:1050px;margin:auto;padding:26px 18px}p{line-height:1.65}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0}figcaption{font-weight:700;margin-bottom:12px}img{width:100%;display:block}.ko{max-width:420px;margin:20px auto}section{margin:42px 0}table{border-collapse:collapse;width:100%;table-layout:fixed}td,th{border:1px solid #aaa;padding:12px;overflow-wrap:anywhere}summary{cursor:pointer;padding:14px 0}a{color:inherit}.status{border:1px solid #b99a2e;padding:14px}@media(max-width:650px){.pair{grid-template-columns:1fr}main{padding:18px 12px}}
</style><main><h1>최신 CARD-FLOW 영문 현지화</h1><p class="status">별도 검토 초안 · 사용자 승인 전 · 커밋·푸시 없음<br>국문 문구·레이아웃 보존. 원본과 이전 초안은 수정하지 않았습니다.</p><p>국문 최신 버전에 맞춘 영문 10장입니다. 특히 4번 제조번호 대조, 7번 한 장 안의 제출 예외, 9번 문서 예시를 함께 맞췄습니다. 두 영문 버전은 동일 Chromium에서 1080×1350으로 렌더했습니다. 각 장의 펼침 메뉴에서 최신 국문과 영문을 대조할 수 있습니다.</p>'''+''.join(sections)+'''<p><a href="../review.md">검수 결과</a> · <a href="../legal-parity.md">법률 조건 대조</a> · <a href="../assets.md">자산 출처</a></p><p>Emoji graphics: Twemoji © Twitter and contributors, <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Lucide ISC/MIT.</p></main></html>''')
write('comparison/browser-checks.json',json.dumps({'chromium':version,'network':'blocked','koreanPixelMatches':10,'checks':checks},ensure_ascii=False,indent=2))
write('comparison/metrics.json',json.dumps({'before':OLD.name,'koreanSource':KO.name,'protectedFiles':len(hashes),'protectedHashesMatch':True,'koreanCopyUnchanged':True,'koreanPixelMatches':10,'englishCards':10,'cards':[{'page':a['page'],'beforeChars':sum(map(len,strings(a))),'afterChars':sum(map(len,strings(b)))} for a,b in zip(old['cards'],new['cards'])]},ensure_ascii=False,indent=2))
print('20 English renders checked; Korean copy and 10 paired pixel comparisons unchanged; protected',len(hashes),'files')
