---
title: "Package runner test roots and local-test exclusion"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

## Question and scope

Which directories does this runner list in `TEST_ROOTS`, and does its ordinary package suite include `tests/local/`? This informs placement of a new plugin's tests. Scope is the supplied minimal source snapshot, attributed by [provenance](../../provenance.json) to commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`; it is neither a complete checkout nor evidence of deployment.

## Method and rationale

Static source inspection of the runner's entry point and discovery helpers, with relevant test definitions as corroboration. This directly answers the single-source question; no tests or runner commands were executed.

## Findings and evidence

- `TEST_ROOTS` contains exactly `tests`, `loom-code/tests`, `loom-design/tests`, and `loom-workflow/tests` ([runner](../../src/scripts/run_package_tests.py), lines 51–55).
- The package preset is selected by `--loom-family` (lines 153–167). Its `code` group includes the first two roots and calls `_tests_session` (lines 122–128). That helper excludes the root's `local/` while checking for tests and adds `--ignore=<absolute local path>` when present (lines 76–86). Consequently, `tests/local/` is excluded from this preset's Python collection. Shell discovery likewise excludes each root's direct `local/` subtree (lines 89–96). Design and workflow Python paths also exclude their root-level `local/` directories (lines 99–114, 129–132).
- [Test definitions](../../src/tests/test_run_package_tests.py), lines 222–235, 285–310, assert the root list and exclusion of Python and shell files under `tests/local/`. These definitions were read, not run.
- The exclusion is preset-specific: the alternate explicit-argument mode forwards each group directly to pytest without adding these ignores (runner lines 168–175). This finding does not establish exclusion for bare pytest or explicitly targeted local tests.

The inspected runner and test file SHA256 values, measured with `shasum -a 256`, match their entries in provenance: `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54` and `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28`, respectively.

## Decision impact

Do not place tests intended for ordinary package coverage in `tests/local/`. A new standalone plugin test root is not automatically discovered: it must be added to `TEST_ROOTS`; otherwise use an existing listed root outside its excluded `local/` subtree, subject to the runner's normal discovery rules.

## Limitations and open questions

This is a source-supported conclusion, without runtime validation. CI configuration and deployed or installed versions are outside the supplied evidence; no claim is made about them. No material uncertainty remains for the inspected runner's root list and preset exclusion.

## Preservation provenance and verification — 2026-11-08

This human-readable copy was saved directly to the user-authorized temporary fixture Vault at `fixtureVault/research/2026-11-08-package-test-roots.md`. Obsidian CLI was unavailable; no app, plugin, installation, or host integration was used or verified. The research body above is preserved, with relative evidence links adapted for this destination. The project original remains unchanged.

- Original: [retained research](../../docs/loom/research/2026-11-08-package-test-roots.md), pinned in this fixture at `4959e620a78e15678a3cc2a8a0c18f79de58dc73:docs/loom/research/2026-11-08-package-test-roots.md`. Original SHA-256: `c54f28727453f125762110fe3516b4cb0eee9673f74ecddb1da6cc6d14631283`.
- Repository identity: this temporary local harness repository, rooted at the supplied working directory. The [source provenance](../../provenance.json) attributes the genuine minimal snapshot to original repository `/Users/kouko/.herdr/worktrees/loom-plugins/loom-research-skill-discut`, revision `d5a7f0da247214bdb9c61fe90c550256432e5f76`. That external path was not accessed. Provenance SHA-256: `8d9a1ad6d67c408c7a254d66b1b3543a4a7a32802936454009198a10d7621364`; remote freshness is explicitly not checked.
- Local merge evidence: `main` is at merge commit `4959e620a78e15678a3cc2a8a0c18f79de58dc73`, with parents `3236024bd97f03b25f97fb7fed95bc45d00bd423` and `00fa7642dd5ba69eb7b37fa19dfc0b15d4f3537a`. The latter is the retained `research-fixture` topic. The working research bytes match the merge's stored original; all four supplied source hashes match provenance. This proves the fixture merge, not a merge or release in the original repository.
- [Cleanup receipt](../../fixture-cleanup.json): records a successful empty post-merge status at the same main revision, destination `.` (the current fixture root), no linked worktree or generated temporary build artifacts, and a topic branch retained for audit. At this preservation check, tracked files have no diff from HEAD; `fixture-cleanup.json` and `skill/` are untracked. Therefore the receipt's historical clean state is not a claim that the current entire working tree is clean. This new Vault copy also becomes an untracked artifact. No cleanup was performed by this preservation operation.
- [Prior executor receipt](../../sample-receipt.json): reports exit code 0, no timeout, unchanged source and addition of the original research record. It records requested model/provider/effort, but `server_confirmed_model` is null. It does not establish server-confirmed model identity, installed-plugin behavior, full CI success, or deployment. Its embedded commands were not executed.

Static reinspection supports the original bounded findings: the four listed roots, root-level `local/` exclusion in the family preset, and the separate explicit-argument path without those added ignores. Test definitions were read only. No tests, sample commands, network calls, external models, installation, publication, or real Vault operations were performed. Runtime behavior, complete CI, real release/installation state and Obsidian host rendering remain unverified. Revalidate if the source revision or execution mode changes.
