# Loom evidence drift guards — acceptance test evidence (FULL re-run at f155bad5)

Tried on 2026-10-22, in a clean worktree of the project at f155bad5
(`git worktree add --detach <path> f155bad5` from `feat/2026-10-12-loom-evidence-drift-guards`,
detached HEAD `f155bad5f010ee5fb920750b369fce73a74ba13c`; worktree path
`/private/var/folders/pv/m7y9m2v56lg68nl8wtxkbm0c0000gn/T/opencode/at-rerun2-f155bad5`).

This is the FULL re-run after the mechanism fixes at `f155bad5` (the checker
rules themselves changed, so every Acceptance line was re-tested in full,
over every surface each line names).

## Earlier run (25a9d92), superseded

The run at `25a9d92` reported three important findings, all addressed by the
fix commit `f155bad5`:

1. `intake.attestation-coverage` collapsed report rows into a set, so a
   duplicate-only report (every line covered, one line repeated) passed, and
   the recorded `acceptance_status` derived from row presence, never from the
   row's Verdict cell — a line reported `fails` was recorded `works`.
2. The intent-version recompute command used bash process substitution
   `<(...)`, which prints nothing under a minimal POSIX shell.
3. The three new rules had no behaviour unit tests, and the finalize
   `acceptance_status` shape had no regression test.

The evidence below is this run's own output at `f155bad5`; it stands alone.

## Setup

- README "Development" dependencies installed into a fresh `.venv` in the
  clean worktree: `uv venv .venv && uv pip install --python .venv/bin/python
  -r requirements-package-tests.lock` (pytest, pytest-xdist, pyyaml, …).
- Setup check: `loom_checker.py --list-rules` printed the full rule list,
  including `intake.attestation-coverage`, `intake.commit-identity`,
  `intake.intent-version`, `intake.plan-boundary-tests`; worktree
  `git status --porcelain` empty (clean).
- Checker invocation throughout:
  `<worktree>/.venv/bin/python <worktree>/loom-code/scripts/loom_checker.py`.
- Fixture harness: `/private/var/folders/pv/m7y9m2v56lg68nl8wtxkbm0c0000gn/T/opencode/at-rerun2-f155bad5-fixtures/`
  (`harness.py`, `run_line1.py` … `run_prfloor.py`). Each fixture repo:
  `git init -b main`, baseline commit with `docs/loom/KICKOFF-DEFAULTS.md`
  (`- package-tests: python3 -c pass — fixture (2026-09-08)`), fake remote
  refs, a feature branch, committed intent with `intent_confirmed_sha`
  (computed the way capture-intent does: blob sha of the file with the
  `status:` and `intent_confirmed_sha:` lines removed), committed acceptance
  report, and a review-input JSON written outside the repo so the tree stays
  clean. `finalize-review` executed the declared package command
  (`python3 -c pass`) and the committed adversarial probe where the delta
  required one.

## 1. A change whose acceptance report does not account for every intent Acceptance line's identity and status (omission or duplicate included) fails the check, which names the offending line numbers.

Fixture: intent with 3 Acceptance lines; report rows varied; report pinned at
the HEAD being reviewed (so only the coverage rule can fail). Runs through the
real `finalize-review` CLI.

- 1a rows 1–2 only → `exit=1`,
  `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`
- 1b rows 1–4 → `exit=1`,
  `BLOCK intake.attestation-coverage: acceptance test report carries rows for Acceptance lines the intent does not have: 4`
- 1c rows 1,2,2 (duplicate 2, missing 3) → `exit=1`, both named:
  `… no row for Acceptance lines: 3` and
  `… carries duplicate rows for Acceptance lines: 2`
- 1d rows 1,2,3 → `exit=0`, attestation written; recorded
  `acceptance_status: [{"acceptance": 1, "status": "works"}, {"acceptance": 2, "status": "works"}, {"acceptance": 3, "status": "works"}]`
- 1e rows 1,2,2,3 (duplicate-only: every line covered, line 2 appears twice)
  → **`exit=1`**, `BLOCK intake.attestation-coverage: acceptance test report
  carries duplicate rows for Acceptance lines: 2` — the fixed half of finding
  1: rows are counted, not collapsed
  (`_report_rows`/`counts` in
  `loom-code/scripts/loom_checker/rule_checks/evidence_coverage.py:40-127`).
