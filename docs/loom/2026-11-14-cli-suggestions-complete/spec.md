# Complete CLI advisory guidance — spec
intent: 2026-11-14-cli-suggestions-complete@609c81d1e2f03b259090e32a968220aa7b9f8c1f
pre-build-review: required — all-command output contracts include publication, cleanup, advisory exit-zero states and host/CI protocol boundaries

## Requirements

REQ-1 — Complete command coverage
The CLI shall define and exercise advisory behavior for all sixteen registered commands and their applicable modes, explicitly identifying protocol-preserving exceptions without leaving ordinary commands deferred → Acceptance #1

REQ-2 — Outcome-appropriate guidance
WHEN a refusal, error or unresolved outcome needs follow-up, the CLI shall provide consistently labeled, cause-appropriate advice while preserving uncertainty and never deriving completion solely from exit zero → Acceptance #2

REQ-3 — Compatible JSON advice
WHERE an existing JSON result is emitted, the CLI shall expose optional suggested_next advice consistently across all five JSON commands, preserve existing required and legacy next fields, and use the same advice value for its corresponding text result → Acceptance #3

REQ-4 — Advisory content is not authority
WHEN advice is present, absent, unusable or cannot be written, the CLI shall retain original result classification, exits, policy and authorization without executing suggestions, retrying, falling back or bypassing trust and reconciliation → Acceptance #4

REQ-5 — Protocol and data preservation
WHEN help, progress, hooks, CI, setup or cleanup handoffs are used, the CLI shall preserve their existing protocol and purpose without introducing new user-data mutation from advisory guidance → Acceptance #5

REQ-6 — Independent all-command evidence
WHEN the completed guidance is documented and independently exercised, every applicable normal, negative and special-mode surface shall have traceable evidence, with simulation and untested live-host/remote boundaries explicitly disclosed → Acceptance #6

## Design decision

