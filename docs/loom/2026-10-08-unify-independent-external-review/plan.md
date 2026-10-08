# Unified independent external review — plan
intent: 2026-10-08-unify-independent-external-review@34ece76cee1980a8c4391b6401e7cafb528b8445
spec: docs/loom/2026-10-08-unify-independent-external-review/spec.md@10fe4937
charter: 1.1

## Task DAG

### Wave 1 — Shared outside execution boundary

**W1-01 Explicit outside executor profile**  after: none  acceptance: 4, 5
- Files: loom-code/skills/external-review/SKILL.md, loom-code/scripts/external_review.py, loom-code/tests/test_external_review.py
- Test: A4 positive: explicit-codex-claude-agy; boundary: discovery-unavailable. A5 positive: accepted-evidence-level; negative: mismatch-timeout-no-fallback.
- Risk: agent-decided — the named loom-code skill owns one executor boundary for every task; REQ-4/5 require explicit settings and truthful CLI-specific evidence.

### Wave 2 — Route review tasks without changing their criteria

**W2-01 Independent-advisor routing and consent**  after: W1-01  acceptance: 1, 2, 3
- Files: loom-workflow/skills/independent-advisor/SKILL.md, loom-workflow/skills/independent-advisor/references/executor-detection.md, loom-workflow/skills/independent-advisor/references/dispatch-protocol.md, loom-workflow/skills/independent-advisor/test-prompts.json, loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py, loom-workflow/skills/independent-advisor/README.md, loom-workflow/skills/independent-advisor/README.ja.md, loom-workflow/skills/independent-advisor/README.zh-TW.md
- Test: A1 positive: named-code-plan-decision-review; negative: failed-outside-distinct. A2 positive: owning-contract-verdict; negative: advisor-verdict-substitution. A3 positive: prompt-only-notice; negative: unapproved-probe.
- Risk: agent-decided — invoke loom-code:external-review by skill name and retire duplicated probes; REQ-1/2/3 keep the incumbent review and opt-in boundary.

**W2-02 Closing review retains incumbent and uses shared profile**  after: W1-01  acceptance: 1, 2, 5
- Files: loom-code/skills/closing-review/SKILL.md, loom-code/scripts/loom_checker/reviewers.py, loom-code/scripts/loom_checker/attestation.py, loom-code/scripts/loom_checker/command_handlers/finalize.py, loom-code/tests/test_loom_attestation.py, loom-code/tests/test_selection_finalize.py, loom-code/tests/test_contract_manifest.py, docs/loom/evidence/mechanisms.yaml
- Test: A1 positive: floor-one-adds-outside; negative: no-incumbent. A2 positive: same-lens-yaml; negative: invalid-verdict. A5 positive: explicit-pair-required; negative: default-fallback.
- Risk: agent-decided — recompute reviewer count and bind outside verdict to a runner receipt; the old gate metadata and its dispatch-profile pin are updated with REQ-1/2/5.

### Wave 3 — Selection, integration and release

**W3-01 Vendor selection and notice alignment**  after: W2-01, W2-02  acceptance: 3, 4, 5
- Files: loom-code/scripts/second_vendor_policy.py, loom-code/tests/test_second_vendor_policy.py, loom-code/skills/write-plan/references/second-vendor-ask-and-docs-lint.md, loom-workflow/skills/independent-advisor/references/report-contract.md
- Test: A3 positive: opt-in-selection; negative: pending-no-execution. A4 positive: agy-selected-family; boundary: cross-family-CLI. A5 positive: provenance-disclosed; negative: unknown-family.
- Risk: agent-decided — model provider family decides independence, not CLI branding; REQ-3/4/5 keep suggestion non-blocking.

**W3-02 Loom-code release metadata**  after: W3-01  acceptance: 1, 2, 3, 4, 5
- Files: loom-code/plugin.json, loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/CHANGELOG.md, loom-code/README*.md, loom-code/package.json, loom-code/tests/test_write_plan_station_text.py
- Test: A1 positive: route-activation; negative: failed-leg. A2 positive: same-contract; negative: substituted-format. A3 positive: notice-only; negative: implicit-dispatch. A4 positive: explicit-pair; boundary: stale-candidate. A5 positive: visible-limitation; negative: silent-fallback.
- Risk: agent-decided — sync the loom-code release mirrors after behavior stabilizes; REQ-1–5 need package and acceptance evidence.

