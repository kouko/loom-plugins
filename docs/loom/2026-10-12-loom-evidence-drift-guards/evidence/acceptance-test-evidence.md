# Loom evidence drift guards — acceptance test evidence (re-run at 25a9d92)

Tried on 2026-10-22, in a clean worktree of the project at 25a9d92
(`git worktree add` from `feat/2026-10-12-loom-evidence-drift-guards`, detached HEAD 25a9d929;
worktree path `/private/var/folders/pv/m7y9m2v56lg68nl8wtxkbm0c0000gn/T/opencode/at-rerun-wt`).

Setup followed the repo's README "Development" section: dependencies installed
from `requirements-package-tests.lock` into a fresh `.venv` in the clean
worktree (`uv venv .venv && uv pip install --python .venv/bin/python -r requirements-package-tests.lock`);
the checker ran from the worktree with that python. Setup check: `loom_checker.py --list-rules`
printed the full rule list including `intake.attestation-coverage`,
`intake.commit-identity`, `intake.intent-version`, `intake.plan-boundary-tests`;
worktree `git status --porcelain` empty (clean).

Fixture harness: `/private/var/folders/pv/m7y9m2v56lg68nl8wtxkbm0c0000gn/T/opencode/at-rerun-fixtures/`
(`harness.py`, `run_line1.py`, `run_line2.py`, `run_line3.py`, `run_line4.py`,
`run_line567.py`, `run_prfloor.py`). Each fixture repo: `git init -b main`, baseline
commit with `docs/loom/KICKOFF-DEFAULTS.md` (`- package-tests: python3 -c pass — fixture (2026-09-08)`),
fake remote refs (`update-ref refs/remotes/origin/main HEAD` + `symbolic-ref refs/remotes/origin/HEAD`),
a feature branch, committed intent with `intent_confirmed_sha` (computed the way
`capture-intent` does: blob sha of the file with the `status:` and
`intent_confirmed_sha:` lines removed), committed acceptance report, and a
review-input JSON written outside the repo so the tree stays clean.
`finalize-review` executed the declared package command (`python3 -c pass`) and
the committed adversarial probe where the delta required one.

Checker invocation throughout: `<worktree>/.venv/bin/python <worktree>/loom-code/scripts/loom_checker.py`.

## 1. A change whose acceptance report does not account for every intent Acceptance line's identity and status (omission or duplicate included) fails the check, which names the offending line numbers.

Fixture: intent with 3 Acceptance lines; report rows varied; report pinned at the
HEAD being reviewed (so only the coverage rule can fail).

- 1a rows 1–2 only → `exit=1`,
  `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`
- 1b rows 1–4 → `exit=1`,
  `BLOCK intake.attestation-coverage: acceptance test report carries rows for Acceptance lines the intent does not have: 4`
- 1c rows 1,2,2 (duplicate 2, missing 3) → `exit=1`,
  `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`
- 1d rows 1,2,3 → `exit=0`, `wrote docs/loom/l1d_complete/attestation.json for ae536990…`
- 1e rows 1,2,2,3 (duplicate-only: every line covered, line 2 appears twice) → `exit=0`,
  `wrote docs/loom/l1e_dup_only/attestation.json for 24f676fd…` — **duplicates are not
  detected when all lines are covered**; the row set collapses under set-based parsing
  (`_get_report_acceptance_numbers` in `loom-code/scripts/loom_checker/rule_checks/evidence_coverage.py:31`).
  The intent's Acceptance 1 explicitly includes duplicates ("含省略或重複條目"), so this is a gap.
- 1f rows 1,2,3 with row 2's verdict cell `fails` → `exit=0`, attestation written;
  the recorded `acceptance_status` is
  `[{"acceptance": 1, "status": "works"}, {"acceptance": 2, "status": "works"}, {"acceptance": 3, "status": "works"}]`
  — the recorded status is derived from row *presence* (`evidence_coverage.py:43-48`),
  never from the row's verdict cell, so a line reported as `fails` or `not verified`
  is recorded as `works` in the durable attestation.

## 2. An attestation that does not record both the tested commit and the reviewed commit fails; when the two differ in functional content (not evidence files) it fails.

- 2a report without the fixed "Tried on … at <sha>" line → `exit=1`,
  `BLOCK intake.commit-identity: v2 attestation is missing required bookkeeping fields: tested_commit=None reviewed_commit='22328ea8…'; the acceptance test report and closing review must supply them`
