# Build verification — W1-01 and W2-01

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
