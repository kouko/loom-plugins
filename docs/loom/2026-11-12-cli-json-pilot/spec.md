# Optional JSON results for preparation checks — spec
intent: 2026-11-12-cli-json-pilot@d19fc147
pre-build-review: required — This introduces a public result contract while preserving existing callers and fail-closed behavior.

## Requirements

REQ-1 — Parseable check results
  WHEN a caller selects JSON output for plan or intake, the checker shall provide a parseable result distinguishing a passed check, rule blockers and invocation errors with their diagnostic information → Acceptance #1

REQ-2 — Existing callers remain compatible
  WHEN a caller uses an existing text invocation, the checker shall preserve its output streams, exit status, evaluated rules and authorization or verification conditions → Acceptance #2

REQ-3 — Traceable comparison
  The pilot shall retain a comparison of text and JSON operation on the same genuine tasks, reporting interpretation errors, corrections, operation counts and output volume with limitations and non-improvements → Acceptance #3

## Design decision

- user-decided — Limit the pilot to optional `--json` for plan and intake; preserve existing text output and exit codes. The accepted proposal does not authorize a global output migration.
- agent-decided — Accept JSON mode only when the final argument is exactly `--json`: `plan <path> --json` and `intake <station> <change-id> --json`. Remove that one mode selector before validating the remaining operands; in selected JSON mode, reject any remaining standalone `--json` as a duplicate selector. This gives an unambiguous, small grammar without replacing the parser. Missing operands and extra arguments remain errors. Without a final selector, an earlier `--json` remains an ordinary operand under the existing grammar; do not silently scan or reorder operands. `plan ./--json --json` can check a file literally named `--json`.
- agent-decided — Preserve exact existing `command --help` and `command -h` forms as text-only, exit 0 without validation. A help token combined with JSON is not a help request: remaining operands are validated normally. Expand those two help pages and overall usage to document the final-position selector and result contract.
- agent-decided — Emit one UTF-8 JSON object and one trailing newline on stdout for every completed in-process JSON-mode invocation, including malformed operands, unreadable files, rule blockers and unexpected exceptions. Emit no human diagnostic, notice, appended help hint or traceback outside that object. No progress stream is introduced for these short local checks. This prevents a valid JSON object from being contaminated by existing intake stdout. Launcher readiness/startup failures before checker dispatch, process termination, and broken output pipes are outside this result guarantee and remain observable process failures.
- agent-decided — Use the following version-1 fields, always present: `schema_version` (integer 1), `command` (`plan` or `intake`), `status` (`passed`, `blocked`, `error`), `diagnostics` (ordered array of `{rule_id, message}` strings), `notices` (ordered array of strings), and `error` (null or `{kind, message}`, where kind is `usage` or `internal`). `passed` and `blocked` have null error; `error` has empty diagnostics. Empty collections are `[]`, never null. `blocked` requires at least one rule diagnostic. Status describes only this invocation's implemented checks; it is not workflow completion, publication authority or a claim that every possible check ran.
- agent-decided — Exit 0 pairs with `passed`; exit 1 with `blocked`; exit 2 with `error`. Keep invocation/unreadable-operand failures as `error.kind: usage`; keep unexpected exceptions as `error.kind: internal`. Preserve the current reason text, including the existing internal-error exception type and message, without adding traceback or environment dumps. A structured error does not authorize an automatic retry.
- agent-decided — Retain the existing ordered `(rule_id, reason)` failures as the source of diagnostics. Serialize those values before human `BLOCK ...` formatting; do not recover fields by parsing stdout/stderr prose. Existing usage-error exceptions and explicit unreadable-file reasons supply usage errors directly. Retain conditional intake advisory messages as notices directly from the emitting path, without interpreting a notice as a pass or blocker. JSON rendering must not execute checks twice or maintain a second set of rule decisions.
- agent-decided — Keep text rendering byte-compatible, including conditional `interface-surfaces (...)` stdout, early confirmation failures before that notice, original BLOCK ordering, missing-file messages and appended help hints. Preserve partial notices if a later JSON-mode check raises; the final status is still error. Normal JSON mode is a representation change, never a weaker check.
- agent-decided — Keep formatting support bounded to these two handlers and the public dispatch boundary for their JSON-mode exceptions; do not add a global framework, new dependency, new rule IDs, configurable serializer or conversion tool. Mechanism budget exception: one optional representation/serialization mechanism, justified by REQ-1, with public-entry regression cases for success, blockers, usage/internal errors, mixed notices and text parity. No new gate or policy mechanism is introduced.
- agent-decided — The schema is a versioned pilot contract, not a copy of gh's field selection API or delivery's goal/completion schema. Within version 1, keep field names, types and meanings stable; do not make consumers depend on key order, indentation or diagnostic message wording. A future incompatible shape needs another schema version and a separate change.
- agent-decided — REQ-3 requires a preregistered task set, interpretation answers and counting rules before the comparison starts. Use identical genuine artifact snapshots and equivalent tasks for the two modes; preserve raw commands, separated streams, exits, source SHA and operator answers. Count stdout/stderr UTF-8 bytes separately; label any token estimate. Report all four requested metrics even when equal or worse. Planning owns the bounded procedure and independent operators; acceptance owns judging the evidence. Do not call an informed comparison blind, infer broad efficiency from a small sample, or manufacture a benefit threshold after observing results.
- agent-decided — These local read-only checks add no paid service, network dispatch, data migration or automatic repair. Existing user state is not changed by either output mode; comparison corrections use disposable copies.

