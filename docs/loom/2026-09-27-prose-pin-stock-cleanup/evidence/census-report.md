# Census Report — Prose-Pin Stock Cleanup (W0-01)

Generated: 2026-09-28
Total test files scanned: 167

## Per-Class Counts

| Class | Count |
|-------|-------|
| behavior | 79 |
| grammar-invariant | 5 |
| not-prose | 33 |
| other | 10 |
| sentence-pin | 11 |
| structure | 29 |

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
| loom-code/tests/test_check_doc_citations.py | structure |  |
| loom-code/tests/test_check_mechanisms.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-code/tests/test_check_skill_crossrefs.py | sentence-pin | has_pins=yes |
| loom-code/tests/test_closing_review_recovery_rules.py | sentence-pin | has_pins=yes |
| loom-code/tests/test_codex_hook_trust_contract.py | sentence-pin | has_pins=yes |
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
| loom-code/tests/test_probes_coldread_baselines_four_dirs_n10_sonnet.py | structure |  |
| loom-code/tests/test_probes_coldread_changelog_carries_1_5_1.py | structure |  |
| loom-code/tests/test_probes_coldread_readme_role_section_has_three_way_paragraph.py | structure |  |
| loom-code/tests/test_probes_coldread_baselines_four_dirs_n10_sonnet.py | structure |  |
| loom-code/tests/test_probes_coldread_changelog_carries_1_5_1.py | structure |  |
| loom-code/tests/test_probes_coldread_baselines_four_dirs_n10_sonnet.py | structure |  |
| loom-code/tests/test_probes_cumulative_boundary_reassessment.py | structure |  |
| loom-code/tests/test_probes_language_policy.py | structure |  |
| loom-code/tests/test_probes_replaceable_boundary_behavior.py | behavior | has_pins=no |
| loom-code/tests/test_publish_command_detection.py | behavior | has_pins=no |
| loom-code/tests/test_readme_review_order.py | sentence-pin | has_pins=yes |
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
| loom-workflow/tests/scripts/test_loom_visualization_description_ab.py | sentence-pin | has_pins=yes |
| loom-workflow/tests/scripts/test_no_live_cot_explain_references.py | behavior | has_pins=no |
| loom-workflow/tests/scripts/test_no_retired_loom_code_skill_names.py | sentence-pin | has_pins=yes |
| loom-workflow/tests/scripts/test_readme_card_timing.py | structure |  |
| loom-workflow/tests/scripts/test_recap_state_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_release_metadata.py | structure |  |
| loom-workflow/tests/scripts/test_validate_skill_folder_structure_hook.py | behavior | has_pins=no |
| loom-workflow/tests/scripts/test_visualization_card_hook.py | behavior | has_pins=no, marker=grammar-invariant-content |
| tests/hooks/test_check_codex_manifest_drift.py | behavior | has_pins=no |
| tests/hooks/test_check_memory_store_integrity.py | behavior | has_pins=no |
| tests/hooks/test_remind_memory_mirror.py | behavior | has_pins=no |
| tests/test_adversarial_agy_rule_sync.py | behavior | has_pins=no |
| tests/test_agy_install_docs.py | structure |  |
| tests/test_check_plugin_boundaries.py | behavior | has_pins=no |
| tests/test_kickoff_defaults.py | structure |  |
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
| loom-design/tests/principles/test_principles_ratified_line.py | structure |  |
| loom-design/tests/principles/test_validate_principles_output.py | structure |  |
| loom-design/tests/spec/test_capture_intent_contract.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-design/tests/spec/test_write_spec_contract.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/conftest.py | not-prose |  |
| loom-code/tests/test_adversarial_case_count_scan.py | not-prose |  |
| loom-code/tests/test_adversarial_change_store_programs.py | not-prose |  |
| loom-code/tests/test_adversarial_probe_cap_coverage.py | not-prose |  |
| loom-code/tests/test_check_mechanisms_adversarial.py | not-prose |  |
| loom-code/tests/test_claede_reviewer.py | not-prose |  |
| loom-code/tests/test_codex_stale_hook.py | not-prose |  |
| loom-code/tests/test_contract_charter.py | not-prose |  |
| loom-code/tests/test_git_exec.py | not-prose |  |
| loom-code/tests/test_github_rules.py | not-prose |  |
| loom-code/tests/test_land_cleanup.py | not-prose |  |
| loom-code/tests/test_land_sweep.py | not-prose |  |
| loom-code/tests/test_lang_detect.py | not-prose |  |
| loom-code/tests/test_loom_checker_modules.py | not-prose |  |
| loom-code/tests/test_migration_history.py | not-prose |  |
| loom-code/tests/test_plan_skip_missing_files.py | not-prose |  |
| loom-code/tests/test_pr_floor_workflow.py | not-prose |  |
| loom-code/tests/test_probes_coldread_fixture_items_verbatim_prior_list.py | not-prose |  |
| loom-code/tests/test_probes_rehearsal_abuse_rehearse_probes.py | not-prose |  |
| loom-code/tests/test_rehearse_probes.py | not-prose |  |
| loom-code/tests/test_repo_files.py | not-prose |  |
| loom-code/tests/test_review_json_template.py | not-prose |  |
| loom-code/tests/test_selection_capture.py | not-prose |  |
| loom-code/tests/test_selection_ledger.py | not-prose |  |
| loom-code/tests/test_selection_store.py | not-prose |  |
| loom-code/tests/test_sync_trunk.py | not-prose |  |
| loom-design/tests/test_ci_workflow.py | not-prose |  |
| loom-design/tests/test_marketplace_entry.py | not-prose |  |
| loom-design/tests/test_plugin_manifest.py | not-prose |  |
| loom-design/tests/test_unified_pytest_root.py | not-prose |  |
| tests/conftest.py | not-prose |  |
| tests/test_adversarial_agy_sync.py | not-prose |  |
| tests/test_loom_design_ci_unified_root.py | not-prose |  |
| loom-code/tests/test_check_skill_crossrefs.py | other |  |
| loom-code/tests/test_codex_hook_trust_contract.py | other |  |
| loom-code/tests/test_principles_amendment.py | other |  |
| loom-code/tests/test_ship_guidance_presence.py | other |  |
| loom-workflow/tests/scripts/test_distill_sessions_compaction.py | other |  |
| loom-workflow/tests/scripts/test_loom_visualization_description_ab.py | other |  |
| loom-workflow/tests/scripts/test_no_retired_loom_code_skill_names.py | other |  |
| loom-workflow/tests/scripts/test_skill_count.py | other |  |
| tests/test_kickoff_defaults.py | other |  |
| tests/test_principles_ratification.py | other |  |

