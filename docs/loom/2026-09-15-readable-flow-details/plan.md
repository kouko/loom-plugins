# Carry details agreed before the intent into the spec, and use tables and diagrams where they help — plan
intent: 2026-09-15-readable-flow-details@33a5ad54
charter: 1.0

## Current State Evidence
- Forward: `loom-design/skills/capture-intent/SKILL.md:268` defers behaviour to spec and deletes unsupported detail; `:283` and `:318` carry only questions in the hand-off, not agreed details.
- Reverse: `loom-code/skills/write-plan/SKILL.md:289` writes a spec for `needs-design: no` only when rationale outgrows a Risk line; `:326` reads UI flows back one sentence at a time.
- Error: `loom-design/skills/write-spec/references/ui-flows.md:9` prescribes one line per operation and `:74` one sentence per operation at decision point 2, with no link to tables or diagrams.
- Data: `loom-design/skills/write-spec/references/spec-forms.md:31` and `:60` already define tables and Mermaid; only `docs/loom/2026-09-14-loom-visualization/spec.md` uses either.
- Boundary: `loom-code/contract/templates/spec-minimal.md:29-30` gives UI flows a one-line placeholder; the checker excludes non-code template paths from interface surfaces (`loom-code/scripts/loom_checker/rule_checks/intent.py:342`).

## Task DAG
<!-- When a spec requirement changes after this commit, the un-landed
     tasks it touches are replaced and the reason is named in the commit
     message. Landed tasks stay as they are. -->

### Wave 1 — station guidance

**W1-01 capture-intent carries agreed details and allows intent forms**  after: none  acceptance: 1, 5, 6
- Files: `loom-design/skills/capture-intent/SKILL.md`, `loom-design/scripts/spec/test_capture_intent_contract.py`
- Test: A1 positive: hand-off-lists-agreed-details-and-requires-spec; negative: no-details-no-forced-spec. A5 positive: engineering-restatement-shows-carried-details-table; boundary: nothing-agreed-shows-no-table. A6 positive: intent-sections-may-use-tables-and-diagrams; negative: acceptance-stays-numbered-list-and-flows-stay-out.
- Risk: a carried-details list invites agent-invented detail; the text limits it to details the user stated or agreed. user-decided.

**W1-02 write-spec records carried details and lays out flows**  after: W1-01  acceptance: 1, 2, 3
- Files: `loom-design/skills/write-spec/SKILL.md`, `loom-design/skills/write-spec/references/ui-flows.md`, `loom-design/skills/write-spec/references/spec-forms.md`, `loom-design/scripts/spec/test_write_spec_contract.py`
- Test: A1 positive: spec-records-each-carried-detail; negative: agent-proposal-not-agreed-not-recorded. A2 positive: parallel-cases-table-branching-diagram; boundary: short-flow-stays-lines. A3 positive: readback-leads-with-table-or-text-diagram; negative: chat-readback-has-no-mermaid.
- Risk: consumes the W1-01 hand-off, so it runs after it; the one-sentence read-back stays after the table. agent-decided.

**W1-03 write-plan mirrors the guidance and the template points to forms**  after: W1-02  acceptance: 1, 3, 4, 5
- Files: `loom-code/skills/write-plan/SKILL.md`, `loom-code/contract/templates/spec-minimal.md`, `loom-code/scripts/test_write_plan_shape_text.py`
- Test: A1 positive: carried-details-force-minimal-spec; negative: no-details-keeps-evidence-only-plan. A3 positive: write-plan-readback-leads-with-table-or-text-diagram; negative: write-plan-readback-has-no-mermaid. A4 positive: both-stations-share-form-rules; boundary: template-placeholder-names-table-and-diagram. A5 positive: write-plan-intake-shows-carried-details-table; boundary: write-plan-no-details-no-table.
- Risk: mirrors W1-01 and W1-02 wording, so it runs last; a `.md` template edit stays off interface surfaces. agent-decided.

### Wave 2 — release

