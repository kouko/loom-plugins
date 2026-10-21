# Reliable Loom Python runtime — acceptance test evidence

Tried on 2026-10-21 in a fresh `git clone --no-local` at `01bf1afebb8a4e669e6362ad3e3a82c35de42eaa`, at `/private/tmp/loom-acceptance.0QMDbQ/repo`. Source was `/Users/kouko/.herdr/worktrees/loom-plugins/loom-plugin-dependicy`. The source tree had no pre-existing local changes. The clone and all runtime caches were outside the source tree. The repository README's checker setup was followed by invoking the launcher in the clean clone. Host plugin installation could not be exercised from this isolated environment.

## 1. Repair missing, old, or incomplete Python and rerun checks

- How I tried it: `XDG_CACHE_HOME=/private/tmp/loom-acceptance.0QMDbQ/runtime-cache UV_CACHE_DIR=/private/tmp/loom-acceptance.0QMDbQ/uv-cache UV_PYTHON_INSTALL_DIR=/private/tmp/loom-acceptance.0QMDbQ/uv-python loom-code/scripts/loom-python --repair --list-rules` in the clean clone. Initially, without `UV_PYTHON_INSTALL_DIR`, sandbox write restrictions prevented uv's Python download directory from being created; the second invocation placed all uv state under `/private/tmp`.
- What came back: the first sandboxed run exited 2 after DNS failure. A later network-approved run used a second, entirely new cache at `/private/tmp/loom-acceptance-real.XCVWZm` with `XDG_CACHE_HOME`, `UV_CACHE_DIR`, and `UV_PYTHON_INSTALL_DIR` all set there. The same `--repair contract --require 2.1` command downloaded and installed CPython 3.11.17 and PyYAML 6.0.2, exited 0, and printed `contract 2.3.1 satisfies requires-contract >=2.1`. No project environment was modified. uv warned that an unrelated existing `~/.local/bin/python3.11` was not uv-managed; it did not replace that executable.
- Evidence: the real runtime's `bin/python --version` printed `Python 3.11.17`, and `import yaml; print(yaml.__version__)` printed `6.0.2`. `test_repair_then_ready_offline_uses_cached_interpreter` and `test_script_mode_uses_runtime_and_preserves_script_exit` also passed, though their fake uv alone would not prove a real installation.

## 2. Skills and host hooks use the repaired environment despite an unsuitable default

- How I tried it: After the real repair, ran `XDG_CACHE_HOME=/private/tmp/loom-acceptance-real.XCVWZm/cache PATH=/usr/bin:/bin loom-code/scripts/loom-python --ready contract --require 2.1`. `/usr/bin/python3 --version` reported `Python 3.9.6`, and its `import yaml` failed. Extracted the `PreToolUse` shell command from each of the four host hook JSON files and executed each with its host-shaped `git status` input, the real repaired cache, and the same old-default PATH. Ran targeted station command and hook tests.
- What came back: the skill-style checker command exited 0 and reported a satisfied contract. Claude, Codex, OpenCode, and Antigravity hook commands each exited 0; Antigravity returned `{"decision": "allow"}`. This directly tested the configured command, not loading the plugin in a live host session.
- Evidence: actual host default `/usr/bin/python3` is 3.9.6 without PyYAML; actual cached runtime is 3.11.17 with PyYAML 6.0.2. `loom-code/tests/test_loom_runtime_skill_commands.py`, `loom-code/tests/test_hooks_json.py::test_host_hooks_use_ready_runtime_without_host_python`, and host hook tests passed. The targeted tests' own old-Python scenarios use fixtures; the real `/usr/bin/python3` observation is separate evidence.

## 3. Repair barriers are actionable and not misreported as a contract result

