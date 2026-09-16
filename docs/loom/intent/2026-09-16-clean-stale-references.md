# Clean stale references
originator: kouko
kind: engineering
needs-design: no — mechanical cleanup of documentation references
status: confirmed 2026-09-16
publication: automatic — authorized 2026-09-16 by kouko

## Problem
Documentation and skill references in the repository are stale, pointing to files or sections that no longer exist (e.g., `codex-tools.md`, obsolete frozen store paths in README). This misleads contributors and agents.

## Proposed outcome
All identified stale references are updated to reflect the current codebase structure and patterns.

## Acceptance
1. `loom-workflow/skills/distill-sessions/references/codex-tools.md` refers to internal dispatch patterns instead of `codex-tools.md`.
2. `docs/loom/README.md` no longer lists `plans/`, `specs/`, `backlog/`, `design/`, `archive/`, or `BACKLOG.md` as active/relevant paths.
3. `loom-design/skills/write-spec/SKILL.md` no longer refers to "ten completeness questions".

## Constraints
- None.

## Out of scope
- Fixing other unrelated documentation errors.
- Refactoring the actual skill logic.

## Open questions
- none