## Spot-Check Verification (≥8 files)

| File | Expected | Actual | Notes |
|------|----------|--------|-------|
| loom-code/tests/test_agy_tool_mapping.py | sentence-pin (has_pins=yes) | sentence-pin (has_pins=yes) | Pure prose pin: imports prose_pin, has sentence assertions, no execution ✅ |
| loom-code/tests/test_write_plan_shape_text.py | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | Tests gate marker grammar (<!-- gate: -->), also pins station prose ✅ |
| loom-code/tests/test_loom_checker_intake.py | behavior (has_pins=no) | behavior (has_pins=no) | Executes loom_checker.py via subprocess, asserts on returncode ✅ |
| loom-code/tests/test_selection_store.py | not-prose () | not-prose () | No .md references — pure git/selection store logic ✅ |
| loom-code/tests/test_prose_pin_rule_text.py | grammar-invariant (has_pins=no) | grammar-invariant (has_pins=no) | Tests prose_pin matcher rules in adversary.md & engineering-baseline.md ✅ |
| loom-code/tests/test_lenses_deletion_first.py | sentence-pin (has_pins=yes, note) | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | Tests negation matcher self-tests (baseline §8) — imports prose_pin, has sentence assertions, has_pins=yes ✓ |
| loom-code/tests/test_write_plan_station_text.py | behavior (has_pins=yes) | behavior (has_pins=yes, marker=grammar-invariant-content) | Executes loom_checker.py, pins exact station prose sentences ✅ |
| loom-code/tests/test_simplified_station_text.py | behavior (has_pins=yes) | behavior (has_pins=yes) | Executes loom_checker.py, pins simplified station prose ✅ |
| loom-code/tests/test_package_tests_command.py | structure () | structure () | Only asserts on document shape (frontmatter, sections, gate markers) ✅ |
| loom-code/tests/test_adversary_routing.py | behavior (has_pins=yes) | behavior (has_pins=yes) | Executes pytest inside copied repos, asserts returncode, also pins prose ✅ |
| loom-workflow/tests/scripts/test_critique_compaction.py | sentence-pin (has_pins=yes) | sentence-pin (has_pins=yes) | Compaction test: pins exact sentences from merged critique skill ✅ |
| loom-workflow/tests/scripts/test_goal_create_compaction.py | sentence-pin (has_pins=yes) | sentence-pin (has_pins=yes) | Compaction test: pins exact sentences from goal-create skill ✅ |
| loom-workflow/tests/handoff/test_handoff_skill_md.py | structure () | structure () | Compaction test: checks structural elements (key presence in dictionaries) ✅ |
| loom-workflow/tests/scripts/test_recap_state_compaction.py | structure () | structure () | Compaction test: checks document shape (frontmatter, sections, headings) ✅ |