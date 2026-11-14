# CLI compatibility and recovery — replanning proposal

Status: historical recovery-first proposal; implementation scope superseded
by the user's 2026-11-14 selection of interface consistency first. Retained
for provenance. The current intent and spec own the first delivery; automatic
fallback/retry below is not an approved first-batch obligation. This is an intake planning aid,
not the implementation plan or an approved runtime contract. No implementation,
acceptance run, release or publication is claimed by this document.

Scope source: the user selected whole-inventory planning with incremental
delivery, then requested recovery when Loom implementation faults otherwise
interrupt work. The earlier two-consumer-only proposal is superseded in scope;
its still-applicable behavior and evidence remain retained. No formal review
episode has begun for this open change.

## Evidence baseline

Inspected revision: `6fe61c99ea1981f238f8a8550abbd1e36e93cfab`.
`loom-code/scripts/loom_checker.py` owns the sixteen-entry `COMMANDS` mapping,
the exact-help boundary, dispatch and caught exceptions. Its command help is
cross-checked with the handler sources below; help alone is not evidence of
successful recovery. A subcommand and an invocation mode are different units:
all modes must be classified before their batch begins.

Five subcommands currently expose optional JSON. `plan`/`intake` have the
six-field preparation result, `contract`/`reviewer-count` add typed `data`, and
ordinary `delivery` retains its distinct result. Neither this count nor the
presence of JSON establishes complete client validation. Native hook feedback
is a separate host protocol, not another ordinary CLI JSON mode.

## Inventory and proposed delivery grouping

Paths below are relative to `loom-code/scripts/loom_checker/command_handlers/`.
They locate current behavior, not future evidence of implementation.

| Command | Modes and current result | Effects and completion limit | Group |
|---|---|---|---|
| contract | Required-version check; text or optional JSON | Reads bundled manifest; incompatibility is a real rejection | B |
| reviewer-count | One change-id; text integer or optional JSON | Reads clean Git state; two can be conservative, never proof of review | B |
| plan | Named plan file; text or optional JSON | Reads file and checks field caps; passing is not whole-plan approval | C |
| intake | write-spec/write-plan prerequisites; text or optional JSON | Reads artifacts and Git; notices can coexist with rejection | C |
| intent | Named intent, optional commit-message evidence; text | Reads artifact and conditional Git delta; does not confirm intent | C |
| standing | Named intent; warnings and policy checks | Reads standing documents; advisory warnings and real rejection differ | C |
| charter | Bundled or explicit manifest; Markdown table and diagnostics | Reads manifest; may render rows while reporting incomplete charters | C |
| intents | List or selected ID, remote and optional metadata; TSV | Reads local Git only; indeterminate is not live remote failure or freshness | C |
| github-rules | Inspect or print setup; prose | Network reads; exit zero can mean unconfirmed; printing setup does not run it | C |
| delivery | Ordinary observation, goal and optional intent/JSON | Read-only local/live observations; incomplete is not successful delivery | C |
| pr-floor | Body/base/head and optional branch; CI annotations | May append GITHUB_STEP_SUMMARY; body pass is not verification pass | D |
| finalize-review | Review input and change ID; progress and result | Executes supplied qualified checks and writes attestation; not a harmless read retry | D |
| sync-trunk | Synchronize clean change branch; prose/WARN/BLOCK | Fetches and may rebase/merge; exit zero can mean unsynced | D |
| publish | Intent or legacy authorization, title/body; progress and PR | Pushes, creates/reuses Ready PR and observes CI; response loss may follow a write | E |
| land | Accepted merge, named cleanup, sweep with optional confirmation | May fetch/prune even during sweep listing; merge, trunk update and cleanup differ | E |
| push | Host hook, install native hooks, remove native hooks | Hook reads stdin and emits host feedback; native modes change shared Git configuration files | E |

