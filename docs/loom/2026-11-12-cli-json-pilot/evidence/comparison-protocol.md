# Preregistered preparation-result comparison

Registered before JSON implementation or operator execution on 2026-11-13.
This packet specifies observations, not a passing verdict or a benefit claim.

## Frozen source and candidate binding

Use the genuine prior change checkout at
`c2bab0811a1ba1083e2452d84375d9c02c79bc3a`, with local main at
`21cdc28d0044f642c6b8409b166ed510e24d3a12`. Do not fetch or advance that
checkout's main: doing so would change historical delivery eligibility.
Set the disposable clone's selected origin default to a newly created
`refs/remotes/origin/comparison-base` at that same historical main SHA;
point `refs/remotes/origin/HEAD` at it. Cloning the current candidate otherwise
inherits an origin default containing the delivered historical change and
would invalidate the intended task. This is explicit local fixture metadata,
not a claim about the live server's default branch. Create the comparison ref
only when absent; never overwrite an existing ref or change source worktrees.
The original change is `2026-11-12-cli-guidance-consistency`; its intent,
spec and plan are committed historical artifacts, not newly authored fixtures.
Use a separate disposable snapshot for every task, operator and mode.

Before W3 begins, bind the completed candidate launcher to a full commit SHA
and SHA-256 source inventory in an appended execution-binding section here.
Pin each disposable fixture's relevant artifact hashes against the oracle.
The launcher comes from the candidate; the checked artifacts and repository
come from the frozen historical snapshot. The historical result is not a
review of the new JSON implementation.

Task content, mutations, expected classifications and scoring definitions
below are frozen now. Candidate binding is the only planned later addition.
Any other change needs a separately identified amendment before execution;
never revise expectations after seeing answers.

## Operators and disclosure

Dispatch two fresh non-implementing operators sequentially. Operator A uses
text then JSON; operator B uses JSON then text. Both modes use the same task
order T1 through T6. Each operator completes twelve task runs. Their second
mode is informed by their first: report carryover, not blindness or a causal
population estimate. Neither operator receives expected answers, the oracle,
implementation explanations or prepared command lines. No external paid
executor or remote write is required.

The coordinator prepares isolated task directories and applies only the
declared controlled mutations. Give operators the candidate launcher path,
task directory, assigned mode and the verbatim goal below. They may discover
the command through public help, read the relevant artifacts and make the
requested correction only in their disposable copy. They must not read this
protocol's private scoring companion or other operators' records. Give them
the following answer form without answer values: initial classification,
reason/rule, whether advisory output means success, correction made, final
classification, remaining limitation. Preserve their first interpretation
before allowing a correction or a second check.

## Task goals given verbatim to operators

| ID | Goal |
|---|---|
| T1 | Check the historical change's canonical plan. Explain the outcome and what it does and does not establish. |
| T2 | Check the provided plan copy. Explain any failure, correct only the identified defect using the authentic source supplied, and check it again. |
| T3 | Try the plan check without supplying its required target. Explain the result, discover the missing input and check the historical canonical plan. |
| T4 | Check whether the historical change meets the prerequisites for entering write-plan. Explain the outcome and the meaning of any advisory output. |
| T5 | Check whether the historical change meets write-plan prerequisites. Explain any failure, restore only the affected original content from the supplied authentic source, and check again. |
| T6 | Check whether the historical change meets write-plan prerequisites. Explain any failure and advisory output, restore only the affected original content from the supplied authentic source, and check again. |

For T3 only, the task necessarily specifies the initial missing-operand probe;
disclose that it measures diagnosis/recovery, not spontaneous mistake rate.
In JSON mode, the operator selects the candidate's optional JSON output for
checks; help remains text. Do not supply a complete invocation in either mode.

## Coordinator fixture preparation — withheld from operators

T1, T3 and T4 use unmodified historical artifacts. For T2, copy the genuine
canonical plan to `comparison-plan.md`, then rename the sole
`## Simplicity check` heading to `## Deliberately removed simplicity record`.
For T5, change only the historical intent's confirmed status line to
`status: open`, retaining its original content pin. For T6, apply T2's heading
rename to the canonical plan itself. These are deliberate negative mutations,
not authentic original defects. Supply immutable original files separately
for correction. Hash both original and mutated bytes; do not reconstruct the
whole artifact or invent review evidence. Preserve the original Git history.

## Four preregistered metrics

1. Interpretation errors: score each first answer against the oracle's
   outcome, identified cause and advisory meaning. Count at most one error
   per task answer if any required proposition is wrong; retain the specific
   propositions as annotations. Score the final answer separately, never
   erase the initial error. Missing answers are incomplete, not zero errors.
2. Corrections: count each changed invocation or artifact between an observed
   failed attempt and the next check attempt. A single edit fixing multiple
   lines counts once. Retries without a change count as attempts, not fixes.
   The declared negative starting condition is not itself an operator fix.
3. Operations: count all operator tool invocations from receiving a task to
   its final answer, including reads, help, edits and checks. Also count CLI
   invocations separately. A tool call containing multiple operations must
   list its constituent operations; retain both tool-call and constituent CLI
   counts. Coordinator setup is excluded and logged separately.
4. Output volume: measure actual UTF-8 stdout and stderr bytes separately for
   every CLI invocation, including help and failed attempts. Report task
   check bytes and total CLI bytes separately so discovery costs remain
   visible. File reads and operator prose are excluded, explicitly. Do not
   call byte counts token counts; no token or time saving is promised.

