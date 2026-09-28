# Compaction essence-dict mapping (W1-08)

Scope: the `test_*_compaction.py` files under `loom-workflow/tests/scripts/`, eight files. The candidate rows for these files come from the container census (W1-07): 439 rows in 16 functions. The rationale is `docs/loom/memory/a-compaction-test-written-from-the-compacted-file-cannot-see-what-left.md`. An `essence` dict, or a phrase list like it, is read off the compacted file. So a rule the compaction dropped is never in it, and the list cannot see the loss it claims to guard. The guard against that loss is a before/after rule diff at review.

Rule applied to every file: an `essence` dict or phrase list goes whole. That includes the field keys, commands and labels inside it, which the census classes structural: they sit in the same presence list and share its defect. What stays: headings and their order, absence checks, word caps, file existence, and every path the dict named, now checked to resolve on disk. A separate structural assert outside a dict also stays (the loom-visualization command block). No function runs a program. No whole file is deleted. Five of these files are whole-file evals in `docs/loom/evidence/mechanisms.yaml` (handoff, recap-state, loom-visualization, git-memory, independent-advisor), and each keeps at least one test.

Rule-3 grep: none of the 16 function names appears in `docs/loom/evidence/mechanisms.yaml`, `AGENTS.md`, `loom-code/tests/test_module_criteria_text.py` or any other file outside these tests and this change's evidence. The `# @req: REQ-n` comments in the independent-advisor functions have no machine consumer (no script parses `@req`), so they went with their functions.

"Docs lens" means the Docs table in `loom-code/skills/closing-review/references/lenses.md`.

## Decisions

One row per function. "delete" removes the function. "prune" removes the dict or phrase list and keeps the rest. Counts are census rows (prose / structural).

