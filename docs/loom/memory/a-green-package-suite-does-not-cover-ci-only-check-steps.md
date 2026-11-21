---
name: a-green-package-suite-does-not-cover-ci-only-check-steps
description: CI can run check scripts as their own workflow steps outside the package suite, so a green local package suite does not mean CI will pass; before pushing, run every check step the CI workflow runs, not only the package suite
type: gotcha
sources:
  - resource: deleted entry verified-gate-pytest-suite-misses-skill-structure-word-cap (2026-08-15 plain-relay-contract arc; a SKILL.md word-cap breach passed the local pytest suite and failed CI's separate skill-structure job) — removed in commit 5a8008d89, recoverable from b2c4bdc8e
  - resource: deleted entry leading-at-req-comment-trips-living-spec-checker (PR #590, 2026-07-19; a leading `@req` comment passed the package pytest and failed CI's check-living-spec-index.py step) — removed in commit 5a8008d89, recoverable from b2c4bdc8e
  - resource: deleted entry ci-skill-structure-scan-gap-obsidian (2026-07-10; CI's skill-structure job scanned only some plugins, so a SKILL.md word-cap breach elsewhere merged silently) — removed in this branch, recoverable from b2c4bdc8e
  - resource: 2026-11-20-stale-doc-references adversary probe test_deleted_memory_lesson_survives.py (the two deletions dropped this shared lesson)
---

`scripts/run_package_tests.py` collects pytest files and `test-*.sh`
shell tests. CI also runs check scripts as their own steps, which the
package suite never calls. A branch can therefore be green locally and
red in CI.

As of 2026-11-21, `.github/workflows/loom-code-ci.yml` runs these
CI-only checks:

- `python3 scripts/check_plugin_boundaries.py <plugin>` (loom-code,
  loom-design, loom-workflow)
- `python3 loom-code/scripts/check_mechanisms.py --baseline origin/main`
  and `--measure`
- `python3 loom-code/scripts/check_contract_citations.py`
- `check_doc_citations.py`, fed every tracked Markdown file in the
  operative locations (CI step "Check doc citations resolve"):
  `git ls-files '*.md' | grep -E '^(docs/loom/[^/]+\.md|docs/loom/intent/|loom-(code|design|memory|workflow)/(skills|agents|references|contract)/)' | xargs python3 loom-code/scripts/check_doc_citations.py`
- `python3 loom-code/scripts/check-skill-crossrefs.py`

The two earlier cases were a skill-structure word cap and a living-spec
`@req` tag check, each a CI step the local suite did not run. The
living-spec check has since been removed (see the deleted entry
leading-at-req-comment-trips-living-spec-checker).

The size-cap lesson still applies: AGENTS.md sets a SKILL.md body hard cap
of ~6,000 tokens (~4,500 words). As of 2026-11-21 no repo-wide check
enforces it; only two per-skill tests do
(`loom-workflow/tests/loom-memory/test_skill_contract.py` `WORD_HARD_CAP`
and `loom-workflow/tests/scripts/test_independent_advisor_compaction.py`).
For any other SKILL.md, verify by hand with `wc -w <skill>/SKILL.md`
(≤ 4,500). (Historical, 2026-08-15: the cap was then enforced in CI by
`scripts/check-skill-structure.py`'s word count, outside the package
suite, run from `.github/workflows/skill-structure.yml` — see the deleted
entries verified-gate-pytest-suite-misses-skill-structure-word-cap and
ci-skill-structure-scan-gap-obsidian, both recoverable from b2c4bdc8e;
that script and workflow are no longer in the repo.)

**Why:** "the package suite passed" and "CI will pass" are checked by
different commands. A verify step that covers only the suite misses
exactly the checks CI runs next, and the push wastes a CI round.

**How to apply:** before pushing, read the `run:` lines of the CI
workflows under `.github/workflows/` and run each check step that is
not the package suite, with the same arguments. The list above is a
snapshot; the workflow files are the source.
