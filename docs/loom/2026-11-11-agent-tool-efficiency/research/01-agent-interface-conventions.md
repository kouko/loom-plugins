---
title: "Selecting consistent agent-facing tool conventions for Loom"
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
change: 2026-11-11-agent-tool-efficiency
tags:
  - loom/research
---

# Selecting consistent agent-facing tool conventions for Loom

## Question and scope

Which established practices should guide the agent-facing Python tools before
implementing progress output, eliminating unnecessary collection, and evaluating
review-data conversion? The user requested external research before choosing the
conventions. This record selects a bounded design; it does not implement a CLI
migration or establish a new runtime gate.

Inspected checkout: `91ee36100708f73af5d1df33107dbf98b91ac44f`.
The local `origin/main` reference was `70a05fd73b86c6629a89b816fc45a3ad14a509ed`.
`git diff --stat HEAD origin/main -- loom-code/scripts` returned no differences.
No remote refresh or installed-host parity claim is made.
The existing [intent](../../intent/2026-11-11-agent-tool-efficiency.md) remains the
scope anchor. This is a design input, not a replacement confirmation record.

## Method and rationale

Lightweight trade study plus targeted local call-path inspection. Criteria:
predictable invocation, machine-readable results, understandable failures,
observable waiting, safe repeat behavior, compatibility, and implementation cost.
Preserving existing authorization and check decisions is mandatory.

English and Japanese discovery queries were used; primary English documentation
answered the relevant questions. External sources describe documented contracts,
not measured adoption or verified upstream implementations. A fixed MCP revision
(2025-06-18) is used for conceptual comparison; no claim that it is the latest
protocol or that Loom implements it. No package installation or network mutation.

## Evidence

### Established practices

