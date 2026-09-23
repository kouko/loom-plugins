# Make each adversarial probe earn its place
originator: kouko
kind: engineering
needs-design: no — adversary contract, station prose and checker rules are skill/gate artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-23
publication: automatic — authorized 2026-09-23 by kouko

## Problem
The adversary is the slowest step of a change — about 9 minutes on the
2026-09-23 docs-only change, against 7 for the implementer and 3.5 for two
reviewers in three rounds — and its output is governed by a floor with no
ceiling, plus a mutation-evidence duty on every update. Across 134 changes in
five repositories it has produced 255 probe files and 1,644 test functions.
Those programs run twice, at the end of Build and in finalize-review, and are
never run again: they sit outside the package suite, so a probe that never
went red buys no protection against a later regression. On the 13
documentation-only changes, no probe program ever caught a defect that reading
did not; on code changes, 37 to 46 per cent did. The floor itself is stated in
six places and three of them disagree about its scope: one limits it to code
changes with no mutation tooling, one states it as what the adversary always
does, one states it for the whole loom family. The same "at least one
adversarial execution" check is written twice in the checker with two
different messages. The user's words for this are 花的時間太久，產生了很多複雜
的自動測試.

## Proposed outcome
The adversary spends its effort where an executed behaviour can fail in a way
reading cannot foresee, states what each program defends against, and leaves
behind only programs that are run again — and each of these rules is stated
once, so the next change to them is one edit rather than six.

## Acceptance
1. A change whose delta the checker already classifies as narrow also skips the adversarial step, through the same mechanism that skips spec, plan and blind-run today; no second definition of "small enough" is introduced anywhere.
2. The boundary that mechanism uses is re-examined against the recorded history in this change's evidence, and either kept with the evidence stated or adjusted, because it now decides the adversarial step as well as the reviewer count.
3. For a change that does run the adversarial step, the adversarial programs committed for it number at most five; the cap has no written-reason escape, because the user can already ask for more, or for the step to be skipped, in plain words (user-decided 2026-09-23: nothing committed today carries such a reason, and adding a field for it was refused as unnecessary structure).
4. Every committed probe program carries a line naming the kind of defect it defends against; its content is free text at this stage, and a program without that line is rejected mechanically.
5. Acceptance 3 and 4 are recomputed by exactly one new checker rule, and the checker's rule list grows by exactly one entry; no existing rule id is retired or renamed.
6. A probe program that caught a defect on its own change is carried into the suite that runs on every later change, and one that caught none is reported and not left in the repository; this is a station rule the closing review checks, and it adds no checker rule.
7. The mutation-evidence duty applies only to a program carried into that suite, and it is stated in one file.
8. No runtime file states a minimum number of adversarial cases: the count a change needs is a ceiling, not a floor, because the `concern:` line and the reviewers already answer what the floor was there for. How many cases a change may commit is stated in exactly one runtime file; every other runtime location that states it today either points at that file or drops the claim, and a check fails the repository if a second statement of it reappears.
9. The agent contract's own trigger text, the three translated READMEs and the repository conventions file may restate the rule in their own words, and a check fails the repository when such a restatement contradicts the single source.
10. The requirement that a change record at least one adversarial execution unless the step was skipped is computed by one shared predicate, not by two copies with different messages.

11. When the checker judges a change narrow, the steps that judgement skips are named to the user in one line as they are skipped, and listed in the pull request, so the cost of the judgement is visible every time and never only in the code.

## Constraints
- The user's plain-words skip stays exactly as it is; nothing here asks for a typed code or narrows what a user may skip.
- The adversary still never fixes the product and never judges its own output.
- Per-artifact-kind recipes stay split as PR #33 left them; only rules that hold for every kind move to the shared protocol.
- No new file is added to the recipes folder, and no folder is nested.
- Probe programs already committed for past changes stay where they are.
- Runtime prose cites no development record of this repository; the industry sources behind these rules are named as provenance only.
- The closed vocabulary for the defect-kind line is deferred: this change collects values, a later change may fix the list.

## Out of scope
- A defect-kind catalogue with a fixed set of allowed values.
- Changing the reviewer count policy itself, beyond re-examining the shared narrow-delta boundary named in Acceptance 2.
- Removing or rewriting the probe programs of past changes.
- Whether the package suite itself should run faster.

## Open questions
- none
