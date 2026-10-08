---
name: closing-review
description: |
  Run closing review and generate an attestation. Use after Build completes or functional changes invalidate prior review evidence.
version: 1.5.0
---

# Closing review

Reviewer findings and generated evidence are written in English.
Every message to the user, including a relayed reviewer or acceptance-tester
result, is written in the user's conversation language, even on a turn with no
new user message, such as a background agent's completion or a resume after
compaction.

`closing-review` decides whether the completed functional content is ready. It produces
`docs/loom/<change-id>/attestation.json`; agents never edit that file by hand.

## 1. Establish the content

Resolve the branch base, read the confirmed intent and retained plan when present, and list the
cumulative diff. If only publication metadata changed and a matching
attestation already exists, stop: the evidence is still valid and Ship owns
the remaining work.

At entry, omit any step the user told you to skip in plain words; §2 and §3
say how skipped reviewers, adversarial and acceptance-test are handled. Words that ask to skip independent acceptance testing —
"acceptance testing", or the step formerly called "blind run" — mean the
`acceptance-test` step. At station entry, keep the full flow unless the user
instructed a skip. Automatic narrow-change simplification belongs
to finalization and attestation validation. The default is the full
flow: skip a step only when the user
tells you to in plain words, then tell the user in one line which step is
skipped and continue. When you honour such a skip, append one line
`skipped-by-instruction: <step> <YYYY-MM-DD>` to the plan's `## Risks` section,
or the intent's `## Constraints` section when plan is absent or skipped, and commit it
before dependent checks. Commit that line before reviewers read the final digest,
because it changes the digest; a later commit is harmless only when the skip
sends the change to Ship unattested (§5).

## 2. Compute review depth

Use the confirmed intent when spec or plan is skipped. Give reviewers and
testers the retained artifact paths and omitted steps; apply Acceptance
directly when spec is omitted, and use bounded task handoffs when plan is
omitted. Any downstream reference to a spec, plan or its sections applies
only when that artifact is retained; use the intent's Constraints for a
record otherwise assigned to plan Risks. Missing skipped artifacts require
no recovery; all retained verification still applies.

Before every host-native dispatch, the station must resolve the model-and-effort
profile as the [shared dispatch profile](../../references/dispatch-profile.md)
defines and apply its result. Repeat this resolution for every reviewer,
second-vendor reviewer, and acceptance tester dispatch. `<loom-code>` (this plugin's
root) is `${CLAUDE_PLUGIN_ROOT}` on Claude Code; on any other host it is the
directory two levels above this SKILL.md.

On Antigravity CLI or OpenCode, map tool and agent names with
[`../../references/antigravity-tools.md`](../../references/antigravity-tools.md) or
[`../../references/opencode-tools.md`](../../references/opencode-tools.md).

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
complete package suite passing or `package-tests` is skipped by the user's plain-words
instruction, and that it
reports every adversarial program passing or `adversarial` is skipped by the user's
plain-words instruction, each
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

When acceptance testing is needed, finish it and commit its report (§3) before
dispatching the first reviewers. After Build commits completed functional
content, run:

```text
python3 <loom-code>/scripts/loom_checker.py reviewer-count <change-id>
```

The output is the computed reviewer floor: dispatch that many
fresh-context reviewers with distinct agent identities. The checker derives the
floor from the cumulative branch delta and fails closed to two when it cannot
classify the whole change. `finalize-review` recomputes the same policy, and
the PR's verification status reports a mismatch as `stale`; the orchestrator
never declares or overrides it. When `reviewers` is skipped by the user's plain-words
instruction, dispatch no
reviewer and pass no `verdicts`.
- Unless reviewers are skipped, resolve a selected second vendor from the
  standing fixed CLI, the per-change `ask` answer, or a committed
  `user-decided — second-vendor selection-confirmed: <vendor>` plan line.
  Record an accepted `ask` answer with that same line before reviewing, so
  `reviewer-count`, finalization and attestation validation can recompute it.
  With no selection, do not start external execution. With a selection, retain
  at least one incumbent reviewer and dispatch an additional outside reviewer.
  A floor of one rises to two; at a higher floor, the outside reviewer may
  occupy one slot, but cannot replace the incumbent. Finalization requires
  both vendor families in distinct passing verdicts.

Reviewer independence is a quality requirement, not a ledger field. Give each
reviewer the branch base, changed paths, intent, spec when present, plan, and
the applicable lens from `references/lenses.md`. Reviewers return the
structured YAML required by `agents/reviewer.md`; the orchestrator converts
the accepted fields to the temporary JSON consumed by finalization.

