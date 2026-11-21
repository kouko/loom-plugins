---
name: skill-folder-structure-hook-reads-stdin-json-and-ignores-argv
description: A PostToolUse hook script that reads its target from the stdin JSON event ignores a path passed as argv — invoking it as `bash hook.sh <path>` from CI or a reviewer shell exits 0 without checking anything, so a "structure check" step built on the hook is a silent no-op; use the package-suite test `tests/test_skill_folder_flatness.py` for any non-hook invocation
type: gotcha
sources:
  - resource: think-orbit Part 1 close-out (2026-08-18) — `.claude/hooks/validate-skill-folder-structure.sh <path>` was used as a CI step and as reviewer GREEN evidence for six tasks; a probe with a nested subfolder returned exit 0, revealing the hook reads `tool_input.file_path` from stdin (`INPUT=$(cat)`) and never looks at `$1`; `tsundoku-ci.yml` carries the same dead step
---

`.claude/hooks/validate-skill-folder-structure.sh` is written as a
PostToolUse hook: it reads the tool event as JSON on stdin and extracts
`tool_input.file_path`. Called with a path argument and no stdin, it
finds no skill root and exits 0 — the invocation looks like a check but
checks nothing. It is not registered in this repo today (AGENTS.md
"Skill Structure"), so it does not even run on edits; enforcement is the
package-suite test `tests/test_skill_folder_flatness.py`.

**Why:** the CI convention of "run the same hook the editor runs" is
attractive, but the hook's input contract is the harness event, not
argv. Every downstream reader (workflow YAML, reviewer instructions,
memory recipes) that says `bash hook.sh <path>` inherits a green light
that never turned red.

**How to apply:** for CI or manual verification of skill folder
structure, run `python3 -m pytest tests/test_skill_folder_flatness.py`
(flat skill folders); do not cite the hook as evidence. When a check step
exits 0 suspiciously fast, feed it a known-bad input once before trusting
it — the same probe habit as
[[a-mechanical-check-can-go-green-by-skipping]].

**Name the tool, not the category** (folded in from the retired entry
two-skill-structure-checkers-disagree-name-which-one, 2026-08-19). When
two tools enforce one convention with different rules, "the
skill-structure checker forbids X" is two claims, and a reviewer can
honestly disprove it by running the other tool. Historical (2026-08-19):
the hook rejected nested directories only, while the since-removed
`scripts/check-skill-structure.py` also rejected loose top-level files
(`CHK-SKL-012`); a docs review was lost when a reviewer ran the hook
against a sentence true only of the python checker. Today the hook and
`tests/test_skill_folder_flatness.py` both reject only nesting (the test
also rejects symlinks and gitlinks), and nothing rejects a loose file at
a skill root. So in prose, name the tool (and rule id, if it has one) and
say what it does not check.
