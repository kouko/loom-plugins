# Clean up the eight reviewer nits left by the structured-node helper change
originator: kouko
kind: engineering
needs-design: no — internal cleanup of loom-visualization helper code, its tests and release notes; every generator's output and error text stay byte-identical
evidence: [docs/loom/2026-09-28-structured-node-shared-helper/attestation.json]
status: confirmed 2026-10-20
publication: automatic — authorized 2026-10-20 by kouko

## Problem
PR #63 (shared structured-node helpers in `loom-workflow/skills/loom-visualization/scripts/width.py`) merged with eight non-blocking reviewer nits left in its Follow-ups. Until they are cleaned up, a future contributor meets a test that only restates a constant's text, a wrapping test that would not notice a wrong wrap width, plan-only labels and unreachable branches in the helper file, a run of blank lines in `gen_arch.py`, a 5.11.1 release note that omits one added helper, and change records (golden-diff evidence, Acceptance 1 wording) that no longer match what finally shipped.

## Proposed outcome
All eight nits are resolved in one small change, with every diagram generator behaving exactly as it does on trunk today.

## Acceptance
1. For the same inputs, including every error path, all five diagram generators produce output and error messages byte-identical to trunk before this change.
2. The structured-node wrapping test fails when the width the body wraps at is changed.
3. No test only restates a constant's literal text; the empty-body error text stays checked through the generator entry points.
4. The shared helper file carries no plan-only labels and no branch that cannot change its output, and `gen_arch.py` has no run of more than two blank lines.
5. The 5.11.1 release note lists every helper that release added, and the structured-node change's golden-diff evidence and intent each carry a note pointing to what finally shipped (the 26-sample comparison; five sites derived from one error constant), with their original text kept.
6. The complete package suite passes.

## Constraints
- No user-visible behaviour change in any generator (byte-identical output and error text).
- Records of the already-merged structured-node change are only appended to, never rewritten.

## Out of scope
- The `.json` version-only low-risk reviewer-floor rule left from PR #35.
- Any other loom-visualization behaviour or helper refactor.

## Open questions
- none
