# Six historical skips — disposition and coverage ownership

This is the pre-implementation disposition at base `fbdc29af358413bc9d55b599231b2a6cbcb4524d`, confirmed-intent HEAD `b2ecdfa81756606b098ae92c6c8adf2b0621a3e6`. It records source observations, not completed test results.

| Historical skipped test | Smallest disposition | Continuing coverage and limit |
| --- | --- | --- |
| `loom-code/tests/test_probes_coldread_changelog_carries_1_5_1.py::test_plugin_manifests_version_1_5_1_and_changelog_carries_it` | Retire the live historical probe file and move its unconditional `[1.5.1]` heading assertion into the existing current-release guard. Preserve the archived original. | `loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized` guards current manifests/changelog/readme and retains the historical heading proof; adjacent tests guard all three plugin readmes and root table/section. The remaining graduated-copy identity guard needs no exclusion or weakening. |
| `loom-code/tests/test_probes_coldread_abuse_coldread_branch_end.py::test_memory_step_store_integrity_check_exits_zero` | Delete only this retired-command function and imports made unused by its removal. | `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py::test_legacy_validator_and_its_tests_are_retired` protects intentional retirement; `test_migrated_store_validates_clean_and_regenerates_idempotently` exercises the current validator. Never restore the retired script. Other coldread evidence tests remain. |
| `loom-design/tests/test_unified_pytest_root.py::test_shadowed_basename_resolves_from_the_expected_station` | Delete the winner test and its now-unused pytest import. | Preserve unified collection, complete station pythonpath membership, and the existing duplicate-basename check with its empty allowed set. With no conflicting pair, there is no valid winner to pin. |
| `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py::test_lesson_and_guide_concept_counts_are_293_and_1` | Retire this completed one-time real-store proof; strengthen the existing synthetic public-entry migration test to compare exact input/output lesson inventory and a separate single guide. | Use a small temporary Git repository and at least two distinguishable lessons, rather than a fixed 293-file snapshot. Preserve live-store validation. This does not re-prove the historical corpus count. |
| `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py::test_lesson_bodies_and_descriptions_survive_migration_byte_for_byte` | Retire historical branch-baseline comparison; strengthen the same existing public-entry test with pre-migration input expectations. | Compare every fixture lesson's exact body, description, name, existing type and origin-to-source preservation; cover an origin-less lesson with its actual introducing SHA. Retain default-type, extra-key, tricky-description, body and failure/no-write tests. Include an extra dated metadata value to demonstrate passthrough without inventing a date contract. |
| `loom-workflow/tests/loom-memory/test_migrate_legacy_store.py::test_guide_concept_metadata_and_charter_prose` | Retire historical README-baseline comparison; strengthen the same existing public-entry test's guide assertions. | Assert guide type/name, meaningful description, exact introducing-commit source and complete fixture charter bytes after the documented separator normalization; assert index removal and regenerated validity. This preserves migration fidelity without freezing current repository charter prose. |

Remove `_pre_migration_ref`, `_require_pre_migration_ref`, `_git_show`, and `_pre_migration_lesson_paths` only when their three deleted consumers leave them unused. Update the migration module's opening description and obsolete section comments accordingly. Keep `STORE`, live-store validation and all 17 remaining active migration/validator tests; extend existing coverage rather than creating a new test framework. Fixture inputs must be captured before calling `migrate()` and must not use its transformation helpers to compute the expected output.

The temporary Git fixture must not query the enclosing worktree's trunk or history. No production migration code, runtime contracts, CLI behavior, current memory corpus or external worktree is changed. A check that merely scans for absent skip text would not establish coverage and is not planned.

Implementation source readback found that the existing graduated-copy guard compares the old changelog probe byte-for-byte with its archived source. Agent-decided: move the still-valid heading assertion to its current-release owner and retire the live historical copy, rather than add a named exception to that guard. Keep the archive and the remaining comparison logic unchanged; only update its population wording where needed. This preserves proof ownership without introducing an allowlist. W1-01 includes the current-release test file for this assertion; W2-02 later changes only its release pin.

## Verification evidence ownership

The focused observations below retain the original skips and actual `pytest -rs` outcomes, with plugin configurations run separately. Subsequent complete package-suite, independent adversarial and acceptance observations belong in `evidence/build-verification.md`, not appended to this functional disposition after verification. Those records must identify every remaining skip, distinguish passed, failed and skipped outcomes, and retain failed attempts. The complete package runner remains the final inventory; focused results alone cannot establish Acceptance 4.

## W1-01 implementation and focused verification

Implemented the six dispositions. The historical changelog module is removed;
its unconditional `## [1.5.1]` assertion now lives in the existing current-release
metadata test. The graduated-copy guard continues to compare all remaining
matching pairs without an exception or archive modification. The migration
module retains all 17 formerly active cases, including current-store validation
and every failure/no-write guard. Its existing public-entry fixture now has two
distinct lessons and a separate guide, independent expected metadata/body bytes,
a captured introducing Git SHA followed by a later unrelated commit, dated extra
metadata, exact output inventory/counts, complete normalized charter bytes, and
idempotent valid index regeneration. Only orphaned historical helpers were removed.

