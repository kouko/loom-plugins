# Historical test-source archive

The twelve historical `test_run_package_tests.py` copies are retained as data in
[`historical-test-fixtures.tar.gz`](../../2026-11-07-engineering-research-trial/historical-test-fixtures.tar.gz).
They are frozen inputs and outputs from earlier dogfood runs, not tests collected
by the current package suite. Publishing expanded copies under
`docs/skill-dogfood/` violated the existing tests-folder guard.

[`historical-provenance.json`](historical-provenance.json) records the archive
SHA-256 and maps each original repository-relative member path to its SHA-256.
The twelve entries moved from `selected_files` into `archives[0].members`;
452 expanded files plus twelve archived members retain the original selection
of 464 files. Every member matches both the recorded historical selection and
the pre-existing-file snapshot. The original worktree's 3,688 historical files
remain unchanged.

The archive contains exactly twelve regular files, sorted by their original
repository-relative paths. Tar timestamps and owner IDs are zero, modes are
0644, owner/group names are empty, the gzip timestamp is zero, and its filename
is empty. Rebuilding from the same bytes produces the same archive.

Historical reports and their contents remain frozen. Links in those reports to
the twelve expanded paths **do not resolve in this delivery**; consult the
archive member map and inspect or extract the matching member in a separate
scratch directory. The archive preserves those bytes without rewriting the
reports or representing their historical results as current verification.