- 1f rows 1,2,3 with row 3 verdict `fails` → `exit=0` (a legal status); the
  recorded `acceptance_status` is now
  `[{"acceptance": 1, "status": "works"}, {"acceptance": 2, "status": "works"}, {"acceptance": 3, "status": "fails"}]`
  — the attestation records the report's stated verdict, not row presence
  (`acceptance_coverage`, `evidence_coverage.py:67-83`).
- 1g rows with `not verified` (row 2) and `NOT_VERIFIED` (row 3) → `exit=0`;
  recorded statuses `not_verified` for both — both spellings accepted
  case-insensitively (`_normalise_verdict`, `evidence_coverage.py:60-64`).
- 1h row 2 verdict `maybe` (no template status) → `exit=1`,
  `BLOCK intake.attestation-coverage: acceptance test report states no Verdict in (works / partly / not verified / fails) for Acceptance lines: 2`
- 1i row 2 verdict `partly` → `exit=0`; recorded
  `{"acceptance": 2, "status": "partly"}`.

Unit tests covering this criterion:
`loom-code/tests/test_evidence_drift_guards.py` — `test_coverage_fails_and_names_a_missing_line`,
`test_coverage_fails_and_names_an_extra_line`,
`test_coverage_fails_and_names_a_duplicated_line`,
`test_coverage_fails_and_names_an_unreadable_verdict`,
`test_coverage_passes_a_complete_report`,
`test_coverage_passes_a_report_in_the_attestation_underscore_spelling`,
`test_coverage_requires_a_report`,
`test_acceptance_status_reads_the_verdict_cell`,
`test_acceptance_status_shape_matches_the_validator_vocabulary`,
`test_acceptance_status_records_not_verified_for_a_missing_row` — all pass
(22 passed in the file).

## 2. An attestation that does not record both the tested commit and the reviewed commit fails; when the two differ in functional content (not evidence files) it fails.

- 2a report without the fixed "Tried on … at <sha>" line → `exit=1`,
  `BLOCK intake.commit-identity: v2 attestation is missing required bookkeeping fields: tested_commit=None reviewed_commit='65b812b4…'; the acceptance test report and closing review must supply them`
- 2b report pinned at the intent-only commit; HEAD later gained
  `scripts/tool.py` (tested `893b74f`, reviewed `45583e1`) → `exit=1`,
  `BLOCK intake.commit-identity: functional content differs between the tested commit 893b74f and the reviewed commit 45583e1; the acceptance evidence was produced on other code than what is being reviewed`
- 2c report pinned at the intent commit; HEAD later gained only
  `docs/loom/l2c_evidence_only/evidence/notes.md` (evidence file) → `exit=0`,
  attestation written; recorded `tested_commit: ad13a37`,
  `reviewed_commit: 2f55b84`, `intent_confirmed_sha: 7e29e20`
  (evidence-only drift passes; whitelist at
  `loom-code/contract/manifest.yaml:13-16`:
  `publication_only_paths: docs/loom/<change-id>/attestation.json,
  docs/loom/<change-id>/acceptance-test-report.md,
  docs/loom/<change-id>/evidence/**`).
- 2d direct calls of `check_commit_identity`: v1
  `{"schema": "loom-attestation/v1"}` → `[]` (skipped, backward compatible);
  v2 `{"schema": "loom-attestation/v2", "reviewed_commit": "0"*40}` →
  `[('intake.commit-identity', 'v2 attestation is missing required bookkeeping fields: tested_commit=None reviewed_commit=\'000…0\'; …')]`
  (`loom-code/scripts/loom_checker/rule_checks/commit_identity.py:20-32`).

Unit tests: `test_evidence_drift_guards.py` —
`test_commit_identity_skips_a_v1_attestation`,
`test_commit_identity_fails_when_a_v2_field_is_missing`,
`test_commit_identity_fails_on_functional_drift`,
`test_commit_identity_ignores_evidence_only_drift`,
`test_commit_identity_passes_identical_functional_content` — pass.

