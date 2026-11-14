# CLI consistency and checked consumers — spec
intent: 2026-11-14-consume-readonly-json@e0cfabe5
pre-build-review: required — an executable consumer boundary and station guidance interpret public result contracts

## Requirements
REQ-1 — Whole-inventory scope without false completion
  The delivery shall retain a source-grounded sixteen-command inventory with mode differences, common consumption principles and explicit migrated/unmigrated status → Acceptance #1
REQ-2 — Adopt typed observations in real stations
  WHEN planning checks compatibility or closing review obtains its reviewer floor, the station shall invoke the checked JSON consumer and use validated compatibility or reviewer data without parsing success prose → Acceptance #2
REQ-3 — Validate before accepting an observation
  WHEN a selected result is consumed, the consumer shall verify version, command, required structure/types, request identity and exit/status agreement, allow compatible extra fields, and reject malformed or contradictory observations → Acceptance #3
REQ-4 — Preserve producer behavior and authority
  WHEN checked consumption is used, the system shall preserve existing direct text/JSON behavior, domain policy, authorization, hook trust and operation reconciliation without introducing write effects or implicit retries → Acceptance #4
REQ-5 — Document and independently exercise the delivered boundary
  WHEN this first batch is delivered, its help, station guidance and fresh-copy dogfood shall agree on successful, rejected and invalid observations and disclose unverified boundaries → Acceptance #5

## Design decision
- user-decided — The latest direction is consistency first. The user's response
  "先處理一致性的缺口 吧" selects the preceding comparison's common inventory,
  two real consumers and necessary failure semantics; automatic text fallback
  and generalized recovery are deferred. Earlier open drafts never started a
  formal review episode. Preserve their provenance, not their superseded scope.
- user-decided — Preserve text/JSON contracts, host trust, existing recovery and
  every worktree. Publication authorization was disclosed in the intake dialogue;
  merge remains decision point ③. No installed-plugin refresh or paid outside
  model execution is part of this change.
- agent-decided — Add one bounded executable script,
  `loom-code/scripts/checked_readonly.py`, through the existing loom-python
  `--script` path. It has two concrete callers now: write-plan compatibility
  and closing-review reviewer count. It is not another checker subcommand;
  COMMANDS remains sixteen. No launcher change, new dependency, registry,
  schema service, retry state or producer rewrite is needed.
- agent-decided — The script's public entry is `main`; validation stays private
  in that file. Run the sibling checker once using the current interpreter,
  argument-list subprocess execution and a 30-second timeout. The outer
  launcher owns readiness/repair; the child uses its already prepared runtime.
  No stdin, shell evaluation, installation, network, artifact write, dispatch,
  automatic retry or fallback is introduced by this script.

### Invocation and discovery
```
loom-python --repair --script checked_readonly.py contract --require 2.1
loom-python --ready --script checked_readonly.py reviewer-count <change-id>
loom-python --ready --script checked_readonly.py --help
```
- Accept only contract or reviewer-count as the selected command, forward their
  operands unchanged, and append the final JSON selector to the child checker.
  The checker remains the owner of operand grammar, last-require wins and policy.
  Unknown commands and an empty invocation fail before child execution. Callers
  must omit --json because the consumer adds it; supplying one is a usage error
  before the child. Literal selector operands are outside this bounded consumer;
  direct checker calls retain their current meaning.
- Exact script --help or -h prints safe text and exits 0 without a child. Help
  describes invocation, the validated fields and errors, the timeout, readiness
  boundary and the lack of fallback/authority. Command-specific producer help
  remains available through the original exact command-plus-help forms.

### Result acceptance rules
- Decode one complete JSON object; reject invalid syntax, trailing objects,
  duplicate mapping keys at any depth and non-JSON NaN/Infinity values. Leading
  or trailing whitespace is harmless. Never rely on key order or exact prose.
- Require integer schema_version exactly 1 (boolean is not integer here), the
  requested command, status passed|blocked|error, diagnostics and notices arrays,
  error and a data object. Ignore unrelated additional keys, including nested
  additions, while preserving them in the accepted observation.
- Require each diagnostic to contain nonblank string rule_id and string message;
  each notice is a string. Passed maps to exit 0, empty diagnostics and null
  error. Blocked maps to exit 1, nonempty diagnostics and null error. Error maps
  to exit 2, empty diagnostics and an error object with kind usage|internal and
  string message. Wrong types, unknown status/version/command, nonzero success,
  diagnostics on passed, or contradictory error/state are invalid observations.
- Contract data requires nonblank contract_version/required_version strings and
  a boolean compatible for passed/blocked. Require compatible true for passed,
  false for blocked, and required_version equal to the final supplied requirement
  operand without normalization. Do not recompute version policy or compare the
  observed current version against a second independently maintained manifest.
- Reviewer data requires the unchanged requested change_id and a positive integer
  reviewer_floor (not boolean); require passed, never blocked. The producer's
  present floor is one or two; accepting a future positive larger floor preserves
  conservative compatibility without claiming policy classification or completion.
- Valid error results require null values for the known command data fields.
  Extra fields remain allowed. No domain observation is usable on error.
