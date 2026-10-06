앞으로 웹페이지용 글에서는 시리즈 간 직접 링크를 빼고, 각 글이 단독으로 읽혀도 완결되는 형태로 구성한다. 

## 웹사이트 블로그 MD (국문·영문)

웹사이트 블로그 글은 `docs/website-md-spec.md`에 따라 `website.ko.md`와 `website.en.md` 두 파일로 만든다. 요청에 "웹사이트", "홈페이지", "MD"가 있으면 별도 지시가 없어도 두 파일을 함께 낸다. 머리말은 관리자 입력 칸(슬러그·제목·요약·분류·태그)과 1:1로 맞추고, 본문은 웹사이트가 변환하는 마크다운만 쓴다(마크다운 표 금지, `**` 짝 맞추기, 본문 `#` 제목 금지). 영문은 다시 쓰고 행정사는 Administrative Attorney로 쓴다. 검사: `python scripts/validate_website_md.py content/<ID>`.
