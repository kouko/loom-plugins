# Remove stale references to deleted tools and renamed skills
originator: kouko
kind: engineering
needs-design: no — documentation and skill wording only; no interface surface (cli/api/commands/tsx/templates) is touched
evidence: []
status: confirmed 2026-11-21
publication: automatic — authorized 2026-11-21 by kouko
intent_confirmed_sha: c18257f

## Problem
A repo-wide terminology audit (2026-11-20) found living documents that point at things that no longer exist. About eight committed memory entries cite deleted scripts and CI workflows as current tools; a runtime reference in loom-visualization and three loom-workflow docs name skills that were moved or renamed; memory bodies still name retired plugins and dead doc paths; and KICKOFF-DEFAULTS.md cites a dbt-wiki directory the repo no longer has. An agent following these is sent to a missing file or a missing skill.

## Proposed outcome
Every living document names only tools, skills, paths and plugins that exist today, or marks a historical mention as history.

## Acceptance
1. No memory entry under docs/loom/memory/ presents a deleted script, workflow or path as a current tool; each such entry is corrected or removed, and the memory index matches the entries left.
2. No living document outside per-change history names a skill or agent that does not exist (requesting-docs-review, skill-refactor and skill-tuning under loom-workflow, complexity-critique, code-reviewer).
3. KICKOFF-DEFAULTS.md and docs/loom/README.md name no directory that does not exist.
4. The complete package suite passes.

## Constraints
- Per-change records (docs/loom/<date>-*/, docs/loom/intent/, docs/loom/research/, docs/skill-dogfood/) and files marked ARCHIVED stay as written.
- Plugins whose files change get a version bump and CHANGELOG entry per the repository's release rule.

## Out of scope
- Renaming terms inside skills (separate change).
- README translation sync (separate change).

## Open questions
- none
