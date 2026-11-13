# Build verification — read-only JSON pilot

Worker evidence, 2026-11-14. Independent acceptance testing, adversarial testing,
complete package suite, closing review, CI and merge are pending at this record.
These checks do not establish installed-plugin parity, live-host reloading,
completed review or authorization beyond the confirmed intent.

## W1-01 — public-entry extension

Source commit: `3c843616952e91922f9ea8d5d3ca87b7e9991c10`.
Six planned files changed: four production files and two existing test files.
Actual delta: production +67/-16 (net +51); tests +86/-3 (net +83);
total +153/-19 (net +134). No new dependency or generic result framework.

Focused command:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_preparation_json.py loom-code/tests/test_loom_checker_cli.py -q -rs
```

- RED, before production changes: **3 failed, 43 passed in 11.29s**.
  The three new public-entry tests each raised `JSONDecodeError: Expecting
  value: line 1 column 1 (char 0)` because the old commands rejected the final
  selector and emitted no JSON stdout. Log: `/private/tmp/loom-readonly-json-red.txt`.
- First implementation run: **2 failed, 44 passed**. One test incorrectly
  expected manifest version `2.0` (actual `2.3.1`); the other exposed selected
  reviewer help reaching repository lookup. Corrected the expectation and
  bounded help validation to the new selected mode, preserving text parsing.
  Log: `/private/tmp/loom-readonly-json-green.txt`.
- Final exact tree: **47 passed in 15.97s**, using the focused command plus
  `loom-code/tests/test_loom_python_runtime.py::test_all_command_help_uses_ready_runtime_without_repair`.
  Log: `/private/tmp/loom-readonly-json-green-final.txt`. An earlier green run
  passed the same 47 cases before moving the `io` import to module scope.

Coverage adds typed contract observations, compatibility blockers, last-value
wins, whitespace/leading-zero behavior, reviewer floors one/two, unchanged
change-id, argument/selector validation before domain reads, missing/dirty
repositories and late caught usage/internal failures. Late-failure cases first
populate data and both streams, then verify one complete object, empty stderr
and all-null domain data. Existing preparation/delivery shape and text/exit
baselines remain in the focused suites. No complete package suite was run by
this worker.

The first sandboxed test attempt could not create a lock in the existing uv
cache. The offline command then used authorized host-cache access; no fresh
cache/download was requested. Linked-worktree metadata similarly required
host permission for the scoped commit.

## W2-01/W2-02 — release and consumer documentation

The orchestrator freshly verified remote main as
`80c8a2744bb8f9a5087bd9ef8e47d73ec6d9ca47`; planned minor `3.76.0` was retained.
Only the Claude manifest was edited as the version source; mirrors were derived
with `python3 scripts/sync_codex_manifests.py --all`. Historical changelog
sections remain; localized README changes contain version strings only.

Existing release guards, before and after the packet:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_write_plan_station_text.py -k 'current_release_metadata or readme_version or root_readme_plugin_table or root_readme_loom_code_section' -q -rs
python3 scripts/sync_codex_manifests.py --all --check
git diff --check
```

Both pytest runs: **6 passed, 37 deselected in 0.03s**. Manifest sync check and
diff whitespace check exited 0. Logs:
`/private/tmp/loom-readonly-json-release-before.txt` and
`/private/tmp/loom-readonly-json-release-after.txt`.

The documented Python block was extracted verbatim from the English README,
substituting only its explicit plugin path placeholder, and executed against
the actual `scripts/loom-python --ready` entrypoint in a temporary clean Git
repository. Existing fixture setup created the repository; the documented
consumer itself invoked only the read-only commands.

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python /private/tmp/loom-readonly-json-examples.py
```

| Actual input/state | Process result and consumer decision |
|---|---|
| Contract requirement `2.0` | Exit 0; typed `compatible: true` permits the simulated next step. |
| Clean empty delta | Exit 0; typed floor 2 requires two simulated distinct reviewers. |
| Clean committed Markdown-only delta | Exit 0; typed floor 1 requires one simulated distinct reviewer. |
| Requirement `2.99` | Exit 1; consumer rejects the blocked observation. |
| Requirement `bad` | Exit 2; consumer rejects the usage error. |
| Duplicate selector or reviewer mixed help | Exit 2; consumer rejects each error. |
| Dirty or missing repository | Exit 2; consumer rejects each error. |
| Cold runtime via temporary `XDG_CACHE_HOME` | Exit 86; no parseable JSON, consumer rejects before reading data. |

Consumer output: `/private/tmp/loom-readonly-json-examples.txt`. These are
worker example checks, not independent dogfood. Floor two is not a complete
classification claim. No paid model, real external writer, installed-plugin
update or efficiency measurement was performed. Temporary scripts/logs are
local evidence; retained commands, inputs, outcomes and limitations above allow
the independent acceptance owner to replay the behavior.

Self-review checked dropped sentences, numbers, names, obligation words and
cross-references across every modified README/changelog paragraph. The two
new modes are additive; delivery's distinct shape and preparation's six fields
are preserved. Full-suite/adversarial/acceptance/review results must be added
by their respective owners rather than inferred from these focused checks.
