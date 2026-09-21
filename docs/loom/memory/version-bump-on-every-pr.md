---
name: version-bump-on-every-pr
description: Adopted rule — every merged PR that touches a plugin must bump that plugin's version (patch by default; minor when station guidance, field, rule id, or contract manifest changes) so `claude plugin update` delivers merged changes to installed copies
type: project
sources:
  - resource: user request 2026-09-21 — discussed during 2026-09-20-mechanical-calculations merge
---

**Rule (adopted 2026-09-21, committed in AGENTS.md "Versioning & Release")**: Every merged PR that touches a plugin must increment that plugin's version (patch by default; minor when the change includes station guidance, field, rule id, or contract manifest changes).

**Why:**
- `claude plugin update` compares version string only; without bump, merged fixes never reach installed copies (3.7.2 bump PR #32 fixed this for #30 + #31 after they merged)
- Bump-on-every-PR eliminates "forgot to bump" class of release failures
- Keeps CHANGELOG as continuous record of every released change

**How to apply (this change):**
- Bump `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, and `loom-code/.codex-plugin/plugin.json` to the same new version.
- Add a matching `CHANGELOG.md` entry in the same commit.
- Update READMEs in all supported languages to the same version.
- Update the existing version assertions and adversarial boundary tests without adding new test machinery.

**Related:** [[version-bump-packets-must-name-changelog-entry]] — existing gotcha about requiring CHANGELOG entry in bump commits