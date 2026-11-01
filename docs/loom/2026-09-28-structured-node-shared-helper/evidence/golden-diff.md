# Golden output comparison — before vs after refactor

Ten samples covering all six generators and the structured/CJK/plain label
classes, rendered once from the branch base (946e06d) and once from the
refactored tree. `diff -r before after` is empty.

Samples: flow-structured, flow-plain, flow-multi, arch-cjk, arch-structured,
tree-structured, tree-cjk, seq, bar, table.

All outputs byte-identical; align.py reports `✓ no drift` on the box
generators (flow/arch).

Note (2026-10-20): the final comparison after the trunk sync used 26 samples, including every error path; see docs/loom/2026-09-28-structured-node-shared-helper/acceptance-test-report.md.
