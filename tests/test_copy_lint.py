import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import copy_lint  # noqa: E402
from build_cards import build  # noqa: E402


def card(page, kind, headline, takeaway="기준을 확인하세요.", body=None, **extra):
    base = {"page": page, "type": kind, "bg": "navy", "oneMessage": headline, "headline": headline,
            "body": body or ["내용"], "takeaway": takeaway, "sourceTrace": {"heading": "h", "evidence": "F"}}
    base.update(extra)
    return base


def run(cards, lang="ko", terms=None):
    report = copy_lint.Report()
    copy_lint.lint_cards({"cards": cards}, lang, report, terms)
    return report


def rules(report):
    return {finding["rule"] for finding in report.findings}


class CopyLintTests(unittest.TestCase):
    def test_repeated_question_headlines_and_negative_framing_are_flagged(self):
        cards = [card(i, "concept", f"주제 {i}를 지금 정해야 할까요?", "그 둘은 같은 말이 아닙니다.") for i in range(1, 6)]
        found = rules(run(cards))
        self.assertIn("question-headlines", found)
        self.assertIn("negative-framing", found)

    def test_mid_sentence_negation_and_questions_are_not_negative_framing(self):
        cards = [card(1, "concept", "서버는 해외, 법인은 없습니다. 어떻게 할까요?", "지정하지 않으면 과태료가 있을 수 있습니다.")]
        self.assertNotIn("negative-framing", rules(run(cards)))

    def test_statute_numbers_are_limited_per_card(self):
        cards = [card(1, "concept", "기준", body=["제21조의5 해외게임물", "제21조의4 등급"])]
        self.assertIn("statute-density", rules(run(cards)))
        self.assertNotIn("statute-density", rules(run([card(1, "concept", "기준", body=["제21조의5 해외게임물"])])))

    def test_cover_must_promise_a_payoff(self):
        self.assertIn("cover-payoff", rules(run([card(1, "cover", "서버는 해외입니다")])))
        self.assertNotIn("cover-payoff", rules(run([card(1, "cover", "서버는 해외입니다", promise="출시 전 6가지 질문")])))

    def test_term_must_be_glossed_on_first_use(self):
        terms = {"ko": ["국내대리인"]}
        self.assertIn("unglossed-term", rules(run([card(1, "concept", "국내대리인을 지정하세요")], terms=terms)))
        self.assertNotIn("unglossed-term", rules(run([card(1, "concept", "국내대리인(연락을 맡는 국내 주체)을 지정하세요")], terms=terms)))

    def test_gloss_in_another_field_of_the_same_card_counts(self):
        terms = {"ko": ["E-7"]}
        glossed = card(1, "cover", "E-7 채용이 막힐까요?", body=["E-7 — 지정된 전문활동을 위한 체류자격"])
        self.assertNotIn("unglossed-term", rules(run([glossed], terms=terms)))

    def test_unresolved_marker_is_flagged(self):
        self.assertIn("placeholder", rules(run([card(1, "concept", "기준", takeaway="확인 못 했습니다 [미확인]")])))

    def test_placeholder_is_flagged(self):
        self.assertIn("placeholder", rules(run([card(1, "concept", "기준", body=["출처 입력"])])))

    def test_protected_token_diff_catches_removed_and_added_facts(self):
        old = {"cards": [card(1, "concept", "기준", body=["제21조의5, 2천만 원"])]}
        new = {"cards": [card(1, "concept", "기준", body=["제21조의4, 2천만 원"])]}
        report = copy_lint.Report()
        copy_lint.compare(old, new, report)
        messages = " ".join(f["message"] for f in report.findings)
        self.assertIn("제21조의5", messages)
        self.assertIn("제21조의4", messages)
        self.assertNotIn("2천만원", messages)

    def test_moved_to_caption_is_info_only(self):
        old = {"cards": [card(1, "concept", "기준", body=["제21조의5"])]}
        new = {"cards": [card(1, "concept", "기준", body=["특례"])]}
        report = copy_lint.Report()
        copy_lint.compare(old, new, report, moved_to="근거: 제21조의5")
        self.assertEqual({f["level"] for f in report.findings}, {"info"})


