# A standing ARCHITECTURE.md that agents are held to, the way DESIGN.md is — plan
intent: 2026-09-25-standing-architecture-doc@448fad32
spec: docs/loom/2026-09-25-standing-architecture-doc/spec.md@4564baef
charter: 1.0

## Task DAG

### Wave 0 — the tool and its consumers

**W0-01 The architecture tool, its schema and validator**  after: —  acceptance: 2, 3, 4
- Files: `loom-design/skills/architecture/SKILL.md`, `loom-design/skills/architecture/references/architecture-md-schema.md`, `loom-design/scripts/architecture/validate_architecture_output.py`, `loom-design/tests/architecture/test_architecture_skill.py`, `loom-design/tests/architecture/test_validate_architecture_output.py`, `loom-design/tests/pytest.ini`
- Test: A2 positive: ratified-rules-only-file-valid; negative: overview-section-rejected. A3 positive: rule-with-existing-guard-valid; negative: missing-guard-path-rejected. A4 positive: schema-states-failure-message-fields; boundary: review-only-rule-needs-no-guard.
- Risk: landed as 7c2fb913 (record-only scope); mirrors design-system's shape (spec Design decision); no gate marker; agent-decided.

**W0-04 The tool designs with the user; Decisions section; re-design mode**  after: W0-01  acceptance: 1, 2, 8
- Files: `loom-design/skills/architecture/SKILL.md`, `loom-design/skills/architecture/references/architecture-md-schema.md`, `loom-design/skills/architecture/references/design-know-how.md`, `loom-design/scripts/architecture/validate_architecture_output.py`, `loom-design/tests/architecture/test_architecture_skill.py`, `loom-design/tests/architecture/test_validate_architecture_output.py`, `docs/loom/2026-09-25-standing-architecture-doc/evidence/architecture-design-research.md`
- Test: A1 positive: skill-reads-code-and-proposes-two-options-per-choice; negative: single-answer-proposal-not-allowed. A2 positive: decisions-section-valid; negative: decisions-section-missing-rejected. A8 positive: skill-states-redesign-updates-decisions-rules-guards; negative: unratified-file-rejected.
- Risk: intent amended at decision point one after W0-01 landed; widens `test_validate_architecture_output.py` coverage, none narrowed; know-how cited from the research evidence; agent-decided.

**W0-02 Standing WARN and contract entries name ARCHITECTURE.md**  after: W0-04  acceptance: 7
- Files: `loom-code/scripts/loom_checker/rule_checks/standing.py`, `loom-code/scripts/loom_checker/command_handlers/standing.py`, `loom-code/scripts/loom_checker/rules.py`, `loom-code/contract/manifest.yaml`, `loom-code/tests/test_loom_checker_standing.py`, `loom-code/tests/test_contract_manifest.py`
- Test: A7 positive: missing-architecture-named-in-warn; negative: waiver-silences-architecture-warn.
- Risk: `test_loom_checker_standing.py` coverage widens (three documents); tool count 10→11 reaches the 18 ceiling; rule list unchanged; agent-decided.

**W0-03 write-plan reads it; review scores conformance**  after: W0-02  acceptance: 5, 6
- Files: `loom-code/skills/write-plan/SKILL.md`, `loom-code/skills/closing-review/references/lenses.md`, `loom-code/agents/reviewer.md`, `loom-code/tests/test_architecture_doc_consumers.py`
- Test: A5 positive: write-plan-step5-reads-architecture-and-names-rule; negative: absent-document-adds-no-step. A6 positive: code-lens-has-architecture-conformance-na-without-doc; negative: no-reviewer-count-change.
- Risk: code lens grows to twelve dimensions; reviewer.md list kept in sync; SOLID dimension untouched (spec Design decision); agent-decided.

### Wave 1 — registration and release

**W1-01 loom-design registers the tool; minor release 2.4.0**  after: W0-03  acceptance: 1
- Files: `loom-design/skills/using-loom-design/SKILL.md`, `loom-design/plugin.json`, `loom-design/.claude-plugin/plugin.json`, `loom-design/.codex-plugin/plugin.json`, `loom-design/CHANGELOG.md`, `loom-design/README.md`, `loom-design/README.ja.md`, `loom-design/README.zh-TW.md`
- Test: A1 positive: router-row-routes-architecture; negative: manifests-out-of-sync-detected.
- Risk: codex manifest regenerated via `scripts/sync_codex_manifests.py`; agent-decided.

