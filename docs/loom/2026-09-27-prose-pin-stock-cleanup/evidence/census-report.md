# Census Report — Prose-Pin Stock Cleanup (W0-01)

Generated: 2026-09-28
Total test files scanned: 238

## Per-Class Counts

| Class | Count |
|-------|-------|
| behavior | 112 |
| grammar-invariant | 4 |
| not-prose | 58 |
| other | 10 |
| sentence-pin | 13 |
| structure | 41 |

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
| loom-code/tests/test_adversary_recipe_code.py | sentence-pin | has_pins=yes |
| loom-code/tests/test_adversary_recipe_shape.py | sentence-pin | has_pins=yes |
| loom-code/tests/test_adversary_recipe_skill_gate.py | sentence-pin | has_pins=yes |
| loom-code/tests/test_adversary_recipe_spec.py | sentence-pin | has_pins=yes |
| loom-code/tests/test_adversary_routing.py | behavior | has_pins=yes |
| loom-code/tests/test_agent_model_frontmatter.py | structure |  |
| loom-code/tests/test_agy_adapter.py | behavior | has_pins=no |
| loom-code/tests/test_agy_tool_mapping.py | sentence-pin | has_pins=yes |
| loom-code/tests/test_architecture_doc_consumers.py | structure |  |
| loom-code/tests/test_build_mechanical_checks.py | behavior | has_pins=yes |
| loom-code/tests/test_build_recovery_rules.py | sentence-pin | has_pins=yes |
| loom-code/tests/test_check_contract_citations.py | behavior | has_pins=no |
| loom-code/tests/test_check_doc_citations.py | behavior | has_pins=no |
| loom-code/tests/test_check_mechanisms.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-code/tests/test_closing_review_recovery_rules.py | sentence-pin | has_pins=yes |
| loom-code/tests/test_coldread_role_split.py | behavior | has_pins=no |
| loom-code/tests/test_contract_manifest.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-code/tests/test_dispatch_profile_contract.py | sentence-pin | has_pins=yes |
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
| loom-code/tests/test_module_criteria_text.py | sentence-pin | has_pins=yes |
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
| loom-code/tests/test_prose_pin_rule_text.py | behavior | has_pins=no, marker=grammar-invariant-content |
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
| loom-workflow/tests/goal-create/test_input_floor.py | sentence-pin | has_pins=yes |
| loom-workflow/tests/goal-create/test_readmes.py | structure |  |
| loom-workflow/tests/goal-create/test_skill_md.py | sentence-pin | has_pins=yes |
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
| loom-workflow/tests/scripts/test_critique_compaction.py | sentence-pin | has_pins=yes |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_git_memory_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_goal_create_compaction.py | sentence-pin | has_pins=yes |
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
| loom-code/tests/test_agy_tool_mapping.py | sentence-pin (has_pins=yes) | sentence-pin (has_pins=yes) | Pure prose pin: imports prose_pin, has sentence assertions, no execution ✅ |
| loom-code/tests/test_write_plan_shape_text.py | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | Tests gate marker grammar (<!-- gate: -->), also pins station prose ✅ |
| loom-code/tests/test_loom_checker_intake.py | behavior (has_pins=no) | behavior (has_pins=no) | Executes loom_checker.py via subprocess, asserts on returncode ✅ |
| loom-code/tests/test_selection_store.py | not-prose () | not-prose () | No .md references — pure git/selection store logic ✅ |
| loom-code/tests/test_prose_pin_rule_text.py | grammar-invariant (has_pins=no) | grammar-invariant (has_pins=no) | Tests prose_pin matcher rules in adversary.md & engineering-baseline.md ✅ |
| loom-code/tests/test_lenses_deletion_first.py | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | Tests negation matcher self-tests (baseline §8) — imports prose_pin, has sentence assertions, has_pins=yes ✓ |
| loom-code/tests/test_write_plan_station_text.py | behavior (has_pins=yes) | behavior (has_pins=yes, marker=grammar-invariant-content) | Executes loom_checker.py, pins exact station prose sentences ✅ |
| loom-code/tests/test_simplified_station_text.py | behavior (has_pins=yes) | behavior (has_pins=yes) | Executes loom_checker.py, pins simplified station prose ✅ |
| loom-code/tests/test_package_tests_command.py | structure () | structure () | Only asserts on document shape (frontmatter, sections, gate markers) ✅ |
| loom-code/tests/test_adversary_routing.py | behavior (has_pins=yes) | behavior (has_pins=yes) | Executes pytest inside copied repos, asserts returncode, also pins prose ✅ |
| loom-workflow/tests/scripts/test_critique_compaction.py | sentence-pin (has_pins=yes) | sentence-pin (has_pins=yes) | Compaction test: pins exact sentences from merged critique skill ✅ |
| loom-workflow/tests/scripts/test_goal_create_compaction.py | sentence-pin (has_pins=yes) | sentence-pin (has_pins=yes) | Compaction test: pins exact sentences from goal-create skill ✅ |
| loom-workflow/tests/handoff/test_handoff_skill_md.py | structure () | structure () | Compaction test: checks structural elements (key presence in dictionaries) ✅ |
| loom-workflow/tests/scripts/test_recap_state_compaction.py | structure () | structure () | Compaction test: checks document shape (frontmatter, sections, headings) ✅ |
| loom-workflow/tests/loom-memory/test_skill_contract.py | behavior (has_pins=no) | behavior (has_pins=no) | Runs subprocess git ls-files, binds .stdout to staged variable, asserts on returncode ✅ |
| loom-workflow/tests/decision-map/test_delivery_binding.py | behavior (has_pins=no) | behavior (has_pins=no) | Imports delivery_binding production module (scripts/), validates ticket/brief bindings with repo I/O ✅ |

## Removed sentence-pin tests → replacement evidence

| File | Disposition | What the pins guarded | Replacement evidence |
| :--- | :--- | :--- | :--- |
| `loom-code/tests/test_adversary_recipe_code.py` | pruned | Prose recipe rules for adversary | Structural tests + review lens: omission |
| `loom-code/tests/test_adversary_recipe_shape.py` | pruned | Prose recipe shape for adversary | Structural tests + review lens: omission |
| `loom-code/tests/test_adversary_recipe_skill_gate.py` | pruned | Prose recipe gates for adversary | Structural tests + review lens: omission |
| `loom-code/tests/test_adversary_recipe_spec.py` | pruned | Prose recipe spec for adversary | Structural tests + review lens: omission |
| `loom-code/tests/test_adversary_routing.py` | pruned | Reword-planting assertion | Reword-planting guard |
| `loom-code/tests/test_agy_tool_mapping.py` | deleted | Reference mapping to AgY tools | Review lens: incorrect-fact |
| `loom-code/tests/test_dispatch_profile_contract.py` | pruned | Dispatch profile prose contract | Structural tests + review lens: incorrect-fact |
| `loom-code/tests/test_module_criteria_text.py` | deleted | Modular split criteria | Checker rules + review lens: ambiguity |
| `loom-workflow/tests/goal-create/test_input_floor.py` | deleted | Input slot names contract | Structural tests |
| `loom-workflow/tests/goal-create/test_skill_md.py` | pruned | Goal-create input prose pins | Structural tests + review lens: inconsistency |
| `loom-workflow/tests/scripts/test_critique_compaction.py` | pruned | Critique skill compaction | Structural tests + review lens: omission |
| `loom-workflow/tests/scripts/test_goal_create_compaction.py` | deleted | Goal-create skill compaction | Structural tests |