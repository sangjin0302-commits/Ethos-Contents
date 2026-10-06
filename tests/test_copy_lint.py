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

    def test_dropped_hedge_is_flagged_on_compare(self):
        old = {"cards": [card(1, "concept", "기준", takeaway="과태료 대상이 될 수 있습니다.")]}
        new = {"cards": [card(1, "concept", "기준", takeaway="과태료 대상입니다.")]}
        report = copy_lint.Report()
        copy_lint.compare(old, new, report)
        self.assertIn("hedge-removed", {f["rule"] for f in report.findings})

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


class InformationTests(unittest.TestCase):
    def lint(self, cards, lang="ko"):
        report = copy_lint.Report()
        copy_lint.lint_information({"cards": cards}, lang, report)
        return report

    def test_thin_set_is_flagged_and_full_set_is_not(self):
        thin = [card(i, "concept", "제목", takeaway="결론", body=["짧은 항목"]) for i in range(1, 7)]
        full = [card(i, "concept", "가" * 28, takeaway="나" * 50, body=["다" * 90]) for i in range(1, 7)]
        self.assertIn("thin-set", rules(self.lint(thin)))
        self.assertIn("thin-cards", rules(self.lint(thin)))
        self.assertEqual(rules(self.lint(full)), set())

    def test_cover_cta_and_quote_do_not_count_as_thin_cards(self):
        cards = [card(1, "cover", "제목", takeaway="결", body=["표지"]), card(2, "cta", "제목", takeaway="결", body=["안내"]),
                 card(3, "quote", "제목", takeaway="결", body=["인용"]), card(4, "concept", "가" * 28, takeaway="나" * 50, body=["다" * 400])]
        self.assertNotIn("thin-cards", rules(self.lint(cards)))


class TablerAndBarsTests(unittest.TestCase):
    DATA = BuilderComponentTests.DATA

    def test_tabler_icons_resolve_after_lucide_and_need_their_own_provenance_row(self):
        import tempfile
        page = build(card(2, "concept", "c", icon="building-bank"), self.DATA)
        self.assertIn('class="ico"', page)
        self.assertNotIn("icon-tabler", page)  # the source class attribute is stripped when vendored
        with tempfile.TemporaryDirectory() as tmp:
            folder = pathlib.Path(tmp)
            (folder / "assets.md").write_text("EXTERNAL ASSETS: Yes\n| lucide/building-bank.svg |", encoding="utf-8")
            report = copy_lint.Report()
            copy_lint.lint_assets(folder, {"ko": {"cards": [card(1, "cover", "c", art=["building-bank", "scale"])]}}, report)
            self.assertTrue(any("building-bank" in f["message"] for f in report.findings))
            (folder / "assets.md").write_text("EXTERNAL ASSETS: Yes\n| tabler/building-bank.svg |", encoding="utf-8")
            report = copy_lint.Report()
            copy_lint.lint_assets(folder, {"ko": {"cards": [card(1, "cover", "c", art=["building-bank"])]}}, report)
            self.assertFalse(any("building-bank" in f["message"] for f in report.findings))

    def bars(self, rows):
        return card(5, "checklist", "b", layout="bars", body=rows)

    def test_bars_length_follows_value_and_shows_display_text(self):
        html = build(self.bars([{"key": "사전통지", "text": "", "value": 6, "display": "6개월"}, {"key": "최종", "text": "t", "value": 3, "display": "3개월"}]), self.DATA)
        self.assertIn("width:100.0%", html)
        self.assertIn("width:50.0%", html)
        self.assertIn("6개월", html)
        self.assertEqual(html.count('class="bar-copy"'), 1)  # empty text draws no empty line

    def test_smallest_bar_keeps_a_visible_stub(self):
        html = build(self.bars([{"key": "a", "text": "", "value": 100, "display": "100"}, {"key": "b", "text": "", "value": 1, "display": "1"}]), self.DATA)
        self.assertIn("width:7.0%", html)

    def test_bars_lint_flags_missing_numbers_and_mixed_units(self):
        report = copy_lint.Report()
        copy_lint.lint_bars({"cards": [self.bars([{"key": "a", "text": "t", "value": 6, "display": "6개월"}, {"key": "b", "text": "t", "value": 3, "display": "3일"}])]}, "ko", report)
        self.assertIn("bars-units", rules(report))
        report = copy_lint.Report()
        copy_lint.lint_bars({"cards": [self.bars([{"key": "a", "text": "t"}, {"key": "b", "text": "t", "value": 3, "display": "많이"}])]}, "ko", report)
        self.assertEqual(sum(f["rule"] == "bars-data" for f in report.findings), 2)
        report = copy_lint.Report()
        copy_lint.lint_bars({"cards": [self.bars([{"key": "a", "text": "t", "value": 6, "display": "6개월"}, {"key": "b", "text": "t", "value": 3, "display": "3개월"}])]}, "ko", report)
        self.assertEqual(report.findings, [])


