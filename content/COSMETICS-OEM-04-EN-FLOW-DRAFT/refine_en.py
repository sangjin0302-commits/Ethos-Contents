from pathlib import Path
import json
here=Path(__file__).resolve().parent
p=here/'card-data.en.json'
d=json.loads(p.read_text(encoding='utf-8')); c=d['cards']
c[0]['body']=['For OEM production in Korea, the brand receives and manages test results.']
c[0]['promise']='Quality control before you sign'
c[2]['body'][1]['text']=c[2]['body'][1]['text'].replace('facility','testing provider')
c[4]['body'][1]=c[4]['body'][1].replace('product standards','product specification documents')
c[5]['body'][1]['text']='For changes that may affect quality, you may agree on advance notice and delivery of relevant records, then confirm the change and its effective date in writing.'
c[5]['takeaway']='Align notification and approval procedures and name the internal reviewer. Further testing depends on the change.'
c[6]['headline']='Sharing quality records'
c[6]['body'][0]={'key':'Manufacturer’s duty','text':'Give the responsible distributor necessary quality-control information from manufacturing and quality records.'}
c[6]['body'][1]['text']='Submission may be omitted if both are the same business.'
c[6]['body'][2]['key']='Separate businesses: all three'
c[6]['body'][2]['text']='The manufacturer designs, develops and produces the product. Omission must not affect quality or safety management. The information is a trade secret under both parties’ contract.'
c[7]['takeaway']='Submission may be omitted only where all three apply, and only within that scope. A trade-secret claim is no blanket exemption.'
c[8]['note']='Illustrative wording. For specification changes, results that differ from agreed standards or post-sale inquiries, check whom to consult and who handles the records.'
c[9]['body'][1]['text']=c[9]['body'][1]['text'].replace('quality rules','quality-control rules')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
