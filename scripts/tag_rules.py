#!/usr/bin/env python3
"""Tag checks shared by the blog linter and the website MD validator (docs/blog-authoring-spec.md §10).

Naver blog tags are `#tag` words at the end of blog.md; website tags are one comma-separated line without `#`.
Both should spread across different kinds of words (topic, law/system name, what readers search, situation,
procedure) instead of repeating one pair of nouns. The check is a hint, never a gate.
"""

import re

BLOG_RANGE = (12, 20)
WEBSITE_RANGE = (4, 10)
DOMINANT_SHARE = 0.6  # the two most repeated words appearing in this share of the tags means the set is lopsided
MIN_TAGS_FOR_SHARE = 6
MIN_WORD = 2
MAX_SAME_WORD = 3  # one word may appear in at most this many tags (its variants count)


def split_blog_tags(text):
    """`#a #b #c` words from the last line that is made only of hashtags; [] when there is none."""
    for line in reversed([l.strip() for l in text.splitlines() if l.strip()]):
        words = line.split()
        if words and all(re.fullmatch(r"#[^\s#]+", w) for w in words):
            return [w[1:] for w in words]
        if re.search(r"#[^\s#]+", line) and len(re.findall(r"#[^\s#]+", line)) >= 3:
            return [t for t in re.findall(r"#([^\s#]+)", line)]
        break
    return []


def split_website_tags(value):
    if isinstance(value, str):
        return [t.strip() for t in value.split(",") if t.strip()]
    return [str(t).strip() for t in (value or []) if str(t).strip()]


def _words(tags):
    out = set()
    for tag in tags:
        out.update(w for w in re.split(r"\s+", tag) if len(w) >= MIN_WORD)
    return out


def dominant_words(tags):
    """Greedy pick of up to two words whose substrings cover the most tags; returns (words, share)."""
    if len(tags) < MIN_TAGS_FOR_SHARE:
        return [], 0.0
    covered, picked = set(), []
    for _ in range(2):
        best, gain = None, 0
        for word in _words(tags):
            hit = {i for i, tag in enumerate(tags) if word in tag.replace(" ", "") or word in tag}
            new = len(hit - covered)
            if new > gain:
                best, gain, best_hit = word, new, hit
        if best is None:
            break
        picked.append(best)
        covered |= best_hit
    return picked, len(covered) / len(tags)


MIN_PART = 3  # Naver tags have no spaces (#영업정지과징금); shared parts this long count as the same word


def _parts(tags):
    """Whole words plus 3+ character pieces of space-less tags, so '영업정지' is found inside '영업정지과징금'."""
    out = _words(tags)
    for tag in tags:
        if " " in tag:
            continue
        out.update(tag[i:j] for i in range(len(tag)) for j in range(i + MIN_PART, len(tag) + 1))
    return out


def overused_words(tags):
    """(word, count) for words that sit inside more than MAX_SAME_WORD tags, most repeated first.

    A piece is dropped when a longer piece covers exactly the same tags ('영업' and '정지' give way to '영업정지').
    """
    if len(tags) < MIN_TAGS_FOR_SHARE:
        return []
    hits = {}
    for word in _parts(tags):
        hit = frozenset(i for i, tag in enumerate(tags) if word in tag)
        if len(hit) > MAX_SAME_WORD:
            hits[word] = hit
    found = [(word, len(hit)) for word, hit in hits.items()
             if not any(word != other and word in other and hits[other] == hit for other in hits)]
    return sorted(found, key=lambda item: (-item[1], item[0]))


def check(tags, kind):
    """Messages (strings) about count, duplicates and lopsided wording. kind is "blog" or "website"."""
    low, high = BLOG_RANGE if kind == "blog" else WEBSITE_RANGE
    messages = []
    if tags and not low <= len(tags) <= high:
        messages.append(f"태그 {len(tags)}개 (권장 {low}~{high}개)")
    if len({t.replace(" ", "") for t in tags}) != len(tags):
        messages.append("같은 태그가 두 번 있습니다(띄어쓰기만 다른 것 포함)" if kind == "blog" else "같은 태그가 두 번 있습니다")
    crowded = overused_words(tags)
    if crowded:
        listed = ", ".join(f"'{word}' {count}개" for word, count in crowded[:3])
        messages.append(f"같은 낱말이 여러 태그에 들어 있습니다({listed}). 같은 낱말의 변형은 {MAX_SAME_WORD}개까지로 하고, "
                        "독자가 실제로 검색할 표현·상황·절차어로 바꾸세요")
    words, share = dominant_words(tags)
    if words and share >= DOMINANT_SHARE and not crowded:
        messages.append(f"태그 {round(share * 100)}%가 '{'·'.join(words)}' 한두 낱말에 몰려 있습니다. 같은 낱말의 변형은 3개까지로 하고, "
                        "독자가 실제로 검색할 표현(예: 행정심판 대리, 허가 거부 대응), 상황·대상, 절차어를 섞으세요")
    return messages