class IconSuffixTests(unittest.TestCase):
    DATA = BuilderComponentTests.DATA

    def test_svg_suffix_is_accepted_and_means_the_same_icon(self):
        self.assertEqual(build(card(2, "concept", "c", icon="scale.svg"), self.DATA), build(card(2, "concept", "c", icon="scale"), self.DATA))
        with self.assertRaises(ValueError):
            build(card(2, "concept", "c", icon="../scale.svg"), self.DATA)
        data = {"cards": [card(1, "cover", "c", art=["scale.svg", "server"])]}
        self.assertEqual(copy_lint.used_icons(data), {"scale", "server"})

    def test_schema_accepts_the_suffix_but_not_paths(self):
        from jsonschema import Draft7Validator
        schema = json.loads((ROOT / "schema" / "card-data.schema.json").read_text(encoding="utf-8"))
        icon = Draft7Validator(schema["definitions"]["icon"])
        self.assertTrue(icon.is_valid("scale.svg"))
        self.assertTrue(icon.is_valid("scale"))
        self.assertFalse(icon.is_valid("../scale.svg"))
        self.assertFalse(icon.is_valid("scale.png"))


class VisualAndChainTests(unittest.TestCase):
    DATA = BuilderComponentTests.DATA

    def test_plain_set_and_plain_cover_are_flagged(self):
        cards = [card(1, "cover", "c")] + [card(i, "concept", "c") for i in range(2, 7)]
        report = copy_lint.Report()
        copy_lint.lint_visuals({"cards": cards}, "ko", report)
        self.assertEqual({f["rule"] for f in report.findings}, {"plain-set", "plain-cover"})
        cards[0]["art"] = ["scale", "server"]
        cards[1]["icon"] = "scale"
        cards[2]["layout"] = "bars"
        report = copy_lint.Report()
        copy_lint.lint_visuals({"cards": cards}, "ko", report)
        self.assertEqual(report.findings, [])

    def test_dense_set_is_flagged(self):
        dense = [card(i, "concept", "가" * 28, takeaway="나" * 50, body=["다" * 200]) for i in range(1, 7)]
        report = copy_lint.Report()
        copy_lint.lint_information({"cards": dense}, "ko", report)
        self.assertIn("dense-set", rules(report))

    def test_long_dot_chain_may_wrap_but_short_one_stays_together(self):
        short = build(card(2, "concept", "c", body=[{"key": "k", "text": "과실·시정 노력을 봅니다"}]), self.DATA)
        longer = build(card(2, "concept", "c", body=[{"key": "k", "text": "적용 법률·위반조항·위반차수·예정기간을 표시합니다"}]), self.DATA)
        self.assertIn('<span class="nobr">과실·시정</span>', short)
        self.assertNotIn("위반조항·위반차수·예정기간</span>", longer)


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

    def test_concept_items_without_key_use_full_width(self):
        html = build(card(3, "concept", "제목", body=["그렇지 않습니다.", "위반사실은 남습니다.", "따로 확인합니다."]), BuilderComponentTests.DATA)
        self.assertIn("rule-item no-key", html)
        self.assertNotIn('data-role="subheading"></div>', html)

    def test_legacy_set_can_opt_into_v2_layout_without_editorial_records(self):
        self.assertIn("dens-low", build(self.short_card(), {**self.LEGACY, "layoutVersion": "2"}))

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


