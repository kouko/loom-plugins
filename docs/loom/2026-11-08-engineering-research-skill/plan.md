# Engineering research — plan
intent: 2026-11-08-engineering-research-skill@7c1b6042
spec: docs/loom/2026-11-08-engineering-research-skill/spec.md@aa274a9a
charter: 1.1

## Task DAG

W0–W2 below are landed historical tasks. W3 follows the user's explicit
ownership reconfirmation and replaces only their ownership/integration surfaces;
research behavior and completed fix histories remain applicable as the spec's
Requirement continuity section defines.

### Wave 0 — Research capability

**W0-01 Promote question-scoped research instructions** after: none acceptance: 3,4,5,6,7
- Files: loom-workflow/skills/engineering-research/, loom-workflow/tests/engineering-research/
- Test: A3 positive: verified-evidence; negative: false-artifact. A4 positive: mixed-evaluation; boundary: direct-fact. A5 positive: continuation; boundary: changed-conditions. A6 positive: saved-record; negative: no-write. A7 positive: source-path; negative: graph-causality.
- Risk: agent-decided — Follow spec REQ-3 through REQ-7; preserve frozen revision-5 inputs and verify real research outputs rather than prose-only presence.

### Wave 1 — Discovery and finishing ownership

**W1-01 Integrate optional routing and preservation** after: W0-01 acceptance: 1,2,8,9
- Files: loom-workflow/skills/, loom-workflow/tests/, loom-design/skills/capture-intent/SKILL.md, loom-design/skills/write-spec/SKILL.md, loom-code/skills/write-plan/SKILL.md, loom-code/skills/build/SKILL.md, loom-code/skills/ship/SKILL.md, tests/
- Test: A1 positive: isolated-loader; negative: absent-plugin. A2 positive: consequential-small-check; negative: routine-lookup. A8 positive: merged-consented; negative: unpublished-unconsented. A9 positive: actual-record-readback; boundary: untested-host-disclosure.
- Risk: agent-decided — Follow spec REQ-1, REQ-2, REQ-8, REQ-9; use skill-name delegation and isolated fixture Vaults, preserving existing user installations and tests.

### Wave 2 — Registry and release integration

**W2-01 Register and release the bounded capability** after: W1-01 acceptance: 9
- Files: loom-code/contract/manifest.yaml, docs/loom/evidence/mechanisms.yaml, loom-code/scripts/check_mechanisms.py, loom-code/tests/, loom-workflow/tests/scripts/test_skill_count.py, README.md, CHANGELOG.md, **/plugin.json
- Test: A9 positive: synchronized-release; negative: registry-drift. Run manifest synchronization and complete declared package inventory; verify executable budget population and declared exceptions.
- Risk: agent-decided — Follow spec REQ-9; bump affected plugins minor for guidance/contracts, synchronize derived manifests, changelogs and README pins, and admit the counted tool explicitly without a standalone exemption.

### Wave 3 — Confirmed code ownership

**W3-01 Move the research capability and isolate design** after: W2-01 acceptance: 1,2,9
- Files: loom-code/skills/, loom-code/tests/engineering-research/, loom-workflow/skills/, loom-workflow/tests/engineering-research/, loom-design/skills/capture-intent/SKILL.md, loom-design/skills/write-spec/SKILL.md, tests/
- Test: A1 positive: code-only-discovery; negative: design-direct-reference. A2 positive: code-station-handoff; boundary: standalone-engineering. A9 positive: moved-bundle-links; negative: old-owner-copy.
- Risk: agent-decided — Follow revised spec REQ-1; preserve seven runtime files and records, move existing tests, add no-design-reference coverage, retarget code callers and remove workflow routing without a compatibility wrapper.

