# Suggested next steps — plan
intent: 2026-11-14-cli-next-guidance@e2b6c517d2d3bfd54c6fc68bdb98214983cf2859
spec: docs/loom/2026-11-14-cli-next-guidance/spec.md@837620d2
charter: 1.1

## Task DAG

### Wave 1 — Producer and consumer advice

**W1-01 Add bounded advisory output** after: none acceptance: 2, 3, 4, 5
- Files: `loom-code/scripts/loom_checker.py` (entry: main), `loom-code/scripts/loom_checker/preparation_output.py` (entries: new_result/report_result/error_result), `loom-code/scripts/checked_readonly.py` (entry: main), `loom-code/tests/test_preparation_json.py`, `loom-code/tests/test_checked_readonly.py`, `loom-code/tests/test_loom_checker_cli.py`
- Test: Existing: test_preparation_json.py, test_checked_readonly.py, test_loom_checker_cli.py. A2 positive: known-advice; boundary: unknown-failure. A3 positive: advisory-only; negative: bad-hint-controls-result. A4 positive: direct-parity; negative: legacy-drift. A5 positive: accurate-help; boundary: startup-timeout. Extend existing entry cases; no new test module.
- Risk: REQ-2/3/4/5; agent-decided shared renderer and public entries. Widen existing advice/error cases without losing malformed-result, precision, isolation or policy coverage; keep legacy Help hints and direct successful text. Do not alter domain handlers or policy.

### Wave 2 — Consumer guidance and migration inventory

**W2-01 Adopt advisory reading rules** after: W1-01 acceptance: 1, 2, 3, 4, 5
- Files: `loom-code/references/cli-results.md`, `loom-code/skills/write-plan/SKILL.md`, `loom-code/skills/write-plan/references/codex-first-contact.md`, `loom-code/skills/closing-review/SKILL.md`, `loom-code/README.md`
- Test: Existing: test_loom_runtime_skill_commands.py, test_write_plan_station_text.py, test_closing_review_recovery_rules.py. A1 positive: migration-inventory; negative: all-migrated. A2 positive: usable-suggestion; boundary: unknown-repair. A3 positive: result-prerequisite; negative: advice-authorizes. A4 positive: legacy-guidance; negative: authority-drift. A5 positive: real-replay; boundary: absent-advice.
- Risk: REQ-1/2/3/4/5; agent-decided one common contract plus short station references. Preserve existing text-test safeguards; add no prose-pin tests. Carry exact user naming and distinguish legacy delivery.next. Runtime prose cites portable bundled references, not development records.

### Wave 3 — Synchronized release and measured evidence

**W3-01 Release advisory guidance** after: W2-01 acceptance: 4, 5
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A4 positive: release-parity; negative: stale-pin. A5 positive: accurate-release; boundary: unmigrated-interfaces. Reuse existing metadata and README guards; derive manifests with scripts/sync_codex_manifests.py --all, then --all --check.
- Risk: REQ-4/5; agent-decided minor 3.78.0 for the additive field and station contract, subject to remote recheck. Preserve historical release records; update current pin, dated CHANGELOG and README in one coherent packet with W3-02.

**W3-02 Preserve localized parity and build evidence** after: W3-01 acceptance: 4, 5
- Files: `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `docs/loom/2026-11-14-cli-next-guidance/evidence/build-verification.md`
- Test: A4 positive: localized-parity; negative: stale-locales. A5 positive: retained-replays; boundary: unverified-hosts. Existing release guard and real producer/consumer calls verify this packet; record actual source/test delta separately from rough intake estimates.
- Risk: REQ-4/5; agent-decided localized version strings only. Same implementer executes W3-01 then W3-02 as one release commit, retaining historical REDs and clear pending independent/full-suite/CI boundaries. No installed plugin update or efficiency claims.

## Simplicity check
- none found

## Questions asked
① — what — 依這個首批範圍繼續嗎？

## Risks
1. user-decided — Suggested next step: and suggested_next emphasize advice. The amended intake confirmation retains the two-consumer scope; existing delivery.next is not renamed.
2. agent-decided — Mechanism budget exception: one additive advisory field on two existing results, implemented within existing modules. No new checker command, registry, rule, source/test module, execution engine or authorization mechanism.
3. agent-decided — Advice remains optional for consumption. Existing core validation and raw precision preservation stay authoritative; unusable hints are ignored rather than converted into failure or executable commands.
4. agent-decided — Public-contract and trust-interpretation risk requires focused negative cases and independent acceptance. Do not guess repairs, flatten outdated consumer/producer diagnostics, hide original faults or measure success by field presence alone.
5. agent-decided — Engineering change; decision point ② is exempt. No skipped steps. Mandatory implementers run tasks sequentially, then trunk sync, independent adversary, complete configured suite and declared programs; closing review runs clean-copy acceptance and distinct reviewers before finalization.
6. user-decided — Automatic publication follows passing verification, as disclosed at intake. Merge requires separate acceptance; preserve every existing worktree, prior evidence and installed plugin state. No paid outside execution is authorized.
