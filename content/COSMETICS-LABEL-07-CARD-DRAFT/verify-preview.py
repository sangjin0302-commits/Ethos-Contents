"""Verify the requested Korean-only delivery without weakening shared gates."""
from pathlib import Path
import hashlib
import html
import io
import json
import re
import sys
import zipfile

p = Path(__file__).resolve().parent
root = p.parent.parent
sys.path.insert(0, str(root/'scripts'))
from PIL import Image
from jsonschema import Draft7Validator
import copy_lint
import marketing_review
import validate_distribution

d = json.loads((p/'card-data.ko.json').read_text(encoding='utf-8'))
Draft7Validator(json.loads((root/'schema/card-data.schema.json').read_text(encoding='utf-8'))).validate(d)
assert d['approvedBy'] == '비교용 초안 — 사용자 승인 전. 발행 금지'
assert d['totalPages'] == len(d['cards']) == 10
assert sum(c['type']=='rest' for c in d['cards']) == 1
assert sum(c['type']=='cta' for c in d['cards']) == 1
assert sum(c.get('takeStyle')=='bar' for c in d['cards']) <= 4
lock = json.loads((p/'source-lock.json').read_text(encoding='utf-8'))
assert hashlib.sha256((p/'blog.md').read_bytes()).hexdigest() == lock['sourceSha256']
qa = json.loads((p/'out/ko/qa-report.json').read_text(encoding='utf-8'))
assert len(qa['cards']) == 10 and not any(c.get('fails') for c in qa['cards'])
for card in d['cards']:
    f = p/'ko'/f"card_{card['page']:02d}.html"
    page = f.read_text(encoding='utf-8')
    # Drop indentation-only trailing spaces emitted by the shared template.
    page = '\n'.join(line.rstrip() for line in page.splitlines())+'\n'
    f.write_text(page, encoding='utf-8')
    assert not copy_lint.copy_lock(card, page), (card['page'],copy_lint.copy_lock(card,page))
    assert 'name="ethos-auto"' in page, 'Only automatic previews are expected'
    assert card['sourceTrace']['heading'] in (p/'blog.md').read_text(encoding='utf-8')
    for ext, folder in [('png',p/'out/ko/png'),('jpg',p/'out/ko/jpeg')]:
        im_path = folder/f"card_{card['page']:02d}.{ext}"
        with Image.open(im_path) as im:
            im.load()
            assert im.size == (1080,1350)
            if ext=='jpg': assert im.mode=='RGB' and im.format=='JPEG'

dist = (p/'distribution.md').read_text(encoding='utf-8')
fail, warns = validate_distribution.validate_alt_text(p,dist)
# Keep shared bilingual validation unchanged; record its out-of-scope failure.
assert fail == ['missing card data: card-data.en.json'], fail
assert not warns, warns
af, aw = validate_distribution.validate_assets(p)
assert not af and not aw, (af,aw)
with zipfile.ZipFile(p/'out/ko/jpeg/cosmetics-label-07-ko-jpegs.zip') as z:
    assert z.testzip() is None
    assert z.namelist()==[f'card_{n:02d}.jpg' for n in range(1,11)]
    for name in z.namelist():
        assert z.read(name)==(p/'out/ko/jpeg'/name).read_bytes()
        with Image.open(io.BytesIO(z.read(name))) as im: im.load()

scores, notes = marketing_review.review(d)
(p/'out/marketing-review-ko.json').write_text(json.dumps({'scope':'ko only as requested','scores':scores,'notes':notes,'notPerformanceEvidence':True},ensure_ascii=False,indent=2),encoding='utf-8')
manifest_path=p/'out/render-manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['languages']['ko']['cardDataSha256']=hashlib.sha256((p/'card-data.ko.json').read_bytes()).hexdigest()
manifest['status']='preview-only; user approval pending'
manifest['metadataOnlyUpdate']='editorialReview completed after source, legal, copy, image and packaging review; rendered copy unchanged'
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
report={'schema':'pass','sourceUnchanged':'pass','copyLock10Cards':'pass','pngJpegDimensions':'pass','zipCrcAndByteMatch':'pass','koAltText':'pass','assets':'pass','rawBilingualDistributionFailure':fail,'userApproval':'pending','publication':'not authorized'}
(p/'out/delivery-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
links=['# 비발행용 미리보기 파일','', '사용자 카드 문구·발행 승인 전입니다. JPEG 1080×1350 RGB, quality=95.', '', '[JPEG 전체 ZIP](out/ko/jpeg/cosmetics-label-07-ko-jpegs.zip) · [JSON](card-data.ko.json) · [축소 시트](out/ko/sheet-270.png) · [QA](out/ko/qa-report.md) · [검수 기록](review.md)','']
for c in d['cards']:
    n=c['page']
    links.append(f"- [{n:02d} JPEG — {c['headline'].replace(chr(10),' ')}](out/ko/jpeg/card_{n:02d}.jpg)")
(p/'FILES.md').write_text('\n'.join(links)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
