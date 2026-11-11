# Ordinary added files must not trigger test collection when a review record is rechecked — plan
intent: 2026-11-11-stop-verification-git-only@bddf642
charter: 1.1

## Current State Evidence
- Forward: `loom-code/scripts/loom_checker/probes.py:512-518` — `graduated_probe_programs` runs `suite_collection` (subprocesses, a temporary directory) on each added program path before the git-only `_carries_concern`.
- Reverse: `loom-code/scripts/loom_checker/attestation.py:285-288` — a `no_program` record makes `validate_attestation` call `stored_probe_programs`; `command_handlers/publish.py:548` reaches it on every Stop, `:825` when shipping, `finalize.py:287` at finalize.
- Error: `docs/loom/2026-11-11-stop-verification-git-only/evidence/hook-reproduction.md` — three added program files produced three `pytest --collect-only` launches and three temporary directories in both the direct recomputation and the Stop hook.
- Data: `docs/loom/*/attestation.json` on main at `31b98646` — 1 of 136 attestations records `no_program`.
- Boundary: `loom-code/tests/test_adversarial_probe_cap_coverage.py:160-249` — existing tests pin which added files count as graduated: moved, copied, `tests/local/`, runner-ignored.

## Task DAG

**W1-01 Check the concern line before collecting**  after: none  acceptance: 1,2,3,4
- Files: `loom-code/scripts/loom_checker/probes.py` (entry: `graduated_probe_programs`), `loom-code/tests/test_delivery_stop.py`
- Test: A1 positive: stop_hook_no_program_ordinary_files_git_only; boundary: stop_hook_reminder_unchanged. A2 positive: recompute_ordinary_files_git_only_valid; boundary: ordinary_file_never_collected. A3 positive: concern_probe_contradicts_no_program; boundary: existing_tests_local_probe_not_graduated. A4 positive: existing_over_cap_refusal_unedited; boundary: existing_moved_probes_not_counted_unedited.
- Risk: swap the two filter conditions — agent-decided: an AND of independent predicates keeps the same set, so `test_adversarial_probe_cap_coverage.py` coverage is preserved and stays unedited; `existing_` cases name its tests. Concern-bearing files are still collected.

**W1-02 Release 3.65.1**  after: W1-01  acceptance: 4
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `loom-code/README*.md`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A4 positive: existing_release_metadata_synchronized; negative: existing_sync_test_fails_on_old_pin.
- Risk: patch bump with a `## [3.65.1]` CHANGELOG entry and the pin-test rewrite as deliverables; derived manifests come from `scripts/sync_codex_manifests.py --all`, never hand edits.

## Simplicity check
- Prove A4 with the existing cap and graduated tests instead of two new cases — taken
- Keep `test_adversarial_probe_cap_coverage.py` unedited and drop the new `tests/local` boundary, leaving `probes.py` plus one test file — taken
- Drop W1-02's negative case and its A4 ownership — declined: `intake.test-case-pair` requires every task to own an Acceptance line with a pair; the pair now names the existing synchronization test, so no new test is added.

## Questions asked
① — consequence — 「這樣的理解對嗎？」 restated intent with the automatic-publication consequence (2026-11-11); the user chose 「現在修吧」 after asking for a re-evaluation and a reproduction run.
① — consequence — 「要改字還是改程式？」 after the adversary measured one git read per added file (2026-11-11): reword the Proposed outcome, recommended, or batch the reads; the user answered 「請繼續」.

## Risks
1. A concern-bearing added program beside a `no_program` record still runs collection during recomputation; that state already contradicts the record, and removing it would change which programs count (intent Constraints).
2. `finalize.py:287` shares the reordered filter; finalize-review executes suites by design, so it only loses redundant collection of ordinary files.
3. The hook-level test intercepts `subprocess.run` and `tempfile.TemporaryDirectory`; a collection route using another launcher would escape it, so the test also asserts `suite_collection` itself is never entered.