**W2-01 loom-design release notes and versions**  after: W1-03  acceptance: 7
- Files: `loom-design/CHANGELOG.md`, `loom-design/README.md`, `loom-design/README.ja.md`, `loom-design/README.zh-TW.md`, `loom-design/plugin.json`, `loom-design/.claude-plugin/plugin.json`, `loom-design/.codex-plugin/plugin.json`, `README.md`
- Test: A7 positive: loom-design-version-2-2-0-consistent; negative: stale-2-1-6-pin-fails.
- Risk: minor release 2.2.0 because station guidance changes; the root README carries both plugin rows. agent-decided.

**W2-02 loom-code release notes, versions and checks**  after: W2-01  acceptance: 7
- Files: `loom-code/CHANGELOG.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/scripts/test_write_plan_station_text.py`
- Test: A7 positive: package-groups-and-check-mechanisms-green; negative: stale-3-6-1-pin-fails.
- Risk: minor release 3.7.0 after main shipped 3.6.1 (trunk synced at 8a30883a); contract version changes only if a manifest test pins the template text. agent-decided.

### Wave 3 — adversary findings (end-of-Build probes at 97017250)

**W3-01 capture-intent and write-spec close carried-detail gaps**  after: W2-02  acceptance: 1, 5, 6
- Files: `loom-design/skills/capture-intent/SKILL.md`, `loom-design/skills/write-spec/SKILL.md`, `loom-design/scripts/spec/test_capture_intent_contract.py`, `loom-design/scripts/spec/test_write_spec_contract.py`, `loom-design/CHANGELOG.md`
- Test: A1 positive: only-explicit-yes-is-carried; negative: unanswered-or-deferred-proposal-dropped. A5 positive: product-needs-design-no-shows-table-at-intent-confirmation; boundary: product-needs-design-yes-defers-to-write-spec. A6 positive: intent-diagram-form-is-flowchart-or-table; negative: negated-pin-mutant-killed.
- Risk: silence read as agreement failed all three cold reads; a product change without a spec had no stop showing its details. agent-decided.

**W3-02 write-plan and intake checker accept flow forms and confirm product specs**  after: W3-01  acceptance: 1, 2, 3, 5, 6
- Files: `loom-code/skills/write-plan/SKILL.md`, `loom-code/scripts/loom_checker/command_handlers/intake.py`, `loom-code/scripts/loom_checker/rule_checks/intake.py`, `loom-code/scripts/test_write_plan_shape_text.py`, `loom-code/scripts/test_loom_checker_intake.py`, `loom-code/CHANGELOG.md`, `loom-code/scripts/loom_checker/rule_checks/intent.py`, `loom-code/scripts/test_loom_checker_intent.py`
- Test: A1 positive: write-plan-only-explicit-yes-is-carried; negative: write-plan-unanswered-proposal-dropped. A2 positive: table-or-mermaid-ui-flows-count-as-flows; negative: empty-ui-flows-still-blocked. A3 positive: product-non-visible-detail-on-requirement-line; negative: product-detail-not-on-design-decision. A5 positive: product-spec-under-needs-design-no-requires-confirmed-behavior; boundary: engineering-spec-under-no-skips-confirmed-behavior. A6 positive: mermaid-keywords-in-fence-not-identifiers; negative: snake-case-node-label-still-blocked.
- Risk: intake now checks an existing product spec regardless of needs-design, enforcing the existing write-plan gate. agent-decided.

**W3-03 Re-record cold reads and re-run checks**  after: W3-02  acceptance: 1, 7
- Files: `docs/loom/2026-09-15-readable-flow-details/evidence/coldread/run-1.txt`, `docs/loom/2026-09-15-readable-flow-details/evidence/coldread/run-2.txt`, `docs/loom/2026-09-15-readable-flow-details/evidence/coldread/run-3.txt`
- Test: A1 positive: three-fresh-readers-carry-only-agreed-details; negative: stale-recording-fails. A7 positive: package-suite-and-all-probes-green; negative: any-probe-failure-blocks-hand-off.
- Risk: recorded runs load the global CLAUDE.md; recording uses the existing probe command unchanged. agent-decided.

