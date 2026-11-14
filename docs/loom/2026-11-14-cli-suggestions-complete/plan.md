# Complete CLI advisory guidance — plan
intent: 2026-11-14-cli-suggestions-complete@609c81d1e2f03b259090e32a968220aa7b9f8c1f
spec: docs/loom/2026-11-14-cli-suggestions-complete/spec.md@4b2ccac7d2e39cc3d2770c7108db075aae159887
charter: 1.1

## Task DAG

### Wave 1 — Common presentation boundary

**W1-01 Share dependency-free advice and ordinary CLI handling** after: none acceptance: 1, 2, 3, 4, 5, 6
- Files: `loom-code/scripts/loom_checker/cli_advice.py` (entries: suggested_next/write_suggestion), `loom-code/scripts/loom_checker/preparation_output.py` (entries: new_result/report_result/error_result), `loom-code/scripts/loom_checker.py` (entry: main), `loom-code/scripts/checked_readonly.py` (entry: main), `loom-code/tests/test_loom_checker_cli.py`, `loom-code/tests/test_preparation_json.py`, `loom-code/tests/test_checked_readonly.py`, `loom-code/tests/test_loom_python_runtime.py`
- Test: Existing: test_loom_checker_cli.py/test_preparation_json.py/test_checked_readonly.py/test_loom_python_runtime.py. A1 positive: dispatch; negative: unknown. A2 positive: advice; boundary: returned-usage. A3 positive: preparation-parity; negative: shape-drift. A4 positive: preserved-result; negative: advisory-write-failure. A5 positive: hook-framing; negative: contamination. A6 positive: help; boundary: dependency-free-startup.
- Risk: REQ-1–6; agent-decided one stdlib-only shared module. Preserve/widen existing authoritative validation, raw precision, import-isolation, selectors and no-child help cases. Test through public entries, keep command registry authoritative and advice writes best-effort; protected modes receive no dispatcher prose.

### Wave 2 — Remaining JSON family

**W2-01 Add compatible delivery advice alias** after: W1-01 acceptance: 1, 2, 3, 4, 5, 6
- Files: `loom-code/scripts/loom_checker/command_handlers/publish.py` (entry: cmd_delivery), `loom-code/tests/test_delivery.py`, `loom-code/tests/test_delivery_stop.py`, `loom-code/tests/test_preparation_json.py`
- Test: Existing: test_delivery.py/test_delivery_stop.py/test_preparation_json.py. A1 positive: delivery-states; negative: unconfirmed. A2 positive: actual-next; boundary: usage. A3 positive: alias-parity; negative: removed-legacy. A4 positive: no-write; negative: repeated-operation. A5 positive: hook-framing; negative: extra-payload. A6 positive: documented-result; boundary: pre-object-failure.
- Risk: REQ-1–6; agent-decided alias existing next value only. Widen delivery JSON/text checks while preserving every original field, observer policy, legacy text, Help and hook behavior. No DeliveryResult redesign, remote write or duplicate dispatcher recommendation.

### Wave 3 — Semantic advisory states and handoffs

**W3-01 Cover unsynced and unconfirmed zero exits** after: W2-01 acceptance: 1, 2, 4, 5, 6
- Files: `loom-code/scripts/loom_checker/command_handlers/sync.py` (entry: cmd_sync_trunk), `loom-code/scripts/loom_checker/command_handlers/github_rules.py` (entry: cmd_github_rules), `loom-code/tests/test_sync_trunk.py`, `loom-code/tests/test_github_rules.py`
- Test: Existing: test_sync_trunk.py/test_github_rules.py. A1 positive: state-coverage; negative: exit-only. A2 positive: uncertainty-advice; negative: false-completion. A4 positive: existing-remedies; negative: retry. A5 positive: setup-preserved; negative: script-pollution. A6 positive: real-fixtures; boundary: remote-failure.
- Risk: REQ-1/2/4/5/6; agent-decided advice at actual outcome owners. Preserve/widen fetch/history/rollback and ruleset/bypass tests. Keep exit-zero warnings advisory, no additional network calls or stdout parsing; setup output and existing control decisions stay unchanged.

**W3-02 Cover standing warnings and CI verification notices** after: W3-01 acceptance: 1, 2, 4, 5, 6
- Files: `loom-code/scripts/loom_checker/command_handlers/standing.py` (entry: cmd_standing), `loom-code/scripts/loom_checker/rule_checks/standing.py` (entry: check_standing_warn), `loom-code/scripts/loom_checker/command_handlers/pr_floor.py` (entry: cmd_pr_floor), `loom-code/tests/test_loom_checker_standing.py`, `loom-code/tests/test_pr_floor.py`, `loom-code/tests/test_pr_floor_workflow.py`
- Test: Existing: test_loom_checker_standing.py/test_pr_floor.py/test_pr_floor_workflow.py. A1 positive: notice-coverage; negative: omitted-state. A2 positive: advisory-notice; negative: false-gate. A4 positive: unchanged-policy; negative: automatic-fix. A5 positive: annotation-summary; negative: protocol-drift. A6 positive: warnings; boundary: waived-docs.
- Risk: REQ-1/2/4/5/6; agent-decided derive advice from emitted-warning/state facts. Preserve/widen waiver, principle refusal, annotation escaping and summary-write tests. A non-valid verification notice stays exit zero; no new CI gate or standing-document mutation.

