#!/usr/bin/env python3
"""Synthetic migration/advisory checks; --scratch must be outside a source tree."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import reference_updates as updates
import retire_links as links

SCRATCH = None
PIN = "a" * 40
HEAD = "b" * 40
NEXT = "c" * 40
REF = {"name": "example", "repo": "example/reference", "branch": "main", "pin": PIN}


def upstream(count=5, status="ahead", head=HEAD):
    def api(endpoint):
        if "/compare/" in endpoint:
            return {"status": status, "ahead_by": count}
        if "/commits/" in endpoint:
            return {"sha": head}
        return {"default_branch": "main"}
    return api


class ReferenceTests(unittest.TestCase):
    def test_threshold_and_cursor(self):
        notice, cursor = updates.inspect_reference(REF, {}, upstream(4))
        self.assertIsNone(notice)
        self.assertEqual(cursor, {})
        notice, cursor = updates.inspect_reference(REF, cursor, upstream(5))
        self.assertIn("5 additional", notice)
        self.assertEqual(cursor["head"], HEAD)
        self.assertIsNone(updates.inspect_reference(REF, cursor, upstream(99))[0])
        self.assertIsNone(updates.inspect_reference(REF, cursor, upstream(4, head=NEXT))[0])
        self.assertIn("5 additional", updates.inspect_reference(REF, cursor, upstream(5, head=NEXT))[0])

    def test_reviewed_pin_resets_notice_baseline(self):
        _, cursor = updates.inspect_reference(REF, {}, upstream())
        reviewed = dict(REF, pin=HEAD)
        self.assertIsNone(updates.inspect_reference(reviewed, cursor, upstream(head=HEAD))[0])
        calls = []
        def api(endpoint):
            calls.append(endpoint)
            return upstream(4, head=NEXT)(endpoint)
        self.assertIsNone(updates.inspect_reference(reviewed, cursor, api)[0])
        self.assertIn(HEAD + "..." + NEXT, calls[-1])

    def test_divergence_is_reported_once_and_can_recover(self):
        notice, cursor = updates.inspect_reference(REF, {}, upstream(status="diverged"))
        self.assertIn("history", notice)
        self.assertEqual(cursor["head"], PIN)
        self.assertIsNone(updates.inspect_reference(REF, cursor, upstream(status="behind", head=NEXT))[0])
        notice, cursor = updates.inspect_reference(REF, cursor, upstream())
        self.assertIn("additional", notice)
        self.assertNotIn("diverged", cursor)

    def test_default_branch_and_invalid_response(self):
        self.assertIsNotNone(updates.inspect_reference(dict(REF, branch=None), {}, upstream())[0])
        with self.assertRaises(ValueError):
            updates.inspect_reference(REF, {}, upstream(head="not-a-revision"))

    def test_divergence_can_recur_after_small_recovery(self):
        _, cursor = updates.inspect_reference(REF, {}, upstream(status="diverged"))
        _, cursor = updates.inspect_reference(REF, cursor, upstream(count=2))
        self.assertNotIn("diverged", cursor)
        notice, cursor = updates.inspect_reference(REF, cursor, upstream(status="diverged", head=NEXT))
        self.assertIn("history", notice)
        _, cursor = updates.inspect_reference(REF, cursor, upstream(head=PIN))
        self.assertNotIn("diverged", cursor)

    def test_rollback_to_pin_after_notice_is_reported(self):
        _, cursor = updates.inspect_reference(REF, {}, upstream())
        notice, cursor = updates.inspect_reference(REF, cursor, upstream(status="behind", head=PIN))
        self.assertIn("history", notice)
        self.assertEqual(cursor["head"], HEAD)

    def test_outage_preserves_cursor_and_recovers(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            with patch.object(updates, "registered_references", return_value=[REF]):
                updates.check(root, root / "state", upstream())
                def failed(_):
                    raise ValueError("unavailable")
                self.assertEqual(len(updates.check(root, root / "state", failed)), 1)
                self.assertEqual(updates.check(root, root / "state", failed), [])
                saved = json.loads((root / "state/reference-notices.json").read_text())
                self.assertEqual(saved["example"]["head"], HEAD)
                updates.check(root, root / "state", upstream())
                self.assertEqual(len(updates.check(root, root / "state", failed)), 1)

    def test_only_approved_committed_references_are_checked(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            def git(*args):
                return subprocess.check_output(["git", "-C", str(root), *args], text=True)
            (root / ".installation-policy.json").write_text(json.dumps({"example": "reference", "active": "user"}))
            (root / ".publication-policy.json").write_text(json.dumps({"paths": ["example"]}))
            (root / ".gitmodules").write_text('[submodule "example"]\n path = example\n url = https://github.com/example/reference.git\n branch = main\n')
            git("add", ".")
            git("update-index", "--add", "--cacheinfo", "160000," + PIN + ",example")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "Synthetic fixture")
            before = (git("rev-parse", "HEAD"), git("diff", "--raw"), git("ls-tree", "HEAD", "example"))
            self.assertEqual(updates.registered_references(root), [REF])
            self.assertEqual(len(updates.check(root, root / "state", upstream())), 1)
            after = (git("rev-parse", "HEAD"), git("diff", "--raw"), git("ls-tree", "HEAD", "example"))
            self.assertEqual(before, after)
            (root / ".installation-policy.json").write_text('{"example":"reference","example":"user"}')
            with self.assertRaises(ValueError):
                updates.registered_references(root)


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.dot = self.root / "dotfiles"
        self.user = self.root / "user"
        self.project = self.root / "project"
        self.refs = {"reference": "nested"}
        (self.dot / "skills/reference/nested").mkdir(parents=True)
        (self.dot / "AGENTS.md").write_text("synthetic instructions\n")
        (self.dot / "CLAUDE.md").symlink_to("AGENTS.md")
        self.project.mkdir()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        self.make_link(self.project / "AGENTS.md", self.dot / "AGENTS.md")
        self.make_link(self.project / "CLAUDE.md", self.dot / "CLAUDE.md")

    def make_link(self, path, target):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(target)
        return path

    def plan(self, mode="moreh-dev"):
        return links.plan(self.dot, self.user, self.project, mode, self.refs)

    def test_invalid_registry_is_rejected_before_planning(self):
        path = self.dot / "skills/.installation-policy.json"
        for content in ('{"reference":"user","reference":"reference"}', '[]', '{"reference":"unknown"}'):
            path.write_text(content)
            with self.assertRaises(ValueError):
                links.read_scopes(path)

    def test_retirement_and_idempotency(self):
        ref = self.make_link(self.user / ".agents/skills/reference", self.dot / "skills/reference/nested")
        duplicate = self.make_link(self.user / ".codex/AGENTS.md", self.dot / "AGENTS.md")
        links.apply(self.plan())
        self.assertFalse(ref.is_symlink())
        self.assertFalse(duplicate.is_symlink())
        self.assertTrue((self.project / "AGENTS.md").is_symlink())
        self.assertEqual(self.plan(), [])

    def test_overrides_and_tracked_entries_survive(self):
        real = self.user / ".agents/skills/reference"
        real.mkdir(parents=True)
        override = self.make_link(self.user / ".claude/skills/reference", self.root / "other")
        tracked = self.make_link(self.project / ".agents/skills/reference", self.dot / "skills/reference/nested")
        subprocess.run(["git", "-C", str(self.project), "add", "--force", str(tracked)], check=True)
        actions = self.plan()
        links.apply(actions)
        self.assertTrue(real.is_dir())
        self.assertTrue(override.is_symlink())
        self.assertTrue(tracked.is_symlink())
        self.assertEqual({a["status"] for a in actions}, {"preserve override", "preserve tracked path"})

    def test_retained_project_link_must_be_verified(self):
        (self.project / "AGENTS.md").unlink()
        duplicate = self.make_link(self.user / ".codex/AGENTS.md", self.dot / "AGENTS.md")
        links.apply(self.plan())
        self.assertTrue(duplicate.is_symlink())

    def test_host_global_keeps_global_instructions(self):
        duplicate = self.make_link(self.user / ".codex/AGENTS.md", self.dot / "AGENTS.md")
        links.apply(self.plan("host-global"))
        self.assertTrue(duplicate.is_symlink())

    def test_changed_target_is_not_removed(self):
        ref = self.make_link(self.user / ".agents/skills/reference", self.dot / "skills/reference/nested")
        actions = self.plan()
        ref.unlink()
        ref.symlink_to(self.root / "different")
        with self.assertRaises(ValueError):
            links.apply(actions)
        self.assertTrue(ref.is_symlink())

    def test_symlinked_discovery_root_cannot_delete_source(self):
        source = self.make_link(self.dot / ".codex/AGENTS.md", self.dot / "AGENTS.md")
        self.make_link(self.user / ".codex", self.dot / ".codex")
        actions = self.plan()
        links.apply(actions)
        self.assertTrue(source.is_symlink())
        self.assertEqual(actions[0]["status"], "preserve discovery-root override")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, required=True)
    args, remaining = parser.parse_known_args()
    SCRATCH = args.scratch.resolve()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    unittest.main(argv=[__file__, *remaining])
