# Project identity implementation evidence

## W1: retain and resolve invocation provenance

- Commit: 7133f89c76ec97fcfa961cb1a12d6621c2ac318c.
- RED: the two adapter cases failed for the missing Event field; after adding nullable fields, three behavioral cases still failed because known repositories returned unknown identities.
- GREEN: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/skill-retro/test_ingest.py -q` — 24 passed.
- Cases used temporary Git repositories, subdirectories and a linked worktree. They cover both adapters, context replacement, missing context and failed/unavailable/timed-out Git inspection.
- Added 85 net test lines. Session identifiers and invocation detection remain unchanged.

## W2: known-only aggregation and CLI output

- Commit: c4ce8fd66004199f9d6383f682027a4b066f5f92.
- RED: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/skill-retro/test_aggregate.py loom-workflow/tests/skill-retro/test_main_e2e.py -q -k 'partial_map_unknown or cli_project_attribution'` — 6 failed, 21 deselected.
- The binding top-one case selected A instead of B; shared and mixed project cases inflated counts; empty mapping manufactured session projects.
- GREEN: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/skill-retro -q` — 154 passed.
- The provenance test initially referenced a nonexistent payload key and was corrected to the existing `session_events` key; no product behavior was relaxed.
- Added 74 net test lines. Real CLI cases exercise separate repositories, shared worktrees, unknown and mixed attribution, source locations and a binding top-N cut.

## W3 and integrated Build verification

- Release commit: 2498b645. Updating the existing version pin first produced 10 failures and 4 passes; synchronized 5.21.0 release metadata then produced 14 passes, with no added test lines.
- `sync-trunk` before adversarial testing and before closing review reported up to date with origin/main at a8ec84e02740b58820055249e40e186d63233fbd; no merge commit or warning.
- Adversary: 7 attack points, none successful, no product findings. Temporary trials plus focused cases produced 54 passes. Only a concern comment on the existing ingestion test was retained, in fa61939d1a414dd807758f80dc28cad50f372134.
- Attacks covered path aliases and hostile spelling, malformed context replacement, bad explicit mappings, inherited Git routing, linked worktree context, dependency failure and binding CLI selection.
- Full suite at fa61939d: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` — exit 0; pytest groups totaled 4191 passed and 6 skipped; shell-test groups also passed.
- Adversarial replay after the full suite: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/skill-retro/test_ingest.py` — 24 passed, exit 0.
- The package runner's temporary npm install emitted an audit advisory (2 low, 1 critical); no dependency change or audit remediation was performed by this repair. The declared suite completed successfully.

## Round 1 finding and Round 2 repair

Reviewer A returned PASS. Reviewer B returned NEEDS_REVISION for one fatal correctness finding at ingest.py:452: hashing an untrusted array/object record type could raise TypeError and abort preview. No finding was dismissed.

The class search covered complete changed files and ingestion acceptance surfaces. Five ingestion membership sites shared the mechanism: metadata record type, content item type, message role, function-call type and output type. The repair at 22ff4ee5d6eda5a53969aed1613721dd15ad64d1 uses non-hashing tuple membership at each site. Plan task W4 retains the same requirements and review episode.

- RED: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/skill-retro/test_ingest_malformed_types.py -q` — 8 failed with TypeError.
- GREEN: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/skill-retro -q` — 162 passed.
- One parameterized test adds 36 lines, preserving valid later invocations and unknown-context replacement. The existing adversarial artifact remains unchanged.
- End-of-Build replay at 22ff4ee5: the declared full package suite exited 0, totaling 4199 pytest passes and 6 skips plus successful shell groups; the unchanged adversarial ingestion command then passed all 24 tests. No adversary re-dispatch was needed because its existing program remained runnable and passed.

## Scope limits

These executions validate the ingestion and preview CLI, not host automatic skill routing or the downstream model-generated proposal. Project identity observes the current filesystem. Duplicate-session handling and threshold configuration overrides remain outside this repair.
