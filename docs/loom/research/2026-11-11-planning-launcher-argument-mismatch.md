---
title: "Why planning launcher calls fail with argument mismatches"
type: loom-research
status: concluded
created: 2026-11-11
updated: 2026-11-11
tags:
  - loom/research
---

# Why planning launcher calls fail with argument mismatches

## Question and scope

Determine why an agent can stop before planning because its checker call has
the wrong arguments. Inspect the current checkout at `882d99bf` and installed
Codex loom-code 3.62.2, with a historical loom-code 3.50.0 incident under Claude Code as a
separate observation. The user confirmed the other machine also uses Codex;
its raw command and error are unavailable. Keep repair complexity low and preserve the preceding
skill-lens change as separate work.

## Method and rationale

Hypothesis-driven diagnosis: compare caller misuse, documentation mismatch,
installed-source drift and a failing plan checker. Read the launcher, connected
checker dispatch and plan handler, station examples and relevant runtime tests.
Reproduce only read-only argument and help calls. Stop once the local failure
mechanism is established; do not infer the remote machine's cause.

## Findings

1. **Observed proximate cause:** callers treat `loom-python` as a Python
   interpreter and insert `loom_checker.py`. It is instead a launcher that
   already selects that checker. Before the mode, that path fails launcher
   parsing; after the mode, it reaches the checker as an unknown subcommand.
2. **Repeated observation:** the earlier Claude Code session first omitted
   the mode, then added it while retaining the redundant script path, and
   failed again. The current Codex release implementer made the same insertion;
   removing it let the plan check pass. These are two observed contexts, not
   a measured error rate or proof of the other-machine cause.
3. **Confirmed recovery weakness:** the first error only says to put a mode
   before checker arguments. It does not say that the checker is implicit or
   show a complete valid command. Both launcher `--help` and checker `--help`
   fail with exit 2. The checker's fallback usage prints direct
   `loom_checker.py` commands and omits the supported `plan` and `charter`
   commands. This is an incomplete recovery surface. Its contribution to
   misunderstanding is an inference; it is not proof that documentation caused
   the initial mistake.
4. **Counterevidence:** write-plan's command examples already use the correct
   launcher form. The current implementer says no document supplied its bad
   form; it scheduled reading the launcher and executing the guessed command
   in one batch. Installed and checkout launcher bytes have the same SHA-256.
   A correct plan call returns 0. No local evidence supports a version mismatch
   or a broken plan validator.
5. **Separate validation failure:** a ten-entry plan Files field exceeded its
   eight-entry cap. That returned a named `BLOCK plan.field-caps` with exit 1,
   unlike the exit-2 command-shape failure. Consolidating only the three README
   paths resolved it without changing implementation scope.

## Evidence

Source inspection (paths relative to this record):

- [Launcher](../../../loom-code/scripts/loom-python), lines 10–28 and final
  exec: mode first, default bundled checker, explicit `--script` override.
- [Checker entry](../../../loom-code/scripts/loom_checker.py), docstring and
  `COMMANDS` / `main`: fallback usage, no help handler, supported `plan` and
  `charter` omitted from usage.
- [Plan handler](../../../loom-code/scripts/loom_checker/command_handlers/plan.py):
  one plan file argument; usage errors differ from rule failure.
- [Planning station](../../../loom-code/skills/write-plan/SKILL.md), Workflow
  setup and final plan check examples: correct launcher prefix and arguments.
- [Runtime tests](../../../loom-code/tests/test_loom_python_runtime.py): inspected
  mode/runtime coverage; this investigation does not claim those tests ran.

Measured on installed 3.62.2 from the current project root. `L` below denotes
the installed `scripts/loom-python`, `P` the existing scoped skill-review plan:

| Call | Exit | Observed result |
|---|---:|---|
| `L loom-code/scripts/loom_checker.py --ready plan P` | 2 | use --repair or --ready before checker arguments |
| `L --ready loom-code/scripts/loom_checker.py plan P` | 2 | unknown sub-command for the checker path |
| `L --help` | 2 | use --repair or --ready before checker arguments |
| `L --ready --help` | 2 | unknown sub-command '--help'; fallback usage lacks plan |
| `L --ready plan` | 2 | plan needs a path |
| `L --ready plan P` | 0 | no output |

Launcher SHA-256 (checkout and installed copy):
`2ada1d8b058f33a668017e6d86bea0ef89f980cd1b20c34838fc0c92b72c46f7`.

