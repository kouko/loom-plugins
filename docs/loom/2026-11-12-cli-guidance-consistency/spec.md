# Consistent planning-command guidance — spec
intent: 2026-11-12-cli-guidance-consistency@ecaac7d971c5e7ffc75996b4c78ac76517eaf908
pre-build-review: required — Extends the public CLI help and failure-guidance contract; an inaccurate success description could misrepresent verification.

## Requirements

REQ-1 — Discover and use the next bounded command batch
  WHEN an operator requests help for `plan`, `intake` or `reviewer-count`, the CLI shall provide consistent purpose, invocation, input requirements, outcome interpretation and recovery guidance sufficient for an independent operator to perform each existing task → Acceptance #1

REQ-2 — Recover without mistaking a check for completion
  WHEN a covered invocation fails through an existing usage or reported-check outcome, the CLI shall preserve the diagnostic and append the matching help entry point on stderr, with guidance distinguishing invalid invocation, blocked checks and limited successful checks → Acceptance #2

REQ-3 — Preserve existing execution contracts
  The CLI shall preserve existing valid-call stdout, exit statuses, argument validation, authorization and verification conditions, while exact help requests return stdout and exit 0 without executing their handlers → Acceptance #3

## Design decision

- agent-decided — Select `plan`, `intake` and `reviewer-count` as this batch: they are local, read-only preparatory checks used by planning and review, have three distinct input shapes, and can be exercised without remote writes. This advances the confirmed incremental scope without adding publication or cleanup risk.
- agent-decided — Extend the existing exact-help mapping and failure-hint policy rather than introduce another parser, registry or formatter. The common guidance order is purpose, usage, inputs/preconditions, outcomes/recovery and explicit help-only notice. Existing covered commands retain their behavior.
- agent-decided — Accept only the existing exact `<command> --help` and `<command> -h` forms for help, including outside a repository. Extra operands retain existing rejection; a token embedded elsewhere in a normal invocation does not become a help request.
- agent-decided — Document `plan <path>` as a direct check of the named file's field caps, not a complete plan approval, canonical-change check or evidence of passing later stations. Files without a `charter:` frontmatter key bypass these caps; charter 1.1 or later additionally checks the Simplicity check record. Empty content may pass the existing check; do not invent stronger validation.
- agent-decided — Document `intake <write-spec|write-plan> <change-id>` as a check of that station's current prerequisites in the selected repository. A successful check does not authorize publication, perform the station or establish final verification. The change ID is an identifier, not a file path.
- agent-decided — Preserve intake's existing conditional stdout: after confirmation checks pass, engineering intents and needs-design=yes write-plan intake (unless spec is skipped) print the existing `interface-surfaces (<source>): <globs> (non-code paths under **/templates/** excluded)` diagnostic. It may precede either success or a later BLOCK and is advisory, not a result. Other intake paths emit no stdout payload; preserve both variants byte-for-byte.
- agent-decided — Document `reviewer-count <change-id>` as requiring a clean repository and committed functional content. Its stdout is the required reviewer floor, not a review verdict; policy can conservatively return two when the delta is unreadable. Do not claim this handler validates change-ID grammar beyond its current nonblank operand requirement.
- agent-decided — Existing normal failures keep their original diagnostic and status; add only the help hint. Internal exceptions retain the existing internal-error path without an additional hint. No progress heartbeat, JSON envelope, automatic repair or retry is added. These local checks have no durable running state to resume.
- agent-decided — Mechanism budget: zero new dispatch or validation mechanisms; reuse the existing help-only early return and hint mechanism, with regression coverage for the three added command entries. Handler logic and rule populations stay unchanged.
- agent-decided — Independent acceptance uses a clean committed real change and its retained artifacts; a first-use operator discovers the commands and prepares calls from bundled guidance, without fabricated verdicts. Controlled negative cases supplement this execution rather than replace it.

## Alternatives considered

- Cover every remaining command now: rejected because write, cleanup and host-hook commands have different authorization and side-effect boundaries and exceed the requested incremental change.
- Introduce structured errors or a generic CLI framework: rejected because neither is needed for consistent discovery, and both expand compatibility and migration obligations.
- Documentation-only instructions outside the tool: rejected because the confirmed gap includes the tool's own discoverability and failure response.
- Include `sync-trunk` or `land` in this batch: deferred because they mutate repository or remote state; the selected read-only batch tests the shared pattern with a smaller blast radius.

## Current state evidence

