"""Public request runner regression checks; no external model calls."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts import proofreader_request as rq

BRANCH = 'proofreader/request/test-request-01'
COMMIT = 'a' * 40
TEXT = '자료는 3쪽 이하로 작성할 수 있습니다. 파일은 이메일 또는 공유 폴더로 전달합니다.\n\n회의 자료를 정리하며 원본을 따로 남깁니다.'


def report(text=TEXT, verdict='✅'):
    return '✅ **교정을 마쳤습니다.**\n\n---\n\n## 교정본\n\n' + text + '\n\n---\n\n' + verdict + ' **원고 대조 — 확인했습니다.**\n'


class RequestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root / '_proofreader/requests/test-request-01'
        self.folder.mkdir(parents=True)
        (self.folder / 'source.md').write_bytes(TEXT.encode('utf-8'))
        self.data = dict(version=1, request_id='test-request-01', base_commit=COMMIT,
                         source_sha256=rq.sha256(TEXT.encode('utf-8')), mode='proofread',
                         consent=dict(public_repository=True, external_processing=True,
                                      no_private_data=True, authorization='공개 가능한 시험 원고의 실행 승인'),
                         preserve=['자료는 3쪽 이하로 작성할 수 있습니다.'])
        self.save()
        self.env = patch.dict(os.environ, {'ETHOS_UPSTAGE_API_KEY': '', 'ETHOS_OPENROUTER_API_KEY': ''})
        self.env.start()
        self.addCleanup(self.env.stop)

    def save(self):
        (self.folder / 'request.json').write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')

    def load(self):
        return rq.load_request(self.root, BRANCH)

    def run_request(self, response=None):
        with patch.object(rq.hp, 'call_remote', return_value=response or report()) as call:
            summary = rq.process(self.root, BRANCH, COMMIT, 'https://github.com/example/run', verify=False)
        return summary, call

    def test_valid_request(self):
        data, text, _ = self.load()
        self.assertEqual(data['request_id'], 'test-request-01')
        self.assertEqual(text, TEXT)

    def test_main_is_never_a_request_branch(self):
        with self.assertRaises(ValueError):
            rq.load_request(self.root, 'main')

    def test_path_traversal_ids_rejected(self):
        for name in ['../secret', 'abc/def', 'abc;echo', '-bad']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                rq.request_id(rq.BRANCH_PREFIX + name)

    def test_consent_must_be_explicit_boolean(self):
        for key in ('public_repository', 'external_processing', 'no_private_data'):
            for value in (False, 'true', 1, None):
                with self.subTest(key=key, value=value):
                    self.data['consent'][key] = value
                    self.save()
                    with self.assertRaises(ValueError):
                        self.load()
                self.data['consent'][key] = True

    def test_missing_authorization_rejected(self):
        self.data['consent']['authorization'] = ''
        self.save()
        with self.assertRaises(ValueError):
            self.load()

    def test_changed_source_rejected_before_network(self):
        (self.folder / 'source.md').write_text(TEXT + '추가', encoding='utf-8')
        summary, call = self.run_request()
        self.assertEqual(summary['status'], 'invalid_request')
        self.assertFalse(summary['external_attempted'])
        call.assert_not_called()

    def test_unknown_keys_rejected(self):
        self.data['endpoint'] = 'https://example.com'
        self.save()
        with self.assertRaises(ValueError):
            self.load()

    def test_deep_not_enabled(self):
        self.data['depth'] = 'deep'
        self.save()
        with self.assertRaises(ValueError):
            self.load()

    def test_wrong_id_rejected(self):
        self.data['request_id'] = 'other-id'
        self.save()
        with self.assertRaises(ValueError):
            self.load()

    def test_preserve_must_exist(self):
        self.data['preserve'] = ['없는 문장']
        self.save()
        with self.assertRaises(ValueError):
            self.load()

    def test_utf16_input_limit(self):
        text = '가' * 20001
        (self.folder / 'source.md').write_text(text, encoding='utf-8')
        self.data.update(source_sha256=rq.sha256(text.encode()), preserve=[])
        self.save()
        with self.assertRaises(ValueError):
            self.load()

    def test_symlink_input_blocked(self):
        source = self.folder / 'source.md'
        source.unlink()
        target = self.root / 'private.md'
        target.write_text(TEXT, encoding='utf-8')
        try:
            source.symlink_to(target)
        except OSError:
            self.skipTest('symlink privilege unavailable')
        with self.assertRaises(ValueError):
            self.load()

    def test_success_produces_retrievable_files(self):
        summary, call = self.run_request()
        self.assertEqual(summary['status'], 'succeeded')
        self.assertEqual(call.call_args.args[0], rq.hp.DEFAULT_URL)
        self.assertEqual(call.call_args.args[2]['strength'], '보수')
        self.assertEqual(call.call_args.args[2]['depth'], 'standard')
        self.assertFalse(summary['publication_approved'])
        self.assertEqual(summary['semantic_review'], 'pending')
        output = self.root / '_proofreader/results/test-request-01'
        self.assertEqual((output / 'proposal.md').read_text(encoding='utf-8'), TEXT)
        self.assertTrue((output / 'changes.diff').is_file())
        self.assertEqual((self.folder / 'source.md').read_text(encoding='utf-8'), TEXT)
        self.assertTrue(summary['source_unchanged'])

    def test_remote_abort_cannot_pass(self):
        summary, _ = self.run_request(report(verdict='⛔'))
        self.assertEqual(summary['status'], 'gate_rejected')
        self.assertFalse(summary['remote_gate'])

    def test_number_change_cannot_pass(self):
        summary, _ = self.run_request(report(TEXT.replace('3쪽', '4쪽')))
        self.assertEqual(summary['status'], 'gate_rejected')
        self.assertFalse(summary['local_gate'])
        self.assertFalse(summary['preserve_gate'])

    def test_unknown_remote_format_saves_raw_report(self):
        summary, _ = self.run_request('예상하지 못한 응답')
        self.assertEqual(summary['status'], 'gate_rejected')
        self.assertTrue((self.root / '_proofreader/results/test-request-01/report.md').is_file())

    def test_provider_failure_is_not_success_and_is_not_retried(self):
        with patch.object(rq.hp, 'call_remote', side_effect=rq.hp.ProofreaderError('PRIVATE BODY')) as call:
            summary = rq.process(self.root, BRANCH, COMMIT, '', verify=False)
        self.assertEqual(call.call_count, 1)
        self.assertEqual(summary['status'], 'remote_error')
        self.assertNotIn('PRIVATE BODY', json.dumps(summary))

    def test_personal_paid_keys_blocked(self):
        with patch.dict(os.environ, {'ETHOS_UPSTAGE_API_KEY': 'test-not-real'}):
            summary, call = self.run_request()
        self.assertFalse(summary['external_attempted'])
        call.assert_not_called()

    def test_duplicate_results_cannot_be_overwritten(self):
        self.run_request()
        with patch.object(rq.hp, 'call_remote') as call:
            with self.assertRaises(ValueError):
                rq.process(self.root, BRANCH, COMMIT, '', verify=False)
        call.assert_not_called()

    def test_diagnosis_does_not_invent_proposal(self):
        self.data['mode'] = 'read_through'
        self.save()
        summary, _ = self.run_request('통독 소견')
        self.assertEqual(summary['status'], 'succeeded')
        self.assertFalse((self.root / '_proofreader/results/test-request-01/proposal.md').exists())

    def test_tree_validation_blocks_nonrequest_changes(self):
        with patch.object(rq, 'git', side_effect=[COMMIT, '', 'scripts/unsafe.py']):
            with self.assertRaises(ValueError):
                rq.verify_tree(self.root, self.data, COMMIT)

    def test_tree_validation_accepts_only_two_input_files(self):
        prefix = '_proofreader/requests/test-request-01/'
        with patch.object(rq, 'git', side_effect=[COMMIT, '', prefix+'request.json\n'+prefix+'source.md']):
            rq.verify_tree(self.root, self.data, COMMIT)

    def test_bool_version_is_not_integer_version(self):
        self.data['version'] = True
        self.save()
        with self.assertRaises(ValueError):
            self.load()


if __name__ == '__main__':
    unittest.main()
