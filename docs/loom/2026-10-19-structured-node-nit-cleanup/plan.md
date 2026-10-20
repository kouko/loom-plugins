# Clean up the eight structured-node reviewer nits — plan
intent: 2026-10-19-structured-node-nit-cleanup@9ed422fa
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/skills/loom-visualization/scripts/width.py:150` plan label `# W1-01:`; `:197` docstring says "(4 copies)"; `center`, `render_structured_node` are the shared entries.
- Reverse: `gen_flow.py:29`, `gen_arch.py:28`, `gen_tree.py:30` import `EMPTY_BODY`; `gen_flow.py:128`, `gen_arch.py:204`, `gen_tree.py:57` raise it on dict-path empty bodies.
- Error: `test_ascii_width.py:296` only restates the `EMPTY_BODY` literal; dict-path empty-body text has no generator-entry test (`test_ascii_generators.py:1031` covers only the string path).
- Data: `width.py:173`, `:213`, `:225` clamp negative padding to zero; Python `" " * n` is already `""` for n < 0, so all three are output-neutral.
- Boundary: `test_ascii_width.py:382` checks only border characters of wrapped body lines, not wrapped widths; `gen_arch.py:29-32` holds four consecutive blank lines.

## Task DAG

**W1-01 Tighten helper code and its tests**  after: none  acceptance: 1, 2, 3, 4
- Files: loom-workflow/skills/loom-visualization/scripts/width.py, loom-workflow/skills/loom-visualization/scripts/gen_arch.py, loom-workflow/tests/loom-visualization/test_ascii_width.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A1 positive: existing-generator-suite-unchanged; boundary: over-wide-label-renders-unpadded. A2 positive: wrapped-body-exact-lines; negative: wrap-width-mutation-left-to-adversary. A3 positive: dict-empty-body-error-at-entries; negative: delete-test_EMPTY_BODY_constant. A4 positive: no-plan-labels; boundary: over-wide-label-renders-unpadded.
- Risk: Removes `test_EMPTY_BODY_constant` from `test_ascii_width.py`; coverage preserved by new flow/arch/tree dict-path entry tests asserting the literal text. Clamp removal relies on negative string repetition (agent-decided).

**W2-01 Correct release records and bump loom-workflow to 5.11.2**  after: W1-01  acceptance: 5, 6
- Files: loom-workflow/CHANGELOG.md, docs/loom/2026-09-28-structured-node-shared-helper/evidence/golden-diff.md, docs/loom/intent/2026-09-28-structured-node-shared-helper.md, loom-workflow/**/plugin.json, loom-workflow/package.json, loom-workflow/README*.md, README.md, loom-workflow/tests/scripts/test_release_metadata.py
- Test: A5 positive: changelog-lists-every-5.11.1-helper; boundary: merged-records-only-appended. A6 positive: package-suite-passes; negative: existing-pin-tests-fail-on-unsynced-5.11.2.
- Risk: Merged-change records get appended notes only (intent Constraint); old intent note in its own language. Patch bump; CURRENT pin rewrite and 5.11.2 CHANGELOG entry are deliverables (agent-decided).

## Simplicity check
- Merge release-note fix and version bump into one task, since both edit CHANGELOG.md — taken
- Reuse the existing CURRENT pin tests as the version negative check instead of a new test — taken
- One over-wide boundary test for center and both node pads, wrap-width mutation left to the adversary, A3 negative recorded as a deletion — taken

## Questions asked
① — what — 這樣對嗎？

## Risks
1. A concurrent PR may bump loom-workflow first; re-check the trunk version at sync-trunk and re-bump to the next free patch if taken.
