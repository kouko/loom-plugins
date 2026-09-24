---
name: closing-review
description: |
  Run closing review and generate an attestation. Use after Build completes or functional changes invalidate prior review evidence.
version: 1.5.0
---

# Closing review

Reviewer findings and generated evidence are written in English.

`closing-review` decides whether the completed functional content is ready. It produces
`docs/loom/<change-id>/attestation.json`; agents never edit that file by hand.

## 1. Establish the content

Resolve the branch base, read the confirmed intent and plan, and list the
cumulative diff. If only publication metadata changed and a matching
attestation already exists, stop: the evidence is still valid and Ship owns
the remaining work.

At entry, run `loom_checker.py selection show <change-id>` and omit the steps
`selection show` lists as skipped, plus any step the user told you to skip in
plain words; §2 and §3 say how skipped reviewers, adversarial and acceptance-test are
handled; [expert-mode](../expert-mode/SKILL.md) stays an optional route the
user may invoke. Words that ask to skip independent acceptance testing —
"acceptance testing", or the step formerly called "blind run" — mean the
`acceptance-test` step. When `selection show` reports `bound: false` with a non-empty
`skip` field, the checker judged this change narrow: as you omit those steps,
tell the user its `narrow_change_line` field (`Skipped as a narrow change:
<steps>`) exactly as printed, rather than rebuilding it from conversation recall
or the raw `skip` ids. The default is the full
flow: skip a step only when the user
tells you to in plain words, then tell the user in one line which step is
skipped and continue. When you honour such a skip, append one line
`skipped-by-instruction: <step> <YYYY-MM-DD>` to the plan's `## Risks` section
and commit it. Commit that line before reviewers read the final digest,
because it changes the digest; a later commit is harmless only when the skip
sends the change to Ship unattested (§5). Never ask the user for a generated
code to skip a step.

## 2. Compute review depth

Before every host-native dispatch, the station must resolve the model-and-effort
profile as the [shared dispatch profile](../../references/dispatch-profile.md)
defines and apply its result. Repeat this resolution for every reviewer,
second-vendor reviewer, and acceptance tester dispatch. `<loom-code>` (this plugin's
root) is `${CLAUDE_PLUGIN_ROOT}` on Claude Code; on any other host it is the
directory two levels above this SKILL.md.

On Antigravity CLI, map tool and agent names with
[`../../references/antigravity-tools.md`](../../references/antigravity-tools.md).

Before dispatching reviewers in Round 1, run
`python3 <loom-code>/scripts/loom_checker.py sync-trunk` from the change
worktree. When it reports `up to date`, continue. When it reports
`content changed`, dispatch no reviewer and return to Build §3 to re-run the
complete package suite and the existing adversarial programs, then start
Round 1 again. When it prints `WARN review.sync`, state the warning in the
round report and continue. When it prints `BLOCK review.sync`, dispatch no
reviewer and return the change to Build. Any other result, including exit 2,
dispatches no reviewer and reports the printed message. Run it before
acceptance testing (§3), so acceptance testing exercises the synced content.

