# Self-service CLI discovery and recovery
intent: 2026-11-12-cli-self-service@4eebeb0f
pre-build-review: required — externally consumed CLI help and recovery advice must preserve authorization and evidence boundaries

## Requirements
REQ-1 — Discover and prepare
  WHEN a first-time agent operates the covered verification and publication commands, the CLI shall expose sufficient bundled guidance to select the command and assemble its existing inputs from authentic supplied evidence → Acceptance #1
REQ-2 — Recover from input errors
  WHEN a covered invocation fails because of caller-correctable input, the CLI shall preserve its diagnostic and direct the caller to actionable usage and input guidance without requiring implementation inspection → Acceptance #2
REQ-3 — Interpret actual outcomes
  The command guidance shall distinguish completion, waiting, blocking and unconfirmed outcomes, including partial success and help-only execution → Acceptance #3
REQ-4 — Preserve compatibility and authority
  The CLI shall preserve existing valid calls, result formats, exit codes, authorization and independent verification requirements → Acceptance #4
REQ-5 — Evidence without supplied answers
  The acceptance evidence shall retain actual first-use and recovery attempts, supplied context, results and untested boundaries without claiming unmeasured cross-host or efficiency benefits → Acceptance #5

## Design decision

- agent-decided — REQ-1/2: bound this rollout to `finalize-review`, `publish` and `delivery`, the same verification/publication task boundary as the previous change. Add exact `<command> --help` and `<command> -h` forms. Top-level help names the covered forms. Help executes before repository lookup, runtime command dispatch, credential checks or external operations, returns 0 on stdout, and explicitly says no validation/publication occurred. Launcher runtime readiness remains required.
- agent-decided — REQ-1: keep help text beside the existing command dispatch in `loom_checker.py`, with a bounded mapping for the three covered commands. No new command framework, registry file, schema generator, converter, dependency or global output envelope. Long prose may be factored into a bundled sibling resource only if implementation demonstrates a concrete maintenance benefit; do not split merely to lower file length.
- agent-decided — REQ-1/4: finalization help describes positional change-id versus input-file path, clean committed content, review target HEAD versus diff base, distinct real reviewer attribution, original verdict preservation, findings, and adversarial program/no-program alternatives. Show a clearly labelled illustrative JSON shape with placeholders, not fabricated ready-to-submit approvals. Explain that skipped steps follow existing explicit instructions and that a no-program reason is an observed outcome, not a bypass. Refer to the bundled closing-review skill for complete outside-review receipt/probe rules by portable plugin-relative path.
- agent-decided — REQ-1/4: publish help names required authorization, title and body arguments, the nine required PR headings, verification disclosure and how to use a reported correction. Explicitly distinguish an already-authorized intent from the legacy confirmation argument: help never grants authority. Exit 2 includes invocation or authorization errors and internal failures; read the diagnostic for the next action rather than infer a retry from the code alone. Publishing may write remotely; help never does. Existing filename snapshots, origin/head reconciliation and branch/title policy remain unchanged.
- agent-decided — REQ-1/3: delivery help describes local/published/merged goals, optional intent path, JSON fields `state`, `reason`, `next`, `evidence`, `complete`, and the distinction between observation and authorization. The local goal checks that attributable paths are committed, not finalization, attestation or verification. A JSON object or `complete: false` is not proof of successful delivery. Document exit 0 for achieved goal, exit 1 for incomplete/unconfirmed outcome, and exit 2 for invocation/internal errors, according to the existing handler.
- agent-decided — REQ-2/4: at the public dispatcher, append one portable help hint for covered commands returning nonzero or raising UsageError. Preserve original diagnostic text, rule IDs, stdout and exit status; do not reclassify internal faults or parse diagnostic strings. The hint directs users to `<loom-code>/scripts/loom-python --ready <command> --help` and explains the placeholder. It must not cause a retry, mutation or exception swallowing. Uncovered commands and hooks retain their current behavior.
- agent-decided — REQ-3: guidance states stderr progress is advisory and can also contain errors; callers inspect exit/result and generated evidence. Stage pass is not overall finalization success; exit 0 with no required CI checks means no checks registered, not tests passed. A publication observation failure may follow a remote write: use delivery observation before considering another publication. No within-child heartbeat or new success summary is implemented here.
- agent-decided — REQ-4: only the exact two-token help forms are recognized. Extra operands, interspersed flags and unknown command names retain normal rejection; help must not accidentally turn an intended mutation into exit-0 success. No `--help` interpretation inside input values, shell scripts or hook arguments.
- agent-decided — REQ-5: independent acceptance runs in disposable local copies. Give the operator only the task, launcher location, allowed public documentation, raw authentic reviewer outputs and actual probe outcomes; no chosen command, completed input JSON, spec, plan, tests or implementation. The operator must retain its own first commands and failures. Provide one malformed caller input for recovery, and a missing-authorization publication task whose correct outcome is refusal rather than bypass. Real remote writes are excluded from this acceptance exercise; publication on the actual branch remains separately authorized through Ship.
- agent-decided — REQ-5: predeclare the acceptance task expectations outside the operator packet, record exact source/model observability and any mid-run help from the orchestrator. A fixture/setup issue is repaired transparently without erasing the failed attempt. Do not count repaired attempts as clean first-attempt success. No baseline improvement percentage is claimed without a comparable baseline run.
- agent-decided — complexity: prefer a bounded help mapping and dispatcher hint over a new protocol layer. Production growth is estimated at roughly 80–140 lines of explanatory text and 10–20 routing lines, with focused entry-level tests; these are estimates, not measured gains. No existing validator can be deleted without weakening the requirement. Replace any superseded help wording instead of duplicating it. This explicit bounded help mechanism is the exception budget under PRINCIPLES.md non-negotiable 4; it requires regression coverage and grants no generic framework budget.
- user-decided — preserve the existing worktree for this and subsequent work. Publication is authorized by the confirmed intent; merge still waits for acceptance, and cleanup must preserve this directory.

