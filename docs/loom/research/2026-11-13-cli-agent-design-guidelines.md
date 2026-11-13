---
title: "CLI and agent-operated CLI design guidance for Loom"
type: loom-research
status: concluded
created: 2026-11-13
updated: 2026-11-13
tags:
  - loom/research
---

# CLI and agent-operated CLI design guidance for Loom

## Question and scope

Which external CLI conventions should inform Loom's common machine-readable
contract, and what is the smallest useful next change? This follows the
[research scoping assessment](2026-11-13-cli-design-research-scope.md) and informs
the still-open [result-contract intent](../intent/2026-11-13-cli-result-contract.md).
This is research, not a ratified interface specification or implementation.

Local baseline: merged commit `fbdc29af358413bc9d55b599231b2a6cbcb4524d`,
loom-code 3.72.0, inspected in `/private/tmp/loom-pr149-land` and the installed
3.72.0 cache. Preserve existing text, preparation JSON v1, delivery JSON,
authorization and hook contracts. No source edits or remote writes were made.

## Method and rationale

Use a lightweight trade study supported by targeted source inspection and
eight local read-only discovery/error probes. Compare a universal JSON retrofit,
documented result families with staged adoption, and retaining current outputs.
Relevant criteria: discoverability, deterministic consumption, compatibility,
correct lifecycle interpretation, write/retry safety and maintenance cost.

English/Japanese searches located primary documentation and community proposals.
Read authoritative/project-authored sources, then trace selected implementation
paths where documentation alone could mislead. No source quota or popularity
ranking was used. Stop after identifying applicable rules, exceptions and a
first batch; no new agent-performance benchmark was needed.

## Findings

### Evidence strength and disagreements

