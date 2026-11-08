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

## Provenance of this copy

- Human-readable copy of [docs/loom/research/2026-11-08-package-test-roots.md](../../docs/loom/research/2026-11-08-package-test-roots.md) (SHA256 `c54f28727453f125762110fe3516b4cb0eee9673f74ecddb1da6cc6d14631283`), as merged in local fixture commit `4959e62` (research slice `00fa764`). Only the relative links were rewritten to resolve from this location; the body is otherwise unchanged. The original was not edited.
- Source revision: upstream `d5a7f0da247214bdb9c61fe90c550256432e5f76` per [provenance](../../provenance.json); remote freshness was not checked. The local git history is a temporary fixture, not the real project.
- Re-check on 2026-11-08: the runner and test-file SHA256 values still match provenance. Some line anchors in the findings are off by one against the snapshot (for example `TEST_ROOTS` is at line 53 within the block at 51–54; the `code` group is at 124–128; shell discovery at 88–95; explicit-argument mode at 168–176). The conclusions are unaffected.
- No tests, runner commands, CI or deployed versions were run or inspected. Merge into the fixture is not release or installation.
