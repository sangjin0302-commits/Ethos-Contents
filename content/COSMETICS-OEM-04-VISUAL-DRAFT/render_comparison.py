"""Same-browser baseline capture, copy visibility checks and comparison screenshots."""
from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'COSMETICS-OEM-04-READABILITY-DRAFT'
d=json.loads((HERE/'card-data.ko.json').read_text(encoding='utf8'))
norm=lambda s:re.sub(r'\s+','',s)
def strings(card):
    for k in ['headline','takeaway','promise','note']:
        if card.get(k):yield card[k]
    for item in card['body']:
        if isinstance(item,str):yield item
        else:yield item['key'];yield item['text']
results=[]
(HERE/'comparison/before').mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(timeout=20000)
    page=browser.new_page(viewport={'width':540,'height':675},device_scale_factor=2)
    page.route('http://**',lambda route:route.abort())
    page.route('https://**',lambda route:route.abort())
    for n in range(1,11):
        page.goto((BASE/f'ko/card_{n:02}.html').as_uri(),wait_until='load',timeout=20000)
        page.evaluate('document.fonts.ready')
        page.locator('.card').screenshot(path=str(HERE/f'comparison/before/card_{n:02}.png'))
        page.goto((HERE/f'ko/card_{n:02}.html').as_uri(),wait_until='load',timeout=20000)
        page.evaluate('document.fonts.ready')
        visible=norm(page.locator('.body').inner_text())
        assert all(norm(s) in visible for s in strings(d['cards'][n-1])),f'copy missing {n}'
        assert page.locator('.z-main').get_attribute('data-fit')=='1.00',f'shrunk {n}'
        assert page.locator('.z-main').get_attribute('data-fit-overflow')=='0',f'overflow {n}'
        assert page.locator('img').evaluate_all('(xs)=>xs.every(x=>x.complete && x.naturalWidth>0)'),f'asset missing {n}'
        sizes=page.locator('.item p').evaluate_all('(xs)=>xs.map(x=>parseFloat(getComputedStyle(x).fontSize))')
        results.append({'page':n,'allJsonCopyVisible':True,'imagesLoaded':True,'fitScale':1,'bodyMinCssPx':min(sizes) if sizes else 23,'bodyMinAt360px':round((min(sizes) if sizes else 23)*360/540,2)})
    page.set_viewport_size({'width':1100,'height':900})
    page.goto((HERE/'comparison/index.html').as_uri())
    for n in [4,7,9,10]:
        page.locator(f'#card-{n}').screenshot(path=str(HERE/f'comparison/card-{n:02}-before-after.png'))
    page.set_viewport_size({'width':390,'height':844})
    page.goto((HERE/'comparison/blog.html').as_uri())
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'blog horizontal overflow'
    page.locator('article').nth(1).scroll_into_view_if_needed()
    page.screenshot(path=str(HERE/'comparison/blog-mobile.png'))
    (HERE/'comparison/browser-checks.json').write_text(json.dumps({'chromium':browser.version,'network':'blocked during render','cards':results,'blog390pxHorizontalOverflow':False},ensure_ascii=False,indent=2),encoding='utf8')
    browser.close()
print('10 same-browser baseline captures; 10 new-card copy/fit/image checks passed; blog mobile width passed')
