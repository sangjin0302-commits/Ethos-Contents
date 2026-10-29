"""Regressions for natural copy without weakening fact/approval boundaries."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import ai_polish
import copy_lint


def card(page=1, kind='cover', **fields):
    return {'page': page, 'type': kind, 'headline': '한국 출시 기준입니다',
            'body': ['실제 역할을 확인합니다.'], 'takeaway': '기준은 서로 다릅니다.', **fields}


class EditorialQualityTests(unittest.TestCase):
    def test_unnumbered_payoff_in_both_languages(self):
        for lang, promise in [('ko', '내게 필요한 출시 절차를 구분합니다'),
                              ('en', 'Find the route that fits your launch')]:
            report = copy_lint.Report()
            copy_lint.lint_cards({'cards': [card(promise=promise)]}, lang, report)
            self.assertNotIn('cover-payoff', [f['rule'] for f in report.findings])

    def test_style_ratios_do_not_become_strict_errors(self):
        report = copy_lint.Report()
        copy_lint.lint_cards({'cards': [card(i, 'concept', headline='필요할까요?',
                                             takeaway='같은 것은 아닙니다.') for i in range(1, 7)]}, 'ko', report)
        findings = [f for f in report.findings if f['rule'] in {'question-headlines', 'negative-framing'}]
        self.assertEqual(len(findings), 2)
        self.assertTrue(all(f['level'] == 'info' for f in findings))

    def test_prose_context_excludes_markdown_and_quotes_are_protected(self):
        text = '# 제목\n\n첫 문단입니다.\n\n두 번째 문단입니다.\n\n> 인용입니다.\n\n```\n코드입니다.\n```'
        items = ai_polish.collect_prose(text, 'blog')
        self.assertEqual([x['text'] for x in items], ['첫 문단입니다.', '두 번째 문단입니다.'])
        self.assertEqual(items[1]['context']['previousParagraph'], '첫 문단입니다.')
        self.assertEqual(items[0]['context']['channel'], 'blog')

    def test_card_context_has_trace_neighbors_and_real_source(self):
        source = '원문\n실제 업무에 따라 절차를 확인합니다.'
        data = {'cards': [card(oneMessage='첫 판단', sourceTrace={'paragraph': '실제 업무'}),
                          card(2, 'concept', oneMessage='다음 판단')]}
        item = ai_polish.collect(data, source)[0]
        self.assertEqual(item['context']['nextMessage'], '다음 판단')
        self.assertIn('실제 업무', item['context']['sourceExcerpt'])
        self.assertEqual(ai_polish.source_excerpt(source, {'heading': '없는 제목'}), '')
        self.assertEqual(ai_polish.collect({'cards': [card(kind='quote')]}), [])

    def test_apply_invalidates_old_approval_but_noop_does_not(self):
        data = {'approvedBy': 'prior approval', 'editorialReview': {'semanticRecheck': 'pass'}, 'cards': [card()]}
        result = ai_polish.apply_changes(data, {'p1.headline': '고친 제목'})
        self.assertNotIn('approvedBy', result)
        self.assertEqual(result['editorialReview']['semanticRecheck'], 'pending')
        self.assertEqual(ai_polish.apply_changes(data, {}), data)
        self.assertIn('approvedBy', data)

    def test_duplicate_or_missing_response_ids_are_rejected(self):
        items = [{'id': 'a'}, {'id': 'b'}]
        row = {'id': 'a', 'text': '문구', 'changed': False, 'rules': [], 'reason': ''}
        for rows in ([row], [row, row]):
            with self.assertRaises(ValueError):
                ai_polish.validate_response(items, {'items': rows})

    def test_small_numbers_quotes_and_added_hedges_are_not_silently_changed(self):
        for old, new in [('대상은 2 곳입니다.', '대상은 3 곳입니다.'),
                         ('“확인합니다”라고 말했습니다.', '“검토합니다”라고 말했습니다.'),
                         ('기준을 확인합니다.', '기준을 확인할 수 있습니다.')]:
            self.assertFalse(ai_polish.check({'text': old, 'max_length': 100}, {'text': new, 'changed': True})[0])

    def test_english_prompt_is_native_marketing_copy_with_legal_boundaries(self):
        rules = ai_polish.ETHOS_EN_RULES
        for phrase in ('professional English-speaking reader', "reader's situation",
                       'Administrative Attorney Office', 'AND/OR', 'free preliminary review'):
            self.assertIn(phrase, rules)
        payload = ai_polish.request_payload([{'context': {'channel': 'card'}}], 'en')
        self.assertEqual(payload['language'], 'en')
        self.assertIn('native professional English', payload['editorialGoal'])

    def test_english_qualifiers_are_protected_and_card_limits_are_language_specific(self):
        original = {'text': 'You may file online or by mail.', 'max_length': 100}
        changed = {'text': 'You must file online and by mail.', 'changed': True}
        ok, note = ai_polish.check(original, changed, 'en')
        self.assertFalse(ok)
        self.assertIn('may', note)
        data = {'cards': [card(headline='A natural English headline', takeaway='A clear English conclusion.')]}
        items = ai_polish.collect(data, lang='en')
        self.assertEqual(items[0]['max_length'], copy_lint.LIMITS['headline']['coverEn'])

    def test_english_prose_collection_skips_korean_only_blocks(self):
        text = '# Title\n\nA useful English paragraph.\n\n한국어 문단입니다.\n\n> Quoted English.'
        items = ai_polish.collect_prose(text, 'blog', 'en')
        self.assertEqual([item['text'] for item in items], ['A useful English paragraph.'])

    def test_thirty_percent_limit_matches_policy(self):
        with patch.object(ai_polish, 'change_ratio', return_value=0.31):
            ok, note = ai_polish.check({'text': '기준을 먼저 확인합니다.', 'max_length': 100},
                                       {'text': '기준부터 확인합니다.', 'changed': True})
        self.assertFalse(ok)
        self.assertIn('30%', note)

    def test_kiwi_sentence_split_and_fallback(self):
        analyser = copy_lint.kiwi()
        if analyser:
            text = '자료를 확인합니다.\n다음 절차를 안내합니다.'
            self.assertEqual(copy_lint.split_sentences(text), [s.text.strip() for s in analyser.split_into_sents(text)])
        with patch.object(copy_lint, 'kiwi', return_value=None):
            self.assertEqual(copy_lint.split_sentences('확인합니다. 다음입니다.'), ['확인합니다.', '다음입니다.'])

    def test_blog_only_cli_and_offline_prose_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = pathlib.Path(tmp)
            blog = folder / 'blog.md'
            blog.write_text('기준을 먼저 확인합니다.', encoding='utf-8')
            lint = subprocess.run([sys.executable, str(ROOT / 'scripts/copy_lint.py'), tmp, '--blog'], capture_output=True)
            self.assertEqual(lint.returncode, 0, lint.stderr)
            request = ai_polish.collect_prose(blog.read_text(encoding='utf-8'), 'blog')
            response = folder / 'response.json'
            response.write_text(json.dumps({'items': [{'id': request[0]['id'], 'text': '기준부터 확인합니다.',
                                                       'changed': True, 'rules': ['I-2'], 'reason': '간결하게'}]}), encoding='utf-8')
            run = subprocess.run([sys.executable, str(ROOT / 'scripts/ai_polish.py'), '--text', str(blog),
                                  '--response-file', str(response), '--report', str(folder / 'report.md')], capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(blog.read_text(encoding='utf-8'), '기준을 먼저 확인합니다.')
            self.assertIn('API 미사용', (folder / 'report.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