No production/tool code, current real memory-store files, historical evidence,
other worktrees, or package dependencies changed. Across the five test files,
the W1 diff is 67 inserted and 356 removed lines (net 289 removed). The retired
functions are the six historical cases; the old heading check's responsibility
moves into an already collected test rather than adding a new test case.

Baseline commands used `uv run --with-requirements requirements-package-tests.lock
python -m pytest <paths> -q -rs`, separately for each plugin configuration:

| Stage | Paths / cases | Actual outcome | Raw output |
| --- | --- | --- | --- |
| Baseline code | Historical changelog + coldread branch-end modules | 16 passed, 2 skipped | `/private/tmp/loom-retired-skips-baseline-code.txt` |
| Baseline design | Unified pytest root module | 3 passed, 1 skipped | `/private/tmp/loom-retired-skips-baseline-design.txt` |
| Baseline workflow | Migration module | 17 passed, 3 skipped | `/private/tmp/loom-retired-skips-baseline-workflow.txt` |
| W1 code | Coldread branch-end module + `test_current_release_metadata_is_synchronized` | 17 passed, 0 skipped | `/private/tmp/loom-retired-skips-green-code.txt` |
| W1 design | Unified pytest root module | 3 passed, 0 skipped | `/private/tmp/loom-retired-skips-green-design.txt` |
| W1 workflow | Migration module | 17 passed, 0 skipped | `/private/tmp/loom-retired-skips-green-workflow.txt` |

The initial sandboxed uv attempt could not create its cache lock under
`/Users/kouko/.cache/uv` (operation not permitted), before test collection. The
same isolated dependency command succeeded with approved cache access; no package
was installed into a base environment. This is an environment attempt, not a test
failure or pass.

### Strengthened assertion sensitivity

Because production migration behavior is already correct, no artificial
production fix or fabricated pre-implementation failing test is claimed. The six
baseline skips above are the original observed gap. To verify the strengthened
test actually detects fidelity regressions, a temporary `git archive HEAD` copy
at `/private/tmp/loom-retired-skips-mutation` received the updated migration test.
Each isolated mutation changed the copied **production migration** seam, never
the test oracle. Each was restored with `apply_patch` before the next mutation:

| Copied production mutation | Actual outcome | Raw output |
| --- | --- | --- |
| Replace a lesson description with another valid description | 1 failed: exact description assertion | `/private/tmp/loom-retired-skips-mutation-description-red.txt` |
| Append text to a migrated lesson body | 1 failed: exact body bytes assertion | `/private/tmp/loom-retired-skips-mutation-body-red.txt` |
| Append text to the guide charter | 1 failed: complete charter bytes assertion | `/private/tmp/loom-retired-skips-mutation-charter-red.txt` |
| Replace origin-less provenance with a syntactically valid wrong SHA | 1 failed: independently captured introducing SHA assertion | `/private/tmp/loom-retired-skips-mutation-source-red.txt` |
| Restore all copied production mutations | 1 passed | `/private/tmp/loom-retired-skips-mutation-restored-green.txt` |

These are implementer sensitivity checks, not the mandatory independent Build
adversarial pass or independent acceptance testing. Full-suite acceptance remains
pending end-of-Build verification in `evidence/build-verification.md`; these
focused runs do not establish Acceptance 4 by themselves. Historical 293-file migration execution is not
reclaimed as a current passing result.


## W2 release packet

The coherent maintenance release is loom-code 3.72.1, dated 2026-11-13. The
Claude manifest is the source; `scripts/sync_codex_manifests.py --all` derives
its Codex, Antigravity and OpenCode mirrors. Only version strings change in
the four README files, and only `CURRENT_VERSION` changes further in the release
test; its historical 1.5.1 assertion remains. Loom-design and loom-workflow
versions remain unchanged. The separate help PR/worktree is untouched.

The new release pin was run before updating metadata and failed against 3.72.0,
as expected (`/private/tmp/loom-retired-skips-release-red.txt`). Actual complete
release-guard and manifest-sync results are retained by the parent in
`evidence/build-verification.md` with the later Build verification observations.

## W3 CI environment preparation

The confirmed extension adds AC5/6: prepare each CI test job before testing and
expose setup failures. The code, design and workflow Python jobs now install the
same hash-verified package lock used locally. The code job explicitly installs
zsh and uv, verifies Python 3.11, and installs the pinned official agy payload
after SHA512 verification. It checks the executable version and all three local
plugin validators before exporting the executable for the test step. The workflow
Python job prepares Node and Mermaid dependencies in its own workspace; the
separate Mermaid job cannot supply those dependencies across job boundaries.
Both event filters in all three consuming workflows include the requirements
source and lock. Existing job names and suite inventory remain unchanged.

The installation steps retain native Actions failure ordering: no setup or suite
step ignores errors or overrides the default success condition. A regression
test executes the actual agy installation shell with a corrupt download and
checks that checksum failure prevents extraction and PATH publication. It does
not emulate the Actions scheduler or replace a live agy validation result.

The prior AC1–4 observations remain historical evidence at their recorded
commits. New local focused observations and honest pending Linux execution are
recorded in `evidence/ci-environment-verification.md`; independent Build, full
package execution, acceptance and closing review must cover the cumulative tree.
The existing 3.72.1 release packet includes this CI maintenance extension; no
runtime tool behavior, platform matrix or other worktree changed.
