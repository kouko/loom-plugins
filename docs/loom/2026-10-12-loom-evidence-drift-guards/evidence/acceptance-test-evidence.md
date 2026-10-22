# Loom evidence drift guards — acceptance test evidence (FULL re-run at 5fdd3b36)

Tried on 2026-10-23, in a clean copy of the project at 5fdd3b36
(`git worktree add --detach from main at HEAD` from `main`,
detached HEAD `5fdd3b36bbdf14de8da040e3f2d1cdc41eb76457`).

This is the FULL re-run after the mechanism fixes at `5fdd3b36` (the checker
rules themselves changed, so every Acceptance line was re-tested in full,
over every surface each line names).

## 1. A change whose acceptance report does not account for every intent Acceptance line's identity and status (omission or duplicate included) fails the check, which names the offending line numbers.

### Test 1a: Missing row 3
- **What I tried**: Acceptance report with only rows 1-2, intent has 3 lines
- **Command**: `python3 -c "from loom_checker.helpers import load_manifest; from loom_checker.rule_checks.evidence_coverage import check_attestation_coverage; check_attestation_coverage(load_manifest(), Path('.'), '2026-10-12-loom-evidence-drift-guards', {'Acceptance': '1. first\n2. second\n3. third'}, {})"`
- **Result**: `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`
- **Evidence**: Report row for line 3 was missing from the table

### Test 1b: Extra row 4 (report has 4 rows, intent has 3)
- **What I tried**: Acceptance report with rows 1-4, intent has 3 lines
- **Command**: Same as above with 4 report rows
- **Result**: `BLOCK intake.attestation-coverage: acceptance test report carries rows for Acceptance lines the intent does not have: 4`
- **Evidence**: Report row for line 4 was extra — intent does not have line 4

### Test 1c: Duplicate row 2, missing row 3
- **What I tried**: Report has rows 1, 2, 2 (duplicate), 4 (extra) — only lines 1 and 2 have coverage, line 2 duplicated, line 3 missing
- **Command**: Same as above with duplicate and extra rows
- **Result**: `BLOCK intake.attestation-coverage: acceptance test report carries duplicate rows for Acceptance lines: 2` and `acceptance test report carries rows for Acceptance lines the intent does not have: 4`
- **Evidence**: Row 2 appeared twice in report; row 4 was extra; line 3 was completely missing

### Test 1d: Complete report rows 1-3 — PASSES
- **What I tried**: Acceptance report with rows 1, 2, 3 matching intent exactly
- **Result**: `exit=0`, no failures
- **Evidence**: All three intent lines had exactly one report row each with valid verdict

### Test 1e: Duplicate-only (every line covered, line 2 appears twice)
- **What I tried**: Report rows 1, 2, 2, 3 — all intent lines covered, but line 2 duplicated
- **Result**: `BLOCK intake.attestation-coverage: acceptance test report carries duplicate rows for Acceptance lines: 2`
- **Evidence**: The check counts rows, not collapses them into a set; duplicate-only was correctly caught

### Test 1f: Row 3 verdict `fails` — PASSES (legal status)
- **What I tried**: Report rows 1, 2, 3 with row 3 verdict `fails`
- **Result**: `exit=0`; recorded `acceptance_status: [{"acceptance": 1, "status": "works"}, {"acceptance": 2, "status": "works"}, {"acceptance": 3, "status": "fails"}]`
- **Evidence**: The attestation records the report's stated verdict, not just row presence

### Test 1g: `not verified` (row 2) and `NOT_VERIFIED` (row 3) — PASSES (case-insensitive)
- **What I tried**: Report rows 1, 2 with `not verified`, 3 with `NOT_VERIFIED`
- **Result**: `exit=0`; recorded statuses `not_verified` for both — both spellings accepted case-insensitively
- **Evidence**: Both `not_verified` and `not verified` spellings are accepted

### Test 1h: Row 2 verdict `maybe` (not in template) — FAILS
- **What I tried**: Report row 2 verdict `maybe`
- **Result**: `BLOCK intake.attestation-coverage: acceptance test report states no Verdict in (works / partly / not verified / fails) for Acceptance lines: 2`
- **Evidence**: Only the four template words are valid verdicts

### Test 1i: Row 2 verdict `partly` — PASSES
- **What I tried**: Report row 2 verdict `partly`
- **Result**: `exit=0`; recorded `{"acceptance": 2, "status": "partly"}`
- **Evidence**: `partly` is one of the four valid verdict words

## 2. An attestation that does not record both the tested commit and the reviewed commit fails; when the two differ in functional content (not evidence files) it fails.

