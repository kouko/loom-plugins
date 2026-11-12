# Build verification — W1-01 and W2-01

## Completed Build checkpoint

At `b3204e76a99c2c2af4be8188706f6edab58c051b`, the complete declared
package command exited 0: 4,261 pytest passes and 6 skips across its printed
pytest summaries, plus the runner's shell surfaces. See
[complete output](package-after-fix.txt). The earlier integration run exited 1
on the dispatcher architecture guard; [failed output](package-before-fix.txt)
is retained. The existing guard was preserved and the extra callable removed.

The independent adversary tried four attack points (2,460 argument permutations
and 13 real subprocess calls), found no defect and reused the existing CLI
test module with a concern-only annotation. See
[raw report](adversarial-review.yaml) and [results](attack-results.json).
After the fix, its declared command was rerun unchanged and exited 0 with
38 passes; [output](adversarial-after-fix.txt). No adversary redispatch was
needed: the existing program still passed and scope did not widen.

The installed `sync-trunk` command reported up to date before Build verification
and again before Closing Review: the branch already contained
`origin/main` at `ab40f0e634db492c9b250da8e95b53579aeb23c2`.
No unresolved adversary finding remains. This is mechanical Build evidence;
independent first-use acceptance and closing review are separate.

Commands:
- `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
- `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py`

Date: 2026-11-12. Worktree: `/private/tmp/loom-agent-tool-efficiency`.
W1 implementation was tested before commit; its subsequently committed source
is `b6084d6e55f8b5e293a662f265bb01c62d7d24e7`. W2 release checks below ran
with the 3.68.0 metadata changes uncommitted on that commit.

## Focused CLI tests

```text
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py -q
```

- Initial sandboxed invocation: exit 2 because uv could not write its existing
  cache lock; [setup output](w1-setup.log). This was not RED test evidence.
- Before production edits, after approved cache access: exit 1, **6 failed,
  32 passed in 4.45s**; [RED output](w1-red.log).
- After implementation: exit 0, **38 passed in 5.08s**; [GREEN output](w1-green.log).
- After import-order cleanup: exit 0, **38 passed in 5.30s**;
  [final focused output](w1-green-final.log).

The tests exercise exact command help through the public entry, help outside
a repository, malformed and rejected input, authorization-argument refusal,
incomplete delivery JSON, dispatcher compatibility and hook handling. Existing
tests remain intact. Original logs and the command record also remain under
`/private/tmp/loom-selfservice-w1/`.

## Release metadata

The Claude manifest is the 3.68.0 source of truth. Generated manifests were
updated with `python3 scripts/sync_codex_manifests.py --all` (exit 0); its
`--all --check` mode also returned 0. Other plugins have no changed files.

```text
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_write_plan_station_text.py -q -k 'current_release_metadata_is_synchronized or readme_version_matches_manifest or root_readme_plugin_table_row_version_matches_manifest'
```

Result: exit 0, **5 passed, 38 deselected in 0.03s**;
[release test output](release.log). This metadata-only change reused existing
tests; no artificial RED run was created. `git diff --check` returned 0.

## Limits

These are implementer-owned mechanical checks, not independent first-use or
acceptance evidence. No authentic review finalization, remote publication,
installed-host operation, cross-host compatibility or efficiency improvement
was established by these runs. The complete package suite, adversarial pass
and independent acceptance remain separate subsequent work. No user approvals
or reviewer judgments were synthesized for test or help examples.

## Build integration correction — dispatcher callable boundary

The subsequent orchestrator package run found the existing architecture test
`test_loom_checker_modules.py::test_entry_point_owns_only_cli_dispatch` failing:
the code group reported **1 failed, 2831 passed, 2 skipped in 120.39s**.
The original integration log remains at
`/private/tmp/loom-selfservice-package-build.log`; this supersedes the earlier
statement that the package suite was still subsequent work, but is not a
successful complete-suite result.

Defect class: an extra top-level callable violated the public dispatcher's
main-only architecture contract. The orchestrator's search covered the whole
contents of changed files and Acceptance 4 surfaces; it found only `help_hint`
and its two calls in `loom-code/scripts/loom_checker.py`, the only changed
production Python file. The implementer re-read that module and the existing
architecture test before editing. The fix removes the helper, computes an
optional hint string once inside `main`, and emits it at the same two error
paths. The existing architecture guard and CLI tests remain unchanged.

Focused reproduction before the fix:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_modules.py::test_entry_point_owns_only_cli_dispatch -q
```

Exit 1, **1 failed in 0.02s**; [retained RED output](dispatch-red.log).

Focused verification after the fix:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_modules.py loom-code/tests/test_loom_checker_cli.py -q
```

Exit 0, **43 passed in 21.30s**; [retained GREEN output](dispatch-green.log).
`git diff --check` returned 0. This correction did not rerun the complete
package suite or modify adversarial material; those integration steps remain
with the orchestrator. No closing-review or acceptance result is claimed.
