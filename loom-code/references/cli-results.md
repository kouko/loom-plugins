# CLI result consumption

All sixteen checker commands define advisory next-step behavior. Five expose
direct JSON, and only two have checked station consumers: compatibility in
planning and reviewer count in closing review. Advisory coverage adds no JSON
modes or checked consumers to the other commands.

## Command coverage and executable evidence

The command registry and exact per-command help in
[`../scripts/loom_checker.py`](../scripts/loom_checker.py) own operand grammar
and result details. Five commands provide direct JSON; two of those have checked
station consumers. The helper is a script, not a seventeenth checker command.
The shared [CLI entry checks](../tests/test_loom_checker_cli.py) exercise every
registered command's ordinary result handling, exact discovery, unknown input,
protected-mode suppression and advice-only write failures. The command-specific
checks below exercise actual outcome semantics and protocol boundaries; a
coverage row alone is not a test result. Complete-suite execution and independent
clean-copy acceptance remain separate release evidence.

| Checker command | Advice and preserved modes | Executable evidence |
|---|---|---|
| `intent` | Refusals refer to the artifact owner and authentic confirmation; preserve `--commit-msg` and notices. Passing checks need no filler. | [Intent entry cases](../tests/test_loom_checker_intent.py) |
| `intents` | Indeterminate exit 1 requires remote-default evidence; keep empty lists, selected IDs, `--remote` and `--metadata` columns. | [CLI local-ref cases](../tests/test_loom_checker_cli.py) |
| `intake` | Version-1 JSON or text advice addresses station prerequisites; retain notices and skipped-artifact semantics. | [Intake cases](../tests/test_loom_checker_intake.py), [JSON parity](../tests/test_preparation_json.py) |
| `push` | Ordinary native install/remove errors retain ownership/origin remedies; host `--hook` and installed native-hook bytes stay separate. | [Native ownership](../tests/test_native_git_protection.py), [host framing](../tests/test_hooks_json.py) |
| `publish` | Refusals retain prerequisites and reconciliation; success suggests inspecting evidence and awaiting acceptance. Progress and write/poll counts remain unchanged. | [Controlled publication cases](../tests/test_loom_publish.py) |
| `delivery` | JSON `suggested_next` aliases legacy `next`; text keeps its legacy lines and adds the same advice. Pre-result usage errors retain text diagnostics; incomplete/unconfirmed stays incomplete. | [Delivery states/parity](../tests/test_delivery.py), [Stop protocol](../tests/test_delivery_stop.py), [CLI usage](../tests/test_loom_checker_cli.py) |
| `land` | Refusals preserve accepted-merge versus cleanup remedies; a removable sweep list requests review and approval before token use. Preserve `next: cd`, freshness and no-repeat-merge behavior. | [Merge](../tests/test_land_merge.py), [cleanup](../tests/test_land_cleanup.py), [sweep](../tests/test_land_sweep.py) |
| `sync-trunk` | Fetch WARN remains exit 0 and explicitly unsynced; refusals preserve work and normal Build recovery. No extra fetch or method switch. | [Real temporary Git cases](../tests/test_sync_trunk.py) |
| `github-rules` | Missing/unconfirmed normal reports use the canonical label on stdout without granting admin authorization; confirmed protection needs no filler. Preserve `--print-setup`. | [Read-only probes/setup](../tests/test_github_rules.py) |
| `pr-floor` | Absent/stale verification at exit 0 gets separate stderr advice without becoming a gate; preserve escaped annotations and summary writes. | [CI outcomes/stream faults](../tests/test_pr_floor.py), [workflow](../tests/test_pr_floor_workflow.py) |
| `standing` | Emitted warnings get nonblocking guidance; waivers and principle refusals remain authoritative. No automatic document changes. | [Standing policy cases](../tests/test_loom_checker_standing.py) |
| `contract` | Version-1 JSON plus typed `data`; blocked advice follows the diagnostic's indicated plugin. Checked compatibility in write-plan. | [Compatibility CLI](../tests/test_loom_checker_cli.py), [JSON](../tests/test_preparation_json.py), [consumer](../tests/test_checked_readonly.py) |
| `charter` | Refusal advice refers to the reported manifest/row; preserve Markdown table output, row order and `--manifest`. | [Charter cases](../tests/test_contract_charter.py) |
| `plan` | Version-1 JSON or text; missing/unreadable-file errors keep usage advice matching JSON, not an asserted internal failure. | [Field caps](../tests/test_plan_field_caps.py), [JSON parity](../tests/test_preparation_json.py) |
| `reviewer-count` | Version-1 JSON plus typed `data`, or text integer; errors preserve the real floor policy without a default. Checked in closing-review. | [JSON](../tests/test_preparation_json.py), [consumer boundaries](../tests/test_checked_readonly.py) |
| `finalize-review` | Refusals require authentic evidence through its owner; success suggests committing generated evidence before authorized publication. Preserve execution/progress/attestation rules. | [CLI failures](../tests/test_loom_checker_cli.py), [finalization](../tests/test_probe_confirmation_finalize.py) |