**W1-02 Inventory pins and mechanism entries**  after: W0-02, W0-03, W1-01  acceptance: 1
- Files: `tests/test_loom_plugin_install_layout.py`, `tests/test_loom_skill_description_catalog.py`, `loom-code/tests/test_simplified_station_text.py`, `loom-design/tests/spec/test_capture_intent_contract.py`, `loom-design/tests/test_plugin_manifest.py`, `docs/loom/evidence/mechanisms.yaml`, `docs/skill-dogfood/2026-09-13-compress-loom-skill-descriptions/cases.md`
- Test: A1 positive: installed-layout-includes-architecture; negative: description-budget-exceeded-detected.
- Risk: inventory pins widen by one tool, none narrowed; description added within the catalog budget; agent-decided.

**W1-03 loom-code minor release 3.16.0 with budget exception**  after: W1-02  acceptance: 6, 7
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/tests/test_write_plan_station_text.py`, `README.md`, `loom-code/scripts/check_mechanisms.py`, `loom-code/tests/test_check_mechanisms.py`
- Test: A6 positive: versions-synchronized-3.16.0; negative: check-mechanisms-without-exception-fails. A7 positive: changelog-names-standing-warn-change; boundary: contract-version-bumped.
- Risk: minor release; `budget-exception:` line for net 140→142; skill cap 22→23 admits architecture (user-decided 2026-09-25); widens `test_check_mechanisms.py` cap cases.

### Wave 2 — adversary fixes

**W2-01 Validator rejects outside, duplicated and misordered sections; root-only lookup; graduate the probe**  after: W1-03  acceptance: 2, 3, 7
- Files: `loom-design/scripts/architecture/validate_architecture_output.py`, `loom-code/scripts/loom_checker/command_handlers/standing.py`, `loom-code/tests/test_loom_checker_standing.py`, `docs/loom/2026-09-25-standing-architecture-doc/evidence/probes/test_abuse_architecture_validator.py`, `loom-design/tests/architecture/test_abuse_architecture_validator.py`
- Test: A2 positive: in-order-single-sections-valid; negative: duplicated-or-misordered-section-rejected. A3 positive: repo-relative-guard-valid; negative: absolute-or-parent-guard-rejected. A7 positive: root-architecture-silences-warn; negative: docs-loom-architecture-still-warns.
- Risk: class "validator accepts a malformed ARCHITECTURE.md" searched across the validator and schema; lookup class searched across standing handler, write-plan, skill, manifest; probe graduates unchanged; agent-decided.

## Questions asked
① — what — 我原本以為他就是要幫我 設計整個系統架構 的噎 → 我想要走方案 2 因為正常流程就是應該要設計好工程架構跟專案資料夾管理
① — done — 對
① — done — 對 檔名用根目錄的 ARCHITECTURE.md 和 PRINCIPLES.md、DESIGN.md 放在一起
① — consequence — 檔名用根目錄的 ARCHITECTURE.md（vs docs/ 底下）

## Risks
1. user-decided — ARCHITECTURE.md lives at the repository root beside PRINCIPLES.md and DESIGN.md (2026-09-25).
2. Acceptance 1–4 and 8 run in a target repository, so acceptance testing follows the tool in a throwaway repository and breaks a rule to see the guard fail.
3. The counted tool budget reaches its ceiling of eighteen; a later tool needs a budget decision first.
4. `selection show` judged the intent-only branch narrow; the full flow runs because the change adds a tool and edits three stations (agent-decided).
5. The intent was amended and re-confirmed (448fad32) after W0-01 landed: the tool designs, not only records; W0-04 carries the delta (user-decided 2026-09-25).
6. Keep complexity low (user, 2026-09-25): the validator checks structure only, the know-how reference stays under about 150 lines, at most one positive/negative pair per Acceptance line.
7. user-decided — the counted skill cap rises from 22 to 23 to admit the architecture tool, as releases 3.1.3 and 3.4.0 did (2026-09-25).
8. Known limitations (deliberate-only): all rules marked `check: review`, an empty guard, or a guard the suite never runs pass the validator; review's architecture-conformance dimension is the backstop. Non-UTF-8 ARCHITECTURE.md crashes the validator (not fixed).
