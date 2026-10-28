# Change records start on the change branch — plan
intent: 2026-10-29-change-branch-before-intent@f4b4f3da
charter: 1.1

## Current State Evidence

- Forward — capture-intent Step 5 lets the intent be committed on the trunk and creates no branch (`loom-design/skills/capture-intent/SKILL.md:339`).
- Reverse — write-plan branches at Step 6 (`loom-code/skills/write-plan/SKILL.md:452-464`) or via Step 3 (`:209`); its confirmation commit comes earlier (`references/confirm-intent.md:108-118`).
- Error — land's `sync_trunk` fast-forwards only and prints `trunk not updated` on divergence (`land.py:310-341`); ship §5 never says what to do then (`ship/SKILL.md:244-278`).
- Data — the branch is `<type>/<change-id>`; Step 6's type list is pinned by `test_write_plan_station_text.py:207`, bare names by its repo sweep at `:259`.
- Boundary — write-spec commits its spec with no branch guidance (`loom-design/skills/write-spec/SKILL.md:282`); the intent checker already refuses to run on the trunk (`helpers.py:279`).

## Task DAG

### Wave 1 — every station branches before its first change-owned commit

**W1-01 write-plan states one branch rule before any commit**  after: none  acceptance: 4, 5
- Files: `loom-code/skills/write-plan/SKILL.md`, `loom-code/skills/write-plan/references/confirm-intent.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A4 positive: branch-rule-precedes-confirmation-and-skip-record-commits; negative: intent-on-trunk-allowance-absent. A5 positive: own-change-branch-reused; boundary: unrelated-branch-or-detached-head-resolved-before-commit.
- Risk: agent-decided — one rule near entry, referenced from Step 3, confirm-intent and Step 6; `test_write_plan_station_text.py` typed-branch pins follow it to its new section, coverage preserved.

**W1-02 capture-intent and write-spec commit only on the change branch**  after: W1-01  acceptance: 1, 5
- Files: `loom-design/skills/capture-intent/SKILL.md`, `loom-design/skills/write-spec/SKILL.md`, `loom-design/tests/spec/test_capture_intent_contract.py`, `loom-design/tests/spec/test_write_spec_contract.py`
- Test: A1 positive: capture-intent-branches-before-confirmation-commit; negative: trunk-commit-allowance-absent. A5 positive: own-change-branch-reused-at-capture; boundary: write-spec-guard-defers-to-capture-intent-rule.
- Risk: agent-decided — loom-design never reads loom-code files at runtime, so capture-intent restates the type list once and write-spec only guards with one sentence; the byte-identical station-summary table stays untouched; word caps apply.

**W1-03 ship never discards a diverged trunk unasked**  after: none  acceptance: 2, 3
- Files: `loom-code/skills/ship/SKILL.md`, `loom-code/tests/test_ship_station_text.py`
- Test: A3 positive: ship-reports-trunk-not-updated-and-asks; negative: acceptance-is-not-permission-to-discard. A2 positive: existing test_clean_trunk_fast_forwards; negative: existing test_trunk_not_fast_forward_message_has_no_rebase_advice.
- Risk: `land.py` `sync_trunk` and `test_land_cleanup.py` stay unchanged (intent Constraints); A2 follows from W1-01 and W1-02 keeping change commits off the trunk.

### Wave 2 — one release packet for both plugins

**W2-01 Release loom-code 3.51.0 and loom-design 2.16.0**  after: W1-01, W1-02, W1-03  acceptance: 1, 4
- Files: `loom-{code,design}/.claude-plugin/plugin.json`, `README.md`, `loom-{code,design}/CHANGELOG.md`, `loom-code/README*.md`, `loom-design/README*.md`, `loom-code/tests/test_write_plan_station_text.py`, `loom-design/tests/spec/test_capture_intent_contract.py`
- Test: A4 positive: every loom-code manifest and README reads 3.51.0; negative: an unsynchronized derived manifest fails the pin. A1 positive: loom-design reads 2.16.0 everywhere; negative: a stale changelog heading fails the pin.
- Risk: `sync_codex_manifests.py --all` writes derived manifests; minor bumps because station guidance changes; the bump lands before finalize-review or the attestation goes stale.

## Simplicity check

- Merge the two release tasks into one, removing the ordering edge forced by the shared root README — taken
- write-spec carries one guard sentence pointing at capture-intent's rule instead of a second type list — taken
- Release task cites no Acceptance line — declined: every non-memory task must reference one, and the release is what ships A1 and A4 to installed copies

## Questions asked

① — what — restatement v1 of the intent (branch before the first commit, plus a ship sentence never discarding trunk commits unasked; automatic publication), ending 「這樣對嗎？」 — answered 「可以幫我用 codex 再獨立 review 一次嗎」
① — what — restatement v2 after the Codex review (five Acceptance lines; committing an intent on the trunk for later is removed; automatic publication) — answered 「對」

## Risks

1. Prose-only behaviour: text pins prove the rules are present; A1-A3 behaviour is shown by the acceptance tester running a sandbox change through capture-intent and land.
2. Run suites with `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID`; SKILL.md word caps are pinned in the contract tests (`test_capture_intent_contract.py`, `test_write_spec_contract.py`), so added prose must stay within them.
3. Implementers add no `# concern:` header to task tests; that header counts against the adversarial probe cap.
4. Outside review already ran on the intent: Codex gpt-6.1-sol/high, PROCEED-WITH-CAVEAT, six findings folded into the intent before confirmation.
