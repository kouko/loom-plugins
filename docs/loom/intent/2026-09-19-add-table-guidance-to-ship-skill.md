---
originator: kouko
kind: engineering
needs-design: no
status: confirmed 2026-09-19
---

## Problem
The ship skill currently lacks explicit guidance on using Markdown tables for list-type or comparison-type information in PR bodies, causing reliance on external ascii-graph-toolkit visualization card for such reminders.

## Proposed outcome
Add a clear instruction in the ship skill to use Markdown tables for any list-type or comparison-type information, making the skill self-contained.

## Acceptance
1. The ship skill SKILL.md contains a line advising to use Markdown tables for list/comparison info and to avoid inline ①②③ lists.
2. The line is placed after the publication template block in the Prepare publication text section.
3. The guidance is visible when running the ship skill (e.g., via loom_code:ship) or reading the SKILL.md.

## Constraints
- Do not introduce a dependency on another skill; keep guidance internal to ship.
- Preserve existing Mermaid diagram guideline.
- Follow Loom's PR body heading structure.

## Value case
Improves self-containment of the ship skill and reduces external skill references, simplifying onboarding and maintenance.

## Out of scope
- Changing the Mermaid diagram guideline.
- Modifying other Loom skills or workflows.

## Open questions
- None