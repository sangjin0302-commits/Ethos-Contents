"""Package actual before/after PNGs and inspect computed legal-card typography.
Run baseline QA into _verification/oem-before/{ko,en} and draft QA first.
"""
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / 'comparison'
OUT.mkdir(exist_ok=True)
measurements = {}
for lang in ('ko', 'en'):
    before = ROOT / '_verification' / 'oem-before' / lang
    after = HERE / 'out' / lang
    reports = [json.loads((p / 'qa-report.json').read_text(encoding='utf-8')) for p in (before, after)]
    if not all(r['allPass'] for r in reports):
        raise SystemExit('Only compare current passing renders')
    for page in (3, 7):
        shutil.copyfile(before / 'png' / f'card_{page:02d}.png', OUT / f'before-{lang}-{page}.png')
    shutil.copyfile(before / 'sheet-270.png', OUT / f'before-{lang}-sheet.png')
    measurements[lang] = {'beforeQA': reports[0], 'afterQA': reports[1], 'computedType': {}}

html = '''<!doctype html><html lang="ko"><meta charset="utf-8"><title>OEM 별도 초안 — 실제 렌더 비교</title>
<link rel="stylesheet" href="../../../brand/fonts.css"><style>
*{box-sizing:border-box}body{margin:0;background:#eceae4;color:#1b2b6b;font-family:Pretendard,sans-serif}
main{width:1160px;margin:auto}h1{font-size:28px;margin:0 0 8px}p{margin:8px 0 18px;line-height:1.5}
.board{padding:24px;background:#eceae4}.row{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
figure{margin:0}figcaption{font-weight:700;font-size:17px;margin-bottom:10px}img{display:block;width:100%;height:auto}
h2{font-size:22px;margin:0 0 14px}.sheet{padding:24px}a{color:inherit}
</style><main>'''
for name, old, pages, title in [('legal',7,[7,8],'제출 의무와 영업비밀 예외를 두 장으로'),('testing',3,[3,4],'검사 생략 조건과 남는 의무를 두 장으로')]:
    html += f'<section class="board" id="{name}"><h1>{title}</h1><p>같은 Chromium · 540 × 675 CSS px · 원본 PNG 1080 × 1350. 별도 미승인 비교 초안.</p><div class="row">'
    html += f'<figure><figcaption>기존 {old}번</figcaption><img src="before-ko-{old}.png"></figure>'
    for page in pages:
        html += f'<figure><figcaption>새 초안 {page}번</figcaption><img src="../out/ko/png/card_{page:02d}.png"></figure>'
    html += '</div></section>'
for lang in ('ko', 'en'):
    for label, src in [('기존',f'before-{lang}-sheet.png'),('새 초안',f'../out/{lang}/sheet-270.png')]:
        html += f'<section class="sheet"><h2>{lang.upper()} · {label} 10장 전체</h2><img src="{src}"></section>'
html += '</main></html>'
(OUT / 'index.html').write_text(html, encoding='utf-8')
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1160, 'height': 850}, device_scale_factor=1)
    page.goto((OUT / 'index.html').as_uri())
    page.evaluate('document.fonts.ready')
    page.locator('#legal').screenshot(path=str(OUT / 'legal-before-after.png'))
    page.locator('#testing').screenshot(path=str(OUT / 'testing-before-after.png'))
    for lang in ('ko', 'en'):
        for version, folder, pages, selector in [
            ('before', ROOT / 'content' / 'COSMETICS-OEM-04', (3,7), '.krow-t'),
            ('after', HERE, (3,4,7,8), '.copy-text')]:
            for number in pages:
                page.goto((folder / lang / f'card_{number:02d}.html').as_uri())
                page.evaluate('document.fonts.ready')
                measurements[lang]['computedType'][f'{version}-{number}'] = page.locator(selector).evaluate_all(
                    '(es)=>es.map(e=>({text:e.innerText,fontPx:parseFloat(getComputedStyle(e).fontSize),lineHeightPx:parseFloat(getComputedStyle(e).lineHeight)}))')
    browser.close()
(OUT / 'render-comparison.json').write_text(json.dumps(measurements, ensure_ascii=False, indent=2), encoding='utf-8')
print(OUT / 'index.html')
