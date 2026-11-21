# Remove stale references to deleted tools and renamed skills
originator: kouko
kind: engineering
needs-design: no — documentation and skill wording only; no interface surface (cli/api/commands/tsx/templates) is touched
evidence: []
status: confirmed 2026-11-22 (renewed 2026-11-22: Acceptance narrowed after NON_CONVERGENT outside review)
publication: automatic — authorized 2026-11-21 by kouko
intent_confirmed_sha: 354a4f6

## Problem
A repo-wide terminology audit (2026-11-20) found living documents that point at things that no longer exist. About eight committed memory entries cite deleted scripts and CI workflows as current tools; a runtime reference in loom-visualization and three loom-workflow docs name skills that were moved or renamed; memory bodies still name retired plugins and dead doc paths; and KICKOFF-DEFAULTS.md cites a dbt-wiki directory the repo no longer has. An agent following these is sent to a missing file or a missing skill.

## Proposed outcome
The documents this change edits, and the existing claims it invalidates, name only tools, skills, paths and plugins that exist today, or mark a historical mention as history. Unrelated pre-existing stale content elsewhere in the repo is recorded in PR Follow-ups, not fixed here.

## Acceptance
1. Current references and instructions work. Verify every new or substantively changed current claim in the final diff from `b2c4bdc8e`, all 11 Round 3 locations recorded against `dc38b83e2`, and existing claims this change invalidates, including in unchanged files. Check targets, capabilities and command arguments against their authoritative sources. Label history, placeholders and schema patterns. Record unrelated pre-existing defects in PR Follow-ups.
2. Historical wording is preserved. Compare original proposals, dated incident records, quotations and attributions with `b2c4bdc8e` and preserve their wording. Put clarifications in separate dated notes. Verify that frozen files present at the base are unchanged.
3. Memory remains usable. Run the validator across the whole store. For each edited or deleted entry, cite where each actionable lesson survives or give evidence that it no longer applies. Apply Acceptance 1 to current procedures in added and edited entries and to the named Round 3 memory findings. Label past procedures as historical.
4. The complete package suite passes on the final candidate commit.

## Constraints
- Per-change records (docs/loom/<date>-*/, docs/loom/intent/, docs/loom/research/, docs/skill-dogfood/) and files marked ARCHIVED stay as written.
- Plugins whose files change get a version bump and CHANGELOG entry per the repository's release rule.
- Round 3 outside-review locations, recorded against `dc38b83e2`, that Acceptance 1 and 3 name:
  - loom-workflow/docs/quarterly-audit-runbook.md:101
  - loom-workflow/docs/quarterly-audit-runbook.md:161
  - docs/loom/memory/a-docs-reviewer-dimension-sentence-gates-templates-not-generated-instances.md:3
  - docs/loom/memory/contract-class-review-does-not-reach-generated-artifacts.md:3
  - docs/loom/memory/run-the-push-gate-at-every-checkpoint-not-only-the-intake-gates.md:31
  - docs/loom/memory/reviewer-dispatch-isolated-worktree.md:62
  - docs/loom/memory/same-reviewer-delta-confirmation-dies-at-a-context-compaction.md:67
  - docs/loom/memory/test-must-land-in-the-ci-lane-its-plugin-runs.md:3
  - docs/loom/memory/a-green-package-suite-does-not-cover-ci-only-check-steps.md:35 (also :17)
  - docs/loom/KICKOFF-DEFAULTS.md:8
  - docs/loom/memory/headless-branch-plugin-testing-recipe.md:58

## Out of scope
- Renaming terms inside skills (separate change).
- README translation sync (separate change).

## Open questions
- none
