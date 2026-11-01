# Loom evidence drift guards — acceptance test evidence

Tried on 2026-11-01, in a clean copy of the project at
81d3f31bde5b7db2d045cdafc68d5fa2998e3420 (`git worktree add <tmp> HEAD`,
detached at that exact commit; every exercise below ran inside that clean
copy or in a second worktree at 771d9d91, never in the working repo).

HEAD at test time: `81d3f31bde5b7db2d045cdafc68d5fa2998e3420`
(feat/2026-10-12-loom-evidence-drift-guards post-merge: merge of
origin/main into the branch at 13bd8e52, then the fix commit 81d3f31b).

Registration check (line 1/6 prerequisite):
```
$ python3 loom-code/scripts/loom_checker.py --list-rules
intake.attestation-coverage  Acceptance test report must have a row for each intent Acceptance line with valid Verdict status (works/partly/not_verified/fails).
intake.commit-identity       Functional content diff between tested_commit and reviewed_commit in attestation must be limited to evidence files only.
intake.intent-version        Intent Acceptance lines must match those recorded at confirmation time (intent_confirmed_sha).
intake.plan-boundary-tests   Each Risk line in plan (charter 1.1+) should have a corresponding boundary test task.
```
The four rules are registered in loom-code/scripts/loom_checker/rules.py,
wired into intake at command_handlers/intake.py:95-100 and re-run by the
finalize block at command_handlers/finalize.py:444-449.

Unit tests (run in the clean copy):
```
$ python3 -m pytest loom-code/tests/test_evidence_drift_guards.py -q
22 passed in 1.93s
$ python3 -m pytest loom-code/tests/test_loom_checker_intake.py loom-code/tests/test_selection_finalize.py -q
177 passed in 85.80s
```

## 1. acceptance report 未逐條交代身分與狀態 → 檢查失敗並指出條號

Exercised `check_attestation_coverage` (rule_checks/evidence_coverage.py,
the intake.attestation-coverage rule) against a synthetic three-line intent
(1/2/3), writing each broken report to the change's real report path:

| report shape | result |
|---|---|
| rows 1,2 only (line 3 missing) | BLOCK `intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3` |
| row 2 duplicated | BLOCK `... duplicate rows for Acceptance lines: 2` |
| extra row 8 | BLOCK `... rows for Acceptance lines the intent does not have: 8` |
| row 2 verdict cell `OK I guess` | BLOCK `... states no Verdict in (works / partly / not verified / fails) for Acceptance lines: 2` |
| rows 1..3, verdicts works/not verified/fails | no failures |

Then the real change's own report at this HEAD (7 rows for 7 lines, all
`works`): `check_attestation_coverage(...)` → no failures.

## 2. attestation 未記錄被測/被審查 commit、兩者功能內容不同 → 檢查失敗

Exercised `check_commit_identity` (rule_checks/commit_identity.py, the
intake.commit-identity rule) against four real commits made inside the
clean copy (whole-tree digests via loom_checker/digest.py, the publication
whitelist from loom-code/contract/manifest.yaml):

- T 99a178f7 — synthetic baseline ("tested commit")
- E 3dc3854f — T plus one line changed in
  docs/loom/2026-10-12-drift-synthetic/evidence/acceptance-test-evidence.md only
- P d5223792 — T plus one new file
  docs/loom/2026-10-12-drift-synthetic/evidence/probes/probe_a.py
- F 90d8a9b3 — T plus a functional edit to synthetic-src/module.py

| attestation | result |
|---|---|
| v2, tested_commit missing | BLOCK `v2 attestation is missing required bookkeeping fields: tested_commit=None reviewed_commit='99a178f...'; the acceptance test report and closing review must supply them` |
| v2, reviewed_commit missing | BLOCK same message, naming the missing reviewed_commit |
| tested T, reviewed E (evidence file only) | no failures |
| tested T, reviewed P (probe program only) | BLOCK `functional content differs between the tested commit 99a178f and the reviewed commit d522379; the acceptance evidence was produced on other code than what is being reviewed` — this is the corrected whitelist (`evidence/*`, not `evidence/**`) working: evidence/probes/ stays functional content |
| tested T, reviewed F (source change) | BLOCK same message naming 99a178f and 90d8a9b |
| v1 schema, no bookkeeping fields | no failures (exempt) |

## 3. intent 確認版本與現況不符 → 檢查失敗並指出受影響條目與重確認路徑

Exercised `check_intent_version` (rule_checks/intent_version.py, the
intake.intent-version rule) on the synthetic intent:

- pin = intent_identity(intent) = 6d3bc70ae00d; attestation carrying it → no failures.
- attestation with `intent_confirmed_sha: None` → no failures (optional field).
- after editing Acceptance line 2, same attestation → BLOCK:
  `the intent has changed since the attestation pinned its confirmation
  (recorded 6d3bc70, current e907f1f); every Acceptance line of the intent
  may be affected. recompute it with `grep -v -e '^status:' -e
  '^intent_confirmed_sha:' docs/loom/intent/2026-10-12-drift-synthetic.md |
  git hash-object --stdin` and re-confirm the intent before closing review`
  — names both versions, all acceptance lines, and the recompute path.
- after recomputing the pin → no failures.
- status line changed to `status: open`, stale pin → no failures (nothing
  confirmed to compare with).

