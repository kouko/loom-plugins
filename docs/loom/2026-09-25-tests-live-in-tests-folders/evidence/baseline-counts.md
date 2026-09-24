# Package-suite baseline before the move

Measured 2026-09-25 on origin/main 23dad634 with
`uv run --isolated --with-requirements requirements-package-tests.lock` and one
subprocess per command from `scripts/run_package_tests.py::loom_family_commands`.
Every command exited 0.

| Group | Command target | Result |
|---|---|---|
| code | `loom-code/scripts/ scripts/ .claude/hooks/` (xdist) | 2271 passed, 2 skipped |
| design | `loom-design/scripts/` | 245 passed, 1 skipped |
| workflow-python | `loom-workflow/tests/test_loom_visualization_page_scripts.py` | 52 passed |
| workflow-python | `loom-workflow/scripts` | 196 passed |
| workflow-python | `loom-workflow/skills/decision-map/scripts` | 261 passed |
| workflow-python | `loom-workflow/skills/distill-sessions/scripts` | 121 passed |
| workflow-python | `loom-workflow/skills/git-memory/scripts` | 64 passed |
| workflow-python | `loom-workflow/skills/goal-create/scripts` | 43 passed |
| workflow-python | `loom-workflow/skills/handoff/scripts` | 13 passed |
| workflow-python | `loom-workflow/skills/independent-advisor/scripts` | 1 passed |
| workflow-python | `loom-workflow/skills/loom-memory/scripts` | 80 passed, 3 skipped |
| workflow-python | `loom-workflow/skills/loom-visualization/scripts` | 209 passed |
| workflow-python | `loom-workflow/skills/recap-state/scripts` | 12 passed |
| workflow-shell | 17 `loom-workflow/tests/test-*.sh` scripts | 145 PASS / 0 FAIL in total |
| workflow-mermaid | `npm ci` + `validate_mermaid.mjs` + negative check | pass |

Totals: pytest 3568 passed, 6 skipped (code 2271/2, design 245/1, workflow-python
1052/3); shell 145 PASS.

Not collected by the suite at baseline:

| Path | Tests | Result when run by hand |
|---|---|---|
| `loom-code/skills/build/probes/` | 8 | 8 passed |
| `loom-code/skills/closing-review/probes/` | 13 | 13 passed |
| `loom-code/skills/ship/probes/` | 2 | 2 passed |
| `loom-workflow/.claude-plugin/test_plugin_manifest.py` | 1 | 1 passed |
| `loom-code/tests/integration/*.sh` (local-only) | 4 scripts | 2 exit 0, 2 exit 1 on this machine |

After the move the suite must report the same per-plugin pytest totals plus the
24 newly collected tests (code +23, workflow +1), the same shell totals, and the
mermaid check; the local-only integration scripts stay out of the suite.
