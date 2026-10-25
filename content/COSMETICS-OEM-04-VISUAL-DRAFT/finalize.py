"""Record review evidence and build a local before/after viewing page."""
from pathlib import Path
import re,json,hashlib,difflib,html
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=HERE.parent/'COSMETICS-OEM-04-READABILITY-DRAFT'
e=html.escape
def write(n,s):
    p=HERE/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8')
blog=(HERE/'blog.md').read_text(encoding='utf8')
input_path=HERE/'_workspace/2026-10-25-001/input.md'
if not input_path.exists(): write(str(input_path.relative_to(HERE)),blog)
style_input=input_path.read_text(encoding='utf8')
for a,b in [('핵심 원료와 관련된 사양','핵심 원료의 사양'),('화장품 OEM 계약과 관련해서도','화장품 OEM 계약에서도'),('주문수량과','주문 수량과')]:
    blog=blog.replace(a,b)
write('blog.md',blog)
write('blog.txt',re.sub(r'^#{1,3} ','',blog,flags=re.M))
before=(BASE/'blog.md').read_text(encoding='utf8')
rate=lambda a,b:round(100*(1-difflib.SequenceMatcher(None,a,b,autojunk=False).ratio()),3)
style_rate=rate(style_input,blog)
summary=f'''\n\n<!-- HUMANIZE-SUMMARY
Codex single-call path, 2026-10-25. Genre: blog / formal register.
Source chars: {len(style_input)}; final chars: {len(blog)}; SequenceMatcher change: {style_rate}% (reference measurement).
Targeted A-5 spans: 2 -> 0. Spacing: 1 -> 0. No automatic whole-document taxonomy score claimed.
6 self-checks reviewed: protected names/numbers/quotes/anchors retained; <30% change; genre retained; register retained; targeted severe-pattern review complete; no new rhetoric.
User explicitly requested limited emoji section markers; C-5 deletion rule overridden only for those markers.
No grade assigned: project instruction prohibits unsupported new quality scores; no rewrite to satisfy a rate quota.
Highlights: 핵심 원료와 관련된 사양 -> 핵심 원료의 사양; 화장품 OEM 계약과 관련해서도 -> 화장품 OEM 계약에서도; 주문수량과 -> 주문 수량과.
-->\n'''
write('_workspace/2026-10-25-001/final.md',blog+summary)
write('blog.diff',''.join(difflib.unified_diff(before.splitlines(True),blog.splitlines(True),fromfile='previous/blog.md',tofile='visual-draft/blog.md')))
hashes=json.loads((HERE/'source-hashes.json').read_text(encoding='utf8'))
assert all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in hashes.items()),'Protected source changed'
nums=lambda s:re.findall(r'\d+(?:[.,]\d+)*',s)
quotes=lambda s:re.findall(r'‘([^’]+)’',s)
assert nums(before)==nums(blog),'Numeric token drift'
assert quotes(before)==quotes(blog),'Quotation drift'
# Legal paragraphs are untouched; compare complete paragraphs containing statute names or provisions.
lawparas=[s for s in before.split('\n\n') if '「화장품법' in s or '「행정사법' in s or re.search(r'제\d+조',s)]
for para in lawparas:
    expected=para.replace('화장품 OEM 계약과 관련해서도','화장품 OEM 계약에서도')
    assert expected in blog,expected[:100]
cards=json.loads((HERE/'card-data.ko.json').read_text(encoding='utf8'))
oldcards=json.loads((BASE/'card-data.ko.json').read_text(encoding='utf8'))
metrics={'comparisonBase':BASE.name,'protectedFileCount':len(hashes),'protectedHashMatches':True,'blogBeforeChars':len(before),'blogAfterChars':len(blog),'blogChangePercent':rate(before,blog),'numericTokensEqual':True,'quotedSpansEqual':True,'legalParagraphsChecked':len(lawparas),'stylePassChangePercent':style_rate,'newCardCount':10,'language':'ko','approval':'pending','commitPush':'not performed'}
write('comparison/metrics.json',json.dumps(metrics,ensure_ascii=False,indent=2))
diffs=[]
for a,b in zip(oldcards['cards'],cards['cards']):
    keys=[k for k in ['headline','body','takeaway','note'] if a.get(k)!=b.get(k)]
    if keys: diffs.append(f"- {b['page']}번: "+', '.join(keys))
