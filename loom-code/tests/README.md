# loom-code tests

loom-code's pytest files live here, apart from the scripts and skills they
test; `conftest.py` puts `loom-code/scripts/` on the import path for the
tests that import a script by bare module name. The package suite
(`scripts/run_package_tests.py --loom-family`) runs this folder in its `code`
group.

| Directory | What it holds |
|---|---|
| [`local/`](local/) | Cross-plugin behaviour scripts — loom-code beside `domain-teams:code-team`, `loom-workflow:git-memory`, and obra/superpowers. Each skips gracefully when its other plugin is absent. Local-only: the package suite does not run this folder. |

The pre-1.0 prompt clusters (`skill-triggering/`, the `*-pressure/`
directories, `codex-cli/`) were manual eyeball rituals over skills that no
longer exist. Their successor is the cold-read dogfood registered in
`docs/loom/evidence/mechanisms.yaml`: a fresh agent is handed one station's
SKILL.md and one real task, and the result is recorded as an eval rather
than read once and thrown away.

## Running `local/`

```bash
bash loom-code/tests/local/test-code-team-coexistence.sh
```

All of them are local-only: they read the installed CLI's plugin state, so
a runner without `claude` reports SKIP rather than PASS.
