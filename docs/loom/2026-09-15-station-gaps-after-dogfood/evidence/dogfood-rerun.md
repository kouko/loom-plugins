# Dogfood re-run — station gaps after the 3.5.0 dogfood

Change: 2026-09-15-station-gaps-after-dogfood. Evidence for Acceptance 4 (behaviour) and 5 (word budget).

## Method

- Same scenarios, rubric and prompts as the 3.5.0 dogfood (S2, S3 for Build; S7-a for closing review), with the
  contract path pointed at this change's worktree text.
- Executors: fresh general-purpose subagents, session default model, plan-only (no dispatch, edit, commit or test run),
  given only the station contract path and the scenario.
- Auditors: two independent opus subagents, given only the executor outputs and the rubric sections S2, S3, S7-a, plus
  two conditions from Acceptance 4 — the post-fix re-run of the complete package suite and adversarial programs must not
  be listed as a guess (S2, S3), and S7-a must contain no technical design re-look.

## Timeline

1. W1-01 (8459654b) and W1-02 (18d932ef) landed.
2. Re-run 1: S2 and S3 re-ran both checks after the fix citing the new Build sentence, with the suite command taken from
   the `package-tests:` declaration; neither listed the re-run as a guess. S7-a **still inserted a technical design
   re-look**. Its stated reasons: the reviewer contract still said "Round 3 is terminal and occurs only after the
   orchestrator's technical design re-look" (agents/reviewer.md:150-151), and the new §5 sentence "That round is fix
   verification, as in Round 2." clashed with §4's "Round 3 — terminal verification".
3. W1-04 (51561c7b) removed the re-look clause from agents/reviewer.md and replaced the §5 sentence with "No technical
   design re-look precedes that round unless the episode is stuck."
4. Re-run 2 (S7-a only; Build text unchanged since re-run 1): no technical design re-look; the fixed content passes
   Round 3 before finalize-review runs again; NON_CONVERGENT on failure. Remaining guess: whether a finalize failure
   after a clean Round 2 counts as a stuck trigger — the executor assumed not (plan Risk 3, "blocker" undefined).

## Auditor verdicts

| Scenario | Auditor 1 | Auditor 2 |
|---|---|---|
| S2 | CONFORMS — implementer fixes; the suite and all adversarial programs re-run before hand-off as a firm step, not a guess; no new adversary | CONFORMS — fix by implementer; the suite and every adversarial program re-run as a real step, not a guess; hand-off only after all pass (harmless extra: programs run once after the suite had failed) |
| S3 | CONFORMS — the important finding is fixed like a failing check; suite and programs re-run (not a guess); an unresolved finding is listed, never dropped | CONFORMS — finding fixed like a failing check; suite and programs re-run without a new adversary (not a guess); hand-off lists it if unresolved |
| S7-a | CONFORMS — fix returns to Build; Round 3 reviews the fixed content before finalize-review runs again; no technical design re-look | CONFORMS — fix returns to Build; no design re-look; Round 3 reviews the fixed content before finalize-review runs again; only Round 3 verdicts used |

Luck lists:

- Auditor 1: (S7-a) "not stuck" rests on counting only reviewer blockers — counting the finalize failure as a blocker would add a re-look (plan Risk 3); (S3) handing off with an open finding listed was a guess (dogfood FINDING-007, out of scope); (S2) the executor assumed the failure came from this change — judging it pre-existing and handing off would violate S2 (new observation).
- Auditor 2: (S7-a) passed on the "not stuck" reading; reading the stuck triggers the other way would add a re-look (plan Risk 3); (S2) assumed the failure came from this change — treating it as pre-existing could hand off with a failing suite (new observation); (S3) "try to fix first, then list" is a reading of the gate (FINDING-007); (S3) closure checked by reading the diff because re-dispatching the adversary is forbidden.

Both runs grade all three scenarios CONFORMS (Acceptance 4 met). Residual ambiguities are recorded as plan Risk 3 ("blocker" undefined), dogfood FINDING-007 (unresolved adversary findings), and one new observation: Build does not say what to do when an end-of-Build failure predates the change.

## Validity after W1-05

W1-05 (d8e3988b), landed after both re-runs, closed the end-of-Build adversary findings: it rewrote Build step 2's
suite-command sentence to cover an absent declaration and `none`, deleted Build §3's restated hand-off consequence, and
rewrapped one closing-review §5 line without word changes. It extended the step-2 suite-command sentence the S2/S3
executors cited (adding the absent and `none` cases); the declared-value reading they used is unchanged at HEAD. It did
not touch the re-run sentence the S2/S3 trajectories cite or any §4/§5 wording the S7-a trajectory cites, so the verdicts
above still describe the station text at HEAD.

## Word budget (Acceptance 5)

| File | 9906c79c | HEAD |
|---|---|---|
| loom-code/skills/build/SKILL.md | 848 | 848 |
| loom-code/skills/closing-review/SKILL.md | 2104 | 2102 |
| **Combined** | **2952** | **2950** |
| loom-code/agents/reviewer.md (not in the budget) | 1584 | 1575 |

### After merging trunk #16

PR #16 (040e5010, loom-code 3.6.0) merged to main after publication and was merged into this branch. It adds a
`sync-trunk` step to Build §3 and a Round 1 sync paragraph to closing review, 182 station words in total. From the
merge on, Acceptance 5 is measured against that trunk tip, so trunk words are not counted as this change's:

| File | 040e5010 | HEAD after merge |
|---|---|---|
| loom-code/skills/build/SKILL.md + loom-code/skills/closing-review/SKILL.md | 3134 | 3132 |

The merge renumbered Build §3 (the suite step is now step 3); the re-run sentence and the §4/§5 wording the scenarios
cite are unchanged, so the verdicts above still apply.

## Raw outputs

Executor and auditor outputs are kept outside the repository (session scratchpad) and summarised above; the quoted
sentences are verbatim from them.
