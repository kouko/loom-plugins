---
name: the-package-suite-needs-pyyaml-in-uvs-base-interpreter
description: The KICKOFF package-tests command (`uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family`) only passes when the base interpreter uv builds its venv on can itself import PyYAML — otherwise ~38 hook, launcher and agy-adapter tests fail with "installed runtime failed Python/PyYAML validation", "uv is unavailable" or "python3 not found", on untouched main too, while CI stays green; check `uv python find` and point UV_PYTHON at an interpreter whose base has PyYAML before suspecting the change or the uv cache
type: gotcha
sources:
  - resource: branch feat/2026-11-20-land-keep-worktree (2026-11-21) — complete suite failed 38/2920 on the change and the same files failed on untouched origin/main b2c4bdc8 while its CI passed; uv had picked an active conda base without PyYAML; rerun with UV_PYTHON set to an interpreter with PyYAML passed
---

**Trigger:** the complete package suite fails locally in
`loom-code/tests/test_loom_python_runtime.py`, `loom-code/tests/test_hooks_json.py`,
`loom-code/tests/test_agy_adapter.py`, `loom-code/tests/test_opencode_loader.py`
or the hook-recovery tests with launcher messages about PyYAML validation,
a missing uv or a missing python3, and the change touched none of those
areas.

**Correct path:** run `uv python find` from the repository root. If the
interpreter it names cannot run `python -E -s -c "import yaml"`, rerun the
suite (and later `finalize-review`, which executes the same declared command)
with the UV_PYTHON environment variable set to an interpreter whose own
site-packages has PyYAML. Confirm by running the failing files on an
untouched checkout of origin's main branch first: identical failures there mean the
environment, not the change.

**Why:** `fake_uv` in `loom-code/tests/test_loom_python_runtime.py` (and the
hook tests that share the pattern) builds the fake loom runtime by
symlinking its python to `sys.executable`. Outside the uv venv's own
directory that symlink resolves to the base interpreter, and the launcher
validates the runtime with `-E -s`, so only the base's site-packages count.
`.github/workflows/loom-code-ci.yml` pip-installs the lock into the
setup-python 3.11 base, which is why CI never sees it. uv prefers an active
conda base environment when choosing the base, so the same command can pass
in one shell and fail in another.

**Limits:** this is the workaround, not a fix — making the fake runtime
independent of the base interpreter's site-packages would remove the
dependency. Until then, the declared command is only reproducible on a base
that already carries PyYAML.
