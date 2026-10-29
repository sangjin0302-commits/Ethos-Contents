#!/usr/bin/env python3
"""ETHOS 카드뉴스 QA 게이트 + 렌더.

사용:
  python scripts/qa_render.py --html-dir output/html --source source/blog.md
  (예시 검증)  python scripts/qa_render.py --html-dir examples/html --source examples/source/blog-excerpt.md --allow-partial

동작: 모든 카드를 gates.json 기준으로 검사 -> 하나라도 fail 이면 PNG를 내보내지 않고 exit 1.
       전부 통과하면 프로필별 PNG(1:1 또는 4:5), sheet-270.png, qa-report.(json|md) 생성.
필요: pip install playwright pillow && playwright install chromium
"""
import os
import argparse, json, pathlib, re, sys, unicodedata
from playwright.sync_api import sync_playwright
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parent.parent

JS = r"""
() => {
  const card = document.querySelector('.card');
  if (!card) return { error: 'no .card' };
  const cr = card.getBoundingClientRect();
  const canvasW = cr.width, canvasH = cr.height;
  const rect = el => { const r = el.getBoundingClientRect(); return {l:r.left-cr.left,t:r.top-cr.top,r:r.right-cr.left,b:r.bottom-cr.top,w:r.width,h:r.height}; };
  const parse = s => { const m = s.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/); return m ? [+m[1],+m[2],+m[3], m[4]===undefined?1:+m[4]] : [0,0,0,0]; };
  const over = (top, bot) => { const a = top[3]; return [0,1,2].map(i => top[i]*a + bot[i]*(1-a)); };
  const effBg = el => {
    const chain = [];
    for (let e = el; e; e = e.parentElement) {
      const c = parse(getComputedStyle(e).backgroundColor);
      if (c[3] > 0) chain.push(c);
      if (e === card) break;
    }
    if (!chain.length) return [255,255,255];
    let res = chain[chain.length-1].slice(0,3);
    for (let i = chain.length-2; i >= 0; i--) res = over(chain[i], res);
    return res;
  };
  const lines = el => {
    const rg = document.createRange(); rg.selectNodeContents(el);
    const tops = [];
    [...rg.getClientRects()].filter(r => r.width > 0 && r.height > 0).forEach(r => {
      if (!tops.some(t => Math.abs(t - r.top) < r.height*0.5)) tops.push(r.top);
    });
    return tops.length;
  };
  const frameEls = {}; card.querySelectorAll('[data-frame]').forEach(e => { frameEls[e.dataset.frame] = rect(e); });
  const texts = [], problems = [], gradients = [];
  let maxBottom = 0, chars = 0, words = 0;
  card.querySelectorAll('*').forEach(el => {
    const st = getComputedStyle(el), r = rect(el);
    if (!r.w && !r.h) return;
    const isFrame = !!el.closest('[data-frame]');
    if (r.l < -0.5 || r.t < -0.5 || r.r > canvasW + 0.5 || r.b > canvasH + 0.5) problems.push('outside-card:' + (el.className||el.tagName));
    if (el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0 && st.display !== 'inline') problems.push('overflow-x:' + (el.className||el.tagName));
    // A clipped panel can hide text even when the main zone itself fits.
    if (el !== card && !el.matches('[data-zone]') && el.clientHeight > 0 &&
        el.scrollHeight > el.clientHeight + 1 && st.display !== 'inline' &&
        ['hidden','clip','scroll','auto'].includes(st.overflowY) &&
        el.textContent.trim()) problems.push('clipped-text:' + (el.className||el.tagName));
    // title/take zones use intrinsic flex height; the main zone is the only constrained scroll area.
    if (el.matches('[data-zone="main"]') && el.scrollHeight > el.clientHeight + 1) problems.push('zone-overflow:' + el.dataset.zone);
    if (st.backgroundImage && st.backgroundImage !== 'none' && st.backgroundImage.includes('gradient')) gradients.push(el.className||el.tagName);
    const own = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').replace(/\s+/g,' ').trim();
    if (own) {
      const col = parse(st.color);
      const bg = effBg(el);
      const fg = over(col, bg);
      const zoneEl = el.closest('[data-zone]');
      texts.push({
        text: own, size: parseFloat(st.fontSize), weight: parseInt(st.fontWeight)||400, family: st.fontFamily,
        fg, bg, rawColor: col.slice(0,3), alpha: col[3], opacity: parseFloat(st.opacity),
        frame: isFrame, decor: !!el.closest('[data-decor]'),
        role: (el.closest('[data-role]')||{dataset:{}}).dataset.role || '',
        symbolOk: !!el.closest('[data-symbol-ok]'),
        zone: zoneEl ? zoneEl.dataset.zone : '', cls: el.className||el.tagName,
        lines: lines(el)
      });
      if (!isFrame) {
        chars += own.replace(/\s/g,'').length;
        words += own.split(/\s+/).filter(Boolean).length;
      }
    }
    if (!isFrame && !el.matches('.card,.body,[data-zone]') && r.b > maxBottom && (own || el.tagName==='svg' || st.backgroundColor !== 'rgba(0, 0, 0, 0)' || st.borderTopWidth !== '0px')) maxBottom = Math.max(maxBottom, r.b);
  });
  const zone = n => { const z = card.querySelector('[data-zone="'+n+'"]'); return z ? {rect: rect(z), children: z.children.length, inner: [...z.children].map(rect)} : null; };
  const mainZ = zone('main');
  let fill = null;
  if (mainZ && mainZ.inner.length) {
    const used = Math.max(...mainZ.inner.map(x=>x.b)) - Math.min(...mainZ.inner.map(x=>x.t));
    fill = used / mainZ.rect.h;
  }
  const zonesSeen = [...card.querySelectorAll('[data-zone]')].map(z => z.dataset.zone);
  return {
    free: !!document.querySelector('meta[name="ethos-design"][content="free"]'),
    type: card.dataset.cardType || '', bg: card.dataset.bg || '', page: parseInt(card.dataset.page)||0,
    canvas: card.dataset.canvas || 'portrait', visualFamily: card.dataset.visualFamily || 'social-native',
    lang: document.documentElement.lang || '', creamClass: card.classList.contains('cream'),
    size: [cr.width, cr.height], texts, problems, gradients, frameEls, maxBottom, chars, words,
    fill, mainChildren: mainZ ? mainZ.children : 0, zonesSeen,
    hasTake: !!card.querySelector('.take'),
    images: [...card.querySelectorAll('img')].map(img => ({src:img.getAttribute('src')||'', alt:img.getAttribute('alt')||'', loaded:img.complete && img.naturalWidth > 0})),
    fonts: {
      required: (window.__required || []),
    },
    bodyText: [...card.querySelectorAll('*')].filter(e=>!e.closest('[data-frame]')).map(e=>[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('')).join(' ')
  };
}
"""

