# Every test lives in a tests folder, apart from the code it tests — plan
intent: 2026-09-25-tests-live-in-tests-folders@cafa860d
charter: 1.0

## Current State Evidence
- Forward: `scripts/run_package_tests.py:43-80` lists test folders by hand; skill `probes/` and `loom-workflow/.claude-plugin/` are absent.
- Reverse: 216 test files outside any `tests/` folder (104 loom-code scripts, 61 in skills, 36 plugin scripts/manifest, 15 root).
- Error: RL-06 in `loom-code/skills/closing-review/probes/` stayed red from PR #43 to PR #51 because the suite never collected it.
- Data: `evidence/baseline-counts.md` records per-command baseline: pytest 3568 passed/6 skipped, shell 145 PASS, 24 uncollected tests.
- Boundary: 65 loom-code tests use bare sibling imports; 22 use sibling-relative paths; duplicate basenames exist across loom-workflow skills.

## Task DAG

### Wave 0 — move tests, one owner at a time

**W0-01 Root: repository-level tests into `tests/`**  after: —  acceptance: 1, 2, 3
- Files: `scripts/test_*.py` → `tests/`, `.claude/hooks/test_*` → `tests/hooks/`, `scripts/run_package_tests.py`
- Test: A1 positive: no-root-test-outside-tests; negative: stray-root-test-detected. A2 positive: code-group-count-unchanged; boundary: hooks-tests-still-collected. A3 positive: new-root-test-picked-up; negative: tests-local-skipped.
- Risk: the suite inventory is rewritten here to discover every `tests/` folder (one session per plugin, `tests/local/` skipped); later tasks only move files; agent-decided.

**W0-02 loom-code: scripts tests and skill probes into `loom-code/tests/`**  after: W0-01  acceptance: 1, 2, 4
- Files: `loom-code/scripts/test_*.py` → `loom-code/tests/`, `loom-code/skills/*/probes/` → `loom-code/tests/`, `loom-code/tests/conftest.py`, `loom-code/tests/integration/` → `loom-code/tests/local/`, `loom-code/skills/closing-review/references/adversarial.md`, `loom-code/scripts/rehearse_probes.py`
- Test: A1 positive: scripts-and-skills-hold-no-tests; negative: probe-left-in-skill-detected. A2 positive: code-count-plus-23-probes; boundary: duplicate-basename-isolated. A4 positive: runtime-docs-name-new-paths; negative: old-path-in-runtime-doc-detected.
- Risk: conftest puts `loom-code/scripts` on the import path for 65 bare-import tests; 22 sibling-relative paths rewritten; assertions untouched; agent-decided.

**W0-03 loom-design: scripts tests into `loom-design/tests/`**  after: W0-02  acceptance: 1, 2
- Files: `loom-design/scripts/**/test_*.py` → `loom-design/tests/`, `loom-design/scripts/pytest.ini` → `loom-design/tests/pytest.ini`
- Test: A1 positive: design-scripts-hold-no-tests; negative: stray-design-test-detected. A2 positive: design-count-unchanged; boundary: importlib-mode-kept.
- Risk: its pytest.ini sets importlib mode, which is why it runs in its own session; the ini moves with the tests; agent-decided.

**W0-04 loom-workflow: skill, scripts and manifest tests into `loom-workflow/tests/`**  after: W0-03  acceptance: 1, 2
- Files: `loom-workflow/skills/*/scripts/test_*.py` → `loom-workflow/tests/<skill>/`, skill `conftest.py`/`pytest.ini` → same, `loom-workflow/scripts/test_*.py` → `loom-workflow/tests/scripts/`, `loom-workflow/.claude-plugin/test_plugin_manifest.py` → `loom-workflow/tests/`
- Test: A1 positive: skills-hold-no-tests; negative: stray-skill-test-detected. A2 positive: workflow-count-plus-1; boundary: duplicate-basenames-in-separate-sessions.
- Risk: per-skill subfolders keep duplicate basenames apart and carry each skill's conftest/pytest.ini; sibling imports of skill scripts go through conftest; agent-decided.

### Wave 1 — convention, CI and release

**W1-01 State the convention; align CI and runtime documents**  after: W0-04  acceptance: 3, 4, 5
- Files: `AGENTS.md`, `.github/workflows/*.yml`, `docs/loom/evidence/mechanisms.yaml`, `docs/loom/memory/*.md`, `docs/loom/2026-09-25-tests-live-in-tests-folders/evidence/after-counts.md`
- Test: A3 positive: ci-runs-same-groups; negative: ci-path-filter-misses-tests. A4 positive: agents-md-states-tests-folders; negative: runtime-doc-old-path-detected. A5 positive: rules-26-mechanisms-unchanged; negative: no-dispatch-words.
- Risk: memory entries are durable guidance, so their test paths are updated; merged plans, reports and CHANGELOG history are not edited; agent-decided.

**W1-02 Release metadata for three plugins**  after: W1-01  acceptance: 5
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-design/CHANGELOG.md`, `loom-workflow/CHANGELOG.md`, `README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A5 positive: versions-synchronized; negative: check-mechanisms-not-raised.
- Risk: patch bumps (no station guidance, field or rule change); loom-design and loom-workflow manifests and READMEs are bumped in the same commit though not listed here for the eight-entry cap; agent-decided.

## Questions asked
① — what — 可以先研究一下業界慣例 看一下業界到底是把 skill 測試放在哪裡嗎？
① — what — 我在考慮是不是應該要放 testing 之類的資料夾 更明確區分是測試用的 還是實際生產用的
① — what — 評估直接整個 repo 改完
① — what — 根目錄裡的測試應該也要一起搬吧？ 都要統一了說
① — done — 對
① — consequence — 本機專用的整合測試：放 tests/local/ 並讓 package 測試跳過（A，推薦）／全部照跑／留在原處
① — done — Ａ

## Risks
1. Acceptance 2 is the oracle: before/after pytest and shell totals per plugin must match plus 24 newly collected tests; any gap means a lost test, not a flaky one.
2. user-decided — local-only integration tests live in `tests/local/`, which the package suite skips (option A, 2026-09-25); the two failing scripts are a separate follow-up.
3. Two local-only integration scripts fail on this machine before the move; fixing them is out of scope and is reported as a follow-up.