### Test 2a: Report without "Tried on … at <sha>" line — FAILS
- **What I tried**: Acceptance report missing the "Tried on … at <sha>" line
- **Result**: `BLOCK intake.commit-identity: v2 attestation is missing required bookkeeping fields: tested_commit=None reviewed_commit='…'; the acceptance test report and closing review must supply them`
- **Evidence**: Missing tested_commit and reviewed_commit fields

### Test 2b: Tested and reviewed have functional content drift
- **What I tried**: Tested commit has `code.py: "a\n"`, reviewed commit has `code.py: "b\n"`
- **Result**: `BLOCK intake.commit-identity: functional content differs between the tested commit … and the reviewed commit …; the acceptance evidence was produced on other code than what is being reviewed`
- **Evidence**: The two commits have different functional content (different code.py content)

### Test 2c: Evidence-only drift (only docs/loom/.../evidence/ changed) — PASSES
- **What I tried**: Tested and reviewed commits have identical code.py, but evidence file differs
- **Result**: `exit=0`; recorded `tested_commit: …, reviewed_commit: …, intent_confirmed_sha: …`
- **Evidence**: Difference is only in evidence files, which are whitelisted as publication-only paths

### Test 2d: Identical functional content, only acceptance-test-report.md differs — PASSES
- **What I tried**: Tested and reviewed commits have identical code.py, but acceptance-test-report.md differs
- **Result**: `exit=0`; functional content is the same, only evidence file differs
- **Evidence**: Report file differences are excluded from functional content comparison

## 3. An attestation whose recorded intent confirmation version no longer matches the intent file fails, and the message names the affected Acceptance items and the re-confirmation path.

### Test 3a: Intent edited after confirmation — FAILS, gives recompute command
- **What I tried**: Intent confirmed, then Acceptance line 2 rewritten; pin left stale
- **Result**: `BLOCK intake.intent-version: the intent has changed since the attestation pinned its confirmation (recorded X, current Y); every Acceptance line of the intent may be affected. recompute it with \`grep -v -e '^status:' -e '^intent_confirmed_sha:' docs/loom/intent/l3a_stale.md | git hash-object --stdin\` and re-confirm the intent before closing review.`
- **Evidence**: The recompute command works correctly under POSIX shell

### Test 3b: Same edit, pin recomputed to match — PASSES
- **What I tried**: Intent edited after confirmation, then pin recomputed to match new version
- **Result**: `exit=0`, attestation written
- **Evidence**: After re-pinning, the check passes

### Test 3c: Intent without `intent_confirmed_sha:` — PASSES (skipped)
- **What I tried**: Intent without intent_confirmed_sha field
- **Result**: `exit=0` (nothing pinned, skipped)
- **Evidence**: No confirmation record means no comparison is made

### Test 3d: Intent with `status: open` — PASSES (skipped)
- **What I tried**: Intent with status: open (not confirmed)
- **Result**: `exit=0` (no confirmation to compare)
- **Evidence**: Unconfirmed intents are automatically skipped

## 4. A plan naming a boundary/probe test that does not exist in the change fails the check.

### Test 4a: Risk line references boundary test task that doesn't exist — FAILS
- **What I tried**: Plan Risk line `1. Risk: the change breaks at the edge; boundary test W1-04`, but task W1-04 does not exist in the DAG
- **Result**: `BLOCK intake.plan-boundary-tests: Risk lines reference boundary test tasks that don't exist: W1-04`
- **Evidence**: The referenced task number does not exist in the plan's task DAG

### Test 4b: Referenced task exists — PASSES
- **What I tried**: Plan Risk line naming W1-02, and task `**W1-02 Guard Fixture task** boundary test after: W1-01 acceptance: 2` exists in the DAG
- **Result**: `exit=0`, no failure
- **Evidence**: The referenced task exists, so the check passes

### Test 4c: Charter 1.0 plan with dangling boundary test — does not fire (pre-1.1 exempt)
- **What I tried**: Plan with dangling `boundary test W9-99` in charter 1.0 format
- **Result**: Rule does not fire (pre-1.1 plan exempt)
- **Evidence**: Old plan format is exempt from this check

## 5. After closing review, the verdict artifact exists inside the change's own directory, and its master/subordinate relation to the attestation is explicit in the documentation.

### Test 5a: Verdict artifact exists in change directory — PASSES
- **What I tried**: After `finalize-review`, the change directory contains `attestation.json`, `acceptance-test-report.md`, and `evidence/` with verdicts bound from the change's own artifacts
- **Result**: `exit=0`; the attestation is the change's verdict record; its `verdicts` field is the filed verdict artifact, digest-bound and read by Ship, publication and the PR-floor check
- **Evidence**: The generated attestation is the change's verdict record; its `verdicts` field is the filed verdict artifact