**W3-02 Align ownership registries and release surfaces** after: W3-01 acceptance: 9
- Files: loom-code/contract/manifest.yaml, docs/loom/evidence/mechanisms.yaml, loom-workflow/tests/scripts/, tests/test_loom_skill_description_catalog.py, README.md, loom-code/, loom-workflow/, loom-design/
- Test: A9 positive: owner-census-release-parity; negative: stale-workflow-registration. Retain prior cap and budget regressions; run complete declared package inventory after integration.
- Risk: agent-decided — Follow revised spec REQ-1 and REQ-9; retain one counted skill/tool, restore design runtime/release surfaces to trunk baseline, and synchronize code/workflow manifests, documentation and tests.

### Wave 4 — User-approved bounded dogfood repair

**W4-01 Make saved-content completion and preservation navigation concrete** after: W3-02 acceptance: 2,3,8,9
- Files: loom-code/skills/engineering-research/SKILL.md, loom-code/skills/engineering-research/references/preservation.md
- Test: Frozen Claude F02/F04/F06 trajectories are behavioral RED for saved-content inspection; F05 for preservation links. Run package invariants and a fresh old/new six-case comparison with independent trajectory judgment. Prose-token assertions cannot establish behavioral GREEN.
- Risk: agent-decided — User approved repair/retest on 2026-11-08. Existing obligations and attempts continue; keep description, methods, framework selection, ownership, schema and historical failed outputs unchanged.

**W4-02 Bound test tools and rerun both versions under identical conditions** after: W4-01 acceptance: 2,3,8,9
- Files: loom-code/tests/local/engineering_research_retest/, docs/loom/2026-11-08-engineering-research-skill/evidence/, docs/skill-dogfood/2026-11-08-code-owned-engineering-research/
- Test: Live boundary checks cover traversal, external paths, symlink escapes and writes; omit command tools. Reuse six prompts/fixtures/rubric; run one fresh old/new pair each with identical confined tools. Two independent revision-blinded auditors inspect trajectories. Preserve earlier native-tool results separately.
- Risk: agent-decided — Confinement is a fixed harness control, not production safety or skill improvement. Six pairs give directional evidence only. Retain first-party Anthropic/OpenAI identities and existing data boundaries; no real Vault, installation, publication, merge or trigger claims.

### Wave 5 — User-approved save-result tool experiment

**W5-01 Prototype one confined save operation with substantive results** after: W4-02 acceptance: 3,8,9
- Files: loom-code/tests/local/engineering_research_save_probe/, docs/loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/, docs/skill-dogfood/2026-11-08-code-owned-engineering-research/
- Test: RED/GREEN tests cover real persisted-body output, local-link results, missing/outside links, unauthorized paths, symlink escapes, no-write, collision and stale updates. Exercise the stdio adapter locally; public native-host control precedes private behavioral runs.
- Risk: agent-decided — User said continue after the save-result proposal. Prototype stays test-local; runtime skill, gate, schema and installations remain unchanged. A complete tool result is evidence availability, not proof the agent inspected it or judged research correctly.

**W5-02 Compare save-result behavior under an unchanged research contract** after: W5-01 acceptance: 3,8,9
- Files: loom-code/tests/local/engineering_research_save_probe/, docs/loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/, docs/skill-dogfood/2026-11-08-code-owned-engineering-research/
- Test: Freeze matched save-confirmation/full-result tools and current skill. Prioritize F04 creation, F01 update, F06 authorized copy; include no-write control. Preserve histories and independent trajectory judgments. Confirm native custom-tool isolation before transmitting private fixtures.
- Risk: agent-decided — This tests a tool intervention, not another prose revision or automatic activation. Preserve W4 residual failures and attempts. No production promotion or external transmission beyond specifically authorized payloads; prepare concrete frozen inputs before any required permission request.

**W5-03 Repair local-probe integration findings without weakening guards** after: W5-01 acceptance: 9
- Files: loom-code/tests/local/engineering_research_retest/prepare_audits.py, loom-code/tests/local/engineering_research_retest/test_harness.py, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py
- Test: Reproduce retired-name scan collision and census unclassified-helper failure. Rename the local masking function consistently; retain frozen history. Let the adversary update its census program for the added helper scope. Re-run focused guards and the complete package runner.
- Risk: agent-decided — These integration failures appeared after earlier local harness files became tracked. Earlier package passes covered their prior tracked inventory only. Preserve failures, frozen W5 dependencies and all original rules; no task-attempt reset or private model retry is implied.

