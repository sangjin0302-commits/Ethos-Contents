"""Create local planning/provenance records from the authored card JSON."""
from pathlib import Path
import json
import hashlib
import re
import shutil

p = Path(__file__).resolve().parent
root = p.parent.parent
d = json.loads((p/'card-data.ko.json').read_text(encoding='utf-8'))
source = (p/'blog.md').read_text(encoding='utf-8')
sample = (root/'examples/writing/samples/cosmetics-label-07-user-edited-20261023.md').read_text(encoding='utf-8')
sample_body = sample.split('## 사용자 제공 전체 원고 (편집기 잔여물만 정리)', 1)[1]
norm = lambda s: re.sub(r'[\s#*_`>-]+', '', s)
match = norm(source.split('\n', 1)[1]) == norm(sample_body)
assert match, 'Source differs from user-edited sample beyond Markdown formatting'
for c in d['cards']:
    assert c['sourceTrace']['heading'] in source, c['page']

spoken = [
'기능성 원료도 있고 시험자료도 있어도, 포장과 광고에서 쓰려는 문구를 실제 제품자료에 맞춰 따로 봐야 합니다.',
'상자에 전성분과 주소를 적었다고 용기에 아무것도 안 적어도 되는 것은 아닙니다. 크림 용기에도 제품 식별정보와 사용기간 표시가 남아야 합니다.',
'작은 용기는 얼마나 작은지에 따라 생략 범위가 다릅니다. 견본품인지와 제외되는 제품인지도 보고, 생략한 성분을 소비자가 확인할 방법을 남겨야 합니다.',
'복합원료는 여러 성분이 섞인 원료입니다. 그 원료를 2% 넣은 것과 이름에 쓴 성분이 완제품에 2% 들어 있는 것은 구분해서 봐야 합니다.',
'두 기능성 원료를 넣었는지만 보지 말고, 실제 크림이 미백과 주름개선 모두 심사 또는 보고를 마쳤는지 자료로 확인하세요.',
'앞에서 본 표시사항과 함량, 기능성 내역은 결국 실제로 판매할 제품의 자료에 맞춰야 합니다.',
'미백 기능을 인정받았더라도 기미를 치료한다고 광고할 수는 없습니다. 사진이나 영상이 암시하는 효과까지 함께 보세요.',
'원료의 시험성적서가 크림 전체의 효과까지 증명하는 것은 아닙니다. 완제품 시험이라도 어떤 제품과 조건에서 나온 결과인지 보아야 합니다.',
'광고를 대행사에 맡기거나 협찬 영상으로 바꿔도 기준은 같습니다. 상세페이지에서 뺀 표현이 자막이나 사진으로 다시 들어오지 않았는지 확인하세요.',
'지금 가진 시안과 광고 문안, 해당하는 기능성 자료부터 준비하세요. 사전 확인과 실제 행정기관 제출 서류를 작성하고 제출하는 업무는 구분해서 협의합니다.'
]
header = '''# 국문 카드 기획 — 사용자 승인 전, 발행 금지

CONTENT ID: COSMETICS-LABEL-07-CARD-DRAFT
SOURCE: 이 브랜치의 blog.md, 사용자 수정본. PR #71 미사용.
SOURCE COMMIT: 49b4066741f38f1218b130d17fee38d39f602a0b
SPEC MAIN: 031ffe31d171d125835b898b1799088472f84ad0 (필수 두 명세가 브랜치와 동일함 확인)
CONTENT INVENTORY SOURCE: none
CONTENT INVENTORY MATCH: SNS·카드 재가공 / Issue #76 직접 요청
FRESHNESS VERIFIED ON: 2026-10-23 (채택한 카드 주장 범위; 근거 대조는 review.md)
REFRESH TRIGGER: 관련 법령 변경 또는 발행 전 재확인
REVIEW DUE: event-triggered
CLUSTER PARENT / HUB: 내 화장품 브랜드를 만들기 전에 알아야 할 인허가
PREVIOUS CONTENT: ⑥ 기능성화장품 심사·보고
NEXT CONTENT: 원문에 확정 제목 없음
CTA PATH: Composite → Free review
CARD DECISION: full carousel / 포장·함량·기능성·광고 자료의 경계를 비교하면 인쇄 전 판단에 도움이 됨
TARGET READER: OEM 크림의 인쇄와 광고 공개를 앞둔 브랜드 사업자
TOPIC VALUE TYPE: Composite
RARITY SIGNAL: 문서 정합성, 제도 교차
DECISION TENSION: 공장이 준 자료와 소비자가 보는 문구가 서로 다를 수 있음
HUMAN JUDGMENT PROOF: 문서 정합성표 (별도 고객 제공물을 약속하는 뜻 아님)
HUMAN VALUE: 같은 제품인지, 어떤 기능인지, 어떤 시험 조건인지 실제 자료를 대조해야 함
PRIMARY OBJECTIVE: 저장
SOURCE LANGUAGE: ko
OUTPUT LANGUAGES: ko (사용자 직접 범위; 영문·아랍어 제외)
CHANNEL OUTPUTS: Instagram 검토용 JPEG
ANGLE: 인쇄와 광고 공개 전에 실제 판매제품의 자료와 문구를 맞춘다.
SERIES LABEL / No.: 내 화장품 브랜드를 만들기 전에 알아야 할 인허가 / No.07
CANVAS: portrait 540×675 CSS / 1080×1350 이미지
VISUAL FAMILY: social-native
CARD COUNT: 10

## OMITTED

- 2026년 점검 건수·기사 및 보도자료: 중심 판단에 필수적이지 않으며 원자료 재검증을 끝내지 않았으므로 카드와 캡션에서 제외.
- AI 전문가 오인 광고의 시행 예정 규정: 매체별 일반 기준과 시행시점이 섞이지 않도록 제외.
- 실증자료 제출 요청 후 15일, 정당한 사유에 따른 연장과 중지명령: 광고 전 자료 대조에 집중하려고 제외. 기간을 광고 사전승인 기한으로 바꾸지 않음.
- 외부 포장의 법정 전체 항목, 가격 표시·한글 표시 세부, 화장비누 예외: 크림의 상자/용기 차이에 집중. 카드 2는 전 항목 목록이 아님.
- 소용량 제외 품목의 이름 및 개별 주의사항: 카드에서는 제외 규정 확인을 명시. 법정 수치와 간소화/일부 성분 생략 구분은 유지.
- 천연·유기농 기준과 추출물 함량: 복합원료 2%와 특정 성분 2%의 차이에 집중.
- 구체적 수임 사례·성과·새 서비스·무료 배포자료: 원문 범위 밖이므로 추가하지 않음.

## MARKETING INTENT

READER QUESTION: 인쇄 전에 어떤 자료와 문구를 맞춰야 하나?
PRACTICAL PAYOFF: 포장, 성분 함량, 기능성 내역, 광고 시험자료의 대조 지점을 안다.
COVER INTENT: 인쇄 직전이라는 실제 작업 시점.
SAVE VALUE: 마지막 시안과 상세페이지를 검토할 때 다시 참고.
CTA INPUTS: 용기·상자 시안 / 해당 심사 또는 보고 자료 / 광고 문안.
CTA OUTCOMES: 우선 볼 표시사항 / 자료 간 불일치 / 추가 요청자료.
PERFORMANCE HYPOTHESIS: 사용 시점을 드러낸 표지가 저장으로 연결되는지 관찰.
KOREAN COPY TREATMENT: manual-equivalent
HOOK A: 미백·주름개선 크림, 인쇄 전 문구부터 비교하세요.
HOOK B: 공장 자료와 패키지의 ‘2중 기능성’, 서로 맞나요?
HOOK C: 원료 시험자료로 완제품의 효과까지 광고해도 될까요?
SELECTED: A. 제품과 작업 시점이 함께 보임.

## CARDS — 말로 쓴 초안과 압축 방향

'''
rows = []
wire = ['비발행용 자동 미리보기 와이어프레임. 자유 디자인 최종본 아님.','']
for c, draft in zip(d['cards'], spoken):
    rows += [f"### {c['page']:02d}. {c['type']} / {c['visualBeat']}", f"한 메시지: {c['oneMessage']}", f"말로 한 초안: {draft}", f"카드 제목: {c['headline'].replace(chr(10), ' / ')}", f"시각 중심: {c['design']}", f"원문 위치: {c['sourceTrace']['heading']} / {c['sourceTrace']['evidence']}", '']
    wire += [f"[{c['page']:02d} {c['bg']}]", '[고정 헤더]', '[제목: 왼쪽 정렬]' if c['type']!='rest' else '[큰 결론: 쉼]', f"[본문: {c['design']}]", '[결론: '+c.get('takeStyle','close')+']', '[고정 푸터]', '']
