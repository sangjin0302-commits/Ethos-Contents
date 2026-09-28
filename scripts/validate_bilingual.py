#!/usr/bin/env python3
"""Validate bilingual card data before HTML rendering."""

import argparse
import json
import pathlib
import sys

from jsonschema import Draft7Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("content_dir", help="content/<ID> directory")
    args = parser.parse_args()
    folder = pathlib.Path(args.content_dir)
    schema = load(ROOT / "schema" / "card-data.schema.json")
    validator = Draft7Validator(schema)
    data = {}
    errors = []

    for language in ("ko", "en"):
        path = folder / f"card-data.{language}.json"
        if not path.exists():
            errors.append(f"missing: {path}")
            continue
        item = load(path)
        data[language] = item
        for error in sorted(validator.iter_errors(item), key=lambda e: list(e.path)):
            location = ".".join(map(str, error.path)) or "root"
            errors.append(f"{path.name}:{location}: {error.message}")
        if item.get("language") != language:
            errors.append(f"{path.name}: language must be '{language}'")

    if len(data) == 2:
        ko, en = data["ko"], data["en"]
        for field in ("contentId", "totalPages"):
            if ko.get(field) != en.get(field):
                errors.append(f"bilingual mismatch: {field}")
        ko_cards, en_cards = ko.get("cards", []), en.get("cards", [])
        if len(ko_cards) != len(en_cards):
            errors.append("bilingual mismatch: card count")
        for index, (kc, ec) in enumerate(zip(ko_cards, en_cards), 1):
            for field in ("page", "type", "bg"):
                if kc.get(field) != ec.get(field):
                    errors.append(f"card {index}: bilingual mismatch: {field}")
            for field in ("heading", "evidence"):
                if kc.get("sourceTrace", {}).get(field) != ec.get("sourceTrace", {}).get(field):
                    errors.append(f"card {index}: sourceTrace mismatch: {field}")

    if errors:
        print("FAIL")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("PASS: bilingual card data share the same structure and source trace")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
