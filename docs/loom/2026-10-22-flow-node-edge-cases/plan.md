# Fix the flow diagram's flush body line and string-body splitting — plan
intent: 2026-10-22-flow-node-edge-cases@2dd66470
charter: 1.1

## Current State Evidence
- Forward: `gen_flow.py:55` sizes a structured step at `min(natural body, budget)`, interior `+2` at `:95`; `width.py:197` `render_structured_node` wraps body at `interior - 1` (`width.py:223`).
- Reverse: `render_structured_node` is shared with `gen_arch.py:216,232`, whose flush body line was accepted in PR #104; only flow sizing changes for the flush defect.
- Error: a dict `body` given as `str` is iterated per character at `gen_flow.py:78` and `gen_arch.py:90,105,125`, then wrapped one character per line.
- Data: body wider than the budget wraps at budget+1 cells, so a wrapped line can fill the interior with no right pad (`width=10`, 11-cell body).
- Boundary: `test_ascii_generators.py:1347` asserts on `_TRUNK_PINS` keys only; `split_lines('')` returns `['']` (`width.py:47`), unlike trunk's empty `''` body.

## Task DAG

**W1-01 Fold the pin-coverage check into the drawn-output pin test**  after: none  acceptance: 4
- Files: loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A4 positive: one-test-draws-every-pin-and-covers-six-generators; negative: merged-test-red-on-altered-pin.
- Risk: Merges `test_trunk_pins_cover_all_six_generators` into the parametrized pin test (`:1341-1348`), keeping its six-generator assertion; widens coverage from keys to drawn output (agent-decided).

**W1-02 Draw a single-string description as its lines**  after: W1-01  acceptance: 2, 3
- Files: loom-workflow/skills/loom-visualization/scripts/gen_flow.py, loom-workflow/skills/loom-visualization/scripts/gen_arch.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A2 positive: flow-and-arch-string-body-draws-lines; boundary: empty-string-body-keeps-trunk-error. A3 positive: existing-trunk-pins-pass; negative: string-with-newlines-matches-list-body.
- Risk: Normalize a non-empty `str` body with `split_lines` at each generator entry; an empty `''` body keeps trunk's `Body cannot be empty` (user-decided option A; normalization agent-decided).

**W1-03 Keep the flow body line's right padding under a width**  after: W1-02  acceptance: 1, 3
- Files: loom-workflow/skills/loom-visualization/scripts/gen_flow.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A1 positive: flow-width-10-long-unbroken-body-keeps-right-pad; boundary: flow-two-cell-body-narrow-width-keeps-pad. A3 positive: new-pin-flow-width-given-body-fits; boundary: flow-empty-title-empty-body-line-unchanged.
- Risk: gen_flow re-wraps at interior-2 only a line that would fill the interior; wrapping all at interior-2 moved breaks for 20,669/200k non-flush fuzz inputs; char floor rises one; arch unchanged (agent-decided).

**W2-01 Release loom-workflow 5.12.4**  after: W1-01, W1-02, W1-03  acceptance: 5
- Files: loom-workflow/CHANGELOG.md, loom-workflow/**/plugin.json, loom-workflow/package.json, loom-workflow/README*.md, README.md, loom-workflow/tests/scripts/test_release_metadata.py
- Test: A5 positive: package-suite-passes; negative: existing-pin-tests-fail-on-unsynced-5.12.4.
- Risk: Patch bump (bug fix, no field or rule change); CHANGELOG 5.12.4 entry and CURRENT pin rewrite are deliverables (agent-decided).

## Simplicity check
- Merge the pin-coverage test into the parametrized pin test instead of a second drawing pass — taken
- Cite existing trunk pins as A3 evidence instead of new per-task A3 cases; add one pin for flow with a width and a fitting body — taken
- Pre-wrap flow body at interior-2 instead of widening the box by one cell, which left long unbroken bodies flush (reviewer note; Build narrowed it to flush lines) — taken

## Questions asked
① — what — 這樣對嗎？
① — consequence — 說明文字寫成字串時要選 A 還是 B？

## Risks
1. A concurrent PR may bump loom-workflow first; check the trunk version before closing review and re-bump to the next free patch if taken.
2. user-decided — a single-string description is drawn as its lines rather than rejected (option A, 2026-10-22), so an agent's string body renders instead of erroring.
3. A string body is split with str.splitlines, not split_lines, so a control character draws exactly as the list form and as trunk does; the adversary showed the stricter split broke Acceptance 2 and 3 (agent-decided).
4. Pre-wrapping at interior-2 reaches width 0 when the interior is 2 (empty title, empty body line); that case must keep trunk output rather than raise (agent-decided).
