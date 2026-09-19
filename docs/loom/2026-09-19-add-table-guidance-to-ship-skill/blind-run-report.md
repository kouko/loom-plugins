# Blind-Run Report: 2026-09-19-add-table-guidance-to-ship-skill

## Acceptance Verification

### 1. The ship skill SKILL.md contains a line advising to use Markdown tables for list/comparison info and to avoid inline ①②③ lists.
- **How I tried it**: Read `/Users/kouko/.herdr/worktrees/loom-plugins/pr-merge-fix/loom-code/skills/ship/SKILL.md` and searched for the guidance regarding Markdown tables and inline lists.
- **What happened**: Found the exact sentence on line 65: "Use a Markdown table for any list‑type or comparison‑type information (options, trade‑offs, decision summaries, etc.). Do not use inline ①②③ lists or plain‑text enumerations."
- **Evidence**: Line 65 of `loom-code/skills/ship/SKILL.md`.
- **Verdict**: works

### 2. The line is placed after the publication template block in the Prepare publication text section.
- **How I tried it**: Verified the position of the guidance line relative to the PR body template block in the "2. Prepare publication text" section of `SKILL.md`.
- **What happened**: The publication template block ends on line 64. The guidance line is on line 65, immediately following the block.
- **Evidence**: `loom-code/skills/ship/SKILL.md` lines 37-65.
- **Verdict**: works

### 3. The guidance is visible when running the ship skill (e.g., via loom_code:ship) or reading the SKILL.md.
- **How I tried it**: Confirmed the guidance exists in the `SKILL.md` file, which is the source of truth for the `ship` skill's behavior and instructions.
- **What happened**: The text is present and legible in the skill definition.
- **Evidence**: `loom-code/skills/ship/SKILL.md` line 65.
- **Verdict**: works

## Data Impact
This change modifies the internal instructions of the `ship` skill. It does not affect any existing user data or previous publications.

## Decisions on Behalf of User
No decisions were made on behalf of the user.

## Open Questions
None.

## Artifact Compliance
| Artifact | Rule | Result | Evidence |
|---|---|---|---|
| Plan | English | works | /Users/kouko/.herdr/worktrees/loom-plugins/pr-merge-fix/docs/loom/2026-09-19-add-table-guidance-to-ship-skill/plan.md |
| Spec | N/A | works | Not required (needs-design: no) |
| Reviewer Findings | Conventional Comments | works | N/A |
| Evidence | English | works | `loom-code/skills/ship/SKILL.md` |
| Test Docstrings | `test_<unit>_<state>_<expected>` | works | N/A |
| Test Names | `test_<unit>_<state>_<expected>` | works | N/A |
| Commit Messages | Conventional Commits | works | `0ee798da` |
