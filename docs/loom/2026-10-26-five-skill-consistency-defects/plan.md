# Five skill/checker consistency defects — plan
intent: 2026-10-26-five-skill-consistency-defects@e732cfc95c4b6ce0fd296189a2902cf9589bbd8b
charter: 1.1

## Current State Evidence

- Forward — an agent following `adversarial.md` with no committed program is refused at `loom-code/scripts/loom_checker/probes.py:566` (`missing_adversarial_execution`), called from `finalize.py:283` and `attestation.py:195`.
- Reverse — `skills/closing-review/references/adversarial.md:78` says reuse "spends nothing against the ceiling"; the ceiling recomputes over distinct paths from stored, graduated and supplied programs (`probes.py:518`, `finalize.py:334`).
- Error — the `executions` grammar (`manifest.yaml:202`) admits only executed rows, and both validators check command and digest before kind (`attestation.py:158`, `intent_state.py:143`), so a no-program outcome has nowhere to be recorded.
- Data — six U+2501 runs, each inside a `<div style='text-align:left'>` label: 23 (`02-linear-steps.md:62`), 18/22/25/23 (`04-reasoning-chain.md:70,74`) and 23 (`08-system-architecture.md:63`, a layer box); the verifier fixes the run at six (`verify_cot_html.py:60`).
- Boundary — Record routes an equivalent entry to Reconcile (`SKILL.md:130-131`), whose trigger names only contradiction or narrowing (`SKILL.md:143-145`, `references/operations.md:90-95`).

## Task DAG

### Wave 1 — four independent repairs, one per defect

**W1-01 Adversarial no-program outcome recorded and accepted**  after: none  acceptance: 1
- Files: `loom-code/scripts/loom_checker/command_handlers/finalize.py`, `loom-code/scripts/loom_checker/attestation.py`, `loom-code/scripts/loom_checker/intent_state.py`, `loom-code/contract/manifest.yaml`, `loom-code/skills/closing-review/SKILL.md`, `loom-code/tests/test_selection_finalize.py`, `loom-code/tests/test_loom_attestation.py`, `loom-code/tests/test_loom_checker_intake.py`
- Test: A1 positive: marker row finalizes, revalidates and is delivery-recognized; negative: blank reason, marker plus program, and no record each refused.
- Risk: agent-decided — marker row instead of a v3 schema; both validators accept it before the program-only checks, and it stays out of execution and cap counting. See Risks 6-8.

**W1-02 Adversarial protocol prose matches the checker**  after: W1-01  acceptance: 1, 2, 5
- Files: `loom-code/skills/closing-review/references/adversarial.md`, `loom-code/agents/adversary.md`, `loom-code/skills/build/SKILL.md`, `loom-code/tests/test_adversary_protocol.py`
- Test: A1 positive: producer names the record; negative: no ask-user-to-skip when no program exists, plain-words skip paths kept. A2 positive: reuse counts distinct paths; boundary: own-path reuse adds none. A5 positive: versioned launchers accepted; negative: bare run refused.
- Risk: prose follows the checker on the ceiling and the command form; the protocol gains no case-count floor and no second statement of the limit.

**W1-03 loom-memory names the equivalence outcome**  after: none  acceptance: 3
- Files: `loom-workflow/skills/loom-memory/SKILL.md`, `loom-workflow/skills/loom-memory/references/operations.md`, `loom-workflow/tests/loom-memory/test_skill_contract.py`
- Test: A3 positive: equivalence routes to Reconcile with one named outcome; negative: a second entry for the same subject stays forbidden.
- Risk: agent-decided — extend both files' trigger and outcome steps; Record's routing stays untouched because editing it forces a section-digest re-eval.