- user-decided — One complete delivery covers all sixteen commands, replacing the proposed two-command continuation. The confirmed scope says: "這次『全部』指建議介面涵蓋全部命令；原先沒有 JSON 的命令維持文字輸出。" It includes existing five JSON commands, not new JSON modes or a universal envelope.
- user-decided — Keep exact `Suggested next step:` and `suggested_next` naming. Existing `delivery.next` remains compatible; existing required cleanup/cwd handoff data is not downgraded to optional advice.
- agent-decided — Extend existing `preparation_output.py` advice generation and add one small best-effort text emitter, used by main and semantic outcome owners. No new source module, dispatcher, executor, per-error parser or dependency is required. Command-specific guidance is bounded data about current commands, not a second domain policy evaluator.
- agent-decided — Ordinary text advice is emitted on stderr using the exact label. Preserve original diagnostics, successful data stdout, Help hints, tables, tabular metadata and operation receipts. Existing rich inline `next:` remedies may remain within original diagnostics for compatibility; the canonical advice entry points to the specific reported condition and does not contradict that remedy. The GitHub rules human report keeps its existing stdout report location while adopting the canonical label; its setup-script mode is separate.
- agent-decided — The dispatcher provides common ordinary refusal/usage/internal-error advice only for registered commands, with global help advice for empty/unknown invocations. Do not reflect arbitrary command strings into runnable commands. A returned error code alone is not asserted to mean an internal exception: preserve known plan returned-usage behavior and use neutral advice where classification is unavailable. Typed preparation errors retain their original error.kind.
- agent-decided — Keep JSON schema_version 1 for the four existing preparation/read-only commands, adding suggested_next to plan/intake as an additive extension. New passed results carry null; blocked/error results carry nonblank English advice. Preserve diagnostics ordering, notices even on late error, typed data for contract/reviewer-count, selectors and single execution. Error advice must not depend on parsing human messages.
- agent-decided — Ordinary delivery JSON retains state/reason/next/evidence/complete and adds suggested_next with the same value as next. Do not add a schema version, status or common envelope to delivery. Ordinary text retains its existing state and legacy next line, and also exposes that same advice with the canonical label on stderr. Suppress any duplicate dispatcher advice for already-rendered delivery observations. Preserve existing delivery Help behavior and its pre-result usage/startup boundaries; no universal JSON-on-every-failure guarantee is introduced.
- agent-decided — Core result validation is unchanged. Missing/null/blank/non-string advice never changes a valid observation; checked_readonly still supports only contract/reviewer-count, preserves accepted raw JSON and numeric precision, and does not become an all-command validator. After core acceptance, clients may display a nonblank advice string; they never execute it or infer authority from it.
- agent-decided — Error advice is grounded in command purpose and original diagnostics: restore named intent/plan/intake/charter prerequisites through their owners; obtain missing human confirmation instead of forging records; preserve work and existing hook ownership; use existing publication/cleanup routes and delivery reconciliation after ambiguous remote effects. Preserve the established producer-versus-consumer contract update distinction. Unknown internal errors ask for investigation without claiming a repair or transient cause.
- agent-decided — State-sensitive exit-zero advice is generated where facts exist, not by scanning stdout. A sync fetch warning remains exit zero and explicitly unsynced; GitHub rule uncertainty remains unconfirmed and cannot authorize setup; standing warnings remain nonblocking; absent/stale PR verification remains a notice rather than a PR-floor failure. Each adds or normalizes advice without changing its result meaning.
- agent-decided — Useful ordinary success follow-up is permitted, such as reviewing publication evidence and awaiting acceptance or committing generated verification before authorized publication. Do not manufacture advice for successful checks, empty listings or unchanged tables. A land sweep with removable entries must emphasize reviewing the list and obtaining approval before using its existing token; no automatic confirmation is added.
- agent-decided — Text advice output is best-effort: an OSError or UnicodeError from writing only the advisory line cannot change the original exit, repeat a mutation or hide the already-produced result. Do not broadly swallow primary result/diagnostic failures, process termination or memory errors. JSON output still has its existing stream-failure limits; adding advice does not guarantee a final object after termination or a broken pipe.
- agent-decided — Native push hook mode, delivery stop-hook mode and mixed/invalid hook invocations preserve existing host payload framing, fail-open/refusal decisions and streams; no ordinary advisory line or CLI alias is injected into those protocols. Existing host-readable message strings and native Git-hook bytes remain unchanged. Native hooks use exact bytes for ownership checks, so rewriting their embedded Next text would make old installations foreign; that is a concrete protocol exception, not unfinished migration.
- agent-decided — Keep github-rules --print-setup output unchanged, with no advisory text inserted into executable setup content. Keep pr-floor annotation escaping, stdout records and step-summary write count/content unchanged; any new normal advice is separate stderr. Keep progress labels/timing/flush and mutation counts unchanged. Preserve literal land next: cd handoff and sweep token/list semantics; never append commands to those records or authorize removal through a suggestion.
- agent-decided — Exact help and --list-rules remain discovery-only with unchanged grammar and no domain execution. Update help/guide to explain field, label, optional consumption and protocol exceptions. Preserve launcher preparation/repair ownership and existing pre-Python remedies: the launcher and standalone dispatch/external-review scripts are not additional registered checker commands.
- agent-decided — Complete the existing CLI inventory as an executable-coverage map, keeping counts distinct: sixteen commands, five existing JSON commands, two checked consumers. Record each command's ordinary/advisory/protocol evidence and permitted exceptions, rather than equating a table row or generic prefix with semantic completion. Runtime prose references portable bundled documentation, not development records.
- agent-decided — Reuse existing public-entry tests and real temporary Git fixtures; exercise remote operations with existing controlled external runners and record that boundary. Independent acceptance runs source CLI in a clean copy, not installed-host parity or unconsented live publish/merge/cleanup on user repositories. No improvement in success rate, time, tokens or cost is inferred. The plan declares the expanded advisory mechanism budget and Build measures actual source/test/prose growth.

## Command and mode obligations