class BuilderComponentTests(unittest.TestCase):
    DATA = {"language": "ko", "series": "S", "issue": "No.1", "totalPages": 6, "canvasProfile": "portrait", "visualFamily": "social-native"}

    def test_new_components_render_from_data_not_page_numbers(self):
        flow = build(card(3, "flow", "흐름", body=[{"key": "A", "text": "a"}, {"key": "B", "text": "b"}], note="보충"), self.DATA)
        self.assertIn('class="flow flow-2"', flow)
        self.assertIn("flow-note", flow)
        table = build(card(9, "table", "표", body=[{"key": "Q", "text": "A"}], head=["질문", "답"]), self.DATA)
        self.assertIn("tbl-head", table)
        cover = build(card(1, "cover", "표지", promise="6가지 질문"), self.DATA)
        self.assertIn("cover-promise", cover)

    def test_checklist_layout_is_data_driven(self):
        questions = build(card(2, "checklist", "q", body=["a", "b", "c"], layout="questions"), self.DATA)
        keyed = build(card(8, "checklist", "k", body=[{"key": "1조 원", "text": "t"}]), self.DATA)
        plain8 = build(card(8, "checklist", "p", body=["x"]), self.DATA)
        self.assertIn("question-grid", questions)
        self.assertIn(">1조 원<", keyed)
        self.assertNotIn("1조 원", plain8)
        self.assertNotIn("question-grid", build(card(6, "checklist", "p", body=["x"]), self.DATA))

    def test_take_style_defaults_by_type_and_can_be_overridden(self):
        self.assertIn('class="take"', build(card(2, "cta", "c"), self.DATA))
        self.assertIn("editorial-close", build(card(1, "concept", "c"), self.DATA))
        self.assertIn('class="take"', build(card(5, "concept", "c", takeStyle="bar"), self.DATA))


