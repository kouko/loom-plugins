# Suggested next steps — spec
intent: 2026-11-14-cli-next-guidance@e2b6c517
pre-build-review: required — additive public JSON advice and agent-consumption guidance need independent contract review

## Requirements

REQ-1 — Bounded shared guidance
The CLI result guide shall define common next-step advice principles and distinguish the first two migrated consumers, existing advice and remaining command interfaces → Acceptance #1

REQ-2 — Actionable but honest advice
WHEN either first-batch command refuses or fails, the CLI shall provide cause-appropriate suggested handling, retaining uncertainty and investigation guidance when a reliable repair is unknown → Acceptance #2

REQ-3 — Advice is not authority
WHEN advice is present, absent or unusable, the consumer shall keep authoritative result classification and existing authorization unchanged and shall not execute advice, retry or fall back to text automatically → Acceptance #3

REQ-4 — Compatible existing results
The first-batch advice shall preserve existing result facts, exit codes, required data, reviewer policy, authority, host trust and operation reconciliation without new write effects or breaking existing next-step advice → Acceptance #4

REQ-5 — Executable documentation and evidence
WHEN the first-batch interfaces are documented and tried independently, their help and guidance shall match observed normal, refused and error behavior and disclose missing-advice and unverified boundaries → Acceptance #5

## Design decision

- user-decided — The accepted naming proposal was: "文字輸出可用 Suggested next step:，JSON 欄位可用 suggested_next。規範仍應明寫：這是建議，不改變判定結果，也不構成執行授權。" The user answered "ＯＫ" after requesting emphasis on the advisory wording. Use the exact text label `Suggested next step:` and JSON key `suggested_next` in this batch.
- agent-decided — Scope is the existing `contract` and `reviewer-count` producer results, their checked consumer faults, and their documented station use. Preserve all sixteen commands in the inventory; neither new JSON modes nor an all-command migration is required. Leave delivery's existing string `next` and publish/land/launcher remedies intact; explicitly label them unmigrated or legacy guidance rather than silently rename them.
- agent-decided — Add an optional advisory top-level member to the two existing schema-version-1 JSON results. New producers always emit `suggested_next` as a nonblank English string for blocked/error, or null for passed. All existing envelope/data fields, diagnostics, notices, stdout purity and 0/1/2 meanings remain. Preparation `plan`/`intake` and delivery shapes do not gain this member in this batch.
- agent-decided — Store advice generation with the existing bounded result renderer, keyed by command and actual result category, and let text and JSON reuse the same advice value. Do not match human error prose or duplicate compatibility/reviewer policy. A few known outcomes need no registry, new source module, action class, command list or dispatcher.
- agent-decided — Contract blocked advice directs the caller to update the plugin identified by the real contract diagnostic, then recheck supported requirements. The existing checker can identify an outdated consuming plugin rather than loom-code itself; never flatten these into an unconditional loom-code update. Contract usage advice asks the caller to inspect the reported operand/manifest issue and command help, then correct it before deliberate re-execution.
- agent-decided — Reviewer usage advice asks the caller to inspect the diagnostic and help, select the intended repository, preserve outstanding work and establish a clean completed change before deliberate re-execution. Do not tell the agent to discard, automatically commit unrelated work, reduce the reviewer floor or assume that every usage error is a dirty tree.
- agent-decided — Internal error advice asks for investigation of the reported failure and preservation of work; it does not guess a repair, claim a transient condition, tell the user to update for every error or authorize repeated execution. Known errors share concise category-appropriate advice, not a fragile per-message catalog.
- agent-decided — Direct text calls preserve their original result/error lines and successful stdout. Append one labeled advice line on stderr for the two commands' refusal/usage/internal results. Existing Help hints stay available. JSON calls keep accepted result/error advice inside the single JSON object, never mix that text label into JSON stdout or introduce JSON-mode stderr for ordinary command outcomes.
- agent-decided — Missing, null, blank or non-string `suggested_next` never changes core observation validity. The checked consumer keeps strict validation of authoritative fields as shipped; advice is an optional extension, not required data. Preserve accepted raw JSON, compatible unknown fields and numeric precision. Station guidance may read a nonblank string after accepting the core observation, otherwise ignore the advice and retain the original diagnostic. Do not claim that a core-valid observation makes arbitrary advice trustworthy or executable.
- agent-decided — Checked-consumer local usage, validation faults, startup 86, OSError/Unicode/deep-JSON failures and timeout continue to have empty stdout and their existing exit distinction. Append one `Suggested next step:` stderr line generated locally, suitable for discovery/input correction, runtime investigation or output-contract investigation as applicable. Never derive recovery commands from malformed child stdout or unexpected stderr. The subprocess remains one execution with Python import isolation and the configured 30-second timeout; no change to readiness/repair ownership.
- agent-decided — Exact script help is still safe text exit 0 with no child. Unknown/empty commands and supplied `--json` still run no child. Help can describe suggestion semantics but emits no invented result or recommendation on successful checks. No useful advice is a valid state.
- agent-decided — Existing station consumers keep their deterministic core-result prerequisites, then present applicable advice as advisory content, never as authorization to continue, retry, publish, merge or bypass host trust. Without a usable suggestion, report the original diagnostic. An unknown observation cannot authorize its dependent action merely because a suggestion exists.
- agent-decided — The shared guide owns advice principles and the migration table. Explain the difference between structured decision facts and prose inside a JSON string. No gain in resolution rate, time, tokens or cost has been measured. Extend existing behavior tests through public entries and actual subprocess/launcher seams; do not add a prose-pin suite or a recovery framework.
- agent-decided — The change adds maintained advice and tests rather than reducing total code. Intake estimates were +30–70 source lines, +40–100 test lines and +40–100 guidance lines with no new source/test module; these are rough estimates, not limits or observed effort. No safe source/test deletion is established. Plan declares the additive public-field mechanism budget exception and records actual delta before review.