| Source | Supported observation | Applicability and boundary |
|---|---|---|
| [Command Line Interface Guidelines](https://clig.dev/#the-basics), help and output sections | Separate primary output from diagnostics; expose help; use success/failure exit status; avoid terminal animations in redirected output. | A practitioner-authored guide, not a formal universal standard. Its human-first emphasis must be adapted to machine callers. |
| [GitHub CLI formatting](https://cli.github.com/manual/gh_help_formatting) | Some commands offer explicit JSON with selectable fields; ordinary output is text. | Supports selective structured output, not a requirement to wrap every command in one universal object. Documentation inspected, implementation not tested. |
| [gcloud scripting](https://docs.cloud.google.com/sdk/docs/scripting-gcloud) | Automation should use explicit formatting and exit status, not parse diagnostic wording. Nonzero completion can coexist with partial side effects. Prompts can be disabled. | Adopt explicit output and partial-outcome handling. Do not copy automatic default acceptance: Loom's approvals remain separate. |
| [MCP tools, 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) | Tool input schemas and optional output schemas describe data; declared output schemas constrain structured results. Tool failures differ from protocol failures. | Reuse typed contracts and error distinctions. This does not require an MCP server, JSON-RPC transport, or MCP error codes in a CLI. |
| [MCP progress, 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/progress) | Progress is separate from the response, tied to an active request, optionally lacks a total, and stops on completion; rate limiting is recommended. | Reuse separate, bounded progress. Do not invent percentage completion for unknown CI duration or pretend a CLI line is an MCP notification. |
| [Amazon Builders' Library: safe retries](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) | An unanswered request can already have created resources. Safe repeated operations require explicit semantics; AWS describes caller-provided request identifiers and parameter matching. | Require reconciliation after ambiguous mutations. A request identifier alone would not make Loom's Git/GitHub operations atomic or safe. |

### Local observations

Paths below refer to this checkout; line anchors were inspected on the revision
above. Source inspection establishes behavior paths, not a fresh runtime test.

- [Checker entry](../../../../loom-code/scripts/loom_checker.py), lines 97–118:
  top-level help returns zero; command handlers receive output/error streams;
  usage errors and unexpected exceptions both currently return 2. Therefore
  exit 2 alone does **not** distinguish bad input from an internal fault.
- [Shared findings](../../../../loom-code/scripts/loom_checker/helpers.py), lines
  41–44: rule identifiers already accompany failure text; findings return 1.
  Existing stable identifiers should be reused rather than renamed for style.
- [Dispatch CLI](../../../../loom-code/scripts/dispatch_profile.py), lines
  302–311: reads JSON from stdin, returns JSON on stdout, and emits input errors
  to stderr with exit 2. It is already a structured interface.
- [Intake](../../../../loom-code/scripts/loom_checker/command_handlers/intake.py),
  lines 28–44: positional station/change ID parsing; no per-command help branch.
  The top-level help branch does not handle `intake --help` before dispatch.
- [Delivery and publish](../../../../loom-code/scripts/loom_checker/command_handlers/publish.py),
  lines 590–649, 677–711, 925–953, 1035–1038, 1069–1072: delivery already offers
  JSON and text; publish emits text before observing CI; CI polling emits terminal
  outcomes but no pending transitions. Existing PR matching validates repository,
  head and base. This is partial reconciliation evidence, not proof of universal
  retry safety under races or interrupted network requests.
- [Finalization](../../../../loom-code/scripts/loom_checker/command_handlers/finalize.py),
  lines 237–270, 350–369, 454: structured file input is validated; probe subprocess
  output is captured; a final write announces the artifact. Changing only Python
  buffering would not expose captured child output while the child runs.

## Findings and selection

| Alternative | Benefit | Cost or limitation | Decision |
|---|---|---|---|
| Keep current interfaces and add individual progress messages | Smallest code change | Leaves common rules unstated and error interpretation fragmented | Insufficient for the user's priority |
| Apply a small CLI convention set, informed by MCP data/error semantics | Fits existing invocation and supports gradual compatibility | Requires per-command contracts and focused tests | Selected, agent-decided |
| Migrate all tools to an MCP server now | Standardized discovery and transport for MCP clients | Adds server/client lifecycle and host integration work not justified here | Deferred pending an actual host integration need |
| Introduce one new JSON envelope/framework for every command | Uniform syntax | Breaks existing consumers or requires adapters; common syntax does not establish correct semantics | Not selected |

The selected combination uses established CLI channels and explicit machine
output while borrowing useful schema and error distinctions. It is a Loom design
choice, not a claim of industry consensus or formal MCP compliance.

## Proposed minimum conventions

These are proposed requirements for the owning spec. They are not claims of
existing support and do not silently change every command in this change.

1. **Discoverability and input.** Each public agent-facing command documents its
   purpose, operands, example, output, failure behavior and side effects. Help
   must not validate a repository, read stdin indefinitely, or mutate state.
   Simple parameters remain arguments; nested review data remains a JSON file
   or documented stdin JSON. Reject invalid types and ambiguity before mutation;
   explicitly define missing versus null fields. Do not add duplicate input
   methods solely for symmetry. Existing public names remain compatible.
2. **Final results.** Preserve existing machine modes and their shapes. Commands
   needing machine-consumed compound results use an explicit documented mode
   (prefer the existing `--json` spelling when adding one). In that mode stdout
   contains one final JSON value and no progress, ANSI styling, or child logs.
   Known ordinary failures have a documented result/error shape; abrupt process
   death may yield no valid final value, so callers must check both exit status
   and parseability. Define required fields, types, optionality and compatibility
   with an output schema where structured data is added. Do not mandate a new
   global envelope or add duplicate `ok`, `success`, and `status` booleans.
3. **Progress.** Send bounded, newline-terminated stage/wait messages to stderr
   and flush them at emission. Emit stage starts and meaningful transitions;
   report elapsed waiting only at a specified bounded interval if needed.
   Never invent a total or completion percentage. Preserve stdout parsing and
   stop progress on completion. Machine decisions must not depend on wording.
   A machine event stream is deferred until a concrete consumer needs it.
   Captured children require parent stage events or deliberate streaming, not
   just an unbuffered launcher. Host display latency remains a separate test.
4. **Errors and decisions.** Retain existing 0/1/2 meanings and hook-specific
   host behavior. For documented structured modes, distinguish invalid input,
   failed checks, external failure, and internal error through stable identifiers
   and categories. Preserve existing rule IDs. Include an actionable reason and
   relevant evidence, without exposing secrets. A successful observation can
   report an unmet delivery goal; preserve that command's nonzero goal-result
   convention. Do not equate a completed check with a passing check.
5. **Mutation and retries.** Document whether a command is read-only, writes
   locally, or changes remote state. Document whether repeating it is safe and
   under which identity/preconditions. A timeout means outcome unknown unless
   observed otherwise. Preserve any known artifact/PR identity and direct the
   caller to read-only reconciliation before repeating a mutation. A suggested
   retry never grants authorization. Do not add generic automatic retries.
6. **Automation and compatibility.** Automation must not wait for hidden input
   or silently supply authorization. Missing required consent remains blocked.
   Existing text and hook protocols retain their compatibility boundary. A new
   explicit machine mode can define its own contract; changing an existing shape
   requires migration evidence. Additive fields still require consumer checks.

## Decision impact and bounded validation

Write the common rules before progress implementation, then map only the affected
commands to them. Proposed first implementation remains progress in publish and
finalization plus the separately justified collection-order optimization. Help,
new JSON modes and a full error-format migration are an inventory for later
bounded changes unless the owning spec demonstrates they are necessary now.
This separates selecting a target convention from authorizing an all-tool rollout.

For progress, validate that events arrive before child completion, machine output
remains parseable, terminal success/failure is truthful, quiet waits remain
bounded, and failure does not drop existing output or change exit codes. For
future structured interfaces, validate malformed input, missing/null distinctions,
known failures, unknown fields, partial side effects, and compatibility fixtures.
For publish, test ambiguous remote outcomes before promising retry safety.

Measure the review converter only after the selected conventions: compare caller
steps, correctness, error recovery, identity/provenance retention and maintenance
cost on identical cases. Converting YAML to JSON is not itself evidence that a
new tool is valuable. No latency, token, cost or reliability improvement has been
measured in this research.

## Limitations and open questions

- Documentation review and static Loom inspection only; no runtime experiment,
  new tests, external CLI execution, or full command inventory in this pass.
- No upstream implementation audit or claim of the latest MCP version. Revisit
  the protocol version and host capabilities if an MCP integration is selected.
- Existing hook adapters are intentionally outside the generic terminal contract;
  their host-specific exit/JSON semantics must not be globally normalized.
- A structured failure category does not by itself prove that a retry is safe.
- The exact progress cadence and schema for any new machine mode belong in the
  spec with compatibility tests, not in a generic research recommendation.
- Findings are retained in this working tree only; no Python implementation,
  release, publication, installed cache update, or merge was performed.
