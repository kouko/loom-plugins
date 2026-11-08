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

Which directories does this runner list in `TEST_ROOTS`, and does its ordinary package suite include `tests/local/`? This informs placement of a new plugin's tests. Scope is the supplied minimal source snapshot, attributed by [provenance](../../provenance.json) to commit `d5a7f0da247214bdb9c61fe90c550256432e5f76` (remote freshness not checked); it is neither a complete checkout nor evidence of deployment.

## Method and rationale

Static source inspection of the runner's entry point and discovery helpers, with relevant test definitions as corroboration. This directly answers the single-source question; no tests or runner commands were executed.

## Findings and evidence

- `TEST_ROOTS` contains exactly `tests`, `loom-code/tests`, `loom-design/tests`, and `loom-workflow/tests` ([runner](../../src/scripts/run_package_tests.py), lines 51–55).
- The package preset is selected by `--loom-family` (lines 153–167). Its `code` group includes the first two roots and calls `_tests_session` (lines 122–128). That helper excludes the root's `local/` while checking for tests and adds `--ignore=<absolute local path>` when present (lines 76–86). Consequently, `tests/local/` is excluded from this preset's Python collection. Shell discovery likewise excludes each root's direct `local/` subtree (lines 89–96). Design and workflow Python paths also exclude their root-level `local/` directories (lines 99–114, 129–132).
- [Test definitions](../../src/tests/test_run_package_tests.py), lines 222–235, 285–310, assert the root list and exclusion of Python and shell files under `tests/local/`. These definitions were read, not run.
- The exclusion is preset-specific: the alternate explicit-argument mode forwards each group directly to pytest without adding these ignores (runner lines 168–175). This finding does not establish exclusion for bare pytest or explicitly targeted local tests.

## Decision impact

Do not place tests intended for ordinary package coverage in `tests/local/`. A new standalone plugin test root is not automatically discovered: it must be added to `TEST_ROOTS`; otherwise use an existing listed root outside its excluded `local/` subtree, subject to the runner's normal discovery rules.

## Limitations and open questions

This is a source-supported conclusion, without runtime validation. CI configuration and deployed or installed versions are outside the supplied evidence; no claim is made about them. No material uncertainty remains for the inspected runner's root list and preset exclusion.

## Copy provenance

- Human-readable copy of the fixture research record [docs/loom/research/2026-11-08-package-test-roots.md](../../docs/loom/research/2026-11-08-package-test-roots.md); the original was not modified. Relative links above were adjusted to resolve from `fixtureVault/research/` to this temporary fixture's sources. Body text is otherwise unchanged.
- Fixture git (harness observation, `fixture-observations.json`; not run by the writer): `main` = `4959e620a78e15678a3cc2a8a0c18f79de58dc73`, `research-fixture` = `00fa7642dd5ba69eb7b37fa19dfc0b15d4f3537a`, which is an ancestor of `main`. No tags or remotes. This is a temporary harness repository, not the original project, a release, or an installation.
- Source SHA256 (harness observation, matching `provenance.json` entries): runner `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54`; tests `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28`. Original research record SHA256 at observation time: `c54f28727453f125762110fe3516b4cb0eee9673f74ecddb1da6cc6d14631283`.
- This temporary fixture Vault copy is not a real user Vault. The merge shown is local to the fixture and is not publication or installation.
