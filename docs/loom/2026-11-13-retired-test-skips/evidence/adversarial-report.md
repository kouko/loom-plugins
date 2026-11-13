# Independent adversarial report

Attack points tried: 8. Attacks that succeeded: 0. New programs committed: 0.
One existing repository test module is reused with a concern-only comment.

Target: b28b4e3422ea15dff2259c186fd55304b866661a, compared with
fbdc29af358413bc9d55b599231b2a6cbcb4524d. No production implementation,
historical archive, current memory corpus or other worktree was edited.
The code recipe applies; docs, intent and plan have no additional recipe.
No declared mutation/fuzz runner was found in the dependency/config inventory.

## Executed attacks

The unchanged committed test oracle ran against independently mutated production
in a Git archive at `/private/tmp/retired-adversary-valid-20261113`.
Every mutation was applied and restored with apply_patch. Each changed exactly
one production seam; the test assertions were never changed. These failures
demonstrate sensitivity to regressions, not defects in the unmutated change.

Let `P` be `uv run --with-requirements requirements-package-tests.lock python -m pytest`.
For the first six rows the command was `P loom-workflow/tests/loom-memory/test_migrate_legacy_store.py::test_migrate_transforms_a_legacy_store_into_a_valid_okf_profile -q -rs`.

| Attack | Copied production edit | Actual observation |
| --- | --- | --- |
| Description corruption | Replace legacy description with a different valid string | 1 failed at exact description equality |
| Existing type loss | Replace preserved type with DEFAULT_TYPE | 1 failed at exact type equality |
| Body corruption | Append corruption to staged lesson body | 1 failed at independent body bytes equality |
| Origin loss | Replace existing origin resource with another valid string | 1 failed at exact sources equality |
| Wrong introducing commit | Replace origin-less resource SHA with forty zeroes | 1 failed against fixture's captured introducing SHA |
| Guide corruption | Append corruption to complete charter output | 1 failed at complete normalized charter bytes equality |
| Historical heading loss | Rename only the 1.5.1 changelog heading | 1 failed at relocated historical heading assertion |
| New shadowed module | Add adversary_collision.py to interface and principles script directories | 1 failed at empty duplicate-basename assertion |

For the heading attack: `P loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized -q -rs`.
For the shadow attack: `P loom-design/tests/test_unified_pytest_root.py::test_duplicated_non_test_basenames_are_only_the_known_shadowed_pair -q -rs`.
Raw outputs: `/private/tmp/retired-adversary-valid-{description,type,body,origin,source,charter,heading,collision}.txt`.
The precise mutation seams are `_migrate_concept_frontmatter` description/type/resource assignments,
the staged lesson append, `readme_new_text`, the historical heading and the two named modules.

## Restored observations and limitations

- Before attacks, the migration module passed all 17 tests in an archive without repository history.
- After restoration, the same full module passed all 17 tests (0 skipped); it includes live copied-store validation and failure/no-write cases. It never touched the real store.
- Restored unified-root module: 3 passed, 0 skipped, including collection and exact station membership.
- Coldread plus complete write-plan station module in the archive: 58 passed, 1 failed. The unchanged precap-contract Git-history check cannot run without .git. Re-running those two modules in the original checkout yielded 59 passed, 0 skipped; those code tests do not regenerate the memory store.
- Initial sandbox uv cache lock access failed before collection; approved existing-cache access resolved it. An attempted direct transient uv interpreter had already expired (exit 127). The first six mutation attempts used incomplete indentation and failed collection (exit 4); those setup errors are excluded from mutation evidence and were repeated in a fresh archive with valid indentation, yielding assertion failures (exit 1). Earlier temporary copies and raw output were preserved.
- No complete package suite was run here; that remains the parent's responsibility. This is neither a historical 293-file replay nor an acceptance verdict.

No actual regression survived these attacks. Reuse the existing migration module,
which independently captures fixture metadata/body and introducing SHA, rather
than adding a new green harness. Its only change in this dispatch is its concern comment.

```yaml
attack_points: {found: 8, earned_a_program: 0, committed: 0}
adversarial:
  - command: "uv run --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/loom-memory/test_migrate_legacy_store.py"
    artifact: loom-workflow/tests/loom-memory/test_migrate_legacy_store.py
probes:
  - artifact: loom-workflow/tests/loom-memory/test_migrate_legacy_store.py
    status: reused
    reason: Existing independent temporary-store fidelity and failure tests killed the attempted production regressions.
findings: []
```
