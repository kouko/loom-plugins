# Fix the layered-architecture diagram's early wrap and empty-name edge cases
originator: kouko
kind: engineering
needs-design: no — bug fixes inside loom-visualization's generator scripts and their tests; the diagram box shape is already defined by the generators and their tests, and no new surface or argument is added
evidence: [docs/loom/2026-10-21-diagram-narrow-width-fixes/acceptance-test-report.md]
status: confirmed 2026-10-21
publication: automatic — authorized 2026-10-21 by kouko

## Problem
Three defects on trunk, left as follow-ups by PR #103, hit anyone (person or agent) drawing a layered-architecture diagram with loom-visualization:

| Defect | Reproduced on trunk 5e850c70 | Consequence |
|---|---|---|
| Body line split one cell early | `render_arch([{'name': {'title': 'API', 'body': ['handles requests']}, 'components': ['auth', 'db']}])` draws `handles` and `requests` on two lines, with or without `width=40`; the same happens for a string name `'API\nhandles requests'` | Any layer whose description line is its widest line is broken across lines for no reason |
| Empty single-line name, no components | `render_arch([{'name': '', 'components': []}])` draws a box whose last row is one cell wider than the rest | The box is misaligned |
| Empty title at a narrow width or with an empty description line | `render_arch([{'name': {'title': '', 'body': ['x']}, 'components': []}])` (also `'\nx'`) raises `ValueError: max_width must be positive`; so do other empty-title layers at width budgets of 1 or less, and an empty title with an empty description line | No diagram is produced |

PR #103's code-lens reviewer also left two test notes: the suite pins the exact trunk output of only two unaffected inputs, and the two hang-guarded render helpers in `test_ascii_generators.py` are near-duplicates.

## Proposed outcome
The layered-architecture generator keeps a description line on one line whenever the width budget allows it, and draws an aligned box for an empty name or an empty title at any width; every other input renders exactly as it does today, and the test suite guards that.

## Acceptance
1. A layered-architecture layer whose description line is its widest line shows that line unbroken, in a box whose borders line up, whenever no width budget forces it narrower.
2. A layer with an empty single-line name and no components draws a box whose borders line up.
3. A layer with an empty title and at least one description line draws a box whose borders line up instead of raising an error, at any width budget.
4. For inputs that hit none of the three defects, every diagram generator's output and error messages are byte-identical to trunk before this change.
5. The package suite pins the exact trunk output of unaffected inputs for every diagram generator, and the hang-guarded rendering in the generator tests goes through one shared helper.
6. The complete package suite passes.

## Constraints
- No change to the generators' arguments or to inputs that hit none of the three defects.

## Out of scope
- The `.json` version-only low-risk reviewer-floor rule left from PR #35.
- The empty-component separator warning from `align.py`.
- Any other loom-visualization behaviour or refactor.

## Open questions
- none