- An accepted result is emitted as one normalized JSON object plus newline,
  empty consumer stderr, retaining its child exit 0/1/2. Preserve additional
  fields and the original diagnostic/notices strings. This is a validated
  observation, not a new whole-workflow success result.
- Malformed/mismatched results or unexpected child stderr produce no stdout,
  a concise `checked-readonly:` stderr diagnostic and exit 2. They do not emit
  a fabricated producer passed/blocked object. Child invocation/timeout failures
  similarly exit 2 with an actionable diagnostic, retaining the distinction
  from a valid business rejection. An observed child readiness exit 86 remains
  86 with its failure diagnostic; outer launcher failures remain its own contract.
- Validation does not prove computational truth: well-formed incorrect values
  may pass structural checks. This batch neither promises arbitrary defect
  recovery nor claims text fallback could independently verify shared logic.

### Consumer guidance and ownership
- write-plan and its Codex first-contact duplicate use the checked contract
  invocation. Continue only for an accepted passed observation and true
  compatibility. Only a valid contract.requires diagnostic establishes the
  existing outdated-contract response. Valid usage/internal errors, invalid
  observations and startup errors retain their diagnostics and stop that
  prerequisite; never label all failures as version incompatibility.
- closing-review uses the checked reviewer invocation. Only validated passed
  data determines how many independent reviewers to dispatch. Recompute the
  existing policy later as before; the consumer never overrides it. Invalid
  or error observations do not dispatch reviewers or substitute a default floor.
- Update the existing English documentation, helper discovery and release
  metadata. Localized README version strings retain parity. Publish the
  sixteen-command inventory as current status, not sixteen completed migrations;
  retain delivery's different JSON shape and the separate host hook protocols.
- Complexity: one two-command consumer is smaller than per-station inline
  parsers, multiple schema files, an all-command adapter or generic recovery
  framework. It adds maintained validation/tests; measure the real delta during
  Build. No new station, rule ID or broad mode is introduced. Declare the one
  bounded script's mechanism-budget exception in the plan and cover it through
  its real entry and two consumers, rather than adding a second policy gate.

## Alternatives considered
- Switch two command examples to --json only: smaller, but leaves deterministic
  acceptance of malformed observations unimplemented.
- Duplicate an inline Python validator in each skill: creates two drift surfaces
  and long shell instructions; rejected in favor of one bounded script.
- Migrate every producer or create a universal schema/adapter registry: exceeds
  the known consumer gap and forces incompatible result families together.
- Automatically retry or parse text after malformed JSON: lacks incident-backed
  necessity, increases paths and can conceal a shared computation defect.

## Current state evidence
- Forward: `loom-code/skills/write-plan/SKILL.md :: Step 0` and
  `loom-code/skills/closing-review/SKILL.md :: reviewer-count` still consume text.
- Reverse: `loom-code/skills/write-plan/references/codex-first-contact.md :: At the start`
  repeats the contract call; both new callers belong to loom-code only.
- Error: `loom-code/scripts/loom_checker.py :: main` catches exceptions and
  `loom_checker/preparation_output.py :: error_result` clears known partial data;
  neither validates a consumer observation.
- Data: `loom_checker/command_handlers/contract.py :: cmd_contract` and
  `command_handlers/reviewer_count.py :: cmd_reviewer_count` own observations;
  `preparation_output.py :: new_result` owns existing producer envelopes.
- Boundary: `loom-code/scripts/loom-python :: --script` already runs plugin
  scripts using its runtime; `command_handlers/land.py :: _squash_merge` owns
  existing completion reconciliation, which this change leaves intact.

## UI flows
| Case | Invocation/action | Visible result and next step |
|---|---|---|
| Help | Ask the consumer for exact help | Text exit 0, no checker call; read its field/error contract before use. |
| Empty/unknown command | Omit or choose an unsupported command | No JSON, usage diagnostic exit 2; correct the command. |
| Compatible contract | Run checked contract with supported requirement | Validated JSON exit 0; station may continue its prerequisite. |
| Incompatible contract | Run checked contract with incompatible requirement | Validated blocked JSON exit 1; follow the real diagnostic and stop the prerequisite. |
| Reviewer floor | Run checked reviewer count in a clean eligible repository | Validated passed JSON exit 0; station uses its positive integer floor for distinct reviewers. |
| Ordinary input/domain failure | Child emits a valid usage/internal error | Validated error JSON exit 2 with null known data; correct the indicated failure before a deliberate rerun. |
| Malformed or contradictory result | Child output violates acceptance rules | Empty stdout, checked-readonly diagnostic exit 2; inspect the reported mismatch, no fallback or success claim. |
| Readiness failure | Required runtime is unavailable | Existing launcher exit 86 for ready mode; follow its repair guidance, do not call it a contract blocker. |
| Waiting/timeout | Checker is running | No new progress stream; after 30 seconds, empty stdout and timeout diagnostic exit 2; investigate before deliberately rerunning. |

No operation rewrites existing user data or sends it to an outside model.
Invocation/field standards use Python's documented subprocess argument-list and
JSON APIs: https://docs.python.org/3/library/subprocess.html and
https://docs.python.org/3/library/json.html . The existing public producer
contracts and the retained research record supply the project-specific semantics.
