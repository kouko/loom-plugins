# 2026-09-21-versioning-rule
originator: kouko
kind: engineering
needs-design: no — the change updates AGENTS.md with versioning policy, which is meta-information about skill development and release process
status: confirmed 2026-09-21
publication: automatic — authorized 2026-09-21 by kouko

## Problem
The loom plugin versioning follows a conservative rule: patch bumps only occur when there is no station guidance, field, rule id, or contract manifest change. This causes merged fixes to be invisible to `claude plugin update` if the version number is not bumped, as seen with PR #30 and #31 which required a dedicated version bump PR (#32) to reach installed copies.

## Proposed outcome
Change the versioning rule to require a version bump on every merged PR that touches a plugin. Every PR must increment the plugin version (patch by default; minor if the change includes station guidance, field, rule id, or contract manifest changes). This ensures `claude plugin update` reliably delivers all changes to installed copies.

## Acceptance
1. Every merged PR touching loom-code must bump the version in all three manifests: `loom-code/plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`
2. The CHANGELOG.md must include a new entry `## [X.Y.Z] — <date> — <summary>` in the same commit as the version bump
3. README version strings must be synchronized with the manifest versions
4. The change is documented in AGENTS.md under a new "Versioning & Release" section
5. The rule is justified by the need for `claude plugin update` to detect changes via version string comparison
6. Existing mechanized tests (e.g., `test_current_release_metadata_is_synchronized`) validate version consistency
7. The change does not alter station contracts, rule IDs, or core functionality—it is a release process improvement
8. Package tests continue to pass and mechanism count remains stable

## Constraints
- The change affects only the release process, release metadata, and their existing mechanized checks
- No modifications to station guidance, field definitions, rule IDs, or contract manifest (`loom-code/contract/manifest.yaml`)
- The version bump process follows semantic versioning: patch for documentation/process changes, minor for station/field/rule/contract changes
- The Loom workflow stations (capture-intent → write-plan → build → closing-review → ship) remain unchanged
- Reviewer floor, fresh-context reviewer independence, and writer-not-judge separation are preserved

## Out of scope
- Altering the semantic meaning of version numbers (major/minor/patch)
- Changing the station execution order or requirements
- Modifying how `claude plugin update` works internally
- Adjusting the CHANGELOG format beyond standard practice

## Open questions
- none