| Command | Ordinary outcome/advice obligation | Preserved mode or boundary | Evidence surface |
|---|---|---|---|
| intent | Valid check needs no invented follow-up; invalid shape/prerequisite points to original diagnostic and owner confirmation | --commit-msg evidence, notices and existing exits | CLI/intent entry tests with valid and refused inputs |
| intents | Keep active/delivered/indeterminate states; indeterminate advice concerns selected remote-default evidence | Empty list, selected ID, --remote, --metadata stdout columns | Real local-ref fixtures and argument errors |
| intake | Passed null; blocked advises restoring named station prerequisites, errors remain usage/internal | Notices survive blockers and late failure, skipped-artifact semantics unchanged | Existing preparation and intake entry cases |
| push | Explicit native install/remove failures gain ordinary advice about ownership/origin without granting installation | --hook payloads and fail-open/refusal behavior, NATIVE_HOOK exact bytes unchanged | Existing hook/native-hook fixtures plus normal usage errors |
| publish | Refusal/error advice preserves precise remedy and reconciliation; completed publication awaits acceptance, not merge | Progress, canonical route, authorization and write/CI-poll counts | Existing controlled Git/gh public-entry scenarios |
| delivery | Same next value in legacy and new JSON keys and text advice; incomplete/unconfirmed never becomes complete | --hook host claude/codex unchanged; pre-result errors stay outside ordinary object guarantee | Delivery state/JSON/text and stop-hook cases |
| land | Refusals preserve accepted/cleanup distinction; sweep list advice requires approval, not token execution | --accepted-by/--cleanup/--sweep/--confirm, literal next: cd, no repeated merge after observed success | Existing merge/cleanup/sweep fixtures and runner counts |
| sync-trunk | Refusal advice preserves work; fetch warning says unsynced even at exit zero | No method switching, rollback/history protections, existing progress/outcome text | Real local Git fixtures and controlled fetch failures |
| github-rules | Missing/unconfirmed rule advice retains admin/read-access requirements; confirmed result needs no filler | --print-setup content unchanged; ordinary human report stays stdout | Ruleset/classic/uncertainty and setup fixtures |
| pr-floor | Malformed body remains failure; absent/stale verification at exit zero gets advice without becoming failure/success proof | Escaped workflow annotations and existing step-summary write unchanged | Existing valid/malformed-body and verification-state entry cases |
| standing | Required-principle refusal remains blocked; emitted warnings remain advisory and get nonblocking guidance | Waiver semantics and verbatim WARN lines, no automatic standing-doc edits | Existing standing command scenarios |
| contract | Existing typed compatibility and indicated-plugin advice preserved | Duplicate/final selectors, original version policy, passed null | Existing real contract and JSON parity cases |
| charter | Preserve table even on failure; advice refers to reported manifest/row issue | --manifest, table cell/order and exits | Existing real/invalid manifest cases |
| plan | Passed null, field-cap refusal and unreadable/missing plan advice match actual category | Literal paths/selectors, JSON/text parity and Help | Existing plan/preparation cases including direct returned usage |
| reviewer-count | Existing floor and input/repository advice preserved, no default floor | Exact request, positive future floor, raw precision and checked faults | Existing checked/read-only and CLI cases |
| finalize-review | Failure advice requires resolving actual evidence; success can suggest committing generated evidence and authorized publication | Package/probe executions, generated attestation, progress and identities unchanged | Existing finalize public-entry fixtures and controlled executions |

## Alternatives considered

- Continue two commands at a time: smaller batches but no longer meets the confirmed single all-command delivery.
- Add only one generic suffix everywhere: misses advisory exit-zero states and can pollute JSON/hooks/setup or repeat hints; semantic owners must handle those cases explicitly.
- Rewrite all outputs as one JSON envelope: changes eleven command interfaces and separate host protocols without authorization or necessity.
- Require advice for every successful output: creates filler and confuses discovery/receipts with recommendations; emit only useful known follow-up.
- Rename/remove delivery.next, native-hook messages or land handoff: breaks existing consumers, exact-byte ownership or required cwd movement; keep compatibility records.
- Parse Next lines or human diagnostics to decide actions: duplicates fragile prose interpretation; select advice from command category and actual owner state.
- Add executable actions, a callback framework, retry logic or a universal result engine: increases policy and mutation paths without serving the advisory-only goal.

## Current state evidence

