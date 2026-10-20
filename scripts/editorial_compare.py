#!/usr/bin/env python3
"""Read-only source protection and evidence checks for a separate editorial draft.

Exact excerpts prove traceability, never legal equivalence or reader preference.
The snapshot must be taken before editing; it is deliberately never overwritten.
"""
import argparse
import hashlib
import json
from pathlib import Path


def file_hashes(folder):
    if not folder.is_dir():
        raise ValueError(f'Baseline folder does not exist: {folder}')
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob('*')) if p.is_file()}


def protect_source(folder, snapshot, initialize=False):
    current = file_hashes(folder)
    if not current:
        raise ValueError('Baseline folder has no files to protect')
    if initialize:
        if snapshot.exists():
            raise ValueError('Snapshot already exists; refusing to replace source evidence')
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also prevents a concurrent initializer replacing evidence.
        with snapshot.open('x', encoding='utf-8') as handle:
            handle.write(json.dumps(current, indent=2) + '\n')
    expected = json.loads(snapshot.read_text(encoding='utf-8'))
    changed = sorted(k for k in expected.keys() | current.keys()
                     if expected.get(k) != current.get(k))
    return {'files': len(expected), 'unchanged': not changed, 'changed': changed}


def visible_text(card):
    """Only public copy; metadata/sourceTrace cannot satisfy a condition."""
    def flatten(value):
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return [s for item in value for s in flatten(item)]
        if isinstance(value, dict):
            return [s for key, item in value.items() if key in ('key', 'text', 'label', 'value', 'display')
                    for s in flatten(item)]
        return []
    return '\n'.join(s for key in ('headline', 'body', 'takeaway', 'promise', 'paths', 'note', 'hero', 'head')
                     for s in flatten(card.get(key)))


def check_conditions(source, mapping, datasets):
    errors, seen = [], set()
    if not datasets:
        errors.append('No card datasets supplied')
    for lang, dataset in datasets.items():
        pages = [c.get('page') for c in dataset.get('cards', [])]
        if not pages or None in pages or len(set(pages)) != len(pages):
            errors.append(f'{lang}: empty cards or missing/duplicate page numbers')
    rows = mapping.get('conditions', [])
    if not rows:
        errors.append('No conditions recorded')
    for row in rows:
        ident = row.get('id', '')
        if not ident or ident in seen:
            errors.append(f'{ident}: missing/duplicate condition id')
        seen.add(ident)
        excerpt = row.get('sourceExcerpt', '')
        if not excerpt or excerpt not in source:
            errors.append(f'{ident}: source excerpt missing')
        targets = row.get('targets', [])
        if len({x.get('lang') for x in targets}) != len(targets):
            errors.append(f'{ident}: duplicate target language')
        if {x.get('lang') for x in targets} != set(datasets):
            errors.append(f'{ident}: target languages differ from supplied datasets')
        for target in targets:
            lang = target.get('lang')
            cards = {c['page']: c for c in datasets.get(lang, {}).get('cards', []) if 'page' in c}
            pages = target.get('pages', [])
            if not pages or any(page not in cards for page in pages):
                errors.append(f'{ident}/{lang}: target page missing')
                continue
            copy = '\n'.join(visible_text(cards[p]) for p in pages)
            excerpts = target.get('excerpts', [])
            if not excerpts or any(not x or x not in copy for x in excerpts):
                errors.append(f'{ident}/{lang}: target excerpt missing from visible copy')
    return {'conditions': len(rows), 'tracePass': not errors, 'errors': errors,
            'scope': 'Exact excerpt trace only. Independent legal/semantic review is required.'}


def copy_metrics(data):
    # Unicode characters, including spaces within fields. Field joins excluded.
    counts = {str(c['page']): len(visible_text(c).replace('\n', '')) for c in data['cards']}
    return {'cards': len(counts), 'visibleCharsByPage': counts,
            'totalVisibleChars': sum(counts.values()), 'maxVisibleChars': max(counts.values(), default=0)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline', required=True, type=Path)
    p.add_argument('--draft', required=True, type=Path)
    p.add_argument('--initialize', action='store_true', help='Capture immutable baseline before editing')
    args = p.parse_args()
    base, draft = args.baseline.resolve(), args.draft.resolve()
    if base == draft or base in draft.parents or draft in base.parents:
        p.error('Baseline and draft must be separate, non-nested folders')
    protection = protect_source(base, draft / 'baseline-sha256.json', args.initialize)
    if args.initialize:
        print(json.dumps(protection, ensure_ascii=False))
        return 0
    datasets = {f.name.split('.')[1]: json.loads(f.read_text(encoding='utf-8'))
                for f in sorted(draft.glob('card-data.*.json'))}
    mapping = json.loads((draft / 'condition-map.json').read_text(encoding='utf-8'))
    trace = check_conditions((base / 'blog.md').read_text(encoding='utf-8'), mapping, datasets)
    metrics = {lang: {'before': copy_metrics(json.loads((base / f'card-data.{lang}.json').read_text(encoding='utf-8'))),
                      'after': copy_metrics(data)} for lang, data in datasets.items()}
    report = {'sourceProtection': protection, 'conditionTrace': trace, 'copyMetrics': metrics,
              'limitations': 'Character counts are density measures, not a score for naturalness, design, or legal accuracy.'}
    (draft / 'comparison-metrics.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if protection['unchanged'] and trace['tracePass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
