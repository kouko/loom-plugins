# Census Report — Prose-Pin Stock Cleanup (W0-01, regenerated in the end-of-Build fix round)

Regenerated in the end-of-Build fix round at HEAD of branch `engineering/2026-09-27-prose-pin-stock-cleanup` (2026-09-28), from
`python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py`.
Total test files scanned: 234

## Per-Class Counts

| Class | Count |
|-------|-------|
| behavior | 111 |
| gate-eval | 5 |
| grammar-invariant | 5 |
| not-prose | 58 |
| other | 13 |
| sentence-pin | 0 |
| structure | 42 |

## Full Per-File Classification

| File | Class | Secondary Markers |
|------|-------|-------------------|
| loom-code/tests/test_acceptance_test_report_shape.py | grammar-invariant | has_pins=yes, note=mixed-grammar-and-pin |
| loom-code/tests/test_adversarial_agy_adapter.py | behavior | has_pins=no |
| loom-code/tests/test_adversarial_agy_anchor_turns.py | behavior | has_pins=no |
| loom-code/tests/test_adversarial_auto_skip_portability.py | behavior | has_pins=no |
| loom-code/tests/test_adversarial_bare_script_lint.py | behavior | has_pins=no |
| loom-code/tests/test_adversarial_blocked_publish_routes.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-code/tests/test_adversarial_narrow_delta_waiver.py | behavior | has_pins=no |
| loom-code/tests/test_adversarial_plugin_root_marker.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-code/tests/test_adversarial_version_metadata_sync.py | behavior | has_pins=no |
| loom-code/tests/test_adversary_layout.py | behavior | has_pins=no |
| loom-code/tests/test_adversary_protocol.py | behavior | has_pins=yes |
| loom-code/tests/test_adversary_recipe_shape.py | structure | auto=sentence-pin, override=structure, reason=split_sentences feeds a duplicate-sentence check across recipe files; no prose literal is asserted, has_pins=yes |
| loom-code/tests/test_adversary_routing.py | behavior | has_pins=yes |
| loom-code/tests/test_agent_model_frontmatter.py | structure |  |
| loom-code/tests/test_agy_adapter.py | behavior | has_pins=no |
| loom-code/tests/test_architecture_doc_consumers.py | structure |  |
| loom-code/tests/test_build_mechanical_checks.py | behavior | has_pins=yes |
| loom-code/tests/test_build_recovery_rules.py | gate-eval | has_pins=yes |
| loom-code/tests/test_check_contract_citations.py | behavior | has_pins=no |
| loom-code/tests/test_check_doc_citations.py | behavior | has_pins=no |
| loom-code/tests/test_check_mechanisms.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-code/tests/test_closing_review_recovery_rules.py | gate-eval | has_pins=yes |
| loom-code/tests/test_coldread_role_split.py | behavior | has_pins=no |
| loom-code/tests/test_contract_manifest.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-code/tests/test_dispatch_profile_contract.py | gate-eval | has_pins=yes |
| loom-code/tests/test_dispatch_profile_resolver.py | behavior | has_pins=no |
| loom-code/tests/test_expert_mode_skill.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_fix_handoff_text.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_fix_scope_text.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_hooks_json.py | behavior | has_pins=no |
| loom-code/tests/test_kickoff_defaults_grammar.py | behavior | has_pins=no |
| loom-code/tests/test_land_merge.py | behavior | has_pins=no |
| loom-code/tests/test_language_anchor_hook.py | behavior | has_pins=no |
| loom-code/tests/test_legacy_contract_removed.py | behavior | has_pins=no |
| loom-code/tests/test_lenses_deletion_first.py | grammar-invariant | has_pins=yes, note=mixed-grammar-and-pin |
| loom-code/tests/test_loom_attestation.py | behavior | has_pins=no |
| loom-code/tests/test_loom_checker_cli.py | behavior | has_pins=no |
| loom-code/tests/test_loom_checker_intake.py | behavior | has_pins=no |
| loom-code/tests/test_loom_checker_intent.py | behavior | has_pins=no |
| loom-code/tests/test_loom_checker_standing.py | behavior | has_pins=no |
| loom-code/tests/test_loom_publish.py | behavior | has_pins=no |
| loom-code/tests/test_one_way_door_copies.py | structure |  |
| loom-code/tests/test_package_tests_command.py | structure |  |
| loom-code/tests/test_plan_field_caps.py | behavior | has_pins=no |
| loom-code/tests/test_plan_simplicity_text.py | behavior | has_pins=yes |
| loom-code/tests/test_pr_floor.py | behavior | has_pins=no |
| loom-code/tests/test_probes_charter_charter.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_branch_end.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_run_status.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_runner.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_scoring.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_wave1.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_wave1_fix.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_baselines_four_dirs_n10_sonnet.py | structure |  |
| loom-code/tests/test_probes_coldread_changelog_carries_1_5_1.py | structure |  |
| loom-code/tests/test_probes_coldread_readme_role_section_has_three_way_paragraph.py | structure |  |
| loom-code/tests/test_probes_cumulative_boundary_reassessment.py | behavior | has_pins=no |
| loom-code/tests/test_probes_language_policy.py | structure |  |
| loom-code/tests/test_probes_replaceable_boundary_behavior.py | behavior | has_pins=no |
| loom-code/tests/test_prose_pin_rule_text.py | grammar-invariant | has_pins=no |
| loom-code/tests/test_publish_command_detection.py | behavior | has_pins=no |
| loom-code/tests/test_readme_review_order.py | structure |  |
| loom-code/tests/test_review_convergence_contract.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_reviewer_mechanical_evidence.py | grammar-invariant | has_pins=yes, note=mixed-grammar-and-pin |
| loom-code/tests/test_second_vendor_policy.py | behavior | has_pins=no |
| loom-code/tests/test_selection_finalize.py | behavior | has_pins=no |
| loom-code/tests/test_selection_guard.py | behavior | has_pins=no |
| loom-code/tests/test_session_start_words.py | behavior | has_pins=no |
| loom-code/tests/test_ship_station_text.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_ship_worktree_merge.py | behavior | has_pins=no |
| loom-code/tests/test_simplified_station_text.py | behavior | has_pins=yes |
| loom-code/tests/test_sync_before_review_text.py | behavior | has_pins=yes |
| loom-code/tests/test_sync_codex_manifest.py | behavior | has_pins=no |
| loom-code/tests/test_test_budget_text.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_verification_status.py | behavior | has_pins=no |
| loom-code/tests/test_write_plan_shape_text.py | grammar-invariant | has_pins=yes, note=mixed-grammar-and-pin |
| loom-code/tests/test_write_plan_station_text.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-workflow/tests/decision-map/test_check_map_fog.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_check_map_links.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_delivery_binding.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_delivery_evidence.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_governance_ratification.py | structure |  |
| loom-workflow/tests/decision-map/test_map_init.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_map_module_boundaries.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_map_progress.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_map_store.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_map_transaction.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_migrate_map_v3.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_skill_doc.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-workflow/tests/decision-map/test_start_delivery.py | behavior | has_pins=no |
| loom-workflow/tests/distill-sessions/test_apply.py | behavior | has_pins=no |
| loom-workflow/tests/distill-sessions/test_main.py | behavior | has_pins=no |
| loom-workflow/tests/distill-sessions/test_main_e2e.py | behavior | has_pins=no |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py | structure |  |
| loom-workflow/tests/distill-sessions/test_propose.py | behavior | has_pins=no |
| loom-workflow/tests/distill-sessions/test_report.py | behavior | has_pins=no |
| loom-workflow/tests/git-memory/test_loom_delegation.py | structure |  |
| loom-workflow/tests/git-memory/test_memory_grep_version.py | structure |  |
| loom-workflow/tests/git-memory/test_privacy_scan.py | behavior | has_pins=no |
| loom-workflow/tests/git-memory/test_probes_memory_grep_render.py | behavior | has_pins=no |
| loom-workflow/tests/git-memory/test_probes_memory_grep_single_pass.py | behavior | has_pins=no |
| loom-workflow/tests/goal-create/test_goal_lint.py | behavior | has_pins=no |
| loom-workflow/tests/goal-create/test_goal_shape.py | structure |  |
| loom-workflow/tests/goal-create/test_readmes.py | structure |  |
| loom-workflow/tests/goal-create/test_skill_md.py | gate-eval | has_pins=yes |
| loom-workflow/tests/handoff/test_handoff_readmes.py | structure |  |
| loom-workflow/tests/handoff/test_handoff_schema.py | structure |  |
| loom-workflow/tests/handoff/test_handoff_skill_md.py | structure |  |
| loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py | structure |  |
| loom-workflow/tests/loom-memory/test_loom_memory.py | behavior | has_pins=no |
| loom-workflow/tests/loom-memory/test_migrate_legacy_store.py | behavior | has_pins=no |
| loom-workflow/tests/loom-memory/test_skill_contract.py | behavior | has_pins=no |
| loom-workflow/tests/loom-visualization/test_adversarial_probes.py | behavior | has_pins=no |
| loom-workflow/tests/loom-visualization/test_detect_client.py | behavior | has_pins=no |
| loom-workflow/tests/loom-visualization/test_references.py | structure |  |
| loom-workflow/tests/loom-visualization/test_skill_script_paths.py | behavior | has_pins=no |
| loom-workflow/tests/loom-visualization/test_templates.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-workflow/tests/recap-state/test_readmes.py | structure |  |
| loom-workflow/tests/recap-state/test_seven_block_schema.py | structure |  |
| loom-workflow/tests/recap-state/test_skill_md.py | structure |  |
| loom-workflow/tests/scripts/test_adversarial_description_ab_probes.py | behavior | has_pins=no |
| loom-workflow/tests/scripts/test_adversarial_hook_probes.py | behavior | has_pins=no |
| loom-workflow/tests/scripts/test_adversarial_visualization_card_hosts.py | behavior | has_pins=no |
| loom-workflow/tests/scripts/test_critique_compaction.py | gate-eval | has_pins=yes |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_git_memory_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_handoff_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_independent_advisor_plugin_readmes.py | structure |  |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_no_live_cot_explain_references.py | behavior | has_pins=no |
| loom-workflow/tests/scripts/test_readme_card_timing.py | structure |  |
| loom-workflow/tests/scripts/test_recap_state_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_release_metadata.py | structure |  |
| loom-workflow/tests/scripts/test_validate_skill_folder_structure_hook.py | behavior | has_pins=no |
| loom-workflow/tests/scripts/test_visualization_card_hook.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-workflow/tests/test_loom_visualization_page_scripts.py | behavior | has_pins=no |
| tests/hooks/test_check_codex_manifest_drift.py | behavior | has_pins=no |
| tests/hooks/test_check_memory_store_integrity.py | behavior | has_pins=no |
| tests/hooks/test_remind_memory_mirror.py | behavior | has_pins=no |
| tests/test_adversarial_agy_rule_sync.py | behavior | has_pins=no |
| tests/test_agy_install_docs.py | structure |  |
| tests/test_check_plugin_boundaries.py | behavior | has_pins=no |
| tests/test_loom_plugin_install_layout.py | behavior | has_pins=no |
| tests/test_loom_skill_description_catalog.py | structure |  |
| tests/test_run_package_tests.py | behavior | has_pins=no |
| tests/test_state_anchor_carrier_inventory.py | behavior | has_pins=no |
| tests/test_sync_codex_manifests.py | behavior | has_pins=no |
| tests/test_tests_folder_convention.py | behavior | has_pins=no |
| loom-design/tests/architecture-design/test_abuse_architecture_validator.py | structure |  |
| loom-design/tests/architecture-design/test_architecture_skill.py | structure |  |
| loom-design/tests/architecture-design/test_validate_architecture_output.py | behavior | has_pins=no |
| loom-design/tests/interface/test_design_md_schema_keys.py | behavior | has_pins=no |
| loom-design/tests/interface/test_design_system_skill.py | structure |  |
| loom-design/tests/interface/test_knowledge_triage.py | behavior | has_pins=no |
| loom-design/tests/interface/test_north_star_purpose_retarget.py | structure |  |
| loom-design/tests/interface/test_validate_design_output.py | structure |  |
| loom-design/tests/principles/test_principles_checker_parity.py | behavior | has_pins=no |
| loom-design/tests/principles/test_principles_ratified_line.py | structure |  |
| loom-design/tests/principles/test_validate_principles_output.py | structure |  |
| loom-design/tests/spec/test_capture_intent_contract.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-design/tests/spec/test_write_spec_contract.py | behavior | has_pins=yes, marker=grammar-invariant-content |

