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


class LayoutVariantTests(unittest.TestCase):
    V2 = dict(BuilderComponentTests.DATA, editorialReview={"pipelineVersion": "2.0"})
    LEGACY = dict(BuilderComponentTests.DATA, editorialReview={"pipelineVersion": "legacy"})

    def short_card(self, **extra):
        return card(3, "comparison", "짧은 제목", body=[{"key": "가", "text": "나"}, {"key": "다", "text": "라"}], **extra)

    def test_density_only_applies_to_v2_sets(self):
        self.assertIn("dens-low", build(self.short_card(), self.V2))
        self.assertNotIn("dens-low", build(self.short_card(), self.LEGACY))
        self.assertNotIn("dens-low", build(self.short_card(), BuilderComponentTests.DATA))

    def test_dense_cards_get_no_density_class(self):
        body = [{"key": "가" * 10, "text": "나" * 90}] * 2
        self.assertNotIn("dens-", build(card(3, "comparison", "제목", body=body), self.V2))

    def test_illustration_only_when_card_is_light_and_headline_short(self):
        self.assertIn("il-wrap", build(self.short_card(illustration="documents"), self.V2))
        self.assertNotIn("il-wrap", build(self.short_card(illustration="documents"), self.LEGACY))
        long_title = card(3, "comparison", "가" * 40, body=[{"key": "가", "text": "나"}] * 2, illustration="documents")
        self.assertNotIn("il-wrap", build(long_title, self.V2))
        heavy = card(3, "comparison", "제목", body=[{"key": "가" * 10, "text": "나" * 90}] * 2, illustration="documents")
        self.assertNotIn("il-wrap", build(heavy, self.V2))

    def test_unknown_or_unsafe_illustration_fails(self):
        for name in ("nope", "../icons/lucide/server"):
            with self.assertRaises(ValueError):
                build(self.short_card(illustration=name), self.V2)

    def test_cover_styles(self):
        panel = build(card(1, "cover", "표지", coverStyle="panel", illustration="bridge"), self.V2)
        self.assertIn("cover-panel", panel)
        self.assertNotIn("cover-art", panel)
        stat = build(card(1, "cover", "표지", coverStyle="stat", hero={"value": "6", "label": "가지 질문"}), self.V2)
        self.assertIn("hero-val", stat)

    def test_every_illustration_file_renders(self):
        for path in sorted((ROOT / "assets" / "illustrations").glob("*.svg")):
            self.assertIn('class="il"', __import__("build_cards").illustration_svg(path.stem))


class AiPolishGuardTests(unittest.TestCase):
    def setUp(self):
        import ai_polish
        self.p = ai_polish
        self.original = {"id": "p8.takeaway", "text": "지정하지 않으면 2천만 원 이하 과태료 대상이 될 수 있습니다.", "max_length": 40}

    def suggest(self, text):
        return {"id": "p8.takeaway", "text": text, "changed": True, "rules": ["A-1"], "reason": "r"}

    def test_fact_token_change_is_rejected(self):
        ok, note = self.p.check(self.original, self.suggest("지정하지 않으면 3천만 원 이하 과태료 대상이 될 수 있습니다."))
        self.assertFalse(ok)
        self.assertIn("사실 토큰", note)

    def test_too_long_and_too_different_are_rejected(self):
        self.assertFalse(self.p.check(self.original, self.suggest("가" * 41))[0])
        self.assertFalse(self.p.check(self.original, self.suggest("2천만 원 이하 과태료. 전혀 다른 문장."))[0])

    def test_small_natural_edit_is_accepted(self):
        ok, _ = self.p.check(self.original, self.suggest("지정하지 않으면 2천만 원 이하 과태료를 낼 수 있습니다."))
        self.assertTrue(ok)

    def test_unchanged_is_not_a_suggestion(self):
        self.assertFalse(self.p.check(self.original, dict(self.suggest(self.original["text"]), changed=False))[0])

    def test_apply_changes_patches_strings_and_dicts_without_touching_source(self):
        data = {"cards": [card(1, "concept", "제목", body=["가", {"key": "k", "text": "나"}])]}
        patched = self.p.apply_changes(data, {"p1.body.0": "다", "p1.body.1": "라", "p1.headline": "새 제목"})
        self.assertEqual(patched["cards"][0]["body"], ["다", {"key": "k", "text": "라"}])
        self.assertEqual(patched["cards"][0]["headline"], "새 제목")
        self.assertEqual(data["cards"][0]["headline"], "제목")

    def test_quote_cards_are_not_sent_for_rewriting(self):
        data = {"cards": [card(2, "quote", "판례", body=["대법원 2008도3970", "판시", "메모"])]}
        ids = [item["id"] for item in self.p.collect(data)]
        self.assertNotIn("p2.body.0", ids)


class KiwiEndingTests(unittest.TestCase):
    def test_same_ending_run_is_reported(self):
        if not copy_lint.kiwi():
            self.skipTest("kiwipiepy not installed")
        cards = [card(i, "concept", f"제목 {i}", takeaway="확인이 필요합니다.") for i in range(1, 6)]
        self.assertIn("ending-run", rules(run(cards)))
        mixed = [card(i, "concept", f"제목 {i}", takeaway=t) for i, t in enumerate(["확인합니다.", "확인하세요.", "구조부터.", "봅니다.", "끝입니다."], 1)]
        self.assertNotIn("ending-run", rules(run(mixed)))

    def test_allomorphs_count_as_one_ending(self):
        if not copy_lint.kiwi():
            self.skipTest("kiwipiepy not installed")
        self.assertEqual(copy_lint.sentence_ending("확인합니다."), copy_lint.sentence_ending("있습니다."))


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
