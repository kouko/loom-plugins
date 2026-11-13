# Read-only CLI JSON pilot — spec
intent: 2026-11-14-cli-readonly-json@752d18c7efe09c0cd8bd0b2b764f3500d05ca330
pre-build-review: required — two new public CLI result contracts

## Requirements
REQ-1 — Parseable results with domain data
  WHEN either selected command receives the final JSON selector, the checker shall emit one complete typed result for success, blocking, usage failure or caught internal failure, with the common semantics and command data defined below → Acceptance #1
REQ-2 — Existing callers remain compatible
  WHEN a caller omits the JSON selector or uses an existing JSON interface, the checker shall preserve its text, streams, exit codes, check predicates, repeated-require behavior and authorization semantics → Acceptance #2
REQ-3 — Honest execution boundary
  WHEN JSON is selected, the checker shall remain read-only and noninteractive, reject invalid arguments before unrelated domain work, preserve startup boundaries and distinguish a successful observation from completed verification or authority → Acceptance #3
REQ-4 — Discoverable limits
  WHEN a caller reads help or the relevant command documentation, the checker shall describe the final-selector grammar, required operands, result fields, exit meanings, conservative reviewer floor and startup/error limitations consistently → Acceptance #4
REQ-5 — Real consumer evidence
  WHEN the pilot is validated in a clean environment, the validation shall exercise a consumer that branches on typed JSON fields for contract compatibility and reviewer policy, record success and failure cases alongside baseline text compatibility, and disclose untested boundaries without claiming efficiency gains → Acceptance #5

## Design decision
- agent-decided — Use the existing preparation result semantics for these two
  commands: they already distinguish passed, blocked and error without asking
  consumers to parse human text. Reuse plain existing functions/data where
  applicable; a small extension is preferable to a new registry or framework.
- agent-decided — Select JSON only with a final `--json` token after the command.
  Strip that token before normal command parsing. A remaining `--json` token
  is a duplicate-selector usage error before domain work. Exact command
  `--help`/`-h` stays text, exit 0; help combined with a final selector is an
  ordinary invocation and fails argument validation in JSON, exit 2.
- agent-decided — Without a final selector, preserve each token's existing
  meaning, including a literal reviewer-count change-id `--json` when it is
  not the final token selector form. `reviewer-count --json` selects JSON
  and reports the missing operand. No new escaping syntax or operand validity
  policy is introduced. This follows the bounded preparation pilot grammar.
- agent-decided — `contract --require A --require B --json` retains last-value
  wins; validate the final required value as today, without rejecting an
  earlier malformed value that the existing parser replaces. Unknown or
  missing arguments fail before manifest reads. reviewer-count accepts exactly
  one nonblank operand and checks the selected repository's clean tree before
  computing its floor. Do not tighten change-id validation in this pilot.

### Common result contract
- JSON stdout is exactly one object followed by a newline; checker stderr is
  empty, including help hints, domain blockers and caught exceptions. No text
  prefixes, progress lines, multiple objects or traceback precede the object.
- Fields: `schema_version` integer 1; `command` string `contract` or
  `reviewer-count`; `status` string `passed`, `blocked` or `error`;
  `diagnostics` ordered array of `{rule_id: string, message: string}`;
  `notices` ordered array of strings; `error` null or
  `{kind: "usage"|"internal", message: string}`; `data` object as below.
- `passed` maps to exit 0, empty diagnostics and null error; `blocked` maps
  to exit 1, nonempty rule diagnostics and null error; `error` maps to exit 2,
  empty diagnostics and a nonnull error. Empty arrays remain `[]`.
- Diagnostics carry check failures; notices carry nonblocking observations or
  actionable help only when actually relevant. Neither changes the status
  semantics. Consumers use keys, types and exit/status agreement, never key
  order or message prose. Existing plan/intake fields and delivery's distinct
  JSON contract remain unchanged; do not add their `data` field in this change.
- agent-decided — Missing repository and dirty-tree conditions retain the
  existing UsageError classification, rendered as `error.kind: usage`.
  Unexpected caught exceptions use `internal`; retain the existing checker
  exception message convention. Error rendering must also work before any
  repository is available. Never convert an exception into `passed`.

### Command data
- `contract` data always has `contract_version: string|null`,
  `required_version: string|null`, `compatible: boolean|null`.
  Passed/blocked results provide the actual stripped manifest version and
  final supplied requirement string, with compatible true/false respectively.
  Error results have all three values null: partial work is not a completed
  compatibility observation. Numeric major.minor parsing and matching stay
  exactly as implemented, including surrounding whitespace handling.
- `reviewer-count` data always has `change_id: string|null`,
  `reviewer_floor: integer|null`. Passed results carry the unchanged supplied
  change-id and computed integer floor (1 or 2 under current policy). Error
  results carry null for both fields; this command has no new blocker case.
- agent-decided — Expose the existing floor without a new classification
  claim: two is conservative when the committed delta cannot be classified,
  and may also be required by ordinary policy or outside-review selection.
  A floor of two and exit 0 do not prove complete classification, completed
  review, acceptance, finalization or successful delivery. One means the
  existing policy proved its narrow condition, not that review may be skipped.

### Effects and verification limits
- Both modes read the same manifest/repository facts and compute checks once.
  Neither writes artifacts, installs runtime, dispatches reviewers, requests
  confirmation, changes authorization or performs automatic retries. Correct
  inputs/repository conditions first, then rerun deliberately; observations can
  change between invocations. Contract checks need no Git repository.
