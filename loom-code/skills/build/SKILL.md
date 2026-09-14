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
prose steps it lists as skipped (intent, spec, plan, implementer, tdd,
blind-run). The agent may suggest skipping steps at most once per change: it
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
Code or `python3 <injected loom-code plugin root>/scripts/dispatch_profile.py`
from Codex, with the explicit observed JSON defined by the shared contract
before each spawn. Pass its deterministic JSON result to the host-native spawn:
apply both fields from `overrides`, or apply neither when it is `null`. Feed
every completed result back as an `after-execution` event before any
redispatch. Describe an omitted or wrong
task result as a post-execution capability-quality failure only when it meets
the contract's checkable definition; describe rejected routing parameters as
a pre-execution host rejection, which selects the one atomic fallback instead
of model escalation.

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
integration checks once to expose cross-task defects. Do not run the complete
package suite as a speculative push preflight; `finalize-review` owns its one
content-bound execution.

## 4. Hand off to Review

Commit functional changes normally. Report the branch base, HEAD, changed
paths, focused test results, and any unresolved risk. Call `loom-code:review`
once over the cumulative branch. Build never writes `attestation.json` and
never edits it after Review generates it.