Before dispatching reviewers in any round, confirm on the current functional
content (a committed acceptance test report aside) that Build's hand-off reports the
complete package suite passing or `package-tests` is skipped (listed by
`selection show` or skipped by the user's plain-words instruction), and that it
reports every adversarial program passing or `adversarial` is skipped (listed
by `selection show` or skipped by the user's plain-words instruction), each
skip waiving only its own check. When that hand-off reports a check failing, return the change to
Build and dispatch no reviewer. Reviewers read only content whose Build
mechanical checks passed.

<!-- gate: review.absence-recovery -->
Absence is a distinct antecedent from a failing check. On a re-entry with
every planned task already committed, that hand-off is not in context, and the
item this station needs may itself be missing. Neither state is a check
reporting a failure, and neither routes like one. When an item is absent, read
`loom-code/contract/manifest.yaml` (`stations[].produces` and
`actions[].owner`) for the station that produces the absent item; this file
keeps no second copy of that mapping. This lookup covers only an item this
rule names: the adversarial programs, the acceptance test report or the
attestation. Take the owner, never
`charter.signoff`, which names where an artifact is signed off rather than
who produces it. When that owner is this station, produce the item here and
route it nowhere; for an acceptance test report specifically, that means following
§3. When it is
another station, return the change there, naming the station sequence
entered so far, and dispatch no reviewer. Recovery adds a path and waives
nothing: every check
above runs on the recovered content. Keep the stations this run has entered as
a list in entry order, in the active task context and not in a committed
ledger, and name that list in the handoff and in either stop below. A second
entry to a station is the last one allowed; a third entry to any station is a
recovery that has failed, and it stops and reports under the rule below rather
than routing on. The run enters no station more than twice, a count that
tracks only entries made to resolve an absent item under this rule and is
never incremented by §4's ordinary round-and-digest progression.

Stop and ask when producing an absent item needs a decision point the user
has not answered for this change, naming the station sequence entered so
far. When the user has answered it, including a
general delegation such as "you decide", proceed and record the choice as
user-decided. This governs only whether the run asks again; a user-requested
skip follows the plain-words rule in §1.

Stop when the attempt to produce an absent item fails. Report which item is
absent, what was attempted, and where it failed. Also report the station
sequence entered so far. Do not attempt that item a
second time and do not hand the change on to another station.

<!-- /gate -->

When acceptance testing is needed, it starts together with the first-round
reviewers on the same functional content (§3), and the reviewers give their
Round 1 verdict only after reading its committed report. After Build commits completed functional
content, run:

```text
python3 <loom-code>/scripts/loom_checker.py reviewer-count <change-id>
```

The output is the computed reviewer floor: dispatch exactly that many
fresh-context reviewers with distinct agent identities. The checker derives the
floor from the cumulative branch delta and fails closed to two when it cannot
classify the whole change. `finalize-review` recomputes the same policy, and
the PR's verification status reports a mismatch as `stale`; the orchestrator
never declares or overrides it. When `reviewers` is skipped (listed by
`selection show` or skipped by the user's plain-words instruction), dispatch no
reviewer and pass no `verdicts`.
- Unless reviewers are skipped, a selected second vendor remains required.
  Resolve it from the standing
  fixed CLI, the per-change `ask` answer, or a `selection-confirmed` line
  naming the second vendor in the plan's `## Risks` section; the
  last form is write-plan's active-task handoff for a timely `suggest` opt-in.
  The selected vendor fills one computed reviewer slot; it does not add a
  reviewer beyond the floor.

Reviewer independence is a quality requirement, not a ledger field. Give each
reviewer the branch base, changed paths, intent, spec when present, plan, and
the applicable lens from `references/lenses.md`. Tell each first-round
reviewer whether acceptance testing runs alongside this round. Reviewers return the
structured YAML required by `agents/reviewer.md`; the orchestrator converts
the accepted fields to the temporary JSON consumed by finalization.

<!-- gate: review.atomic-claude-dispatch -->
On Codex, when the selected second vendor is Claude Code, send that complete
reviewer prompt on stdin to one installed-plugin invocation:

```text
python3 <loom-code>/scripts/claude_reviewer.py [--model <model> --effort <effort>] --timeout-seconds 600
```

When the resolver returns a complete `overrides` pair, pass both flags. When
it returns `null`, invoke the runner with neither flag so Claude Code uses its
host defaults. The runner rejects a partial pair before starting Claude; the
caller must never reconstruct a missing half.

Run this invocation outside the Codex sandbox with reusable host approval
scoped to the installed `python3 <loom-code>/scripts/claude_reviewer.py`
command. This is the standard Codex-to-Claude path because the sandbox can
hide an existing Claude login that the same runner can use outside it. If that
narrowly scoped permission is denied or unavailable, report an authorization
blocker. Do not fall back to a sandboxed Claude invocation, infer that the user
logged out, run a separate authentication preflight, or request broader Python
or shell access. Do not read, copy, or move Claude credentials into the
sandbox. Only an unauthenticated result from this outside-sandbox invocation
produces the Claude login diagnosis; stop without treating it as transient.

The runner executes one Claude attempt and does not retry. Exit 0 carries the
raw non-empty reviewer output, which must still satisfy `agents/reviewer.md`.
The runner must never parse or validate reviewer YAML. The `closing-review` orchestrator
enforces its stricter one-retry limit and owns that validation even when the
shared resolver still has more completed-redispatch budget available.
Its JSON stderr names `empty-output` for blank stdout and `timeout` when the
attempt exceeds the bound. Do not run a model-backed preflight. Treat either
result as the transient executor failure already governed below: invoke the
runner at most once more for the same functional-content digest and reviewer
identity. If that attempt also fails before a conforming verdict exists, report
both diagnostics and end the episode as `EXECUTION_FAILED`.

A model rejection before task execution follows the shared
host-rejection path instead: feed the rejection to the resolver and invoke its
override-free replacement in the same task attempt. If that replacement is
also rejected, feed back `rejection_retried: true`, accept
`execution-failed`, and stop. The rejected replacement must not enter the
generic transient-executor retry, so the two policies cannot create a third
Claude invocation.

The override-free replacement consumes the one same-digest transient-retry
slot. After it, no further Claude invocation occurs for that digest regardless
of failure kind.

The runner reports `host-rejection` only for a non-zero Claude result carrying
the exact `[claude-code:unrecognized_model]` marker. A partial pair or an effort
outside Claude Code's grounded five-value CLI set is `input-error` and exits 2
before launch; it is not host rejection. Every other non-zero exit remains a
generic executor failure; the caller must not infer routing rejection from
free-form provider text. Route on the stderr JSON `kind`, not exit status
alone; a plain-text exit 2 is caller misuse rather than a routing signal.
<!-- /gate -->

## 3. Run acceptance testing

Use acceptance testing when an Acceptance line cannot be settled mechanically.
Acceptance testing means dispatching the `loom-code:acceptance-tester` agent
fresh-context, never an agent that touched any part of the change. Its
`docs/loom/<change-id>/acceptance-test-report.md` is functional content; only
`attestation.json` is publication metadata. Start the acceptance tester and the
first-round reviewers on the same commit at the same time. Finish acceptance
testing and commit that report on the change branch before running
`finalize-review`. Its evidence file,
`docs/loom/<change-id>/evidence/acceptance-test-evidence.md`, is functional
content too and is committed with the report under the same deadline.
Once the report and its evidence file are committed, resume each of those
reviewers, the same agent rather than a new one, with the delta from the commit
it started on to the report commit. Each reads the report and evidence against the change it
already reviewed, and only then returns its Round 1 verdict. A reviewer's
return before that resume is not a verdict. The commit the reviewers started
from and the report commit form Round 1's single functional-content digest. A
reviewer that cannot be resumed, such as a one-shot vendor CLI, starts after
the report is committed. A report committed after their verdicts is new
functional content and needs the next round. When the acceptance tester
re-tests after a fix, finish that re-test and commit its report and evidence
file before resuming the reviewers for that round.
When `acceptance-test` is skipped (listed by `selection show` or skipped by
the user's plain-words instruction), run no acceptance testing.

On every dispatch, tell the acceptance tester whether `package-tests` or
`finalize-review` is skipped. On a re-dispatch after a fix, also pass the
earlier report and evidence file paths and the fix's commit range. The
tester's steps 6-7 govern the suite row and what is re-tested.

Closing review dispatches no adversary and creates no adversarial program.
Build commits the adversarial programs, and its hand-off names each program's
path and command; §5 passes them to `finalize-review`. Do not record a claimed
result; finalization executes them. When `adversarial` is skipped (listed by
`selection show` or skipped by the user's plain-words instruction), Build hands
off no adversarial program and §5 omits the `adversarial` input.

<!-- gate: review.probe-graduation -->
A probe program that caught a defect on its own change is carried into the
suite that runs on every later change, through a plan task, before §5 runs
`finalize-review`. That is the deadline, because §5 is what executes the
programs and writes the attestation: a program still sitting in the change's
store when the attestation is written was never graduated. Graduation is a
plan task, so the route is back through Build — this station dispatches no
implementer and moves no file itself. Re-enter §5 once Build reports the move.

A program of this change that caught none is named as such in the review
report and deleted from the repository: a program that never went red is run
twice and never again, so it defends nothing against a later regression. The
adversarial protocol commits a program only when it is red, so this branch
never fires on a program that step produced as intended. It is reached in two
cases and no others: a program carried over from an earlier dispatch whose
case a later fix removed, and a program whose observed result Build's hand-off
does not give, which is read as caught nothing. Read which is which from
Build's hand-off, which records each program's observed result. Probe programs
committed for earlier changes stay where they are.
<!-- /gate -->

## 4. Converge within one bounded episode

<!-- gate: review.bounded-episode -->
A closing Review episode starts when fresh reviewers first evaluate completed
functional content for one confirmed-intent commit. Only a newly confirmed
intent starts another episode. The episode admits at most three distinct
functional-content digests; changing the task, app, branch, reviewer, vendor,
model, or technical design does not reset that limit.
A digest is distinct whenever a functional-content file changed since the
content the reviewers last read; publication-only edits do not change it.
A report commit the reviewers read inside Round 1 (§3) belongs to Round 1's digest.

- **Round 1 — full review.** Review the cumulative functional content.
- **Round 2 — fix verification.** Batch fatal and important findings, return to
  Build, which repeats its end-of-Build mechanical checks, and resume the same
  reviewers over the functional fix delta.
- **Round 3 — terminal verification.** Review the final digest once.
  `NEEDS_REVISION` ends the episode as `NON_CONVERGENT`; never dispatch Round 4.

Treat the episode as stuck when Round 2 still has blockers, the same blocker
survives two consecutive rounds, the blocker count does not decrease after a
functional fix, or the fix repeats the same mechanism shape; stop local
patching then, and use the next available round only after the technical
design re-look. The agent owns that re-plan when it preserves requirements,
visible behavior, and guarantees.

Do not ask the user whether to continue or which technical repair to choose.
Ask only when resolving the blocker would change requirements, visible
behavior, or guarantees; that change requires a newly confirmed intent rather
than another round in this episode.

A malformed response, unavailable executor, or other transient failure before
a conforming verdict exists may retry once against the same functional-content
digest. That retry is not a review round. A second executor failure ends the
episode as `EXECUTION_FAILED`; a conforming `NEEDS_REVISION` always consumes
the current round.

Keep this episode in the active task context. Do not create a review-round
ledger or committed state schema. Wording-only publication edits do not reopen
`closing-review`.
<!-- /gate -->

Before any fix begins, the main agent collects every fatal or important
finding that the reviewers and independent acceptance testing returned on the
current functional-content digest into one list. Every fix starts from that
whole list. Findings that share a defect class, named in words taken from the
findings themselves, go to Build as one hand-off that names every one of their
instances; findings of different classes go as separate hand-offs. Every
hand-off from the list goes to Build in the same fix round, before the
reviewers resume. A verdict label such as `NEEDS_REVISION` names no class.
The per-verdict failure record below is disclosure for the pull request only;
each fix is scoped from this list.

Before any fix round, pass each non-passing reviewer verdict to
`loom_checker.py selection record-failure <change-id> --step reviewers --rule <verdict>`;
a rejection never handed over stays unrecorded. Build scopes each fix to its
defect's whole class before an implementer or the main agent makes it, as
Build §2 states.

Convergence is where a lesson this branch taught is still cheap to keep.
Whatever it taught has surfaced by now — through a finding, a probe, or
acceptance testing — and writing it down after the merge costs a branch and a pull
request for something already known. When this repository has a
`docs/loom/memory/` directory, that is where such a lesson belongs.

A recorded lesson is functional content like anything else committed: it
changes the digest, so it must land in a digest the reviewers read, riding
the fix round already in flight rather than arriving after the last one. It
never justifies exceeding this episode's digests. A lesson that surfaces
once they are spent rides the next change's branch as a batched passenger —
which is still not a branch opened only to record something.

Almost nothing qualifies. Most of what a review surfaces is not a durable
lesson: a one-off implementation slip belongs in its commit message, a
verification result in this change's evidence, an unfinished item in an
intent. Zero to one durable lesson per change is the
normal outcome. This passage states the moment and the bar; it invokes
nothing, requires no plugin to be installed, and asks for no decision from
the user.

## 5. Finalize

Write reviewer output and the adversarial command declarations from Build's
hand-off to a temporary JSON input outside the repository:

```json
{
  "verdicts": [
    {"reviewer":"<id>","vendor":"<vendor>","model":"<model>","lens":"code","verdict":"PASS","findings":[]}
  ],
  "findings": [],
  "adversarial": [
    {"command":"python3 <path>","artifact":"<path>"}
  ]
}
```

The `findings` input carries every unresolved adversarial finding that Build's
hand-off lists.

Then run:

```text
python3 <loom-code>/scripts/loom_checker.py finalize-review <change-id> --input <temporary-json>
```

The checker runs the declared package suite and each adversarial program once.
`finalize-review` waives reviewers, adversarial and package-tests solely for a
bound selection that lists them.
Only after all executions and verdicts pass does it atomically generate the
attestation bound to the functional-content digest. Commit the generated file
with any remaining publication metadata; publication validates that single
attestation directly.

When a step that `finalize-review` needs (reviewers, adversarial, package-tests)
was skipped by the user's plain-words instruction rather than a bound
selection, skip `finalize-review` and leave the change unattested: tell the
user in one line that the PR will show `verification absent`, and hand the
change to Ship.

When `finalize-review` fails for any cause other than the plain-words case above,
return the fix to Build, which repeats its
end-of-Build mechanical checks, and the fixed content, a new functional-content
digest, must pass the next review round (§4) before `finalize-review` runs
again. No technical design re-look precedes that round unless the episode is
stuck. Earlier verdicts are never reused for the fixed content. When no round
remains, the fix would need a fourth distinct digest, which §4 forbids, so it
ends the episode as `NON_CONVERGENT`.

## Handoff

Report the reviewers, executed commands, functional digest, and unresolved
findings. On PASS, hand the matching attestation to `loom-code:ship`.