- The guarantee begins in the loaded checker dispatcher for selected modes.
  Launcher/import failures, unavailable runtime (`--ready` exit 86), process
  termination and broken output pipes remain outside it. Help must tell callers
  to inspect both process exit and parseability rather than assuming JSON.
- agent-decided — Use a temporary clean repository/isolated consumer for dogfood,
  invoking the actual entrypoint, decoding the whole stdout and branching on
  status plus data: compatible requirement permits the next simulated step;
  incompatible requirement blocks it; malformed requirement rejects it; floor
  determines a simulated distinct-reviewer count. Include clean narrow and
  conservative-two cases, dirty and missing repositories, selector/help
  boundaries and a caught internal failure through an isolated test seam.
  Do not parse success prose, invoke paid models or execute live writers.
- Preserve baseline text stdout/stderr/exit observations for both commands,
  repeated requirements, unchanged plan/intake/delivery JSON and startup
  boundaries. Record commands, inputs, actual process results and decisions;
  distinguish automated evidence from untested live-host interactions.
- user-decided — Preserve all worktrees and historical validation records;
  exclude installed-plugin updates, new dependencies and JSON on other tools.
  Publication and automatic merge remain conditional on dogfood, independent
  review, complete package tests and CI passing with no important open issue.
- agent-decided — The prior coarse estimate in
  `/private/tmp/loom-readonly-json-complexity.txt` is planning input only:
  33/19-line handlers, 27-line renderer, estimated +80–160 maintained lines.
  It is not an actual delta or a speed/cost/token measurement. Measure the
  implemented change later; no generic error system or extra mechanism budget
  is justified by this pilot. Preserve the project non-negotiables.

## Alternatives considered
- Bare JSON scalar/version string: rejected because it cannot carry typed
  domain data and distinguish usage failure from incompatibility uniformly.
- New universal CLI result framework: rejected; two bounded commands can reuse
  existing result helpers without registry, dependencies or migrating delivery.
- Allow `--json` anywhere or prioritize help mixed with JSON: rejected because
  the existing final-selector pattern gives a small, explicit parsing boundary.
- Report reviewer-count two as classification complete: rejected because the
  current policy intentionally returns two when it cannot determine the delta.
- Add detailed reviewer classification telemetry: rejected because it requires
  expanding policy computation beyond the requested floor observation.

## Current state evidence
- Forward: `loom-code/scripts/loom_checker.py :: main` selects final JSON only
  for plan/intake and routes COMMANDS; COMMAND_HELP documents both text commands.
- Reverse: `loom-code/skills/closing-review/SKILL.md :: reviewer-count` consumes
  the floor; `loom-design/.claude-plugin/plugin.json :: requires-contract`
  declares the consuming plugin's required compatibility floor.
- Error: `loom-code/scripts/loom_checker/command_handlers/contract.py :: cmd_contract`
  validates arguments then reports contract.requires; `command_handlers/reviewer_count.py :: cmd_reviewer_count`
  raises UsageError on dirty trees; `helpers.py :: repo_root` rejects missing Git.
- Data: `loom-code/scripts/loom_checker/preparation_output.py :: new_result`
  defines the existing envelope; `reviewers.py :: required_reviewer_count`
  returns two on unreadable deltas; `rule_checks/contract.py :: check_contract_requires`
  retains actual compatibility rules; `loom-code/tests/test_preparation_json.py`
  asserts exact existing fields, and `loom-code/tests/test_delivery.py` consumes delivery JSON.
- Boundary: `loom-code/scripts/loom-python :: --ready` owns startup before the
  dispatcher; `PRINCIPLES.md :: Non-negotiables` requires machine evidence,
  independent review, preserved user data and no unbudgeted new mechanisms.

## UI flows
| Case | What the caller does | What they see |
|---|---|---|
| Contract success | Request a supported version with final JSON selector | One object, compatible true, passed, exit 0. |
| Contract blocked | Request an incompatible version | One object, compatible false, contract.requires diagnostic, exit 1; update the appropriate plugin before retrying. |
| Missing or malformed input | Omit or corrupt the required version, omit the change-id, add extra operands or repeat the selector | One usage error object, unavailable data null, exit 2; correct arguments and rerun. |
| Reviewer success | Supply a change-id in a clean repository | One passed object with integer reviewer floor, exit 0; obtain that many distinct reviewers. |
| Empty/unclassifiable delta | Request a floor where policy cannot prove the narrow condition | One passed object with floor two, exit 0; treat it as a conservative requirement rather than completed verification. |
| Dirty or absent repository | Request a floor without its repository prerequisites | One usage error object, exit 2; preserve work, finish and commit it or select a repository, then rerun. |
| Internal failure | A loaded checker encounters an unexpected exception | One internal error object, exit 2; correct the failure before retrying. |
| Help | Ask for exact command help without JSON | Text help, exit 0; no domain check runs. Mixed help and final JSON instead yields a usage error object, exit 2. |
| Text compatibility | Run either command without selecting JSON | Existing text streams and exits, including blockers and errors. |
| In progress | Run either bounded read | No progress output; wait for the one final result and process exit. |
| Startup failure | Run with unavailable runtime or a failure before the checker loads | Existing launcher outcome, potentially text and exit 86; inspect process output before parsing and repair runtime deliberately. |

Both commands are independently reachable; no persistent session or resumable
operation exists. After any error, retry revalidates the current inputs and
repository, preserving existing user work. No destructive operation is added.
