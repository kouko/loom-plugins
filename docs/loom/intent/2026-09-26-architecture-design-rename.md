originator: kouko
kind: engineering
needs-design: no — rename of skill identifiers within the existing skill surface; no new workflow or multi-state behavior
status: confirmed 2026-09-26

# Rename architecture skill to architecture-design

## Problem
The `architecture` skill is currently named `architecture`, which is inconsistent with the naming convention of other design-type skills. The user wants it renamed to `architecture-design` for clarity and consistency.

## Proposed outcome
Rename the skill tool from `architecture` to `architecture-design` across all relevant files, with no alias period (user confirmed no backward compatibility needed). The ARCHITECTURE.md document filename stays unchanged (it's a project artifact, not a skill name). The `architecture-conformance` review dimension stays unchanged. All tests, documentation, plugin registrations, and manifest entries are updated to use the new name.

## Acceptance
1. The skill is discoverable as `architecture-design`, with no `architecture` alias.
2. The contract manifest names `architecture-design` as the tool producing `ARCHITECTURE.md`.
3. Plugin registrations and marketplace descriptions consistently identify `architecture-design`.
4. The write-plan and using-loom-design routes direct agents to `architecture-design`.
5. Renamed skill, validator, and test locations resolve correctly, and regression tests reject stale operative references.
6. Current documentation describes and links the renamed tool; historical records retain their original evidence. Release metadata is synchronized for every changed plugin.
7. Intent validation, the complete package suite, independent review, and the PR checks pass.

## Constraints
- ARCHITECTURE.md document filename stays unchanged
- `architecture-conformance` review dimension name stays unchanged
- No backward-compatible alias period (user explicitly said no)
- Package tests must pass after changes

## Out of scope
- Changing the ARCHITECTURE.md document filename
- Changing the `architecture-conformance` review dimension name
- Adding backward compatibility aliases
- Changing validator behavior or the architecture design workflow

## Open questions
- none