| Source | Evidence actually inspected | What it establishes and what it does not |
|---|---|---|
| [CLIG](https://clig.dev/) | Practitioner-authored guidance: help, streams, errors, noninteractive operation, subcommands and compatibility | A useful human-oriented baseline; not a formal universal standard or agent-performance experiment |
| [gh formatting](https://cli.github.com/manual/gh_help_formatting), [exit codes](https://cli.github.com/manual/gh_help_exit-codes) | Official manuals plus exporter and PR-view source at pinned commit below | A concrete optional export design; not a requirement to copy its parser, field selector or numeric exits |
| [AWS output formats](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html) | Official documentation | Multiple formats, JSON default and format-dependent query/pagination semantics; documentation-only, no AWS execution |
| [gws](https://github.com/googleworkspace/cli) | Project documentation plus pinned main, executor, schema and error/output paths | Concrete agent-oriented discovery/output and request-preview design; not an officially supported Google product or universal model |
| [Agent-First CLI](https://agentfirstcli.github.io/), [about](https://agentfirstcli.github.io/about/) | Community principle index and author/provenance page | Useful hypotheses on progress, partial failures, discovery and schema stability; adoption or effectiveness not established |
| Loom pilot | Existing actual R1/R2 comparison and acceptance artifacts | Local compatibility and small-sample observations, not general JSON superiority |

CLIG recommends clear help, explicit script-oriented output, proper stream
separation, noninteractive inputs and compatible evolution. It explicitly
prioritizes human readability. Its recommendations are a baseline to adapt,
not authority to change Loom's published behavior.

The external examples do not converge on one flag meaning or result envelope.
For example, gh uses `--json` to select exported response fields; gws uses
`--json` for request bodies and has separate formatting controls. Consistency
must be defined within Loom, with explicit exceptions, rather than inferred
from a familiar flag spelling.

### Source-traced external examples

**gh** at `3d5a9e355a837f2f5ee78d7484c118cc1342ad1a`:
[JSON flags/exporter](https://github.com/cli/cli/blob/3d5a9e355a837f2f5ee78d7484c118cc1342ad1a/pkg/cmdutil/json_flags.go)
and [PR view](https://github.com/cli/cli/blob/3d5a9e355a837f2f5ee78d7484c118cc1342ad1a/pkg/cmd/pr/view/view.go).
`NewCmdView` registers supported fields with `AddJSONFlags`; `viewRun` uses
the requested fields and invokes the exporter. The exporter serializes data
to `IOStreams.Out`, with optional jq/template processing. This is a traced
data-export path, not parsing terminal prose. Unknown fields are rejected with
available fields. No gh binary was built or invoked for this research.

**gws** at `cd3697e07eb520056dcf142d0c7439bbb9ba32e9`:
[main](https://github.com/googleworkspace/cli/blob/cd3697e07eb520056dcf142d0c7439bbb9ba32e9/crates/google-workspace-cli/src/main.rs),
[executor](https://github.com/googleworkspace/cli/blob/cd3697e07eb520056dcf142d0c7439bbb9ba32e9/crates/google-workspace-cli/src/executor.rs),
[schema](https://github.com/googleworkspace/cli/blob/cd3697e07eb520056dcf142d0c7439bbb9ba32e9/crates/google-workspace-cli/src/schema.rs),
[error](https://github.com/googleworkspace/cli/blob/cd3697e07eb520056dcf142d0c7439bbb9ba32e9/crates/google-workspace-cli/src/error.rs).
Main dispatches schema lookup and passes parsed arguments to the executor.
The executor validates inputs and returns a preview on dry-run before its API
request loop. Main can still process discovery/authentication first: preview
is not proof of offline execution. Main's error path emits JSON through the
error formatter; that formatter also emits human stderr. No build, login or
API call was performed. Its architecture document had stale crate paths;
actual paths above were verified in the source checkout.

### Loom inventory: all sixteen principal subcommands

Paths below are relative to `loom-code/scripts/loom_checker/command_handlers/`.
Each row's `cmd_*` function was read; selected nested paths are identified
where they change side effects or completion meaning. Generic exceptions and
usage errors also pass through `loom_checker.py::main`.

| Command / source anchor | Existing result | Effects / completion caveat | JSON / dedicated exact help |
|---|---|---|---|
| `intent` — `intent.py::cmd_intent` | Rule diagnostics; conditional stdout advisories | Reads artifacts/Git; a valid intent is not delivery | No / No |
| `intents` — `intents.py::cmd_intents` | Tab-separated ID/state/optional metadata; indeterminate can exit 1 | Reads local repository/default-ref evidence; not a live-server freshness guarantee | No / No |
| `intake` — `intake.py::cmd_intake` | Checks selected prerequisites; conditional notices | Local read; partial station checks do not establish full verification | Preparation v1 / Yes |
| `plan` — `plan.py::cmd_plan` | Field-cap diagnostics or empty successful text | Local read of supplied file; not a full semantic plan review | Preparation v1 / Yes |
| `standing` — `standing.py::cmd_standing` | Warnings plus blocking checks | Local read; warnings are not failures | No / No |
| `contract` — `contract.py::cmd_contract` | Current/required contract text or BLOCK | Local manifest read; not plugin release or runtime readiness | No / No |
| `charter` — `charter.py::cmd_charter` | Markdown table plus rule failures | Local read; table can coexist with failure | No / No |
| `reviewer-count` — `reviewer_count.py::cmd_reviewer_count` | Integer floor | Requires clean repository; count is not completed review | No / Yes |
| `finalize-review` — `finalize.py::cmd_finalize_review`, `_finalize` | stderr progress, diagnostics, final artifact path | Executes declared suite/programs and atomically writes attestation; early stage pass is not final success | No / Yes |
| `sync-trunk` — `sync.py::cmd_sync_trunk` | up-to-date/changed/WARN/BLOCK text | Fetches and may rebase/merge; fetch warning may exit 0 unsynced | No / No |
| `github-rules` — `github_rules.py::cmd_github_rules`, `_probe` | Advisory protection-state/setup text | Network read; unconfirmed is not missing or present; advisory path exits 0 | No / No |
| `pr-floor` — `pr_floor.py::cmd_pr_floor` | CI annotations and verification status | Can append `GITHUB_STEP_SUMMARY`; success may disclose stale verification | No / No |
| `push` — `push.py::cmd_push`, `_native_hooks` | Hook feedback / diagnostics | Hook-install/remove modes create/remove owned hook files, read/refuse core.hooksPath overrides, and report caught native failures as stderr diagnostics with exit 2; hook reminder failures may allow | No / No |
| `publish` — `publish.py::cmd_publish`, `_cmd_publish_trusted`, `_observe_required_ci` | Progress, PR URL, CI result or refusal | Local snapshot + remote push/PR write before CI observation; later failure can follow successful write; no required checks can exit 0 | No / Yes |
| `delivery` — `publish.py::cmd_delivery`, `observe_delivery` | state/reason/next/evidence/complete | Local or remote read; goal defines completion; malformed invocation can remain text even with JSON flag | Delivery object / Yes |
| `land` — `land.py::cmd_land`, `_land_accepted`, `execute_cleanup` | Merge/sync/cleanup messages | Remote merge and branch deletion, local branch/worktree cleanup; merge may succeed before cleanup fails | No / No |

Result: three commands offer opt-in JSON and six have dedicated exact help.
The others are not necessarily defective: CI annotations, hooks and lifecycle
commands have real distinct consumers. `pr-floor` is not strictly read-only
when the summary environment variable is set. `sync-trunk` is a writer despite
its name. Neither belongs in a generic first read-only batch.

### Local execution evidence

Executed installed 3.72.0 through `loom-python --ready`, cwd
`/private/tmp/loom-pr149-land`; exact argv and separated outputs are retained
in the companion [probe record](2026-11-13-cli-agent-design-probes.json).

| Probe | Actual exit / observation |
|---|---|
| overall help | 0; command inventory |
| plan help | 0; dedicated guidance plus JSON description |
| intake help | 0; dedicated guidance plus JSON description |
| contract help | 2; unexpected `--help` |
| charter help | 2; unexpected `--help` |
| reviewer-count help | 0; dedicated guidance |
| plan JSON with missing operand | 2; valid preparation JSON usage error |
| intake JSON with missing operands | 2; valid preparation JSON usage error |

These probes do not claim all sixteen normal/error paths were executed.
No publishing, merge, cleanup, network probe or environment repair was run.

### Adopt, adapt, defer or reject

The following are research recommendations, not already-enforced rules.

| Decision | Proposed Loom rule / rationale | Concrete validation scenario |
|---|---|---|
| Adopt | Every public command exposes side-effect-free exact help; inventory declares actual capabilities and exceptions | All command help forms offline return guidance without dispatching a mutating handler |
| Adopt | Machine mode has deterministic parseable stdout; diagnostics/notices/data are distinct | Parse the complete stdout for passed/blocked/usage/internal cases; inject a late exception after a notice |
| Adapt | Share common meanings, retain command-specific typed payloads | Contract version pair and reviewer integer remain directly available without prose parsing |
| Adopt | Preserve published modes and numbers; explicit schema/version changes for incompatible additions | Baseline byte-parity text cases and old JSON consumers continue working |
| Adapt | Process exit and observed domain outcome are separate concepts | github-rules returns process success while result is unconfirmed; no false completion |
| Adopt | Discovery describes operands, modes, preconditions and result scope before expensive execution | Cold operator discovers supported mode; unsupported mode fails before remote writes |
| Adopt | Noninteractive automation must fail clearly on absent inputs and must not consume unrelated stdin | Open pipe never hangs a non-hook command; hook stdin follows its own host contract |
| Adopt | Lifecycle progress does not masquerade as a terminal result | CI pending messages never create completed=true; one final result after process exits |
| Adapt | State write effects and recovery obligations explicitly; observation before a write retry | Push succeeds but CI observation fails; subsequent read-only delivery finds existing PR |
| Defer | Full structured progress/partial-write schemas for write commands | Trigger: an actual structured lifecycle consumer and adversarial partial-success coverage |
| Defer | Universal field filtering, JSONL pagination or dynamic schema registry | Trigger: measured output growth or a concrete consumer needing bounded pages/fields |
| Defer | New short launcher name/default runtime mode | Trigger: separate discovery/cold-start evidence; compatibility and safe hook no-install behavior designed first |
| Reject for now | Automatic JSON switching based solely on TTY or guessed agent identity | Same explicit invocation should not silently change representation across hosts |
| Reject | Global `--yes`/`--force` as a substitute for authorization | Existing intent/maintainer authority remains required despite automation |
| Reject | Claim every command can safely retry, or every dry-run is complete/offline | Local/remote state and side effects must be examined per operation |
| Reject | Treat six preparation fields as a universal envelope by wrapping text | Existing delivery and data-producing commands require real domain data; no stringly typed retrofit |

## Decision impact

**Recommended: semantic consistency with documented result families and staged
adoption.** Keep current text by default and preserve both published JSON
families. Define a compact table of shared meanings (mode, status, error kind,
diagnostics/notices, command data, completion scope, schema compatibility),
not a universal runtime framework or mandatory field list. A parser for error
prose, mass handler rewrite and new dependencies are unnecessary.

First implementation batch: `contract` and `reviewer-count`. They are bounded
local reads, have existing real station consumers, and test a missing dimension
of the pilot: useful command-specific values, rather than only validation
outcomes. Add exact help for contract and preserve reviewer-count help. The
spec must decide compatible result-family/version selection before promising
new fields; do not append undocumented data to preparation v1 or change
delivery's meaning. A precise supported-mode inventory may initially be
documentation generated/checked from existing definitions; it need not be a new
runtime introspection command. Consumer evidence must justify that later.

Next candidates are `intent` and `standing` (mostly validation plus notices),
then charter/intents (tables/lists), with their data and indeterminate-state
semantics specified. CI/hook adapters and writers remain explicitly separate.
Do not delay a bounded correct batch until every writer is redesigned.

| Alternative | Compatibility / burden | Decision |
|---|---|---|
| Keep current interfaces only | Zero new output maintenance; discovery/consumer differences remain | Viable if no automation consumer exists; retain as baseline |
| Common semantics + two read-only data commands | Modest new contract/test surface; exercises real data while preserving legacy modes | Recommended under the requested consistency goal |
| Add JSON to all sixteen immediately | Large lifecycle/hook/CI surface and partial-write recovery obligations | Reject current scope; a matching flag does not establish equivalent guarantees |
| Add a general framework or MCP migration | New maintenance boundary not required by the observed gaps | Defer until concrete consumers demonstrate need |

The prior [pilot comparison](../2026-11-12-cli-json-pilot/evidence/comparison-r2-results.md)
found no operation/recovery benefit and larger check output (4,446 versus
3,074 bytes). Therefore this recommendation is about deterministic integration
and discoverability, not a claim that JSON makes LLMs smarter or cheaper.
Future adoption should use an actual consuming script/agent workflow with
explicit field-based decisions and verify error/compatibility handling.

## Limitations and open questions

- This is not evidence of industry-wide prevalence, certification or universal
  agent-CLI standards. Agent-first proposals are attributed community ideas.
- Upstream source inspection supports the named paths, not full product
  correctness. No upstream tests were run or tools installed/authenticated.
- GNU guideline fetch timed out; POSIX page returned 403. Neither was treated
  as inspected evidence. A missing guessed gws crate path was corrected using
  its actual source tree. Pinned gh raw web fetch was unavailable; a shallow
  source clone verified the exact commit and paths instead.
- No SIGINT, broken-pipe, partial network write or credential-redaction fault
  experiment was run. Such tests become mandatory scope-specific acceptance
  cases if those affected surfaces are changed, not general prerequisites for
  the two-command read-only batch.
- The old draft intent remains open. The user authorized research, not a
  launcher rename, write-command implementation, new paid service or publishing
  this research. Findings should inform a revised specification only after the
  intended implementation scope is confirmed.
