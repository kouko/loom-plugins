# Step policy boundaries — spec
intent: 2026-09-26-step-policy-boundaries@66edfd0d
pre-build-review: not-required — bounded repair of existing internal policies; no new public interface, security boundary or data migration

## Requirements
REQ-1 — Plain-language skips remain usable
  A user instruction may skip its named step without expert-mode confirmation. Other steps remain required, and missing verification is disclosed honestly. → Acceptance #1
REQ-2 — Omitted artifacts have no mandatory consumers
  Skipping spec or plan removes its creation, intake and downstream dependency, while confirmed intent and non-skipped checks remain. → Acceptance #2
REQ-3 — Early progress is not a complete scope
  Before implementation, a docs-only committed delta does not waive planning steps. Late verification may simplify based on committed functional content; explicit selections take precedence. → Acceptance #3
REQ-4 — Architecture takes effect on ratification
  Draft architecture is advisory; only ratified rules constrain planning, review and activated guards. Existing ratified rules continue during redesign. → Acceptance #4
REQ-5 — Reuse the existing policy surfaces
  Use existing records and carriers; add no ledger, phase store, confirmation ceremony or speculative abstraction. → Acceptance #5

## Design decision
- user-decided — repair all three issues together, preserve direct natural-language skips, and avoid additional complexity.
- agent-decided — remove early automatic simplification rather than predict future scope or record a new lifecycle state.
- agent-decided — keep explicit selection and natural-language instructions distinct; an instruction is not a fabricated confirmation record or a verification verdict.
- agent-decided — use intent as the fallback carrier when plan is omitted; task handoffs retain enough scope without creating a substitute plan artifact.
- agent-decided — stage proposed architecture guards for validation without enabling them in the normal suite until ratification; retain existing ratified guards during redesign.

## Alternatives considered
- New phase flags, workflow database, or predictive scope classifier: unnecessary state and duplicate policy.
- Remove step skipping: contradicts the user's required capability.
- Disable all late simplification: larger behavior change than needed.

## Current state evidence
- Forward: loom-code/skills/build/SKILL.md §1 requires a plan check even after skipping plan.
- Reverse: loom-code/scripts/loom_checker/command_handlers/intake.py cmd_intake does not consult skipped spec.
- Error: loom-code/scripts/loom_checker/command_handlers/plan.py cmd_plan exits 2 when the omitted file is absent.
- Data: loom-code/scripts/loom_checker/selection.py effective_selection uses committed-delta automatic skips at every entry.
- Boundary: loom-design/skills/architecture-design/SKILL.md promises unratified documents never block, while write-plan and review lenses use existence.

## UI flows
N/A — internal repair; no new user command, confirmation step or product UI.
