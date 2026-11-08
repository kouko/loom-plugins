---
title: "Package runner test roots and local-test exclusion"
type: loom-research-export
status: concluded
created: 2026-11-08
updated: 2026-11-08
source_repo: loom-plugins (source snapshot only)
source_commit: d5a7f0da247214bdb9c61fe90c550256432e5f76
tags:
  - loom/research
  - loom/research-export
---

# Package runner test roots and local-test exclusion

> UNSAVED CANDIDATE. Not written to any Vault. Copy of a project research record; the project original stays authoritative.

## Provenance

- Original record: `docs/loom/research/2026-11-08-package-test-roots.md` (project-relative path, in the temporary fixture repo; pinned by fixture merge commit `4959e620a78e15678a3cc2a8a0c18f79de58dc73` on `main`).
- Source scope: minimal snapshot of `scripts/run_package_tests.py` and `tests/test_run_package_tests.py` at upstream commit `d5a7f0da247214bdb9c61fe90c550256432e5f76` (`origin/main` as locally recorded; remote freshness not checked).
- Merge status: the fixture research branch is merged into fixture `main`. That says nothing about any release or installation.

## Question and conditions

Which directories does the runner list in `TEST_ROOTS`, and does its package preset (`--loom-family`) include `tests/local/`?

## Findings (source-supported, not run)

- `TEST_ROOTS` = `tests`, `loom-code/tests`, `loom-design/tests`, `loom-workflow/tests`.
- The `--loom-family` preset excludes each root's `local/` subtree for Python (`--ignore=`) and shell discovery.
- The exclusion is preset-specific: the explicit-argument mode forwards groups directly to pytest with no added ignores.
- Implication: do not put tests meant for ordinary package coverage in `tests/local/`; a new plugin test root must be added to `TEST_ROOTS`.

## Limits

Static source inspection only. No tests or runner commands were executed. CI configuration and deployed or installed versions were not examined. Link to the full original: the project path above (no portable link is created).
