---
name: version-bump-through-claude-ssot-and-sync-script
description: Version bumps go through the Claude SSOT (`loom-code/.claude-plugin/plugin.json`) then `scripts/sync_codex_manifests.py --all`; hand-editing the derived manifests fails the version-sync tests
type: gotcha
sources:
  - resource: change 2026-10-23-memory-and-agents-md-fix — SSOT correction in AGENTS.md
  - resource: docs/loom/memory/version-bump-on-every-pr.md — version bump-on-every-pr rule
---

**Rule (gotcha):** `loom-code/.claude-plugin/plugin.json` is the single source of truth (SSOT) for the plugin version; `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, and `loom-code/package.json` are all derived by `python3 scripts/sync_codex_manifests.py --all`. Hand-editing any derived manifest fails the version-sync tests, and the bump is never delivered to installed copies because `claude plugin update` compares version strings only.

**Why:** The derived files read like authoritative manifests, so implementers hand-edit them directly and the diff looks right. Nothing fails at the task level — `test_write_plan_station_text.py::test_current_release_metadata_is_synchronized` catches the mismatch only at whole-branch review, and earlier arcs shipped stale derivatives to main that way.

**How to apply:** Bump only `loom-code/.claude-plugin/plugin.json` in the commit, then run `python3 scripts/sync_codex_manifests.py --all` and regenerate every derived file in the same commit. Never hand-edit `.codex-plugin/plugin.json`, `plugin.json`, or `package.json`.

**Related:** [[version-bump-on-every-pr]], [[version-bump-packets-must-name-changelog-entry]]
