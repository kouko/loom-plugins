# External review consent follows the final user choice — plan
intent: 2026-10-10-external-review-consent@5c13213
charter: 1.1

## Current State Evidence
- Forward: `loom-code/scripts/external_review.py:84` checks the record before discovery or execution.
- Reverse: `loom-code/tests/test_external_review.py:86` tests refusals, corrections, and direct requests at the runner boundary.
- Error: `loom-code/scripts/external_review.py:69` accepts a quote that excludes the selected executor when it names that executor.
- Data: `loom-code/skills/external-review/SKILL.md:44` records a verbatim quote and target but no explicit interpretation of the final selected executor.
- Boundary: `loom-workflow/skills/independent-advisor/SKILL.md:51` allows a direct named request without a second confirmation.

## Task DAG

**W0-01 Bind outside execution to the user's final selected executor**  acceptance: 1, 2, 3
- Files: `loom-code/scripts/external_review.py`, `loom-code/skills/external-review/SKILL.md`, `loom-code/tests/test_external_review.py`, `loom-workflow/skills/independent-advisor/SKILL.md`, `loom-code/skills/closing-review/SKILL.md`
- Test: A1 positive: excluded-executor-blocked; negative: no-discovery-on-refusal. A2 positive: direct-request-runs; boundary: no-second-choice. A3 positive: selected-executor-bound; negative: ambiguous-scope-blocked.
- Risk: agent-decided — make the owning flow record the final selection and have the runner verify it before egress; consider only a correction marker followed by a selection or cancellation verb, and require that correction to select the dispatched executor explicitly. This keeps ordinary "no need" or "wait for the result" wording from changing the choice. The bounded runner patterns do not replace the owning flow's interpretation of the full request.

**W0-02 Retain the defect-catching exclusion probe in the package suite**  after: W0-01  acceptance: 1, 3
- Files: `docs/loom/2026-10-10-external-review-consent/evidence/probes/test_excluded_executor_no_egress.py`, `loom-code/tests/test_excluded_executor_no_egress.py`
- Test: A1 positive: graduated-probe-green; negative: excluded-executor-no-egress. A3 positive: package-suite-collects; boundary: retained-concern-header.
- Risk: agent-decided — move the proven probe intact with its concern header so every later package suite and finalization run retains the regression case.

## Simplicity check
- none found

## Questions asked
1 — what — 這是你要的下一輪修正範圍嗎？（使用者回答：「對」）

## Risks
1. A free-form quote cannot be interpreted reliably by a deterministic runner; the owning flow must bind the final selected executor and active target before any external step.
2. User authorized local work only; no push, PR, or external coding-agent invocation is part of this change.
