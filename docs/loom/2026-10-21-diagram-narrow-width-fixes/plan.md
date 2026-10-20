# Fix the layered-architecture diagram's narrow-width hang and title overflow — plan
intent: 2026-10-21-diagram-narrow-width-fixes@22d49a42
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/skills/loom-visualization/scripts/gen_arch.py:54` `render_arch` is the entry; `:93` `get_layer_width` sizes the shared interior; `width.py:61` `wrap_label` is the wrap entry, called only from `width.py:218` `render_structured_node` at `interior - 1`.
- Reverse: `render_structured_node` is shared by `gen_flow.py:116`, `:130` and `gen_arch.py:188`, `:204`; flow adds a 2-cell margin (`gen_flow.py:54`) and shows neither defect.
- Error: `width.py:91-140` — a first character wider than `max_width` leaves `k` 0, so `remaining` never shrinks; `render_arch` reaches it with a two-cell body char at `width=1` (`gen_arch.py:188`, `:204`).
- Data: `gen_arch.py:78-82` sizes a title at bare width, but `width.py:209-211` draws it after one leading space, so the widest title overflows the right border by one cell.
- Boundary: `test_ascii_width.py:263`, `:284` cover `wrap_label` only at widths that fit every character; no arch test has a title wider than its body and components.

## Task DAG

**W1-01 Stop the wrap hang and keep arch boxes aligned**  after: none  acceptance: 1, 2, 3, 4
- Files: loom-workflow/skills/loom-visualization/scripts/width.py, loom-workflow/skills/loom-visualization/scripts/gen_arch.py, loom-workflow/tests/loom-visualization/test_ascii_width.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A1 positive: arch-cjk-body-width-1-aligned; boundary: arch-multiline-string-name-cjk-body-width-1-aligned. A2 positive: wrap-cjk-at-width-1-returns; boundary: wrap-ascii-at-width-1-unchanged. A3 positive: arch-dict-long-title-aligned; boundary: arch-multiline-string-name-long-title-aligned. A4 positive: single-line-string-name-long-title-unchanged; negative: trunk-byte-compare-on-non-defect-inputs.
- Risk: wrap_label takes one char when none fits; floor max(title+1, widest body char+1) only for structured names (dict, or string with newline); single-line names unchanged (agent-decided). Widens test_ascii_width.py coverage.

**W1-02 Close the adversary's two findings and graduate its probes**  after: W1-01  acceptance: 1, 4
- Files: loom-workflow/skills/loom-visualization/scripts/gen_arch.py, loom-workflow/skills/loom-visualization/scripts/gen_flow.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py, docs/loom/2026-10-21-diagram-narrow-width-fixes/evidence/probes/test_arch_non_defect_error_text.py, docs/loom/2026-10-21-diagram-narrow-width-fixes/evidence/probes/test_flow_narrow_cjk_body_alignment.py, loom-workflow/tests/loom-visualization/
- Test: A1 positive: flow-cjk-body-width-0-aligned; boundary: flow-multiline-string-cjk-body-width-0-aligned. A4 positive: arch-empty-title-one-cell-body-keeps-trunk-error; negative: graduated-probes-red-before-fix.
- Risk: Arch char floor applies only to two-cell body chars; flow floors interior at widest body char+1, changing only inputs that hung on trunk (agent-decided).

**W2-01 Release loom-workflow 5.12.2**  after: W1-01  acceptance: 5
- Files: loom-workflow/CHANGELOG.md, loom-workflow/**/plugin.json, loom-workflow/package.json, loom-workflow/README*.md, README.md, loom-workflow/tests/scripts/test_release_metadata.py
- Test: A5 positive: package-suite-passes; negative: existing-pin-tests-fail-on-unsynced-5.12.2.
- Risk: Patch bump (bug fix, no field or rule change); CHANGELOG 5.12.2 entry and CURRENT pin rewrite are deliverables (agent-decided).

## Simplicity check
- Limit the interior floor to structured names so single-line string names stay byte-identical — taken
- Name both structured sizing sites, dict and newline string, in tests and Risk — taken

## Questions asked
① — what — 這樣對嗎？

## Risks
1. A concurrent PR may bump loom-workflow first; check the trunk version before closing review and re-bump to the next free patch if taken.
2. A body line exactly as wide as the interior still wraps one cell early in arch (`T` / `abcdefghij` renders `abcdefghi` + `j`); outside this intent (Acceptance 4 keeps it byte-identical) — listed as a PR follow-up.