## 3. An attestation whose recorded intent confirmation version no longer matches the intent file fails, and the message names the affected Acceptance items and the re-confirmation path.

- 3a intent edited after confirmation (Acceptance line 2 rewritten) with the
  pin left stale → `exit=1`,
  `BLOCK intake.intent-version: the intent has changed since the attestation pinned its confirmation (recorded 4cfbb8f, current 671cbf9); every Acceptance line of the intent may be affected. recompute it with \`grep -v -e '^status:' -e '^intent_confirmed_sha:' docs/loom/intent/l3a_stale.md | git hash-object --stdin\` and re-confirm the intent before closing review`.
  The recompute command was run under a real POSIX shell (`sh -c`, where
  `/bin/sh` on this machine is dash): `exit=0`, output
  `671cbf969008ce29c3db4bf616831ee12377484d`, which equals
  `intent_identity(intent)` and starts with the message's `current 671cbf9`.
  Control: the pre-fix bash-only form
  `git hash-object <(grep …)` fails under the same shell with
  `sh: syntax error near unexpected token '('` (exit 2) — the fix is
  POSIX-safe (`recompute_command`,
  `loom-code/scripts/loom_checker/rule_checks/intent_version.py:25-31`).
- 3b same edit, pin recomputed to match → `exit=0`, attestation written.
- 3c intent without `intent_confirmed_sha:` → `exit=0` (nothing pinned,
  skipped).
- 3d intent with `status: open` → `exit=0` (no confirmation to compare).

Unit tests: `test_evidence_drift_guards.py` —
`test_intent_version_passes_while_the_intent_is_unchanged`,
`test_intent_version_fails_after_a_post_confirmation_edit`,
`test_intent_version_recovers_by_re_pinning`,
`test_intent_version_skips_an_unpinned_attestation`,
`test_intent_version_skips_an_unconfirmed_intent`,
`test_intent_version_accepts_an_abbreviated_pin`,
`test_recompute_command_works_under_posix_sh` — pass.

## 4. A plan naming a boundary/probe test that does not exist in the change fails the check.

Fixture: intent + plan committed; `loom_checker.py intake write-plan <id>`.
(Unrelated plan rules — field-caps, test-case-pair — also fire on the minimal
fixture; only the presence of `intake.plan-boundary-tests` is asserted.)

- 4a charter 1.1 plan, Risk line `1. Risk: the change breaks at the edge; boundary test W1-04`,
  no such task →
  `BLOCK intake.plan-boundary-tests: Risk lines reference boundary test tasks that don't exist: W1-04`
- 4b same Risk naming W1-02, Task DAG contains
  `**W1-02 Guard Fixture task** boundary test after: W1-01 acceptance: 2`
  → rule does not fire (referenced task exists).
- 4c charter 1.0 plan with dangling `boundary test W9-99` → rule does not
  fire (pre-1.1 exempt).
- 4d the current plan template's Risks hint comment copied verbatim → rule
  does not fire (no false positive on the hint).

Unit tests: `loom-code/tests/test_loom_checker_intake.py` — plan-boundary-tests
tests, pass (171 passed together with `test_loom_checker_cli.py`).

## 5. After closing review, the verdict artifact exists inside the change's own directory, and its master/subordinate relation to the attestation is explicit in the documentation.

Fixture 2c's change directory after `finalize-review`:
`docs/loom/l2c_evidence_only/` contains `acceptance-test-report.md`,
`attestation.json`, `evidence/`. The attestation holds `verdicts`
(reviewer-1/reviewer-2, both PASS), `content_digest` (4445ddd5…), and the
bookkeeping fields (`acceptance_status`, `tested_commit`, `reviewed_commit`,
`intent_confirmed_sha`).
`loom-code/skills/closing-review/SKILL.md:397-407`: "The generated
attestation is the change's verdict record: its `verdicts` field is the filed
verdict artifact, digest-bound and read by Ship, publication and the PR-floor
check. The review input JSON above is temporary — it is not a record and
nothing reads it after finalization — so verdict and attestation stay one
artifact instead of two copies that can drift. Its bookkeeping fields are
bound from the change's own artifacts, not re-typed here: …".
Unit test: `loom-code/tests/test_loom_attestation.py` — passes.

