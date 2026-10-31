"""Smoke checks for the pinned optional claude-blog submodule integration."""

from __future__ import annotations

import configparser
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUBMODULE = "vendor/claude-blog"
UPSTREAM_SHA = "354442348815a7f0327077ad89af2c43cf4b4ab4"
UPSTREAM_URL = "https://github.com/AgriciDaniel/claude-blog.git"


class ClaudeBlogIntegrationTests(unittest.TestCase):
    def test_gitmodules_references_exact_upstream(self) -> None:
        config = configparser.ConfigParser()
        self.assertTrue(config.read(ROOT / ".gitmodules"))
        entry = config['submodule "vendor/claude-blog"']
        self.assertEqual(entry["path"], SUBMODULE)
        self.assertEqual(entry["url"], UPSTREAM_URL)

    def test_gitlink_is_pinned_and_not_vendored_over_files(self) -> None:
        if not (ROOT / ".git").exists() or not shutil.which("git"):
            self.skipTest("Git worktree not available in this source archive")
        result = subprocess.run(
            ["git", "ls-files", "--stage", "--", SUBMODULE],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        parts = result.stdout.split()
        self.assertEqual(parts, ["160000", UPSTREAM_SHA, "0", SUBMODULE])

    def test_ethos_policy_and_local_skill_are_present(self) -> None:
        guide = (ROOT / "docs/claude-blog-integration.md").read_text(encoding="utf-8")
        skill = (ROOT / ".claude/skills/ethos-blog/SKILL.md").read_text(encoding="utf-8")
        claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        for token in (UPSTREAM_SHA, "Source Lock", "git submodule update --init"):
            self.assertIn(token, guide)
        self.assertIn("name: ethos-blog", skill)
        self.assertIn("docs/blog-authoring-spec.md", skill)
        self.assertIn("MANIFEST.md", claude)


if __name__ == "__main__":
    unittest.main()