Private local provenance, intentionally not copied into this repository:
Claude session `32e806fe-4cb1-4476-85bc-5f89cf7d5aaa`, original JSONL lines
107–113, 124–125 and 131–133 were read directly. They contain the failed
commands, mode-only correction, repeated failure and corrected invocation.
Current implementer `/root/scope_release` returned its exact failed/successful
commands and acknowledged the unsupported insertion. The current six-call
capture is retained locally as `launcher-reproduction.json` alongside the
retrospective's temporary evidence; it contains actual argv and output.

## Version provenance

Git history identifies separate introduction points; each version below was
checked against that commit's `loom-code/.claude-plugin/plugin.json`:

- `aab60494e` (2026-10-22, 3.45.0, PR #105): the launcher introduced the mode
  requirement, incomplete bad-mode diagnostic and no top-level help. The
  incomplete publication-hook repair hints date to this change too.
- `2b20d37bf` (2026-11-10, 3.62.0, PR #135): Stop's modeless hint and the
  delivery exception's bare launcher hint were introduced together.
- `b568ba1ae` (2026-09-23, 3.8.0, PR #43): `template_step` already emitted
  bare `loom_checker.py`. This predates the launcher: the historical defect was
  the executable/PATH assumption, not a mismatch with a then-existing launcher.
- `c08b1f425` (2026-09-06, 1.7.0, PR #798 in the predecessor repository):
  `plan` and `charter` were introduced but omitted from `USAGE` at that commit.

The earliest caller misuse observed in this investigation is the historical
loom-code 3.50.0 incident under Claude Code on 2026-10-28, followed by the present
loom-code 3.62.2 incident under Codex. Observation dates do not establish when agents first made this mistake
or prove that the guidance caused it.

## Bounded same-pattern audit during implementation

The follow-up audit searched runtime skill, agent and reference Markdown across
loom-code, loom-design and loom-workflow for `loom-python` and `loom_checker.py`,
then inspected emitted hook and checker recovery hints. Formal station examples
already include a mode and the operation; the host-prefix table is explicitly a
prefix, not a standalone command. No launcher references were found in
loom-design or loom-workflow runtime skills. Helper calls correctly select their
script with `--script`, including dispatch-profile and external-review helpers.
These findings do not establish whether an agent will follow those examples.

The same incomplete-recovery class was present in six hook hints: Claude/Codex
Stop omitted the mode and depended on `loom-python` being on PATH; publication
fallbacks in all four host manifests omitted the original operation and inputs.
The [hook tests](../../../loom-code/tests/test_hooks_json.py) reproduced those
six failures, then replayed the corrected hints through the real launcher and a
recording checker with a cached test interpreter, a plugin path containing spaces
and no launcher on PATH. Stop now emits the installed launcher path and
`--repair delivery --json`; publication hints explicitly preserve the original
executable, arguments, working directory and stdin while replacing the mode.
Hook commands and fail-open policy are unchanged.

Two checker-emitted hints had the same PATH assumption:
[delivery Stop fallback](../../../loom-code/scripts/loom_checker/command_handlers/publish.py)
and [GitHub rules template recovery](../../../loom-code/scripts/loom_checker/command_handlers/github_rules.py).
Both now derive and shell-quote the installed launcher path and retain the
operation with an explicit mode. Existing delivery deadline and GitHub template
tests reproduced the failures; the latter replays the hint against its existing
fake GitHub fixture. No publication, live GitHub call or hook installation was
performed by these regression checks. Historical observations above remain
evidence about the inspected pre-fix versions, not claims about updated installs.

## Decision impact

Treat caller misuse plus insufficient recovery guidance as the actionable
local problem. Prioritize a bounded fix to help/usage/error guidance, preserving
the current accepted command syntax and exit semantics for invalid calls.
Show a complete launcher example, explain the implicit checker, and include
the existing plan command in discoverable usage. Test the observed mistakes
and the valid command using existing tests; a small cold-agent recovery trial
would test whether the guidance actually helps.

Do not introduce a new command framework, silently discard arbitrary arguments,
or expand planning stages. Documentation-only correction would not repair the
observed fallback path; permissive argument normalization would expand accepted
syntax and could conceal genuine mistakes. Defer either until evidence requires it.

## Limitations and open questions

The other machine is confirmed as Codex by the user. Its full command, raw
error and installed version are still needed to attribute its incident. It may have a different failure such
as passing a change id instead of a plan path. Current reproductions establish
the local mechanism, not that all planning stalls share it. The regression
checks above do not establish an installed-host or automatic-routing improvement.
