# Code-first backfill guidance — plan
intent: 2026-10-04-code-first-backfill-guidance@d76e4d26
charter: 1.1

## Current State Evidence
- Forward: `loom-code/references/engineering-baseline.md` §2 "Legacy backfill is not a violation" covers inherited code at task level only.
- Reverse: `loom-code/agents/implementer.md` reads engineering-baseline.md; `loom-code/tests/test_prose_pin_rule_text.py` pins baseline prose with the shared `prose_pin` matcher.
- Error: the same paragraph calls a skipped test-first opportunity a violation and never mentions a user-instructed `tdd` skip.
- Data: `skipped-by-instruction: tdd <date>` in plan `## Risks` (build/SKILL.md:28) and the PR `Skipped by instruction:` line already record and disclose the skip.
- Boundary: no checker rule, intent field, manifest entry or station step changes; contract manifest stays 2.3.1.

## Task DAG
Wave 1 writes the guidance; wave 2 releases it.

**W1-01 Baseline states the code-first backfill path**  after: none  acceptance: 1, 2
- Files: loom-code/references/engineering-baseline.md, loom-code/tests/test_prose_pin_rule_text.py
- Test: A1 positive: baseline-states-characterise-first-and-record-scope; negative: legacy-paragraph-still-present. A2 positive: baseline-keeps-uninstructed-skip-violation; boundary: compile-failure-not-red-evidence.
- Risk: agent-decided — one paragraph after the Legacy backfill paragraph; one pin test reusing the shared prose_pin matcher; existing baseline pins preserved, coverage widened only.

**W2-01 Release metadata for loom-code 3.30.0**  after: W1-01  acceptance: 3, 4
- Files: loom-code/CHANGELOG.md, loom-code/plugin.json, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/package.json, README.md, loom-code/README*.md, loom-code/tests/test_write_plan_station_text.py
- Test: A3 positive: existing-rule-population-pin-passes; negative: existing-manifest-version-pin-passes. A4 positive: release-metadata-sync-test-passes-at-3.30.0; negative: sync-codex-manifests-check-exits-0.
- Risk: agent-decided — minor bump because engineering guidance read by implementers changes; loom-design and loom-workflow untouched.

## Simplicity check
- Reuse existing rule-population and manifest-version pins as A3 evidence instead of new A3 cases — taken

## Questions asked
① — what — #47、#48 的程式碼在流程前是否也已寫好 → 「只算 #45」
① — what — 重新表達案例要不要改 komado-Viewfinder → 「只在 loom-plugins 放副本」
① — what — 原範圍／先改程式再補流程模式／不加機制 → 「選 B」
① — what — 既有實作檔案清單手寫或由 git 算出 → 「自動算出」
① — what — #45 案例用假案例或複製真實 intent（公開 repo） → 「照結構做假案例」
① — what — 補紀錄強度（只記錄／輕量／完整） → 使用者確認現有省略機制即可
① — consequence — 複雜度檢驗 RESHAPE：最小做法或維持規劃 → 「照最小做法重寫 intent」
① — what — 覆述 intent（含自動發布授權） → 「對」

## Risks
1. Guidance only: nothing mechanically proves code preceded tests; the intent records the user's choice and the re-trigger for a checked version.