## 4. plan 具名的 boundary test 不存在 → 檢查失敗

Exercised through the real CLI in the clean copy:

```
$ python3 loom-code/scripts/loom_checker.py intake write-plan 2026-10-12-drift-synthetic
BLOCK intake.plan-boundary-tests: Risk lines reference boundary test tasks that don't exist: W9-99
exit=1
```
(the plan's Risks item 1 named `a boundary test in W9-99`; no such task).

Pass case — same plan with the risk naming W1-01, whose header carries the
suffix marker the plan template documents (`**W1-01 Boundary test for the
risky path**  after: none  boundary test  acceptance: 1`):
```
$ python3 loom-code/scripts/loom_checker.py intake write-plan 2026-10-12-drift-synthetic
exit=0
```
Exemptions (direct rule call): plan without a charter line → []; charter
1.0 → []. Plan template (loom-code/contract/templates/plan.md lines 31-35)
documents the required suffix marker, so the template hint does not misfire.

Observed quirk (reported as an open question): a task whose title alone
says "Boundary test ..." but whose suffix lacks the marker is NOT
recognized — `**W1-01 Boundary test for the risky path**  after: none
acceptance: 1` still BLOCKs `... don't exist: W1-01`.

## 5. verdict 產物在 change 目錄內、與 attestation 的主從關係明確

- The change's own store holds docs/loom/2026-10-12-loom-evidence-drift-guards/
  attestation.json with `verdicts: [reviewer-1, reviewer-2]` (both PASS) —
  the filed verdict artifact lives inside the change directory.
- loom-code/skills/closing-review/SKILL.md at this HEAD, section "5.
  Finalize" (lines ~390-441): reviewer output goes to "a temporary JSON
  input outside the repository"; `finalize-review` "atomically generate[s]
  the attestation bound to the functional-content digest"; "publication
  validates that single attestation directly" (line ~441). The master
  artifact is the attestation; the input is explicitly temporary.
- No verdict artifact exists at the repo root.

Observation (reported as an open question): the change's own store still
contains a committed review-input.json (from earlier rounds) whose verdicts
duplicate the attestation's; validate_attestation never reads it, so it
cannot drift the record, but the current document calls such input
temporary and outside the repository.

## 6. 檢查在發布前失效檢查中再次執行

(a) Review entrance is not where the attestation-based checks run:
```
$ python3 loom-code/scripts/loom_checker.py intake write-plan 2026-10-12-loom-evidence-drift-guards
exit=0
```

(b) The finalize block (command_handlers/finalize.py lines 413-450, the
EVIDENCE DRIFT GUARD CHECKS) re-runs all three rules when the attestation
is written. Reproduced verbatim on the synthetic change:
- report missing row 3 → BLOCK `intake.attestation-coverage: ... no row for
  Acceptance lines: 3`;
- complete report (Tried-on line naming tested commit 99a178f) → no
  failures; the block's regex extracted tested_commit from the report's
  `Tried on ... at <sha>` line and built acceptance_status from the rows.

(c) Pre-publication invalidation check (`verification_status` →
`validate_attestation`, loom-code/scripts/loom_checker/verification.py,
run by publish/land/hooks/CI) re-validates the committed attestation:
- in a worktree at 771d9d91 (the commit that wrote the v2 attestation),
  delta scoped to that change (`base=771d9d91^`): `valid`;
- `validate_attestation` on the untouched attestation there → [];
- at the new HEAD 81d3f31b: `stale (attestation functional content digest
  does not match the selected tree)` — the merged functional content
  (30+ commits plus the fix) invalidates the earlier attestation;
- acceptance_status element rewritten to `"ship-it"` → `push.attestation:
  attestation acceptance_status has invalid status: 'ship-it'` — the
  pre-publication validator catches a malformed status cell.

## 7. 新變更的模板預設帶有上述欄位

- loom-code/contract/templates/attestation.json carries schema
  loom-attestation/v2 with keys: acceptance_status, change_id,
  content_digest, executions, findings, intent_confirmed_sha,
  reviewed_commit, selection, tested_commit, verdicts.
- loom-code/skills/closing-review/references/acceptance-test-report.md
  pins the `Tried on <date>, in a clean copy of the project at <short sha>`
  line and the one-row-per-Acceptance table with the fixed Verdict words.
- loom-design/skills/capture-intent/templates/intent.md line 8 pre-writes
  `intent_confirmed_sha: <sha7>` with the recompute recipe.
- Population is exercised: the finalize block (line 6b above) filled
  tested_commit from the report's Tried-on line and acceptance_status from
  the rows; the real change's own committed attestation shows the fields
  populated (tested_commit 288d9d58, reviewed_commit e7509a6d,
  intent_confirmed_sha null because this change predates the mechanism,
  acceptance_status 7 x works).

## Package suite

Command (run once, in the clean copy, `uv` 0.13.4, node v22.23.1):
```
$ uv run --isolated --with-requirements requirements-package-tests.lock \
    python scripts/run_package_tests.py --loom-family -q
exit=0
```
Result: 1005 pytest tests passed across the four test roots, shell tests
all PASS, no FAILED/ERROR anywhere in the log
(553 lines, saved at <tmp>/at-drift-scratch/package-suite.log).