Record exact argv, cwd, timestamp, exit, separated raw streams and first/final
operator answers, with mode, task ID, operator identity and candidate SHA.
Retain setup failures outside task metrics. Report all 24 task runs, per-task
and per-operator results, mode totals, incomplete cases, ties and regressions.
No benefit threshold determines success; Acceptance 3 is an honest comparison.
An unexpected result is evidence or a limitation, never a substituted task.

## Integrity and scope

Keep `comparison-oracle.json` private from operators until both complete.
The coordinator scores their retained answers afterward; independent
acceptance judges that scoring. This packet is not a runtime contract.
No automatic routing, cross-host behavior, fresh-machine installation or
broad efficiency inference is tested. W3 records the actual model/profile
observability rather than guessing a concrete inherited model.

## Execution binding

Pending W2 completion. No operator execution is authorized by this unbound
packet. Append candidate SHA, source inventory hashes and fixture hashes
before dispatching either operator; preserve this preregistration commit.

## Preregistration verification

The coordinator verified the six declared fixtures with installed 3.70.0 text
output before JSON implementation. The observed exits were 0, 1, 2, 0, 1, 1;
T4 and T6 emitted the interface advisory, T5 did not. These are fixture sanity
checks, excluded from operator metrics and not JSON comparison observations.
The setup initially ran checkout outside the new clone and stopped; a corrected
cwd succeeded. The first intake check inherited the candidate's origin default
and reported the historical change delivered; explicitly selecting the frozen
comparison base corrected that fixture setup. Both setup failures remain
disclosed rather than counted as task interpretation errors. Raw fixture
observations remain at `/private/tmp/loom-json-prereg-baseline.json`.

## Bound candidate for W3

Candidate: `2cef40163b6a562971780da6e6fd107289304962` (release 3.71.0).
Preregistration commit remains `030eb89604df322e6dafea25294c76c97edd645e`.

The 66 tracked files under `loom-code/scripts` and `loom-code/contract`
have aggregate SHA-256
`ed77294ca4699ccbd5e099576b7dd47a6e2b3500d8f59700e1846057b8eacbc3`.
Recompute by sorting tracked paths lexicographically, concatenating each
UTF-8 path, NUL, its lowercase content SHA-256 and newline, then hashing that
concatenation with SHA-256. Exclude untracked files; do not normalize bytes.

Fixture originals and deliberate mutation hashes are pinned in
`comparison-oracle.json` under `source_artifacts`; the historical checkout
and selected comparison-base SHA remain frozen above. Every task starts
with a fresh checkout before its declared mutation. The coordinator verifies
those hashes before dispatch. Operators receive only
`operator-instructions.md`, assigned mode order and task directory paths.
No operator has run and no comparison outcome has been observed.

A combined inventory/prose-writing shell request was refused by the local
command guard before execution. The inventory was obtained with a direct Git
read, hashes computed separately and this prose applied with the edit tool;
no command guard or security setting was changed.

## R2 supplemental capture amendment — fixed before supplemental execution

Registered on 2026-11-13, before either supplemental operator starts. This
amendment preserves the confirmed requirements, six tasks, frozen oracle,
candidate `2cef40163b6a562971780da6e6fd107289304962`, historical artifact/base
identities, mutations and four metrics. R1 remains retained and partially
complete; no R1 failure or missing measurement is overwritten by R2.

R1's subprocess recorder omitted initial launcher help and complete native
tool bookkeeping. The first technical repair recovered original native-call
counts and merged bootstrap bytes from the same two R1 sessions, but could
not separate those bootstrap streams or uniquely allocate shared task calls.
Independent acceptance therefore reported Acceptance 3 partly complete.
That repair attempt is spent and stays recorded. R2 is the second technical
repair path for the same comparison obligation, not a newly named task or a
counter/budget reset. No substantive requirement change is claimed.

R2 uses the same original operator identities, separately labeled R2A/R2B,
with fresh identical task directories. A keeps text then JSON; B keeps JSON
then text. Both operators already know R1's outcomes and repairs. This is an
informed supplemental capture exercise, not a replacement blind trial or an
independent replication of efficiency. Report R1 and R2 separately; never
pool them to inflate sample size or claim removed learning effects.

The new capture obligation is mechanical: load the generic subprocess
harness before any launcher call, capture every checker/launcher invocation
including the first launcher help with separate original streams and byte
counts, tag each native tool call with one unambiguous phase, and finish
one task before another starts. A tool call cannot mix tasks or task answer
bookkeeping with a later check. Native tool counts will be independently
recovered from the original R2 sessions after execution; bootstrap, reporting
and coordination stay separately inventoried. The underlying preregistered
metric is unchanged: actual tool calls, not fractional allocations or child
command counts used as substitutes.

The general-purpose measurement harness is temporary infrastructure, not
production code or an adversarial probe: `/private/tmp/loom-json-r2-capture.py`,
SHA-256 `71d0e5a165b88c3a1bf13cb67873b28a4008b5d4b47721c2146cda4a84f135d5`.
It exposes only `run(argv, cwd)` and records supplied arguments/results;
it contains no task commands, interpretation logic or expected answers.
The operator-only packet is `operator-instructions-r2.md`; the oracle remains
withheld. Coordinator fixture creation and hash checks remain setup activity,
outside task metrics. No new paid execution or remote write is introduced.

Before dispatch, commit this amendment and operator packet and verify all
24 R2 fixtures against the unchanged original/mutation hashes. Preserve the
amendment commit, candidate SHA, harness hash, actual operator session IDs,
exact tool/CLI records, initial answers, failures and all R2 deviations.
If capture still fails, retain the limitation and return to independent
acceptance; do not silently rename or restart the experiment. R2 outcomes
are pending at amendment time. This document issues no passing verdict.
