---
name: build
description: |
  Implement a committed plan with test-first changes. Use when a confirmed intent and plan are ready to build.
version: 1.2.0
---

# Build

Build produces functional content. It does not maintain review accounting or
generate publication evidence.

## 1. Establish scope

Read the confirmed intent, spec when present, plan, current branch, and branch
base. Preserve unrelated and untracked work. Work only on planned paths.

At entry, run `loom_checker.py selection show <change-id>` and omit the steps
`selection show` lists as skipped (spec, plan, implementer, tdd, adversarial,
package-tests, blind-run), plus any step the user told you to skip in plain
words; [expert-mode](../expert-mode/SKILL.md) stays an optional route the user
may invoke. When `selection show` reports `bound: false` with a non-empty
`skip` field, the checker judged this change narrow: name those steps to the
user in one line as you omit them, `Skipped as a narrow change: <steps>`, read
from that field rather than from conversation recall. The default is the full
flow: skip a step only when the user tells
you to in plain words, then tell the user in one line which step is skipped and
continue. When you honour such a skip, append one line
`skipped-by-instruction: <step> <YYYY-MM-DD>` to the plan's `## Risks` section
and commit it. Never ask the user for a generated code to skip a step.

Finding no task left to implement is not a reason to end Build. It means §2 has
nothing to implement, not that the run is over: continue to §3, which states
what such a re-entry runs.

## 2. Implement test first

Before every host-native dispatch, the station must resolve the model-and-effort
profile as the [shared dispatch profile](../../references/dispatch-profile.md)
defines and apply its result. `<loom-code>` (this plugin's root) is
`${CLAUDE_PLUGIN_ROOT}` on Claude Code; on any other host it is the directory
two levels above this SKILL.md.

On Antigravity CLI, map tool and agent names with
[`../../references/antigravity-tools.md`](../../references/antigravity-tools.md).

Unless `tdd` is skipped (listed by `selection show` or skipped by the user's
plain-words instruction), for every behavior change:

1. Write the smallest failing test and run it to observe RED.
2. Implement the minimum change and run it to GREEN.
3. Refactor only while the focused suite stays green.

Unless `implementer` is skipped (listed by `selection show` or skipped by the
user's plain-words instruction), implementer dispatch is mandatory for every
implementation task; when it is skipped, the main agent implements the task
itself. Scheduling
multiple implementers concurrently is optional and used only for genuinely
independent file sets; no dispatch ledger is created. If implementer dispatch
is unavailable, stop and report the blocker. Unless `implementer` is skipped
(listed by `selection show` or skipped by the user's plain-words instruction),
the main agent must not substitute itself as implementer. An implementation agent never acts as its own closing
reviewer.

Internal plans, commits, and verification evidence are written in English.

## 3. Verify integration

Run focused tests after each task. After all tasks land, run the relevant
integration checks once to expose cross-task defects. Then end Build with its
mechanical checks, in this order:

1. From the change worktree, run
   `python3 <loom-code>/scripts/loom_checker.py sync-trunk`, so the adversary,
   the suite and the programs all see the fetched trunk tip. On
   `BLOCK review.sync`, fix the cause inside Build, where a conflict is resolved as
   implementation work in a new build round, never by the command. On
   `WARN review.sync`, continue unsynced. Any other result, including exit 2,
   does not continue and reports the printed message.
2. Dispatch the `loom-code:adversary` agent fresh-context, resolving its
   profile as §2 requires before every host-native dispatch. Never dispatch an
   agent that implemented any part of the change. Give it only the change id,
   `HEAD`, and paths: the intent, the plan, and the changed paths with their
   artifact types; never pass an implementer's explanation of its own code. The adversary writes and commits its
   adversarial programs. It works from the recipes in
   [`adversarial.md`](../closing-review/references/adversarial.md).
3. Run the repository's complete package suite, then each committed
   adversarial program. The suite command is the `package-tests:` value in
   `docs/loom/KICKOFF-DEFAULTS.md`, or, when absent, the command detected from
   build markers; when it is `none`, the complete package suite is skipped:
   either `package-tests` is listed by `selection show`, or the change reaches
   Ship unattested and the PR discloses `absent`.

When a check fails, the fix is made inside Build as §2 assigns implementation
work; the adversary never fixes what it breaks. Every fatal or important
finding the adversary returns is fixed inside Build like a failing check before
hand-off, and any finding left unresolved is listed in the §4 hand-off. Build does not hand off to
`closing-review` until the complete package suite has passed or `package-tests`
is skipped (listed by `selection show` or skipped by the user's plain-words
instruction), and until every adversarial program has passed or `adversarial`
is skipped (listed by `selection show` or skipped by the user's plain-words
instruction), each skip waiving only its own check.
`finalize-review` still executes both once more on committed content.
When the user skipped the suite or the adversary in plain words, closing-review
hands the change to Ship unattested (closing-review §5).

When `adversarial` is skipped (listed by `selection show` or skipped by the
user's plain-words instruction), dispatch no adversary and run no adversarial
program. When `package-tests` is skipped (listed by `selection show` or skipped
by the user's plain-words instruction), run no complete package suite.

Repeat these end-of-Build checks after every fix: run the complete package
suite and re-run the existing adversarial programs. After a fix where every
adversarial program still passes, or fails only for a product defect, do not
dispatch the adversary again.

<!-- gate: build.absence-recovery -->
Build enters these end-of-Build checks on absence as well as after a fix: when
Build is entered with every planned task already committed and an item Build
owes is absent, it runs this section from step 1 to produce that item. Absence
is a distinct antecedent from a failing check; an item that exists and fails is
a failure and is fixed as above. Read `loom-code/contract/manifest.yaml`
(`stations[].produces` and `actions[].owner`) to decide whether an absent item
is Build's to produce; this file keeps no second copy of that mapping. This
lookup covers only an item this rule names: the adversarial programs, the
blind-run report or the attestation. Absence
dispatches the adversary only when no adversarial program is committed;
committed programs are re-run, never re-dispatched, exactly as after a fix.

A recovery run is bounded across stations, not only within Build: an entry here
made to resolve an absent item counts toward that bound; an entry made for an
ordinary review-round fix never does. [closing-review](../closing-review/SKILL.md) §2
states the bound and the record of entered stations it is counted from. Read it
there; this file keeps no count of its own.

Build dispatches the `loom-code:adversary` agent fresh-context again to update
its own programs when a fix widens or changes what the change covers, or trunk
content brought in by a trunk sync changes it, and a committed adversarial
program fails, or is unable to run, for that reason, rather than for a product
defect it correctly caught. A program that still passes keeps its content.
Build decides which case
applies from the program's failure and the widened scope, and fixes a product
defect in the product as above. Give the adversary the step 2 inputs plus the
widened changed paths, or the trunk paths the sync brought in, and the
failing program's output. The adversary updates only its own programs. Implementers and the orchestrator never edit an
adversarial program. After the update, Build repeats these end-of-Build checks.

<!-- /gate -->

## 4. Hand off to closing-review

Commit functional changes normally. Report the branch base, HEAD, the
`sync-trunk` result with any warning it printed, changed paths, focused test
results, the complete package suite command and its result,
each adversarial program's path and command, each adversary re-dispatch with its reason, every unresolved adversary finding, the station sequence entered so far when this run recovered from an absent item, and any unresolved risk. Call `loom-code:closing-review`
once over the cumulative branch. Build never writes `attestation.json` and
never edits it after `closing-review` generates it.