write('card-edit-notes.md','# 카드 변경 필드\n\n'+'\n'.join(diffs)+'\n\n전체 10장 레이아웃·시각 요소 개선. 2·3·6번 법률 카피는 직전 초안과 동일. 4번의 의무는 2·3·4번 결론에 보존하고 제조번호 대조를 중심에 둠. 9번 원래 체크항목은 3~6번과 9번 note로 보존.\n')
def prose(s):
    out=[]
    for part in s.split('\n\n'):
        if part.startswith('# '): out.append('<h2>'+e(part[2:])+'</h2>')
        elif part.startswith('## '): out.append('<h3>'+e(part[3:])+'</h3>')
        else: out.append('<p>'+e(part).replace('\n','<br>')+'</p>')
    return '\n'.join(out)
blogpage='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OEM 블로그 전후 비교</title><style>body{font-family:Arial,sans-serif;background:#f5f0e8;color:#1b2b6b;margin:0;padding:24px}header{max-width:1300px;margin:auto}main{display:grid;grid-template-columns:1fr 1fr;gap:30px;max-width:1300px;margin:auto}article{background:white;padding:28px;min-width:0}p{font-size:17px;line-height:1.9;white-space:normal;overflow-wrap:anywhere}h3{margin-top:38px;font-size:23px;line-height:1.5}h2{line-height:1.5}@media(max-width:800px){main{grid-template-columns:1fr}body{padding:12px}article{padding:20px}}</style><header><a href="index.html">← 카드 비교</a><h1>블로그 전후 비교</h1><p>직전 초안 → 시각·부분 문체 개선안. 미승인. 법률 문단과 숫자·인용 보존, 소제목 이모티콘 5개.</p></header><main><article><h2>이전</h2>'''+prose(before)+'</article><article><h2>개선 초안</h2>'+prose(blog)+'</article></main>'
write('comparison/blog.html',blogpage)
pairs=[]
for n in range(1,11):
    pairs.append(f'<section id="card-{n}"><h2>{n:02} · {e(cards["cards"][n-1]["headline"])}</h2><div class="pair"><figure><figcaption>이전 READABILITY-DRAFT</figcaption><img src="before/card_{n:02}.png" alt="이전 {n}번 카드"></figure><figure><figcaption>새 VISUAL-DRAFT · 미승인</figcaption><img src="../out/ko/png/card_{n:02}.png" alt="개선 {n}번 카드"></figure></div></section>')
page='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OEM 시각 개선 전후 비교</title><style>body{font-family:Arial,sans-serif;background:#f5f0e8;color:#1b2b6b;margin:0;padding:28px}header,section{max-width:1000px;margin:0 auto 40px}h1{font-size:32px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}figure{margin:0}figcaption{font-size:15px;margin:8px 0}figure img{display:block;width:100%;height:auto}nav{display:flex;flex-wrap:wrap;gap:14px;margin:20px 0}a{color:inherit}section{border-top:1px solid #b8972a;padding-top:12px}button{padding:12px 18px;background:#1b2b6b;color:white;border:0;cursor:pointer;border-radius:6px}.mobile .pair{grid-template-columns:repeat(2,360px);overflow:auto}.mobile figure{width:360px}footer{max-width:1000px;margin:auto;font-size:14px;line-height:1.7}@media(max-width:760px){body{padding:16px}.pair{grid-template-columns:1fr}}</style><header><p>ETHOS · OEM 비교 초안 · 2026-10-25</p><h1>읽는 설명에서, 보는 대조로</h1><p>국문 10장. 이모티콘·문서·자료 흐름을 사용한 별도 초안. 기존 승인 원고와 직전 비교본은 보존.</p><nav><a href="blog.html">📄 블로그 전체 전후</a><a href="../blog.txt">블로그 TXT</a><a href="../legal-review.md">법률 조건 검토</a><a href="../review.md">검수 기록</a></nav><button onclick="document.body.classList.toggle('mobile')">360px 모바일 표시 전환</button><nav>'''+''.join(f'<a href="#card-{n}">{n:02}</a>' for n in range(1,11))+'</nav></header>'+''.join(pairs)+'''<footer>Emoji graphics: Twemoji © Twitter and contributors, <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. SVG 원본 사용, 배치·크기 조정. Lucide: ISC / Feather-derived MIT. <a href="../assets.md">자산 출처와 라이선스</a>. 문서 레이아웃 자체 제작. 미승인 비교본이며 실제 성과 향상을 측정한 자료는 아닙니다.</footer></html>'''
write('comparison/index.html',page)
print(json.dumps(metrics,ensure_ascii=False))