## 6. The checks run again in the pre-publication invalidation check after closing review, not once at the review entrance only.

- 6a the same defective change (report missing row 3): `intake write-plan` →
  no `intake.attestation-coverage` in output (attestation does not exist at
  intake; the attestation-based checks are deferred —
  `command_handlers/intake.py` runs only `check_plan_boundary_tests`);
  `finalize-review` on the same change → `exit=1`,
  `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`
  (runs at the end of closing review, before the attestation is generated).
- 6b valid change finalized, attestation committed → `push --hook` silent
  (`exit=0`); `pr-floor` reports
  `::notice title=verification::valid`. After a late functional commit
  (`scripts/tool_late.py` added post-attestation) → `push --hook` prints
  `loom: verification stale (attestation functional content digest does not
  match the selected tree) (missing: plan); publishing anyway.` and
  `pr-floor` prints
  `::notice title=verification::stale (attestation functional content digest does not match the selected tree)`.
  The invalidation re-run is `verification_status` → `validate_attestation`
  (recomputes the functional-content digest at the pre-publication head),
  used by `publish`, `land`, `push --hook` and `pr-floor`.
- 6c attestation with malformed `acceptance_status`
  (`[{"line": 1, "status": "covered"}]`) committed → `push --hook` prints
  `loom: verification stale (attestation acceptance_status items must have
  'acceptance' and 'status' fields) (missing: plan); publishing anyway.` and
  `pr-floor` prints
  `::notice title=verification::stale (attestation acceptance_status items must have 'acceptance' and 'status' fields)`.

Unit tests: `loom-code/tests/test_verification_status.py` — pass.

## 7. New loom changes created after this change carry the new fields by default in their attestation and acceptance report templates.

- `loom-code/contract/templates/attestation.json` (schema
  `loom-attestation/v2`) carries `intent_confirmed_sha`, `tested_commit`,
  `reviewed_commit`, `acceptance_status`.
- `loom-code/contract/templates/intent.md` and
  `loom-design/skills/capture-intent/templates/intent.md` carry
  `intent_confirmed_sha` with the hash recipe.
- `loom-code/skills/closing-review/references/acceptance-test-report.md`
  carries the fixed
  "Tried on <date>, in a clean copy of the project at <short sha>." line —
  the tested_commit extraction point.
- `loom-code/contract/templates/plan.md` Risks section carries the
  boundary-test hint.
- A brand-new fixture change (`l7_fresh`) finalized at this HEAD generated
  `acceptance_status: [{"acceptance": 1, "status": "works"}, {"acceptance": 2, "status": "works"}, {"acceptance": 3, "status": "works"}]`,
  `tested_commit: 6ea0eae…`, `reviewed_commit: 45a0ef8…`.
  `validate_attestation` on that generated attestation returns `[]` (valid);
  `pr-floor` reports `verification: valid`. The previous shape mismatch
  (`{"line": N, "status": "covered"}` vs the validator's
  `{"acceptance", "status"}`) is gone: `acceptance_coverage` now emits the
  validator vocabulary and the fix has a regression test:
  `loom-code/tests/test_selection_finalize.py::test_finalize_binds_the_report_verdicts_into_acceptance_status`
  (asserts the generated `acceptance_status` shape, `tested_commit` =
  report-head, `reviewed_commit` = finalize-head, validator `[]`) — passes.

## Focused tests run (per criterion; the full package suite is left to finalize-review)

- `test_evidence_drift_guards.py` — 22 passed (rules 1, 2, 3 behaviour).
- `test_selection_finalize.py::test_finalize_binds_the_report_verdicts_into_acceptance_status` — 1 passed (rule 7 generated shape).
- `test_loom_checker_intake.py` + `test_loom_checker_cli.py` — 171 passed (rule 4 + registration).
- `test_loom_attestation.py` + `test_verification_status.py` + `test_review_json_template.py` + `test_acceptance_test_report_shape.py` — 63 passed (rules 5, 6, 7).

257 focused tests passed. The package suite (which runs before the change is
accepted and blocks on failure) is executed by finalize-review; this run does
not substitute for it.
