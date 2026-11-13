# Help-only release Build verification

Functional candidate: `c620ced91667d6d564dd5516f613923117a92bc4`.
Base: `fbdc29af358413bc9d55b599231b2a6cbcb4524d`.
No workflow step was skipped. The user's confirmed scope now excludes new JSON.

## Synchronization and release

The installed `loom-python --ready sync-trunk` fetched origin and reported up
to date at `9cedb9f9917640917d1b39d75ce384de59a0b63e`, with origin/main
`fbdc29af358413bc9d55b599231b2a6cbcb4524d`; no commit was added. Only the
adversary's concern comment and evidence followed that synchronization.
Release metadata is 3.73.0; the existing release guard observed RED then GREEN
(6 passed, 37 deselected), and derived manifest check passed.

## Complete suite

Executed from the candidate checkout:

`uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`

Exit 0. Across the runner's isolated pytest invocations: **4264 passed, 11
skipped**, plus all shell and Mermaid groups passed. The runner prepares
Mermaid dependencies after workflow Python tests; five visualization tests
therefore skipped on this initial fresh-worktree invocation. After preparation,
the entire visualization test directory was independently rerun using the same
locked uv environment: **253 passed, zero skipped**, including those five.
The remaining six skips are not counted as passes. Finalization will rerun the
complete suite on the committed reviewed content with dependencies present.

Raw complete output: `/private/tmp/loom-help-release-package-tests.txt`.
Supplement output: `/private/tmp/loom-help-release-visualization-supplement.txt`.

## Adversarial handoff and rerun

Independent adversary `help_release_adversary` reported eight attack points,
zero successful attacks, zero new programs, and one reused repository test.
Its report is [adversarial-help-release.md](adversarial-help-release.md).
The unchanged trial program remains outside the repository; no new green
program was added merely to create evidence. No unresolved finding or
adversary redispatch is present.

Declared artifact: `loom-code/tests/test_loom_checker_cli.py`.
Executed after the complete suite:

`uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py`

Exit 0, **39 passed in 9.29s**. Raw output:
`/private/tmp/loom-help-release-adversarial-rerun.txt`.
No live publication, merge, cleanup, hook installation or paid review ran.

## Next boundary

Build functional checks pass, subject to the explicitly recorded six skips.
Independent clean-copy acceptance, branch-end reviews and generated
attestation remain required. Earlier help checkpoints and the Claude audit
are retained historical evidence, not substitutes for final-content reviews.

## Reverification after acceptance document findings

The first clean-copy acceptance at `1ccb7f514ec63aaf2d02d90108ea5b67d65fe4b7`
found stale current README discovery guidance and a research snapshot labeling
clarification. The original partly result is committed at `b824c462`.
The bounded fix `34143f6cc4a1aa349ba5672caaaf0de95487de8d` updates README,
research context and the retained plan only; dispatcher, handlers and tests
are unchanged. The prior adversary's program remains applicable and passed,
so no adversary redispatch or new green program was needed.

At the fixed commit, `sync-trunk` fetched and reported up to date against the
same origin/main `fbdc29af358413bc9d55b599231b2a6cbcb4524d`. The complete suite
command above ran again: **exit 0, 4269 passed, 6 skipped**, with every shell
and Mermaid group successful. All five earlier visualization dependency skips
now executed. Raw output:
`/private/tmp/loom-help-release-package-tests-final-build.txt`.

The same declared adversarial command then reran: **exit 0, 39 passed in
9.29s**. Raw output:
`/private/tmp/loom-help-release-adversarial-final-build.txt`.
The original Build result remains above; these are new observations rather
than edits to the earlier numbers. Clean-copy acceptance is being rerun for
the document fix before branch-end reviewers are dispatched.

## Round 2 after canonical confirmation repair

Round-1 finalization passed both functional execution stages but refused the
old canonical confirmation ancestry; no attestation was generated. The actual
cause and narrow repair are retained in
[confirmation-provenance-fix.md](confirmation-provenance-fix.md). This does not
change the user's help-only requirements or retry accounting.

At `6aad2e920e7d2507f26a659295ab573e4518dfd8`, `sync-trunk` fetched and reported
up to date against origin/main `fbdc29af358413bc9d55b599231b2a6cbcb4524d`.
The complete suite above reran: **exit 0, 4269 passed, 6 skipped**, all shell
and Mermaid groups passed. Raw output:
`/private/tmp/loom-help-release-package-tests-round2.txt`.
The same reused adversarial command reran afterwards: **exit 0, 39 passed
in 9.38s**; output `/private/tmp/loom-help-release-adversarial-round2.txt`.
No adversarial program failed or changed scope, so the prior independent
adversary's artifact remains applicable without redispatch.

The intent's identity excluding its status/pin remains unchanged. Source,
tests, help text, ordinary output and release bytes are unchanged. Fresh
acceptance will record this corrected candidate; the same two branch-end
reviewers resume with the confirmation/plan-only fix delta for Round 2.
