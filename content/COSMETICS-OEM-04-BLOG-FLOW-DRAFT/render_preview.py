from pathlib import Path
import json
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':780,'height':1100},device_scale_factor=2)
    page.route('https://**/*',lambda route:route.abort())
    page.route('http://**/*',lambda route:route.abort())
    page.goto((HERE/'images/document-comparison.html').as_uri());page.evaluate('document.fonts.ready')
    assert page.evaluate('document.fonts.check("18px P")')
    page.locator('.graphic').screenshot(path=str(HERE/'images/document-comparison.png'))
    checks=[]
    for version in ['before','after']:
        page.set_viewport_size({'width':390,'height':1100})
        page.goto((HERE/f'comparison/{version}.html').as_uri());page.evaluate('document.fonts.ready')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert page.evaluate('Array.from(document.images).every(x=>x.complete && x.naturalWidth>0)')
        for section,anchor in [('long','long-section'),('documents','document-section')]:
            page.locator('#'+anchor).evaluate('(e)=>scrollTo(0,e.getBoundingClientRect().top+scrollY-20)')
            # Capture a long, equal-width slice, allowing the inserted figure to be seen.
            y=page.evaluate('scrollY')
            height=min(2500,page.evaluate('document.documentElement.scrollHeight')-y)
            page.screenshot(path=str(HERE/f'comparison/{version}-{section}.png'),full_page=True,clip={'x':0,'y':y,'width':390,'height':height})
        checks.append({'version':version,'width':390,'overflow':False,'imagesLoaded':True,'fontsLoaded':True})
        if version=='after':
            page.locator('figure').evaluate('(e)=>scrollTo(0,e.getBoundingClientRect().top+scrollY-20)')
            page.screenshot(path=str(HERE/'comparison/after-figure-mobile.png'))
        page.set_viewport_size({'width':1280,'height':1000})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.locator('#document-section').evaluate('(e)=>scrollTo(0,e.getBoundingClientRect().top+scrollY-20)')
        page.screenshot(path=str(HERE/f'comparison/{version}-desktop.png'))
        checks.append({'version':version,'width':1280,'overflow':False})
    browser.close()
(HERE/'comparison/render-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print('PASS: local fonts, image load, mobile width, four before/after captures')
