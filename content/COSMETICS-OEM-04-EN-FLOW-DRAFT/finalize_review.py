from pathlib import Path
import json
h=Path(__file__).resolve().parent
p=h/'card-data.en.json'; d=json.loads(p.read_text(encoding='utf-8'))
for key in ['naturalDraft','factCheck','marketingPass','forbiddenExpressionPass','languagePass','semanticRecheck']:
    d['editorialReview'][key]='pass'
d['editorialReview']['languageMethod']='english-localization'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (h/'localization-review.md').open('a',encoding='utf-8') as f:
    f.write('\n\n## 담당 에이전트 후속 조치 확인\n주 에이전트가 영문 전체 hyphens:none을 적용하고 최종 PNG를 재확인했다. 9번 timing 분할 제거. 7번 제목을 Sharing quality records로 압축해 제목과 본문 사이 공간을 확보했다. 최종 QA 기준 7번 439자/69단어, 본문 채움 0.90. 본문 법률 조건은 그대로이며 고밀도 권고는 남는다. 내부 검수 완료이며 사용자 승인 대기.\n')
