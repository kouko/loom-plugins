# Add table usage guidance to ship skill — plan
intent: 2026-09-19-add-table-guidance-to-ship-skill@0ee798da
charter: 1.0

## Current State Evidence
- Forward: loom-code/skills/ship/SKILL.md:65 — added Markdown table guidance line after publication template.
- Reverse: none — no existing guidance to replace.
- Error: none — change only adds guidance, no behavioral change.
- Data: 0ee798da — baseline commit on PR-Merge-fix branch before this change.
- Boundary: none — modification confined to ship skill SKILL.md.

## Task DAG

### Wave 1

**W1-01 Add table usage guidance to ship skill**  after: none  acceptance: 1
- Files: loom-code/skills/ship/SKILL.md
- Test: A1 positive: verify SKILL.md contains the new table guidance line; negative: line missing or incorrect.
- Risk: agent-decided — guidance is internal to ship skill, no external skill dependency introduced.

## Questions asked
① — intent — Confirmed that the ship skill should self-contain table usage guidance without relying on ascii-graph-toolkit.

## Risks
1. None — change only adds documentation guidance, no functional impact.