**W3-04 Carry flow details in the user's words, not background or inference**  after: W3-03  acceptance: 1, 7
- Files: `loom-design/skills/capture-intent/SKILL.md`, `loom-code/skills/write-plan/SKILL.md`, `loom-design/scripts/spec/test_capture_intent_contract.py`, `loom-code/scripts/test_write_plan_shape_text.py`, `docs/loom/2026-09-15-readable-flow-details/evidence/coldread/run-1.txt`, `docs/loom/2026-09-15-readable-flow-details/evidence/coldread/run-2.txt`, `docs/loom/2026-09-15-readable-flow-details/evidence/coldread/run-3.txt`
- Test: A1 positive: carried-detail-kept-in-user-words; negative: background-context-and-inference-not-carried. A7 positive: re-recorded-cold-reads-and-package-suite-green; negative: added-interpretation-flagged.
- Risk: the W3-03 recording showed a reader carrying background (cron use) and appending its own inference (non-interactive). agent-decided.

### Wave 4 — closing review round 1 findings (reviewed a99757de)

**W4-01 Product details confirmed at decision point 2 only; quote the user**  after: W3-04  acceptance: 1, 5
- Files: `loom-design/skills/capture-intent/SKILL.md`, `loom-design/skills/write-spec/SKILL.md`, `loom-design/scripts/spec/test_capture_intent_contract.py`, `loom-design/scripts/spec/test_write_spec_contract.py`, `loom-design/CHANGELOG.md`, `docs/loom/2026-09-15-readable-flow-details/evidence/coldread/run-1.txt`, `docs/loom/2026-09-15-readable-flow-details/evidence/coldread/run-2.txt`, `docs/loom/2026-09-15-readable-flow-details/evidence/coldread/run-3.txt`
- Test: A1 positive: carried-detail-quotes-user-or-agreed-proposal; negative: non-visible-detail-never-new-req. A5 positive: intent-confirmation-table-engineering-only; negative: product-needs-design-no-not-shown-at-intent-confirmation.
- Risk: the product needs-design no path showed details twice once write-plan's forced spec ran decision point 2; cold reads re-recorded because capture-intent changes. agent-decided.

**W4-02 write-plan mirrors round 1 fixes; checker notes**  after: W4-01  acceptance: 1, 2, 5, 7
- Files: `loom-code/skills/write-plan/SKILL.md`, `loom-code/scripts/test_write_plan_shape_text.py`, `loom-code/scripts/loom_checker/rule_checks/intake.py`, `loom-code/scripts/test_loom_checker_intake.py`, `loom-code/CHANGELOG.md`
- Test: A1 positive: write-plan-quotes-user-words; negative: write-plan-no-branch-ui-flows-not-forced-na. A2 positive: graph-and-statediagram-aliases-documented; negative: below-floor-table-row-and-single-letter-nodes-blocked. A5 positive: write-plan-confirmation-table-engineering-only; negative: write-plan-product-details-not-at-intent-confirmation. A7 positive: package-suite-and-probes-green; negative: stale-cold-read-fails.
- Risk: write-plan crosses the soft word target; the PR body carries the one-line reason. agent-decided.

## Questions asked
① — what — 你在聊天確認當下難讀，還是事後讀文件難讀？ kouko: "兩者都有點難讀"
① — what — 想在哪個時間點確認談好的細節有被保留？ kouko: "Ｃ 但是照理說細節應該在 spec 的時候會被記錄下來 所以應該不用額外的機制？"
① — what — engineering 改動要不要讓你在 build 前看到帶過來的細節？ kouko: "B 吧？"
① — what — 帶過來的細節要不要放進最終驗收？ kouko: "A"
① — what — restated intent and automatic publication; kouko: "對"

## Risks
1. user-decided — carried details get no new final-acceptance check; product blind runs already walk UI flows, engineering details rely on spec reviewers.
2. Prose rules cannot be checked against the conversation; the end-of-Build adversary runs a fresh-context cold read over a sample conversation to confirm no invented detail is carried.
3. Details live only in the conversation between intent confirmation and spec writing; compaction in that window can still drop them. Accepted for this change.
4. The carried-details paragraphs are deliberately not gate-marked: the intent's constraint allows no new mechanism beyond carrying details into the spec.
