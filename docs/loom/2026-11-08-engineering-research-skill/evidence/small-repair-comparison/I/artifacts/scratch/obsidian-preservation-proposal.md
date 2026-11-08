# UNSAVED CANDIDATE: Obsidian preservation proposal (not written anywhere)

Status: awaiting user decision. Nothing has been written to fixtureVault. No Obsidian CLI is available, so no Vault was discovered.

## Source
- Project original (stays in place): `docs/loom/research/2026-11-08-package-test-roots.md`
- Merge evidence: `docs/loom/research/2026-11-08-merge-release-status.md`
- Fixture repo: temporary local git, `main` = `4959e620a78e15678a3cc2a8a0c18f79de58dc73` (merge of `research-fixture` `00fa764`)
- Underlying upstream snapshot: commit `d5a7f0da247214bdb9c61fe90c550256432e5f76` (remote freshness not checked)

## Destination (unresolved)
Proposed: `<fixtureVault>/<folder you choose>/2026-11-08-package-test-roots.md`. Please give the exact Vault path. If a file already exists there, overwriting needs separate authorization.

## Content scope
Included: the package-test-roots finding only (a source-supported, version-pinned finding with lasting cross-repository value). Excluded: release-dependent claims (no release evidence), the merge-status record, fixture JSON files, and any batch, sync or reorganization.

## Draft note

```markdown
---
title: "Package runner test roots and local-test exclusion"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
  - engineering-research
---

# Package runner test roots and local-test exclusion

Provenance: temporary fixture `main` 4959e620a78e15678a3cc2a8a0c18f79de58dc73; sources are a minimal snapshot of upstream commit d5a7f0da247214bdb9c61fe90c550256432e5f76 (remote freshness not checked). Not deployment evidence; no release evidence exists. Project original: docs/loom/research/2026-11-08-package-test-roots.md in the fixture repo (relative links not copied; they would break in the Vault).

## Question
Which directories does the runner list in TEST_ROOTS, and does the ordinary package suite include tests/local/?

## Findings
- TEST_ROOTS = tests, loom-code/tests, loom-design/tests, loom-workflow/tests (scripts/run_package_tests.py lines 51-55).
- The --loom-family preset excludes each root's local/ directory for Python (--ignore) and shell discovery. Explicit-argument mode does not add these ignores.
- Test definitions assert this; they were read, not run.

## Decision impact
Do not put tests meant for ordinary package coverage in tests/local/. A new plugin test root must be added to TEST_ROOTS.

## Limits
Source inspection only, with no runtime validation. CI and installed versions are not covered.
```

## Decision requested
Reply with (1) the destination path, (2) approval of this content scope, and (3) whether to overwrite if the note exists. Silence or refusal leaves this unsaved.
