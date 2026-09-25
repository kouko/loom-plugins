originator: kouko
kind: engineering
needs-design: no — rename of internal skill identifiers; slash command name is registered via plugin.json and no new CLI surface is introduced
status: confirmed — 2026-09-26

# Rename architecture skill to architecture-design

## Problem
The `architecture` skill is currently named `architecture`, which is inconsistent with the naming convention of other design-type skills. The user wants it renamed to `architecture-design` for clarity and consistency.

## Proposed outcome
Rename the skill tool from `architecture` to `architecture-design` across all relevant files, with no alias period (user confirmed no backward compatibility needed). The ARCHITECTURE.md document filename stays unchanged (it's a project artifact, not a skill name). The `architecture-conformance` review dimension stays unchanged. All tests, documentation, plugin registrations, and manifest entries are updated to use the new name.

## Acceptance
1. **Skill name**: `loom-design/skills/architecture/SKILL.md` has `name: architecture-design` instead of `name: architecture`
2. **Manifest**: `loom-code/contract/manifest.yaml` has `name: architecture-design` instead of `name: architecture` (both entries)
3. **Plugin registrations**: All 4 plugin.json files (loom-design, .claude-plugin, .codex-plugin, marketplace) reference `architecture-design` instead of `architecture`
4. **write-plan Step 5**: `loom-code/skills/write-plan/SKILL.md` references `loom-design:architecture-design` instead of `loom-design:architecture`
5. **Tests**: All test files in `loom-design/tests/architecture/` are moved to `loom-design/tests/architecture-design/` with updated references
4. **Documentation**: All README/CHANGELOG files reference `architecture-design` where they previously referenced `architecture`
5. **Verification**: After changes, `python3 loom-code/scripts/loom_checker.py intent docs/loom/intent/2026-09-26-architecture-design-rename.md` exits 0

## Constraints
- ARCHITECTURE.md document filename stays unchanged
- `architecture-conformance` review dimension name stays unchanged
- No backward-compatible alias period (user explicitly said no)
- Changes happen across 34+ files in multiple directories
- Package tests must pass after changes

## Out of scope
- Changing the ARCHITECTURE.md document filename
- Changing the `architecture-conformance` review dimension name
- Adding backward compatibility aliases
- Renaming `loom-design/scripts/architecture/` (it's a scripts directory, not a skill directory)

## Open questions
- none