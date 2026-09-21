# 2026-09-21-versioning-rule — plan
intent: 2026-09-21-versioning-rule@4f7b41d9
charter: 1.0

## Current State Evidence
- Forward: `loom-code/plugin.json:3` now reads `"version": "3.7.3"`; `loom-code/.claude-plugin/plugin.json:6` and `loom-code/.codex-plugin/plugin.json:6` updated in same commit
- Reverse: `docs/loom/memory/version-bump-on-every-pr.md:1` records the adopted rule; `AGENTS.md:95-104` documents the "Versioning & Release" section
- Error: prior to this change, `3.7.2` bump PR (#32) was required after #30/#31 merged; without bump, `claude plugin update` delivered nothing — the exact failure this change fixes
- Data: `loom-code/CHANGELOG.md:3` has `## [3.7.3] — 2026-09-21 — the version that carries the versioning-rule change`; all three READMEs (`README.md:11`, `README.ja.md:11`, `README.zh-TW.md:9`) display `3.7.3`

## Task DAG
### Wave 1 — metadata synchronization (already committed)
**W1-01 Synchronize plugin.json version across three manifests**  after: none  acceptance: 1
- Files: `loom-code/plugin.json:3`, `loom-code/.claude-plugin/plugin.json:6`, `loom-code/.codex-plugin/plugin.json:6`
- Test: A1 positive: all three manifests read `"version": "3.7.3"`; negative: any manifest still reads `"3.7.2"` triggers stale-file probe
- Risk: patch release 3.7.1 → 3.7.2 pattern repeated; agent-decided — reversible by another bump

**W1-02 Update CHANGELOG with `## [3.7.3]` entry**  after: none  acceptance: 2
- Files: `loom-code/CHANGELOG.md:3`
- Test: A2 positive: top of CHANGELOG contains `## [3.7.3] — 2026-09-21 — the version that carries the versioning-rule change`; negative: heading missing or reads older version
- Risk: changelog format drift; agent-decided — format stays consistent with prior entries

**W1-03 Sync README version strings**  after: none  acceptance: 3
- Files: `loom-code/README.md:11`, `loom-code/README.ja.md:11`, `loom-code/README.zh-TW.md:9`
- Test: A3 positive: each README displays `3.7.3` in its version line; negative: any README still reads `3.7.2`
- Risk: localized README omission; agent-decided — all three language versions updated in same commit

**W1-04 Document rule in AGENTS.md**  after: none  acceptance: 4, 5
- Files: `AGENTS.md:95-104`
- Test: A4 positive: section titled "Versioning & Release" exists with rule, rationale, and synchronization requirements; negative: section missing or outdated. A5 positive: section states the `claude plugin update` version-string justification; negative: justification absent
- Risk: section drift; agent-decided — governed by contract manifest version 2.3.1, no semantic change

**W1-05 Add memory entry**  after: none  acceptance: 6
- Files: `docs/loom/memory/index.md`
- Test: A6 positive: `version-bump-on-every-pr.md` entry present with adopted rule summary; negative: entry missing or outdated
- Risk: index drift; agent-decided — one-line addition, soft cap 24.4 KB

### Wave 2 — test alignment (already committed)
**W2-01 Align adversarial and unit tests to 3.7.3**  after: none  acceptance: 7, 8
- Files: `loom-code/scripts/test_adversarial_version_metadata_sync.py`, `loom-code/scripts/test_write_plan_station_text.py`
- Test: A7 positive: contract manifest version stays 2.3.1 and mechanism count unchanged; negative: manifest or count changed. A8 positive: full package suite passes; negative: any group fails
- Risk: test drift after future bumps; agent-decided — update literals only, no new test machinery

## Questions asked
① — what — which follow-up items this change includes; kouko: "好" (all metadata synchronization tasks)
② — behaviour — visible behaviour confirmed: `claude plugin update` now picks up merged PR changes; kouko: "對"
③ — consequences — if bump omitted, merged fixes invisible to installed copies; kouko: "對"

## Risks
1. user-decided — kouko's confirmation at ① (2026-09-21) adopts the version-bump-on-every-pr rule exactly as intended
2. Main may advance before shipping; a local guard blocks agents from merging main, so kouko runs any needed merge himself
3. No behaviour changes; the adversarial probe file from the previous change must still pass unchanged