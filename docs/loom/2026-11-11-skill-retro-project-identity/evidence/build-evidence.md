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

## Scope limits

These executions validate the ingestion and preview CLI, not host automatic skill routing or the downstream model-generated proposal. Project identity observes the current filesystem. Duplicate-session handling and threshold configuration overrides remain outside this repair.