- Forward: `loom-code/scripts/loom_checker.py:219` (`COMMANDS`) exposes the three handlers; `main` currently intercepts exact help only for the existing `COMMAND_HELP` entries.
- Reverse: `loom-code/skills/closing-review/SKILL.md:136` calls `reviewer-count`; `loom-code/scripts/loom_checker/command_handlers/plan.py:12` records the direct-path check used by planning and publication callers; `loom-code/scripts/loom_checker/command_handlers/intake.py:28` receives station and change-ID calls.
- Error: `loom-code/scripts/loom_checker/command_handlers/plan.py:19` rejects missing paths and reports unreadable files; `command_handlers/intake.py:29` rejects missing or invalid station/ID input; `command_handlers/reviewer_count.py:15` rejects missing operands and dirty trees. `loom-code/scripts/loom_checker/helpers.py:41` prints `BLOCK <rule>: <reason>` and returns 1 for reported check failures.
- Data: `loom-code/scripts/loom_checker/command_handlers/plan.py:23` reads a file path; `command_handlers/intake.py:44` loads canonical artifacts through the manifest; `loom-code/scripts/loom_checker/reviewers.py:511` computes an integer floor from committed branch evidence.
- Boundary: `loom-code/scripts/loom_checker.py:241` owns help hints and `main`'s exact-help interception. `loom-code/tests/test_loom_checker_cli.py:145` already checks reviewer-count success and dirty-tree refusal. This change leaves handlers, rule computation, hook behavior and remote operations outside its functional edits.

## UI flows

The same cases apply to both long and short exact help forms. Checks run synchronously; no new in-progress output is introduced. Every normal invocation revalidates its current inputs; help preserves repository and file state.

| Case | What the operator does | What they see |
|---|---|---|
| Help success | Runs `plan --help`, `intake --help` or `reviewer-count --help`, even outside a repository | Purpose, usage, prerequisites, limited outcomes and recovery on stdout; help-only notice; exit 0. No check runs. |
| Empty invocation | Runs a covered command with no operands | Existing `plan needs a path.`, `intake needs a station and a change-id.` or `reviewer-count needs one change-id.` on stderr, followed by that command's help hint; exit 2. Read the help and supply the required operands. |
| Invalid help shape | Adds operands after a help token | Existing handler validation rejects the invocation; stderr gains the matching help hint; nonzero status remains unchanged. Correct to the exact help form. |
| Plan success | Runs `plan <path>` on a readable file with no field-cap violations | No success payload; exit 0. Only the named file's implemented field-cap rules passed. An empty file is not thereby an approved plan. |
| Plan missing/unreadable file | Runs `plan <path>` for unavailable content | Existing `no such plan file: <path>` or `cannot read plan file <path>: <reason>` on stderr and help hint; exit 2. Correct the path or read access, then retry. |
| Plan blocked | Checks a file that exceeds a field cap | Existing `BLOCK plan.field-caps: <reason>` and help hint on stderr; exit 1. Correct the reported field and rerun the check. |
| Intake success | Runs `intake write-spec <change-id>` or `intake write-plan <change-id>` with the applicable prerequisites satisfied | Exit 0. Engineering intents and applicable needs-design=yes write-plan intake retain the existing `interface-surfaces (...)` stdout diagnostic; other paths have no stdout payload. That diagnostic is advisory; the exit status establishes that the selected intake passed, not that the station ran or verification completed. |
| Intake invalid inputs | Supplies an unsupported station, malformed ID or extra operand | Existing `unknown station ...`, `... is not a change-id; expected ...` or `unexpected argument ...` diagnostic and help hint on stderr; exit 2. Read the accepted station/ID form and correct the call. |
| Intake blocked | Runs intake with missing or inconsistent required artifacts | Existing `BLOCK <rule>: <reason>` lines and help hint on stderr; exit 1. A later failure may follow the existing conditional `interface-surfaces (...)` stdout diagnostic; early confirmation failure returns before it. The diagnostic does not override the failure. Supply or correct authentic required artifacts through their owning workflow, then rerun. |
| Reviewer floor success | Runs `reviewer-count <change-id>` on clean committed content | Existing integer floor and newline on stdout; exit 0. Obtain that many independent reviewers; this output is not a passing review. |
| Dirty repository | Requests the reviewer floor before committing attributable changes | Existing `reviewer-count needs a clean tree with completed functional content.` and help hint on stderr; exit 2. Preserve work, complete and commit the change before checking again. |
| Outside a repository | Runs `intake` or `reviewer-count` outside a Git work tree | Existing `<path> is not inside a git work tree.` diagnostic and matching help hint on stderr; exit 2. Run inside the intended repository and retry; the failed invocation establishes no readiness. |
| Internal failure | Encounters an actual unexpected exception during a covered command | Existing `loom_checker internal error: <type>: <reason>` diagnostic and exit 2; no new failure hint. Resolve the reported internal/environment failure before retrying; do not infer success or authorization. |
| Redirected output | Captures stdout and stderr separately | Successful normal output remains byte-compatible; help is stdout, diagnostics and appended hints are stderr. Inspect the exit status as well as output. |

Recovery returns to the same command with corrected inputs; no previous successful check waives revalidation. The operator may abandon a failed call without losing artifacts. No operation introduced by this change rewrites, deletes or sends existing user data.
