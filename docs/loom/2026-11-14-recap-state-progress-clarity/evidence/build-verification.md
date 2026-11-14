# Build verification

Functional commit: `be34122e8106f595d6b01a0dae033b2fa2162c9a`.
Branch base after synchronization: `3bf50711f983e12ac25b219c6340f5b164f5201c`.

## Test-first work

- Before the contract change, the focused entry tests reported 3 failed and 9 passed. The new failures named implementation/delivery separation, scoped test evidence and event-date grounding.
- After the source clarification, the recap suite reported 23 passed. These prose guards do not establish semantic output behavior; the independent acceptance evidence records actual native model outputs separately.
- The first complete package run failed on 9 release-version assertions because the existing current-release pin still named 5.23.0. The focused reproduction reported 9 failed and 5 passed.
- The first integration fix changed only that pin to 5.24.0 and extended the release task's file inventory. All assertions were preserved. Focused release checks then reported 16 passed. The historical 5.23.0 changelog entry remains unchanged.

## Trunk synchronization

The initial sync detected an adjacent README version-table conflict without changing the worktree. The merge preserved upstream loom-code 3.79.0 guidance and this change's loom-workflow 5.24.0 metadata. The final sync reported up to date at the functional commit above, containing origin/main at the stated base.

## Adversarial work

The independent adversary found 3 attack points, none exposing a product defect, and committed no new program. It reused `loom-workflow/tests/recap-state/test_skill_md.py`, adding only its concern comment in commit `29892d099`.

The reused program rejected empty guidance, a negated tested-scope instruction and a cross-sentence decoy. Its normal execution reported 12 passed; it was rerun after the integration fix with:

`uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/recap-state/test_skill_md.py`

No adversarial findings remain unresolved. No adversary redispatch was needed because the release-pin fix changed neither the program nor the covered skill obligations.

## Complete package suite

Command: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`

The complete rerun after the integration fix exited 0: 4,290 pytest cases passed, 5 skipped; all discovered shell checks passed. The 15 pytest group totals were 2857, 211, 53, 264, 64, 22, 13, 13, 58, 125, 250, 12, 23, 163 and 162. The package runner remains the inventory; these observed counts are not a separate test-selection list.

No workflow step was skipped by user instruction. Build did not generate an attestation. Closing Review must execute the suite and reused program again before generating one.