## Spot-Check Verification (≥8 files)

| File | Expected | Actual | Notes |
|------|----------|--------|-------|
| loom-code/tests/test_agy_tool_mapping.py | sentence-pin (has_pins=yes) | deleted (W1) | Pure prose pin, deleted in this batch; not in the census at HEAD |
| loom-code/tests/test_write_plan_shape_text.py | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | Tests gate marker grammar (<!-- gate: -->), also pins station prose ✅ |
| loom-code/tests/test_loom_checker_intake.py | behavior (has_pins=no) | behavior (has_pins=no) | Executes loom_checker.py via subprocess, asserts on returncode ✅ |
| loom-code/tests/test_selection_store.py | not-prose () | not-prose () | No .md references — pure git/selection store logic ✅ |
| loom-code/tests/test_prose_pin_rule_text.py | grammar-invariant (has_pins=no) | grammar-invariant (has_pins=no) | Tests prose_pin matcher rules in adversary.md & engineering-baseline.md ✅ |
| loom-code/tests/test_lenses_deletion_first.py | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | Tests negation matcher self-tests (baseline §8) — imports prose_pin, has sentence assertions, has_pins=yes ✓ |
| loom-code/tests/test_write_plan_station_text.py | behavior (has_pins=yes) | behavior (has_pins=yes, marker=grammar-invariant-content) | Executes loom_checker.py, pins exact station prose sentences ✅ |
| loom-code/tests/test_simplified_station_text.py | behavior (has_pins=yes) | behavior (has_pins=yes) | Executes loom_checker.py, pins simplified station prose ✅ |
| loom-code/tests/test_package_tests_command.py | structure () | structure () | Only asserts on document shape (frontmatter, sections, gate markers) ✅ |
| loom-code/tests/test_adversary_routing.py | behavior (has_pins=yes) | behavior (has_pins=yes) | Executes pytest inside copied repos, asserts returncode, also pins prose ✅ |
| loom-workflow/tests/scripts/test_critique_compaction.py | gate-eval (has_pins=yes) | gate-eval (has_pins=yes) | Pruned in W1; still pins sentences but is named by a mechanisms.yaml `eval:`, so reclassified gate-eval (W3-02); batch 2 |
| loom-workflow/tests/scripts/test_goal_create_compaction.py | sentence-pin (has_pins=yes) | deleted (W1) | Compaction pin file, deleted in this batch; not in the census at HEAD |
| loom-workflow/tests/handoff/test_handoff_skill_md.py | structure () | structure () | Compaction test: checks structural elements (key presence in dictionaries) ✅ |
| loom-workflow/tests/scripts/test_recap_state_compaction.py | structure () | structure () | Compaction test: checks document shape (frontmatter, sections, headings) ✅ |
| loom-workflow/tests/loom-memory/test_skill_contract.py | behavior (has_pins=no) | behavior (has_pins=no) | Runs subprocess git ls-files, binds .stdout to staged variable, asserts on returncode ✅ |
| loom-workflow/tests/decision-map/test_delivery_binding.py | behavior (has_pins=no) | behavior (has_pins=no) | Imports delivery_binding production module (scripts/), validates ticket/brief bindings with repo I/O ✅ |
| loom-code/tests/test_adversary_recipe_shape.py | structure (override) | structure (auto=sentence-pin, override=structure) | Manual override, see Classifier corrections: split_sentences feeds a duplicate-sentence check across recipe files; no prose literal asserted |
| loom-code/tests/test_adversary_recipe_code.py | other | other (not in the table) | Was grammar-invariant only through an appended comment; the pin tables are deleted, and what is left (case-class table cells, one-home check) matches no STRUCTURE signal |