class IconTests(unittest.TestCase):
    DATA = BuilderComponentTests.DATA

    def test_icons_render_inline_and_unknown_icons_fail_loudly(self):
        badge = build(card(2, "concept", "c", icon="scale"), self.DATA)
        self.assertIn('class="card-icon"', badge)
        self.assertIn("has-icon", badge)
        self.assertIn('class="ico"', badge)
        self.assertNotIn(" width=", badge.split("<svg", 1)[1].split(">", 1)[0])
        art = build(card(1, "cover", "c", art=["server", "landmark"]), self.DATA)
        self.assertEqual(art.count("art-disc"), 2)
        with self.assertRaises(ValueError):
            build(card(2, "concept", "c", icon="not-a-real-icon"), self.DATA)
        with self.assertRaises(ValueError):
            build(card(2, "concept", "c", icon="../../etc/passwd"), self.DATA)

    def test_no_icon_means_no_icon_markup(self):
        plain = build(card(2, "concept", "c"), self.DATA)
        self.assertNotIn("has-icon", plain)
        self.assertNotIn("<svg", plain)

    def test_stats_layout_and_item_icons(self):
        stats = build(card(8, "checklist", "s", layout="stats", body=[{"key": "1조 원", "text": "t", "icon": "check"}]), self.DATA)
        self.assertIn("stat-row", stats)
        self.assertIn("ico-wrap", stats)

    def test_unrecorded_icon_is_flagged(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            folder = pathlib.Path(tmp)
            (folder / "assets.md").write_text("EXTERNAL ASSETS: Yes\n| lucide/scale.svg |", encoding="utf-8")
            report = copy_lint.Report()
            copy_lint.lint_assets(folder, {"ko": {"cards": [card(1, "cover", "c", art=["server", "scale"])]}}, report)
        self.assertEqual(sum("server" in f["message"] for f in report.findings), 1)
        self.assertFalse(any("'scale'" in f["message"] for f in report.findings))


class LimitTests(unittest.TestCase):
    def lint(self, cards, lang="ko"):
        report = copy_lint.Report()
        copy_lint.lint_limits({"cards": cards}, lang, report)
        return report

    def test_slightly_over_limit_is_info_and_far_over_is_warn(self):
        slight = self.lint([card(1, "concept", "가" * 33)])
        far = self.lint([card(1, "concept", "가" * 60)])
        self.assertEqual({f["level"] for f in slight.findings if f["rule"] == "over-limit"}, {"info"})
        self.assertEqual({f["level"] for f in far.findings if f["rule"] == "over-limit"}, {"warn"})

    def test_item_count_and_field_limits_follow_the_card_shape(self):
        rows = [{"key": "k", "text": "t"}] * 7
        self.assertIn("item-count", rules(self.lint([card(1, "table", "표", body=rows)])))
        long_key = [{"key": "가" * 40, "text": "t"}] * 3
        self.assertIn("over-limit", rules(self.lint([card(1, "flow", "흐름", body=long_key)])))
        self.assertEqual(rules(self.lint([card(1, "table", "표", body=[{"key": "k", "text": "t"}] * 3)])), set())

    def test_every_limit_key_has_a_matching_card_shape(self):
        import copy_lint as lint
        for name in lint.LIMITS["types"]:
            self.assertIn("items", lint.LIMITS["types"][name], name)


class CiRenderTests(unittest.TestCase):
    def test_explicit_ids_win_and_templates_are_skipped(self):
        import argparse
        import ci_render
        self.assertEqual(ci_render.content_ids(argparse.Namespace(ids=["A-01"], changed=None)), ["A-01"])
        ids = ci_render.content_ids(argparse.Namespace(ids=None, changed="0" * 40))
        self.assertTrue(ids)
        self.assertFalse(any(i.startswith(("_", ".")) for i in ids))


class SyncPhilosophyTests(unittest.TestCase):
    def test_copy_is_headed_and_idempotent(self):
        import tempfile
        import sync_philosophy
        source = (ROOT / "docs" / "brand-philosophy.md").read_text(encoding="utf-8")
        content = sync_philosophy.build_copy(source, "abc1234")
        self.assertTrue(content.startswith("<!-- 자동 동기화 사본"))
        self.assertIn("abc1234", content.splitlines()[0])
        self.assertIn(sync_philosophy.version_of(source), content.splitlines()[0])
        self.assertTrue(content.endswith(source.lstrip("﻿")))
        with tempfile.TemporaryDirectory() as tmp:
            dest = pathlib.Path(tmp) / "docs" / "contracts" / "brand-philosophy.md"
            dest.parent.mkdir(parents=True)
            dest.write_text("사람이 고친 사본", encoding="utf-8")
            sync_philosophy.sys.argv = ["x", "--dest", str(dest), "--commit", "abc1234"]
            sync_philosophy.main()
            self.assertEqual(dest.read_text(encoding="utf-8"), content)
            self.assertTrue(sync_philosophy.matches_copy(dest, content))
            self.assertFalse(sync_philosophy.matches_copy(dest, content + "changed"))

            sync_philosophy.sys.argv = ["x", "--compare", str(dest), "--commit", "abc1234"]
            self.assertEqual(sync_philosophy.main(), 0)
            dest.write_text("outdated", encoding="utf-8")
            self.assertEqual(sync_philosophy.main(), 1)

    def test_missing_version_line_fails(self):
        import sync_philosophy
        with self.assertRaises(SystemExit):
            sync_philosophy.build_copy("버전 줄 없음", "x")


class CommittedSetsStayIdentical(unittest.TestCase):
    """Approved sets must rebuild byte-for-byte, so refactors cannot silently restyle published cards."""

    def test_rebuild_matches_committed_html(self):
        for content_id in ("GAME-OVERSEAS-06", "SUSPENSION-SURCHARGE-04"):
            for lang in ("ko", "en"):
                folder = ROOT / "content" / content_id
                data = json.loads((folder / f"card-data.{lang}.json").read_text(encoding="utf-8"))
                for item in data["cards"]:
                    committed = (folder / lang / f"card_{item['page']:02d}.html").read_text(encoding="utf-8")
                    self.assertEqual(build(item, data), committed, f"{content_id}/{lang}/card_{item['page']:02d}")


if __name__ == "__main__":
    unittest.main()
