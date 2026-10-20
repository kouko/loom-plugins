# Fix the layered-architecture diagram's early wrap and empty-name edge cases — plan
intent: 2026-10-21-diagram-arch-edge-cases@5f0964d2
charter: 1.1

## Current State Evidence
- Forward: `gen_arch.py:54` `render_arch` sizes one shared interior at `:123`; structured names render through `width.py:197` `render_structured_node`, which wraps body lines at `interior - 1` (`width.py:223`).
- Reverse: `render_structured_node` is shared with `gen_flow.py`, which adds a 2-cell margin and never wraps early; only `gen_arch.py` sizing changes.
- Error: `gen_arch.py:121` applies the body-char floor only to two-cell chars, so empty title plus one-cell body yields interior 1 and `wrap_label` raises at width 0.
- Data: `gen_arch.py:98-101` and `:80` size a body line at bare width, omitting the leading space, so the widest body line wraps; empty name with no components gives interior 0 (`:156-166`).
- Boundary: `test_ascii_generators.py:1125` pins the empty-title error this change removes; `:1067` and `:1134` are near-duplicate hang-guarded helpers.

## Task DAG

**W1-01 Pin unaffected outputs and share the hang-guarded helper**  after: none  acceptance: 4, 5
- Files: loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A4 positive: every-generator-pins-trunk-output; negative: pins-fail-on-changed-output. A5 positive: pins-cover-all-six-generators; negative: one-shared-isolated-render-helper.
- Risk: Pins capture trunk 5e850c70 output on inputs hitting none of the three defects, landing before the sizing change; the merged helper keeps every caller's coverage (agent-decided).

**W1-02 Keep the widest body line whole and draw empty names aligned**  after: W1-01  acceptance: 1, 2, 3
- Files: loom-workflow/skills/loom-visualization/scripts/gen_arch.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A1 positive: arch-dict-widest-body-line-unbroken; boundary: arch-dict-body-wider-than-budget-still-wraps. A2 positive: arch-empty-name-no-components-aligned; boundary: arch-one-cell-name-no-components-unchanged. A3 positive: arch-empty-title-one-cell-body-aligned; boundary: arch-empty-title-one-cell-body-width-1-aligned.
- Risk: Body floor min(widest line+1, budget) for dict names, widest+1 for string names; char floor covers one-cell chars; interior floors at 1 (agent-decided). Rewrites the :1125 error pin.

**W1-03 Render every empty-title layer and graduate the trailing-space probe**  after: W1-02  acceptance: 3, 4
- Files: loom-workflow/skills/loom-visualization/scripts/gen_arch.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py, docs/loom/2026-10-21-diagram-arch-edge-cases/evidence/probes/test_arch_trailing_space_body_trunk_bytes.py
- Test: A3 positive: arch-empty-title-empty-body-line-aligned; boundary: arch-empty-title-narrow-widths-aligned. A4 positive: arch-trailing-space-body-trunk-bytes; negative: graduated-probe-red-before-fix.
- Risk: Structured-name floor gains a 2-cell minimum, reached only by empty-title layers that errored on trunk (user-decided, option A); the probe moves into the suite (agent-decided).

**W2-01 Release loom-workflow 5.12.3**  after: W1-01, W1-02, W1-03  acceptance: 6
- Files: loom-workflow/CHANGELOG.md, loom-workflow/**/plugin.json, loom-workflow/package.json, loom-workflow/README*.md, README.md, loom-workflow/tests/scripts/test_release_metadata.py
- Test: A6 positive: package-suite-passes; negative: existing-pin-tests-fail-on-unsynced-5.12.3.
- Risk: Patch bump (bug fix, no field or rule change); CHANGELOG 5.12.3 entry and CURRENT pin rewrite are deliverables (agent-decided).

## Simplicity check
- Build the trunk-output pins once (W1-01) before the sizing change instead of a second A4 guard inside the sizing task — taken

## Questions asked
① — what — 這樣對嗎？
① — consequence — 你選 A 還是 B？

## Risks
1. A concurrent PR may bump loom-workflow first; check the trunk version before closing review and re-bump to the next free patch if taken.
2. Existing tests that pin early-wrapped arch output are pinning defect-1 output; the implementer updates them and lists each one in the hand-off.
3. A dict body line at least as wide as an explicit width budget still wraps, because the budget forces it narrower (Acceptance 1 wording); a string-name body is not budget-capped today and stays uncapped.
4. user-decided — every empty-title layer with a description line renders at any width (option A, 2026-10-21), rather than a special case keeping trunk's error outside the one-cell shape.
5. A title or name made only of zero-width marks (e.g. U+0301) counts as empty for Acceptance 2 and 3; HEAD renders it aligned where trunk misaligned or errored (agent-decided, shown at decision point ③).
