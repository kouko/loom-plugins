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

## Finalization refusal and bookkeeping repair

The first finalization attempt ran the complete suite and declared adversarial
program successfully, then refused to generate an attestation:

```text
finalize-review: package-tests passed
finalize-review: adversarial passed
BLOCK intake.intent-version: confirmation commit aa0f50a has an invalid intent pin; re-confirm the intent
```

The initial orchestrator computation incorrectly included the status line in
the confirmation hash. The canonical contract excludes both status and the pin
line. Repair retains the user's already confirmed content and publication
authorization, changes only bookkeeping and its plan reference, and preserves
the original failed evidence. The requirements and implementation do not change.
Build must rerun its checks; the same reviewers must read the repair delta before
finalization is attempted again. No attestation or publication success is claimed
from this refused attempt.

The repair worker observed the same intent-version check RED before repair and
GREEN (`[]`) after commit `dbec38f577f3ff009ea7a90991508e9f0b7b2bbf`.
The correct canonical identity is `56acccd13debac07366685edc4ee850e40bbde61`.
It also compared the original confirmation and repaired intent with both
excluded lines removed: the bytes were identical. Commit `eeecea327` updates
the plan reference and records the bounded bookkeeping task.

## Build revalidation after bookkeeping repair

At `4d282d7ab801be9ba95b004afa7eb5873437500d`, Build reran the exact complete
package command above and then the exact declared delivery adversarial command.
The ordered process exited 0. The full suite passed again (including 2,859 code
tests and all remaining family groups); the adversarial program collected and
passed all 12 tests in 7.15s. Captured logs are
`/private/tmp/loom-post-merge-build-suite-r2.log` and
`/private/tmp/loom-post-merge-build-adversarial-r2.log`.
The subsequent sync-trunk observation was up to date with `3bf50711f`.
The earlier passing results and refused finalization remain historical evidence;
neither substitutes for this revalidation or the next finalization.

The planning checks then rejected the repair note's word count and missing
positive/negative case pairs. The note was shortened and W4 was assigned only
to its affected Acceptance 3, with the observed identity cases. Both the plan
command and write-plan intake exited 0 before the final Build rerun. These
edits change no runtime source or confirmed requirement.
