---
name: product-principles
description: |
  Ratify PRINCIPLES.md. Use when a product needs principles or someone asks what should govern product, design, or engineering trade-offs.
version: 1.0.0
---

## What this tool does

Relative paths in this document are relative to this skill's own directory.

The user names a product idea. You run one short interview, write
`PRINCIPLES.md` at the consumer project's root, restate it, and — on
"yes" — write the `ratified-by:` line that makes it the repo's standing
constitution. You never invent a principle the user did not confirm, and
you never ask them to judge anything but their own answers.

Most of the time you are not invoked directly: `capture-intent` (or, when
`loom-design` is absent, `loom-code`'s `write-plan`) runs this same
interview inline, in the same conversation as decision point ①, the first
time a `kind: product` change meets a repo with no ratified
`PRINCIPLES.md`. **The interview is the same one `loom-code`'s
`write-plan` runs when `loom-design` is absent** — this tool exists so a
user can also run it stand-alone, on request, before any change is in
flight.

## Step 0 — Check the contract version

Locate the `loom-code` directory as
`../capture-intent/references/locate-loom-code.md` says, then run, with that
directory in place of `<loom-code>`:

```
python3 <loom-code>/scripts/loom_checker.py contract --require 2.1
```

Exit 0: continue. On any other result, or when the checkout cannot be found,
follow that reference's failure rule and **stop**.

## Step 1 — Run the interview

Read `<loom-code>/contract/templates/PRINCIPLES-interview.md` and ask
exactly its five questions, in the user's own words, until each answer is
clear. One line each on their intent:

1. **Who** it is for, and how they solve this today without it.
2. **The one thing** that cannot be compromised (fast, accurate, cheap,
   private, offline, good-looking) — ranked.
3. **What it explicitly will not do.**
4. **The worst failure**, and who it hurts.
5. **What is already fixed** and cannot change (platform, language, a
   paid service, a data format).

Push until each answer is falsifiable — a later decision can be checked
against it, not just admired.

## Step 2 — Write PRINCIPLES.md

Emit `PRINCIPLES.md` at the consumer project's root (not per-feature),
with exactly these five `##` sections, in this order:

```
# Product principles
## Who
## Non-negotiables (ordered)
## Won't do
## Failure we must avoid
## Fixed choices
```

`## Non-negotiables` is an ordered list of **at least three** entries,
each **falsifiable**: state the choice and a concrete pair that would
tell a stranger it held or broke. For example — good: "offline-first: the
app must complete a save with the network off (bad: 'the app should feel
fast')." A non-negotiable with no such pair is a slogan, not a principle;
push back and ask again rather than write it down.

## Step 3 — Restate and ratify

Read the whole file back to the user in their own words — not a diff, the
actual sections. On a correction, fix it and read back again; there is no
round limit. On "yes", write one line at the top of the file, directly
under the title:

```
ratified-by: <name> <date>
```

`<name>` is the user's own name or handle; `<date>` is today,
`YYYY-MM-DD`. A file with no `ratified-by:` line, or one whose
`## Non-negotiables` has fewer than three entries, is not ratified —
`loom-code`'s checker (`standing.product-principles-reject`) recomputes
both conditions itself and rejects a `kind: product` change against an
unratified file; nothing here can talk it out of that.

## Step 4 — Commit

```
git add PRINCIPLES.md
git commit -m "docs(loom): PRINCIPLES.md ratified"
```

## Downstream — how the rest of the flow uses it

`PRINCIPLES.md` is the standing, always-on constraint every later station
reads: `write-spec` loads it before drafting `Requirements`; a product
change with no ratified copy is refused there
(`standing.product-principles-reject`), never silently allowed through.
At `closing-review`, the `principles-conformance` dimension scores the diff
against these Non-negotiables; when nothing in the file speaks to a given
finding, the dimension is scored **N/A with a one-line reason**, never
forced to a number it cannot support. Engineering-only changes are never
blocked by a missing or unratified file — the reject rule fires only on
`kind: product`.

<!-- gate: product-principles.ratified-requires-user-yes -->
**No `ratified-by:` line is ever written without the user having said
yes to the restatement in Step 3.** Writing it on an assumed confirmation
makes a constitution nobody actually agreed to.
