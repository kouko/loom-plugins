# Two read-only JSON results — plan
intent: 2026-11-14-cli-readonly-json@752d18c7efe09c0cd8bd0b2b764f3500d05ca330
spec: docs/loom/2026-11-14-cli-readonly-json/spec.md@8d4a0afd52b9a4ec094189fff9ddafd68cb95bf5
charter: 1.1

Current-state evidence and agent-decided interface choices are in the spec.
The required independent spec+adversarial checkpoint passed without findings.
No ratified ARCHITECTURE.md is present. This engineering change needs no second
human behavior confirmation; the user already authorized conditional merge.

## Task DAG

### Wave 1 — One coherent public-entry extension

**W1-01 Add the two opt-in result contracts** after: none acceptance: 1, 2, 3, 4
- Files: `loom-code/scripts/loom_checker.py` (entry: main), `loom-code/scripts/loom_checker/command_handlers/contract.py`, `loom-code/scripts/loom_checker/command_handlers/reviewer_count.py`, `loom-code/scripts/loom_checker/preparation_output.py`, `loom-code/tests/test_preparation_json.py`, `loom-code/tests/test_loom_checker_cli.py`
- Test: Existing: loom-code/tests/test_preparation_json.py, loom-code/tests/test_loom_checker_cli.py. A1 positive: typed-domain-results; negative: unavailable-error-data. A2 positive: existing-cli-baselines; negative: existing-json-shape-drift. A3 positive: readonly-entry; negative: caught-internal-mixed-output. A4 positive: exact-help; boundary: final-selector. Extend distinct data/error/selector coverage.
- Risk: REQ-1/2/3/4; agent-decided reuse result functions. Preserve/widen coverage in loom-code/tests/test_preparation_json.py and loom-code/tests/test_loom_checker_cli.py; retain loom-code/tests/test_loom_python_runtime.py startup guards. New tests exercise data and error cleanup through main, not a new harness.

### Wave 2 — Document and release the bounded interface

**W2-01 Complete release metadata and consumer examples** after: W1-01 acceptance: 2, 4, 5
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A2 positive: release-parity; negative: stale-pin. A4 positive: five-json-capabilities; negative: stale-help-description. A5 positive: real-field-consumer; negative: consumer-rejects-blocked. Reuse current-release and README parity guards; replay documented examples against actual outputs.
- Risk: REQ-2/4/5; agent-decided minor 3.76.0 for additive public results. Preserve test_write_plan_station_text.py safeguards, changing only its version pin. Derive mirrors from the SSOT; include the dated CHANGELOG entry. Commit together with W2-02 before review.

**W2-02 Preserve localized parity and verification evidence** after: W2-01 acceptance: 2, 5
- Files: `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `docs/loom/2026-11-14-cli-readonly-json/evidence/build-verification.md`
- Test: A2 positive: localized-version-parity; negative: stale-localized-version. A5 positive: recorded-consumer-decisions; boundary: unverified-hosts. Existing test_readme_version_matches_manifest verifies parity; independent acceptance later replays the complete dogfood criteria.
- Risk: REQ-2/5; agent-decided keep localized edits limited to release metadata. Preserve earlier failures and distinguish worker example checks from independent dogfood. Record actual code/test volume and complete-suite results rather than efficiency claims.

Implementer tasks run sequentially because dispatch, handlers, tests and release
mirrors share contracts. Each executable change first fails a qualified existing
or extended public-entry case, then passes it. No temporary compatibility
framework or permanent consumer harness is planned. Complete W2-01/W2-02 as one
release packet, then run sync-trunk, the independent adversary, the configured
complete package suite and declared adversarial commands. Closing review owns
fresh clean-environment dogfood and code/docs review before finalization.

## Simplicity check
- none found

## Questions asked
① — what — 依這份範圍執行，對嗎？

## Risks
1. user-decided — Only contract and reviewer-count gain JSON; text, exits, existing JSON and authorization stay compatible. Preserve every worktree and previous evidence; do not update installed plugins.
2. user-decided — The confirmed instruction authorizes publication and merge once dogfood, independent review, full tests and CI pass without important unresolved issues. Present the acceptance report and final evidence; do not request redundant merge authorization.
3. agent-decided — Spec checkpoint passed; this is a fresh change, not an extension of merged help review rounds. No verification step is skipped, and no outside-model execution is authorized by the merge delegation.
4. agent-decided — Separate JSON observation from authority and completion. Conservative reviewer floor two remains successful observation without claiming complete classification; startup failures remain outside the loaded-checker contract.
5. agent-decided — Compare baseline text and existing JSON shapes through real entry tests. Consumer dogfood branches on actual typed fields and rejects invalid or blocked outcomes; synthetic fixtures do not prove live-host reloading.
6. agent-decided — Recheck remote main before final version selection. New result-contract maintenance is the accepted cost; initial code-volume estimates are not measurements or evidence of lower operation count or token usage.