<!-- gate: review.external-dispatch -->
For the selected outside reviewer, invoke the named
[`loom-code:external-review`](../external-review/SKILL.md) skill. Give it the
complete reviewer packet, including the same lens from `references/lenses.md`
and the same `agents/reviewer.md` YAML contract used by incumbent reviewers.
Supply an explicit executor, model, effort and model-provider family. A
resolver result of `overrides: null` does not select an outside profile;
choose and verify a complete pair or report `EXECUTION_FAILED`. Never use
the external CLI's default model or effort and never substitute another pair
after rejection.

Before any network-backed discovery, probe or review, give the user the
cost, vendor-egress, readable-scope and local-execution disclosures and retain
their approval in the external skill's JSON consent record. An earlier fixed
setting without these disclosures is insufficient; resolve its confirmation
at the existing intent decision point. Changed executor or readable scope
requires fresh approval. Pass the consent record and exact scope to the shared
runner. A missing or stale record prevents execution. On Codex, run the
installed runner outside the sandbox with narrowly scoped host approval when
the selected CLI requires the existing host login; denial is an authorization
blocker, never a login diagnosis.

The shared runner returns execution status, evidence and raw review output;
it does not judge the review. A failed probe or review is a distinct outside
failure and supplies no verdict. On completion, this station validates the
raw YAML against `agents/reviewer.md`, attributes it to the selected model
family, and accepts only a conforming verdict. One transient executor or
malformed-output retry is allowed for the same digest and reviewer identity;
a second failure ends the episode as `EXECUTION_FAILED`. A rejected explicit
model or effort never triggers a default-model retry.
<!-- /gate -->

## 3. Run acceptance testing

Use acceptance testing when an Acceptance line cannot be settled mechanically.
Acceptance testing means dispatching the `loom-code:acceptance-tester` agent
fresh-context, never an agent that touched any part of the change. Its
`docs/loom/<change-id>/acceptance-test-report.md` is functional content; only
`attestation.json` is publication metadata. Finish acceptance testing and commit
that report on the change branch before the reviewers read the final
functional-content digest, and so before running `finalize-review`. A report
committed after their verdicts is new functional content and needs the next
round. Its evidence file,
`docs/loom/<change-id>/evidence/acceptance-test-evidence.md`, is functional
content too and is committed with the report under the same deadline.
When `acceptance-test` is skipped by the user's plain-words
instruction, run no acceptance testing.
When `acceptance-test` is skipped and so no report exists, tell the user, in the conversation before Ship,
every step skipped by instruction, read from the committed
`skipped-by-instruction:` lines and described in plain words by what it would
have done, not as its record id.

On every dispatch, tell the acceptance tester whether `package-tests` or
`finalize-review` is skipped. Also hand it every finding of severity
`important` or worse that the main agent dismissed. A finding of that
severity dismissed after the tester's last dispatch, when Ship comes next, is
listed in the pull request's Verification section instead. On a re-dispatch after a
fix, also pass the earlier report and evidence file paths and the fix's commit range. The
tester's steps 6-7 govern the suite row and what is re-tested.

Closing review dispatches no adversary and creates no adversarial program.
Build commits the adversarial programs, and its hand-off names each program's
path and command; §5 passes them to `finalize-review`. Do not record a claimed
result; finalization executes them. When `adversarial` is skipped by the user's plain-words
instruction, Build hands
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
content the reviewers just read, including the committed acceptance test
report, into one list. Every fix starts from that
whole list. Findings that share a defect class, named in words taken from the
findings themselves, go to Build as one hand-off that names every one of their
instances; findings of different classes go as separate hand-offs. Every
hand-off from the list goes to Build in the same fix round, before the
reviewers resume. A verdict label such as `NEEDS_REVISION` names no class.

Build scopes each fix to its
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
Only after all executions and verdicts pass does it atomically generate the
attestation bound to the functional-content digest. Commit the generated file
with any remaining publication metadata; publication validates that single
attestation directly.

When a step that `finalize-review` needs (reviewers, adversarial, package-tests)
was skipped by the user's plain-words instruction, skip `finalize-review` and leave the change unattested: tell the
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
findings. Also report every finding of severity `important` or worse
dismissed after the acceptance tester's last dispatch, with its reason. On
PASS, hand the matching attestation to `loom-code:ship`.
