# Advanced-trunk integration for the JSON pilot

The parent observed sync-trunk BLOCK before closing review: upstream PR 148
advanced origin/main to `b9ebc787dc4e3c73d1ab0257302b1516b2be3550` and consumed
loom-code 3.71.0. W4 was added and committed as `3b0d6f0b` before any merge.
The first plan check rejected an overlong Risks item; its wording was shortened
and the check passed before that commit. No requirement or comparison metric
changed, and no closing-review episode had begun.

`git merge --no-commit origin/main` produced exactly the expected README and
code CHANGELOG conflicts. Resolution preserves upstream design 2.25.0,
engineering/design research simplification content and the upstream 3.71.0
CHANGELOG entry. This branch's JSON release becomes 3.72.0 above it. The SSOT,
generated manifests, root and three language READMEs, and CURRENT_VERSION pin
are synchronized. No reset, history rewrite, worktree deletion or attestation
edit was performed.

The integration defect class is a concurrent release-packet collision. The
searched surfaces were both conflicted files, all four code manifests, four
README version surfaces, and the release pin test. Historical 3.71.0 references
in already-executed comparison and Build evidence remain historical and are
not rewritten. W2's fixed candidate `2cef40163b6a562971780da6e6fd107289304962`
still identifies the actual tested JSON implementation, not this integrated
release. Neither R1 nor R2 is relabeled as a new operator run.

Comparing the working tree with pre-merge HEAD shows no change under
`loom-code/scripts/loom_checker.py` or `loom-code/scripts/loom_checker/`.
Comparing against origin/main shows no changes under `loom-design/`,
`loom-code/skills/engineering-research/`, the upstream research change store or
its standalone research record. Upstream research/test changes are retained.
The full merge and cumulative path inventories are retained in
[integration-changed-paths.txt](integration-changed-paths.txt).

Commands executed successfully on the resolved integrated tree:

```text
python3 scripts/sync_codex_manifests.py --all
python3 scripts/sync_codex_manifests.py --all --check
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_preparation_json.py loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_loom_checker_modules.py loom-code/tests/test_write_plan_station_text.py -q
```

Actual focused output:

```text
........................................................................ [ 79%]
...................                                                      [100%]
91 passed in 10.21s
```

Raw focused log: `/private/tmp/loom-json-w4-focused.log`. Scoped whitespace
checking passed. The implementer did not rerun the complete suite or adversarial
program, obtain independent acceptance/review or create an attestation on this
integrated content. Those remain the parent's subsequent Build/review work.

Whole-index whitespace checking reports inherited EOF blank lines in the
upstream `2026-11-12-design-research-method-selection` store:
`acceptance-test-report.md:38`, `evidence/acceptance-test-evidence.md:176`,
`evidence/baseline-trials.md:396` and `evidence/candidate-trials.md:407`.
These upstream records are preserved byte-for-byte; they are not cleanup
edits in the release-packet resolution.