## Alternatives considered

- Continue text-only guidance: smaller, but cannot establish the requested program-readable pilot or its comparison.
- Parse captured BLOCK lines into JSON: a small patch but a second, fragile interpretation of rule results; rejected in favor of existing diagnostic values.
- Migrate all commands or change default output: broadens compatibility and acceptance obligations beyond the confirmed pilot.
- Reuse delivery's `complete` and goal states: risks implying whole-workflow completion for bounded prerequisite checks.
- Add selectors, jq integration, a schema validation dependency or a generic result class hierarchy: no current requirement justifies the added surface; fixed ordinary data suffice.
- Guarantee efficiency improvement: not supported by evidence; require an honest comparison instead.

## Current state evidence

- Forward: `loom-code/scripts/loom_checker.py:292` (`main`) dispatches handlers, adds human failure hints and handles usage/internal exceptions; existing exact help forms return before dispatch.
- Reverse: `loom-code/skills/write-plan/SKILL.md` (`The intake check`) invokes intake and plan as separate checks; `loom-code/tests/test_loom_checker_cli.py:483` exercises missing operands through the public CLI.
- Error: `loom-code/scripts/loom_checker/command_handlers/plan.py:26` emits missing/unreadable-file errors; `loom-code/scripts/loom_checker/helpers.py:37` defines UsageError and `:41` formats rule tuples as BLOCK lines.
- Data: `loom-code/scripts/loom_checker/command_handlers/intake.py:68` accumulates ordered rule failures; `loom-code/scripts/loom_checker/rule_checks/intent.py:395` writes the interface-surfaces advisory before possible later failure.
- Boundary: `loom-code/tests/test_loom_checker_modules.py:57` enforces dispatcher ownership; only plan/intake result representation and their exception boundary change. Other commands, hooks, rules and legacy streams remain outside the pilot's behavioral edits.

## UI flows

| Case | What the caller does | What they receive and how to proceed |
|---|---|---|
| Discover | Runs `plan --help` or `intake --help` | Text describes existing operands, final `--json`, result fields and limited check meaning; exit 0; no validation. |
| Existing text | Runs a previously supported invocation without selecting JSON | Existing stdout, stderr and exit status; use the same interpretation and recovery as before. |
| JSON success | Runs a valid check with final `--json` and no rule failures | One object with status passed, diagnostics [], error null and any advisory notices; exit 0. This only reports the selected checks. |
| JSON blockers | Checks genuine content that violates one or more evaluated rules | One object with status blocked, original ordered rule IDs/reasons, any notices and error null; exit 1. Correct the named artifacts through their owning workflow and rerun. |
| Empty or malformed operands | Omits required operands or supplies unsupported station, malformed change ID, duplicate selector or extra argument while selecting JSON | One object with status error, error.kind usage and the original diagnostic; exit 2. Read help separately and correct the invocation. |
| Missing or unreadable plan | Selects JSON for a nonexistent file, directory or inaccessible file | One usage-error object with the original reason; exit 2. Correct the path or access and rerun. |
| Repository usage error | Runs repository-dependent intake outside a Git worktree with JSON selected | One usage-error object with the original repository diagnostic; exit 2. Enter the intended repository and rerun. |
| Advisory then failure | Runs intake that produces an interface notice before a later blocker or exception | The notice is inside notices; status remains blocked or error, with its matching exit. Do not treat an advisory as successful intake. |
| Unexpected internal failure | Encounters an unexpected checker exception after JSON dispatch | One error object with kind internal and the existing exception diagnostic; exit 2. Inspect and resolve the environment/defect before trying again; never treat it as a passed check. |
| Help combined with JSON | Supplies a help token plus final `--json` | This is not exact help: normal operand validation/checking applies and yields its JSON result/exit. Use `command --help` alone to read guidance. |
| Piped output | Captures JSON stdout separately from stderr | Stdout parses as a single object, stderr is empty for completed checker JSON results; exit still distinguishes the outcome. Launcher/process failures are handled from their actual diagnostics. |
| In progress / no diagnostics | Waits for the local check or receives no failures | No new spinner, heartbeat or durable running state. Until the process exits there is no final result. Empty diagnostics on passed means no evaluated rule failed, not that every workflow obligation was examined. |

Recovery reruns the selected check against current artifacts; nothing from the previous result authorizes a write or waives validation. Switching back to text mode changes representation only. There are no destructive actions, resumable jobs or stored user-state transitions in this pilot.
