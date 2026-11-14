# Checked CLI consumers — plan
intent: 2026-11-14-consume-readonly-json@e0cfabe57b9ddcb81e3afbe92df130f531b3f244
spec: docs/loom/2026-11-14-consume-readonly-json/spec.md@a00f119294e3b5667f5d14611859ba5fc0483629
charter: 1.1

The required independent spec+adversarial checkpoint passed without findings.
The spec owns current-state evidence and choices. This first delivery preserves
the sixteen-command inventory but migrates only two existing real consumers.
No ratified ARCHITECTURE.md exists. Coupled tasks run sequentially.

## Task DAG

### Wave 1 — One checked observation boundary

**W1-01 Implement the bounded consumer** after: none acceptance: 2, 3, 4, 5
- Files: `loom-code/scripts/checked_readonly.py` (entry: main), `loom-code/tests/test_checked_readonly.py`, `loom-code/tests/test_loom_python_runtime.py`
- Test: Existing: test_preparation_json.py, test_loom_python_runtime.py. A2 positive: real-observations; negative: wrong-request. A3 positive: compatible-additions; negative: malformed-result. A4 positive: direct-parity; negative: extra-execution. A5 positive: safe-help; boundary: startup-timeout. New entry tests cover consumer validation, not producer duplication.
- Risk: REQ-2/3/4/5; agent-decided one script for two callers. Preserve/widen test_loom_python_runtime.py startup/help coverage; retain test_preparation_json.py producer cases. Use main and real subprocess seam; no internal-only tests, fallback, retries or policy duplication.

### Wave 2 — Real station adoption and common inventory

**W2-01 Adopt checked results and publish the inventory** after: W1-01 acceptance: 1, 2, 4, 5
- Files: `loom-code/skills/write-plan/SKILL.md`, `loom-code/skills/write-plan/references/codex-first-contact.md`, `loom-code/skills/closing-review/SKILL.md`, `loom-code/references/cli-results.md`, `loom-code/README.md`
- Test: Existing: test_write_plan_station_text.py, test_simplified_station_text.py, test_closing_review_recovery_rules.py. A1 positive: sixteen-covered; negative: false-migrated. A2 positive: both-consumers; negative: text-parsing. A4 positive: authority-retained; negative: recovery-bypass. A5 positive: documented-command; boundary: invalid-observation. Replay actual consumer examples.
- Risk: REQ-1/2/4/5; agent-decided replace calls and interpretation together. Preserve station tests' distinct safeguards; no new prose-only executable pins where review and dogfood suffice. Runtime references stay portable and never cite repository development records.

### Wave 3 — One synchronized release packet

**W3-01 Release the station guidance** after: W2-01 acceptance: 4, 5
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A4 positive: release-parity; negative: stale-pin. A5 positive: accurate-release; boundary: unmigrated-commands. Reuse existing release metadata and README guards; derive mirrored manifests with scripts/sync_codex_manifests.py --all and check parity.
- Risk: REQ-4/5; agent-decided minor 3.77.0 for new consumer interface/station guidance, after remote recheck. Preserve current-release and README guards; change only current pin. Include dated CHANGELOG entry and commit with W3-02 before final review.

**W3-02 Preserve localized parity and measured evidence** after: W3-01 acceptance: 4, 5
- Files: `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `docs/loom/2026-11-14-consume-readonly-json/evidence/build-verification.md`
- Test: A4 positive: localized-version-parity; negative: stale-localized-version. A5 positive: retained-commands; boundary: unverified-hosts. Existing README version guard and real consumer executions supply evidence; independent acceptance remains separate.
- Risk: REQ-4/5; agent-decided localized version strings only. Report actual RED/GREEN, code/test volume and limits; no efficiency claim. Preserve historical failures and clearly distinguish worker example runs from independent dogfood and full-suite evidence.

Each executable task observes RED before implementation and GREEN afterwards.
All tasks use mandatory implementers; the orchestrator does not implement them.
After tasks: sync-trunk, fresh independent adversary, complete configured suite
and declared adversarial commands. Closing review then runs independent
fresh-copy acceptance and separate code/docs reviewers before finalize-review.
The reviewer episode has not started; no step is skipped.

## Simplicity check
- Combine W3-02 into W3-01 — declined: eleven Files exceed the charter's eight-entry cap; one implementer executes both sequentially as one release commit, so no extra agent handoff is needed.

## Questions asked
① — what — 依這個小範圍繼續，對嗎？
① — what — 依這份完整範圍繼續，對嗎？
① — what — 確認以這份目標繼續嗎？

## Risks
1. user-decided — Latest selection: interface consistency first. Initial repeated intake questions preceded the final narrowed selection; preserve them here. The confirmed intent excludes automatic fallback/retry and full recovery, not existing diagnostics or reconciliation.
2. agent-decided — Mechanism budget exception: one bounded checked consumer script serves two existing callers. No new checker command, station, rule ID, dependency, policy evaluator or recovery framework. Tests exercise main and actual callers before acceptance.
3. agent-decided — Validate the published producer contract, not computational truth. Compatible extra fields are accepted; unknown/malformed/contradictory data cannot justify continuation or reviewer dispatch. Preserve the same interpreter and no-write execution boundary.
4. agent-decided — A new validation/diagnostic interface is public-contract risk; source-grounded spec checkpoint passed. The current research supports limited scope, not a measured speed, token, cost or incident-frequency improvement.
5. agent-decided — Recheck trunk before release selection. Generated metadata and the release pin must land before attestation. Preserve worktrees, old evidence, hook identities and installed plugin state; no paid outside execution is authorized.
6. user-decided — Automatic PR publication follows passing review/checks, as disclosed during intake. Merge still requires acceptance of the report; the prior merged change's conditional merge delegation does not authorize this new branch's merge.
