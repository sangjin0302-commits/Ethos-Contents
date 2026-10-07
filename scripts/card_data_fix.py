#!/usr/bin/env python3
"""ChatGPT가 card-data를 쓸 때 자주 내는 형식 실수를 렌더 전에 바로잡는다(문구는 바꾸지 않는다).

`Render cards`(ci_render.py)가 스키마 검사 전에 부른다. 고친 내용은 보고서에 그대로 적어, 작성자가 다음부터 맞는 형식으로 쓰게 한다.
저장소의 JSON 파일은 고치지 않는다. 발행본은 Codex가 맞는 형식으로 정리한다.

- table 카드의 body를 {"head": [...], "rows": [...]}로 쓴 경우 → head 필드 + body 배열
- 아이콘 이름에 붙은 ".svg" → 이름만
- editorialReview 단계 값이 pass·pending 밖인 경우(예: "source-lock") → "pending"
"""

import copy

STAGES = ("naturalDraft", "factCheck", "marketingPass", "forbiddenExpressionPass", "semanticRecheck")
STAGE_VALUES = {"pass", "pending", "legacy-unrecorded"}


def _strip_svg(name):
    return name[:-4] if isinstance(name, str) and name.endswith(".svg") else name


def normalize(data):
    """(고친 사본, 고친 내용 목록). 고칠 것이 없으면 목록이 비어 있다."""
    data = copy.deepcopy(data)
    notes = []
    for card in data.get("cards", []):
        page = card.get("page")
        body = card.get("body")
        if isinstance(body, dict) and isinstance(body.get("rows"), list):
            if body.get("head") and not card.get("head"):
                card["head"] = body["head"]
            card["body"] = body["rows"]
            notes.append(f"card {page}: body를 {{head, rows}} 객체로 썼습니다 → head 필드와 body 배열로 바꿔 렌더했습니다")
        if isinstance(card.get("icon"), str) and card["icon"].endswith(".svg"):
            card["icon"] = _strip_svg(card["icon"])
            notes.append(f"card {page}: icon 이름의 .svg를 뺐습니다")
        if isinstance(card.get("art"), list) and any(str(n).endswith(".svg") for n in card["art"]):
            card["art"] = [_strip_svg(n) for n in card["art"]]
            notes.append(f"card {page}: art 이름의 .svg를 뺐습니다")
        for item in card.get("body", []) if isinstance(card.get("body"), list) else []:
            if isinstance(item, dict) and isinstance(item.get("icon"), str) and item["icon"].endswith(".svg"):
                item["icon"] = _strip_svg(item["icon"])
    review = data.get("editorialReview")
    if isinstance(review, dict):
        for stage in STAGES:
            if stage in review and review[stage] not in STAGE_VALUES:
                notes.append(f"editorialReview.{stage}: '{review[stage]}'는 쓸 수 없는 값이라 pending으로 렌더했습니다(pass·pending만)")
                review[stage] = "pending"
    return data, notes
