# Fix the flow diagram's flush body line and string-body splitting
originator: kouko
kind: engineering
needs-design: no — bug fixes inside loom-visualization's generator scripts and their tests; the diagram box shape is already defined by the generators and their tests, and no new surface or argument is added
evidence: [docs/loom/2026-10-21-diagram-arch-edge-cases/acceptance-test-report.md]
status: confirmed 2026-10-22
publication: automatic — authorized 2026-10-22 by kouko

## Problem
Two defects on trunk fc6e9bfc hit anyone (person or agent) drawing a flow or layered-architecture diagram with loom-visualization, and PR #104 left one test note:

| Defect | Reproduced on trunk fc6e9bfc | Consequence |
|---|---|---|
| Flow body line flush against the right border | `render_flow(['Build\nxxxxxxxxxxx', 'Ship'], width=10)` draws `│ xxxxxxxxxxx│`; without `width` the same node draws `│ xxxxxxxxxxx │` | The box loses its right padding only when a width is given |
| Description given as one string is split one character per line | `render_flow([{'title': 'Build', 'body': 'handles requests'}, 'Ship'])` draws 16 one-character lines; `render_arch([{'name': {'title': 'Web', 'body': 'handles requests'}, 'components': []}])` does the same and also draws `│ Web│` with no gap | The diagram is unreadable and nothing reports the mistake |

PR #104's code-lens reviewer noted that `test_trunk_pins_cover_all_six_generators` checks the pin data rather than what the generators draw.

## Proposed outcome
A flow node keeps its right padding when a width is given, a description written as one string draws as its lines, and the pin-coverage test fails when a generator's drawn output changes. Every other input draws exactly as on trunk.

## Acceptance
1. A flow node whose description line is wider than the width budget keeps one space between the text and the right border, as it does with no width given.
2. A flow or architecture node whose description is a single string draws that string as its description lines, one line per line of the string, instead of one character per line.
3. For every one of the six generators, inputs that hit neither defect draw byte-identically to trunk fc6e9bfc, including error messages.
4. The test guarding that all six generators are pinned fails when a generator's drawn output changes.
5. The full package suite passes.

## Constraints
- Only the flow and architecture generators, their tests and the loom-workflow release files change; the six generators' trunk pins from PR #104 stay as they are.
- user-decided — a single-string description is drawn as its lines rather than rejected (option A, 2026-10-22).

## Out of scope
- The layered-architecture body line touching the right border (accepted at PR #104's decision point ③).
- An empty title with no description lines still erroring `Body cannot be empty`.
- Recognizing a version-only `.json` change as low risk (the unfinished part of #35; its own change later).

## Open questions
- none