## Alternatives considered

- Documentation-only expansion: leaves ordinary per-command help failing and error recovery undiscoverable at the tool entry.
- Full structured errors or new JSON envelope: adds consumer migration not needed to expose existing requirements.
- Converter or schema-generation command: the prior comparison did not demonstrate less caller work, and authentic judgment must remain with reviewers.
- All-command migration: multiplies compatibility work without first validating the selected task boundary.
- Heartbeat and child-result summary: separately useful, but not necessary to test command discovery and input recovery; reconsider after measured first-use behavior identifies the next obstacle.

## Current state evidence

- Forward: `loom-code/scripts/loom_checker.py::main` recognizes only top-level `--help`/`-h` and dispatches command operands unchanged.
- Reverse: `loom-code/skills/closing-review/SKILL.md` section 5 supplies review-input shape; `loom-code/skills/ship/SKILL.md` supplies publication body and recovery workflow.
- Error: `command_handlers/finalize.py::_finalize` reports malformed input and schema findings; `command_handlers/publish.py::_publish_usage` and `cmd_delivery` return usage errors without a per-command help target. Observed installed 3.67.0 calls to all three `<command> --help` forms are rejected.
- Data: `command_handlers/finalize.py::_finalize` reads verdicts/findings/adversarial from a JSON object; `command_handlers/publish.py::observe_delivery` produces the existing delivery observation fields.
- Boundary: `loom-code/scripts/loom_checker.py::COMMANDS` is the public dispatch surface; handler validation, host hooks and installed runtime provisioning are outside the change.

## UI flows

| Case | Caller action | Output and next action |
|---|---|---|
| Discover | Request overall help | Existing command list plus covered per-command help guidance; stdout, exit 0, no validation. |
| Command help | Request help for one covered command, including outside a Git repository | Purpose, arguments, input shape or body requirements, outcomes and recovery guidance on stdout; exit 0, no external calls or mutations. |
| Missing data | Attempt a covered call with missing operands or malformed input | Existing diagnostic and exit 2 remain, with a command-specific help hint; inspect guidance, correct input, invoke again. No implicit repair. |
| Rejected evidence | Submit parseable but invalid review evidence | Existing BLOCK diagnostic and exit 1 remain, with help hint; obtain/correct authentic evidence, never invent a passing verdict. |
| Refused publication | Attempt publication without required authorization | Existing authorization diagnostic and exit remain, with help hint; wait for actual authorization rather than treating the help example as consent. |
| Waiting | A normally authorized long command is running | Existing stage/CI progress remains advisory; no new heartbeat. Continue observing the same process. |
| Partial or unknown | A publication command cannot confirm completion | Existing diagnostic/result/exit remain, with help hint explaining observation before any repeat write. |
| Empty CI | No required checks register | Existing success exit and no-checks message remain; help distinguishes absence of checks from tests passing. |
| Complete | Finalization or delivery achieves its goal | Existing artifact announcement or delivery object remains unchanged; no extra help hint on success. |
| Invalid help shape | Append extra operands to a help invocation, or request an unknown command | Existing dispatch/parser rejection and nonzero status remain; correct syntax, no success inferred. |
| Redirected streams | Capture stdout/stderr separately | Help is plain stdout; failures and help hints stay on stderr; machine result stdout remains parseable. |

Retry uses normal validation again and preserves work; abandon makes no additional action. This engineering change has no product decision point ②.
