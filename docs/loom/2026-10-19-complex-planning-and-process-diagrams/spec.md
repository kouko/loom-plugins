# Complex planning and process diagrams — spec
intent: 2026-10-19-complex-planning-and-process-diagrams@b143043
pre-build-review: required — new public diagram-routing and template contracts must distinguish parallel prerequisites from conditional branches and work ownership from message order

## Requirements
REQ-1 — Parallel task dependencies
  WHEN an agent depicts an engineering task plan with parallel prerequisites and a join, the visualization guidance shall route it to an example that shows each prerequisite edge, the concurrently available tasks, and the task that waits for all incoming prerequisites → Acceptance #1

REQ-2 — Cross-role work handoffs
  WHEN an agent depicts a process involving work performed by different roles, the visualization guidance shall route it to an example that identifies the owner of each step and the handoff between owners without treating a message exchange as the whole work process → Acceptance #2

REQ-3 — Valid forms and compatibility
  The two new examples shall provide distinguishable table, ASCII, and Mermaid forms whose stated relationships agree, pass the repository's applicable alignment and Mermaid checks, and leave existing shapes and generator input forms usable → Acceptance #3

## Design decision
- agent-decided — Add one task-dependency DAG template and one cross-role workflow template to the existing shape list because the current linear, branch, and actor-sequence templates answer different questions; do not rewrite those templates.
- agent-decided — In the dependency example, direct each arrow from a prerequisite to the task it enables; a join means every incoming prerequisite is required, not a conditional choice. State this distinction in the template's usage and mistakes sections.
- agent-decided — In the cross-role example, make each work step's owner explicit and label owner changes as handoffs; the existing actor-sequence template remains for ordered messages rather than work ownership.
- agent-decided — Keep the established table, ASCII, and Mermaid template structure. Hand-author and verify compact ASCII examples as the existing branch and state templates do; add no generator unless their forms cannot express the confirmed outcomes.
- agent-decided — Retain the standalone-title rule and existing generator schema. A new template and routing row change the skill's published guidance, so synchronize the loom-workflow minor release metadata before final review.

## Alternatives considered
- Expand the linear-steps template alone — rejected because one fixed sequence cannot show tasks that are concurrently available and later join.
- Treat the actor-sequence diagram as the cross-role process template — rejected because its messages do not assign ownership of each work step.
- Add a generic graph generator now — rejected because these two worked examples do not require a new input contract or diagram engine; the existing manual-example pattern can be checked directly.
- Include UI wireframes in this change — rejected because screen position has a different reading and rendering contract, and the user asked to do it after these templates.

## Current state evidence
- Forward: `loom-workflow/skills/loom-visualization/SKILL.md:62-74` selects among eleven shapes, with no task-dependency or cross-role workflow row.
- Reverse: `loom-workflow/tests/loom-visualization/test_templates.py:32-44` inventories every template, and `loom-workflow/skills/loom-visualization/SKILL.md:76-80` instructs agents to read the selected one.
- Error: `loom-workflow/skills/loom-visualization/templates/02-linear-steps.md:5-9` only covers a fixed order, while `templates/06-actor-sequence.md:5-8` only covers messages ordered in time.
- Data: `loom-workflow/tests/loom-visualization/test_templates.py:29-30,115-123` expects each template to carry table, ASCII, and Mermaid sections; `loom-workflow/skills/loom-visualization/scripts/generate.py:33-65` exposes the current generator shapes.
- Boundary: `loom-workflow/skills/loom-visualization/references/node-structure.md:26-42` defines standalone node titles; `docs/loom/intent/2026-10-19-complex-planning-and-process-diagrams.md:23-27` excludes wireframes and interactive editors.

## UI flows
N/A — this change adds diagram-authoring guidance and examples, with no product screen or command operation.
