"""Rebuild this unapproved comparison draft; never touches its source set."""
import json
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import auto_design as auto
from build_cards import esc, keep_dot_chains, MAX_NOBR


def main_copy(card, data):
    page = card['page']
    if page == 1:
        return (f'<div class="cover-art" data-decor data-focal>{auto.obj_svg("cosmetics-oem")}</div>'
                f'<h1 class="cover-title" data-role="headline">{esc(card["headline"])}</h1>'
                f'<p class="cover-lede">{esc(card["body"][0])}</p>'
                f'<p class="cover-promise">{esc(card["promise"])}</p>')
    style = {2: 'roles', 3: 'branches', 4: 'duties', 5: 'delivery', 6: 'change',
             7: 'principle', 8: 'cumulative', 9: 'checks', 10: 'contact'}[page]
    rows = []
    for item in card['body']:
        if isinstance(item, dict):
            rows.append(f'<div class="copy-row"><h3 class="copy-key">{esc(item["key"])}</h3>'
                        f'<p class="copy-text">{esc(item["text"])}</p></div>')
        else:
            rows.append(f'<div class="copy-row"><p class="copy-text">{esc(item)}</p></div>')
    return f'<div class="editorial {style}" data-focal>' + ''.join(rows) + '</div>'


for lang in ('ko', 'en'):
    data = json.loads((FOLDER / f'card-data.{lang}.json').read_text(encoding='utf-8'))
    out = FOLDER / lang
    out.mkdir(exist_ok=True)
    for card in data['cards']:
        html = auto.build(card, data, depth=3, production=True)
        # Dot-chain wrapping depends on surrounding markup. Replace the explicit
        # zone boundaries, rather than silently missing a text-based replacement.
        marker = '<div class="z-main" data-zone="main">'
        start = html.index(marker) + len(marker)
        end = html.index('\n    <div class="z-take"', start)
        html = html[:start] + keep_dot_chains(main_copy(card, data), MAX_NOBR) + '</div>' + html[end:]
        assert 'class="editorial ' in html or 'class="cover-art"' in html
        (out / f'card_{card["page"]:02d}.html').write_text(html, encoding='utf-8')
    print(f'{lang}: {len(data["cards"])} comparison cards, approval unchanged')
