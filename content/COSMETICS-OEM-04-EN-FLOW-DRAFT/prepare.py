"""One-time English localization draft; never overwrite an existing draft."""
from pathlib import Path
import copy, hashlib, json, shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=HERE.parent/'COSMETICS-OEM-04-CARD-FLOW-DRAFT'
assert not (HERE/'card-data.en.json').exists(), 'Draft already exists'
hashes={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
        for folder in HERE.parent.glob('COSMETICS-OEM-04*') if folder!=HERE
        for p in folder.rglob('*') if p.is_file()}
(HERE/'source-hashes.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['blog.md','design.css','assets.md']:
    shutil.copy2(BASE/name,HERE/name)
for name in ['ko','assets']:
    shutil.copytree(BASE/name,HERE/name)
ko=json.loads((BASE/'card-data.ko.json').read_text(encoding='utf-8'))
ko['contentId']=HERE.name
ko['editorialReview']['reviewNote']='국문 CARD-FLOW의 공개 문구와 HTML을 그대로 복사한 대조 기준. 이 폴더의 영문은 별도 미승인 초안.'
en=copy.deepcopy(ko)
en.update(language='en',series='Cosmetics Brand Launch in Korea',headerLabel='Cosmetics Brand Launch')
en['editorialReview']={k:'pending' for k in ['naturalDraft','factCheck','marketingPass','forbiddenExpressionPass','languagePass','semanticRecheck']}
en['editorialReview']['pipelineVersion']='2.0'
copy_by_page={
1:dict(headline='The factory tests. What does the brand do?',body=['Korean domestic OEM: the brand receives and manages test results.'],promise='Quality checks before you sign',coverLabel='Cosmetics OEM contracts'),
2:dict(headline='Know what each business must do',body=[
    {'key':'Manufacturer','text':'It tests raw materials, supplies and finished products. It also prepares and keeps manufacturing and quality-control records.'},
    {'key':'Responsible distributor','text':'The brand oversees the contractor. It receives and manages results for each batch and the related records.'}],takeaway='Sharing costs by contract does not transfer duties under the Cosmetics Act.'),
3:dict(headline='When may you skip a separate test?',body=[
    {'key':'Same business','text':'The manufacturer and responsible distributor are the same business.'},
    {'key':'Or outsourced testing','text':'For separate businesses, testing must be entrusted to a legally eligible facility, with results available for each batch.'}],takeaway='Oversight, record management and final-product quality duties remain.'),
4:dict(headline='“Test complete”: check the delivery',body=[
    {'key':'Delivered goods','text':'Check the batch number of the goods delivered, not just the product name.'},
    {'key':'Test records','text':'Match the results to that batch number. If only the product name appears, ask for records for that batch.'}],takeaway='Oversight, record management and final-product quality duties remain.'),
5:dict(headline='Agree how test records reach you',body=[
    'Agree who tests and how to check results for the batches being delivered.',
    'Agree who provides and reviews the required product standards and quality-control records, and when.',
    'Keep the records under the company’s quality-control rules.'],takeaway='Receiving records is not the same as judging whether the test results meet the required standards.'),
6:dict(headline='What if the approved specifications change?',body=[
    {'key':'Agreed baseline','text':'Document the approved sample, product specifications, container, packaging and required test standards.'},
    {'key':'Changes','text':'For changes that may affect quality, you may agree on advance notice and records, followed by written confirmation of the change and its effective date.'}],takeaway='Align notice, approval and internal review roles. Further testing depends on the change.'),
7:dict(headline='When must quality records be shared?',body=[
    {'key':'The rule','text':'The manufacturer must give the responsible distributor the information needed for quality control from manufacturing and quality records.'},
    {'key':'Same business','text':'If both are the same business, submission may be omitted.'},
    {'key':'Separate businesses: all three','text':'The manufacturer must design, develop and produce the product. Omission must not affect quality or safety management, and the information must be a trade secret under both parties’ contract.'}],takeaway='Submission may be omitted only within the statutory exception’s scope.'),
8:dict(headline='Separate businesses: meet all three conditions',body=[
    {'key':'Production model','text':'The manufacturer must design, develop and produce the product.'},
    {'key':'Quality and safety','text':'Omission must not affect quality or safety management.'},
    {'key':'Contract terms','text':'The information must be a trade secret under the contract between both parties.'}],takeaway='All three must apply for submission to be omitted within that scope. A trade-secret claim is no blanket exemption.'),
9:dict(headline='Compare three documents before signing',body=[
    {'key':'Quotation','text':'“Quality testing included”'},
    {'key':'Contract','text':'“Payment after delivery”'},
    {'key':'Quality-control rules','text':'“The responsible sales manager checks test records”'}],note='These are examples from the source article. For specification changes, mismatched test results or post-sale inquiries, check whom to consult and who handles the records.',takeaway='Align the people responsible and record-delivery timing across all three documents.'),
10:dict(headline='Before signing, start with what you have',body=[
    {'key':'Your documents','text':'Send any quotation, draft contract, test-report delivery guidance or quality-control rules you already have.'},
    {'key':'Free initial review','text':'Ethos Administrative Attorney Office checks who tests, how batch results reach you, the people named in the contract and quality rules, and what still needs agreement.'}],takeaway='Drafting contracts and related documents is a paid service. Scope and fees are agreed separately.')
}
for c in en['cards']:
    c.update(copy_by_page[c['page']])
for lang,data in [('ko',ko),('en',en)]:
    (HERE/f'card-data.{lang}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'en').mkdir()
print('Created bilingual comparison draft; protected',len(hashes),'existing files')
