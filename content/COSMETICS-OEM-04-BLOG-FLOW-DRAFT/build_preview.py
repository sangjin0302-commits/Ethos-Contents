from pathlib import Path
import re, json, hashlib, html, difflib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=HERE.parent/'COSMETICS-OEM-04-VISUAL-DRAFT'
def write(name,s):
    p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
protected=[HERE.parent/n for n in ['COSMETICS-OEM-04','COSMETICS-OEM-04-READABILITY-DRAFT','COSMETICS-OEM-04-VISUAL-DRAFT']]
if not (HERE/'source-hashes.json').exists():
    write('source-hashes.json',json.dumps({str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for f in protected for p in f.rglob('*') if p.is_file()},ensure_ascii=False,indent=2))
before=(BASE/'blog.md').read_text(encoding='utf-8')
after=before
insertions=[
('계약서에 ‘시험성적서 제공’이라고 적었다면','### 검사자료를 언제, 누구에게 받을지 정하기\n\n'),
('자료를 요청하고 확인할 업무는 이처럼','### 판매 후 문의에도 자료를 찾을 수 있도록\n\n'),
('「화장품법 시행규칙」 제12조제10호는','### 고객 문의와 법정 보고·안전조치 구분하기\n\n'),
('이 예외를 적용하려면 제조업체가','### 영업비밀 예외가 적용되는 범위 확인하기\n\n'),
('제품을 납품받은 뒤 문제가 확인됐다면','### 거래상 비용 부담과 법정 의무 나눠 보기\n\n'),
('견적서에는 ‘품질검사 포함’, OEM 계약서','### 세 문서를 놓고 자료 전달의 빈칸 찾기\n\n')]
for anchor,heading in insertions:
    assert after.count(anchor)==1,anchor
    after=after.replace(anchor,heading+anchor)
splits=[
('받기로 한 물량에는','받기로 한 물량에는'),
('시험성적서라는 이름의 파일 하나로','시험성적서라는 이름의 파일 하나로'),
('제품을 판매한 뒤 고객이','제품을 판매한 뒤 고객이'),
('소비자의 불편 호소만으로','소비자의 불편 호소만으로'),
('모든 고객 문의가 곧바로','모든 고객 문의가 곧바로'),
('후자라 하더라도 어떤 정보가','후자라 하더라도 어떤 정보가'),
('법에서 인정하는 예외는','법에서 인정하는 예외는'),
('당사자 사이의 비용 부담과','당사자 사이의 비용 부담과')]
for anchor,_ in splits:
    assert after.count(' '+anchor)==1,anchor
    after=after.replace(' '+anchor,'\n\n'+anchor)
image_alt='원문 예시: 견적서의 품질검사 포함, 계약서의 납품 후 대금 지급, 품질관리규정의 책임판매관리자가 검사자료를 확인. 세 문서에서 자료를 누구에게 언제 전달하는지 확인합니다.'
anchor='제조업체가 어떤 자료를 언제 줄지는 계약서에 적습니다.'
after=after.replace(anchor,f'![{image_alt}](images/document-comparison.png)\n\n'+anchor)
write('blog.md',after)
write('blog.txt',re.sub(r'^#{1,3} ','',after,flags=re.M).replace(f'![{image_alt}](images/document-comparison.png)',f'[문서 비교 이미지 삽입: images/document-comparison.png]\n대체 텍스트: {image_alt}'))
write('blog.diff',''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='VISUAL-DRAFT/blog.md',tofile='BLOG-FLOW-DRAFT/blog.md')))

# Headings and an illustrative figure are added; source prose remains byte-for-byte
# identical after whitespace normalization, including quotes, numbers and conditions.
def prose_only(s):
    return re.sub(r'\s+','', '\n'.join(l for l in s.splitlines() if not l.startswith(('#','![')) ))
assert prose_only(before)==prose_only(after),'Source prose drift'
for name,sha in json.loads((HERE/'source-hashes.json').read_text(encoding='utf-8')).items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
metrics={'source':BASE.name,'sourceProseEqualIgnoringWhitespace':True,'newSubheadings':len(insertions),'paragraphSplits':len(splits),'newFigures':1,'originalFileCount':len(json.loads((HERE/'source-hashes.json').read_text())),'protectedHashesMatch':True,'commitPush':'not performed'}
write('comparison/metrics.json',json.dumps(metrics,ensure_ascii=False,indent=2))