class StyleTests(unittest.TestCase):
    def style(self, text, repeat=3):
        report = copy_lint.Report()
        copy_lint.style_ko(text, report, "blog", repeat)
        return report

    def test_repeated_connector_and_translationese_are_info_only(self):
        text = "\n".join(["따라서 A를 봅니다.", "따라서 B를 봅니다.", "따라서 C를 통해 봅니다.", "D를 통해 봅니다.", "E를 통해 봅니다."])
        report = self.style(text)
        self.assertIn("repeated-connector", rules(report))
        self.assertIn("translationese", rules(report))
        self.assertTrue(all(f["level"] == "info" for f in report.findings))

    def test_negative_run_is_reported_and_varied_text_is_quiet(self):
        negative = "\n".join(["그렇지 않습니다.", "같은 말이 아닙니다.", "자동으로 되지 않습니다.", "먼저 구조를 보세요."])
        self.assertIn("negative-run", rules(self.style(negative)))
        varied = "\n".join(["먼저 구조를 보세요.", "등급은 플랫폼마다 따로 받습니다.", "대리인은 연락 창구입니다."])
        self.assertEqual(rules(self.style(varied)), set())

    def test_english_readability_flags_noun_piles_only(self):
        report = copy_lint.Report()
        dense = ("independent-rating business entity designated statutory distribution responsibilities "
                 "administrative obligations notwithstanding jurisdictional classification determinations apply")
        plain = "The platform rates the game. Each store needs its own rating. Check this before launch."
        copy_lint.style_en([("card 1", dense), ("card 2", plain)], report, "[en]")
        where = {f["where"] for f in report.findings if f["rule"] == "en-readability"}
        self.assertEqual(where, {"[en] card 1"})


