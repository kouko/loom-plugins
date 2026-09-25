---
name: architecture
description: |
  Ratify a repository's ARCHITECTURE.md: module boundaries, file placement, file size, and CI stage rules, each backed by a guard test. Use when asked for architecture rules or to change one. 架構規則 / アーキテクチャ規約.
version: 1.0.0
---

## What this tool does

Relative paths in this document are relative to this skill's own
directory.

The user asks for architecture rules for a repository. You run one short
interview, write `ARCHITECTURE.md` at the repository root holding **rules
only**, write a guard test for every rule that can be checked mechanically,
restate the rules, and — on "yes" — write the `ratified-by:` line.

## Step 0 — Check the contract version

Locate the `loom-code` directory as
`../capture-intent/references/locate-loom-code.md` says, then run, with that
directory in place of `<loom-code>`:

```
python3 <loom-code>/scripts/loom_checker.py contract --require 2.1
```

Exit 0: continue. On any other result, or when the checkout cannot be found,
follow that reference's failure rule and **stop**.

## Step 1 — When to run

Run this **on request** only. `ARCHITECTURE.md` is **never required**: an
absent or unratified `ARCHITECTURE.md` never blocks a change, at any
station.

When `ARCHITECTURE.md` already exists, run in **update mode**: when a change
alters the structure a rule governs, change the rule and its guard in the
**same commit**, run the validator, then re-ratify (Step 4) — a rule
changed without its guard, or a guard without its rule, leaves the
document and the suite disagreeing.

## Step 2 — Interview → ARCHITECTURE.md

Read the repository's current layout first, then ask, in the user's own
words:

1. **Module boundaries** — which parts may depend on which, and which never.
2. **File placement** — where each kind of file goes (code, tests, scripts).
3. **File size** — the limit files should stay under, if any.
4. **CI stages** — what CI runs, and in what order.

Write `ARCHITECTURE.md` at the repository root following
`references/architecture-md-schema.md`: a title, then exactly the four rule
sections, one line per rule, and no overview or background section.

## Step 3 — Write the guards and validate

For every rule that can be checked mechanically, write a guard test in the
repository's **own test framework**, under a path its `package-tests:`
command in `docs/loom/KICKOFF-DEFAULTS.md` already runs — or extend that
command so it does; a guard the suite never runs holds nothing. Record the
guard's path on the rule line (`check: <guard path>`). A rule that needs
judgment says `check: review` and gets no guard.

Each guard's failure message names the **rule id** and the rule text, the
**offending path**, and both ways out: **conform** to the rule, or
**change the rule and its guard** together and re-ratify. Run the guards
once; a guard that fails on today's code is either a rule the user must
restate or a violation to show them.

Then check the file, with `<loom-design>` standing for this plugin's own
checkout:

```
python3 <loom-design>/scripts/architecture/validate_architecture_output.py ARCHITECTURE.md --draft
```

Exit 0: go to Step 4. Non-zero: fix what it names and run it again. Never
read back a file that has not exited 0 here.

## Step 4 — Restate and ratify

Read every rule back to the user in plain words, with which ones a guard
checks and which a reviewer judges. On a correction, fix it and read back
again. On "yes" — and only then — write one line directly under the title:

```
ratified-by: <name> <date>
```

`<name>` is the user's own name or handle; `<date>` is today, `YYYY-MM-DD`.
Run the validator again without `--draft`.

## Step 5 — Commit

Add `ARCHITECTURE.md` and the guard files by name, then:

```
git commit -m "docs(loom): ARCHITECTURE.md ratified"
```

## Downstream — how the rest of the flow uses it

`write-plan` reads `ARCHITECTURE.md`, when present, before its Task DAG: it
places added or moved files by the rules and names the rule id on the
task's Risk line. At `closing-review`, the code lens dimension
`architecture-conformance` scores the diff against the rules — a violation
is a finding with a fix; with no `ARCHITECTURE.md` the dimension is scored
**N/A with a one-line reason**. A missing `ARCHITECTURE.md` is only the
standing WARN the checker prints and never blocks any station.
