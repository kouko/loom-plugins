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

## Round 3 after task-specific Risk correction

Both resumed Round-2 reviewers identified the same important class: two plan
Risk lines copied unrelated task guidance. The bounded fix
`4e6e2d4dac8e904c527e15e425c8ea337a4769b7` changes only those two lines and
appends their disposition to the existing provenance evidence. User
requirements, source, tests, help and release metadata are unchanged.
The public plan and write-plan intake checks passed; focused existing plan
field tests passed (9 tests). No finding was dismissed.

`sync-trunk` again reported up to date against the same origin/main. The
complete package command reran at this fixed commit: **exit 0, 4269 passed,
6 skipped**, all shell/Mermaid groups passed. Raw output:
`/private/tmp/loom-help-release-package-tests-round3.txt`.
The declared reused adversarial artifact reran afterwards: **exit 0,
39 passed in 9.57s**; output
`/private/tmp/loom-help-release-adversarial-round3.txt`.
The program and covered production behavior did not change, so no new
adversary dispatch or program was justified. Fresh clean-copy acceptance and
the same two reviewers' terminal Round 3 follow on this corrected content.

## Main integration after user-directed continuation, 2026-11-14

The agent disclosed that the original episode had completed Round 3 and that
the installed rule said "never dispatch Round 4". The user then said
“遠端有新版本” and “請繼續”. The parent agent's recorded interpretation is
that this informed continuation authorizes finishing the existing integration
and verification work. Preserve Rounds 1–3 and their failures; this is not a
requirements change, a counter reset or a skipped reviewer/test/acceptance step.

Before integration, published help HEAD was
`4854ad23c62956666abd2a9ebd445580bdf5626a`; main had advanced to
`7c137958db0f78af4d50b99e43d96e17225c8cce` (loom-code 3.74.0 and
loom-workflow 5.22.0). The adapted existing plan was independently checked
for a smaller shape, passed plan and intake checks, and was committed as
`2fc46d9b1`. The confirmed help-only Acceptance lines remain unchanged.

Defect class: release metadata divergence after main advancement. The bounded
search read every cumulative changed file and the release-guard surfaces.
Actual conflicts affected ten paths: root README; the four loom-code manifests;
loom-code CHANGELOG; the three localized loom-code READMEs; and the current
release pin in `test_write_plan_station_text.py`. No production help entry or
handler conflict occurred. Integration uses a merge, preserving published
history rather than rebasing it.

The release is now loom-code 3.75.0. Its help entry retains the unmerged help
release notes under the new version/date, while main's distinct 3.74.0, 3.73.0
and 3.72.1 changelog sections remain intact. The Claude manifest is the SSOT;
`python3 scripts/sync_codex_manifests.py --all` regenerated its three mirrors.
The Codex target's conflict was first restored to main's valid metadata so
the existing synchronizer could read it; version propagation then came from
the SSOT. Workflow remains 5.22.0 and design remains 2.25.0.

Main's historical `## [1.5.1]` release guard is retained. Main-side CI
preparation, explicit external-review continuation and incremental-test
protection files were compared against main and remain byte-identical.
The help dispatcher and its CLI/runtime test files were compared against
the previously published help HEAD and remain byte-identical. AST inspection
confirms both main and help expose the same sixteen command names; the
integrated tree has all sixteen help entries. No new permanent test or test
case was added for this metadata-only integration. The earlier help test
additions and their failing/passing evidence remain available for review.

Focused RED reused the existing release consistency guard while its pin still
read main's 3.74.0: one failed, reporting actual 3.75.0 versus expected 3.74.0.
Raw output: `/private/tmp/loom-help-main-release-red.txt`. After synchronizing
the pin, the resolved focused command was:

`uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_loom_python_runtime.py loom-code/tests/test_write_plan_station_text.py -q -rs`

It exited zero with **92 passed, zero skipped**; raw output:
`/private/tmp/loom-help-main-focused-green.txt`. The generated-manifest check
also exited zero (`/private/tmp/loom-help-main-manifest-check.txt`). The existing
offline adversarial declaration above remains unchanged. Complete integration,
its adversarial rerun, clean-copy acceptance and content-matched closing review
remain the parent's next verification boundaries; these focused results do not
claim them complete or establish CI at a new remote HEAD.

## Complete integration observed at 0efb5f2e6

The configured complete package command exited zero with 4,276 pytest cases passed across 15 sessions, zero skipped, and all shell and Mermaid groups passing. Raw output: `/private/tmp/loom-help-main-package-tests.txt`.

The retained declaration `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py` exited zero with 39 passed in 8.77s; raw output: `/private/tmp/loom-help-main-adversarial.txt`. It remains applicable to unchanged help behavior, so no new adversarial program or adversary redispatch was required for this integration.

Build and pre-acceptance sync both reported up to date against origin/main 7c137958db0f78af4d50b99e43d96e17225c8cce. Original closing-review agents are no longer available to resume; current integrated content will receive fresh independent code and docs review without relabeling or resetting the original three rounds. The plan retains the user's post-disclosure continuation and its interpretation. No new outside-model execution was authorized. Acceptance and exact-head remote CI remain pending at this observation.