- Forward: `loom-code/scripts/loom_checker.py :: COMMANDS / main` owns sixteen command dispatch, exact help, four preparation selectors and ordinary exception rendering; `preparation_output.py :: suggested_next` currently handles two commands only.
- Reverse: `loom-code/references/cli-results.md :: Current inventory` and write-plan/closing-review station consumers distinguish sixteen commands, five JSON producers and two checked consumers; hooks call push/delivery modes through their host wrappers.
- Error: `command_handlers/plan.py :: cmd_plan` returns usage code 2 directly on file errors; `sync.py :: cmd_sync_trunk` returns 0 after fetch warning; `github_rules.py :: _probe / _report` reports uncertainty with 0; `pr_floor.py :: cmd_pr_floor` annotates non-valid verification but returns 0.
- Data: `loom-code/scripts/loom_checker/preparation_output.py :: new_result / error_result / report_result` own four envelopes, two currently with advice; `command_handlers/publish.py :: DeliveryResult / cmd_delivery` own legacy next and ordinary JSON serialization; `loom-code/scripts/loom_checker/rule_checks/standing.py :: check_standing_warn` decides whether warning text is emitted.
- Boundary: `command_handlers/push.py :: NATIVE_HOOK / cmd_push / _emit`, `publish.py :: _delivery_stop`, `github_rules.py :: _probe(print_setup=True)`, `pr_floor.py :: _escaped`, and `land.py :: execute_cleanup / _land_sweep` own protocol bytes, framing, annotations and cwd/token handoffs that must survive unchanged.

## UI flows

| Case | Action | Result and next handling |
|---|---|---|
| Discovery | Request exact help or list rules | Existing text/columns and exit 0; help explains advice, no domain action or invented recommendation. |
| Successful ordinary check | Run a valid intent/plan/contract/reviewer/charter check | Existing result/data and exit; no unnecessary follow-up. Existing JSON check success has null advice. |
| Empty listing | List intents with no applicable rows | Existing empty stdout/exit 0, no fabricated intent or publication suggestion. |
| Refusal | Run a check with unmet prerequisites | Same diagnostics and nonzero code plus canonical advice; resolve named facts/confirmation without bypassing the check. |
| Input/file error | Supply invalid operands or unreadable/missing plan | Original usage result and Help plus matching advice; JSON remains its existing error kind, no internal-error guess. |
| Internal error | A command raises unexpectedly | Preserve original error/exit and investigation advice; no invented repair or automatic retry. |
| Unsynced warning | Sync cannot fetch selected trunk evidence | Same warning/exit 0 and explicit unsynced guidance; no claim that trunk was integrated. |
| Rule uncertainty | Probe lacks rule/bypass read access | Same unconfirmed report/exit 0 with suggested access investigation; no assumed protection or setup authority. |
| Standing warning | Optional standing documents are missing without waiver | Same nonblocking WARN lines plus advisory guidance; no automatic file creation or waiver change. |
| Verification notice | PR body is valid but review evidence absent/stale | Same annotation/summary/exit 0 plus separate advice; body success is not functional certification. |
| Delivery | Observe local/published/merged target | Same state/reason/legacy next/evidence/complete and exit, new advice alias; no result changes or mutation. |
| Publish result | Authorized publish finishes or is refused | Same receipts, CI observations and writes; advice requires checking evidence and acceptance, never implicit merge. |
| Cleanup list/handoff | List a sweep or finish accepted cleanup | Existing list/token and literal cwd handoff preserved; suggestion cannot supply approval or repeat a reported merge. |
| Optional/unusable advice | Read an old result or unusable suggestion | Ignore advice after core checks; original diagnostic and classification remain. No execution or fallback. |
| Advice stream failure | Advisory stderr cannot be written | Keep original result/exit and mutation count; no second action to repair an optional message. |
| Protected protocol | Run hook/CI/setup/handoff mode | Same framing/bytes/escaping and ownership; no ordinary prose injected into a machine payload or script. |
| Waiting/cold startup | Existing operation waits or runtime is unavailable | Existing progress/timeouts/startup diagnosis and repair ownership; no new polling, listener or guarantee after termination. |

No advice invokes a command or changes existing data. Repository operations in
tests use isolated fixtures and controlled external responses; real host/model
compliance and unconsented live remote mutations remain unverified. The design
extends the existing API using stable Python data and output operations; no new
external integration is introduced. Actionable-message precedent remains
https://clig.dev/#errors and https://google.aip.dev/193, neither of which proves
causal improvement for Loom agents.
