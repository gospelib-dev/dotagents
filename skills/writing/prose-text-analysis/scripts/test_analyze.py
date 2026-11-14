#!/usr/bin/env python3
"""Regression tests: the avoid list is found from the analyzed file's repo (or the cwd).

Run: python3 test_analyze.py
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / 'analyze.py'
AVOID_LIST = """# Avoid List

## ⛔ FORBIDDEN — Find an Alternative

### Forbidden Filter Words

| Filter  | Problem  | Fix              |
| ------- | -------- | ---------------- |
| He felt | Telling  | Show the feeling |
"""
PROSE = "The hull groaned around them.\n\nHe felt the deck tilt beneath his boots.\n"


def make_repo(root: Path, avoid_rel='guides/avoid-list.md') -> Path:
    (root / 'AGENTS.md').write_text('# Agents\n', encoding='utf-8')
    (root / avoid_rel).parent.mkdir(parents=True)
    (root / avoid_rel).write_text(AVOID_LIST, encoding='utf-8')
    # A leaf AGENTS.md without an avoid list must not stop the search.
    (root / 'novel' / 'chapters').mkdir(parents=True)
    (root / 'novel' / 'AGENTS.md').write_text('# Leaf\n', encoding='utf-8')
    chapter = root / 'novel' / 'chapters' / 'chapter-01.md'
    chapter.write_text(PROSE, encoding='utf-8')
    return chapter


def run(args, cwd):
    out = subprocess.run([sys.executable, str(SCRIPT), *args, '--json'], cwd=cwd,
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)['avoid_list'], out.stderr


def forbidden_phrases(avoid):
    return [f['phrase'] for f in avoid['forbidden']]


class AvoidListDiscovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'repo'
        self.elsewhere = self.root / 'elsewhere'
        self.repo.mkdir()
        self.elsewhere.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_found_from_analyzed_file_path(self):
        chapter = make_repo(self.repo)
        avoid, _ = run([str(chapter)], cwd=self.elsewhere)
        self.assertIn('he felt', forbidden_phrases(avoid), avoid)

    def test_found_from_cwd_when_file_is_outside_repo(self):
        make_repo(self.repo)
        loose = self.elsewhere / 'chapter-03.md'
        loose.write_text(PROSE, encoding='utf-8')
        avoid, _ = run([str(loose)], cwd=self.repo / 'novel')
        self.assertIn('he felt', forbidden_phrases(avoid), avoid)

    def test_text_mode_uses_cwd(self):
        make_repo(self.repo)
        avoid, _ = run(['--text', PROSE], cwd=self.repo)
        self.assertIn('he felt', forbidden_phrases(avoid), avoid)

    def test_legacy_github_resources_path(self):
        chapter = make_repo(self.repo, avoid_rel='.github/resources/avoid-list.md')
        avoid, _ = run([str(chapter)], cwd=self.elsewhere)
        self.assertIn('he felt', forbidden_phrases(avoid), avoid)

    def test_missing_list_warns_instead_of_silently_empty(self):
        loose = self.elsewhere / 'chapter.md'
        loose.write_text(PROSE, encoding='utf-8')
        avoid, err = run([str(loose)], cwd=self.elsewhere)
        self.assertEqual(forbidden_phrases(avoid), [], avoid)
        self.assertIn('avoid-list checks skipped', err)


if __name__ == '__main__':
    unittest.main()