(p/'brief.md').write_text(header+'\n'.join(rows)+'\nSYMBOLS REQUESTED: None\nBILINGUAL LOCK: N/A — 국문만 요청\nEDITORIAL PIPELINE: 실제 완료 상태는 card-data.ko.json 및 review.md에 기록\n',encoding='utf-8')
(p/'wireframe.txt').write_text('\n'.join(wire),encoding='utf-8')
icons = sorted({i for c in d['cards'] for i in c.get('art',[])}|{c['icon'] for c in d['cards'] if 'icon' in c})
assets = ['# 에셋 출처','', 'EXTERNAL ASSETS: Yes','', '| Asset | Source URL | Creator | License | Checked date | Modification |','|---|---|---|---|---|---|']
for icon in icons:
    assert (root/f'assets/icons/lucide/{icon}.svg').exists(), icon
    assets.append(f'| lucide/{icon}.svg | https://lucide.dev/icons/{icon} | Lucide contributors | ISC, 저장소 assets/icons/lucide 라이선스 | 2026-10-23 | 로컬 렌더러의 브랜드 색/크기 적용 |')
assets.append('| phosphor/file-text | https://github.com/phosphor-icons/core | Phosphor Icons | MIT, 저장소 assets/illustrations/objects/LICENSE-phosphor.txt | 2026-10-23 | 기존 렌더러의 브랜드 색과 크기 적용 |')
assets += ['', '로컬 글꼴과 브랜드 프레임: 저장소 fonts/, brand/, templates/ 그대로 사용. 표지의 큰 문서 그림은 저장소에 포함된 Phosphor 벡터이며 쉼 장식은 기존 프리셋이다. 외부 사진·AI 이미지 없음.', '실제 HTML은 표지에 phosphor/file-text를 사용한다. 제작용 JSON의 모든 아이콘 제안도 위에 기록했으며 자동 디자인에서 모든 제안 아이콘이 표시되는 것은 아니다.']
(p/'assets.md').write_text('\n'.join(assets),encoding='utf-8')
shutil.copyfile(root/'content/_TEMPLATE/performance-log.csv',p/'performance-log.csv')
(p/'source-lock.json').write_text(json.dumps({'sourceCommit':'49b4066741f38f1218b130d17fee38d39f602a0b','specMainCommit':'031ffe31d171d125835b898b1799088472f84ad0','sourceSha256':hashlib.sha256((p/'blog.md').read_bytes()).hexdigest(),'sampleMatchIgnoringMarkdown':match,'approved':False,'oldPr71Used':False},ensure_ascii=False,indent=2),encoding='utf-8')
print('Source/sample match; planning, wireframe, asset and lock records written.')
