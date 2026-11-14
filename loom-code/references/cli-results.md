# CLI result consumption

The first checked consumers let planning establish compatibility and review
obtain its reviewer count from validated fields. This is a two-consumer
migration, not a migration of all sixteen checker commands. Existing direct
text and JSON interfaces remain available.

## Current inventory and delivery order

The command registry and exact per-command help in
[`../scripts/loom_checker.py`](../scripts/loom_checker.py) own operand grammar
and result details. Five commands provide direct JSON; two of those have checked
station consumers. The helper is a script, not a seventeenth checker command.

| Checker command | Current result/modes | Checked station consumer and remaining work |
|---|---|---|
| `intent` | Text checks; optional `--commit-msg` evidence | None; future read-only result design |
| `intents` | Text local-ref states; selected ID and `--metadata` differ | None; future read-only result design |
| `intake` | Text or final `--json` preparation envelope | None; direct JSON exists, consumer migration deferred |
| `push` | Host `--hook` feedback; explicit native hook install/remove modes | None; host protocol and configuration writes stay separate |
| `publish` | Text/progress; authorized remote writes and CI observation | None; future operation-result design must preserve reconciliation |
| `delivery` | Text or `--json` delivery object; separate host hook modes | None; existing observation/reconciliation remains in use |
| `land` | Text/progress; accepted merge, named cleanup, or sweep/confirmation | None; future operation-result design must preserve acceptance and cleanup boundaries |
| `sync-trunk` | Text with WARN/BLOCK; fetch and possible rebase/merge | None; future operation-result design; exit 0 can be unsynced |
| `github-rules` | Advisory text; `--print-setup` prints without executing setup | None; future read-only result design; exit 0 can be unconfirmed |
| `pr-floor` | CI annotations and diagnostics; optional step-summary write | None; future CI result design, retain summary side effect |
| `standing` | Text diagnostics/advisories | None; future read-only result design |
| `contract` | Text or final `--json` preparation envelope plus `data` | Checked compatibility in write-plan, including Codex first contact |
| `charter` | Markdown table plus diagnostics; optional manifest override | None; future read-only result design; table can accompany failure |
| `plan` | Text or final `--json` preparation envelope | None; direct JSON exists, consumer migration deferred |
| `reviewer-count` | Text integer or final `--json` preparation envelope plus `data` | Checked reviewer floor in closing-review |
| `finalize-review` | Text/progress; executes checks and writes attestation | None; future operation-result design must retain evidence verification |

Delivery order is deliberately bounded: this release adopts the two read-only
consumers; later work can design remaining read-only/CI observations, then
operation results around their real completion and recovery needs. No dates or
additional migrations are promised. Help, `--list-rules`, launcher modes and
host hooks are discovery or separate protocols, not extra checker commands.

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
