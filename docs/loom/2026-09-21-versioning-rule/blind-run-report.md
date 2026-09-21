# 2026-09-21-versioning-rule — what I tried and what happened

Tried on 2026-09-21, in a clean copy of the project at 4f7b41d9.

## What you asked for, one line at a time

### 1. Every merged PR touching loom-code must bump the version in all three manifests: `loom-code/plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`
- **How I tried it**: Checked the version field in each of the three manifest files at the target commit.
- **What happened**: All three files contained `"version": "3.7.3"`.
- **Evidence**: loom-code/plugin.json:8, loom-code/.claude-plugin/plugin.json:6, loom-code/.codex-plugin/plugin.json:6
- **Verdict**: works

### 2. The CHANGELOG.md must include a new entry `## [X.Y.Z] — <date> — <summary>` in the same commit as the version bump
- **How I tried it**: Listed the changelog headings and inspected the top entry.
- **What happened**: The changelog began with `## [3.7.3] — 2026-09-21 — the version that carries the versioning-rule change`.
- **Evidence**: loom-code/CHANGELOG.md:3-12
- **Verdict**: works

### 3. README version strings must be synchronized with the manifest versions
- **How I tried it**: Grepped for the version string in each README (English, Japanese, Traditional Chinese).
- **What happened**: Each README showed the version as 3.7.3 (or local equivalent).
- **Evidence**: loom-code/README.md:11, loom-code/README.ja.md:11, loom-code/README.zh-TW.md:9
- **Verdict**: works

### 4. The change is documented in AGENTS.md under a new "Versioning & Release" section
- **How I tried it**: Searched AGENTS.md for the heading and read the section.
- **What happened**: AGENTS.md contained a new section titled "Versioning & Release" with the rule, its rationale, and the synchronization requirements.
- **Evidence**: AGENTS.md:95-104
- **Verdict**: works

### 5. The rule is justified by the need for `claude plugin update` to detect changes via version string comparison
- **How I tried it**: Read the justification in the AGENTS.md section and the CHANGELOG entry.
- **What happened**: Both documents stated that `claude plugin update` only detects changes when the version string changes, so omitting a bump prevents merged fixes from reaching installed copies.
- **Evidence**: AGENTS.md:102, loom-code/CHANGELOG.md:9-10
- **Verdict**: works

### 6. Existing mechanized tests (e.g., `test_current_release_metadata_is_synchronized`) validate version consistency
- **How I tried it**: Ran the adversarial version metadata sync test suite and examined the pinned test.
- **What happened**: All 13 tests in the suite passed. The pinned test asserted that the three manifests and the changelog heading all read 3.7.3, and that no other file incorrectly retained the old version 3.7.2.
- **Evidence**: loom-code/scripts/test_adversarial_version_metadata_sync.py (13 passed); loom-code/scripts/test_write_plan_station_text.py:467-481
- **Verdict**: works

### 7. The change does not alter station contracts, rule IDs, or core functionality—it is a release process improvement
- **How I tried it**: Verified the contract manifest version and mechanism count statements in the changelog; confirmed only documentation files were changed.
- **What happened**: The contract manifest version remained 2.3.1. The changelog entry for 3.7.3 stated the mechanism count was unchanged. The diff showed modifications only to AGENTS.md, the three manifests, the changelog, the READMEs, a memory file, and the two test files (which only updated version assertions).
- **Evidence**: loom-code/contract/manifest.yaml:5, loom-code/CHANGELOG.md:4-5, git diff efcd4991..4f7b41d9 --name-only
- **Verdict**: works

### 8. Package tests continue to pass and mechanism count remains stable
- **How I tried it**: Ran the full loom-family package suite and measured the mechanism count.
- **What happened**: The package suite returned all passed, 3 skipped. Mechanism count measured as 22 counted skills, identical to base.
- **Evidence**: Package test suite summary: all groups passed; mechanism count measurement: "skill count (counted): 22"
- **Verdict**: works

## 对你既有的资料做了什么 (what this did to data you already had)

Nothing — it only touched files this change created or updated as part of the version bump process (manifests, changelog, READMEs, AGENTS.md, a memory file, and test assertions). No existing user data or repositories were altered.

## I decided for you

Nothing — every choice was either yours or forced by the acceptance criteria.

## Things I am not sure you want

Nothing.
