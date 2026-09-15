# Close the two station-text gaps the Build and closing-review dogfood found — plan
intent: 2026-09-15-station-gaps-after-dogfood@49b348d2
charter: 1.0

## Current State Evidence
- Forward: loom-code/skills/build/SKILL.md:88-91 fixes failing checks and adversary findings inside Build but never says to run the checks again after that fix.
- Reverse: loom-code/skills/build/SKILL.md:103-106 re-runs the suite and adversarial programs only when closing review or finalize-review returns the change.
- Error: loom-code/skills/closing-review/SKILL.md:188-191 ties the technical design re-look to Round 3 itself; §5 :274-277 sends a finalize failure to the next round.
- Data: docs/loom/KICKOFF-DEFAULTS.md:8 declares package-tests, while build/SKILL.md:85 says only "the repository's complete package suite".
- Boundary: loom-code/scripts/test_build_mechanical_checks.py:117-118 and test_review_convergence_contract.py:29-38 pin the wording this change rewrites.

## Task DAG
<!-- When a spec requirement changes after this commit, the un-landed
     tasks it touches are replaced and the reason is named in the commit
     message. Landed tasks stay as they are. -->

Wave 1 — station text and its behavioural check

**W1-01 Build re-runs its checks after every fix and names the suite command**  after: none  acceptance: 1, 3
- Files: loom-code/skills/build/SKILL.md, loom-code/scripts/test_build_mechanical_checks.py
- Test: A1 positive: rerun-trigger-covers-every-fix; negative: returned-change-only-trigger-absent. A3 positive: suite-command-names-package-tests-declaration; negative: suite-step-without-command-source-fails.
- Risk: shorten the existing re-run sentence rather than add one; keep hand-off whitelist and negation pins green; agent-decided.

**W1-02 A finalize failure's next round is fix verification**  after: W1-01  acceptance: 2
- Files: loom-code/skills/closing-review/SKILL.md, loom-code/scripts/test_review_convergence_contract.py
- Test: A2 positive: round2-blockers-still-require-relook-before-round3; negative: finalize-failure-round-requires-no-relook.
- Risk: edits gate review.bounded-episode text; move the re-look into the stuck rule, keep lowercase pinned phrases; agent-decided.

**W1-04 Remove the remaining Round-3 re-look coupling**  after: W1-02  acceptance: 2
- Files: loom-code/agents/reviewer.md, loom-code/skills/closing-review/SKILL.md, loom-code/scripts/test_review_convergence_contract.py
- Test: A2 positive: finalize-failure-round-states-no-relook-unless-stuck; negative: reviewer-contract-ties-no-relook-to-round3.
- Risk: dogfood re-run S7-a still re-looked, citing reviewer.md:150-151 and the §5 "fix verification" name clashing with Round 3; delete-first; agent-decided.

**W1-03 Dogfood re-run and word budget evidence**  after: W1-04  acceptance: 4, 5
- Files: docs/loom/2026-09-15-station-gaps-after-dogfood/evidence/dogfood-rerun.md
- Test: A4 positive: s2-s3-s7a-conform-in-blind-audit; negative: executor-listing-rerun-as-guess-fails. A5 positive: combined-words-not-above-2952; negative: added-sentence-over-budget-fails.
- Risk: fresh executors read the worktree text; two blind auditor runs absorb judge variance; baseline 848+2104 words at 9906c79; agent-decided.

Wave 2 — release

**W2-01 loom-code 3.5.1 patch release**  after: W1-03  acceptance: 6
- Files: loom-code/CHANGELOG.md, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/plugin.json, README.md, loom-code/README*.md, loom-code/scripts/test_write_plan_station_text.py
- Test: A6 positive: package-suite-and-mechanism-check-green; negative: checker-code-diff-is-empty.
- Risk: patch bump via sync_codex_manifests.py; version pins move with it; loom-design unchanged; agent-decided.

## Questions asked
① — what — Restated the two station-text gaps (no re-run after an in-Build fix; design re-look after a finalize failure) plus the suite-command source and the 6 Acceptance lines in plain words; asked "以上內容對嗎？" — answered 「對」.
① — consequence — Answering yes authorizes a later non-forced push and Ready PR after Review and publication checks pass; merge stays separate; the user may opt out before publication — answered 「對」.

## Risks
1. Another open worktree (feat/2026-09-15-sync-main-before-review) may edit closing-review; rebase before closing review and re-check the §4/§5 wording.
2. The previous change's committed mutation probe anchors on the old re-run sentence; it is historical evidence outside the package suite and stays untouched; agent-decided.
3. "blocker" stays undefined, so a reader could still count a finalize failure toward the stuck rule; the new §5 sentence argues against it but cannot rule it out.
4. "every fix" may be over-applied to per-task fixes during implementation; the worst case is extra suite runs, not a wrong hand-off.
