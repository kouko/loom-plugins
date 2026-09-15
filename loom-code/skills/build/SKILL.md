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

At entry, run `loom_checker.py selection show <change-id>` and omit only the
steps it lists as skipped (spec, plan, implementer, tdd, adversarial,
package-tests, blind-run). The agent may suggest skipping steps at most once per change: it
runs `loom_checker.py selection propose <change-id> --origin agent`, shows the
table and the confirmation line (type `/loom-code:expert-mode` (Codex:
`$expert-mode`) with the code shown), and keeps working on the full process at
once; a plain "yes" binds nothing. When the user asks in their own words to run
or skip Loom steps, read ../expert-mode/SKILL.md and follow it with
`--origin user`.

## 2. Implement test first

Before every host-native dispatch, the station must read the
[shared dispatch profile](../../references/dispatch-profile.md), classify the
task from its evidence, and resolve the atomic model-and-effort profile against
the selected model's verified host capabilities. Record the requested and
effective profile with its evidence-grounded reason in active task context only.
Apply the resolved overrides at invocation time; a static model or effort pin in
an agent contract is invalid.

Invoke `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/dispatch_profile.py` from Claude
Code or `python3 <loom-code>/scripts/dispatch_profile.py` from any other host,
where `<loom-code>` (this plugin's root) is `${CLAUDE_PLUGIN_ROOT}` on Claude
Code; on any other host it is the directory two levels above this SKILL.md.
Supply the explicit observed JSON defined by the shared contract
before each spawn. Pass its deterministic JSON result to the host-native spawn:
apply both fields from `overrides`, or apply neither when it is `null`. Feed
every completed result back as an `after-execution` event before any
redispatch. Describe an omitted or wrong
task result as a post-execution capability-quality failure only when it meets
the contract's checkable definition; describe rejected routing parameters as
a pre-execution host rejection, which selects the one atomic fallback instead
of model escalation.

On Antigravity CLI, map tool and agent names with
[`../../references/antigravity-tools.md`](../../references/antigravity-tools.md).

Unless `selection show` lists `tdd` as skipped, for every behavior change:

1. Write the smallest failing test and run it to observe RED.
2. Implement the minimum change and run it to GREEN.
3. Refactor only while the focused suite stays green.

Unless `selection show` lists `implementer` as skipped, implementer dispatch is
mandatory for every implementation task; when it is skipped, the main agent
implements the task itself. Scheduling
multiple implementers concurrently is optional and used only for genuinely
independent file sets; no dispatch ledger is created. If implementer dispatch
is unavailable, stop and report the blocker. Unless `selection show` lists
`implementer` as skipped, the main agent must not substitute itself as
implementer. An implementation agent never acts as its own closing
reviewer.

Internal plans, commits, and verification evidence are written in English.

## 3. Verify integration

Run focused tests after each task. After all tasks land, run the relevant
integration checks once to expose cross-task defects. Then end Build with its
mechanical checks, in this order:

1. Dispatch the `loom-code:adversary` agent fresh-context, resolving its
   profile as §2 requires before every host-native dispatch. Never dispatch an
   agent that implemented any part of the change. Give it only paths: the
   intent, the plan, and the changed paths; never pass an implementer's
   explanation of its own code. The adversary writes and commits its
   adversarial programs.
2. Run the repository's complete package suite, then each committed
   adversarial program.

When a check fails, the fix is made inside Build as §2 assigns implementation
work; the adversary never fixes what it breaks. Build does not hand off to
Review until the complete package suite has passed or `selection show` lists
`package-tests` as skipped, and until every adversarial program has passed or
it lists `adversarial` as skipped, each skip waiving only its own check. A
hand-off with neither step skipped therefore means the complete package suite
and every adversarial program pass.
`finalize-review` still executes both once more on committed content.

When `selection show` lists `adversarial` as skipped, dispatch no adversary and
run no adversarial program. When it lists `package-tests` as skipped, run no
complete package suite.

When closing review or a failed `finalize-review` returns the change to Build,
repeat these end-of-Build checks after the fix: run the complete package suite
and re-run the existing adversarial programs. Do not dispatch the adversary
again.

## 4. Hand off to Review

Commit functional changes normally. Report the branch base, HEAD, changed
paths, focused test results, the complete package suite command and its result,
each adversarial program's path and command, and any unresolved risk. Call `loom-code:closing-review`
once over the cumulative branch. Build never writes `attestation.json` and
never edits it after Review generates it.