### Wave 6 — Keep unpromoted experiments out of the maintained package

**W6-01 Archive completed local runners and retain only delivery evidence** after: W5-02,W5-03 acceptance: 9
- Files: loom-code/tests/local/engineering_research_retest/, loom-code/tests/local/engineering_research_save_probe/, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py, docs/loom/2026-11-08-engineering-research-skill/evidence/save-result-prototype/, docs/skill-dogfood/2026-11-08-code-owned-engineering-research/
- Test: Verify every tracked runner/helper byte against a deterministic source archive before deleting only those files. Preserve all raw trials. Remove the now-unused exact census admission through its owner; rerun the package runner and existing adversarial tests.
- Risk: agent-decided — Four paired cases did not establish a general research-quality advantage. The helper remains an archived prototype rather than maintained plugin code. Runtime research behavior and requirement/attempt history stay unchanged; archival links disclose historical execution paths.

### Wave 7 — Repair the existing ownership confirmation record

**W7-01 Make the approved ownership confirmation discoverable** after: W6-01 acceptance: 1,9
- Files: docs/loom/intent/2026-11-08-engineering-research-skill.md, docs/loom/2026-11-08-engineering-research-skill/plan.md
- Test: Existing finalize-review correctly rejected the stale canonical confirmation ancestry. Retain that RED; verify the existing intent-version rule against a canonical confirmation commit, run its regression tests and repeat Build's complete suite plus existing adversarial programs before the same reviewers verify the fix.
- Risk: agent-decided — Defect class: noncanonical intent reconfirmation commit title. The whole 983-path branch delta and A1/A9 surfaces were searched; the single live occurrence is ownership commit 7c1b6042, with spec/plan references already pointing to it. Clarify only the intent title's code ownership, recompute its existing content pin and use the required canonical confirmation subject/body. The original user-approved outcome, all nine Acceptance lines, constraints, authorization and confirmation date stay unchanged. This records the already explicit ownership approval; it is no new requirement or confirmation on the user's behalf. The finalization failure and fix consume the next functional digest in the same bounded Review episode, without resetting prior attempts or partial evidence.

## Simplicity check
- none found

## Questions asked
1 — what — 這份範圍與發布安排，可以確認嗎？

## Risks
1. Research guidance is probabilistic; routing and workflow benchmarks must distinguish actual loads from self-reports and explicit invocation from automatic discovery. No universal improvement claim follows from the prototype results.
2. Optional Vault preservation crosses a filesystem/privacy boundary; use temporary fixtures and explicit per-instance consent. No live Vault writes, automatic merge or installed-plugin changes are authorized by this implementation.
3. Existing frozen trial/dogfood directories are pre-existing untracked evidence. Preserve them unchanged; publish only evidence required to support this change, with explicit raw-evidence provenance and limits rather than silently bulk-staging historical sessions.
4. The new counted skill and contract tool increase the mechanism population; record budget-exception lines and executable admission updates, retaining every earlier population and budget regression case.
5. The spec received independent spec+adversarial PASS against da402f1b; engineering exemption applies to decision point ②, and the plan is agent-decided. The next user decision is acceptance after publication checks.
6. W3 changes the ownership and design-integration obligation by explicit user reconfirmation; it does not reopen completed word-cap, portability or archive fixes, reset their attempts, or authorize the still-blocked native-model payload transmission.
7. W4 retains original findings/attempts. Specific provider permissions and explicit repair/retest approval govern this bounded rerun, without provider substitution or broader data collection. Report lack of improvement rather than iterate indefinitely.
8. W5 changes the experimentally manipulated tool result, not the outcome or earlier failed task identity. Keep the same current skill and criteria across arms. If host isolation cannot be established, retain local results and report the untested behavioral boundary.
