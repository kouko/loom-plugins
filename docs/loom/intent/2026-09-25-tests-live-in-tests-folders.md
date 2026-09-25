# Every test lives in a tests folder, apart from the code it tests
originator: kouko
kind: engineering
needs-design: no — relocates test files and updates the package-test inventory, CI workflows and the repository's test-placement convention; test/tooling artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-25
publication: automatic — authorized 2026-09-25 by kouko

## Problem
Tests in this repository sit in five kinds of place, mixed in with the code
they check, so a reader cannot tell at a glance which files run in
production and which only verify it:

| Where | Test files | Mixed with |
|---|---|---|
| loom-code `scripts/` | 104 | the 14 tools skills run, such as the checker |
| inside skill folders (loom-code `probes/`, loom-workflow `skills/*/scripts/`) | 61 | each skill's runtime files, installed with the skill |
| loom-design `scripts/`, loom-workflow `scripts/` and `.claude-plugin/` | 36 | tooling scripts and the plugin manifest |
| repository root `scripts/` and `.claude/hooks/` | 15 | repository tooling and hooks |
| existing `tests/` folders (loom-code, loom-workflow) | 22 | nothing — already separate |

Placement is also why some tests silently stopped running: the package
suite lists folders by hand, did not list loom-code's skill `probes/`
folders, and the recovery-rule probe RL-06 stayed red on main from PR #43
until PR #51 (2026-09-25).

## Proposed outcome
Every test of a plugin lives under that plugin's `tests/` folder, every
repository-level test lives under the root `tests/` folder, no test file is
left beside production code or inside a skill folder, and the package suite
runs all of them.

## Acceptance
1. Outside `docs/loom/`, every test file in the repository is under a plugin's `tests/` folder (that plugin's tests) or the root `tests/` folder (repository-level tests); none remains beside production code or inside a skill folder.
2. The package suite collects and passes the same tests it collected before the move, plus the skill probe tests it did not collect before, with none lost; the before and after counts per plugin are recorded.
3. A test added later anywhere under a `tests/` folder is run by the package suite without editing the suite command, and CI runs the same tests; the one exception is a `tests/local/` folder, which holds tests that need a locally installed CLI and is named as local-only.
4. The repository's contributor guidance states where tests go, and every document an agent reads at run time names the new locations.
5. The checker's rule list does not grow and no new step, reviewer or dispatch is added.

## Constraints
- The package suite stays the single inventory that Build, finalize-review and CI read.
- Probe programs committed as evidence for earlier changes under `docs/loom/` stay where they are, as the closing-review probe-graduation rule requires.
- No test's assertions change; only locations, and the paths and imports the move requires.

## Out of scope
- Changing what any test checks.
- Evidence probe programs under `docs/loom/`.
- Merged history records that name old test paths (earlier plans, reports, CHANGELOG entries).

## Open questions
- none
