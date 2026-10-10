# External review authorization boundary — plan
intent: 2026-10-10-redesign-external-review-authorization@ccb9b897
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/skills/independent-advisor/SKILL.md` and `loom-code/skills/closing-review/SKILL.md` require the owner to interpret the full request before recording the final choice.
- Reverse: `loom-code/scripts/external_review.py::_consent_valid` checks source, selected executor, review root, disclosures, model and effort before any CLI call.
- Error: `loom-code/scripts/external_review.py::_authorization_valid` parses correction and refusal phrases; local synthetic trials found false blocks and false allows.
- Data: `loom-code/tests/test_external_review.py::consent` builds the source record used for discovery and execution tests.
- Boundary: `loom-code/tests/test_excluded_executor_no_egress.py` currently asserts semantic refusals at the runner instead of final-choice records from the owner.

## Task DAG

### Wave 1

**W1-01 Keep authorization semantics with the owner**  after: none  acceptance: 1, 2, 3
- Files: `loom-code/scripts/external_review.py`, `loom-code/tests/test_external_review.py`, `loom-code/tests/test_excluded_executor_no_egress.py`, `loom-code/skills/external-review/SKILL.md`
- Test: A1 positive: owner-cancellation-probe; negative: stale-record-no-spawn; A2 positive: owner-correction-probe; boundary: corrected-direct-request; A3 positive: complete-record; negative: omitted-or-mismatched-record-no-spawn.
- Risk: agent-decided — narrow semantic coverage in `test_external_review.py` and `test_excluded_executor_no_egress.py` to owner-record boundaries; correct the external-review skill's stale parser claim.

## Simplicity check
- Delete runner phrase parsing without adding a new parser or consent field — taken

## Questions asked
- none

## Risks
1. The runner cannot prove whether the owner's final-choice interpretation matches a conversation; its quote remains audit evidence. The owner instructions already require full-request interpretation; retain synthetic behavior evidence without claiming real-world infallibility.
2. Local-only authorization excludes sending repository code or review packets to any outside CLI and excludes publication.