| # | file::function | rows | decision | reason |
|---|---|---|---|---|
| 1 | test_critique_compaction.py::test_mode_routing_is_declared_before_either_lens | 0 / 6 | keep-structural | mode tokens `mode: proposal` and `mode: complexity` (the mode field grammar) plus four `## ` headings in order; no dict |
| 2 | test_critique_compaction.py::test_routing_boundaries_survive_the_merge | 0 / 0 | keep-absence | retired skill names must be absent |
| 3 | test_distill_sessions_compaction.py::test_entrypoint_preserves_essence | 0 / 4 | prune | `top.json`, `merged.json`, `--approved` go (phrase list); `references/runtime-protocol.md` and its `is_file` stay. The `--approved` refusal is run by `loom-workflow/tests/distill-sessions/test_apply.py::test_refuses_without_approved_flag` |
| 4 | test_dbt_model_style_compaction.py::test_entrypoint_preserves_scope_structure_and_self_check | 24 / 13 | prune | the seven-group dict goes. Its three pointers (`references/dotstar-passthrough.md`, `checklists/dbt-model-self-check.md`, `scripts/validate_header.py`) stay and are now checked to exist. Re-check of hidden labels: `JOINs ≥2 sources`, `USING (key)`, `Consumer layers`, `YAML frontmatter` are prose phrases, not headings |
| 5 | test_git_memory_compaction.py::test_entrypoint_preserves_invocation_privacy_capture_and_recall | 22 / 14 | prune | the eight-group dict and `CONTRACT_BEHAVIORS` go. The four protocol and standard files it read stay as pointers checked to exist. Trailer keys (`Decision:`, `Gotcha:` and the rest) and recall flags lived only in the phrase list |
| 6 | test_git_memory_compaction.py::test_contract_regression_checks_do_not_pin_whole_file_hashes | 0 / 0 | keep-absence | absence scan over this test's own source |
| 7 | test_handoff_compaction.py::test_entrypoint_preserves_prepare_resume_verification_and_stop | 21 / 24 | prune | the nine-group dict goes. The schema-before-step order checks per mode (anchored on `## Prepare mode` / `## Resume mode` headings and the step labels) and the schema `is_file` stay |
| 8 | test_handoff_compaction.py::test_prepare_mode_names_goal_create | 0 / 3 | prune | the verbatim disclaimer sentence pin (not in the census: a sentence compared with `endswith`, a missed form per P1) goes, with its comment. `loom-workflow:goal-create` inside Prepare mode and absent from Resume mode stays |
| 9 | test_independent_advisor_compaction.py::test_mode_routing_is_bound_to_a_citable_fact | 15 / 6 | delete | only the dict and an `is_file` of the entrypoint remained |
| 10 | test_independent_advisor_compaction.py::test_static_detection_excludes_and_never_claims_verification | 19 / 11 | prune | both dicts go. Kept and renamed: the reference pointers, now checked in the entrypoint and on disk for all three references (it takes over the `is_file` asserts of rows 11-13) |
| 11 | test_independent_advisor_compaction.py::test_three_roles_blind_packet_and_dual_order_judging | 45 / 5 | delete | dicts only; its `dispatch-protocol.md` `is_file` moves to row 10 |
| 12 | test_independent_advisor_compaction.py::test_live_probe_verifies_both_tiers_and_frontier_fails_loud | 22 / 8 | delete | dicts only; the `executor-detection.md` `is_file` is in row 10 |
| 13 | test_independent_advisor_compaction.py::test_report_leads_with_divergence_and_discloses_degradation | 30 / 18 | delete | dicts only; its `report-contract.md` `is_file` moves to row 10 |
| 14 | test_independent_advisor_compaction.py::test_blindness_and_scan_claims_are_bounded_by_scope_boundary | 8 / 1 | delete | dict only |
| 15 | test_independent_advisor_compaction.py::test_single_checkpoint_carries_three_elements_and_egress_disclosure | 29 / 0 | delete | dict only |
| 16 | test_independent_advisor_compaction.py::test_skill_body_stays_under_the_repo_word_cap | 0 / 0 | keep | word cap |
| 17 | test_loom_visualization_compaction.py::test_entrypoint_has_required_sections_and_routes | 0 / 16 | prune | the dict goes, and with it `scripts/detect_client.py --target` and `obsidian:obsidian-mermaid-visualizer`. The frontmatter start and seven `## ` headings stay. Every path the dict named stays, now checked to exist |
| 18 | test_loom_visualization_compaction.py::test_entrypoint_within_word_cap | 0 / 0 | keep | word cap |
| 19 | test_loom_visualization_compaction.py::test_page_mode_preserves_extraction_render_and_fidelity_gates | 14 / 16 | prune | the eight-group dict goes. Re-check of hidden labels: `Fewer than 5` and `Ask once` are prose; `Rejected options`, `Assumptions` and the rest are items of the extraction list. Its two paths (`references/fidelity-check.md`, `assets/cot-report-template.md`) move to row 17's pointer list. The render/verify command block (not a dict) and the `cot-explain` absence stay |
| 20 | test_recap_state_compaction.py::test_entrypoint_preserves_goal_grounded_sections_and_synthesis_gate | 31 / 14 | prune | the seven-group dict goes. The ordered six `### ` template headings, the forbidden-tag absence and the schema `is_file` stay. The start anchor moves from the sentence ``Read `references/seven-block-schema.md` `` to the existing `## What to do` heading followed by the schema path (P2) |

## Mapping

Defect class for every row: a compaction dropped a load-bearing rule from the entrypoint or a reference.