- How I tried it: With an empty cache and `PATH=/usr/bin:/bin`, ran `loom-code/scripts/loom-python --repair --list-rules` and `--ready --list-rules`; separately ran the real uv attempt above. Ran the read-only cache and corrupt runtime targeted tests.
- What came back: missing uv exited 2 with `uv is unavailable; install uv and rerun loom-python --repair`; missing ready runtime exited 86 with `run loom-python --repair`. Real network failure exited 2 with network, cache, and permission guidance. None printed `BLOCK contract.requires` or a pass. `test_repair_readonly_cache_reports_write_barrier` passed; its cache is chmod 0555, and this run did not use a live unwritable user account.
- Evidence: `loom-code/tests/test_loom_python_runtime.py::test_missing_installer_and_corrupt_cache_are_bootstrap_errors`, `loom-code/tests/test_runtime_readonly_cache.py::test_repair_readonly_cache_reports_write_barrier`, and captured command output above. Hook-specific fail-open diagnostics are covered by targeted host tests; they retain the pre-existing hook policy.

## 4. Checks run offline with a ready environment

- How I tried it: Reused the genuinely repaired cache with `XDG_CACHE_HOME=/private/tmp/loom-acceptance-real.XCVWZm/cache PATH=/usr/bin:/bin loom-code/scripts/loom-python --ready contract --require 2.1`. This PATH excludes `uv`. The earlier symlink fixture check was superseded by this real-cache check.
- What came back: exit 0 and `contract 2.3.1 satisfies requires-contract >=2.1`; no installer was invoked. The targeted offline reuse test also passed.
- Evidence: captured real-cache output and `loom-code/tests/test_loom_python_runtime.py::test_repair_then_ready_offline_uses_cached_interpreter`. Network disconnection itself was not induced, but the `--ready` path with no `uv` available completed using the existing runtime.

## 5. Project tests retain their own Python and packages

- How I tried it: Ran the targeted checks for station prose and launcher environment isolation. Compared the project test command shown in the closing-review instructions with the checker command; the former remains `python3 -m pytest <path>`.
- What came back: `test_project_python_commands_stay_project_owned` and `test_script_keeps_project_environment_without_importing_project_modules` passed. The latter checks that `PYTHONPATH`, `PYTHONHOME`, and `VIRTUAL_ENV` survive in the process environment while the checker itself isolates Python imports. No real user project was run both directly and through the full Loom flow, so equivalence of package versions and test result remains unobserved.
- Evidence: `loom-code/tests/test_loom_runtime_skill_commands.py` and `loom-code/tests/test_loom_python_runtime.py` in the targeted run.

## 6. Existing rule and hook outcomes remain usable

- How I tried it: With the prepared ready-cache fixture and `PATH=/usr/bin:/bin`, ran `loom-code/scripts/loom-python --ready contract --require 2.1`, `contract --require 999.0`, and `nonsense`. Ran hook and checker targeted tests.
- What came back: successful requirement exited 0 and printed `contract 2.3.1 satisfies requires-contract >=2.1`; impossible requirement exited 1 and printed `BLOCK contract.requires`; invalid subcommand exited 2 and printed usage. Host hook tests covered ready, missing-runtime, stale-root, and payload paths. Live host delivery was not observed.
- Evidence: targeted command: `/Users/kouko/.conda/envs/dbt-redshift/bin/python -m pytest -q loom-code/tests/test_loom_python_runtime.py loom-code/tests/test_runtime_readonly_cache.py loom-code/tests/test_loom_runtime_skill_commands.py loom-code/tests/test_dispatch_profile_resolver.py loom-code/tests/test_ship_worktree_merge.py loom-code/tests/test_hooks_json.py loom-code/tests/test_codex_stale_hook.py loom-code/tests/test_codex_hook_trust_contract.py loom-code/tests/test_language_anchor_hook.py tests/test_loom_plugin_install_layout.py`; result: `133 passed in 11.48s`. `python3 -m pytest` was also attempted but the system Python 3.15 lacked pytest; the installed project test environment's Python then ran the same targeted modules. The full package suite was not run here; `finalize-review` is scheduled to run it and blocks attestation on failure. No package-test or finalization skip was authorized.