FOCAL_JS = """() => {
  const card = document.querySelector('.card'); const body = document.querySelector('.body') || card;
  const b = body.getBoundingClientRect(); const area = b.width * b.height;
  const el = card.querySelector('[data-focal]');
  if (!el) return {present:false};
  const r = el.getBoundingClientRect();
  let maxPx = 0;
  [el, ...el.querySelectorAll('*')].forEach(e => {
    for (const n of e.childNodes) if (n.nodeType === 3 && n.textContent.trim()) { maxPx = Math.max(maxPx, parseFloat(getComputedStyle(e).fontSize)); break; }
  });
  const svg = [el, ...el.querySelectorAll('svg')].filter(e => e.tagName && e.tagName.toLowerCase() === 'svg')
    .map(e => e.getBoundingClientRect()).reduce((m, q) => Math.max(m, q.width * q.height), 0);
  return {present:true, areaRatio:(r.width * r.height) / area, maxPx, svgRatio: svg / area};
}"""

# Measure visible ink rather than full-height flex wrappers. This is advisory:
# deliberate asymmetric layouts can declare top/bottom alignment on the main zone.
BALANCE_JS = """() => {
  const z = document.querySelector('[data-zone="main"]');
  if (!z) return null;
  const box = z.getBoundingClientRect(), rects = [];
  const walker = document.createTreeWalker(z, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const n = walker.currentNode;
    if (!n.textContent.trim() || n.parentElement.closest('svg,script,style')) continue;
    const style = getComputedStyle(n.parentElement);
    if (style.visibility === 'hidden' || style.display === 'none' || Number(style.opacity) === 0) continue;
    const range = document.createRange(); range.selectNodeContents(n);
    rects.push(...[...range.getClientRects()].filter(r => r.width && r.height));
  }
  z.querySelectorAll('svg,img').forEach(el => {
    const r = el.getBoundingClientRect(); if (r.width && r.height) rects.push(r);
  });
  if (!rects.length || !box.height) return null;
  const top = Math.min(...rects.map(r => r.top)), bottom = Math.max(...rects.map(r => r.bottom));
  return {topGap:top-box.top, bottomGap:box.bottom-bottom,
    offsetRatio:((top+bottom)-(box.top+box.bottom))/(2*box.height),
    alignment:z.dataset.contentAlign || 'center'};
}"""


