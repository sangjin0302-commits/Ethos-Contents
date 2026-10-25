"""Create only this unapproved Korean visual draft from locked Git inputs."""
from pathlib import Path
import subprocess, json, hashlib, difflib, re, shutil, urllib.request

HERE = Path(__file__).resolve().parent
if (HERE / 'blog.md').exists() or (HERE / 'card-data.ko.json').exists():
    raise SystemExit('Bootstrap only: existing edited draft protected. Use build.py and finalize.py instead.')
ROOT = HERE.parents[1]
BASE = ROOT / 'content/COSMETICS-OEM-04-READABILITY-DRAFT'
APPROVED = ROOT / 'content/COSMETICS-OEM-04'
def write(name, text):
    p = HERE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
def snapshot(folder):
    return {str(p.relative_to(ROOT)).replace('\\','/'): hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.rglob('*') if p.is_file()}
if not (HERE/'source-hashes.json').exists():
    write('source-hashes.json', json.dumps(snapshot(APPROVED) | snapshot(BASE), ensure_ascii=False, indent=2))

blog = (BASE/'blog.md').read_text(encoding='utf-8')
edits = [
('예를 들어 민수 씨가 ‘미소뷰티’라는 이름으로 보습크림을 판매하려 한다고 해보겠습니다. 민수 씨는 공장을 직접 운영하지 않습니다. OEM 제조업체에 원료 조달과 생산, 충전, 포장, 품질검사를 맡기기로 하고 견적서를 받았습니다.\n\n견적서만 보면 공장이 만들어 검사한 제품을 브랜드 회사가 받아 판매하는 거래입니다. 민수 씨는 품질에 관한 일도 공장에서 다 한다고 생각할 수 있습니다.',
 '앞의 견적서를 받은 사람이 ‘미소뷰티’ 보습크림을 준비하는 민수 씨라고 해보겠습니다. 공장을 직접 운영하지 않는 민수 씨는 OEM 제조업체에 원료 조달과 생산, 충전, 포장, 품질검사를 맡겼습니다. 이제 견적서에 적힌 공장의 일과 브랜드 회사가 맡을 일을 나눠볼 차례입니다.'),
('검사를 누가 수행하는지 정한 뒤에는 어떤 제조번호의 결과를 어떻게 받을지도 정해야 합니다.',
 '검사 담당자를 정했다면, 납품받을 제조번호와 검사결과를 연결해 볼 차례입니다.'),
('이 기준으로 영업비밀의 범위를 정해야 나중에 필요한 품질기록을 요청할 때도 혼선이 줄어듭니다.',
 '영업비밀의 범위와 받을 품질기록을 나눠 적으면, 나중에 어느 자료를 요청할지 분명해집니다.'),
('화장품 OEM 계약서에 서명하기 전이라면 제조업체의 견적서 또는 계약서 초안, 시험성적서 제공 안내나 회사의 품질관리규정 중 현재 보유한 자료를 보내주세요. 에토스 행정사사무소에서는 무료 사전 검토로 검사 담당자와 제조번호별 결과를 어떤 방식으로 전달받는지, 계약서와 관리규정의 담당자가 맞는지, 제조업체와 계약 전에 더 합의할 내용이 무엇인지 먼저 살펴보겠습니다. 계약서와 관련 문서의 실제 작성은 범위와 비용을 별도로 정하는 유료 서비스입니다.',
 '화장품 OEM 계약서에 서명하기 전이라면 제조업체의 견적서 또는 계약서 초안, 시험성적서 제공 안내나 회사의 품질관리규정 중 현재 보유한 자료를 보내주세요. 에토스 행정사사무소에서는 무료 사전 검토로 검사 담당자와 제조번호별 결과의 전달 방식을 살펴보겠습니다. 계약서와 관리규정의 담당자가 맞는지, 제조업체와 계약 전에 더 합의할 내용은 무엇인지도 함께 확인하겠습니다. 계약서와 관련 문서의 실제 작성은 범위와 비용을 별도로 정하는 유료 서비스입니다.')]
for old,new in edits:
    assert blog.count(old)==1, old[:60]
    blog=blog.replace(old,new)
# User-requested visual section markers; not replacements for legal words.
markers = {
 '‘검사 완료’라는 메일과 납품 상자의 번호가 맞지 않는다면':'📦',
 '샘플을 승인한 다음 제품 사양이 달라진다면':'🔄',
 '‘처방은 영업비밀입니다’라는 답을 들었다면':'🔒',
 '다시 첫 견적서를 펼쳐보면 무엇이 달라질까요?':'📄',
 '직접 준비할 수 있는 부분과 맡길 수 있는 문서 작업':'🔍'}
