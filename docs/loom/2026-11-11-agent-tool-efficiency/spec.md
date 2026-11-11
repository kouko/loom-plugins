# Consistent CLI progress and bounded efficiency — spec
intent: 2026-11-11-agent-tool-efficiency@3499c468
pre-build-review: required — externally consumed CLI output and publication observation need compatibility and negative-path review

## Requirements
REQ-1 — Observable execution
  WHEN a selected long-running command executes, the tool shall expose truthful progress before completion while preserving existing final results and exit behavior → Acceptance #1
REQ-2 — Avoid irrelevant discovery
  WHEN a program lacks the required concern marker, the checker shall exclude it before test collection while preserving marked, moved, and unavailable-collection behavior → Acceptance #2
REQ-3 — Measured conversion decision
  WHEN progress and collection improvements have been verified, the evaluation shall compare existing and candidate review-data conversion on identical cases and report correctness, recovery, caller operations, and added maintenance cost → Acceptance #3
REQ-4 — Preserve authority and verification
  The tools shall preserve authorization, independent review, acceptance, and failure-blocking decisions throughout the interface changes → Acceptance #4

## Design decision

- agent-decided — REQ-1/4: adopt the bounded CLI conventions in [research](research/01-agent-interface-conventions.md), using existing command arguments and payloads. No MCP server, global JSON envelope, parser rewrite, new retry engine, or exit-code migration is justified by this change.
- agent-decided — REQ-1: first rollout targets `publish` and `finalize-review`. Existing stdout is compatibility-sensitive and remains unchanged. New progress uses the injected stderr stream, newline termination and explicit flush. No global launcher buffering change is necessary to make these messages observable.
- agent-decided — REQ-1: finalization emits a stage-start event before each blocking probe/package-suite subprocess and a stage-end event only after the existing evidence validators accept or reject its output. A child exit 0 is insufficient: `_runner_evidence`, `_pytest_summary_failure` and `own_pass` must accept it before stage success. Nonzero exit, timeout, execution error, or rejected exit-0 evidence reports failure; stage success is distinct from final attestation success. Child output remains captured under existing handling. A start event must be observable while a controllable child is still running; this does not promise live child logs or a heartbeat inside one long subprocess.
- agent-decided — REQ-1: publish emits a CI-observation start and distinct pending/registration-wait transitions, plus an elapsed wait notice at the first polling opportunity after each 60-second interval during unchanged polling. Existing ten-second polling and timeout limits remain unchanged. A monotonic clock determines elapsed time; tests control it. Terminal progress distinguishes passed, no-required-checks and failed/unconfirmed observations. Unknown total duration never becomes a percentage.
- agent-decided — REQ-1/4: progress includes a command/stage label and actual state, not command operands, environment values, credentials, or raw child logs. Known errors continue through existing error paths. A failed progress write must not convert a failed check into success or launch/repeat a mutation; treat progress-only OSError (including BrokenPipeError) as best-effort loss, preserving the command result and mutation count; do not change the handling of existing result/error stream failures.
- agent-decided — REQ-1/4: retain `delivery --json`, dispatch JSON, existing rule identifiers, and host hook protocols. Exit 2 currently conflates usage and internal faults; this change documents that limitation rather than promising new error categories. No consumer may be newly instructed to parse progress text for gate decisions.
- agent-decided — REQ-2: move the existing `_carries_concern` predicate ahead of `suite_collection` in `graduated_probe_programs`. Preserve the exact `is not False` policy, moved-path exclusion and program classification. No test discovery caching or policy relaxation.
- agent-decided — REQ-3: compare a retained manual YAML-to-JSON baseline with a temporary candidate outside production scripts, using public synthetic reviewer fixtures. Cover valid data, malformed YAML, duplicate keys, missing identity and rejected verdicts. Treat parser differences as results; neither arm may invent approval or passing verdicts. Preserve raw inputs, actual commands, outputs and failure outcomes in the evidence store.
- agent-decided — REQ-3: select a converter only if it demonstrably removes caller work without weakening validation/provenance, and record its maintenance footprint. A successful transform alone is insufficient. Production integration remains outside this change; no model token/time benefit is inferred from local parsing measurements.
- agent-decided — REQ-4: publish timeouts remain unknown outcomes, not proof of absent mutation. Existing repository/head/base reconciliation and authorization are unchanged. No automatic retry is added.
- agent-decided — REQ-1/4: maintain a developer-facing convention and command applicability table in the existing scripts documentation if present, otherwise this spec owns the first-rollout contract. Broader help, typed errors and additional JSON modes remain later migration candidates with explicit compatibility checks, not claims of current compliance.
- agent-decided — mechanism budget: permit at most one small shared progress emitter if both commands need identical formatting/flush behavior; otherwise use existing stream injection. No background threads, persistent state, new dependencies or generic command framework. This bounded observability cost is the declared exception to net-zero mechanisms in PRINCIPLES.md §Non-negotiables 4 and must be backed by regression tests.

