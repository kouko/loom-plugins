# Fix the layered-architecture diagram's narrow-width hang and title overflow
originator: kouko
kind: engineering
needs-design: no — bug fixes inside loom-visualization's generator scripts; the diagram box shape is already defined by the generators and their tests, and no new surface or argument is added
evidence: [docs/loom/2026-10-19-structured-node-nit-cleanup/acceptance-test-report.md]
status: confirmed 2026-10-21
publication: automatic — authorized 2026-10-21 by kouko

## Problem
Two defects on trunk, both left as follow-ups by PR #100, hit anyone (person or agent) drawing a layered-architecture diagram with loom-visualization:

| Defect | Reproduced on trunk 114ad1ce | Consequence |
|---|---|---|
| Narrow width + CJK body | `render_arch([{'name': {'title': 'A', 'body': ['中']}, 'components': ['']}], width=1)` never returns; `wrap_label('中文', 1)` loops forever | The calling agent hangs until it is killed; no diagram is produced |
| Over-wide layer title | A dict layer title wider than every body line and component row renders one cell past the right border | The box is misaligned, so the diagram looks broken in a monospace terminal |

The flow generator does not show either defect with the same inputs.

## Proposed outcome
The layered-architecture generator always finishes and always draws aligned boxes, whatever the width budget and title length; every other input renders exactly as it does today.

## Acceptance
1. Drawing a layered-architecture diagram whose body holds a two-cell character, at the narrowest width budgets, finishes within a few seconds and produces a box whose borders line up.
2. Wrapping text containing two-cell characters at a one-cell width finishes instead of looping.
3. A layered-architecture diagram whose layer title is wider than everything else in the layer shows the whole title inside a box whose borders line up.
4. For inputs that hit neither defect, every diagram generator's output and error messages are byte-identical to trunk before this change.
5. The complete package suite passes.

## Constraints
- No change to the generators' arguments or to inputs that hit neither defect.

## Out of scope
- The `.json` version-only low-risk reviewer-floor rule left from PR #35.
- Any other loom-visualization behaviour or refactor.

## Open questions
- none