## Classifier corrections in the fix round

The end-of-Build adversary showed the earlier zero came partly from comments. Corrections, each applied to every file:

- **Comment stripping.** `#` comments are removed (tokenize) before any signal is matched, so no comment can change a class. Docstrings are kept: stripping them reclassifies 15 unrelated files (none into sentence-pin), a wider change than this round.
- **Reader-call signals removed.** `_flat(`, `flat_prose(` and `rule_prose(` no longer count as sentence assertions: a reader call asserts nothing, and a literal asserted on its result is still caught by the `assert ... in "literal"` alternative. Moves: `test_adversary_recipe_code.py`, `_skill_gate.py`, `_spec.py` sentence-pin → other.
- **Heading-literal exemption.** An `assert "#..." in ...` literal (heading presence) is structure, not a pin.
- **`split_sentences(` kept.** Removing it moved `test_build_recovery_rules.py` and `test_closing_review_recovery_rules.py` from gate-eval to structure, yet both really pin phrases (`_require` phrase lists, exact paragraph endings) in a form no other signal sees; that part was reverted.
- **One manual override** (`MANUAL_OVERRIDES` in the classifier, printed as `auto=…, override=…`): `loom-code/tests/test_adversary_recipe_shape.py` → structure, because split_sentences feeds a duplicate-sentence check across recipe files and no prose literal is asserted.

