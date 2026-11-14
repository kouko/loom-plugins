# Build verification

Date: 2026-11-14
Tested commit: 7de6f54ef6eb7a983d564403c49a151e1ebcd78a
Branch base after integration: 3bf50711f983e12ac25b219c6340f5b164f5201c

## Test-first implementation

The W1 implementer reported two new command-entry cases RED on the original
unidentified-change recovery advice, then 53 focused tests GREEN after the fix.
The release implementer reported the version-consistency case RED before
synchronization and GREEN afterward. These are attributed worker observations;
they are not reconstructed raw output from the orchestrator.

## Upstream integration

The first sync-trunk observed release metadata conflicts with upstream PR #158
and did not attempt a merge. The implementation worker integrated its 3.79.0
CLI advice without replacing this change's guidance or 3.80.0 metadata.
Subsequent sync-trunk returned up to date, including immediately before Review.
No original requirements changed and no review episode had begun.

## Complete package suite

Executed from the change worktree:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

Observed process exit: 0. Raw output was captured outside the repository at
`/private/tmp/loom-post-merge-build-suite.log`. Pytest session summaries follow;
shell tests and Mermaid validation also completed successfully. Existing skips
remain disclosed in the corresponding summaries; no skip was added by this change.

```text
2859 passed in 117.25s (0:01:57)
211 passed in 11.43s
53 passed in 2.63s
264 passed in 7.59s
64 passed in 12.22s
22 passed in 0.06s
13 passed in 0.03s
13 passed in 0.03s
58 passed in 3.43s
125 passed in 2.57s
250 passed, 5 skipped in 1.62s
12 passed in 0.02s
19 passed in 0.04s
163 passed in 1.79s
162 passed in 1.62s
13/13 mermaid blocks parsed
PASS — validator exits 1 on the A -> B block
```

## Adversarial execution

The independent adversary reported nine attempted attack points, zero successful
attacks and no new program. It reused the existing delivery test and committed
only a concern comment. Its report includes literal-reading checks, not a claim
of verified live host termination enforcement.

Build independently ran the declared program after the package suite:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_delivery.py
```

Observed process exit: 0; collected 12 items and 12 passed in 10.77s.
Raw output: `/private/tmp/loom-post-merge-build-adversarial.log`.
No unresolved adversarial findings. Finalization must rerun both the suite
and this program; this note does not substitute for those executions.