def balance_warnings(balance):
    if not balance or balance['alignment'] != 'center':
        return []
    if abs(balance['offsetRatio']) > 0.10 and abs(balance['topGap'] - balance['bottomGap']) > 24:
        return [f"content-balance: 본문 묶음 중심 편차 {balance['offsetRatio']:+.0%} "
                f"(위 {balance['topGap']:.0f}px / 아래 {balance['bottomGap']:.0f}px). "
                "문자 정렬이 아니라 묶음 위치를 확인하세요. 의도한 비대칭은 review.md에 기록합니다."]
    return []


def empty_band(png_path):
    """본문 영역(머리말 아래~꼬리말 위)에서 내용이 없는 가장 긴 가로 띠의 비율. 축소 시트에서 '빈칸'으로 보이는 정도."""
    im = Image.open(png_path).convert('RGB')
    w, h = im.size
    top, bottom = int(h * 0.12), int(h * 0.86)
    px = im.load()
    bg = px[w // 2, int(h * 0.11)]
    xs = range(int(w * 0.06), int(w * 0.94), 3)
    best = run = 0
    for y in range(top, bottom):
        busy = sum(1 for x in xs if sum(abs(a - b) for a, b in zip(px[x, y], bg)) > 40)
        run = run + 1 if busy < 2 else 0
        best = max(best, run)
    return best / max(1, bottom - top)


def lin(c):
    c /= 255
    return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055) ** 2.4

def lum(rgb):
    r, g, b = rgb
    return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b)

def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi+0.05)/(lo+0.05)

