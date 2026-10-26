# Five skill/checker consistency defects — plan
intent: 2026-10-26-five-skill-consistency-defects@e732cfc95c4b6ce0fd296189a2902cf9589bbd8b
charter: 1.1

## Current State Evidence

- Forward — an agent following `adversarial.md` with no committed program is refused at `loom-code/scripts/loom_checker/probes.py:566` (`missing_adversarial_execution`), called from `finalize.py:283` and `attestation.py:195`.
- Reverse — `skills/closing-review/references/adversarial.md:78` says reuse "spends nothing against the ceiling"; the ceiling recomputes over every artifact finalize-review receives (`probes.py:518`, `finalize.py:334`).
- Error — the attestation `executions` grammar (`loom-code/contract/manifest.yaml:202`) admits only executed rows, and both validators reject an unknown kind (`attestation.py:191`), so a no-program outcome has nowhere to be recorded.
- Data — separators measured at `templates/02-linear-steps.md:62` (23), `04-reasoning-chain.md:70` (18, 22) and `:74` (25, 23), `08-system-architecture.md:63` (23); spec and verifier require six (`mermaid-cot-spec.md:204`, `verify_cot_html.py:60`).
- Boundary — Record routes an equivalent entry to Reconcile (`SKILL.md:130-131`), whose trigger names only contradiction or narrowing (`SKILL.md:143-145`, `references/operations.md:90-95`).

## Task DAG

### Wave 1 — four independent repairs, one per defect

**W1-01 Adversarial no-program outcome recorded and accepted**  after: none  acceptance: 1
- Files: `loom-code/scripts/loom_checker/command_handlers/finalize.py`, `loom-code/scripts/loom_checker/attestation.py`, `loom-code/scripts/loom_checker/intent_state.py`, `loom-code/contract/manifest.yaml`, `loom-code/skills/closing-review/SKILL.md`, `loom-code/tests/test_selection_finalize.py`, `loom-code/tests/test_loom_attestation.py`
- Test: A1 positive: no-program record finalizes and is recorded; negative: no program and no record still refused.
- Risk: agent-decided — a marker execution row (`no-program` plus reason) instead of a v3 schema; the delivery witness (`intent_state.py:148`) must accept the kind too.

**W1-02 Adversarial protocol prose matches the checker**  after: W1-01  acceptance: 1, 2, 5
- Files: `loom-code/skills/closing-review/references/adversarial.md`, `loom-code/tests/test_adversary_protocol.py`
- Test: A1 positive: no-program outcome stated; negative: no case-count floor worded. A2 positive: reuse counts toward the ceiling; boundary: own-program reuse stays free. A5 positive: python3 -m pytest accepted; negative: bare run refused.
- Risk: prose follows the checker on the ceiling and the command form; the protocol gains no case-count floor.

**W1-03 loom-memory names the equivalence outcome**  after: none  acceptance: 3
- Files: `loom-workflow/skills/loom-memory/SKILL.md`, `loom-workflow/skills/loom-memory/references/operations.md`, `loom-workflow/tests/loom-memory/test_skill_contract.py`
- Test: A3 positive: equivalence routes to Reconcile with one named outcome; negative: a second entry for the same subject stays forbidden.
- Risk: both files must name the outcome in the same words; no new operation and no second entry.

**W1-04 Template separators normalized to six**  after: none  acceptance: 4
- Files: `loom-workflow/skills/loom-visualization/templates/02-linear-steps.md`, `loom-workflow/skills/loom-visualization/templates/04-reasoning-chain.md`, `loom-workflow/skills/loom-visualization/templates/08-system-architecture.md`, `loom-workflow/tests/loom-visualization/test_templates.py`
- Test: A4 positive: every template separator run is six U+2501; negative: a longer or shorter run fails the guard.
- Risk: separator and heading shape only; node text, bullets, edges and ids stay byte-identical.

### Wave 2 — release packets, one per affected plugin

**W2-01 loom-code minor release packet**  after: W1-01, W1-02  acceptance: 6
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A6 positive: loom-code manifests and READMEs all read 3.50.0; negative: one unsynchronized derived manifest fails the pin.
- Risk: derived manifests come from `sync_codex_manifests.py --all`; the bump lands before closing review or the attestation goes stale.

**W2-02 loom-workflow minor release packet**  after: W1-03, W1-04  acceptance: 6
- Files: `loom-workflow/.claude-plugin/plugin.json`, `loom-workflow/CHANGELOG.md`, `loom-workflow/README.md`, `loom-workflow/README.ja.md`, `loom-workflow/README.zh-TW.md`
- Test: A6 positive: loom-workflow manifests and READMEs all read 5.16.0; negative: an unsynchronized derived manifest fails the sync check.
- Risk: same release packet as W2-01; a missing CHANGELOG entry or README string fails the version pins.

## Simplicity check

- W1-04 narrowed to template 04 only — declined: the spec's Layout layer owns every boxed node including 08's subgraph heading, so all four measured runs in 02/04/08 normalize to six in one task.

## Questions asked

① — what — 你要的是把五處技能文件與檢查程式互相矛盾的地方修好（deadlock、上限計數、等價條目、分隔線、指令寫法），做完後代理能照文件走完流程不被拒絕，對嗎？
① — consequence — 回答「是」授權之後自動推送並開 Ready PR（merge 另行決定）；第一條的最小修法採「不改檢查程式、只修文件計數規則」而非新增 reused 欄位，對嗎？（該句寫「第一條」，所指的「只修文件計數規則」實為第二條的上限計數；第一條改由檢查程式接受一筆無 program 結果，已依 intent Constraint 的一個可選欄位實作。）

## Risks

1. Item 1 changes the attestation's recorded execution kinds, so the closing review must re-run the complete package suite and re-read every attestation consumer.
2. Items 2 and 5 change protocol prose only; acceptance testing must read the prose against `probes.py` rather than look for new runtime behavior.
3. Derived plugin manifests are regenerated by the sync script, never hand-edited; a hand edit drifts silently and the version pins catch it late.
4. Upstream `docs/` evidence and intent text stay untouched, so no review lens re-reads them as changed content.
5. user-decided — second-vendor selection-confirmed: codex