Handler anchors: `contract.py::cmd_contract`,
`reviewer_count.py::cmd_reviewer_count`, `plan.py::cmd_plan`,
`intake.py::cmd_intake`, `intent.py::cmd_intent`, `standing.py::cmd_standing`,
`charter.py::cmd_charter`, `intents.py::cmd_intents`,
`github_rules.py::cmd_github_rules`, `publish.py::cmd_delivery`,
`pr_floor.py::cmd_pr_floor`, `finalize.py::cmd_finalize_review`,
`sync.py::cmd_sync_trunk`, `publish.py::cmd_publish`, `land.py::cmd_land`,
`push.py::cmd_push`.

`delivery --hook` belongs to group E even though ordinary delivery belongs
to C. `--help`, `-h`, launcher readiness/repair and `--list-rules` are cross-cutting
surfaces to retain explicitly; they are not seventeenth ordinary subcommands.

## Proposed common policy

Agent-decided proposals below remain subject to specification and review.

| Observation | Proposed handling | What must remain true |
|---|---|---|
| Supported result with unrelated added fields or changed key order | Consume validated required data and ignore compatible additions | No dependence on prose or exact whole-object key equality in consumers |
| Unknown version, missing required data, wrong type, invalid JSON or contradictory exit/status | Retain raw exit/streams and identify a format/execution fault | Do not use a partial object as a passing observation |
| Qualified read-only invocation with a documented text equivalent | Attempt a bounded, explicitly reported text fallback only for an eligible fault | Same intended predicate, command/version, relevant repository identity and authoritative result; actual rejection remains rejection |
| Text fallback fails or shares the same defective computation | Preserve unknown status, diagnose or repair, and continue independent work | Fallback is an alternative observation, not proof of computational independence |
| Noncritical progress or advisory presentation fails | Continue with a warning when the authoritative operation/result remains available | Lost progress must not fabricate final evidence |
| Completed valid check explicitly rejects | Fix the named condition or investigate a suspected checker defect | No silent reclassification as infrastructure failure or permission bypass |
| Write may have happened but response is unavailable | Inspect authoritative remote/local state before selecting the next action | No blind rerun, duplicate PR/merge, repeated cleanup or alternate publication route |
| No reliable completion evidence | Suspend the dependent operation, preserve work and concrete recovery instructions | No fake success, erased failure evidence or claim the whole session must stop |

Retry eligibility is per mode and observed cause, not a global catch-all.
The specification must name the allowed attempt count, stop condition and
evidence to revalidate for each eligible path. Existing documented one-retry
publication lag handling is retained rather than supplemented with another
generic retry budget. Ineligible writes and ambiguous outcomes default to
observation/reconciliation, not replay. Defaults, cached results or conservative
reviewer counts cannot establish compatibility, authorization or completed work.

Schema validation belongs in deterministic execution where practical. The
agent receives concise field semantics and recovery guidance. A new universal
framework, a second policy evaluator or sixteen separate hand-written schema
copies is not presumed necessary. Discovery and validation should share one
owned definition when the design requires a formal schema; the exact mechanism
is a specification decision, not an intake requirement.

A well-formed but semantically wrong value can pass schema validation. Text
fallback over the same faulty calculation does not detect it either. Tests
must cover selected computational faults and independent authoritative checks
where they exist; arbitrary undetectable implementation errors remain an
explicit limit, not a promised recovery case.

## Proposed batches and completion boundaries

| Batch | Deliverable | Independent acceptance boundary |
|---|---|---|
| A — Whole-inventory contract | Source-grounded inventory, shared compatibility/failure principles, mode exceptions, discovery/version strategy and batch map | All sixteen commands and special modes accounted for; no claim runtime migration is complete |
| B — First real consumers | Existing contract and reviewer-count consumers, necessary validation and bounded read-only recovery | Real installed-path/fresh-copy consumers handle valid, incompatible, malformed and failed results without bypassing policy |
| C — Remaining observation modes | Plan/intake/intent/standing/charter/intents/github-rules/ordinary delivery, including existing contracts | Correct checks, lists, unknown/unconfirmed observations and fallback applicability; no new write path |
| D — Local execution and CI effects | pr-floor, finalize-review and sync-trunk | Faults before/after effects, stable identity, no duplicate execution/summary claims; preserve existing checked guarantees |
| E — Publication, merge and host modes | publish, land, push modes and delivery hook | Authoritative result reconciliation, original consent, host protocol parity and preserved work; no blind write replay |

