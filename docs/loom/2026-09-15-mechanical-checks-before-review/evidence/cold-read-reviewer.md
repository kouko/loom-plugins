# Cold read — reviewer contract

Contract files: `loom-code/agents/reviewer.md`, `loom-code/skills/closing-review/references/lenses.md`. Commit reviewed: `a8552878` ("feat(loom-code): reviewers leave suite and adversarial runs to Build and finalization").

## Commands run

```
cat docs/loom/KICKOFF-DEFAULTS.md
git show a8552878 --stat
git show a8552878
find docs/loom -iname "*mechanical-checks*" -type f
find docs/loom/2026-09-15-mechanical-checks-before-review -type f
python3 --version
which pytest
python3 -m pytest --version
find . -iname "PRINCIPLES.md" -maxdepth 3
python3 -m pytest loom-code/scripts/test_reviewer_mechanical_evidence.py -v
grep -n -i "package suite\|adversarial program\|PASS_WITH_NOTES\|not run\|did not run" loom-code/agents/reviewer.md loom-code/skills/closing-review/references/lenses.md
grep -n -i "engineering\|ratified" PRINCIPLES.md
grep -n -i "reviewer" PRINCIPLES.md
```

(Read-only file reads of `docs/loom/intent/2026-09-15-mechanical-checks-before-review.md` and `docs/loom/2026-09-15-mechanical-checks-before-review/plan.md` were done with the Read tool, not the shell.)

## Did the reader run the complete package suite or any adversarial program?

No. The contract decides this, not my own judgment:

`loom-code/agents/reviewer.md:71-72` — "In every round, you never run the complete package suite or the adversarial programs: both run mechanically at the end of Build, and `finalize-review` executes them again and records the result."

I never ran `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` (the `package-tests:` command in `docs/loom/KICKOFF-DEFAULTS.md`), and I ran no adversarial program.

## Changed test files run

- `loom-code/scripts/test_reviewer_mechanical_evidence.py` (new file in this commit) — run directly with `python3 -m pytest`. Both tests executed and passed, none skipped:
  - `test_reviewer_text_runs_changed_test_files_and_flags_skips` — PASSED
  - `test_no_reviewer_or_lens_text_requires_suite_run_or_downgrade` — PASSED

No other test files were added or changed by this commit (the other two changed files are prose contracts, not test files), so no changed test file was skipped.

## Citations

I cited `PRINCIPLES.md:10` ("Quality comes from machines, not from the user's sign-off: a mechanically computed reviewer floor ... plus a blind run ... and an adversarial pass ...") for the `principles-conformance` dimension. I opened it — read via `grep -n -i "reviewer" PRINCIPLES.md` and confirmed the surrounding lines with `grep -n -i "engineering\|ratified" PRINCIPLES.md`.

A citation I did not open: `lenses.md`'s "Settled by" column names "Beck, *Test-Driven Development* (2002)" as the source for the `tests` dimension. I did not open that book, and my verdict below does not rest any claim on it — the `tests` dimension score instead rests on running the changed test file myself. The contract line that governs a citation I did not open:

`loom-code/agents/reviewer.md:87-88` — "**Open every source you cite.** A citation you did not read is an `incorrect-fact` finding waiting to be made against you."

Per `lenses.md`'s docs dimensions, an unopened citation used to support a claim is exactly the `incorrect-fact` case: "A citation that does not support its claim — open the source and read the cited span before scoring." Had I cited Beck's book to justify a score without opening it, that citation would itself earn an `incorrect-fact` finding against this review, severity `important` (a fact a checker/reader relies on) unless it also changed the verdict, in which case `fatal`.

## Verdict

```yaml
verdict: PASS
lens: code
reviewed_sha: a8552878
dimension_scores:
  security: PASS
  architecture: PASS
  correctness: PASS
  naming: PASS
  tests: PASS
  refactoring: PASS
  cross-task-coherence: PASS
  external-surface-grounding: PASS
  principles-conformance: PASS
  deliberate-simplification: PASS
  deletion-first: PASS
findings: []
notes:
  - "correctness/tests: verified against Acceptance 4 of docs/loom/intent/2026-09-15-mechanical-checks-before-review.md by reading the full text of both edited contract files (not just the diff) and by running the one added test file; I did not run the repository's package-tests command or any adversarial program, per the contract's own instruction not to."
  - "cross-task-coherence: this commit is the whole delta for task W1-01 per docs/loom/2026-09-15-mechanical-checks-before-review/plan.md; no sibling task's diff exists yet to compare against, so there was nothing to find here, not a gap I skipped."
  - "principles-conformance: checked against PRINCIPLES.md:10 (reviewer floor / blind run / adversarial pass guarantee); the change relocates when the adversarial pass runs but does not remove it, and does not touch reviewer-count computation, so no violation."
```

## Ambiguities

None. The two contract files, read in full, gave an unambiguous instruction for every step this task required (which test files to run, what "never run the suite" means, what citation-opening requires, and what the output shape is).
