# Planning intake observation pilot — spec
intent: 2026-11-11-intake-observation-pilot@241362a4
pre-build-review: not-required — final scope clarifies consumption of the existing text command; no new CLI/public format, check, authority or confirmation behavior remains

## Requirements
REQ-1 — Faithful observation
  WHEN a planning intake observation is requested, the checker shall return the existing checks' outcome and blocking reasons, without reporting missing required information as a pass → Acceptance #1
REQ-2 — Read-only scope
  The observation shall leave the inspected project unchanged and shall neither advance a station nor waive confirmation, review or acceptance requirements → Acceptance #2
REQ-3 — Measured comparison
  The pilot evaluation shall retain a reproducible comparison of agent consumption, outcome fidelity and extra cost, explicitly reporting when efficiency improvement is unproved → Acceptance #3
REQ-4 — Input evidence boundaries
  The research shall distinguish independently observed inputs from semantic assertions and demonstrate missing or conflicting input behavior without representing synthetic results as real-task accuracy → Acceptance #4

## Design decision
- agent-decided — REQ-1: retain the existing `intake <station> <change-id>` text interface and its checks, ordering, early exit and diagnostics unchanged. Write-plan consumes its exit code and `BLOCK <rule>: <reason>` lines before and after planning. Informational text is not a readiness result; no additional parser, format or policy engine is introduced.
- agent-decided — REQ-1: exit 0 means all applicable intake checks passed; exit 1 reports returned rule failures. Confirmation failure ends the path before later checks; later returned failures complete the applicable path without passing. Exit 2 is an invocation/observation error. Malformed output, nonzero exits and crashes never establish readiness. A crash alone does not establish how many checks ran.
- agent-decided — REQ-2: recompute each invocation; output is a scoped snapshot, not permission to proceed after inputs change. Preserve blockers and rerun after relevant changes; recover and rerun errors. Existing downstream checks remain in place. No network calls or writes are added; existing read-only Git observations remain.
- agent-decided — REQ-3: adopt guidance-only after the retained comparison found equivalent guided-text and JSON decisions on all six cases, with JSON adding 445 packet bytes. The structured candidate is withdrawn under the original no-benefit alternative. Preserve original answers, failures, costs and historical replay; no model-token, call-count, monetary or total-latency saving is established. The single sequential consumer and synthetic cases limit generalization.
- agent-decided — REQ-4: retain the input provenance research and its seven-case reproduction; independently review its claims. Do not alter dispatch classification or unknown handling in this change.
- user-decided — The user confirmed the bounded intent and automatic non-forced branch/Ready PR publication on 2026-11-11; merge remains separate.

Outcome mapping (REQ-1, agent-decided):

| Observation | Existing output | Applicable checks completed? | Exit | Consumer response |
|---|---|---|---|---|
| All applicable intake checks pass | No returned BLOCK failures | yes | 0 | Intake passed only; retain downstream requirements |
| Confirmation rule fails before later checks | BLOCK intake.confirmed with reason | no | 1 | Preserve blocker; rerun after recovery/input changes |
| Later applicable rules return failures | BLOCK lines with rule/reason | yes | 1 | Preserve blockers; completion is not passing |
| Invalid invocation or unavailable observation | Error diagnostic | not established as complete | 2 | Recover and rerun; readiness unavailable |
| Crash or malformed observation | Partial/unusable output | unknown | nonzero for crashes; otherwise distrust malformed output | Recover and rerun; never infer passing |

An ordinary confirmation-rule failure is a valid blocking observation, even when its reason concerns indeterminate delivery history. Error diagnostics do not establish an underlying rule failure or completed path. These are interpretations of existing text/exit behavior, not new emitted fields. Without enough evidence, preserve uncertainty instead of guessing. Intake completion never means all Loom gates passed.

## Alternatives considered
- Whole-workflow scheduler: rejected because the pilot concerns an existing observation and requires no automatic action.
- Classification model: rejected because these outcomes are already computed by code.
- Parsing rendered `BLOCK` text into another rule system: rejected; the station reads existing results without recreating policy.
- Structured JSON: tried through `7da5d59`, then rejected because the witnessed comparison demonstrated no benefit over guidance-only. Its successful functional checks and duplicate-option repair remain historical evidence, not a reason to retain the interface.
- Guidance-only: selected under the original adoption condition; final changes clarify interpretation without extending the checker.

## Current state evidence
- Forward: `loom-code/scripts/loom_checker/command_handlers/intake.py::cmd_intake` evaluates confirmed intent before remaining applicable checks.
- Reverse: `loom-code/skills/write-plan/SKILL.md::The intake check` invokes the command before and after plan creation.
- Error: `loom-code/scripts/loom_checker/helpers.py::report` writes BLOCK lines; `UsageError` distinguishes unusable invocation.
- Data: `loom-code/scripts/loom_checker/command_handlers/intake.py::failures` holds `(rule, reason)` pairs; interface observations also write text to stdout.
- Boundary: `loom-code/references/dispatch-profile.md::Task classification` remains unchanged; intake does not replace review, acceptance or publication checks.

## UI flows
N/A — final scope is station guidance for the unchanged internal text command; no new public format or UI flow remains.
