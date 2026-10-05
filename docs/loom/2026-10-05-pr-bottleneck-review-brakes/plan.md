# Name lying tests in review and state merge risk in PR bodies — plan
intent: 2026-10-05-pr-bottleneck-review-brakes@c738df63
charter: 1.1

## Current State Evidence
- Forward: loom-code/skills/closing-review/references/lenses.md:54 `tests` row requires tests to "exercise the changed behavior rather than merely exit successfully"; names no lying-test patterns.
- Reverse: loom-code/skills/ship/SKILL.md:69-70 `## Risks and rollback` placeholder reads "remaining risks and a concrete recovery path"; nothing asks for door, blast radius.
- Error: loom-code/scripts/loom_checker/rule_checks/publish.py:103-146 blocks a missing or empty risks heading only; "semantic truth stays review-owned", so wording is the lever.
- Data: loom-code/skills/write-plan/references/one-way-door.md:1-9 defines five door classes; plan `## Risks` records user-decided door answers, which a PR risk line can cite.
- Boundary: loom-code/references/engineering-baseline.md:161-165 sanctions affirmative prose-pin tests; the source-text pattern must exclude them or it flags this repo's own suite.

## Task DAG

Wave 1 — two independent prose edits (different files, no shared symbol).

**W1-01 Name three lying-test patterns in the tests lens**  after: none  acceptance: 1, 2
- Files: loom-code/skills/closing-review/references/lenses.md
- Test: A1 positive: seeded-tautology-mirror-mock-each-flagged; negative: behaviour-test-through-entry-point-not-flagged. A2 positive: affirmative-prose-pin-test-not-flagged; boundary: source-text-test-of-code-structure-still-flagged.
- Risk: one clause in the existing `tests` row, no new row or rule id; agent-decided: prose-pin carve-out cites engineering-baseline rule 8; mutation adversary remains the stronger brake.

**W1-02 State door, blast radius and rollback in the PR risk section**  after: none  acceptance: 3
- Files: loom-code/skills/ship/SKILL.md
- Test: A3 positive: drafted-risk-section-states-door-radius-rollback; boundary: change-with-recorded-one-way-door-names-that-door-in-risk-section.
- Risk: placeholder wording only; no checker rule (cannot verify truth, publish.py already blocks empty); agent-decided: cite the plan's recorded door answers when present.

Wave 2 — release metadata.

**W2-01 Bump loom-code manifests and CHANGELOG to 3.33.0**  after: W1-01, W1-02  acceptance: 4
- Files: loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/plugin.json, loom-code/package.json, loom-code/CHANGELOG.md, loom-code/tests/test_write_plan_station_text.py
- Test: A4 positive: release-metadata-synchronized-at-3.33.0; boundary: sync-codex-manifests-all-check-exits-0.
- Risk: minor bump (station guidance change); package.json is derived by scripts/sync_codex_manifests.py, regenerate rather than hand-edit; CURRENT_VERSION constant moves with the manifests.

**W2-02 Bump README version strings to 3.33.0**  after: W2-01  acceptance: 4
- Files: loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, README.md
- Test: A4 positive: readme-version-matches-manifest; negative: root-readme-table-row-stale-3.32.0-absent.
- Risk: a grep for 3.32.0 outside docs/ lists exactly these four plus W2-01's files; historical CHANGELOG sections keep their old version strings.

## Simplicity check
- none found

## Questions asked
① — what — 上述四項（合併風險、會騙人的測試、收尾回顧、規範分流）要合成一個 loom 改動還是拆開做？（user: 上述四項一起做，然後再開 deep module 討論）
① — what — 剛剛的流程有做複雜度相關的判斷嗎？要不要派 agent 照規定重跑？（user: A，派 agent 重跑）
① — consequence — 範圍縮成兩項（審查點名三種會騙人的測試；PR 風險段落寫明能否撤回／影響範圍／回滾），回答「對」即授權自動發布，merge 另外決定；對嗎？（user: 對，照這兩項做，授權自動發布）

## Risks
1. Review-by-reading catches only obvious lying tests; repo memory records them as found by mutation. Accepted: the lens clause is a cheap first brake, not a replacement for the adversary.
2. A vague door/radius line still passes publish checks; truth stays review-owned by design. No one-way door in this change; every edit is prose and reverts cleanly.
