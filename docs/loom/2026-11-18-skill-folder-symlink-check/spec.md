# Skill-folder check also rejects symlinks — spec
intent: 2026-11-18-skill-folder-symlink-check@5c8c698
pre-build-review: not-required — single root test file, reversible test-only behavior, no security/privacy, irreversible-data, public-contract, or architecture ambiguity

## Requirements
REQ-1 — Reject any symlink in skill scope
  WHEN the complete package suite runs and a path at `<plugin>`, `<plugin>/skills`, or anywhere beneath is a symlink (to a folder or to a single file), the check shall fail and name that path, whether the link is untracked, staged, or committed → Acceptance #1 (carried detail: all symlinks in scope are blocked, including symlinks to a single file — a fresh clone cannot tell what a link pointed at, so scope cannot depend on the target; user accepted 2026-11-18)
REQ-2 — Fresh clones fail on committed symlinks
  WHEN the check runs in a clone that contains only committed content, a committed symlink at any of those places shall fail with the path named → Acceptance #2
REQ-3 — Out-of-scope symlinks pass
  WHEN a symlink exists outside the plugin scope (for example under `tests/` or `docs/`), the check shall not fail the suite → Acceptance #3
REQ-4 — Clean repository stays green
  WHEN the repository has no symlinks in scope, the complete package suite shall still pass → Acceptance #4

## Design decision
- Detect symlinks from git's own path list and fail them in the same `assert_skill_folders_flat` step that fails nested folders and gitlinks, reusing the existing `HOLDS_SKILL_CONTENT` scope (tests/test_skill_folder_flatness.py:50). agent-decided: one check, one message, one docstring.
- Block all symlinks in scope, targets unjudged, because a fresh clone cannot resolve a link's target (a dangling link is indistinguishable from a folder link). user-decided: user accepted the all-symlinks scope 2026-11-18 ("ＯＫ go" to "全部擋掉，就不用判斷目標").
- Update the opening docstring's exception list (remove the "symlink passes" bullet) and drop the folder-link fixture from the passing test at tests/test_skill_folder_flatness.py:228. agent-decided: the docstring is the single statement of exceptions; a fixture asserting the old behavior contradicts the rule.

## Alternatives considered
- Block only symlinks to folders — rejected: a fresh clone cannot tell a folder link from a dangling file link, so the scope cannot depend on the target.
- Walk the disk for symlinks outside git's list — rejected: would flag ignored local products (the 13 `node_modules` links) and bypass the git-list-based design.
- Extend the loom-workflow write-time hook instead — rejected: out of scope per intent (PR #167 excluded hook changes).

## Current state evidence
- Forward: tests/test_skill_folder_flatness.py:91 — `is_folder = full_path.is_dir() and not full_path.is_symlink()` makes a symlink a plain file entry; no violation is ever reported for a link.
- Reverse: tests/test_skill_folder_flatness.py:18 — the docstring bullet "A symlink to a folder: git stores only the link." documents the pass.
- Error: tests/test_skill_folder_flatness.py:75 — `git_listed_paths` lists tracked and untracked non-ignored paths from `git ls-files`; a tracked symlink (mode 120000) is listed in every clone, so the fresh-clone case falls out of the same source.
- Data: `git ls-files -s` shows 0 tracked symlinks at main b7ff56cdf (2026-11-18); 13 working-tree links exist, all under `loom-workflow/tests/mermaid/node_modules/.bin/` (ignored, outside scope).
- Boundary: tests/test_skill_folder_flatness.py:228 — the fixture `os.symlink("..", .../folder-link)` asserts a folder symlink passes today; scope to reuse is `HOLDS_SKILL_CONTENT` (tests/test_skill_folder_flatness.py:50): plugin root, `skills`, and beneath.

## UI flows
N/A — engineering change to a test check; no user-facing surface.
