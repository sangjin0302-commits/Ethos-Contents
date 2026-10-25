"""Render both versions in one browser and record protection/copy/layout evidence."""
from pathlib import Path
import json, re, hashlib, html
from playwright.sync_api import sync_playwright
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = HERE.parent/'COSMETICS-OEM-04-VISUAL-DRAFT'
CHANGED = (2,7,8,9)
e = html.escape
norm = lambda s: re.sub(r'\s+', '', s)

def strings(c):
    for k in ('headline','promise','note','takeaway'):
        if c.get(k): yield c[k]
    for x in c['body']:
        if isinstance(x,str): yield x
        else: yield x['key']; yield x['text']

def write(name, value):
    p = HERE/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(value,encoding='utf-8')

before = json.loads((BASE/'card-data.ko.json').read_text(encoding='utf-8'))
after = json.loads((HERE/'card-data.ko.json').read_text(encoding='utf-8'))
hashes = json.loads((HERE/'source-hashes.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in hashes.items())
assert (BASE/'blog.md').read_bytes()==(HERE/'blog.md').read_bytes()
for a,b in zip(before['cards'],after['cards']):
    if a['page'] not in CHANGED: assert a==b

checks=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':540,'height':675},device_scale_factor=2)
    page.route('http://**',lambda r:r.abort())
    page.route('https://**',lambda r:r.abort())
    for label,folder,data in [('before',BASE,before),('after',HERE,after)]:
        (HERE/f'comparison/{label}').mkdir(parents=True,exist_ok=True)
        for c in data['cards']:
            n=c['page']
            page.goto((folder/f'ko/card_{n:02}.html').as_uri(),wait_until='load')
            page.evaluate('document.fonts.ready')
            page.wait_for_function("document.querySelector('.z-main').hasAttribute('data-fit')")
            visible=norm(page.locator('.body').inner_text())
            assert all(norm(s) in visible for s in strings(c)), (label,n,'copy')
            assert page.locator('img').evaluate_all('(xs)=>xs.every(x=>x.complete&&x.naturalWidth>0)')
            assert page.locator('.z-main').get_attribute('data-fit')=='1.00'
            assert page.locator('.z-main').get_attribute('data-fit-overflow')=='0', (label,n,'overflow')
            stats=page.locator('.item p').evaluate_all('xs=>xs.map(x=>{const s=getComputedStyle(x);return {fontPx:parseFloat(s.fontSize),lines:Math.round(x.getBoundingClientRect().height/parseFloat(s.lineHeight))}})')
            page.locator('.card').screenshot(path=str(HERE/f'comparison/{label}/card_{n:02}.png'))
            checks.append({'version':label,'page':n,'allCopyVisible':True,'imagesLoaded':True,'fitScale':1,'overflow':False,'paragraphs':stats})
    chromium=browser.version
    browser.close()

metrics=[]
for a,b in zip(before['cards'],after['cards']):
    if a['page'] not in CHANGED: continue
    sa=''.join(strings(a)); sb=''.join(strings(b))
    metrics.append({'page':a['page'],'beforeChars':len(sa),'afterChars':len(sb),'beforeMiddleDots':sa.count('·'),'afterMiddleDots':sb.count('·')})
write('comparison/metrics.json',json.dumps({'baseline':BASE.name,'protectedFiles':len(hashes),'allHashesMatch':True,'blogUnchanged':True,'unchangedCards':[1,3,4,5,6,10],'cards':metrics},ensure_ascii=False,indent=2))
write('comparison/browser-checks.json',json.dumps({'chromium':chromium,'network':'blocked','checks':checks},ensure_ascii=False,indent=2))
sections=[]
for n in CHANGED:
    a=before['cards'][n-1]; b=after['cards'][n-1]
    notes=[]
    for k in ('headline','body','note','takeaway'):
        if a.get(k)!=b.get(k):
            notes.append('<tr><th>'+e(k)+'</th><td>'+e(json.dumps(a.get(k),ensure_ascii=False))+'</td><td>'+e(json.dumps(b.get(k),ensure_ascii=False))+'</td></tr>')
    sections.append(f'<section id="card-{n}"><h2>카드 {n}</h2><div class="pair"><figure><figcaption>기존 VISUAL</figcaption><img src="before/card_{n:02}.png" alt="기존 카드 {n}"></figure><figure><figcaption>문장·배치 개선 초안</figcaption><img src="after/card_{n:02}.png" alt="개선 카드 {n}"></figure></div><details><summary>문구 변경 보기</summary><table><tr><th>구간</th><th>기존</th><th>초안</th></tr>{"".join(notes)}</table></details></section>')
write('comparison/index.html','''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OEM 카드 문장 전후 비교</title><style>
body{font-family:system-ui,sans-serif;margin:0;background:#f5f0e8;color:#1b2a67}main{max-width:1040px;margin:auto;padding:28px 18px}h1{font-size:28px}p{line-height:1.7}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0}figcaption{font-weight:700;margin-bottom:10px}img{width:100%;display:block}section{margin:42px 0}table{border-collapse:collapse;table-layout:fixed;width:100%;font-size:14px}td,th{border:1px solid #aaa;padding:10px;overflow-wrap:anywhere}summary{cursor:pointer;padding:14px 0}a{color:inherit}.status{padding:15px;border:1px solid #b99a2e}@media(max-width:650px){.pair{grid-template-columns:1fr}main{padding:18px 12px}}
</style><main><h1>OEM 카드 2·7~9 문장·배치 비교</h1><p class="status">사용자 채택 버전 · 공통 지침 반영 · 실제 발행은 별도<br>기존 승인 원고와 나머지 6장 보존. 두 버전은 동일 Chromium에서 1080×1350으로 렌더했습니다.</p><p>2번은 역할 설명을 넓은 행으로, 7번은 제출 원칙과 예외를 문장으로, 8번은 세 조건을 완결된 설명으로 정리했습니다. 9번의 원문 인용은 그대로 두고 상황별 확인 행동을 풀었습니다. 글자를 자동 축소하지 않았습니다.</p>'''+''.join(sections)+'<p><a href="../review.md">검수·같은 기준 재평가</a> · <a href="../legal-review.md">법률 조건 대조</a> · <a href="metrics.json">측정 지표</a></p><p>Emoji graphics: Twemoji © Twitter and contributors, CC BY 4.0. https://creativecommons.org/licenses/by/4.0/ · Lucide ISC/MIT. 출처와 라이선스: ../assets.md</p></main></html>')
summary = (HERE/'comparison/summary.html').read_text(encoding='utf-8')
index = (HERE/'comparison/index.html').read_text(encoding='utf-8')
write('comparison/index.html', index.replace('<section id=', summary+'<section id=', 1))
# Pair images contain only the two genuine rendered cards, no image editing.
for n in CHANGED:
    images=[Image.open(HERE/f'comparison/{v}/card_{n:02}.png').convert('RGB') for v in ('before','after')]
    canvas=Image.new('RGB',(2184,1350),'white')
    canvas.paste(images[0],(0,0));canvas.paste(images[1],(1104,0))
    canvas.save(HERE/f'comparison/card-{n:02}-before-after.png')
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
    page.goto((HERE/'comparison/index.html').as_uri())
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    browser.close()
print('20 same-browser renders verified; all protected files match; four comparisons created')
