#!/usr/bin/env python3
"""실제 독자가 쓰는 말(검색어·질문)을 모아 state/reader-language.md를 만든다.

글 제목·첫 문장·FAQ 질문을 독자의 표현으로 쓰기 위한 자료다. 오프라인, LLM 없음.

입력(여러 개 가능):
  - Google Search Console '검색어(Queries)' CSV: 열 이름 Top queries / 인기 검색어, Clicks / 클릭수, Impressions / 노출수, CTR, Position
  - 네이버 서치어드바이저 검색어 CSV: 검색어 / 키워드, 노출수, 클릭수
  - --questions 텍스트 파일: 상담에서 들은 질문을 한 줄에 하나씩(이름·연락처는 빼고 적는다)

사용:
  python scripts/reader_phrases.py Queries.csv naver.csv --questions questions.txt --out state/reader-language.md

개인정보처럼 보이는 줄(전화번호·이메일·주민등록번호 형태)은 버린다.
"""
import argparse
import collections
import csv
import datetime
import io
import pathlib
import re
import sys

PII = re.compile(r"(?:\d{2,3}-\d{3,4}-\d{4}|01[016789]\d{7,8}|[\w.+-]+@[\w-]+\.[\w.]+|\d{6}-?[1-4]\d{6})")
QUERY_COLS = ("top queries", "query", "queries", "인기 검색어", "검색어", "키워드", "keyword")
CLICK_COLS = ("clicks", "클릭수", "클릭")
IMPR_COLS = ("impressions", "노출수", "노출")
QUESTION = re.compile(r"(\?|까$|나요$|가요$|되나|될까|할까|있나|없나|방법|가능|얼마|기간|비용|절차|조건|서류|하려면|되려면|차이)")
STOP = {"행정사", "에토스", "ethos", "사무소"}


def pick(header, names):
    low = [h.strip().lower() for h in header]
    for name in names:
        if name in low:
            return low.index(name)
    return None


def number(value):
    try:
        return float(str(value).replace(",", "").replace("%", "").strip() or 0)
    except ValueError:
        return 0.0


def read_csv(path):
    raw = pathlib.Path(path).read_bytes()
    for encoding in ("utf-8-sig", "cp949"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError(f"{path}: 인코딩을 읽을 수 없습니다")
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return []
    header, body = rows[0], rows[1:]
    q, c, i = pick(header, QUERY_COLS), pick(header, CLICK_COLS), pick(header, IMPR_COLS)
    if q is None:
        raise ValueError(f"{path}: 검색어 열을 찾지 못했습니다(열 이름: {', '.join(header)})")
    out = []
    for row in body:
        if len(row) <= q or not row[q].strip():
            continue
        out.append({"query": row[q].strip(), "clicks": number(row[c]) if c is not None and c < len(row) else 0,
                    "impressions": number(row[i]) if i is not None and i < len(row) else 0})
    return out


def topic_words(text):
    """검색어에서 주제 낱말(명사)을 뽑는다. kiwipiepy가 없으면 공백으로 나눈다."""
    try:
        from kiwipiepy import Kiwi
        kiwi = topic_words.kiwi = getattr(topic_words, "kiwi", None) or Kiwi()
        words = [t.form for t in kiwi.tokenize(text) if t.tag in ("NNG", "NNP", "SL") and len(t.form) > 1]
    except Exception:
        words = [w for w in re.split(r"\s+", text) if len(w) > 1]
    return [w for w in words if w.lower() not in STOP]


def build(queries, questions, sources, today):
    merged = collections.defaultdict(lambda: {"clicks": 0.0, "impressions": 0.0})
    for row in queries:
        if PII.search(row["query"]):
            continue
        key = re.sub(r"\s+", " ", row["query"])
        merged[key]["clicks"] += row["clicks"]
        merged[key]["impressions"] += row["impressions"]
    ranked = sorted(merged.items(), key=lambda kv: (-kv[1]["impressions"], -kv[1]["clicks"], kv[0]))
    asked = [q for q, _ in ranked if QUESTION.search(q)]
    topics = collections.Counter()
    for q, v in ranked:
        for w in set(topic_words(q)):
            topics[w] += max(1, v["impressions"])
    # 노출은 많은데 클릭이 적은 검색어: 제목·요약을 그 표현으로 바꿀 후보
    gaps = [(q, v) for q, v in ranked if v["impressions"] >= 50 and v["clicks"] / max(1, v["impressions"]) < 0.02][:15]
    clean_questions = [q.strip() for q in questions if q.strip() and not PII.search(q)]

    lines = [f"# 독자가 쓰는 말 (자동 생성 {today})", "",
             "글 제목·첫 문장·FAQ 질문(`Q.`)을 쓸 때 아래 표현을 그대로 쓴다. 원문에 없는 사실을 만들 근거로 쓰지 않는다. "
             "갱신: `python scripts/reader_phrases.py <검색어 CSV…> --questions <질문.txt> --out state/reader-language.md`", "",
             f"자료: {', '.join(sources) or '없음'} · 검색어 {len(ranked)}개 · 상담 질문 {len(clean_questions)}개", ""]
    lines += ["## 질문형 검색어 (FAQ 질문 후보)", ""] + [f"- {q}" for q in asked[:30]] + [""]
    lines += ["## 상담에서 들은 질문", ""] + ([f"- {q}" for q in clean_questions[:40]] or ["- (없음)"]) + [""]
    lines += ["## 노출 상위 검색어", "", "| 검색어 | 노출 | 클릭 |", "|---|---:|---:|"]
    lines += [f"| {q} | {v['impressions']:.0f} | {v['clicks']:.0f} |" for q, v in ranked[:40]] + [""]
    lines += ["## 제목을 바꿔 볼 검색어 (노출 50 이상, 클릭률 2% 미만)", ""]
    lines += [f"- {q} (노출 {v['impressions']:.0f}, 클릭 {v['clicks']:.0f})" for q, v in gaps] or ["- (없음)"]
    lines += ["", "## 자주 나오는 주제 낱말", "", ", ".join(f"{w}({n:.0f})" for w, n in topics.most_common(30)) or "(없음)", ""]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv", nargs="*", help="Search Console·네이버 서치어드바이저 검색어 CSV")
    parser.add_argument("--questions", help="상담 질문 텍스트(한 줄에 하나)")
    parser.add_argument("--out", help="저장 경로(예: state/reader-language.md)")
    args = parser.parse_args(argv)
    if not args.csv and not args.questions:
        parser.print_help()
        return 2
    queries, sources = [], []
    try:
        for path in args.csv:
            queries += read_csv(path)
            sources.append(pathlib.Path(path).name)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    questions = pathlib.Path(args.questions).read_text(encoding="utf-8").splitlines() if args.questions else []
    if args.questions:
        sources.append(pathlib.Path(args.questions).name)
    text = build(queries, questions, sources, datetime.date.today().isoformat())
    if args.out:
        pathlib.Path(args.out).write_text(text, encoding="utf-8")
        print(f"저장: {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