Also in this round: the appended `# prose_pin matcher self-test` comments were removed from the four recipe modules, and their leftover pin tables and synthetic pin tests deleted.

## Removed sentence-pin tests → replacement evidence

Dispositions are the net diff against base `946e06d1`. Review-lens facets are the `docs` lens facets in `loom-code/agents/reviewer.md` (defined in `loom-code/skills/closing-review/references/lenses.md`); `a.py::f` names one test function.

| File | Disposition | What the pins guarded | Replacement evidence |
| :--- | :--- | :--- | :--- |
| `loom-code/tests/test_adversary_recipe_code.py` | pruned (`test_recipe_affirms_the_rule`, `test_recipe_states_the_rule` + 2 helper self-tests) | Code-recipe rules stated in the recipe | `test_adversary_layout.py::test_every_original_rule_is_still_stated_verbatim`; `test_adversary_recipe_code.py::test_recipe_names_every_class_to_draw_cases_from`; lens facet `omission` |
| `loom-code/tests/test_adversary_recipe_shape.py` | unchanged (net diff vs `946e06d1` empty; edited in 45bd949d, restored in e4ec2437) | nothing removed | none needed |
| `loom-code/tests/test_adversary_recipe_skill_gate.py` | pruned (`test_recipe_affirms_the_rule` + 1 helper self-test) | Skill-and-gate recipe rules stated in the recipe | `test_adversary_recipe_skill_gate.py::test_procedure_sentence_in_both_files_rejected`; `test_adversary_layout.py::test_no_kind_rule_appears_outside_its_own_file`; lens facet `omission` |
| `loom-code/tests/test_adversary_recipe_spec.py` | pruned (`test_recipe_affirms_the_rule`, `test_recipe_states_the_rule` + 2 helper self-tests) | Spec recipe rules stated in the recipe | `test_adversary_recipe_spec.py::test_procedure_sentence_in_both_files_rejected`; `test_adversary_layout.py::test_no_kind_rule_appears_outside_its_own_file`; lens facet `omission` |
| `loom-code/tests/test_adversary_routing.py` | pruned (`test_a_reworded_recipe_is_not_blamed_on_the_addition`, `test_first_planting_fails_when_nothing_was_planted_synthetic`) | A recipe reword must redden only that recipe's own pin test | `test_adversary_routing.py::test_a_reworded_recipe_plants_no_failure_for_the_addition_to_be_judged_on`; `test_adversary_routing.py::test_reword_plants_when_prose_pin_exists_synthetic` |
| `loom-code/tests/test_agy_tool_mapping.py` | deleted | AgY reference names the right tools, station pointers resolve | `test_check_skill_crossrefs.py::test_missing_backtick_path_is_reported` (pointer resolution); lens facet `incorrect-fact` (tool names, role dispatch) |
| `loom-code/tests/test_dispatch_profile_contract.py` | pruned (6 functions) | Profile prose: atomic fallback, five effort tiers, sequential escalation, final redispatch routed | `test_dispatch_profile_resolver.py::test_selected_model_pair_is_checked_atomically`, `::test_all_five_portable_efforts_can_be_inherited`, `::test_reasoning_escalation_is_sequential_and_uses_shared_budget`, `::test_final_allowed_execution_success_is_routed`; `test_dispatch_profile_contract.py::test_stations_do_not_restate_the_resolver_invocation` |
| `loom-code/tests/test_module_criteria_text.py` | deleted | AGENTS.md states the four module criteria, each with a check | `test_adversary_routing.py::test_adding_a_kind_is_one_file_and_one_row` (add), `::test_adding_a_kind_leaves_every_existing_recipe_file_untouched` (change), `::test_removing_a_kind_routed_today_leaves_no_reference` (remove); `test_adversary_layout.py::test_no_kind_rule_appears_outside_its_own_file` (locate); lens facet `ambiguity` |
| `loom-workflow/tests/goal-create/test_input_floor.py` | deleted | Goal input floor: slot names, bar clause, provenance tags | `test_goal_lint.py::test_floor_fails_structure_and_warns_on_judgment`; `test_goal_lint.py::test_field_labels_match_the_shape_reference`; `test_goal_shape.py::test_defines_four_fields_budget_and_surfacing` |
| `loom-workflow/tests/goal-create/test_skill_md.py` | pruned (9 functions) | Goal-create session and activation prose | `test_skill_md.py::test_session_activation_rules_are_one_registered_gate`; `test_skill_md.py::test_invocation_section_counts_the_offer_sites_that_exist`; lens facet `inconsistency` |
| `loom-workflow/tests/scripts/test_critique_compaction.py` | pruned (`test_shared_discipline_is_stated_once`) | Shared discipline stated once in critique SKILL.md | `test_critique_compaction.py::test_routing_boundaries_survive_the_merge`; lens facet `inconsistency` |
| `loom-workflow/tests/scripts/test_goal_create_compaction.py` | deleted | Goal-create entrypoint keeps modes, floor, invocation | `test_skill_md.py::test_declares_two_modes_and_conditional_arc`, `::test_floor_invocation_line_names_the_script`, `::test_invocation_section_counts_the_offer_sites_that_exist` |
| `loom-code/tests/test_principles_amendment.py` | deleted (W4-02) | PRINCIPLES.md non-negotiable 2 sentences and the exact ratified-by line | `tests/test_principles_ratification.py::test_ratified_by_names_2026_09_15_non_negotiable_2_amendment` (log entry); checker rule `standing.product-principles-reject` (signature grammar); lens facet `omission` (the wording) |
| `loom-code/tests/test_ship_guidance_presence.py` | deleted (W4-02) | Ship SKILL.md table and no-inline-list guidance sentences | lens facet `omission` |

