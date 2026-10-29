# The detected package suite runs in a uv project's locked environment — plan
intent: 2026-10-29-suite-runs-in-locked-env@fd80ec8fd372be45c8740ea99ba45c977cb9f82f
charter: 1.1

## Current State Evidence

- Forward — `declared_test_command` returns a declared `package-tests:` first, else the first `TEST_COMMAND_MARKERS` row (`loom-code/scripts/loom_checker/probes.py:26-31`, `:775-815`).
- Reverse — finalize-review runs that command as the package suite (`command_handlers/finalize.py:298`); Build runs it at end of Build (`skills/build/SKILL.md:118-121`).
- Error — `_direct_pytest_collects` accepts only conda, bare pytest and `python -m pytest` forms, else returns not collected (`probes.py:160-180`).
- Data — a revision read uses `git ls-tree` names, so only a committed `uv.lock` counts (`probes.py:796-804`); `_python_argv` already unwraps `uv run` (`probes.py:704-716`).
- Boundary — trial on a fresh sandbox clone, uv 0.13.1: plain `uv run` rewrote a stale `uv.lock`; `--locked` stopped with an `uv lock` hint, lock untouched.

## Task DAG

### Wave 1 — detect the uv command and recognize it

**W1-01 Detect `uv run --locked python -m pytest -q` for a committed uv.lock**  after: none  acceptance: 1, 2, 3
- Files: `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_loom_attestation.py`
- Test: A1 positive: uv-lock-with-pyproject-detects-uv-locked-command; boundary: uv-lock-uncommitted-at-revision-detects-python3. A2 positive: pyproject-without-uv-lock-unchanged; negative: declared-package-tests-wins-over-uv-lock. A3 positive: detected-command-carries-locked-flag; negative: no-frozen-or-bare-uv-run.
- Risk: agent-decided — one marker row ahead of the pyproject row; `--locked` over `--frozen` or plain `uv run` per the Boundary trial; existing detection tests in `test_loom_attestation.py` preserved.

**W1-02 Pytest collection recognizes the `uv run ... python -m pytest` suite form**  after: W1-01  acceptance: 4
- Files: `loom-code/scripts/loom_checker/probes.py`, `loom-code/tests/test_selection_finalize.py`
- Test: A4 positive: uv-pytest-suite-finalizes-a-collected-graduated-probe; negative: uv-pytest-suite-refuses-a-probe-outside-its-paths.
- Risk: agent-decided — one generic branch: split the command where `_python_argv` unwraps it, replacing the conda-only slice; shim `uv` on PATH; conda and python cases in `test_selection_finalize.py` preserved.

### Wave 2 — release

**W2-01 Release loom-code 3.52.0**  after: W1-02  acceptance: 1
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README*.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A1 positive: every loom-code manifest and README reads 3.52.0; negative: an unsynchronized derived manifest fails the pin.
- Risk: bump `.claude-plugin/plugin.json`, then `sync_codex_manifests.py --all`; minor bump because detection behaviour changes; lands before finalize-review.

### Wave 3 — probe graduation

**W3-01 Graduate the ignored-uv.lock probe into the loom-code suite**  after: W2-01  acceptance: 2
- Files: `docs/loom/2026-10-29-suite-runs-in-locked-env/evidence/probes/test_ignored_uv_lock.py`, `loom-code/tests/test_probe_ignored_uv_lock.py`
- Test: A2 positive: the moved probe passes at its suite path and keeps its `concern:` line; negative: the store path no longer exists.
- Risk: the probe caught a defect on this change (fixed in db6ea09c), so closing review requires it in the suite before finalize-review; content unchanged except paths it resolves.

### Wave 4 — acceptance-test fix

**W4-01 Build step 3 names where the detected suite command comes from**  after: W3-01  acceptance: 1
- Files: `loom-code/skills/build/SKILL.md`, `loom-code/tests/test_build_mechanical_checks.py`, `loom-code/CHANGELOG.md`
- Test: A1 positive: build-step-3-points-to-the-checker-marker-table; negative: build-step-3-carries-no-copied-marker-command.
- Risk: acceptance testing found Build step 3 leaves the detected command to agent judgment; point to `TEST_COMMAND_MARKERS` in `probes.py` rather than copy its rows, so one table stays the source; existing tests in `test_build_mechanical_checks.py` preserved.

## Simplicity check
- One generic `_python_argv`-based branch in `_direct_pytest_collects` replacing the conda-only slice instead of adding a uv branch — taken
- Merge W1-02 into W1-01 — declined: the merged Test line exceeds the 40-word cap and separate tasks keep one RED test per Acceptance group

## Questions asked
① — what — （第一次）F2 intent 重述：uv 專案用鎖定環境跑測試；含自動發布後果、複雜度結論、對抗測試指令範圍外 — 以上都對嗎？
① — what — （更新後）加入 uv run --locked、鎖檔不被改寫、graduated program 認得 uv 寫法、跑測試不改已提交檔案 — 以上都對嗎？

## Risks
1. A machine with `uv.lock` committed but no `uv` installed now fails the suite with "command not found" instead of running bare `python3`; accepted at ① as the clearer failure.
2. Adversarial programs still record their own command (intent Out of scope); in a uv repo the adversary may need a `uv run` prefix it chooses itself.
3. An in-flight branch in a uv repo without a declared command sees its detected command change on upgrade, making an existing attestation stale.
4. user-decided — second-vendor selection-confirmed: codex