**W3-03 Preserve accepted-operation and sweep handoffs** after: W3-02 acceptance: 1, 2, 4, 5, 6
- Files: `loom-code/scripts/loom_checker/command_handlers/land.py` (entry: cmd_land), `loom-code/tests/test_land_sweep.py`, `loom-code/tests/test_land_cleanup.py`, `loom-code/tests/test_land_merge.py`, `loom-code/tests/test_loom_publish.py`
- Test: Existing: test_land_sweep.py/test_land_cleanup.py/test_land_merge.py/test_loom_publish.py. A1 positive: operation-modes; negative: missed-mode. A2 positive: approval-advice; negative: assumed-approval. A4 positive: reconciled-result; negative: repeated-merge. A5 positive: cwd-token; negative: altered-handoff. A6 positive: controlled-runner; boundary: cleanup-refusal.
- Risk: REQ-1/2/4/5/6; agent-decided sweep guidance only where list facts require follow-up. Preserve/widen acceptance, cleanup/sweep freshness, exact cwd/token and mutation-count tests. Existing publication/merge/cleanup routes and legacy precise remedies remain authoritative; execute no user-repository cleanup.

### Wave 4 — Complete portable documentation

**W4-01 Publish all-command advice coverage** after: W3-03 acceptance: 1, 2, 3, 4, 5, 6
- Files: `loom-code/references/cli-results.md`, `loom-code/README.md`, `README.md`
- Test: Existing: test_write_plan_station_text.py/test_loom_runtime_skill_commands.py/test_closing_review_recovery_rules.py. A1 positive: sixteen-covered; negative: inventory-only. A2 positive: uncertainty; negative: guessed-fix. A3 positive: five-json; negative: uniform-envelope. A4 positive: optional-advice; negative: advice-authority. A5 positive: exception-map; negative: silent-exclusion. A6 positive: command-replay; boundary: simulated-remotes.
- Risk: REQ-1–6; agent-decided common guide owns rules and evidence map. No new prose-pin tests or duplicate station paragraphs. Distinguish sixteen advised commands, five JSON commands and two checked consumers; correct the now-touched README internal-error wording without unrelated edits.

### Wave 5 — Synchronized release packet

**W5-01 Release completed advisory coverage** after: W4-01 acceptance: 4, 6
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A4 positive: release-parity; negative: stale-pin. A6 positive: accurate-release; boundary: unverified-hosts. Reuse existing release guard, derive manifests with scripts/sync_codex_manifests.py --all and verify --all --check.
- Risk: REQ-4/6; agent-decided minor 3.79.0, subject to current remote version recheck. Preserve historical changelogs, update current pin and dated entry; execute sequentially with W5-02 as one coherent release commit before final review.

**W5-02 Preserve localized parity and measured build evidence** after: W5-01 acceptance: 1, 4, 6
- Files: `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `docs/loom/2026-11-14-cli-suggestions-complete/evidence/build-verification.md`
- Test: A1 positive: coverage-record; negative: unexecuted-claim. A4 positive: localized-parity; negative: stale-locale. A6 positive: retained-logs; boundary: modeled-operations. Reuse release guard and actual command replays; record actual source/test/prose growth independently of intake estimates.
- Risk: REQ-1/4/6; agent-decided localized version strings only. Retain historical failures, actual per-command/mode evidence and simulation limits. Same implementer completes both release tasks sequentially; no plugin install, outside model or efficiency claim.

## Simplicity check
- none found

## Questions asked
① — what — 這個「全部」範圍對嗎？

## Risks
1. user-decided — Complete all sixteen commands in one delivery. Preserve existing JSON families, optional suggested_next naming, delivery.next and special protocols; no new JSON mode, executor, retry or automatic repair.
2. agent-decided — Mechanism budget exception: extend advisory coverage and add one shared stdlib-only formatter module for multiple actual callers. No new source dependency, command, registry, gate, policy evaluator or test module.
3. agent-decided — Standard-library-only wrapper help must survive; preparation_output imports PyYAML through helpers, so shared advice must not live behind that dependency. Keep existing runtime/import isolation and raw result precision.
4. agent-decided — Advice-only stream failures cannot change exits or repeat mutation. Primary output failures, termination and pre-Python readiness retain existing limits. Protocol exceptions need actual framing/byte and counter evidence, not explanatory prose alone.
5. agent-decided — Unknown or exit-zero advisory states remain unconfirmed/unsynced. Do not derive state from displayed prose, guess repair, forge human confirmation, authorize installation/setup, or repeat accepted merge after cleanup failure.
6. agent-decided — All implementation tasks run sequentially with mandatory implementers and RED/GREEN. End Build with trunk sync, independent adversary, complete configured suite and programs; closing review uses clean-copy acceptance, distinct reviewers and generated finalization. No steps skipped.
7. user-decided — Automatic publication follows passing checks, as confirmed at intake; merge requires separate acceptance. Preserve every worktree and prior evidence. Paid outside execution, installed-plugin updates and live user-data cleanup are not authorized.
