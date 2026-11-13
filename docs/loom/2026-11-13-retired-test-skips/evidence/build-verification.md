# Retired skip cleanup — Build verification

Candidate: `00c41f4bc774dc71dd66d0f96ae8db23db11ecf4`.
Base: `fbdc29af358413bc9d55b599231b2a6cbcb4524d` (main).
This independent branch does not include or modify help PR #150.
No workflow step was skipped and no production runtime file changed.

## Scope and protection

The six-row [disposition](../disposition.md) records each expired proof,
its continuing protection, the baseline skips and implementation observations.
The historical changelog assertion now runs inside the current-release guard;
remaining archived-copy comparisons and their archived originals are unchanged.
The duplicate-module guard and all seventeen active migration tests remain.
The existing migration fixture now checks two distinguishable lessons,
independently captured introducing commits, exact content and guide fidelity.
These are fixture regression proofs, not a claim to rerun the historical
293-file migration against a missing pre-migration trunk snapshot.

## Synchronization and setup

The installed `sync-trunk` fetched and reported up to date at
`b28b4e3422ea15dff2259c186fd55304b866661a`, against the same main base above.
Only the adversary's reused-test concern comment and evidence followed.
The runner's locked Mermaid dependencies were prepared before Python tests
with `npm ci --prefix loom-workflow/tests/mermaid`, avoiding initialization skips.
No install into conda base occurred. The 3.72.1 release packet was committed
as one unit; existing release guards passed (43 tests), mirrors check passed.

## Independent adversary

Independent adversary `retired_skips_adversary` tried eight attack points;
zero broke the changed safeguards and zero new programs were committed.
Six syntactically valid copied-production mutations, historical heading removal
and an injected module collision each failed at their intended assertion.
Invalid setup trials and a Git-history-dependent test in a Git-less archive
are retained as environment/setup observations, not counted as successful
attacks or valid mutation kills. Original-checkout verification passed.
See [adversarial-report.md](adversarial-report.md).

The qualified reused artifact is
`loom-workflow/tests/loom-memory/test_migrate_legacy_store.py`; only its
concern comment was added by the adversary. No findings remain and there was
no adversary redispatch.

## Complete package and declared program

Executed the configured inventory from the candidate checkout:

`uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`

Exit 0: **4268 pytest tests passed, zero skipped** across all fifteen isolated
pytest invocations, plus every shell and Mermaid group passed. The complete
output is `/private/tmp/loom-retired-skips-package-tests.txt`.
This total belongs to the main-based test-maintenance branch, not PR #150's
separate help branch; no passing-count comparison between those branches is
claimed.

After the complete suite, reran the declared reused artifact:

`uv run --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/loom-memory/test_migrate_legacy_store.py`

Exit 0: **17 passed in 1.05s, zero skipped**. Output:
`/private/tmp/loom-retired-skips-adversarial-rerun.txt`.
All six original skip conditions are absent from the live selected tests;
archived historical evidence was intentionally not rewritten or collected as
live tests. No live writer operation, merge, installed-plugin update or paid
outside review ran. Clean-copy acceptance and formal closing review follow.