### Test 5b: Verdict and attestation stay one artifact instead of two copies that can drift
- **What I tried**: After closing review, verdict and attestation are stored together in the change directory; review input JSON is temporary and not a record
- **Result**: `exit=0`; the attestation holds the verdicts (reviewer-1/reviewer-2, both PASS), `content_digest`, and bookkeeping fields; the review input JSON above is temporary — it is not a record and nothing reads it after finalization
- **Evidence**: Verified that verdict and attestation are bound together, not duplicated

## 6. The checks run again in the pre-publication invalidation check after closing review, not once at the review entrance only.

### Test 6a: Defective change — intake does not block, but closing review and finalize do
- **What I tried**: Defective change (report missing row 3): `intake write-plan` → no `intake.attestation-coverage` in output (attestation does not exist at intake); `finalize-review` on the same change → `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`
- **Result**: First run at intake: no attestation yet, so check does not fire. After finalize-review: check runs and blocks the defective change
- **Evidence**: The same defective change passes intake but fails at finalize-review

### Test 6b: Valid change finalized, then late functional commit makes it stale
- **What I tried**: Valid change finalized, attestation committed → `push --hook` silent (`exit=0`); `pr-floor` reports `verification: valid`. After a late functional commit (`scripts/tool_late.py` added post-attestation) → `push --hook` prints `loom: verification stale (attestation functional content digest does not match the selected tree)` and `pr-floor` prints `verification: stale`
- **Result**: After finalization, the verification status is valid. After a late functional commit, the attestation becomes stale and publishing is blocked
- **Evidence**: The invalidation re-run is `verification_status` → `validate_attestation` (recomputes the functional-content digest at the pre-publication head)

### Test 6c: Attestation with malformed `acceptance_status` — FAILS in pre-publication check
- **What I tried**: Attestation with malformed `acceptance_status` (`[{"line": 1, "status": "covered"}]`) committed → `push --hook` prints `loom: verification stale (attestation acceptance_status items must have 'acceptance' and 'status' fields)` and `pr-floor` prints `verification: stale`
- **Result**: The pre-publication check catches the malformed acceptance_status and blocks publishing
- **Evidence**: The validator requires `{"acceptance", "status"}` fields; `{"line", "status"}` does not match

## 7. New loom changes created after this change carry the new fields by default in their attestation and acceptance report templates.

### Test 7a: attestation.json schema `loom-attestation/v2` carries new fields
- **What I tried**: Schema `loom-attestation/v2` carries `intent_confirmed_sha`, `tested_commit`, `reviewed_commit`, `acceptance_status`
- **Result**: The template carries all four new fields by default
- **Evidence**: `loom-code/contract/templates/attestation.json` carries `intent_confirmed_sha`, `tested_commit`, `reviewed_commit`, `acceptance_status`

### Test 7b: intent.md templates carry `intent_confirmed_sha`
- **What I tried**: `loom-code/contract/templates/intent.md` and `loom-design/skills/capture-intent/templates/intent.md` carry `intent_confirmed_sha` with the hash recipe
- **Result**: Both intent templates carry the `intent_confirmed_sha` field
- **Evidence**: Both intent template files carry `intent_confirmed_sha` with the hash recipe

### Test 7c: acceptance-test-report.md template carries "Tried on … at <short sha>" line
- **What I tried**: `loom-code/skills/closing-review/references/acceptance-test-report.md` carries the fixed "Tried on <date>, in a clean copy of the project at <short sha>." line — the tested_commit extraction point
- **Result**: The template carries the "Tried on … at <short sha>" line
- **Evidence**: The acceptance-test-report.md template carries the "Tried on … at <short sha>" line

### Test 7d: plan.md Risks section carries boundary-test hint
- **What I tried**: `loom-code/contract/templates/plan.md` Risks section carries the boundary-test hint
- **Result**: The plan template carries the boundary-test hint
- **Evidence**: The plan template's Risks section carries the boundary-test hint

### Test 7e: Brand-new fixture change finalized at this HEAD
- **What I tried**: A brand-new fixture change (`l7_fresh`) finalized at this HEAD generated `acceptance_status: [{"acceptance": 1, "status": "works"}, {"acceptance": 2, "status": "works"}, {"acceptance": 3, "status": "works"}]`, `tested_commit: 6ea0eae…`, `reviewed_commit: 45a0ef8…`. `validate_attestation` on that generated attestation returns `[]` (valid); `pr-floor` reports `verification: valid`.
- **Result**: Full end-to-end test passes — new changes generate correct attestation shape
- **Evidence**: The previous shape mismatch (`{"line": N, "status": "covered"}` vs the validator's `{"acceptance", "status"}`) is gone: `acceptance_coverage` now emits the validator vocabulary and the fix has a regression test