**W3-03 Loom-workflow release metadata**  after: W3-02  acceptance: 1, 2, 3, 4, 5
- Files: loom-workflow/plugin.json, loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json, loom-workflow/CHANGELOG.md, loom-workflow/README*.md, loom-workflow/package.json, loom-workflow/tests/scripts/test_release_metadata.py, README.md
- Test: A1 positive: route-activation; negative: failed-leg. A2 positive: same-contract; negative: substituted-format. A3 positive: notice-only; negative: implicit-dispatch. A4 positive: explicit-pair; boundary: stale-candidate. A5 positive: visible-limitation; negative: silent-fallback.
- Risk: agent-decided — sync workflow mirrors and root version pins before final review; REQ-1–5 need package and acceptance evidence.

### Wave 4 — Retain adversarial regressions

**W4-01 Graduate caught probe programs**  after: W3-03  acceptance: 4, 5
- Files: docs/loom/2026-10-08-unify-independent-external-review/evidence/probes/test_codex_header_spoof.py, docs/loom/2026-10-08-unify-independent-external-review/evidence/probes/test_codex_malformed_listing.py, docs/loom/2026-10-08-unify-independent-external-review/evidence/probes/test_consent_family_mismatch.py, loom-code/tests/test_external_review_adversarial.py
- Test: A4 positive: stderr-header-and-valid-list; negative: spoofed-header-and-null-list. A5 positive: consented-family; negative: contradictory-family.
- Risk: agent-decided — move the three RED-then-GREEN adversarial cases into the package suite before finalization; retain their concern anchors and avoid another harness.

**W4-02 Register the new skill and release metadata**  after: W4-01  acceptance: 1, 4, 5
- Files: tests/test_loom_skill_description_catalog.py, loom-code/skills/using-loom-code/SKILL.md, docs/loom/evidence/mechanisms.yaml, loom-code/scripts/check_mechanisms.py, loom-code/tests/test_check_mechanisms.py, loom-code/CHANGELOG.md, loom-code/package.json, loom-code/skills/external-review/SKILL.md
- Test: A1 positive: router-target-present; negative: missing-leaf-accounting. A4 positive: manifest-sync; negative: derived-package-drift. A5 positive: mechanism-registered; negative: undeclared-budget-increase.
- Risk: agent-decided — declare one counted skill budget exception for the shared handoff; registration and evaluation are necessary to keep repo gates recomputable.

**W4-03 Align advisor structure pin with the shared executor**  after: W4-02  acceptance: 1, 4, 5
- Files: loom-workflow/tests/scripts/test_independent_advisor_compaction.py, loom-workflow/skills/independent-advisor/SKILL.md, loom-workflow/skills/independent-advisor/references/executor-detection.md
- Test: A1 positive: named-external-review-route; negative: lost-incumbent-contract. A4 positive: explicit-pair-evidence; negative: stale-advisor-probe-pin. A5 positive: complete-consent; negative: old-credential-assumption.
- Risk: agent-decided — the old structure test pins deleted advisor-side probe commands; replace those assertions with the current single handoff and consent contract.

### Wave 5 — Close live outside-review findings and remove duplicate consent

**W5-01 Direct-request authorization**  after: W4-03  acceptance: 3, 6
- Files: loom-workflow/skills/independent-advisor/SKILL.md, loom-workflow/skills/independent-advisor/references/executor-detection.md, loom-workflow/skills/independent-advisor/README*.md, loom-code/skills/external-review/SKILL.md, loom-code/skills/closing-review/SKILL.md, loom-workflow/skills/independent-advisor/test-prompts.json, loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py, loom-workflow/tests/scripts/test_independent_advisor_compaction.py
- Test: A6 positive: named-agent-with-active-task-target-runs-after-disclosure; negative: suggestion-or-expanded-scope-stops. A3 negative: notice-does-not-authorize.
- Risk: user-decided — a direct named request authorizes one bounded review without a second confirmation; disclosure remains visible, and missing or expanded choices stop dispatch.

**W5-02 Ground and correct outside CLI execution**  after: W5-01  acceptance: 4, 5
- Files: loom-code/scripts/external_review.py, loom-code/tests/test_external_review.py, loom-code/skills/external-review/SKILL.md, docs/loom/2026-10-08-unify-independent-external-review/evidence/cli-grounding.md
- Test: A4 positive: agy-absolute-workspace-and-explicit-profile plus Codex initialize clientInfo title; negative: missing-workspace-or-title. A5 positive: supported-command-grounding; negative: rejected-pair-stops.
- Risk: agent-decided — Claude Code's outside review identified missing `agy --add-dir`; local CLI help and the repository's Antigravity instructions establish that print mode needs an absolute workspace path. Official Codex app-server guidance also requires a clientInfo title in initialize.