## Alternatives considered
- Launcher-only unbuffering: cannot expose captured child output and does not establish progress semantics.
- Every polling iteration emits progress: repeats unchanged information without a useful bound.
- New JSON mode for all commands: expands compatibility work before a concrete consumer needs it.
- Immediate converter integration: skips the requested measurement and repeats the previous single-consumer adapter risk.
- Full module splitting: private imports and file sizes alone do not demonstrate a necessary boundary change.

## Current state evidence
- Forward: `loom-code/scripts/loom_checker.py::COMMANDS` routes publish and finalization to stream-injected handlers.
- Reverse: `loom-code/skills/ship/SKILL.md` invokes publish; `loom-code/skills/closing-review/SKILL.md` invokes finalize-review with temporary JSON.
- Error: `loom-code/scripts/loom_checker.py::main` returns 2 for usage/internal errors; `helpers.py::report` returns 1 for findings.
- Data: `command_handlers/publish.py::cmd_delivery` supports JSON; `command_handlers/finalize.py::_finalize` validates review JSON and captures subprocess output.
- Boundary: `loom-code/scripts/loom_checker/probes.py::graduated_probe_programs` collects before marker filtering; hooks and decision policy remain unchanged.

## UI flows

| Case | Caller action | Observable result and recovery |
|---|---|---|
| Publish waiting | Publish a reviewed change while CI registers or remains pending | Existing publication result stays on stdout; stderr identifies waiting before completion and reports bounded elapsed waiting. Continue observing; no duplicate publication is requested. |
| Publish success | Required checks pass | Existing `Required CI passed` and exit 0 remain; progress ends. |
| Publish no checks | No required checks register within the existing registration allowance | Existing `No required checks registered` and exit 0 remain; progress states no required checks rather than claiming tests passed. |
| Publish failure | CI fails or cannot be observed | Existing blocking reason, recovery guidance and nonzero exit remain; progress never reports passed. Query delivery before repeating an ambiguous mutation. |
| Finalization running | Finalize with valid review input and runnable verification commands | Stderr names each verification stage before it runs; stdout retains the existing final artifact announcement. |
| Finalization failure | A verification command fails or times out | Existing findings/nonzero exit remain; the stage cannot report success. Correct the reported cause before rerunning. |
| Finalization empty/skipped | Existing policy selects no commands in a category | No fabricated execution event; remaining checks and existing final result run normally. |
| Invalid invocation | Supply invalid operands, unreadable/malformed JSON or an invalid top-level shape | Existing usage/error response and exit 2 remain; correct the input before rerunning. No mutation or progress implying completed work. |
| Rejected review object | Supply valid JSON with rejected verdicts or other semantically invalid review evidence | Existing findings and exit 1 remain; repair the cited evidence before rerunning. |
| Rejected child evidence | A verification child exits 0 but lacks required passing-test evidence | The stage reports failure and existing finalization findings remain; fix the verification command or evidence before rerunning. |
| Redirected output | Capture stdout and stderr separately | Stdout compatibility is preserved; stderr has plain newline records, without animation or carriage-return replacement. |
| Interrupt/repeat | Interrupt a command and subsequently invoke it again | No new automatic resume or retry; existing checks rerun and existing publication identity checks apply. Partial remote outcomes must be observed rather than guessed. |

Collection filtering and conversion evaluation have no additional product UI.
Engineering classification exempts decision point ②; no additional user question
or approval is introduced by this spec.
