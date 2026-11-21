---
name: a-green-package-suite-does-not-cover-ci-only-check-steps
description: CI can run check scripts as their own workflow steps outside the package suite, so a green local package suite does not mean CI will pass; before pushing, run every check step the CI workflow runs, not only the package suite
type: gotcha
sources:
  - resource: deleted entry verified-gate-pytest-suite-misses-skill-structure-word-cap (2026-08-15 plain-relay-contract arc; a SKILL.md word-cap breach passed the local pytest suite and failed CI's separate skill-structure job) — removed in commit 5a8008d89, recoverable from b2c4bdc8e
  - resource: deleted entry leading-at-req-comment-trips-living-spec-checker (PR #590, 2026-07-19; a leading `@req` comment passed the package pytest and failed CI's check-living-spec-index.py step) — removed in commit 5a8008d89, recoverable from b2c4bdc8e
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
- `loom-code/scripts/check_doc_citations.py` (fed the changed docs
  through `xargs`)
- `python3 loom-code/scripts/check-skill-crossrefs.py`

The two earlier cases were a skill-structure word cap and a living-spec
`@req` tag check. Both checks have since been removed, but the gap they
showed stays: each was a CI step the local suite did not run.

**Why:** "the package suite passed" and "CI will pass" are checked by
different commands. A verify step that covers only the suite misses
exactly the checks CI runs next, and the push wastes a CI round.

**How to apply:** before pushing, read the `run:` lines of the CI
workflows under `.github/workflows/` and run each check step that is
not the package suite, with the same arguments. The list above is a
snapshot; the workflow files are the source.