- 2b report pinned at the intent-only commit; HEAD later gained `scripts/tool.py`
  (tested `be161be`, reviewed `6ba7c2c`) → `exit=1`,
  `BLOCK intake.commit-identity: functional content differs between the tested commit be161be and the reviewed commit 6ba7c2c; the acceptance evidence was produced on other code than what is being reviewed`
- 2c report pinned at the intent commit; HEAD later gained only
  `docs/loom/l2c_evidence_only/evidence/notes.md` (evidence file) → `exit=0`,
  attestation written; recorded `tested_commit: 57f0e87`, `reviewed_commit: 62c6d4c`,
  `intent_confirmed_sha: 7e29e20` (evidence-only drift passes).
- 2d direct calls of `check_commit_identity`: v1 `{"schema": "loom-attestation/v1"}`
  → `[]` (skipped, backward compatible); v2 `{"schema": "loom-attestation/v2", "reviewed_commit": "0"*40}`
  → `[('intake.commit-identity', 'v2 attestation is missing required bookkeeping fields: tested_commit=None reviewed_commit=\'000…0\'; …')]`
  (`loom-code/scripts/loom_checker/rule_checks/commit_identity.py:20-32`).

## 3. An attestation whose recorded intent confirmation version no longer matches the intent file fails, and the message names the affected Acceptance items and the re-confirmation path.

- 3a intent edited after confirmation (Acceptance line 2 rewritten) with the pin left
  stale → `exit=1`,
  `BLOCK intake.intent-version: the intent has changed since the attestation pinned its confirmation (recorded 4cfbb8f, current 671cbf9); every Acceptance line of the intent may be affected. recompute it with \`git hash-object <(grep -v -e '^status:' -e '^intent_confirmed_sha:' docs/loom/intent/l3a_stale.md)\` and re-confirm the intent before closing review`.
  The recompute command, run in the fixture with `bash -c`, output
  `671cbf969008ce29c3db4bf616831ee12377484d` — exactly the message's `current` sha.
  (Note: the command uses bash process substitution `<(...)`; run under `sh`/POSIX
  shell it produces nothing. `intent_version.py:16-18`.)
- 3b same edit, pin recomputed to match → `exit=0`, attestation written.
- 3c intent without `intent_confirmed_sha:` → `exit=0` (nothing pinned, skipped).
- 3d intent with `status: open` → `exit=0` (no confirmation to compare).

## 4. A plan naming a boundary/probe test that does not exist in the change fails the check.

Fixture: intent + plan committed; `loom_checker.py intake write-plan <id>`.
(Unrelated plan rules — field-caps, test-case-pair — also fire on the minimal fixture;
only the presence of `intake.plan-boundary-tests` is asserted.)

- 4a charter 1.1 plan, Risk line `1. Risk: the change breaks at the edge; boundary test W1-04`,
  no such task → `BLOCK intake.plan-boundary-tests: Risk lines reference boundary test tasks that don't exist: W1-04`
- 4b same Risk naming W1-02, Task DAG contains
  `**W1-02 Guard Fixture task** boundary test after: W1-01 acceptance: 2`
  → rule does not fire (referenced task exists).
- 4c charter 1.0 plan with dangling `boundary test W9-99` → rule does not fire (pre-1.1 exempt).
- 4d the current plan template's Risks hint comment copied verbatim → rule does not fire
  (no false positive on the hint).
- Unit tests: `loom-code/tests/test_loom_checker_intake.py` — 5 plan-boundary-tests tests, pass.

## 5. After closing review, the verdict artifact exists inside the change's own directory, and its master/subordinate relation to the attestation is explicit in the documentation.

Fixture 2c's change directory after `finalize-review`:
`docs/loom/l2c_evidence_only/` contains `acceptance-test-report.md`, `attestation.json`, `evidence/`.
The attestation holds `verdicts` (reviewer-1/reviewer-2, both PASS), `content_digest`
(4445ddd5…), and the bookkeeping fields. `loom-code/skills/closing-review/SKILL.md:397-406`:
"The generated attestation is the change's verdict record: its `verdicts` field
is the filed verdict artifact, digest-bound and read by Ship, publication and
the PR-floor check. The review input JSON above is temporary — it is not a
record and nothing reads it after finalization — so verdict and attestation
stay one artifact instead of two copies that can drift. Its bookkeeping fields
are bound from the change's own artifacts, not re-typed here …".
Unit test: `loom-code/tests/test_loom_attestation.py::test_finalize_review_runs_and_writes_matching_attestation` passes.

