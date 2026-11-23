# Record kept worktrees so sweep never removes them — plan
intent: 2026-11-23-record-kept-worktrees@7bafdd12
spec: docs/loom/2026-11-23-record-kept-worktrees/spec.md@ff9af3ce
charter: 1.1

## Task DAG

Wave 1 — land code (W1-01), then ship text and help that describe it (W1-02); Wave 2 — release metadata.

**W1-01 Keep record, kept sweep lines and record cleanup in land**  after: none  acceptance: 1, 2, 3, 4
- Files: `loom-code/scripts/loom_checker/command_handlers/land.py`, `loom-code/tests/test_land_sweep.py`, `loom-code/tests/test_land_cleanup.py`
- Test: A1 positive: keep-land-then-sweep-from-main-shows-kept-line; boundary: only-kept-merged-prints-no-token. A2 positive: mixed-listing-confirm-removes-only-unkept; negative: mixed-listing-token-excludes-kept. A3 positive: keep-cleanup-test-asserts-record-set-then-gone; boundary: cleanup-without-local-branch-clears-record. A4 positive: existing-sweep-tests-unchanged; negative: mixed-listing-unkept-on-remove-line.
- Risk: REQ-1..4; extend `test_land_cleanup.py:211`; one mixed-listing case in `test_land_sweep.py`; move existing `config --remove-section` (land.py:527-528) out of `if plan.local:` instead of a second unset path (agent-decided).

**W1-02 Ship and land help describe kept sweep lines**  after: W1-01  acceptance: 5
- Files: `loom-code/skills/ship/SKILL.md`, `loom-code/scripts/loom_checker.py`, `loom-code/tests/test_ship_station_text.py`, `loom-code/tests/test_loom_checker_cli.py`
- Test: A5 positive: ship-leaves-kept-lines-and-asks-before-earlier-work-cleanup; negative: ship-has-no-unasked-earlier-work-cleanup.
- Risk: REQ-5; rewrites ship §5 earlier-work paragraph, so `test_ship_earlier_work_cleanup_spares_kept_worktree` is rewritten and widened to the ask-first rule, not dropped; help gains the kept line (agent-decided).

**W2-01 Release metadata for loom-code minor bump**  after: W1-02  acceptance: 5
- Files: `loom-code/.claude-plugin/plugin.json`, derived manifests (`.codex-plugin/plugin.json`, `plugin.json`, `package.json`), `loom-code/CHANGELOG.md`, `loom-code/README*.md`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A5 positive: release_sync; boundary: release_stale_pin. Pin test `test_current_release_metadata_is_synchronized`; derived manifests via `scripts/sync_codex_manifests.py --all`.
- Risk: minor bump 3.88.0 → 3.89.0 (CLI output and station guidance change); recheck origin/main version before bumping (agent-decided).

**W3-01 Graduate the two kept-record probes into the suite**  after: W2-01  acceptance: 1
- Files: `loom-code/tests/test_land_sweep.py`, `docs/loom/2026-11-23-record-kept-worktrees/evidence/probes/test_probe_sweep_from_kept_worktree.py`, `docs/loom/2026-11-23-record-kept-worktrees/evidence/probes/test_probe_keep_record_write_failure.py`
- Test: A1 positive: sweep-inside-kept-worktree-marks-kept; negative: keep-record-write-failure-exits-nonzero.
- Risk: both probes caught defects fixed in febc9ee7, so review.probe-graduation moves them into the suite before finalize-review; probe files deleted after their cases move (agent-decided).

## Simplicity check
- merge A1 boundary into A1 positive (sweep skips the invoking worktree, so it is one run) — taken
- one mixed kept/unkept sweep case covers A2 and A4 negative — taken
- extend existing keep-then-cleanup test for record set/gone instead of a new A3 test — taken
- reuse existing branch config removal by moving it out of `if plan.local:` — taken
- add the only-kept-merged no-token case from the spec flow — taken
- fewer tasks or files — declined: reviewer found the three-task shape minimal; release metadata is required by the repo versioning rule

## Questions asked
① — consequence — 批次清理遇到保留的變更，要怎麼顯示？另外列出、標明「保留」、永遠不刪（建議）／完全不列出

## Risks
1. A worktree kept under loom-code 3.88.0 has no record and still appears on a `remove` line; ship's ask-first rule covers it (intent Out of scope: no backfill).
2. user-decided — sweep lists kept changes separately, marked kept, never deleted (answer at ①, 2026-11-23).
