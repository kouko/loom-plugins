# Planning intake observation pilot — spec
intent: 2026-11-11-intake-observation-pilot@241362a4
pre-build-review: required — adds a machine-consumed observation format whose failure semantics must not imply unchecked readiness

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
- agent-decided — REQ-1: add opt-in `--json` rendering to the existing `intake <station> <change-id>` command, retaining the same checks, ordering, early exit and ordinary text behavior. This avoids a duplicate policy implementation. Both existing supported stations use the parser; the pilot consumer is write-plan only.
- agent-decided — REQ-1: emit one JSON object on stdout for recognized JSON invocations. Fields: `station`, `change_id`, `state` (`passed`, `blocked`, `unconfirmed`), `checks_complete`, `failures` (objects with `rule` and `reason`), `diagnostics` (text), and `error` (null or diagnostic string). `checks_complete` means the applicable intake path was fully evaluated, not all Loom gates passed. Confirmation early-exit and operational failures set it false. Exit codes remain 0/1 for pass/block and 2 for invalid invocation or unavailable observations. Preserve ordinary mode diagnostics and errors.
- agent-decided — REQ-1: capture current informational output rather than let it corrupt JSON. Repeated flags, unsafe ids and unsupported stations remain invalid; no new command, global scheduler, result store or rule registry. Unexpected crashes remain nonzero failures and must never be interpreted by the consumer as a pass.
- agent-decided — REQ-2: recompute each invocation; output is a scoped snapshot, not permission to proceed after inputs change. Existing downstream checks remain in place. No network calls or writes are added by observation rendering; existing read-only Git observations remain.
- agent-decided — REQ-3: compare ordinary text, text plus explicit interpretation guidance, and structured output on the same controlled cases. Retain actual agent answers and observed correctness/output sizes; record model-token cost only if available. Do not claim call-count or latency savings from shorter output or one fixture run. Prefer guidance-only if structured output adds no demonstrable consumption/error-handling benefit.
- agent-decided — REQ-4: retain the input provenance research and its seven-case reproduction; independently review its claims. Do not alter dispatch classification or unknown handling in this change.
- user-decided — The user confirmed the bounded intent and automatic non-forced branch/Ready PR publication on 2026-11-11; merge remains separate.

Outcome mapping (REQ-1, agent-decided):

| Observation | state | checks_complete | exit | error |
|---|---|---|---|---|
| All applicable intake checks pass | passed | true | 0 | null |
| Confirmation rule returns a failure before later checks | blocked | false | 1 | null |
| Later applicable rules return failures | blocked | true | 1 | null |
| Invalid invocation or unavailable observation | unconfirmed | false | 2 | diagnostic string |

An ordinary confirmation-rule failure is a valid blocking observation, even when its reason concerns indeterminate delivery history. `unconfirmed` is reserved for an invocation/observation error rather than a returned rule failure. If station or change id cannot be obtained from an invalid invocation, its JSON field is null. A consumer accepts readiness only with valid JSON, exit 0, state passed and checks_complete true; every other result preserves the blocker or requires recovery and rerun.

## Alternatives considered
- Whole-workflow scheduler: rejected because the pilot concerns an existing observation and requires no automatic action.
- Classification model: rejected because these outcomes are already computed by code.
- Parsing rendered `BLOCK` text into another rule system: rejected because the checker already has rule/reason pairs.
- Guidance-only: retained as the cheaper comparison arm; implementation adoption depends on measured consumption benefit rather than predicted savings.

## Current state evidence
- Forward: `loom-code/scripts/loom_checker/command_handlers/intake.py::cmd_intake` evaluates confirmed intent before remaining applicable checks.
- Reverse: `loom-code/skills/write-plan/SKILL.md::The intake check` invokes the command before and after plan creation.
- Error: `loom-code/scripts/loom_checker/helpers.py::report` writes BLOCK lines; `UsageError` distinguishes unusable invocation.
- Data: `loom-code/scripts/loom_checker/command_handlers/intake.py::failures` holds `(rule, reason)` pairs; interface observations also write text to stdout.
- Boundary: `loom-code/references/dispatch-profile.md::Task classification` remains unchanged; intake does not replace review, acceptance or publication checks.

## UI flows
N/A — this is an opt-in machine-consumed format for an internal station command; the existing human-facing text invocation remains compatible.
