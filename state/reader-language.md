# 독자가 쓰는 말

아직 자료가 없습니다. Search Console(성과 → 검색어 → 내보내기 CSV)이나 네이버 서치어드바이저 검색어 CSV, 상담에서 들은 질문(이름·연락처 빼고 한 줄에 하나)을 넣고 아래를 실행하면 이 파일이 채워집니다.

```bash
python scripts/reader_phrases.py Queries.csv naver.csv --questions questions.txt --out state/reader-language.md
```

글 제목·첫 문장·FAQ 질문(`Q.`)은 이 파일의 표현을 그대로 쓴다. 원문에 없는 사실을 만들 근거로 쓰지 않는다.
