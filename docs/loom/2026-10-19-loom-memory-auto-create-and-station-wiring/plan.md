# Auto-create store and station wiring for loom-memory — plan
intent: 2026-10-19-loom-memory-auto-create-and-station-wiring@7427832
charter: 1.1

## Task DAG

Wave 1 — store creation primitive and skill contract

**W1-01 Add store-creation subcommand to loom_memory.py**  after: none  acceptance: 1, 5, 6
- Files: loom-workflow/skills/loom-memory/scripts/loom_memory.py, loom-workflow/tests/loom-memory/test_loom_memory.py
- Test: A1 positive: create-store-from-templates-then-validate; negative: refuse-existing-nonempty-store. A5 positive: validate-exits-zero-on-created-store; boundary: legacy-shape-reported-not-touched. A6 positive: existing-store-tests-green; boundary: created-store-matches-template-shape.
- Risk: agent-decided — add an `init <store>` subcommand writing README.md and index.md from bundled templates only when the directory is absent or empty; refuse populated stores; report the legacy shape; preserve every existing script-test case (spec REQ-1, REQ-5, REQ-6).

**W1-02 Record auto-create steps in the skill contract**  after: W1-01  acceptance: 1, 3, 4
- Files: loom-workflow/skills/loom-memory/SKILL.md, loom-workflow/skills/loom-memory/references/operations.md, loom-workflow/skills/loom-memory/evals/record-timing.md, loom-workflow/tests/loom-memory/test_skill_contract.py
- Test: A1 positive: record-step-names-create-when-absent; negative: recall-absent-store-unchanged. A3 positive: recall-reads-index-when-store-exists; boundary: recall-absent-store-still-normal-no-memory. A4 positive: retire-deletes-after-user-approval; boundary: retire-refuses-deletion-without-approval.
- Risk: agent-decided — the Record section is digest-guarded (test_record_section_matches_the_digest_the_cold_reader_eval_was_run_against): any edit goes red until evals/record-timing.md is re-run against the new text and the digest is updated in the same commit; Recall and Retire sections are not edited (spec REQ-1, REQ-3, REQ-4).

Wave 2 — ship routing

**W2-01 Ship durable-lesson routing**  after: W1-02  acceptance: 2
- Files: loom-code/skills/ship/SKILL.md, loom-code/tests/local/test-git-memory-delegation.sh
- Test: A2 positive: ship-names-loom-memory-routing; negative: land-checkpoint-stays-git-memory-only.
- Risk: agent-decided — add one sentence beside the git-memory classification guidance (ship/SKILL.md:118) routing a qualifying durable lesson to loom-workflow:loom-memory, conditioned on the scarcity bar and plugin-optional; the land checkpoint (:230) stays untouched; existing station-text pins must keep passing (spec REQ-2).

Wave 3 — synchronized plugin release metadata

**W3-01 Bump loom-workflow minor version**  after: W2-01  acceptance: 6
- Files: loom-workflow/plugin.json, loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json, loom-workflow/package.json, loom-workflow/CHANGELOG.md, loom-workflow/README*.md, README.md, loom-workflow/tests/scripts/test_release_metadata.py
- Test: A6 positive: release-metadata-synced; negative: stale-manifest-or-readme-pin.
- Risk: agent-decided — new script subcommand and skill Record guidance are a minor release for loom-workflow; bump to the next unused minor above trunk, run test_release_metadata.py before the closing attestation (spec REQ-6).

**W3-02 Bump loom-code minor version**  after: W2-01  acceptance: 6
- Files: loom-code/plugin.json, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/CHANGELOG.md, loom-code/README*.md, README.md, loom-code/tests/test_write_plan_station_text.py
- Test: A6 positive: release-metadata-synced; negative: stale-version-pin.
- Risk: agent-decided — the ship station-guidance change is a minor release for loom-code; bump to the next unused minor above trunk and keep the synchronized-release test green (spec REQ-6).

## Simplicity check
- none found

## Questions asked
① — what — 你目前用 loom 時，memory 有沒有寫入 repo？
① — what — 這個 gap 要不要修？
① — what — store 建立方式要讓使用者做 init，還是 Record 自動偵測建立？
① — what — ship 站要不要把 durable lesson 分流到 loom-memory？
① — what — 結案報告要不要加一行教訓判斷（選項 A 還是 B）？

## Risks
1. The Record-section digest guard turns red on any text edit; the cold-reader eval replay and the digest update must land in the same commit.
2. ship station-text pins (test_simplified_station_text.py, test-git-memory-delegation.sh) reject added headings or forbidden phrases; keep the routing sentence additive.
