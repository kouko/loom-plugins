# Recap state quick orientation — spec
intent: 2026-10-16-recap-state-quick-orientation@a6f0784f
pre-build-review: not-required — reversible skill prose with no security, data migration, or public API change

## Requirements
REQ-1 — Re-establish purpose and position
  WHEN the user requests an in-session recap after a long conversation, the skill shall lead with the conversation-grounded original purpose and current position, show a proposed next step only when the purpose is grounded, and label unavailable facts unknown → Acceptance #1.
REQ-2 — Recover the path to the present
  WHEN significant decisions or completed work explain the current position, the recap shall show those decisions, completed work, and remaining gap without padding a short session → Acceptance #2.
REQ-3 — Present scannable sections and relationships
  WHEN recap content warrants sections, tables, or topology, the recap shall use distinct headings, visible spacing, a short situation sentence before each table, and only information-bearing tables or diagrams → Acceptance #3.
REQ-4 — Preserve evidence and uncertainty
  WHEN user wording affects subsequent behavior, the recap shall quote it exactly and separate confirmed facts, assumptions, and unknowns → Acceptance #4.
REQ-5 — Pause at alignment
  WHEN the recap ends, the skill shall ask only for the purpose if unknown, or a directed next-step question if grounded, and stop until the user responds → Acceptance #5.
REQ-6 — Remain in-session
  WHEN the skill runs, it shall answer only in the current conversation without writing a recap file or replacing handoff or built-in recap → Acceptance #6.

## Design decision
- agent-decided — Keep one runtime schema in the reference bundle and make SKILL.md a short routing contract, avoiding duplicated section rules.
- user-decided — Use an ASCII frame around each section heading, with `■ ` before its text; one fullwidth-space-only line separates sections. The confirmed preview supplied the wording and spacing.
- user-decided — Put a short situation sentence before a table. Use diagrams only when they clarify meaningful rationale, evidence, sequence, dependency, branch, or merge relationships, never a flat status list; route render choice and ASCII alignment through `loom-visualization`.
- agent-decided — Retain the seven-block lineage as historical context but replace its L3 six-section obligations with a variable-length orientation-first schema.

## Alternatives considered
- Keep six mandatory sections and add the new visual rules — rejected because it preserves filler and makes the recap harder to scan.
- Draw a DAG for every recap — rejected because flat status snapshots have no topology to clarify.
- Use the separate ascii-graph skill directly — rejected because loom-visualization already supplies client checks, generators, and alignment verification.

## Current state evidence
- Forward: `loom-workflow/skills/recap-state/SKILL.md` "following this order" mandates six sections.
- Reverse: `loom-workflow/skills/recap-state/references/seven-block-schema.md` "L3 user-visible template" repeats the six-section contract.
- Error: `loom-workflow/skills/recap-state/SKILL.md` "Give 3–5 bullets" can pad a short conversation.
- Data: `loom-workflow/tests/recap-state/test_seven_block_schema.py` `test_l3_contract_defines_goal_grounded_natural_output` pins the old template.
- Boundary: `loom-workflow/skills/recap-state/SKILL.md` "Chat only" and "Wait" preserve in-session scope and the final pause.

## UI flows
- User requests a recap after a long session → sees the grounded original purpose or an explicit unknown, current position, concise history, completed and pending work; if purpose is unknown, the final question asks only for it and waits; if grounded, the recap proposes a next step, asks for alignment, and waits.
- User requests a short recap → sees only relevant sections without filler.
- Recap includes a table → sees a short situation sentence before the table.
- Recap contains a real dependency or branch → sees a diagram only when it clarifies that relationship; `loom-visualization` chooses the rendered form.
