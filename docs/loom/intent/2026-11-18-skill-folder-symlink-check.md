# Skill-folder check also rejects symlinks
originator: kouko
kind: engineering
needs-design: no — test-only change to the root flatness check; no interface surface (cli/api/commands/tsx/templates) is touched
status: confirmed 2026-11-18
publication: automatic — authorized 2026-11-18 by kouko
intent_confirmed_sha: 5c8c698

## Problem
The skill-folder flatness check restored in PR #167 misses symlinks: a path at `<plugin>`, `<plugin>/skills`, or anywhere beneath that is a symlink passes the check — uncommitted, committed, and in a fresh clone. A folder symlink whose target holds nested subfolders lets the flat rule be bypassed while nested content stays readable through the link.

## Proposed outcome
The package-suite flatness check fails on any symlink at `<plugin>`, `<plugin>/skills`, or anywhere beneath, naming the path, regardless of commit state and in a fresh clone. Paths outside that scope are unaffected.

## Acceptance
1. A symlink (to a folder or to a file) created at `<plugin>`, `<plugin>/skills`, or beneath makes the complete package suite fail and name that path, whether untracked, staged, or committed; removing it restores a passing suite.
2. In a fresh clone containing only committed content, a committed symlink at any of those places fails the check with the path named.
3. A symlink outside the plugin scope (for example under `tests/` or `docs/`) does not fail the suite.
4. On the repository as it stands today (no tracked symlinks), the complete package suite still passes after this change.

## Constraints
- All symlinks in scope are blocked, including symlinks to a single file: a fresh clone cannot tell what a link pointed at, so scope cannot depend on the target (user accepted 2026-11-18).
- The check's plugin scope stays defined by `marketplace.json` as in the existing check.
- No plugin content changes and no plugin version bump; the change lives at the repository root.

## Out of scope
- The loom-workflow write-time hook (its false positives and misses stay as excluded in PR #167).
- Stale-reference cleanup left as PR #167 follow-ups.
- Any change to existing gitlink or ignore-rule behavior of the check.

## Open questions
- none