### W4-02 deletion list (written before deleting)

Both are pure sentence pins: they assert prose wording, execute nothing, carry no `mechanisms.yaml` `eval:`, and no test or script imports or reads them (repo grep; the only hits are historical plans, attestations and evidence of earlier changes).

- `loom-code/tests/test_principles_amendment.py` — exact-sentence and exact-line equality on PRINCIPLES.md (lines 58–65); nothing executed.
- `loom-code/tests/test_ship_guidance_presence.py` — two `target in content` sentence checks on ship SKILL.md, opened by a cwd-relative path; nothing executed.

Not deleted, though acceptance testing named it a likely pure pin: `loom-code/tests/test_codex_hook_trust_contract.py` is the `eval:` of `write-plan.codex-installed-hook-trust-boundary` in `mechanisms.yaml`, so it is gate-eval and goes to batch 2.

## A5 executable test count

Test functions (`test*`) under the four test roots whose own body carries the classifier's execution signal (`executes()`, the same patterns that mark a file `behavior`), counted per function.

| Tree | Count |
|------|-------|
| base `6f3acd78` (pre-cleanup) | 727 |
| HEAD | 728 |

HEAD >= base. A per-function name diff of the two trees shows no function disappeared; the one addition is `loom-code/tests/test_adversary_routing.py::test_reword_plants_when_prose_pin_exists_synthetic`.