## Alternatives considered

- Keep `next` for new output: smaller naming reuse, but does not honor the user's explicit advisory naming; retain it only on existing delivery to avoid a breaking rename.
- Prose-only scattered remedies: adds no JSON member but retains the observed location inconsistency and does not satisfy the selected first-batch outcome.
- Require or strictly reject optional advice before accepting core data: makes legacy or malformed advisory content change authoritative classification, violating Acceptance 3 and compatibility.
- Normalize/drop malformed optional advice by re-encoding all JSON: adds transformations and risks precision loss merely to process non-authoritative prose; retain raw valid core observations and require a simple caller-side string check instead.
- Typed executable action objects or auto-repair/retry: introduce execution, environment and authorization semantics without a current automated consumer requiring them; outside this intent.
- Force all commands, progress/help and host hooks into one schema: broadens the batch and changes protocols unrelated to the two real consumers.

## Current state evidence

- Forward: `loom-code/scripts/loom_checker.py :: main` selects the optional read-only envelope, executes a handler once, and renders ordinary text or one JSON result.
- Reverse: `loom-code/skills/write-plan/SKILL.md :: Step 0`, `references/codex-first-contact.md :: At the start` and `loom-code/skills/closing-review/SKILL.md :: reviewer-count` call `checked_readonly.main`; the existing guide inventories sixteen commands and two checked consumers.
- Error: `loom-code/scripts/checked_readonly.py :: main` reports malformed observations and timeout to stderr; `loom_checker.py :: except UsageError / except Exception` owns producer usage/internal rendering.
- Data: `loom-code/scripts/loom_checker/preparation_output.py :: new_result / report_result / error_result` own bounded envelopes; `command_handlers/contract.py :: cmd_contract` and `reviewer_count.py :: cmd_reviewer_count` compute domain values. `rule_checks/contract.py :: check_contract_requires` distinguishes outdated consuming and producing plugins.
- Boundary: `loom-code/scripts/loom_checker/command_handlers/publish.py :: DeliveryResult / observe_delivery / cmd_delivery` retain existing `next`; publish/land remedies and `scripts/loom-python :: --ready / --repair` remain outside implementation scope.

## UI flows

| Case | Action | Result and next handling |
|---|---|---|
| Discovery | Request exact command or script help | Text exit 0; see the advisory label/key and limitations. Script help runs no checker. |
| Compatible observation | Check a supported requirement | Passed exit 0, unchanged data; JSON suggestion is null, text success is unchanged. No fabricated follow-up is required. |
| Incompatible observation | Check an unsupported requirement | Blocked exit 1 and real diagnostic; suggested handling names the diagnostic's indicated plugin, then rechecking the requirement. No continuation or automatic update. |
| Reviewer result | Count reviewers on a completed clean change | Passed exit 0 and unchanged floor; JSON suggestion is null. Dispatch remains governed by the accepted floor and existing review policy. |
| Invalid command input | Omit required operands or supply invalid ones | Error exit 2 with original cause plus labeled or JSON suggestion to inspect help/correct the reported condition. No automatic correction. |
| Invalid repository state | Count reviewers outside the intended eligible clean repository | Usage exit 2, null domain data and advice to inspect conditions while preserving work. No default count or automatic data change. |
| Internal failure | Producer computation raises | Error exit 2 and original internal diagnostic; suggestion asks for investigation, not an invented repair or blind retry. |
| Unknown observation | Child JSON is malformed, contradictory or identity-mismatched | Consumer stdout remains empty, exit 2 and original fault plus locally generated output-contract investigation suggestion. Never trust suggestions in malformed output. |
| Legacy or unusable advice | Accepted core JSON lacks a useful string suggestion | Core status/data stay usable under existing prerequisites; ignore optional advice and retain diagnostics. No inferred continuation or recovery. |
| Local usage failure | Invoke empty/unknown script command or supply its own JSON selector | Exit 2 and no child; see exact help/input-correction suggestion. |
| Startup failure | Runtime or child cannot start | Existing launcher repair guidance remains; consumer-observed 86 stays 86, other execution faults stay 2. Consumer faults may add the advisory label without hiding original diagnostics. |
| Waiting and timeout | One child is still running | No new progress stream. Configured timeout still exits 2 with empty stdout; suggestion asks for investigation before deliberate re-execution. Process creation is not covered by an absolute wall-clock guarantee. |

No operation here rewrites user data, executes advice or sends it to an outside
model. Piped JSON remains one object; successful raw formatting and unknown
numeric extensions remain preserved. General guidance precedent is CLIG's
actionable-error and subsequent-command guidance (https://clig.dev/#errors),
and Google AIP-193's separation of machine-readable errors and actionable
resolution (https://google.aip.dev/193). These are design precedents, not
evidence that this batch improves agent success rates.