| file::function | defect class it guarded | named replacement | kind |
|---|---|---|---|
| test_distill_sessions_compaction.py::test_entrypoint_preserves_essence | artifact names and the approval flag drop out of the entrypoint | docs lens `omission`; kept structural test `test_distill_sessions_compaction.py::test_entrypoint_points_to_runtime_protocol` (pointer resolves) | review lens dimension |
| test_dbt_model_style_compaction.py::test_entrypoint_preserves_scope_structure_and_self_check | style scope, CTE roles, headers, Redshift rules or the self-check step dropped | docs lens `omission`; kept structural test `test_dbt_model_style_compaction.py::test_entrypoint_pointers_resolve` | review lens dimension |
| test_git_memory_compaction.py::test_entrypoint_preserves_invocation_privacy_capture_and_recall | invocation boundary, privacy stop, capture verification, PR ownership or recall routing dropped, in the entrypoint or its protocols | docs lens `omission`; kept structural test `test_git_memory_compaction.py::test_entrypoint_pointers_resolve` | review lens dimension |
| test_handoff_compaction.py::test_entrypoint_preserves_prepare_resume_verification_and_stop | mode routing, state commands, the ten blocks, resume verification, tier policy or the synthesis stop dropped | docs lens `omission`; kept structural test `test_handoff_compaction.py::test_each_mode_reads_the_schema_before_its_artifact_step` | review lens dimension |
| test_handoff_compaction.py::test_prepare_mode_names_goal_create (disclaimer sentence) | the disclaimer stops saying the user invokes goal-create and Prepare mode never does | docs lens `ambiguity`; kept structural test `test_handoff_compaction.py::test_prepare_mode_names_goal_create` (placement and absence) | review lens dimension |
| test_independent_advisor_compaction.py::test_mode_routing_is_bound_to_a_citable_fact, ::test_three_roles_blind_packet_and_dual_order_judging, ::test_live_probe_verifies_both_tiers_and_frontier_fails_loud, ::test_report_leads_with_divergence_and_discloses_degradation, ::test_blindness_and_scan_claims_are_bounded_by_scope_boundary, ::test_single_checkpoint_carries_three_elements_and_egress_disclosure | mode basis, detection, roles and judging, live probe, report shape, scope boundary or checkpoint rules dropped | docs lens `omission`; kept structural test `test_independent_advisor_compaction.py::test_entrypoint_points_to_references_that_resolve`; word cap `test_independent_advisor_compaction.py::test_skill_body_stays_under_the_repo_word_cap` | review lens dimension |
| test_independent_advisor_compaction.py::test_static_detection_excludes_and_never_claims_verification | exclusion reasons or the static-is-not-verified label dropped | docs lens `omission`; kept structural test `test_independent_advisor_compaction.py::test_entrypoint_points_to_references_that_resolve` | review lens dimension |
| test_loom_visualization_compaction.py::test_entrypoint_has_required_sections_and_routes (dict) | a route to a template, script or reference dropped | kept structural test `test_loom_visualization_compaction.py::test_entrypoint_has_required_sections_and_routes` (each pointer named and existing); word cap `test_loom_visualization_compaction.py::test_entrypoint_within_word_cap` | kept structural test |
| test_loom_visualization_compaction.py::test_page_mode_preserves_extraction_render_and_fidelity_gates | extraction net, early exit, layout, markdown authority, fidelity gate or publish consent dropped | docs lens `omission`; kept structural test `test_loom_visualization_compaction.py::test_page_mode_names_render_and_verify_commands` | review lens dimension |
| test_recap_state_compaction.py::test_entrypoint_preserves_goal_grounded_sections_and_synthesis_gate | routing, output boundary, verbatim preservation, visual thresholds or the synthesis stop dropped | docs lens `omission`; kept structural test `test_recap_state_compaction.py::test_entrypoint_reads_schema_before_the_ordered_six_section_template` | review lens dimension |

## Renames

| old | new |
|---|---|
| test_distill_sessions_compaction.py::test_entrypoint_preserves_essence | test_entrypoint_points_to_runtime_protocol |
| test_dbt_model_style_compaction.py::test_entrypoint_preserves_scope_structure_and_self_check | test_entrypoint_pointers_resolve |
| test_git_memory_compaction.py::test_entrypoint_preserves_invocation_privacy_capture_and_recall | test_entrypoint_pointers_resolve |
| test_handoff_compaction.py::test_entrypoint_preserves_prepare_resume_verification_and_stop | test_each_mode_reads_the_schema_before_its_artifact_step |
| test_independent_advisor_compaction.py::test_static_detection_excludes_and_never_claims_verification | test_entrypoint_points_to_references_that_resolve |
| test_loom_visualization_compaction.py::test_page_mode_preserves_extraction_render_and_fidelity_gates | test_page_mode_names_render_and_verify_commands |
| test_recap_state_compaction.py::test_entrypoint_preserves_goal_grounded_sections_and_synthesis_gate | test_entrypoint_reads_schema_before_the_ordered_six_section_template |

Orphans removed: `CONTRACT_BEHAVIORS` (git-memory) and `DETECTION_PATH`, `DISPATCH_PATH`, `REPORT_PATH` (independent-advisor, replaced by the `REFERENCES` tuple).

## Classifier after the edit

`--candidates` lists 0 prose candidates in these eight files. Classes: critique, handoff and recap-state are `structure`. distill-sessions and loom-visualization are `structure` by override row. dbt-model-style, git-memory and independent-advisor are now `other`, because the classifier has no pattern for a pointer-resolve loop. The distill-sessions override reason still names `top.json`, `merged.json` and `--approved`, which this task removed. Both go to W2-01 (P5: this task does not edit the classifier).
