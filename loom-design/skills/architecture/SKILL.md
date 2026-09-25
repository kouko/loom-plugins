---
name: architecture
description: |
  Ratify a repository's ARCHITECTURE.md: module boundaries, file placement, file size, and CI stage rules, each backed by a guard test. Use when asked for architecture rules or to change one. 架構規則 / アーキテクチャ規約.
version: 1.0.0
---

## What this tool does

Relative paths in this document are relative to this skill's own
directory.

The user asks for an architecture for a repository. You design it with the
user — read what exists, propose options with trade-offs, let the user pick
— then write `ARCHITECTURE.md` at the repository root holding **the
decisions and the rules only**, write a guard test for every rule that can
be checked mechanically, restate them, and — on "yes" — write the
`ratified-by:` line.

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

When `ARCHITECTURE.md` already exists, run in **re-design mode**: when a
change alters the structure, re-design only the affected part with the
user (Step 2, for the affected choices alone), then update the affected
decisions, rules and guards in the **same commit**, run the validator, and
re-ratify (Step 4) — a decision, rule or guard changed without the others
leaves the document and the suite disagreeing.

## Step 2 — Design with the user → ARCHITECTURE.md

**Read first.** Read the project's requirements — its intent files,
README and `PRINCIPLES.md`, when present — and the existing code: its
layout, languages, build files, test setup and CI, if any.

**Propose.** The open choices are:

1. **Module split and dependency direction** — which modules exist, which
   may depend on which, and which never.
2. **Main technology choices** — language, framework, key libraries, where
   the existing code has not already settled them.
3. **Folder structure** — where each kind of file goes (code, tests,
   scripts), and the size a file stays under.
4. **Required CI stages** — what CI must run, and in what order.

A choice the existing code already settles is stated, not re-opened —
unless the user asks to revisit it. For each open choice, present **at
least two options** in MADR style: the decision drivers first, then each
option's trade-off against those drivers ("good, because … / bad,
because …"), then your recommendation and what would make it wrong.
**Never present a single answer**, even when one option looks obvious.
Draw the options from `references/design-know-how.md`. The user picks;
on a question, answer it and present the options again.

Data models and API interfaces stay out of this design: they belong to
each change's spec.

**Write.** Write `ARCHITECTURE.md` at the repository root following
`references/architecture-md-schema.md`: a title, a `## Decisions` section
recording each pick (the choice, the options considered, the reason), then
exactly the four rule sections, one line per rule, and no overview or
background section.

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

Read every decision and rule back to the user in plain words, with which
rules a guard checks and which a reviewer judges. On a correction, fix it
and read back again. On "yes" — and only then — write one line directly under the title:

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
