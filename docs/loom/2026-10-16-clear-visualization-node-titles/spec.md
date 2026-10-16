# Independent node titles in loom-visualization — spec
intent: 2026-10-16-clear-visualization-node-titles@70ebf14
pre-build-review: not-required — existing skill guidance and examples only; no security, data, external interface, or ambiguous behavior

## Requirements
REQ-1 — Independent title meaning
  WHEN an agent selects text for a diagram node, the skill shall tell it to use a short title that identifies the node's action, role, state, or claim on its own; body text shall add distinct information only when needed, and title-only nodes shall remain valid → Acceptance #1

REQ-2 — Focused examples
  The relevant engineering and process templates shall demonstrate independently understandable titles, retain a body only when it supplies information absent from the title and edges, and preserve the existing diagram shape and purpose → Acceptance #2

REQ-3 — Verified examples and compatibility
  WHEN the updated examples are checked, their ASCII diagrams shall pass the alignment checker, their Mermaid blocks shall pass the repository parser, and the generator input and output contract shall remain unchanged → Acceptance #3

## Design decision
- agent-decided — Add the semantic title/body rule to `references/node-structure.md`, the existing single home for node wording, and keep `SKILL.md`'s pointer to it; duplicating the rule in each template would create drift.
- agent-decided — Revise only examples that obscure the title/body distinction, especially a command-only title and body text that repeats visible diagram content; keep the existing 11 shapes and generator schema intact.
- agent-decided — A title names a meaningful action, role, state, or claim according to its diagram type. A body may state evidence, conditions, or outputs only if they are not already conveyed by that title, an edge, or an adjacent cell.
- agent-decided — Preserve ASCII and Mermaid's diagram-specific capabilities: state names and decision diamonds can stay title-only, and the tree form keeps its unboxed continuation convention.

## Alternatives considered
- Require every node to carry a body — rejected because it would reintroduce the padding problem that the existing node contract explicitly avoids.
- Add a new dependency DAG or UI wireframe shape — rejected from this change because those need their own routing and rendering contracts; the user ordered them after title work.
- Rewrite every template example — rejected because five templates do not have the relevant boxed node structure and several existing titles already communicate their role.

## Current state evidence
- Forward: `loom-workflow/skills/loom-visualization/SKILL.md:134-135` routes node wording to the existing reference.
- Reverse: `loom-workflow/skills/loom-visualization/templates/02-linear-steps.md:28-29` gives the flow generator a structured `pytest` node, and `templates/03-branching-decision.md:28-34` places branch answers in a node body.
- Error: `loom-workflow/skills/loom-visualization/references/node-structure.md:26-29` rejects an empty separator but does not state what a title must convey by itself.
- Data: `loom-workflow/skills/loom-visualization/scripts/gen_flow.py:44-54` accepts a plain string or a `title`/`body` object; the intended edit needs no new input form.
- Boundary: `loom-design/skills/write-spec/references/ui-flows.md:72-77` already assigns screen wireframes to ASCII, outside this change; `loom-workflow/skills/loom-visualization/references/node-structure.md:36-53` limits structured-node scope by diagram form.

## UI flows
N/A — internal diagram-authoring guidance and examples change, with no product interface operation.
