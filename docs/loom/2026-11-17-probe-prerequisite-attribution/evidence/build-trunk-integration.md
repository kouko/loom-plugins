# Build trunk integration and release collision

## Initial refusal

The installed `sync-trunk` fetched `origin/main` at
`d3faa624d436f22aaa083b8f2b163bb924c2e7ba` (PR #165, roadmap simplification),
then exited 1 before attempting the merge. Its captured output was:

```text
BLOCK review.sync: conflict: README.md
BLOCK review.sync: conflict: loom-code/CHANGELOG.md
BLOCK review.sync: the merge was not attempted; testing-file-limit is still at 8c51d0182788b39943bac45bd0254fd4ca5a12b5 and the worktree is untouched.
BLOCK review.sync: Conflicts are never resolved automatically -- resolve them in a new build round.
Suggested next step: Preserve outstanding work and resolve the reported trunk condition before deliberately rerunning the existing sync workflow.
```

## Manual Build integration

Defect class: concurrent release metadata collision. The cumulative upstream
paths and all locally edited release surfaces were examined. A local
`git merge --no-commit --no-ff origin/main` reproduced conflicts only in
`README.md` and `loom-code/CHANGELOG.md`.

The resolution preserves upstream roadmap behavior and documentation,
loom-design 2.26.0, loom-workflow 5.26.0, and the upstream loom-code 3.83.0
changelog section. This change's release moves to loom-code 3.84.0. Only the
Claude manifest source was edited; `scripts/sync_codex_manifests.py --all`
regenerated the derived release metadata. Root and translated loom-code
READMEs and the existing CURRENT_VERSION test pin were synchronized.

Exact postmerge HEAD: `55952410187ddcb2fd2fe70659cb4370d0ea71f4`.

Merge parents:

- Local Build: `8c51d0182788b39943bac45bd0254fd4ca5a12b5`.
- Fetched trunk: `d3faa624d436f22aaa083b8f2b163bb924c2e7ba`.

The postmerge diff against upstream README contains only this change's two
loom-code version replacements. Its changelog retains the upstream entry and
adds this change's 3.84.0 section. Comparison against the premerge Build HEAD
shows no changes to `probes.py` or `probe_attribution.py`.

## Verification and remaining work

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_adversary_protocol.py -q
```

Result: **56 passed in 0.25s**. Manifest synchronization check
`python3 scripts/sync_codex_manifests.py --all --check` and
`git diff --check` passed before and after the merge commit.

The earlier 84-test focused attribution result remains historical; the full
package suite is still owed after this merge. No adversary, finalizer,
finance test, remote publication or installed-cache update was run.