for heading,emoji in markers.items(): blog=blog.replace('## '+heading,'## '+emoji+' '+heading)
write('blog.md',blog)
write('blog.txt',re.sub(r'^#{1,3} ', '',blog, flags=re.M))
write('blog-edit-notes.md','# 블로그 부분 편집\n\n기준: 직전 READABILITY-DRAFT. 승인 원고는 불변.\n\n'+ '\n\n'.join(f'## {i+1}\n\n이전: {a}\n\n개선: {b}' for i,(a,b) in enumerate(edits))+'\n\n이모티콘 5개는 소제목 탐색용. 법률 조건·인용 안에는 넣지 않음.\n')
write('blog.diff',''.join(difflib.unified_diff((BASE/'blog.md').read_text(encoding='utf8').splitlines(True),blog.splitlines(True),fromfile='previous/blog.md',tofile='visual-draft/blog.md')))
d=json.loads((BASE/'card-data.ko.json').read_text(encoding='utf8'))
d['contentId']=HERE.name
d.pop('approvedBy',None)
d['editorialReview']={ 'pipelineVersion':'2.0','naturalDraft':'pass','factCheck':'pending','marketingPass':'pending','forbiddenExpressionPass':'pending','languagePass':'pending','semanticRecheck':'pending'}
c=d['cards']
c[3].update(headline='‘검사 완료’ 메일과 납품 상자를 대조하세요',type='comparison',body=[
 {'key':'납품 상자','text':'제품명뿐 아니라 납품받는 생산분의 제조번호를 확인합니다.'},
 {'key':'검사자료','text':'그 제조번호의 검사결과인지 대조합니다. 제품명만 적혀 있다면 해당 생산분의 기록을 요청합니다.'}],takeaway='관리·감독, 기록 관리와 최종 제품 품질관리 의무는 남습니다.',design='상자와 검사자료의 제조번호 위치를 같은 색 테두리로 연결. 실제 번호를 창작하지 않음.')
c[3]['sourceTrace']['heading']='‘검사 완료’라는 메일과 납품 상자의 번호가 맞지 않는다면'
c[3]['sourceTrace']['evidence']='S'
c[4]['takeaway']='자료를 받았다는 사실과 검사결과가 적합하다는 판단은 구분합니다.'
c[6].update(headline='품질자료 제출, 원칙과 예외를 구분하세요',body=[
 {'key':'제출 원칙','text':'제조·품질관리 문서 중 품질관리에 필요한 사항을 책임판매업자에게 제출합니다.'},
 {'key':'동일 사업자','text':'제조업자와 책임판매업자가 동일하면 제출하지 않을 수 있습니다.'},
 {'key':'별개 사업자','text':'설계·개발·생산 방식, 품질·안전 영향 없는 범위, 계약상 영업비밀 조건을 모두 충족해야 합니다.'}],takeaway='법정 예외에 해당하는 범위에서 제출하지 않을 수 있습니다.',design='원칙과 예외를 구분. 동일사업자와 별개사업자 조건이 OR임을 구획으로 보여줌.')
c[7]['headline']='별개 사업자, 영업비밀 예외는 세 조건 모두'
c[7]['design']='잠금 이모티콘 뒤 세 조건을 한 묶음으로 연결. 모두라는 글자와 가능 표현 유지.'
c[8].update(type='concept',body=[
 {'key':'견적서','text':'‘품질검사 포함’'},
 {'key':'계약서','text':'‘납품 후 대금 지급’'},
 {'key':'품질관리규정','text':'‘책임판매관리자가 검사자료를 확인’'}],takeaway='자료를 누가 언제 주고받을지 맞추세요. 사양 변경·검사 불일치·판매 후 문의의 협의 및 자료 담당자도 확인합니다.',design='원문의 설명용 문구를 세 문서로 나란히 표시. 아래에 담당자와 전달시점 빈칸을 연결하며 실제 고객 문서처럼 꾸미지 않음.')