Help, `--list-rules`, launcher modes, standalone dispatch scripts and host hooks
are discovery or separate protocols, not extra checker commands. The remaining
eleven commands retain text interfaces; this change adds no JSON mode.

## Common consumption principles

- Read the actual process exit, result fields and diagnostics together. An exit
  0 can be advisory for some commands; a URL, progress line, table, JSON object
  or notice alone does not prove completion.
- Validate supported versions, identity, required fields/types and exit/result
  consistency before using an observation. Permit compatible unknown fields;
  avoid exact prose, key-order or a second copy of domain policy.
- Distinguish explicit refusal, invalid/unknown observations, usage/internal
  failures and startup failures. Stop the dependent action when its prerequisite
  is unestablished; do not invent success, a reviewer default or text fallback.
- Preserve each command's authorization, host trust and recovery behavior.
  For an ambiguous remote write, use the existing delivery observation before
  considering another write. Observation never authorizes publication or merge.

## Suggested next steps

Structured result facts determine whether a prerequisite is established;
`suggested_next` is prose inside a JSON string, not a machine decision or an
executable action. The four version-1 producers (`plan`, `intake`, `contract`,
`reviewer-count`) emit a nonblank English string for blocked/error results and
null for passed results. `contract`/`reviewer-count` additionally retain typed
`data`. `delivery` retains its distinct five legacy fields and adds
`suggested_next` equal to `next`; it has no preparation envelope or new schema
version. Ordinary delivery text keeps its original state/next lines and emits
that same advice on stderr. Existing delivery Help/error stderr and pre-result
text failures remain possible even with `--json`; do not generalize the four
envelopes' empty-checker-stderr contract to delivery.

Ordinary text refusals/errors use `Suggested next step:` on stderr while
retaining diagnostics and existing Help hints. Useful success follow-up is
allowed, such as committing generated verification or awaiting acceptance after
publication. Successful checks and empty lists need no invented follow-up.
State owners retain uncertainty at exit zero: a fetch failure is unsynced,
unreadable GitHub protection is unconfirmed, standing WARNs are nonblocking and
absent/stale PR verification is a notice, not a new body-floor failure. GitHub
rules' normal human report keeps its existing stdout location.

After accepting the core observation, read `suggested_next` only when it is a
string whose trimmed value is nonblank. Present applicable advice as advisory
content alongside the original diagnostic. Ignore missing, null, blank or
non-string advice and retain the original diagnostic. Those states never alter
core validity or classification. The consumer preserves accepted raw JSON,
including unusable advice and compatible numeric extensions; accepting core
fields does not make arbitrary advice trustworthy or executable.

Advice never grants authorization to continue, publish, merge or bypass host
trust. Its presence, absence or contents must not trigger automatic execution,
retry or text fallback. An unknown observation cannot establish a prerequisite
through its suggestion. Absence of a useful suggestion is a valid state.

Text advice is best-effort: an OSError or UnicodeError while writing only the
advisory line cannot change the original result/exit or repeat an operation.
Primary output/diagnostic failures, JSON stream failures, process termination
and pre-Python startup retain their existing limits. The shared formatter is
standard-library-only, preserving checked-readonly's standalone help/startup
boundary without importing the checker's PyYAML dependency.

For contract refusals, follow the actual diagnostic's indicated plugin: either
the consuming plugin or loom-code can be outdated. Usage advice directs input
or repository investigation while preserving work; it does not authorize
discarding work, automatically committing unrelated changes or lowering the
reviewer floor. Internal-error advice retains uncertainty and asks for
investigation rather than inventing a repair or claiming a transient failure.
Local consumer faults retain their own diagnostic and append locally generated
`Suggested next step:` advice for input correction, runtime investigation or
output-contract investigation. Never derive recovery commands from malformed
child stdout or unexpected stderr. Existing launcher readiness/repair ownership
and remote-operation reconciliation remain in force. No improvement in agent
resolution rate, time, tokens or cost has been measured.

## Preserved protocol boundaries

