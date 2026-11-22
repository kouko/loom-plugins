---
name: run-the-push-gate-at-every-checkpoint-not-only-the-intake-gates
description: Do not let the first run of a whole-branch publication check happen at ship — today follow loom-code build's end-of-Build checks (complete package suite plus adversarial programs, repeated after every fix) and dry-run `loom_checker.py pr-floor --body-file <f> --base <sha> --head <sha>`, which blocks only on PR-body structure and reports verification status separately; historical (2026-09-03): a checkpoint that ran only the intake gates and never the since-retired bare `loom_checker.py push` reached ③ with a never-green push gate that blocked on five real rules and cost nine review rounds
type: practice
sources:
  - resource: simple-loom-flow (2026-09-03) — rounds 22–30 of the branch-end review; findings R22-*/R23-*/R24-*, CI-1, CI-2
---

Note 2026-11-22 (current procedure): the bare `loom_checker.py push`
gate described below is retired; `push` now takes only `--hook`,
`--install-git-hooks` or `--remove-git-hooks`, and `push --hook` only
refuses direct git commit, merge or push on main/master and reminds of
the verification status. The current checkpoint procedure is loom-code
build's end-of-Build checks (`loom-code/skills/build/SKILL.md` §3: the
complete package suite and every adversarial program, repeated after every
fix), plus `loom_checker.py pr-floor --body-file <f> --base <sha> --head <sha>`
against the drafted PR body: `pr-floor` blocks (`BLOCK ci.pr-floor`, exit 1)
only on PR-body structure, and reports absent or stale verification
separately as advisory output without changing that result. Everything from
here to the end of the entry is the 2026-09-03 history.

Historical (2026-09-03):

The push gate is the only rule set that recomputes the whole branch
(trailers vs `dispatch[]`, frozen stores, probe re-execution, second
vendor). The intake gates say nothing about any of that. On this change
every checkpoint recorded "three gates exit 0" and the push gate was first
run when the user asked how Codex fits, one step before ship.

What it found was not noise: the repo's own `.codex` shim pointed at a
script deleted three waves earlier; a frozen store had been edited; 17
commits carried dispatched work with no `Task:` trailer because the
orchestrator had "just fixed it" inline; four adversarial probes were
prose nobody could re-run; the scaffold overwrote an adopting repo's
`hooks.json`. Each of those is cheap at the wave it happened and
expensive at ship, where every fix is a code change after the final blind
run and reopens the records-only claim of the acceptance report.

Two corollaries. Orchestrator-inline work cannot be papered over: the
only repair is a user-run history rewrite plus an honest
`agent_id: orchestrator-inline` entry in `dispatch[]`. And a reviewer's
disposition must separate "done" from "scheduled": a sentence in the
completed tense for an action that lives in the next commit was judged a
fatal incorrect-fact twice (R25-C1, R28-C1).

Known gap carried forward: `push.dispatch-covers-tasks` classifies the
scaffold's own `.codex/hooks/contract/` copy as gate work, while
`changed_paths` exempts it — a pure copy refresh needs a trailer until the
two exemption sets are aligned. The intent status grammar in
`loom-code/contract/manifest.yaml` (`open | confirmed | withdrawn`) also
lacks the `closed <date> — PR #<N>` form the ship station writes.

(Note 2026-11-22: the "Known gap carried forward" paragraph above is
2026-09-03 history. `push.dispatch-covers-tasks` and the scaffold's
`.codex/hooks/contract/` copy no longer exist, and the intent status
grammar in `loom-code/contract/manifest.yaml` now includes
`closed <date> — PR #<N>`. For the current checkpoint procedure see the
note at the top of this entry.)
