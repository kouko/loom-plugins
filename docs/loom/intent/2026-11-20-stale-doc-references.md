# Remove stale references to deleted tools and renamed skills
originator: kouko
kind: engineering
needs-design: no — documentation and skill wording only; no interface surface (cli/api/commands/tsx/templates) is touched
evidence: []
status: confirmed 2026-11-21 (renewed 2026-11-21 after outside review: Acceptance rewritten)
publication: automatic — authorized 2026-11-21 by kouko
intent_confirmed_sha: 2bc09fe

## Problem
A repo-wide terminology audit (2026-11-20) found living documents that point at things that no longer exist. About eight committed memory entries cite deleted scripts and CI workflows as current tools; a runtime reference in loom-visualization and three loom-workflow docs name skills that were moved or renamed; memory bodies still name retired plugins and dead doc paths; and KICKOFF-DEFAULTS.md cites a dbt-wiki directory the repo no longer has. An agent following these is sent to a missing file or a missing skill.

## Proposed outcome
Every living document names only tools, skills, paths and plugins that exist today, or marks a historical mention as history.

## Acceptance
1. Current references resolve. In tracked Markdown outside frozen records, every skill or agent presented as current exists under its documented plugin and can do the stated task. Scripts, workflows, files and directories presented as current are checked one by one in docs/loom/memory/, docs/loom/KICKOFF-DEFAULTS.md, docs/loom/README.md, loom-code/PRODUCT-SPEC.md and loom-workflow/docs/{telemetry-setup,skill-governance,quarterly-audit-runbook}.md; other tracked Markdown is searched for the same retired targets. Links, tables and runnable examples count. Historical mentions, placeholders and schema patterns are labelled as such.
2. Historical wording is preserved. In every edited file, original proposals, dated incident records, quotations and attributions are compared with the pre-change commit and keep their original wording; a current-name clarification goes in a separate dated note. Frozen files (ARCHIVED and per-change records) are verified unchanged against the pre-change tree.
3. Memory remains usable. The memory validator confirms the index matches the entries. For every edited or deleted entry, each actionable lesson is cited where it survives, or evidence shows it no longer applies; a lesson still applies when it addresses a current workflow or a failure mode that can still occur. Procedures presented as current are checked against their authoritative source; past procedures are labelled historical.
4. The complete package suite passes.

## Constraints
- Per-change records (docs/loom/<date>-*/, docs/loom/intent/, docs/loom/research/, docs/skill-dogfood/) and files marked ARCHIVED stay as written.
- Plugins whose files change get a version bump and CHANGELOG entry per the repository's release rule.

## Out of scope
- Renaming terms inside skills (separate change).
- README translation sync (separate change).

## Open questions
- none
