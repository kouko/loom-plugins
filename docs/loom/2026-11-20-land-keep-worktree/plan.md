# Keep the worktree when landing an accepted change — plan
intent: 2026-11-20-land-keep-worktree@96e37196
spec: docs/loom/2026-11-20-land-keep-worktree/spec.md@153ebf82
charter: 1.1

## Task DAG

Wave 1 — land code (W1-01), then prose that names the new option (W1-02); Wave 2 — release metadata.

**W1-01 Add --keep-worktree to the accepted land form**  after: none  acceptance: 1, 2, 3, 4
- Files: `loom-code/scripts/loom_checker/command_handlers/land.py`, `loom-code/tests/test_land_merge.py`, `loom-code/tests/test_land_cleanup.py`
- Test: A1 positive: keep-flag-keeps-all-syncs-trunk-then-cleanup-removes-all; negative: keep-flag-with-cleanup-or-sweep-is-usage-error. A2 positive: keep-flag-failing-check-refuses-merge; boundary: keep-flag-still-syncs-trunk. A3 positive: test_merged_change_refs_worktree_removed (existing); boundary: duplicate-keep-flag-usage-error. A4 positive: keep-output-names-cleanup-command; boundary: cleanup-after-keep-removes-all.
- Risk: REQ-1..4; trunk-sync and cleanup-after-keep are asserts inside the A1 fixture; A3 reuses `test_land_cleanup.py:176`; existing cases preserved; no `next: cd` when kept.

**W1-02 Ship text and land help name the keep option**  after: W1-01  acceptance: 5
- Files: `loom-code/skills/ship/SKILL.md`, `loom-code/scripts/loom_checker.py`, `loom-code/tests/test_ship_station_text.py`, `loom-code/tests/test_loom_checker_cli.py`
- Test: A5 positive: ship-text-adds-keep-worktree-when-maintainer-asks; negative: land-help-no-longer-asks-preservation-accepted-form-cannot-honour.
- Risk: REQ-5; help Usage line, accepted-form sentence, line 220 and module docstring updated; ship adds keep sentence and qualifies removal line; `test_ship_station_text.py:123` "never keep the worktree" assertion rewritten, not dodged.

**W2-01 Release metadata for loom-code minor bump**  after: W1-02  acceptance: 5
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A5 positive: release_sync; boundary: release_stale_pin. Pin test `test_current_release_metadata_is_synchronized`; derived manifests via `scripts/sync_codex_manifests.py --all`.
- Risk: minor bump 3.87.0 → 3.88.0 (new CLI option); recheck origin/main version before bumping (agent-decided).

**W3-01 Graduate the keep-block-recovery probe into the suite**  after: W2-01  acceptance: 5
- Files: `loom-code/tests/test_ship_station_text.py`, `docs/loom/2026-11-20-land-keep-worktree/evidence/probes/test_probe_keep_block_recovery.py`
- Test: A5 positive: ship-keep-block-recovery-keeps-worktree; negative: negated-keep-sentence-rejected.
- Risk: probe caught the ship §5 BLOCK-recovery defect, so review.probe-graduation requires moving it into the suite before finalize-review; probe file deleted after its cases move (agent-decided).

## Simplicity check
- drop new A3 test, cite existing `test_land_cleanup.py:176` — taken
- fold trunk-sync and cleanup-after-keep checks into the A1 keep fixture — taken
- name help Usage line, accepted-form sentence and docstring in W1-02 — taken
- rewrite `test_ship_station_text.py:123` instead of preserving it — taken
- merge the three tasks into fewer — declined: reviewer found the three-task shape minimal; release metadata is required by repo versioning rule

## Questions asked
① — consequence — 保留 worktree 時，GitHub 上的遠端分支要不要也保留？A 全部保留、之後一次清掉；B 照常刪遠端、只留本機

## Risks
1. Agents on an older loom-code that read new ship text would pass an unknown flag; land rejects it with a usage error before any merge.
2. user-decided — keep leaves the remote branch too (option A at ①, 2026-11-20).