Commands (from the repo root; `<scratch>` is any directory outside the repo):

```
mkdir -p <scratch>/base && git archive 6f3acd78 | tar -x -C <scratch>/base
python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --count-exec <scratch>/base
python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --count-exec .
```

## Batch 2 (deferred)

Files that still carry sentence pins after this batch, left for a second batch (intent A2/A4 as amended). Gate-eval files (5): named by a `docs/loom/evidence/mechanisms.yaml` `eval:` value, so they are a gate's execution evidence.

- `loom-code/tests/test_build_recovery_rules.py` — gate-eval
- `loom-code/tests/test_closing_review_recovery_rules.py` — gate-eval
- `loom-code/tests/test_dispatch_profile_contract.py` — gate-eval
- `loom-workflow/tests/goal-create/test_skill_md.py` — gate-eval
- `loom-workflow/tests/scripts/test_critique_compaction.py` — gate-eval

Behavior files with `has_pins=yes` (15): they execute programs and also pin sentences.

- `loom-code/tests/test_adversary_protocol.py` — behavior, has_pins=yes
- `loom-code/tests/test_adversary_routing.py` — behavior, has_pins=yes
- `loom-code/tests/test_build_mechanical_checks.py` — behavior, has_pins=yes
- `loom-code/tests/test_expert_mode_skill.py` — behavior, has_pins=yes
- `loom-code/tests/test_fix_handoff_text.py` — behavior, has_pins=yes
- `loom-code/tests/test_fix_scope_text.py` — behavior, has_pins=yes
- `loom-code/tests/test_plan_simplicity_text.py` — behavior, has_pins=yes
- `loom-code/tests/test_review_convergence_contract.py` — behavior, has_pins=yes
- `loom-code/tests/test_ship_station_text.py` — behavior, has_pins=yes
- `loom-code/tests/test_simplified_station_text.py` — behavior, has_pins=yes
- `loom-code/tests/test_sync_before_review_text.py` — behavior, has_pins=yes
- `loom-code/tests/test_test_budget_text.py` — behavior, has_pins=yes
- `loom-code/tests/test_write_plan_station_text.py` — behavior, has_pins=yes
- `loom-design/tests/spec/test_capture_intent_contract.py` — behavior, has_pins=yes
- `loom-design/tests/spec/test_write_spec_contract.py` — behavior, has_pins=yes
