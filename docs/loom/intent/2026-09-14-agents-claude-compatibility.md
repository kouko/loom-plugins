# Make repository instructions compatible across agent hosts
originator: kouko
kind: engineering
needs-design: no — this changes repository instruction entrypoints only; it adds no user-facing product behavior
status: confirmed 2026-09-14
publication: automatic — authorized 2026-09-14 by kouko

## Problem
The repository has a full `CLAUDE.md` but no `AGENTS.md`, so Codex and other
agents that discover only `AGENTS.md` can miss the repository contract.

## Proposed outcome
Keep one complete instruction source that both Claude Code and Codex discover,
with no duplicated policy text that can drift.

## Acceptance
1. `AGENTS.md` contains the existing repository instruction contract unchanged.
2. `CLAUDE.md` contains only `@AGENTS.md` and Claude can follow the shared source.
3. The citation-contract test reads the shared source and verifies the wrapper.

## Constraints
- Preserve the existing instruction wording.
- Do not add a second copy of the contract.

## Out of scope
- Changing any repository policy or Loom workflow rule.

## Open questions
- none