class PublishHygieneTests(unittest.TestCase):
    def test_tracking_links_and_markdown_bold_are_flagged(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "blog.md"
            path.write_text("출처 https://www.law.go.kr/x?ID=1&OC=abc\n**굵게**\nhttps://a.kr/?UTM_SOURCE_PLATFORM=x\n정상 문장입니다.\n", encoding="utf-8")
            report = copy_lint.Report()
            copy_lint.lint_blog(path, report)
        self.assertTrue({"tracking-link", "markdown-bold"} <= rules(report))
        tracked = next(f for f in report.findings if f["rule"] == "tracking-link")
        self.assertIn("2곳", tracked["message"])

    def test_take_bar_share_over_forty_percent_is_info(self):
        cards = [card(i, "concept", f"제목 {i}", takeStyle="bar") for i in range(1, 7)]
        found = [f for f in run(cards).findings if f["rule"] == "take-bar-share"]
        self.assertEqual([f["level"] for f in found], ["info"])

    def test_fit_script_only_for_v2_non_cover_cards(self):
        v2 = dict(BuilderComponentTests.DATA, editorialReview={"pipelineVersion": "2.0"})
        self.assertIn("data-fit", build(card(2, "concept", "제목"), v2))
        self.assertNotIn("data-fit", build(card(2, "concept", "제목"), BuilderComponentTests.DATA))


class FreeDesignTests(unittest.TestCase):
    def test_copy_lock_accepts_line_breaks_and_flags_changed_copy(self):
        item = card(2, "concept", "6개월은 이렇게 정해집니다", "기준을 먼저 맞춰봅니다.", body=[{"key": "법률", "text": "6개월 범위 안에서 정합니다."}])
        good = '<meta name="ethos-design" content="free"><h2>6개월은 이렇게<br>정해집니다</h2><p>법률</p><p>6개월 범위 안에서 정합니다.</p><p>기준을 먼저 맞춰봅니다.</p>'
        self.assertTrue(copy_lint.is_free_design(good))
        self.assertEqual(copy_lint.copy_lock(item, good), [])
        changed = good.replace("6개월 범위 안에서", "6개월 안에서")
        self.assertEqual(copy_lint.copy_lock(item, changed), ["6개월 범위 안에서 정합니다."])

    def test_free_design_example_matches_its_card_data(self):
        folder = ROOT / "examples" / "free-design-realtor"
        data = json.loads((folder / "card-data.ko.json").read_text(encoding="utf-8"))
        for item in data["cards"]:
            html = (folder / "ko" / f"card_{item['page']:02d}.html").read_text(encoding="utf-8")
            self.assertTrue(copy_lint.is_free_design(html))
            self.assertEqual(copy_lint.copy_lock(item, html), [], f"card {item['page']}")


class WebsiteMarkdownTests(unittest.TestCase):
    def run_check(self, ko, en):
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as tmp:
            (pathlib.Path(tmp) / "website.ko.md").write_text(ko, encoding="utf-8")
            (pathlib.Path(tmp) / "website.en.md").write_text(en, encoding="utf-8")
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_website_md.py"), tmp], capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout

    def test_example_passes(self):
        folder = ROOT / "examples" / "website-md-realtor"
        code, out = self.run_check((folder / "website.ko.md").read_text(encoding="utf-8"), (folder / "website.en.md").read_text(encoding="utf-8"))
        self.assertEqual(code, 0, out)

    def test_table_heading_and_term_errors(self):
        ko = "---\nslug: a-b\ntitle: 제목\nexcerpt: 요약\ncategory: license\ntags: [\"a\"]\ndate: 2026-10-06\n---\n# 제목\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n무료 검토\n"
        en = "---\nslug: a-c\ntitleEn: Title here long\nexcerptEn: x\ncategory: license\ntagsEn: [\"a\"]\ndate: 2026-10-06\n---\nAsk a Korean administrative agent.\n\nfree review\n"
        code, out = self.run_check(ko, en)
        self.assertEqual(code, 1)
        for needle in ("'# 제목'", "마크다운 표", "Administrative Attorney", "'slug'가 다릅니다"):
            self.assertIn(needle, out)


NL = chr(10)


class WebsiteTagTests(unittest.TestCase):
    """Website tags are one comma-separated line without '#': the admin field splits on commas and stores text as typed."""

    run_check = WebsiteMarkdownTests.run_check

    def md(self, ko_tags, en_tags="x, y, z, w"):
        ko = NL.join(["---", "slug: a-b", "title: 제목", "excerpt: 요약", "category: license", f"tags: {ko_tags}", "date: 2026-10-06", "---", "## 소제목", "", "본문", "", "무료 검토", ""])
        en = NL.join(["---", "slug: a-b", "titleEn: Title here long", "excerptEn: x", "category: license", f"tagsEn: {en_tags}", "date: 2026-10-06", "---", "## Heading", "", "Body", "", "free review", ""])
        return self.run_check(ko, en)[1]

    def test_hash_in_a_website_tag_is_an_error(self):
        self.assertIn("'#'을 쓰지 않습니다", self.md("#영업정지, 과징금, 사전통지, 행정심판"))

    def test_comma_line_is_accepted_and_array_gets_a_hint(self):
        self.assertNotIn("'#'을 쓰지 않습니다", self.md("영업정지, 과징금, 사전통지, 행정심판"))
        self.assertIn("한 줄(쉼표 구분)", self.md('["영업정지", "과징금", "사전통지", "행정심판"]'))

    def test_tag_count_and_duplicates_are_hints(self):
        out = self.md("영업정지, 영업정지")
        self.assertIn("권장 4~10개", out)
        self.assertIn("같은 태그가 두 번", out)


class TagRuleTests(unittest.TestCase):
    def test_split_blog_tags_reads_only_the_trailing_hashtag_line(self):
        import tag_rules
        text = NL.join(["본문에 #해시 가 있어도 무시", "", "#가 #나 #다"])
        self.assertEqual(tag_rules.split_blog_tags(text), ["가", "나", "다"])
        self.assertEqual(tag_rules.split_blog_tags("본문만 있습니다."), [])

    def test_one_word_in_more_than_three_tags_is_flagged(self):
        import tag_rules
        crowded = ["행정사", "행정사업무범위", "행정사변호사차이", "행정사와변호사", "행정심판대리", "소송대리인자격", "허가거부대응", "불복기간", "보완요구", "식당사장님", "인허가대행", "사전통지"]
        self.assertTrue(any("'행정사'" in m for m in tag_rules.check(crowded, "blog")))
        spread = ["행정심판대리", "소송대리인자격", "허가거부대응", "불복기간", "보완요구", "식당사장님", "인허가대행", "사전통지", "행정사업무범위", "행정사와변호사", "이의신청", "거부처분"]
        self.assertEqual(tag_rules.check(spread, "blog"), [])

    def test_website_tags_dominated_by_two_words_are_flagged(self):
        import tag_rules
        tags = tag_rules.split_website_tags("행정사, 변호사, 행정사 변호사 차이, 행정사 업무범위, 변호사 업무범위, 인허가, 행정심판, 행정소송")
        self.assertTrue(any("몰려" in m for m in tag_rules.check(tags, "website")))
        self.assertEqual(tag_rules.check(tag_rules.split_website_tags("행정심판 대리, 소송대리인 자격, 인허가 대행, 허가 거부 대응"), "website"), [])

    def test_blog_lint_reports_missing_and_crowded_tags(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "blog.md"
            path.write_text("본문.", encoding="utf-8")
            report = copy_lint.Report()
            copy_lint.lint_blog(path, report)
            self.assertIn("blog-tags", rules(report))


class HighlightTests(unittest.TestCase):
    def test_highlight_wraps_one_exact_substring(self):
        html = build(card(2, "concept", "6개월은 이렇게 정해집니다", highlight="6개월"), BuilderComponentTests.DATA)
        self.assertEqual(html.count('<span class="mark-hl">6개월</span>'), 1)
        plain = build(card(2, "concept", "6개월은 이렇게 정해집니다", highlight="없는 말"), BuilderComponentTests.DATA)
        self.assertNotIn('mark-hl', plain)


class FixedTermTests(unittest.TestCase):
    def test_haengjeongsa_must_be_administrative_attorney(self):
        report = copy_lint.Report()
        copy_lint.fixed_terms_en([("card 1", "Ask a Korean administrative agent first."), ("card 2", "An Administrative Attorney reviews it."),
                                  ("card 3", "The UK administrative office handles appeals.")], report, "[en]")
        self.assertEqual([f["where"] for f in report.findings if f["rule"] == "fixed-term"], ["[en] card 1"])

    def test_english_org_name_uses_fixed_term(self):
        en = dict(BuilderComponentTests.DATA, language="en")
        self.assertIn("Ethos Administrative Attorney Office", build(card(2, "concept", "Title"), en))


class ShareImageTests(unittest.TestCase):
    def test_headline_size_shrinks_with_length_and_language(self):
        import build_og
        self.assertGreater(build_og.headline_size("짧은 제목", "ko"), build_og.headline_size("가" * 40, "ko"))
        self.assertGreater(build_og.headline_size("Short", "en"), build_og.headline_size("x" * 60, "en"))

    def test_html_has_safe_zone_and_no_page_number(self):
        import build_og
        data = {"language": "ko", "series": "시리즈", "cards": [card(1, "cover", "표지 제목", promise="6가지 질문", art=["server", "landmark"])]}
        html_text = build_og.og_html(data)
        self.assertIn("data-safe", html_text)
        self.assertIn("표지 제목", html_text)
        self.assertIn("6가지 질문", html_text)
        self.assertNotIn(" / 10", html_text)

    def test_set_without_cover_fails_loudly(self):
        import build_og
        with self.assertRaises(ValueError):
            build_og.cover_of({"cards": [card(1, "concept", "x")]})

    def test_html_escapes_markup_in_headline(self):
        import build_og
        data = {"language": "en", "series": "S", "cards": [card(1, "cover", "<script>alert(1)</script>")]}
        self.assertNotIn("<script>alert", build_og.og_html(data))


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
                    if copy_lint.is_free_design(committed):
                        continue  # 직접 디자인한 카드는 빌더 결과와 같을 필요가 없다(카피 잠금으로 대신 검사)
                    self.assertEqual(build(item, data), committed, f"{content_id}/{lang}/card_{item['page']:02d}")


class SpacingTests(unittest.TestCase):
    @unittest.skipUnless(copy_lint.kiwi(), "kiwipiepy 없음")
    def test_flags_only_standard_spacing_errors(self):
        found = copy_lint.spacing_suggestions("처분을 받을수 있습니다.\n의견을 제출 할 수 있습니다.\n검토해야 할 서류와 영업정지 기준을 봅니다.")
        self.assertIn(("받을수", "받을 수"), found)
        self.assertIn(("제출 할", "제출할"), found)
        flat = " ".join(b for _, b in found)
        self.assertNotIn("해야할", flat)  # kiwi의 비표준 붙임 제안은 버린다
        self.assertNotIn("영업 정지", flat)  # 합성 명사 분리도 버린다


class LegaleseTests(unittest.TestCase):
    def test_flags_document_tone_on_cards(self):
        report = copy_lint.Report()
        copy_lint.style_cards({"cards": [card(2, "concept", "기간은 이렇게 정합니다", takeaway="개별기준 기간은 2분의 1 범위에서 줄일 수 있습니다.")]}, "ko", report)
        self.assertIn("legalese", [f["rule"] for f in report.findings])


if __name__ == "__main__":
    unittest.main()