c[9]['body'][0]['key']='지금 가진 자료'
c[9]['body'][1]['text']='에토스 행정사사무소가 검사 담당자와 제조번호별 결과 전달 방식, 계약서와 관리규정의 담당자, 추가 합의할 내용을 살펴봅니다.'
write('card-data.ko.json',json.dumps(d,ensure_ascii=False,indent=2)+'\n')
write('brief.md','''# OEM 시각 개선 비교 초안

- 국문만 제작. 기존 승인 OEM과 직전 READABILITY-DRAFT는 읽기 전용.
- 독자: 국내 OEM 계약을 준비하는 화장품 브랜드 사업자.
- 질문: 공장 검사 후 브랜드가 확인할 자료와 맡을 일은 무엇인가.
- 역할: 1 질문 / 2 주체 / 3 검사 예외 / 4 제조번호 대조 / 5 자료 흐름 / 6 변경 약정 / 7 제출 원칙·예외 / 8 누적 조건 / 9 문서 대조 / 10 무료·유료 구분.
- CTA 자료·검토 결과: 기존 원고 범위 그대로. 새 서비스·회신기한 없음.
- OMITTED: CGMP와 판매 후 보고 상세, 기술 판정·분쟁 경계 등은 블로그에 유지. 기존 카드의 법률 조건 삭제 없음. 9번 체크항목은 3~6번과 9번 결론에 분산.
- 사용자 직접 요청으로 이모지 SVG 허용. 법률 AND/OR·가능/의무 표현은 글로 유지. 렌더·초안 작성 허용, 발행·커밋·푸시 미승인.
''')
write('wireframe.txt','''01 문서+검사 돋보기 / 질문+직접 답
02 공장·브랜드 아이콘 / 두 역할
03 두 갈래 / OR / 위탁 갈래 안 AND
04 상자·검사자료 / 제조번호 대조
05 자료 요청→전달→보관 / 원문 흐름
06 승인 기준→변경 약정 / 약정할 수 있음
07 원칙 위 / 예외 두 경로 아래
08 잠금 / 세 조건 한 묶음 / 모두 충족
09 세 문서 / 원문 예시 문구 / 담당자·시점 연결
10 보유 자료 / 무료 검토 / 유료 작성 경계
''')
assets=HERE/'assets'; assets.mkdir(exist_ok=True)
# Version-pinned third-party artwork. Never load a CDN while rendering.
for name in ['1f4c4','1f50d','1f4e6','1f3ed','1f4c2','1f512','1f504']:
    p=assets/(name+'.svg')
    if not p.exists():
        urllib.request.urlretrieve('https://raw.githubusercontent.com/twitter/twemoji/v14.0.2/assets/svg/'+name+'.svg',p)
license_file=assets/'TWEMOJI-LICENSE-GRAPHICS'
if not license_file.exists(): urllib.request.urlretrieve('https://raw.githubusercontent.com/twitter/twemoji/v14.0.2/LICENSE-GRAPHICS',license_file)
shutil.copyfile(ROOT/'assets/icons/lucide/LICENSE',assets/'LUCIDE-LICENSE')
for name in ['file-text','clipboard-check','arrow-right','building-2','folder-open','shield-check']:
    shutil.copyfile(ROOT/f'assets/icons/lucide/{name}.svg',assets/(name+'.svg'))
write('assets.md','''# 외부 자산 및 라이선스

- Twemoji v14.0.2, Twitter 및 기여자, CC BY 4.0. https://github.com/twitter/twemoji/tree/v14.0.2/assets/svg
- 원본 SVG 그대로 사용. 크기·배치만 조정. 1f4c4(문서), 1f50d(돋보기), 1f4e6(상자), 1f3ed(공장), 1f4c2(폴더), 1f512(잠금), 1f504(변경).
- 라이선스: assets/TWEMOJI-LICENSE-GRAPHICS, https://creativecommons.org/licenses/by/4.0/
- 발행 시 이미지와 함께 배포되는 캡션/출처 영역에 `Emoji graphics: Twemoji © Twitter and contributors, CC BY 4.0` 및 위 라이선스 링크를 유지한다. 비교 페이지에는 출처를 표시했다.
- Lucide: 저장소에 포함된 lucide-static 1.52.0 자산. ISC 및 Feather 유래 MIT 고지 유지. https://github.com/lucide-icons/lucide
- file-text(문서), clipboard-check(검토), arrow-right(전달), building-2(브랜드), folder-open(보관), shield-check(의무). 도형 수정 없음. 색·크기만 CSS 조절.
- 문서 비교·조건 묶음 레이아웃은 이번 작업에서 직접 작성. 다른 업체 디자인 복제 없음.
- 색이 있는 이모지 사용은 이번 사용자 요청에 따른 초안 한정 예외. 공통 브랜드 색·검수 게이트 변경 없음.
''')
print('Prepared',HERE.name)
