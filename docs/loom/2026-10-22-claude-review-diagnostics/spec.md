# Claude Code external-review recovery — spec
intent: 2026-10-22-claude-review-diagnostics@13a12c32fb0a868faf87f9519464397f65405e48
pre-build-review: required — failure diagnostics touch private review material and the external-review result contract

## Requirements
REQ-1 — Complete a healthy review
  WHEN an authorized Claude Code review is requested and the CLI completes both stages successfully, Loom shall return the review text with model provenance rather than treating the preflight as the review → Acceptance #1

REQ-2 — Explain a failed review safely
  WHEN the Claude Code review stage fails, Loom shall return a bounded failure category and a useful next diagnostic or recovery action without including the review prompt, review text, or raw CLI output in its public result → Acceptance #2

REQ-3 — Preserve review boundaries
  WHEN any outside review does not complete, Loom shall leave the review verdict absent, enforce the existing authorization scope, and keep the other executor paths working → Acceptance #3

## Design decision
- agent-decided — Classify recognized Claude failures from structured CLI fields and bounded known diagnostics; report only fixed categories and recovery guidance because raw stdout and stderr can contain the review packet.
- agent-decided — Give unrecognized failures safe stage, exit, and output-shape information plus a local diagnostic action; an unknown cause must stay explicitly unknown rather than be guessed.
- agent-decided — Keep the preflight and full review as separate executions and require the full review's output for completion; a successful preflight proves only short-request viability.
- agent-decided — Keep consent, selected model and effort, read-only tool restrictions, and the existing result meaning unchanged; this avoids turning a diagnostic repair into a new review policy.

## Alternatives considered
- Returning the first stderr line or complete Claude JSON would be more detailed but can expose the prompt or private review material.
- Automatically retrying or switching to another provider would obscure the failure and exceed the approved single-review boundary.
- Treating a successful preflight as sufficient would create a false completed-review record.

## Current state evidence
- Forward: `loom-code/scripts/external_review.py:508` runs one preflight and then the full review with the selected CLI profile.
- Reverse: `loom-code/skills/external-review/SKILL.md:118` directs review owners to pass their complete packet to this script and validate returned text separately.
- Error: `loom-code/scripts/external_review.py:413` classifies only a short stderr allowlist, and `:521` converts an unrecognized nonzero exit to `unknown error`.
- Data: `loom-code/scripts/external_review.py:468` returns a JSON result with status, reason, provenance, and review_output; `:475` clears probe output on failure.
- Boundary: `loom-code/skills/external-review/SKILL.md:21` requires scoped consent before dispatch, and `:135` excludes failed legs from completed reviews.

## UI flows
| Case | What the user does | What they see |
|---|---|---|
| No authorized request | Requests an outside review without the required selection or consent | No CLI request is sent; the review remains failed with a consent reason and the user can make an explicit selection. |
| In progress | Starts an authorized Claude Code review | Stage and elapsed-time progress appears while the preflight and full review run. |
| Success | Receives a completed full review | The result includes the actual review text and observed model; the owning review flow can then validate a verdict. |
| Recognized failure | Receives a nonzero result from Claude Code | A safe failure category and next action appear; the result has no review text or verdict. |
| Unrecognized failure | Receives a nonzero result with no recognized cause | The result says the cause is unknown, gives safe stage/exit/output-shape facts and a local diagnostic action, and never prints raw CLI output. |

After a failure, a newly authorized review starts again with a fresh preflight; no failed run is promoted to success or silently retried.