Batch C depends on A and the verified recovery shape from B. D and E consume
the same ratified definitions and their own effect-specific evidence. These
are proposed reviewable scopes, not a promise to make every command JSON or
to put each group in exactly one PR. Split an oversized group by distinct
effect boundaries without reopening the common policy. Grouping alone does
not authorize concurrent teams, outside-model calls, deployment or plugin
installation.

The specification and implementation plan must assign each release its own
bounded intent/acceptance evidence while referencing the common contract.
An umbrella requirement that is not yet delivered cannot be marked works
because one batch passed. Every executable batch follows test-first Build,
independent adversary and acceptance, closing review, the configured complete
suite, release metadata and CI. This proposal skips none of those steps.

## Fault-oriented acceptance design

Each applicable mode needs independently executed evidence for: normal result;
real business rejection as a negative control; extra fields; unsupported version;
missing/wrong-type data; non-JSON/partial output; startup/dependency failure;
and fallback failure. Modes with effects also cover failure before the effect,
after the effect but before final response, and recovery after restart.

Read-only fallback evidence must demonstrate both successful recovery from an
output-only fault and refusal to proceed when underlying computation is faulty.
Mutation or injected-fault evidence must exercise the real entry/consumer, not
a test that merely asserts a constant or a parallel copy of the intended logic.
No live write, paid model or user-data mutation is implied by test design.
Do not install global exception hooks or alter host trust settings to make
the demonstration pass.

Record tested commit/version, command, raw outputs/exit, validation decision,
fallback/retry attempted, operation identity, observed completion and unverified
boundaries. Keep this in existing evidence artifacts unless an actual consumer
justifies a new persisted format; no recovery daemon or durable retry ledger
is proposed. Expensive actual verification is owned once per required stage,
not repeated by every reviewer.

## Complexity checkpoint

Mindset: Data over abstractions; reuse published structured data and existing
command owners rather than adding a generic workflow engine.

Q1: The smallest end state is one owned compatibility/recovery policy with
mode-specific effects, adopted by existing consumers. A JSON-only migration
does not meet the clarified availability requirement. A global ignore-errors
switch removes safety instead of solving recovery. Text-only fallback cannot
recover shared computation failures or ambiguous writes.

Q2: This replan changes documents only; production Python functions/files remain
unchanged. As an initial estimate, the first executable consumer batch needs
one small validation/recovery owner of roughly 40–80 maintained lines and
40–80 focused verification lines, plus replacement prose/release metadata.
This is not an implementation estimate for all sixteen commands. The actual
shape, delta and any reuse must be recomputed in the plan; no generic schema
dependency, service, configuration matrix or framework is budgeted by default.

Q3: Replace obsolete interpretation instructions and duplicate ad hoc
consumer validation where verified equivalent. No existing production module
is currently proven removable. Retain public text support and host-specific
protocols; they are compatibility obligations, not dead code.

Verdict: PROCEED-WITH-CAVEAT for whole planning plus the bounded first batch.
Recovery adds code and evidence obligations; the explicit benefit is avoiding
unnecessary total-work interruption for covered faults, not proving lower token
cost or immunity to all Loom defects. Later batches need measured task scopes
before implementation.

## Source guidance and limits

- MCP tools output schema: https://modelcontextprotocol.io/specification/2025-11-25/server/tools#output-schema
  supports declared result contracts and client validation; it is not a CLI
  mandate or a guarantee that a host injects the schema into model context.
- Google AIP-180: https://google.aip.dev/180 supports compatible additions and
  preserving existing consumer behavior; API guidance requires adaptation to CLI modes.
- JSON Schema objects: https://json-schema.org/understanding-json-schema/reference/object
  distinguishes required properties, types and additional-property policy.
- Kubernetes webhook failure policy: https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#failure-policy
  distinguishes callback errors from explicit rejection. The split informs
  this proposal; its Ignore policy is not permission to bypass Loom checks.

No external reference proves this proposed Loom implementation works. No
runtime, model-efficiency, live-host-reload or recovery success is claimed.