**W1-04 Label separators normalized to six**  after: none  acceptance: 4
- Files: `loom-workflow/skills/loom-visualization/templates/02-linear-steps.md`, `loom-workflow/skills/loom-visualization/templates/04-reasoning-chain.md`, `loom-workflow/skills/loom-visualization/templates/08-system-architecture.md`, `loom-workflow/tests/loom-visualization/test_templates.py`
- Test: A4 positive: every `<div style='text-align:left'>` label in the Mermaid blocks of 02, 04 and 08 passes `verify_cot_html.check_node_label` with no failure; negative: the same label with a seven-character run fails it.
- Risk: agent-decided — per-label check, not a full page: the templates lack page-mode headings and edge labels, and adding them would widen the templates, which the intent excludes.

### Wave 2 — release packets, one per affected plugin

**W2-01 loom-code minor release packet**  after: W1-01, W1-02  acceptance: 6
- Files: `loom-code/.claude-plugin/plugin.json`, `README.md`, `loom-code/CHANGELOG.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A6 positive: loom-code manifests and both README levels read 3.50.0; negative: one unsynchronized derived manifest fails the pin.
- Risk: `sync_codex_manifests.py --all` writes the three derived manifests; the bump lands before closing review or the attestation goes stale.

**W2-02 loom-workflow minor release packet**  after: W1-03, W1-04, W2-01  acceptance: 6
- Files: `loom-workflow/.claude-plugin/plugin.json`, `README.md`, `loom-workflow/CHANGELOG.md`, `loom-workflow/README.md`, `loom-workflow/README.ja.md`, `loom-workflow/README.zh-TW.md`, `loom-workflow/tests/scripts/test_release_metadata.py`
- Test: A6 positive: loom-workflow manifests, READMEs and both root rows read 5.16.0; negative: a stale `CURRENT` pin fails the release test.
- Risk: shares root `README.md` with W2-01, so it runs after it; its own `CURRENT` pin and root rows are rewritten here.

## Simplicity check

- W1-04 builds a full page from each template — declined: it would require headings, edge labels and columns the templates do not have; a per-label verifier check proves the separator alone.
- W1-04 leaves template 08 out — declined: its layer label carries the same div separator, and an acceptance tester reading "every template" would find it.
- W1-01 carried as a new attestation schema version — declined: a marker row leaves the key set, template and field pins untouched.

## Questions asked

① — what — 你要的是把五處技能文件與檢查程式互相矛盾的地方修好（deadlock、上限計數、等價條目、分隔線、指令寫法），做完後代理能照文件走完流程不被拒絕，對嗎？
① — consequence — 回答「是」授權之後自動推送並開 Ready PR（merge 另行決定）；第一條的最小修法採「不改檢查程式、只修文件計數規則」而非新增 reused 欄位，對嗎？（該句寫「第一條」，所指的「只修文件計數規則」實為第二條的上限計數；第一條改由檢查程式接受一筆無 program 結果，已依 intent Constraint 的一個可選欄位實作。）

## Risks

1. Item 1 changes how an attestation records the adversarial step, so its producer and every consumer land together: adversary contract, Build hand-off and recovery, finalization, validation and delivery recognition.
2. Acceptance 6 is proved by `scripts/run_package_tests.py --loom-family` at the end of Build; the two release pins check versions only and are not a substitute.
3. Items 2 and 5 change protocol prose only; acceptance testing must read the prose against `probes.py` rather than look for new runtime behavior.
4. Derived plugin manifests are regenerated by the sync script, never hand-edited; a hand edit drifts silently and the version pins catch it late.
5. user-decided — second-vendor selection-confirmed: codex
6. agent-decided — the contract manifest `version:` stays 2.3.1: W1-01 adds a row form inside an existing field, no field added or removed. W2-01's CHANGELOG entry states "contract manifest version stays 2.3.1", the wording `test_adversarial_version_metadata_sync.py:163` reads.
7. W1-01 edits `closing-review/SKILL.md`, which `test_adversary_protocol.py` scans for a case-count floor; its prose gains no wording such as "at least one program", and that test runs after the edit.
8. agent-decided — W1-01 counts the no-program record only through `missing_adversarial_execution` (`probes.py:566`), which finalize-review and the attestation validator both call, so one place decides what satisfies the adversarial step; `intent_state.py` only admits the row shape.
