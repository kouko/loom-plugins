# Reliable Loom Python runtime — plan
intent: 2026-10-21-reliable-loom-python-runtime@8375940dd918f679d9e14932811b51a149e271dc
charter: 1.1

## Current State Evidence
- Forward: `loom-code/skills/write-plan/SKILL.md` Step 0 invokes `python3` before checking the contract.
- Reverse: `loom-code/hooks/hooks-codex.json` invokes the same checker with the host's `python3`.
- Error: `loom-code/scripts/loom_checker/probes.py` imports `tomllib` at module load, before checker error handling.
- Data: `loom-code/scripts/loom_checker/helpers.py` imports third-party `yaml`; `requirements-dev.txt` is for development, not installed-plugin runtime.
- Boundary: `loom-code/scripts/loom_checker.py` delegates project test commands; a plugin runtime must not replace their interpreter or packages.

## Task DAG

### Wave 0 — establish the runtime boundary

**W0-01 Repair and invoke a plugin-owned checker runtime**  after: none  acceptance: 1, 3, 4
- Files: `loom-code/scripts/loom-python`, `loom-code/tests/test_loom_python_runtime.py`
- Test: A1 positive: clean-uv-repair; boundary: no-installer. A3 positive: actionable-failure; negative: no-contract-misreport. A4 positive: ready-offline; boundary: corrupt-runtime.
- Risk: agent-decided — use uv and a versioned user cache; avoid changing the project interpreter. Preserve checker exit codes and show bootstrap errors separately.

### Wave 1 — route every entry through that boundary

**W1-01 Route station commands through the launcher**  after: W0-01  acceptance: 2, 5, 6
- Files: `loom-code/skills`, `loom-code/tests/test_loom_runtime_skill_commands.py`
- Test: A2 positive: station-old-default; negative: stale-command. A5 positive: project-test-env; boundary: isolated-checker. A6 positive: rule-list; negative: bad-input.
- Risk: agent-decided — replace checker and companion runtime invocations in station prose; retain explicit project test commands unchanged.

**W1-02 Route host hooks through a ready runtime**  after: W0-01  acceptance: 2, 3, 6
- Files: `loom-code/hooks`, `loom-code/hooks.json`, `loom-code/tests/test_hooks_json.py`, `loom-code/tests/test_codex_stale_hook.py`
- Test: A2 positive: four-host-ready; negative: old-default. A3 positive: missing-runtime-diagnostic; boundary: stale-plugin. A6 positive: valid-hook; negative: invalid-payload.
- Risk: agent-decided — hooks never install packages; preserve each host's existing allow/deny and stale-checker behavior while surfacing repair guidance.

### Wave 2 — integration and release

**W2-01 Verify the installed-plugin path and release metadata**  after: W1-01, W1-02  acceptance: 1, 2, 3, 4, 5, 6
- Files: `loom-code/tests/test_loom_python_runtime.py`, `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/README.md`
- Test: A1 positive: fresh-install; negative: blocked-install. A2 positive: hook-reuse; boundary: old-python. A3 positive: clear-error; negative: false-pass. A4 positive: offline-reuse; boundary: no-cache. A5 positive: project-command; negative: env-leak. A6 positive: package-suite; negative: invalid-hook.
- Risk: agent-decided — bump plugin version before closing review; test a Python 3.9 host path and a ready offline path without mutating the developer's project environment.

**W2-02 Graduate the cache-permission adversarial probe**  after: W0-01  acceptance: 3
- Files: `docs/loom/2026-10-21-reliable-loom-python-runtime/evidence/probes/test_runtime_readonly_cache.py`, `loom-code/tests/test_runtime_readonly_cache.py`
- Test: A3 positive: readonly-cache-guidance; negative: false-stale-lock.
- Risk: agent-decided — the adversary observed RED at 9c013f0a; move its executable case unchanged into the package suite after the launcher fix.

## Simplicity check
- Pin the single runtime package in the launcher rather than add a requirements file — taken

## Questions asked
- ① — what — 先完成 Loom agent 自行修復環境，成功後再深入研究 Go 重構，對嗎？

## Risks
1. The bootstrap needs a trusted installer and writable cache; neither can be assumed on every host.
2. Publication hooks have intentional fail-open paths; bootstrap failures need explicit diagnostics without silently changing that policy.