| Surface | Preservation rule and executable checks |
|---|---|
| Exact help and `--list-rules` | Discovery performs no handler work; no suggestion is manufactured. [CLI](../tests/test_loom_checker_cli.py), [runtime isolation](../tests/test_loom_python_runtime.py). |
| Push and delivery hooks | Keep host payload framing, streams and fail-open/refusal decisions, including mixed/invalid hook forms; ordinary CLI advice and aliases are excluded. [Host payloads](../tests/test_hooks_json.py), [Stop](../tests/test_delivery_stop.py), [dispatcher](../tests/test_loom_checker_cli.py). |
| Installed native Git hooks | Keep exact embedded bytes, including legacy Next text: ownership checks compare bytes, so changing that text would make existing installations foreign. [Native ownership](../tests/test_native_git_protection.py). |
| `github-rules --print-setup` | Keep executable setup content and existing failure/template output unchanged; no new advice is inserted. Printing setup never authorizes applying it. [Setup/probe cases](../tests/test_github_rules.py). |
| PR-floor CI | Keep stdout annotation escaping and existing step-summary contents/write count; added advice is separate stderr. [CI cases](../tests/test_pr_floor.py). |
| Land cleanup and sweep | Keep the mandatory literal `next: cd` handoff and stdout list/token; advice does not supply approval or repeat an accepted merge. [Sweep](../tests/test_land_sweep.py), [merge](../tests/test_land_merge.py), [cleanup](../tests/test_land_cleanup.py). |
| Progress and launcher readiness | Keep existing cadence, flush, polling and mutation counts. Launcher repair/startup messages and standalone tools are separate interfaces. [Publication](../tests/test_loom_publish.py), [runtime](../tests/test_loom_python_runtime.py). |

Remote-operation tests use controlled Git/gh responses and temporary repositories;
the GitHub-rules server-enforcement case is a local simulation. These checks do
not establish installed-host/model compliance, live GitHub enforcement or
unconsented publication/merge/cleanup on user repositories. Independent acceptance
and full release checks are reported separately, not inferred from this map.

## Checked read-only calls

Replace `<loom-code>` with the installed plugin directory. Planning may prepare
the plugin runtime; subsequent calls reuse it. The consumer itself neither
installs runtime nor writes artifacts.

```sh
"<loom-code>/scripts/loom-python" --repair --script checked_readonly.py contract --require 2.1
"<loom-code>/scripts/loom-python" --ready --script checked_readonly.py reviewer-count <change-id>
"<loom-code>/scripts/loom-python" --ready --script checked_readonly.py --help
```

The [consumer](../scripts/checked_readonly.py) accepts only `contract` and
`reviewer-count`, forwards operands unchanged and adds the final `--json`.
Supplying `--json` yourself is a usage error. Exact script `--help`/`-h` runs no
checker; command-specific help remains the direct checker's exact
`<command> --help` form. Unknown commands and empty invocations run no checker.

Accepted output is one JSON object plus newline with empty consumer stderr.
Outer whitespace is normalized; unknown fields and numeric precision are
preserved. The validated envelope requires integer `schema_version: 1`, the
requested `command`, `status`, `diagnostics`, `notices`, `error` and `data`.
Diagnostics contain nonblank string `rule_id` and string `message`; notices
are strings. Duplicate keys at any depth, NaN/Infinity literals, trailing
objects, missing/wrong fields, request mismatches and contradictory states fail.

| Accepted state | Exit | Required interpretation |
|---|---|---|
| `passed` | 0 | Empty diagnostics and null error; use the command's validated data |
| `blocked` | 1 | Nonempty diagnostics and null error; no dependent continuation |
| `error` | 2 | Empty diagnostics, `error.kind: usage|internal` and string message; known data fields are null |

Contract passed/blocked data contains nonblank `contract_version` and
`required_version` strings and boolean `compatible`. The required version
matches the final supplied `--require` operand exactly; passed requires true,
blocked requires false. Planning continues only on passed/true. Only an
accepted `contract.requires` diagnostic establishes its outdated-contract
response; other failures retain their own diagnostics. The consumer does not
recompute compatibility or compare a separate manifest.
For that response, report the diagnostic and stop; identify the plugin it
names rather than always prescribing a loom-code update.

Reviewer data contains the unchanged requested `change_id` and a positive
integer `reviewer_floor` (a boolean is invalid). Only passed is usable; there
is no blocked reviewer result. The current producer returns one or two, while
a future larger positive floor is conservatively accepted. It specifies how
many distinct independent reviewers to dispatch, not a verdict or completed
review. Errors and invalid observations dispatch nobody and supply no default.
The checker still recomputes reviewer policy during finalization.

Malformed/mismatched output or unexpected child stderr yields empty stdout,
a `checked-readonly:` stderr diagnostic and exit 2. Child startup and timeout
failures also exit 2; an observed child runtime exit 86 is retained. The child
uses the current interpreter with Python import isolation and a configured
30-second subprocess timeout, one argument-list execution, no shell, retry or
fallback. The outer launcher owns readiness/repair: ready mode can exit 86
before the script starts, and repair may write caches/use network. Termination
and broken pipes can prevent a final result. The timeout is not a promise of
an absolute wall-clock limit including process creation.

For a prepared runtime, `contract --require 2.1` passes, `--require 2.99`
blocks, and `--require bad` produces a valid usage error through this helper.
Run reviewer-count inside the selected clean repository after committing
functional work; a dirty or missing repository yields a valid usage error.
Correct the named condition before a deliberate rerun. Structural validation
does not prove computational truth, arbitrary recovery, installed-host parity,
or reduced time, tokens or cost.
