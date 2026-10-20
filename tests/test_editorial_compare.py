import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from editorial_compare import check_conditions, protect_source


def sample():
    mapping = {'conditions': [{'id': 'C1', 'sourceExcerpt': '조건 A와 B', 'targets': [
        {'lang': 'ko', 'pages': [1, 2], 'excerpts': ['조건 A', '조건 B']},
        {'lang': 'en', 'pages': [1], 'excerpts': ['A and B']},
    ]}]}
    data = {'ko': {'cards': [{'page': 1, 'body': ['조건 A']}, {'page': 2, 'body': ['조건 B']}]},
            'en': {'cards': [{'page': 1, 'body': [{'key': 'Rule', 'text': 'A and B'}]}]}}
    return mapping, data


def test_split_condition_and_translation_trace():
    mapping, data = sample()
    assert check_conditions('조건 A와 B', mapping, data)['tracePass']


def test_deleted_condition_cannot_hide_in_metadata():
    mapping, data = sample()
    data['ko']['cards'][1] = {'page': 2, 'body': ['다른 글'], 'sourceTrace': '조건 B'}
    assert not check_conditions('조건 A와 B', mapping, data)['tracePass']


def test_missing_translation_or_page_fails():
    mapping, data = sample()
    mapping['conditions'][0]['targets'].pop()
    assert not check_conditions('조건 A와 B', mapping, data)['tracePass']
    mapping, data = sample()
    data['ko']['cards'].pop()
    assert not check_conditions('조건 A와 B', mapping, data)['tracePass']


def test_changed_source_and_empty_map_fail():
    mapping, data = sample()
    assert not check_conditions('조건 A 또는 B', mapping, data)['tracePass']
    assert not check_conditions('', {'conditions': []}, data)['tracePass']


def test_empty_datasets_cannot_pass_with_empty_targets():
    mapping = {'conditions': [{'id': 'C1', 'sourceExcerpt': 'source', 'targets': []}]}
    assert not check_conditions('source', mapping, {})['tracePass']


def test_duplicate_pages_and_languages_are_ambiguous():
    mapping, data = sample()
    data['ko']['cards'].append({'page': 1, 'body': ['unrelated replacement']})
    assert not check_conditions('조건 A와 B', mapping, data)['tracePass']
    mapping, data = sample()
    del data['ko']['cards'][0]['page']
    assert not check_conditions('조건 A와 B', mapping, data)['tracePass']
    mapping, data = sample()
    mapping['conditions'][0]['targets'].append(mapping['conditions'][0]['targets'][0])
    assert not check_conditions('조건 A와 B', mapping, data)['tracePass']


def test_missing_or_empty_source_cannot_create_evidence(tmp_path):
    snapshot = tmp_path / 'snapshot.json'
    with pytest.raises(ValueError):
        protect_source(tmp_path / 'missing', snapshot, True)
    empty = tmp_path / 'empty'
    empty.mkdir()
    with pytest.raises(ValueError):
        protect_source(empty, snapshot, True)
    assert not snapshot.exists()


def test_protection_detects_edit_delete_add_and_refuses_reset(tmp_path):
    base = tmp_path / 'base'
    base.mkdir()
    (base / 'blog.md').write_text('original', encoding='utf-8')
    snapshot = tmp_path / 'snapshot.json'
    assert protect_source(base, snapshot, True)['unchanged']
    (base / 'blog.md').write_text('edited', encoding='utf-8')
    assert protect_source(base, snapshot)['changed'] == ['blog.md']
    with pytest.raises(ValueError):
        protect_source(base, snapshot, True)
    (base / 'blog.md').unlink()
    (base / 'extra.md').write_text('added', encoding='utf-8')
    assert protect_source(base, snapshot)['changed'] == ['blog.md', 'extra.md']