**W5-03 Recompute outside receipt consistency**  after: W5-02  acceptance: 2, 5
- Files: loom-code/scripts/loom_checker/reviewers.py, loom-code/tests/test_loom_attestation.py, loom-code/skills/closing-review/SKILL.md
- Test: A5 negative: impossible-executor-family-or-evidence-pair-rejected; boundary: observed-model-and-effort-mismatch. A2 positive: legitimate-Claude-receipt-remains-valid.
- Risk: agent-decided — the outside reviewer found that a forged receipt can claim Codex-only observation for Claude; the checker must reject impossible combinations rather than trust caller-supplied fields.

**W5-04 Reject adversarial authorization and CLI contradictions**  after: W5-03  acceptance: 3, 4, 5, 6
- Files: loom-code/scripts/external_review.py, loom-code/scripts/loom_checker/reviewers.py, loom-code/tests/test_external_review.py, loom-code/tests/test_loom_attestation.py, loom-code/tests/test_external_review_adversarial.py, loom-code/skills/external-review/SKILL.md, docs/loom/2026-10-08-unify-independent-external-review/spec.md
- Test: A6 negative: missing authorization source blocks discovery. A4 negative: Claude alias tier mismatch fails; Codex model/list error fails. A5 negative: contradictory Claude receipt fails; legitimate profiles pass.
- Risk: agent-decided — committed adversarial probes exposed three reachable false-success paths; reject them at the shared execution and receipt boundaries.

### Wave 6 — Retain caught W5 probes

**W6-01 Graduate authorization and CLI adversarial probes**  after: W5-04  acceptance: 3, 4, 5, 6
- Files: docs/loom/2026-10-08-unify-independent-external-review/evidence/probes/test_authorization_source.py, docs/loom/2026-10-08-unify-independent-external-review/evidence/probes/test_claude_alias_mismatch.py, docs/loom/2026-10-08-unify-independent-external-review/evidence/probes/test_codex_error_listing.py, loom-code/tests/test_external_review_adversarial.py, loom-code/tests/test_external_review.py
- Test: A6 negative: no authorization blocks subprocess. A4 negative: alias and JSON-RPC errors fail. A5 negative: inconsistent receipt fails. Run graduated tests through the package suite.
- Risk: agent-decided — each new probe caught a real defect, so retaining it under the package test root keeps the regression check active after this change.

### Wave 7 — Close final review routing gaps

**W7-01 Record an outside reviewer when the plan is skipped**  after: W6-01  acceptance: 1, 6
- Files: loom-code/scripts/loom_checker/reviewers.py, loom-code/tests/test_loom_attestation.py, loom-code/tests/test_selection_finalize.py, loom-code/skills/closing-review/SKILL.md
- Test: A1 positive: skipped-plan intent selection raises reviewer floor and requires an outside receipt; negative: no selection retains the floor. A6 positive: direct request remains sufficient.
- Risk: agent-decided — the skill accepts a skipped plan but the checker currently reads selections only from a plan or standing defaults; a committed intent selection keeps the gate recomputable.

**W7-02 Avoid repeating an already named outside choice**  after: W7-01  acceptance: 3, 6
- Files: loom-code/skills/write-plan/references/confirm-intent.md, loom-code/skills/write-plan/references/second-vendor-ask-and-docs-lint.md, loom-code/skills/write-plan/SKILL.md, loom-code/tests/test_write_plan_station_text.py
- Test: A6 positive: direct named agent and target bypass per-change ask; negative: suggestion-only still asks under `second-vendor: ask`. A3 positive: notice stays nonblocking.
- Risk: agent-decided — the standing ask path can duplicate the user's named choice; it should reuse the explicit instruction while retaining a visible disclosure before execution.

## Simplicity check
- Named loom-code skill is the sole executable external-review boundary; duplicated probes and default-model fallback are superseded — taken
- Split release metadata by plugin while retaining all manifest and README mirrors — taken
- Reuse the existing disclosure and receipt fields; add only the checks needed to distinguish an explicit request from a suggestion and to reject impossible execution claims — taken

## Questions asked
① — what — 上述問題與驗收條件是你要的嗎？ 回答「是」也會授權通過審查與發布檢查後，自動推送分支並建立 Ready PR；合併仍由你另行決定，你也可以在發布前明確取消自動發布。

user-decided — second-vendor selection-confirmed: claude

## Risks
1. CLI discovery and result JSON may drift; bounded probes must fail clearly and cannot establish account entitlement for a future run.
2. The current Claude and Antigravity outputs do not independently reveal every effective setting; report requested, accepted and observed evidence separately.
3. CLI working directory does not confine file reads or prove that setup cannot write; the approval record discloses both limits before execution.
4. An explicit user request supplies authorization without second confirmation; quote that request and stop if the provider or review target cannot be determined from it and active context, or the material scope widens.