## 6. The checks run again in the pre-publication invalidation check after closing review, not once at the review entrance only.

- 6a the same defective change (report missing row 3): `intake write-plan` → no
  `intake.attestation-coverage` in output (attestation does not exist at intake; the
  attestation-based checks are deferred — `command_handlers/intake.py:95-98` runs only
  `check_plan_boundary_tests`); `finalize-review` on the same change → `exit=1`,
  `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`
  (runs at the end of closing review, before the attestation is generated).
- 6b valid change finalized, attestation committed → pre-publication checks report the
  attestation as **valid**: `pr-floor --body-file <nine-heading body> --base <root> --head <HEAD> --branch feat/l6b_predate`
  → `::notice title=verification::valid`. After a late functional commit
  (`scripts/tool_late.py` added post-attestation) → `push --hook` prints
  `loom: verification stale (attestation functional content digest does not match the selected tree) (missing: plan); publishing anyway.`
  and `pr-floor` prints `::notice title=verification::stale (attestation functional content digest does not match the selected tree)`.
  The invalidation re-run is `verification_status` → `validate_attestation`
  (`attestation.py:60-63` recomputes the functional-content digest at the pre-publication
  head), used by `publish`, `land`, `push --hook` and `pr-floor`.
- 6c attestation with malformed `acceptance_status` (`[{"line": 1, "status": "covered"}]`)
  committed → `pr-floor` prints
  `::notice title=verification::stale (attestation acceptance_status items must have 'acceptance' and 'status' fields)`
  — the pre-publication check reads the new bookkeeping fields, so the shape fix
  (`14ed02dc`) is enforced there, not only at finalize.

## 7. New loom changes created after this change carry the new fields by default in their attestation and acceptance report templates.

- `loom-code/contract/templates/attestation.json` (schema `loom-attestation/v2`) carries
  `intent_confirmed_sha`, `tested_commit`, `reviewed_commit`, `acceptance_status`.
- `loom-code/contract/templates/intent.md` and `loom-design/skills/capture-intent/templates/intent.md`
  carry `intent_confirmed_sha: <sha7>` with the hash recipe.
- `loom-code/skills/closing-review/references/acceptance-test-report.md` carries the fixed
  "Tried on <date>, in a clean copy of the project at <short sha>." line — the tested_commit
  extraction point.
- `loom-code/contract/templates/plan.md` Risks section carries the boundary-test hint.
- A brand-new fixture change (`l7_fresh`) finalized at this HEAD generated
  `acceptance_status: [{"acceptance": 1, "status": "works"}, {"acceptance": 2, "status": "works"}, {"acceptance": 3, "status": "works"}]`,
  `tested_commit: d6189ae…`, `reviewed_commit: 6b031ef…`, `intent_confirmed_sha: <pin>`.
  `validate_attestation` on that generated attestation returns `[]` (valid); `pr-floor`
  reports `verification: valid`. The shape mismatch that failed the previous run
  (`{"line": N, "status": "covered"}` vs validator's `{"acceptance", "status"}`) is gone:
  `acceptance_coverage` now emits the validator vocabulary
  (`rule_checks/evidence_coverage.py:43-48`, fix `14ed02dc`).
- Focused tests: `loom-code/tests/test_review_json_template.py` (templates carry the
  fields), `test_verification_status.py`, `test_acceptance_test_report_shape.py`,
  `test_loom_checker_cli.py` (rule registration), `test_loom_checker_intake.py`,
  `test_loom_attestation.py` — all pass.
- Gap: no test asserts the *generated* `acceptance_status` shape from the finalize path
  (the fix `14ed02dc` has no regression test); the finalize unit test's fixture has no
  intent file so `acceptance_status` stays `[]` there. And no unit test exists for the
  coverage, commit-identity, or intent-version rules themselves — only CLI registration
  and the plan-boundary-tests rule have behaviour tests.

## Package suite note

Per the acceptance-tester protocol the full package suite is left to `finalize-review`.
The criteria were exercised by the fixture runs above plus the focused test files:
`test_loom_checker_intake.py`, `test_loom_checker_cli.py`, `test_loom_attestation.py`,
`test_verification_status.py`, `test_review_json_template.py`,
`test_acceptance_test_report_shape.py` — 234 passed (pytest run recorded above).
The package suite runs before the change is accepted and blocks on failure; this run
does not substitute for it.
