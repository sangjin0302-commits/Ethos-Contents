"""Offline regression tests for scoped writing/design adapters and source pins."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("writing_design_sources", ROOT / "scripts/check_writing_design_sources.py")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)
NAMES = ("ethos-editorial", "ethos-design-reference", "ethos-art-direction")


class SourceValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = json.loads((ROOT / CHECK.LOCK).read_text(encoding="utf-8"))
        (self.root / "vendor/writing-design").mkdir(parents=True)
        (self.root / ".gitmodules").write_text((ROOT / ".gitmodules").read_text(encoding="utf-8"), encoding="utf-8")
        self.save()
        self.git("init", "-q")
        for source in self.data["sources"]:
            self.git("update-index", "--add", "--cacheinfo", f"160000,{source['commit']},{source['path']}")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True, text=True)

    def save(self):
        (self.root / CHECK.LOCK).write_text(json.dumps(self.data), encoding="utf-8")

    def test_pins_pass_without_optional_checkouts(self):
        self.assertEqual(CHECK.validate(self.root), [])

    def test_strict_mode_reports_uninitialized_sources(self):
        errors = CHECK.validate(self.root, require_checkout=True)
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("Uninitialized" in item for item in errors))

    def test_gitlink_drift_is_rejected(self):
        source = self.data["sources"][0]
        self.git("update-index", "--cacheinfo", f"160000,{'1' * 40},{source['path']}")
        self.assertTrue(any("Gitlink differs" in item for item in CHECK.validate(self.root)))

    def test_url_configuration_drift_is_rejected(self):
        path = self.root / ".gitmodules"
        path.write_text(path.read_text(encoding="utf-8").replace("uxKero/anydesign.git", "other/anydesign.git"), encoding="utf-8")
        self.assertTrue(any("configuration differs" in item for item in CHECK.validate(self.root)))

    def test_moving_branch_is_not_a_pin(self):
        self.data["sources"][0]["commit"] = "main"
        self.save()
        with self.assertRaises(ValueError):
            CHECK.validate(self.root)

    def test_traversal_is_rejected(self):
        self.data["sources"][0]["path"] = "../outside"
        self.save()
        with self.assertRaises(ValueError):
            CHECK.validate(self.root)

    def test_external_transport_is_rejected(self):
        self.data["sources"][0]["url"] = "ssh://example.invalid/repo"
        self.save()
        with self.assertRaises(ValueError):
            CHECK.validate(self.root)

    def test_duplicate_sources_are_rejected(self):
        self.data["sources"].append(copy.deepcopy(self.data["sources"][0]))
        self.save()
        with self.assertRaises(ValueError):
            CHECK.validate(self.root)

    def test_unsupported_schema_is_rejected(self):
        self.data["schema_version"] = 99
        self.save()
        with self.assertRaises(ValueError):
            CHECK.validate(self.root)


    def initialized_source(self):
        source = copy.deepcopy(self.data["sources"][0])
        checkout = self.root / source["path"]
        checkout.mkdir(parents=True)
        CHECK.git(checkout, "init", "-q")
        CHECK.git(checkout, "config", "core.autocrlf", "true")
        (checkout / "SKILL.md").write_bytes(b"# Fixture\n\nA source skill.\n")
        (checkout / "LICENSE").write_bytes(b"MIT\n")
        CHECK.git(checkout, "add", "SKILL.md", "LICENSE")
        CHECK.git(checkout, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Fixture")
        source["commit"] = CHECK.git(checkout, "rev-parse", "HEAD")
        source["entries"] = [{"path": "SKILL.md", "blob_sha": CHECK.git(checkout, "rev-parse", "HEAD:SKILL.md")}]
        self.data["sources"] = [source]
        self.save()
        self.git("update-index", "--cacheinfo", f"160000,{source['commit']},{source['path']}")
        return checkout

    def test_initialized_checkout_passes(self):
        self.initialized_source()
        self.assertEqual(CHECK.validate(self.root, require_checkout=True), [])

    def test_windows_crlf_is_not_a_content_change(self):
        checkout = self.initialized_source()
        path = checkout / "SKILL.md"
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(CHECK.validate(self.root, require_checkout=True), [])

    def test_actual_worktree_edit_is_rejected(self):
        checkout = self.initialized_source()
        (checkout / "SKILL.md").write_bytes(b"Changed content\r\n")
        self.assertTrue(any("skill bytes changed" in item for item in CHECK.validate(self.root, True)))

    def test_initialized_revision_drift_is_rejected(self):
        checkout = self.initialized_source()
        (checkout / "LICENSE").write_bytes(b"MIT\nFixture revision.\n")
        CHECK.git(checkout, "add", "LICENSE")
        CHECK.git(checkout, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Another revision")
        self.assertTrue(any("Checkout differs" in item for item in CHECK.validate(self.root, True)))

    def test_missing_upstream_license_is_reported(self):
        checkout = self.initialized_source()
        (checkout / "LICENSE").unlink()
        self.assertTrue(any("Missing upstream license" in item for item in CHECK.validate(self.root, True)))


class AdapterIntegrationTests(unittest.TestCase):
    def test_repository_pins(self):
        self.assertEqual(CHECK.validate(ROOT), [])

    def test_canonical_skills_and_claude_bridges(self):
        for name in NAMES:
            with self.subTest(name=name):
                path = f".agents/skills/{name}/SKILL.md"
                canonical = (ROOT / path).read_text(encoding="utf-8")
                bridge = (ROOT / f".claude/skills/{name}/SKILL.md").read_text(encoding="utf-8")
                self.assertIn(f"name: {name}", canonical)
                self.assertIn("Source Lock", canonical)
                self.assertIn("docs/writing-design-skills.md", canonical)
                self.assertIn(path, bridge)

    def test_agent_routes_and_active_manifest(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        for name in NAMES:
            self.assertIn(name, agents)
            self.assertIn(name, claude)
        self.assertIn("docs/writing-design-skills.md", (ROOT / "MANIFEST.md").read_text(encoding="utf-8"))

    def test_catalog_scope_is_explicit(self):
        data = json.loads((ROOT / CHECK.LOCK).read_text(encoding="utf-8"))
        decisions = data["catalog_decisions"]
        self.assertEqual(decisions["content-research-writer"], "method-adapted-no-source-copy")
        self.assertEqual(decisions["canvas-design"], "cover-only-method-adapted-no-source-copy")
        self.assertTrue(decisions["brand-guidelines"].startswith("excluded-"))
        self.assertTrue(decisions["theme-factory"].startswith("excluded-"))
        guide = (ROOT / "docs/writing-design-skills.md").read_text(encoding="utf-8")
        for name in decisions:
            self.assertIn(name, guide)


if __name__ == "__main__":
    unittest.main()