def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def norm(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFC', s))

def canvas_profiles(tokens):
    if tokens.get('canvasProfiles'):
        return tokens['canvasProfiles']
    legacy = dict(tokens['canvas'])
    legacy['frame'] = tokens['frame']
    return {'square': legacy}

def emoji_present(s):
    return bool(re.search('[\U0001F300-\U0001FAFF\u2600-\u27BF]', s))

def fit_failures(scale, overflow):
    """Flag text-fitting that conceals an overcrowded design."""
    problems = []
    if overflow == '1':
        problems.append('fit-overflow: content still overflows after font fitting')
    if scale is not None and float(scale) < 0.92:
        problems.append(f'fit-shrink: text scaled to {scale} (<0.92); simplify copy or redesign layout')
    return problems

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--html-dir', default='output/html')
    ap.add_argument('--source', default='source/blog.md')
    ap.add_argument('--gates', default=str(ROOT/'gates.json'))
    ap.add_argument('--tokens', default=str(ROOT/'brand/tokens.json'))
    ap.add_argument('--out', default='output')
    ap.add_argument('--allow-partial', action='store_true', help='예시 검증용: 카드 수·페이지 연속성 게이트 생략')
    a = ap.parse_args()

    G = json.loads(pathlib.Path(a.gates).read_text(encoding='utf-8'))
    T = json.loads(pathlib.Path(a.tokens).read_text(encoding='utf-8'))
    html_dir = pathlib.Path(a.html_dir); out = pathlib.Path(a.out)
    files = sorted(html_dir.glob('card_*.html'))
    if not files:
        sys.exit(f'FAIL: {html_dir} 에 card_NN.html 없음')
    src = norm(pathlib.Path(a.source).read_text(encoding='utf-8')) if pathlib.Path(a.source).exists() else None

    results, cards = [], []
    allowed_text = {hex_rgb(c) for c in T['textColorAllowed']}
    fac = re.compile('|'.join(G['content']['factLock']['patterns']))
    profiles = canvas_profiles(T)
    max_css_width = max(x['cssWidth'] for x in profiles.values())
    max_css_height = max(x['cssHeight'] for x in profiles.values())

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, executable_path=os.environ.get("CHROMIUM_PATH") or None)
        ctx = br.new_context(viewport={'width': max_css_width, 'height': max_css_height}, device_scale_factor=2,
                             locale='ko-KR', timezone_id='Asia/Seoul', color_scheme='light', reduced_motion='reduce')
        # 외부 네트워크 차단: file:// 만 허용
        ctx.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file://') else r.abort())
        for f in files:
            pg = ctx.new_page()
            pg.goto(f.resolve().as_uri(), wait_until='networkidle')
            pg.evaluate('document.fonts.ready')
            pg.evaluate('(list) => Promise.all(list.map(x => document.fonts.load(x)))', T['font']['requiredChecks'])
            font_ok = pg.evaluate('(list) => list.map(x => document.fonts.check(x))', T['font']['requiredChecks'])
            d = pg.evaluate(JS)
            d['file'] = f.name; d['fontOk'] = all(font_ok)
            main_zone = pg.locator('[data-zone="main"]')
            d['fitScale'] = main_zone.get_attribute('data-fit') if main_zone.count() else None
            d['fitOverflow'] = main_zone.get_attribute('data-fit-overflow') if main_zone.count() else None
            cards.append((f, d, pg))
            fails, warns = [], []
            if d['fitScale'] is not None and float(d['fitScale']) < 1:
                warns.append(f"preview-fit: 본문 자동 축소 {d['fitScale']}배; 발행본은 축소 없이 배치를 확인하세요")
            if d.get('error'): fails.append(d['error']); results.append({'card': f.name, 'fails': fails, 'warns': warns}); continue

            profile = profiles.get(d['canvas'])
            if profile is None:
                fails.append(f"canvas-profile: 알 수 없는 프로필 {d['canvas']}")
                profile = profiles[T.get('defaultCanvasProfile', 'portrait')]
            # --- 폰트 ---
            if not d['fontOk']: fails.append('font-load: 필수 로컬 폰트 로드 실패(폴백 금지)')
            fam_ok = re.compile(r'^"?(' + '|'.join(re.escape(x) for x in G['font']['allowedFamilies']) + r')"?(,|$)')
            # --- 크기·프레임 ---
            expected_css = [profile['cssWidth'], profile['cssHeight']]
            if d['size'] != expected_css: fails.append(f"canvas: {d['size']} != {expected_css}")
            fails += d['problems']
            if d.get('free'):
                fails.extend(fit_failures(d['fitScale'], d['fitOverflow']))
            for image in d['images']:
                if not image['alt'].strip(): fails.append(f"image-alt: {image['src']}")
                if not image['loaded']: fails.append(f"image-load: {image['src']}")
            if d['gradients'] and G['style']['noGradient']: fails.append('gradient: ' + ','.join(map(str, d['gradients'][:3])))

            fnt = G['font']; ctr = G['contrast']
            for t in d['texts']:
                tag = f"'{t['text'][:14]}'"
                if not fam_ok.match(t['family']): fails.append(f"font-family: {t['family'][:40]} {tag}")
                if t['size'] < fnt['absoluteMinPx']: fails.append(f"font<{fnt['absoluteMinPx']}px: {t['size']}px {tag}")
                if t['frame']:
                    if t['size'] < fnt['frameMinPx']: fails.append(f"frame-font<{fnt['frameMinPx']}px: {t['size']} {tag}")
                    continue
                need = fnt['labelNoteMinPx'] if t['role'] in ('label', 'note') else fnt['defaultMinPx']
                # 자유 디자인 카드는 본문 하한을 더 높인다(1080px 기준 32px = CSS 16px, 공개 카드뉴스 프로젝트 기준).
                if d.get('free') and t['role'] not in ('label', 'note'): need = max(need, fnt.get('freeDesignMinPx', need))
                if t['role'] == 'headline': need = 22
                if t['size'] < need: fails.append(f"font<{need}px({t['role'] or 'body'}): {t['size']}px {tag}")
                if fnt['noFadedText'] and (t['alpha'] < 0.999 or t['opacity'] < 0.999): fails.append(f"faded-text: alpha={t['alpha']} opacity={t['opacity']} {tag}")
                rgb = tuple(round(v) for v in t['fg'])
                col_raw = tuple(round(v) for v in t['rawColor'])
                if not t['decor']:
                    ratio = contrast(t['fg'], t['bg'])
                    large = t['size'] >= ctr['largeTextPx'] or (t['size'] >= ctr['largeBoldPx'] and t['weight'] >= 700)
                    minr = ctr['largeMin'] if large else ctr['normalMin']
                    if ratio < minr: fails.append(f"contrast {ratio:.1f}<{minr}: {tag} on {tuple(round(v) for v in t['bg'])}")
                    if col_raw not in allowed_text: fails.append(f"text-color-not-in-palette: {col_raw} {tag}")
                    gold = hex_rgb(T['color']['gold'])
                    tolerance = ctr.get('forbiddenColorTolerance', 0)
                    is_gold = all(abs(col_raw[i] - gold[i]) <= tolerance for i in range(3))
                    if (ctr.get('forbidGoldTextOnCream') and d['creamClass'] and is_gold):
                        fails.append(f"gold-text-on-cream: {tag} (네이비 텍스트 또는 네이비 박스 사용)")
                if (d['lang'].lower().startswith('en')
                        and t['role'] in fnt.get('englishSemanticRoles', [])
                        and t['weight'] < fnt.get('englishSemanticMinWeight', 700)):
                    fails.append(f"english-weight<{fnt.get('englishSemanticMinWeight', 700)}({t['role']}): {t['weight']} {tag}")
                if not t['symbolOk']:
                    for s in G['style']['forbiddenSymbols']:
                        if s in t['text']: fails.append(f"symbol '{s}' 미승인(원문 논리 왜곡 위험): {tag}")
                if G['style']['noEmoji'] and emoji_present(t['text']): fails.append(f"emoji: {tag}")
            # --- 레이아웃 ---
            L = G['layout']
            balance = pg.evaluate(BALANCE_JS) if d.get('free') else None
            warns.extend(balance_warnings(balance))
            for z in L['zonesRequired']:
                if z not in d['zonesSeen']: fails.append(f'zone-missing: {z}')
            if d['mainChildren'] > L['mainChildrenMax']: warns.append(f"main-zone 블록 {d['mainChildren']} > 권장 {L['mainChildrenMax']}")
            if d['fill'] is not None and d['fill'] < L['mainZoneMinFillRatio']: warns.append(f"main-fill {d['fill']:.2f} < 권장 {L['mainZoneMinFillRatio']} (여백이 의도적인지 시각 확인)")
            profile_frame = profile.get('frame', T['frame'])
            gap = profile_frame['expected']['org']['top'] - d['maxBottom']
            if gap < L.get('minFooterGapPx', 0): fails.append(f"footer-gap {gap:.0f}px < 최소 {L.get('minFooterGapPx')}px")
            if gap > L['maxBottomGapPx']: warns.append(f"bottom-gap {gap:.0f}px > 권장 {L['maxBottomGapPx']}px (여백 균형 확인)")
            # --- 시각 중심(권고): 표지·마지막 장을 뺀 카드마다 [data-focal] 하나, 충분히 크게 ---
            if d.get('free') and d['type'] not in ('cover', 'cta'):
                focal = pg.evaluate(FOCAL_JS)
                F = L.get('focal', {})
                strong = focal.get('present') and (focal['maxPx'] >= F.get('minPx', 36) or focal['svgRatio'] >= F.get('minSvgRatio', 0.04)
                                                   or focal['areaRatio'] >= F.get('minAreaRatio', 0.30))
                d['focalStrong'] = bool(strong)
                if not focal.get('present'):
                    warns.append("no-focal: 시각 중심([data-focal])이 없습니다. 큰 숫자·핵심어·아이콘 중 하나를 크게 두세요")
                elif not strong:
                    warns.append(f"weak-focal: 시각 중심이 작습니다(글자 {focal['maxPx']:.0f}px, 아이콘 {focal['svgRatio']:.0%}). 36px 이상 글자나 큰 아이콘으로")
            # --- 텍스트 예산 ---
            budget_root = G['budget']
            lang_key = 'en' if d['lang'].lower().startswith('en') else 'ko'
            B = dict(budget_root)
            B.update(budget_root.get('byLanguage', {}).get(lang_key, {}))
            if d['chars'] > B['maxCharsPerCard']:
                level = '강한 경고' if d['chars'] > B.get('hardCharsPerCard', 10**9) else '권고'
                warns.append(f"chars {d['chars']} > {level} {B['maxCharsPerCard']} (문장 압축 또는 카드 분리 검토)")
            if B.get('maxWordsPerCard') and d['words'] > B['maxWordsPerCard']:
                level = '강한 경고' if d['words'] > B.get('hardWordsPerCard', 10**9) else '권고'
                warns.append(f"words {d['words']} > {level} {B['maxWordsPerCard']} (영문 호흡과 모바일 가독성 확인)")
            for t in d['texts']:
                if t['frame']: continue
                if t['role'] == 'headline':
                    lim = B['coverHeadlineMaxLines'] if d['type'] == 'cover' else B['headlineMaxLines']
                    if t['lines'] > lim: warns.append(f"headline-lines {t['lines']} > 권장 {lim}: '{t['text'][:14]}'")
            hl = [t for t in d['texts'] if t['role'] == 'headline' and not t['frame']]
            if hl and d['type'] != 'cover':
                n = sum(len(t['text'].replace(' ', '')) for t in hl)
                if n > B['maxHeadlineChars']: warns.append(f"headline-chars {n} > 권장 {B['maxHeadlineChars']}")
                headline_words = sum(len(t['text'].split()) for t in hl)
                if B.get('maxHeadlineWords') and headline_words > B['maxHeadlineWords']:
                    warns.append(f"headline-words {headline_words} > 권장 {B['maxHeadlineWords']}")
            for t in d['texts']:
                if not t['frame'] and t['role'] not in ('headline',) and t['lines'] > B['paragraphMaxLines']:
                    warns.append(f"paragraph-lines {t['lines']} > 권장 {B['paragraphMaxLines']}: '{t['text'][:14]}'")
            # --- 프레임 좌표/골드바 ---
            fe, ex, tol = d['frameEls'], profile_frame['expected'], L['frameTolerancePx']
            for name in ('wordmark', 'section', 'line', 'org', 'tagline', 'page'):
                if name not in fe: fails.append(f'frame-missing: {name}'); continue
                e, r = ex[name], fe[name]
                for k, v in e.items():
                    actual = {'left': r['l'], 'top': r['t'], 'right': r['r'], 'height': r['h']}[k]
                    if abs(actual - v) > tol: fails.append(f"frame-drift {name}.{k}: {actual:.1f} != {v}")
            for nm, key in (('gold-top', 'goldTop'), ('gold-bottom', 'goldBottom')):
                if nm not in fe: fails.append(f'frame-missing: {nm}'); continue
                if abs(fe[nm]['h'] - profile_frame[key]['height']) > tol or abs(fe[nm]['t'] - profile_frame[key]['top']) > tol:
                    fails.append(f"gold-bar {nm}: h={fe[nm]['h']} top={fe[nm]['t']}")
            # --- 콘텐츠 ---
            body_txt = d['bodyText']
            for s in G['content']['forbiddenStrings']:
                if s.lower() in body_txt.lower(): fails.append(f"forbidden-string: '{s}'")
            if G['content']['factLock']['enabled']:
                if src is None: fails.append('fact-lock: --source 파일 없음')
                else:
                    for m in sorted(set(x.group(0) for x in fac.finditer(body_txt))):
                        if norm(m) not in src: fails.append(f"fact-lock: '{m}' 가 원문에 없음")
            contrast_samples = []
            for t in d['texts']:
                if t['frame'] or t['decor'] or t['role'] not in ('headline', 'subheading', 'takeaway'):
                    continue
                large = t['size'] >= ctr['largeTextPx'] or (t['size'] >= ctr['largeBoldPx'] and t['weight'] >= 700)
                contrast_samples.append({
                    'text': t['text'], 'role': t['role'], 'class': str(t['cls']),
                    'rawColor': [round(v) for v in t['rawColor']],
                    'background': [round(v) for v in t['bg']],
                    'ratio': round(contrast(t['fg'], t['bg']), 2),
                    'requiredRatio': ctr['largeMin'] if large else ctr['normalMin'],
                })
            results.append({'card': f.name, 'type': d['type'], 'page': d['page'], 'canvas': d['canvas'], 'visualFamily': d['visualFamily'], 'fails': fails, 'warns': warns,
                            'fitScale': d['fitScale'], 'fitOverflow': d['fitOverflow'],
                            'chars': d['chars'], 'words': d['words'], 'fill': None if d['fill'] is None else round(d['fill'], 2),
                            'bottomGap': round(gap), 'contentBalance': balance, 'contrastSamples': contrast_samples})

        # --- 세트 게이트 ---
        set_fails, set_warns = [], []
        S = G['set']
        types = [d['type'] for _, d, _ in cards]
        profile_names = [d['canvas'] for _, d, _ in cards]
        if len(set(profile_names)) > 1:
            set_fails.append('canvas-profile: 한 세트에서 프로필 혼용 금지')
        if not a.allow_partial:
            if not (S['cardCount']['min'] <= len(cards) <= S['cardCount']['max']):
                set_fails.append(f"card-count {len(cards)} not in {S['cardCount']['min']}-{S['cardCount']['max']}")
            if S['pageNumbersSequential'] and [d['page'] for _, d, _ in cards] != list(range(1, len(cards) + 1)):
                set_fails.append('page-numbers: 1..N 연속 아님')
            advisory = G.get('compositionAdvisory', {})
            distinct = len(set(types))
            if distinct < advisory.get('minDistinctTypes', 0):
                set_warns.append(f"distinct-types {distinct} < 권장 {advisory['minDistinctTypes']} (내용에 맞는 구성이면 허용)")
            max_share = advisory.get('maxTypeShare')
            if max_share and types:
                dominant = max(set(types), key=types.count)
                share = types.count(dominant) / len(types)
                if share > max_share:
                    set_warns.append(f"type-share {dominant} {share:.0%} > 권장 {max_share:.0%} (반복감 시각 확인)")
            for recommended_type in advisory.get('recommendedTypes', []):
                if recommended_type not in types:
                    set_warns.append(f"recommended-type {recommended_type} 없음 (원문에 실제 내용이 없으면 추가하지 않음)")
        run = 1
        for i in range(1, len(types)):
            run = run + 1 if types[i] == types[i - 1] else 1
            if run > S['maxConsecutiveSameType']: set_warns.append(f"same-type x{run}: {types[i]} (연속 권장 {S['maxConsecutiveSameType']}장)")
        ratio = sum(1 for _, d, _ in cards if d['hasTake']) / len(cards)
        if len(cards) >= 4 and ratio > S['takeawayBarMaxRatio']:
            set_warns.append(f"takeaway-bar {ratio:.0%} > 권장 {S['takeawayBarMaxRatio']:.0%} (같은 골격 반복 여부 확인)")

        inner = [d for _, d, _ in cards if d.get('free') and d.get('type') not in ('cover', 'cta')]
        if inner:
            share = sum(1 for d in inner if d.get('focalStrong')) / len(inner)
            want = G['layout'].get('focal', {}).get('minSetShare', 0.6)
            if share < want:
                set_warns.append(f"focal {share:.0%} < 권장 {want:.0%} (본문 카드 중 시각 중심이 뚜렷한 장의 비율. 목록만 이어지면 양식집처럼 보인다)")
        all_pass = all(not r['fails'] for r in results) and not set_fails
        pngdir = out / 'png'
        if all_pass:
            pngdir.mkdir(parents=True, exist_ok=True)
            for f, d, pg in cards:
                dst = pngdir / (f.stem + '.png')
                pg.locator('.card').screenshot(path=str(dst), animations='disabled', caret='hide')
                profile = profiles[d['canvas']]
                if Image.open(dst).size != (profile['pngWidth'], profile['pngHeight']):
                    set_fails.append(f'png-size {dst.name}'); all_pass = False
                band = empty_band(dst)
                limit = G['layout'].get('maxEmptyBand', 0.22)
                for r in results:
                    if r['card'] == f.name:
                        r['emptyBand'] = round(band, 2)
                        if band > limit:
                            r['warns'].append(f"empty-band {band:.0%} > 권장 {limit:.0%} (의도한 여백인지 확인: 관련 요소의 묶음·중앙 위치를 먼저 보고, 간격이나 장식으로 억지로 채우지 않는다)")
            if all_pass:
                W, gsz = 270, 8
                sample_profile = profiles[profile_names[0]]
                H = round(W * sample_profile['pngHeight'] / sample_profile['pngWidth'])
                cols = min(5, len(cards)); rows = -(-len(cards) // cols)
                sheet = Image.new('RGB', (cols * W + (cols - 1) * gsz, rows * H + (rows - 1) * gsz), (120, 120, 120))
                for i, (f, _, _) in enumerate(cards):
                    im = Image.open(pngdir / (f.stem + '.png')).convert('RGB').resize((W, H), Image.LANCZOS)
                    sheet.paste(im, ((i % cols) * (W + gsz), (i // cols) * (H + gsz)))
                sheet.save(out / 'sheet-270.png')
        for _, _, pg in cards: pg.close()
        br.close()

    out.mkdir(parents=True, exist_ok=True)
    report = {'allPass': all_pass, 'setFails': set_fails, 'setWarnings': set_warns, 'cards': results, 'humanChecks': G['humanChecks'],
              'gatesVersion': G['version'], 'calibration': G['calibration'], 'pngWritten': all_pass}
    (out / 'qa-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
    md = ['# QA Report', '', f"결과: {'PASS — PNG 생성됨' if all_pass else 'FAIL — PNG 생성 안 됨'}", '']
    if set_fails: md += ['## 세트 실패'] + [f'- {x}' for x in set_fails] + ['']
    if set_warns: md += ['## 세트 권고'] + [f'- {x}' for x in set_warns] + ['']
    md += ['| 카드 | 유형 | 글자수 | 단어수 | 본문 채움 | 하단 여백 | 결과 |', '|---|---|---:|---:|---:|---:|---|']
    for r in results:
        md.append(f"| {r['card']} | {r.get('type','')} | {r.get('chars','')} | {r.get('words','')} | {r.get('fill','')} | {r.get('bottomGap','')} | {'PASS' if not r['fails'] else 'FAIL'} |")
    for r in results:
        if r['fails']: md += ['', f"### {r['card']}"] + [f'- {x}' for x in r['fails']]
        if r['warns']: md += ['', f"### {r['card']} 권고"] + [f'- {x}' for x in r['warns']]
    md += ['', '## 사람이 확인할 것 (자동화 불가)'] + [f'- [ ] {x}' for x in G['humanChecks']]
    md += ['', f"게이트 v{G['version']} · 기준은 초기 가설({G['calibration']})"]
    (out / 'qa-report.md').write_text('\n'.join(md), encoding='utf-8')
    print('\n'.join(x for x in md if not x.startswith('- [ ]')))
    sys.exit(0 if all_pass else 1)

if __name__ == '__main__':
    main()