font='../../../fonts/Pretendard-Regular.woff2'
bold='../../../fonts/Pretendard-Bold.woff2'
css=f'''@font-face{{font-family:P;src:url("{font}")}}@font-face{{font-family:P;src:url("{bold}");font-weight:700}}*{{box-sizing:border-box}}body{{margin:0;font-family:P,sans-serif;color:#202a44;background:#f3f0e9}}a{{color:#1b2b6b}}header{{padding:22px;max-width:850px;margin:auto}}article{{max-width:760px;margin:auto;background:white;padding:38px}}h1{{font-size:29px;line-height:1.5}}h2{{font-size:25px;line-height:1.5;margin:54px 0 22px;color:#1b2b6b}}h3{{font-size:20px;line-height:1.6;border-left:3px solid #b8972a;padding-left:14px;margin:36px 0 18px;color:#1b2b6b}}p{{font-size:18px;line-height:1.95;margin:0 0 25px;overflow-wrap:anywhere;word-break:keep-all}}figure{{margin:32px 0}}figure img{{display:block;width:100%;height:auto}}figcaption{{font-size:13px;color:#566176;line-height:1.6;margin-top:10px}}@media(max-width:600px){{article{{padding:24px}}h1{{font-size:25px}}h2{{font-size:23px}}h3{{font-size:19px}}p{{font-size:17px;line-height:1.9}}}}'''
def render(md):
    chunks=[]
    for block in md.split('\n\n'):
        if block.startswith('!['):chunks.append(f'<figure><img src="../images/document-comparison.png" alt="{html.escape(image_alt)}"></figure>');continue
        tag='p';text=block
        for prefix,t in [('### ','h3'),('## ','h2'),('# ','h1')]:
            if block.startswith(prefix):tag=t;text=block[len(prefix):];break
        ident=' id="long-section"' if text.startswith('📦') else (' id="document-section"' if text.startswith('📄 다시') else '')
        chunks.append(f'<{tag}{ident}>'+html.escape(text).replace('\n','<br>')+f'</{tag}>')
    return '\n'.join(chunks)
for name,md,label in [('before',before,'이전 VISUAL-DRAFT'),('after',after,'개선 BLOG-FLOW-DRAFT')]:
    write(f'comparison/{name}.html',f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{label}</title><style>{css}</style><header><a href="index.html">← 전후 비교</a><p>{label} · 미발행 비교본</p></header><article>'+render(md)+'</article></html>')

figure='''<!doctype html><html lang="ko"><meta charset="utf-8"><style>'''+css+'''body{background:#f4f0e8}.graphic{width:620px;padding:32px}.eyebrow{font-size:20px;letter-spacing:2px;color:#967919;margin-bottom:18px}h1{font-size:38px;margin:0 0 14px} .intro{font-size:23px;line-height:1.65;margin-bottom:30px}.doc{background:#fff;border:1px solid #ddd7ca;padding:22px 20px;margin:15px 0;display:grid;grid-template-columns:130px 1fr;align-items:center;gap:18px;border-radius:4px}.doc b{font-size:27px;color:#1b2b6b}.doc p{font-size:29px;line-height:1.5;margin:0}.foot{background:#1b2b6b;color:white;padding:27px 30px;margin-top:30px}.foot strong{font-size:27px;line-height:1.6}.note{font-size:22px;line-height:1.65;color:#576070;margin-top:23px}</style><div class="graphic"><div class="eyebrow">ETHOS · OEM 문서 대조</div><h1>같은 거래, 서로 다른 문구</h1><p class="intro">세 문서에서 자료 전달의 빈칸을 찾아보세요.</p><div class="doc"><b>견적서</b><p>‘품질검사 포함’</p></div><div class="doc"><b>계약서 초안</b><p>‘납품 후 대금 지급’</p></div><div class="doc"><b>품질관리<br>규정</b><p>‘책임판매관리자가<br>검사자료를 확인’</p></div><div class="foot"><strong>검사자료를 누구에게 언제 보내고,<br>회사에서는 누가 받아 살펴볼까요?</strong></div><div class="note">본문에 등장하는 예시 문구를 재구성했습니다.</div></div></html>'''
write('images/document-comparison.html',figure)
write('comparison/index.html','''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OEM 블로그 읽기 흐름 전후 비교</title><style>'''+css+'''main{max-width:1000px;margin:auto;padding:24px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}.pair img{width:100%;height:auto}nav{display:flex;gap:20px;flex-wrap:wrap;margin:20px 0}figure{margin:0}section{margin-bottom:60px}small{line-height:1.6}@media(max-width:650px){.pair{grid-template-columns:1fr}}</style><header><h1>OEM 블로그: 긴 설명에 읽는 순서 만들기</h1><p>본문 문장은 보존. 소제목 6개·문단 분리 8곳·문서 비교 이미지 1개 추가.</p><nav><a href="before.html">이전 전체 글</a><a href="after.html">개선 전체 글</a><a href="../blog.txt">개선 TXT</a><a href="../review.md">검수 기록</a></nav><small>같은 390px 화면·글꼴·본문 크기. 실제 네이버 에디터가 아닌 로컬 발행 미리보기입니다.</small></header><main><section><h2>긴 설명: 자료 요청과 판매 후 문의 구분</h2><div class="pair"><figure><figcaption>이전</figcaption><img src="before-long.png"></figure><figure><figcaption>개선</figcaption><img src="after-long.png"></figure></div></section><section><h2>문서 대조: 글로 설명한 관계를 이미지로</h2><div class="pair"><figure><figcaption>이전</figcaption><img src="before-documents.png"></figure><figure><figcaption>개선</figcaption><img src="after-documents.png"></figure></div></section><nav><a href="../images/document-comparison.png">문서 비교 이미지 원본</a><a href="after.html">개선 글 전체 읽기</a></nav></main></html>''')
write('_workspace/2026-10-25-001/final.md',after+'\n<!-- HUMANIZE-SUMMARY\nConservative single-call review after legal review. Body prose unchanged; structural edit only. C-5 overridden by user heading-emoji preference; A-10 legal qualifiers protected. Six self-checks: meaning, names/numbers/quotes, change scope, genre, register, no new rhetoric. No forced score or change quota. Added six navigation headings; split eight paragraphs; existing narrative and CTA preserved.\n-->\n')
print(json.dumps(metrics,ensure_ascii=False))
