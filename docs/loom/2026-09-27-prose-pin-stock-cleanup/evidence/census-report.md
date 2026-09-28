# Census Report — Prose-Pin Stock Cleanup (W0-01, regenerated in the end-of-Build fix round)

Regenerated in the W4-03 fix round (2026-09-28) on branch `engineering/2026-09-27-prose-pin-stock-cleanup`, in a clean `git worktree` of the fix-round tree (parent `22c7b169` plus this round's probe-file and classifier changes) (no untracked files), from
`python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py` (exit 0; it exits 1 while any file is `other`).
Total test files scanned: 227

## Per-Class Counts

| Class | Count |
|-------|-------|
| behavior | 113 |
| gate-eval | 7 |
| grammar-invariant | 5 |
| not-prose | 54 |
| other | 0 |
| sentence-pin | 0 |
| structure | 48 |

## Full Per-File Classification

Every scanned file, `not-prose` and `other` included.

| File | Class | Secondary Markers |
|------|-------|-------------------|
| loom-code/tests/conftest.py | not-prose |  |
| loom-code/tests/test_acceptance_test_report_shape.py | grammar-invariant | has_pins=yes, note=mixed-grammar-and-pin |
| loom-code/tests/test_adversarial_agy_adapter.py | behavior | has_pins=no |
| loom-code/tests/test_adversarial_agy_anchor_turns.py | behavior | has_pins=no |
| loom-code/tests/test_adversarial_auto_skip_portability.py | behavior | has_pins=no |
| loom-code/tests/test_adversarial_bare_script_lint.py | behavior | has_pins=no |
| loom-code/tests/test_adversarial_blocked_publish_routes.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-code/tests/test_adversarial_case_count_scan.py | not-prose |  |
| loom-code/tests/test_adversarial_census_gaming.py | not-prose |  |
| loom-code/tests/test_adversarial_change_store_programs.py | not-prose |  |
| loom-code/tests/test_adversarial_narrow_delta_waiver.py | behavior | has_pins=no |
| loom-code/tests/test_adversarial_plugin_root_marker.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-code/tests/test_adversarial_probe_cap_coverage.py | not-prose |  |
| loom-code/tests/test_adversarial_version_metadata_sync.py | behavior | has_pins=no |
| loom-code/tests/test_adversary_layout.py | behavior | has_pins=no |
| loom-code/tests/test_adversary_protocol.py | behavior | has_pins=yes |
| loom-code/tests/test_adversary_recipe_code.py | behavior | has_pins=no |
| loom-code/tests/test_adversary_recipe_shape.py | structure | auto=sentence-pin, override=structure, reason=split_sentences feeds a duplicate-sentence check across recipe files; no prose literal is asserted, has_pins=yes |
| loom-code/tests/test_adversary_recipe_skill_gate.py | structure | auto=other, override=structure, reason=one-home check: asserts no rule fragment sits in both the recipe and adversary.md; never asserts a sentence is present |
| loom-code/tests/test_adversary_recipe_spec.py | structure | auto=other, override=structure, reason=one-home check: asserts no rule fragment sits in both the recipe and adversary.md; never asserts a sentence is present |
| loom-code/tests/test_adversary_routing.py | behavior | has_pins=yes |
| loom-code/tests/test_agent_model_frontmatter.py | structure |  |
| loom-code/tests/test_agy_adapter.py | behavior | has_pins=no |
| loom-code/tests/test_architecture_doc_consumers.py | structure |  |
| loom-code/tests/test_build_mechanical_checks.py | behavior | has_pins=yes |
| loom-code/tests/test_build_recovery_rules.py | gate-eval | has_pins=yes |
| loom-code/tests/test_check_contract_citations.py | behavior | has_pins=no |
| loom-code/tests/test_check_doc_citations.py | behavior | has_pins=no |
| loom-code/tests/test_check_mechanisms.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-code/tests/test_check_mechanisms_adversarial.py | not-prose |  |
| loom-code/tests/test_check_skill_crossrefs.py | behavior | auto=other, override=behavior, reason=loads check-skill-crossrefs.py by path and runs find_broken_crossrefs on temp fixtures |
| loom-code/tests/test_claude_reviewer.py | not-prose |  |
| loom-code/tests/test_closing_review_recovery_rules.py | gate-eval | has_pins=yes |
| loom-code/tests/test_codex_hook_trust_contract.py | gate-eval | auto=other, override=gate-eval, reason=pure sentence pin on codex-first-contact.md, named by the mechanisms.yaml eval of write-plan.codex-installed-hook-trust-boundary; batch 2 |
| loom-code/tests/test_codex_stale_hook.py | not-prose |  |
| loom-code/tests/test_coldread_role_split.py | behavior | has_pins=no |
| loom-code/tests/test_contract_charter.py | not-prose |  |
| loom-code/tests/test_contract_manifest.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-code/tests/test_dispatch_profile_contract.py | gate-eval | has_pins=yes |
| loom-code/tests/test_dispatch_profile_resolver.py | behavior | has_pins=no |
| loom-code/tests/test_expert_mode_skill.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_fix_handoff_text.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_fix_scope_text.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_git_exec.py | not-prose |  |
| loom-code/tests/test_github_rules.py | not-prose |  |
| loom-code/tests/test_hooks_json.py | behavior | has_pins=no |
| loom-code/tests/test_kickoff_defaults_grammar.py | behavior | has_pins=no |
| loom-code/tests/test_land_cleanup.py | not-prose |  |
| loom-code/tests/test_land_merge.py | behavior | has_pins=no |
| loom-code/tests/test_land_sweep.py | not-prose |  |
| loom-code/tests/test_lang_detect.py | not-prose |  |
| loom-code/tests/test_language_anchor_hook.py | behavior | has_pins=no |
| loom-code/tests/test_legacy_contract_removed.py | behavior | has_pins=no |
| loom-code/tests/test_lenses_deletion_first.py | grammar-invariant | has_pins=yes, note=mixed-grammar-and-pin |
| loom-code/tests/test_loom_attestation.py | behavior | has_pins=no |
| loom-code/tests/test_loom_checker_cli.py | behavior | has_pins=no |
| loom-code/tests/test_loom_checker_intake.py | behavior | has_pins=no |
| loom-code/tests/test_loom_checker_intent.py | behavior | has_pins=no |
| loom-code/tests/test_loom_checker_modules.py | not-prose |  |
| loom-code/tests/test_loom_checker_standing.py | behavior | has_pins=no |
| loom-code/tests/test_loom_publish.py | behavior | has_pins=no |
| loom-code/tests/test_migration_history.py | not-prose |  |
| loom-code/tests/test_one_way_door_copies.py | structure |  |
| loom-code/tests/test_package_tests_command.py | structure |  |
| loom-code/tests/test_plan_field_caps.py | behavior | has_pins=no |
| loom-code/tests/test_plan_simplicity_text.py | behavior | has_pins=yes |
| loom-code/tests/test_plan_skip_missing_files.py | not-prose |  |
| loom-code/tests/test_pr_floor.py | behavior | has_pins=no |
| loom-code/tests/test_pr_floor_workflow.py | not-prose |  |
| loom-code/tests/test_probes_charter_charter.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_branch_end.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_run_status.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_runner.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_scoring.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_wave1.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_abuse_coldread_wave1_fix.py | behavior | has_pins=no |
| loom-code/tests/test_probes_coldread_baselines_four_dirs_n10_sonnet.py | structure |  |
| loom-code/tests/test_probes_coldread_changelog_carries_1_5_1.py | structure |  |
| loom-code/tests/test_probes_coldread_fixture_items_verbatim_prior_list.py | not-prose |  |
| loom-code/tests/test_probes_coldread_readme_role_section_has_three_way_paragraph.py | structure |  |
| loom-code/tests/test_probes_cumulative_boundary_reassessment.py | behavior | has_pins=no |
| loom-code/tests/test_probes_language_policy.py | structure |  |
| loom-code/tests/test_probes_rehearsal_abuse_rehearse_probes.py | not-prose |  |
| loom-code/tests/test_probes_replaceable_boundary_behavior.py | behavior | has_pins=no |
| loom-code/tests/test_prose_pin_rule_text.py | grammar-invariant | has_pins=no |
| loom-code/tests/test_publish_command_detection.py | behavior | has_pins=no |
| loom-code/tests/test_readme_review_order.py | structure |  |
| loom-code/tests/test_rehearse_probes.py | not-prose |  |
| loom-code/tests/test_repo_files.py | not-prose |  |
| loom-code/tests/test_review_convergence_contract.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_review_json_template.py | not-prose |  |
| loom-code/tests/test_reviewer_mechanical_evidence.py | grammar-invariant | has_pins=yes, note=mixed-grammar-and-pin |
| loom-code/tests/test_second_vendor_policy.py | behavior | has_pins=no |
| loom-code/tests/test_selection_capture.py | not-prose |  |
| loom-code/tests/test_selection_finalize.py | behavior | has_pins=no |
| loom-code/tests/test_selection_guard.py | behavior | has_pins=no |
| loom-code/tests/test_selection_ledger.py | not-prose |  |
| loom-code/tests/test_selection_store.py | not-prose |  |
| loom-code/tests/test_session_start_words.py | behavior | has_pins=no |
| loom-code/tests/test_ship_station_text.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_ship_worktree_merge.py | behavior | has_pins=no |
| loom-code/tests/test_simplified_station_text.py | behavior | has_pins=yes |
| loom-code/tests/test_sync_before_review_text.py | behavior | has_pins=yes |
| loom-code/tests/test_sync_codex_manifest.py | behavior | has_pins=no |
| loom-code/tests/test_sync_trunk.py | not-prose |  |
| loom-code/tests/test_test_budget_text.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-code/tests/test_verification_status.py | behavior | has_pins=no |
| loom-code/tests/test_write_plan_shape_text.py | grammar-invariant | has_pins=yes, note=mixed-grammar-and-pin |
| loom-code/tests/test_write_plan_station_text.py | behavior | has_pins=yes, marker=grammar-invariant-content |
| loom-workflow/tests/decision-map/conftest.py | not-prose |  |
| loom-workflow/tests/decision-map/test_check_map_fog.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_check_map_links.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_delivery_binding.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_delivery_evidence.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_governance_ratification.py | structure |  |
| loom-workflow/tests/decision-map/test_map_init.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_map_lock.py | not-prose |  |
| loom-workflow/tests/decision-map/test_map_module_boundaries.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_map_progress.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_map_store.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_map_transaction.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_migrate_map_v3.py | behavior | has_pins=no |
| loom-workflow/tests/decision-map/test_skill_doc.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-workflow/tests/decision-map/test_start_delivery.py | behavior | has_pins=no |
| loom-workflow/tests/distill-sessions/conftest.py | not-prose |  |
| loom-workflow/tests/distill-sessions/test_aggregate.py | not-prose |  |
| loom-workflow/tests/distill-sessions/test_apply.py | behavior | has_pins=no |
| loom-workflow/tests/distill-sessions/test_cluster.py | not-prose |  |
| loom-workflow/tests/distill-sessions/test_facets.py | not-prose |  |
| loom-workflow/tests/distill-sessions/test_friction_signals.py | not-prose |  |
| loom-workflow/tests/distill-sessions/test_ingest.py | not-prose |  |
| loom-workflow/tests/distill-sessions/test_main.py | behavior | has_pins=no |
| loom-workflow/tests/distill-sessions/test_main_e2e.py | behavior | has_pins=no |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py | structure |  |
| loom-workflow/tests/distill-sessions/test_propose.py | behavior | has_pins=no |
| loom-workflow/tests/distill-sessions/test_report.py | behavior | has_pins=no |
| loom-workflow/tests/git-memory/conftest.py | not-prose |  |
| loom-workflow/tests/git-memory/test_loom_delegation.py | structure |  |
| loom-workflow/tests/git-memory/test_memory_grep_version.py | structure |  |
| loom-workflow/tests/git-memory/test_privacy_scan.py | behavior | has_pins=no |
| loom-workflow/tests/git-memory/test_probe_store_failure_fails_loud.py | not-prose |  |
| loom-workflow/tests/git-memory/test_probes_memory_grep_no_trailers_support.py | not-prose |  |
| loom-workflow/tests/git-memory/test_probes_memory_grep_render.py | behavior | has_pins=no |
| loom-workflow/tests/git-memory/test_probes_memory_grep_single_pass.py | behavior | has_pins=no |
| loom-workflow/tests/goal-create/conftest.py | not-prose |  |
| loom-workflow/tests/goal-create/test_goal_lint.py | behavior | has_pins=no |
| loom-workflow/tests/goal-create/test_goal_lint_languages.py | not-prose |  |
| loom-workflow/tests/goal-create/test_goal_shape.py | structure |  |
| loom-workflow/tests/goal-create/test_readmes.py | structure |  |
| loom-workflow/tests/goal-create/test_skill_md.py | gate-eval | has_pins=yes |
| loom-workflow/tests/handoff/test_handoff_readmes.py | structure |  |
| loom-workflow/tests/handoff/test_handoff_schema.py | structure |  |
| loom-workflow/tests/handoff/test_handoff_skill_md.py | structure |  |
| loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py | structure |  |
| loom-workflow/tests/loom-memory/conftest.py | not-prose |  |
| loom-workflow/tests/loom-memory/test_loom_memory.py | behavior | has_pins=no |
| loom-workflow/tests/loom-memory/test_migrate_legacy_store.py | behavior | has_pins=no |
| loom-workflow/tests/loom-memory/test_skill_contract.py | behavior | has_pins=no |
| loom-workflow/tests/loom-visualization/conftest.py | not-prose |  |
| loom-workflow/tests/loom-visualization/test_adversarial_probes.py | behavior | has_pins=no |
| loom-workflow/tests/loom-visualization/test_ascii_checks.py | not-prose |  |
| loom-workflow/tests/loom-visualization/test_ascii_cli.py | not-prose |  |
| loom-workflow/tests/loom-visualization/test_ascii_generators.py | not-prose |  |
| loom-workflow/tests/loom-visualization/test_ascii_width.py | not-prose |  |
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
| loom-workflow/tests/scripts/test_distill_sessions_compaction.py | gate-eval | auto=other, override=gate-eval, reason=needle presence in SKILL.md, some needles phrases (Read it when, No network calls); named by the mechanisms.yaml eval of distill-sessions; batch 2 |
| loom-workflow/tests/scripts/test_git_memory_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_handoff_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_independent_advisor_plugin_readmes.py | structure |  |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_no_live_cot_explain_references.py | behavior | has_pins=no |
| loom-workflow/tests/scripts/test_no_retired_loom_code_skill_names.py | structure | auto=other, override=structure, reason=asserts no retired loom-code skill name against the skills on disk, plus scanner self-tests; no sentence asserted |
| loom-workflow/tests/scripts/test_readme_card_timing.py | structure |  |
| loom-workflow/tests/scripts/test_recap_state_compaction.py | structure |  |
| loom-workflow/tests/scripts/test_release_metadata.py | structure |  |
| loom-workflow/tests/scripts/test_skill_count.py | structure | auto=other, override=structure, reason=skill directory set and manifest tools agree; no sentence asserted |
| loom-workflow/tests/scripts/test_validate_skill_folder_structure_hook.py | behavior | has_pins=no |
| loom-workflow/tests/scripts/test_visualization_card_hook.py | behavior | has_pins=no, marker=grammar-invariant-content |
| loom-workflow/tests/test_loom_visualization_page_scripts.py | behavior | has_pins=no |
| loom-workflow/tests/test_plugin_manifest.py | not-prose |  |
| tests/conftest.py | not-prose |  |
| tests/hooks/test_check_codex_manifest_drift.py | behavior | has_pins=no |
| tests/hooks/test_check_memory_store_integrity.py | behavior | has_pins=no |
| tests/hooks/test_remind_memory_mirror.py | behavior | has_pins=no |
| tests/test_adversarial_agy_rule_sync.py | behavior | has_pins=no |
| tests/test_adversarial_agy_sync.py | not-prose |  |
| tests/test_agy_install_docs.py | structure |  |
| tests/test_check_plugin_boundaries.py | behavior | has_pins=no |
| tests/test_kickoff_defaults.py | structure | auto=other, override=structure, reason=the lock-file hash graph and the package-tests preset command shape; no prose literal |
| tests/test_loom_design_ci_unified_root.py | not-prose |  |
| tests/test_loom_plugin_install_layout.py | behavior | has_pins=no |
| tests/test_loom_skill_description_catalog.py | structure |  |
| tests/test_principles_ratification.py | structure | auto=other, override=structure, reason=exactly one ratified-by line and no pending-ratification line; no prose literal |
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
| loom-design/tests/test_ci_workflow.py | not-prose |  |
| loom-design/tests/test_marketplace_entry.py | not-prose |  |
| loom-design/tests/test_plugin_manifest.py | not-prose |  |
| loom-design/tests/test_unified_pytest_root.py | not-prose |  |

## Spot-Check Verification (≥8 files)

| File | Expected | Actual | Notes |
|------|----------|--------|-------|
| loom-code/tests/test_agy_tool_mapping.py | sentence-pin (has_pins=yes) | structure (override) | Deleted in W1; restored in fix round 2 with its structure checks only (table-column scan, role dispatch lines, link resolution); auto class `other`, override row in the classifier |
| loom-code/tests/test_write_plan_shape_text.py | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | Tests gate marker grammar (<!-- gate: -->), also pins station prose ✅ |
| loom-code/tests/test_loom_checker_intake.py | behavior (has_pins=no) | behavior (has_pins=no) | Executes loom_checker.py via subprocess, asserts on returncode ✅ |
| loom-code/tests/test_selection_store.py | not-prose () | not-prose () | No .md references — pure git/selection store logic ✅ |
| loom-code/tests/test_prose_pin_rule_text.py | grammar-invariant (has_pins=no) | grammar-invariant (has_pins=no) | Tests prose_pin matcher rules in adversary.md & engineering-baseline.md ✅ |
| loom-code/tests/test_lenses_deletion_first.py | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | grammar-invariant (has_pins=yes, note=mixed-grammar-and-pin) | Tests negation matcher self-tests (baseline §8) — imports prose_pin, has sentence assertions, has_pins=yes ✓ |
| loom-code/tests/test_write_plan_station_text.py | behavior (has_pins=yes) | behavior (has_pins=yes, marker=grammar-invariant-content) | Executes loom_checker.py, pins exact station prose sentences ✅ |
| loom-code/tests/test_simplified_station_text.py | behavior (has_pins=yes) | behavior (has_pins=yes) | Executes loom_checker.py, pins simplified station prose ✅ |
| loom-code/tests/test_package_tests_command.py | structure () | structure () | Only asserts on document shape (frontmatter, sections, gate markers) ✅ |
| loom-code/tests/test_adversary_routing.py | behavior (has_pins=yes) | behavior (has_pins=yes) | Executes pytest inside copied repos, asserts returncode, also pins prose ✅ |
| loom-workflow/tests/scripts/test_critique_compaction.py | gate-eval (has_pins=yes) | gate-eval (has_pins=yes) | Pruned in W1, restored in fix round 2 (named by a mechanisms.yaml `eval:`, so its content waits for batch 2); gate-eval (W3-02) |
| loom-workflow/tests/scripts/test_goal_create_compaction.py | sentence-pin (has_pins=yes) | deleted (W1) | Compaction pin file, deleted in this batch; not in the census at HEAD |
| loom-workflow/tests/handoff/test_handoff_skill_md.py | structure () | structure () | Compaction test: checks structural elements (key presence in dictionaries) ✅ |
| loom-workflow/tests/scripts/test_recap_state_compaction.py | structure () | structure () | Compaction test: checks document shape (frontmatter, sections, headings) ✅ |
| loom-workflow/tests/loom-memory/test_skill_contract.py | behavior (has_pins=no) | behavior (has_pins=no) | Runs subprocess git ls-files, binds .stdout to staged variable, asserts on returncode ✅ |
| loom-workflow/tests/decision-map/test_delivery_binding.py | behavior (has_pins=no) | behavior (has_pins=no) | Imports delivery_binding production module (scripts/), validates ticket/brief bindings with repo I/O ✅ |
| loom-code/tests/test_adversary_recipe_shape.py | structure (override) | structure (auto=sentence-pin, override=structure) | Manual override, see Classifier corrections: split_sentences feeds a duplicate-sentence check across recipe files; no prose literal asserted |
| loom-code/tests/test_adversary_recipe_code.py | behavior (has_pins=no) | behavior (has_pins=no) | Was grammar-invariant only through an appended comment; after the W4-01 fix round it runs the graduated case-class check as a program, so it reads behavior |
| loom-code/tests/test_principles_amendment.py | sentence-pin | deleted (W4-02) | Was in `other`; exact-sentence and exact-line equality on PRINCIPLES.md, nothing executed |
| loom-code/tests/test_codex_hook_trust_contract.py | gate-eval (override) | gate-eval (auto=other, override=gate-eval) | Pure sentence pin, but the mechanisms.yaml `eval:` of `write-plan.codex-installed-hook-trust-boundary`; batch 2 |

## Classifier corrections in the fix round

The end-of-Build adversary showed the earlier zero came partly from comments. Corrections, each applied to every file:

- **Comment stripping.** `#` comments are removed (tokenize) before any signal is matched, so no comment can change a class. Docstrings are kept: stripping them reclassifies 15 unrelated files (none into sentence-pin), a wider change than this round.
- **Reader-call signals removed.** `_flat(`, `flat_prose(` and `rule_prose(` no longer count as sentence assertions: a reader call asserts nothing, and a literal asserted on its result is still caught by the `assert ... in "literal"` alternative. Moves: `test_adversary_recipe_code.py`, `_skill_gate.py`, `_spec.py` sentence-pin → other.
- **Heading-literal exemption.** An `assert "#..." in ...` literal (heading presence) is structure, not a pin.
- **`split_sentences(` kept.** Removing it moved `test_build_recovery_rules.py` and `test_closing_review_recovery_rules.py` from gate-eval to structure, yet both really pin phrases (`_require` phrase lists, exact paragraph endings) in a form no other signal sees; that part was reverted.
- **One manual override** (`MANUAL_OVERRIDES` in the classifier, printed as `auto=…, override=…`): `loom-code/tests/test_adversary_recipe_shape.py` → structure, because split_sentences feeds a duplicate-sentence check across recipe files and no prose literal is asserted.
- **W4-02: the `other` bucket emptied.** Acceptance testing found 12 prose-reading files in a fifth `other` bucket the table did not print. Each now has a `MANUAL_OVERRIDES` row with a reason tied to what it asserts (printed in the per-file table), two pure pins were deleted, the table prints every file, and the classifier exits 1 while any file is `other`.
- **W4-03: no override hides a pin.** Each override states the file's true class with a reason that matches what it asserts. The hash guard is deleted; the kickoff phrase pins and the exact amendment literal in `tests/test_principles_ratification.py` are removed, so those two files are structure with no prose literal; `test_adversarial_description_ab_probes.py` is behavior on its own (its restored renderer probes assert `pytest.raises`), so the fix round dropped its override.

Also in this round: the appended `# prose_pin matcher self-test` comments were removed from the four recipe modules, and their leftover pin tables and synthetic pin tests deleted.

## Removed sentence-pin tests → replacement evidence

Dispositions are the net diff against base `946e06d1`. Review-lens facets are the `docs` lens facets in `loom-code/agents/reviewer.md` (defined in `loom-code/skills/closing-review/references/lenses.md`); `a.py::f` names one test function.

| File | Disposition | What the pins guarded | Replacement evidence |
| :--- | :--- | :--- | :--- |
| `loom-code/tests/test_adversary_recipe_code.py` | pruned (`test_recipe_affirms_the_rule`, `test_recipe_states_the_rule` + 2 helper self-tests) | Code-recipe rules stated in the recipe | `test_adversary_recipe_code.py::test_recipe_names_every_class_to_draw_cases_from` (reads the current recipe for its class list); lens facet `omission`. Recipe-rule presence is now review-only: no test reads each rule in the current recipe |
| `loom-code/tests/test_adversary_recipe_shape.py` | unchanged (net diff vs `946e06d1` empty; edited in 45bd949d, restored in e4ec2437) | nothing removed | none needed |
| `loom-code/tests/test_adversary_recipe_skill_gate.py` | pruned (`test_recipe_affirms_the_rule` + 1 helper self-test) | Skill-and-gate recipe rules stated in the recipe | lens facet `omission`. Recipe-rule presence is now review-only: no test reads each rule in the current recipe |
| `loom-code/tests/test_adversary_recipe_spec.py` | pruned (`test_recipe_affirms_the_rule`, `test_recipe_states_the_rule` + 2 helper self-tests) | Spec recipe rules stated in the recipe | lens facet `omission`. Recipe-rule presence is now review-only: no test reads each rule in the current recipe |
| `loom-code/tests/test_adversary_routing.py` | pruned (`test_a_reworded_recipe_is_not_blamed_on_the_addition`, `test_first_planting_fails_when_nothing_was_planted_synthetic`) | A recipe reword must redden only that recipe's own pin test | `test_adversary_routing.py::test_a_reworded_recipe_plants_no_failure_for_the_addition_to_be_judged_on`; `test_adversary_routing.py::test_reword_plants_when_prose_pin_exists_synthetic` |
| `loom-code/tests/test_agy_tool_mapping.py` | pruned (fix round 2: restored after a whole-file deletion; `test_reference_names_agy_tools_and_every_loom_agent`, the two second-vendor/model-fallback sentence tests, the pointer pin and its self-test stay deleted) | AgY reference names the agy tools and every agent; each station's pointer sentence; second-vendor and model-fallback sentences | kept structure tests `test_agy_tool_mapping.py::test_each_station_points_to_the_reference_and_link_resolves` (link resolution only), `::test_reference_names_no_claude_only_tool_for_agy`, `::test_reference_dispatches_every_role_as_self_reading_its_contract`, `::test_reference_never_invokes_a_plugin_agent_as_typename` + their two synthetic self-tests; the wording is review-only: lens facet `incorrect-fact` (tool names), `omission` (pointer and fallback sentences) |
| `loom-code/tests/test_dispatch_profile_contract.py` | pruned (6 functions; fix round 2 restored the 4 assertion lines removed inside kept functions: 3 in the `eval:`-named `test_class_relative_route_and_insufficient_evidence_boundary`, 1 in `test_nonconforming_output_retry_keeps_validation_and_retry_ownership_separate`) | Profile prose: atomic fallback, five effort tiers, sequential escalation, final redispatch routed, moved invocation obligations; stations link the profile | `test_dispatch_profile_resolver.py::test_selected_model_pair_is_checked_atomically`, `::test_all_five_portable_efforts_can_be_inherited`, `::test_reasoning_escalation_is_sequential_and_uses_shared_budget`, `::test_final_allowed_execution_success_is_routed`; `test_dispatch_profile_contract.py::test_stations_do_not_restate_the_resolver_invocation` (each invocation phrase stated once in the profile); station link presence is review-only (lens facet `omission`) |
| `loom-code/tests/test_module_criteria_text.py` | pruned (fix round 2: restored after a whole-file deletion; `PROPERTY_PINS`, `OPTIONAL_TEST_PIN`, `ROADMAP_PIN` and their tests stay deleted) | AGENTS.md's wording of each criterion, the optional-test-module sentence, the ROADMAP one-skill-per-change line | kept structure tests `test_module_criteria_text.py::test_conventions_name_the_four_properties_and_no_others`, `::test_every_property_the_conventions_state_has_an_entry`, `::test_each_property_is_enforced_by_a_check_that_exists`, `::test_each_check_sits_under_the_criterion_it_enforces`, whose map sends change to `test_adversary_routing.py::test_a_reworded_recipe_plants_no_failure_for_the_addition_to_be_judged_on`, add to `::test_adding_a_kind_is_one_file_and_one_row`, remove to `::test_removing_a_kind_routed_today_leaves_no_reference`, locate to `test_adversary_layout.py::test_no_kind_rule_appears_outside_its_own_file`; the wording is review-only: lens facet `omission` |
| `loom-workflow/tests/goal-create/test_input_floor.py` | pruned (fix round 2: restored after a whole-file deletion, keeping only the slot-mapping cross-seam test) | Goal input floor: slot names, bar clause, provenance tags, slot-to-field mapping | kept structure test `test_input_floor.py::test_slot_mapping_uses_the_shape_reference_field_names` (mapping); `test_goal_lint.py::test_floor_fails_structure_and_warns_on_judgment`; `test_goal_lint.py::test_field_labels_match_the_shape_reference`; the bar-clause and provenance-tag wording is review-only: lens facet `omission` |
| `loom-workflow/tests/goal-create/test_skill_md.py` | pruned (9 functions) | Goal-create session and activation prose; the offer-not-trigger invocation sentence | `test_skill_md.py::test_session_activation_rules_are_one_registered_gate` (activation rules); `test_skill_md.py::test_invocation_section_counts_the_offer_sites_that_exist` (offer sites); the other session wording (bounded proposal, confirmation, fallback, call-site citations, artifact input) is review-only: lens facets `omission`, `inconsistency` |
| `loom-workflow/tests/scripts/test_critique_compaction.py` | unchanged (fix round 2 restored `test_shared_discipline_is_stated_once`: the file is the `eval:` of `critique` in `mechanisms.yaml`, so its content waits for batch 2; net diff vs `946e06d1` empty) | nothing removed | none needed |
| `loom-workflow/tests/scripts/test_goal_create_compaction.py` | deleted | Goal-create entrypoint keeps modes, floor, invocation; ARC's not-applicable sentence; the never-fires sentence | `test_skill_md.py::test_declares_two_modes_and_conditional_arc` (both mode headings), `::test_floor_invocation_line_names_the_script` (floor invocation); the ARC not-applicable and never-fires wording is review-only: lens facet `omission` |
| `loom-code/tests/test_principles_amendment.py` | deleted (W4-02) | PRINCIPLES.md non-negotiable 2 sentences and the exact ratified-by line | `tests/test_principles_ratification.py::test_exactly_one_ratified_by_line` (one log line); checker rule `standing.product-principles-reject` (signature grammar); lens facet `omission` (the wording) |
| `loom-code/tests/test_ship_guidance_presence.py` | deleted (W4-02) | Ship SKILL.md table and no-inline-list guidance sentences | lens facet `omission` |
| `loom-workflow/tests/scripts/test_loom_visualization_description_ab.py` | deleted (W4-03, user-decided) | loom-visualization description equals the A/B-tested text (two hash comparisons, one phrase pin) | skill lens facets `incorrect-fact` and `omission` (semantic reading of the description). A results rerun needs docs/loom/2026-09-14-loom-visualization-description-trigger/ab/run_ab.py repaired first: it fails at import (the catalog moved to tests/) and hard-codes the old description; that repair is follow-up work outside this change. |
| `loom-workflow/tests/scripts/test_adversarial_description_ab_probes.py` | pruned (W4-03: `test_guard_edited_skill_description_fails_closed`, `test_guard_without_docs_still_collects`) | Attacks on the deleted hash guard only | none needed (their target is deleted). Restored in the fix round, loading `_render_description` from `tests/test_loom_skill_description_catalog.py` (it still feeds the description-length budget check) and asserting rendered text, never a hash: `::test_render_description_trailing_whitespace_renders_identically`, `::test_render_description_folded_scalar_fails_closed`, and `::test_render_description_blank_line_paragraph_is_rendered` (was `..._changes_hash`; now asserts the paragraph appears in the rendered text). The run_ab.py parser/decision probes are kept |
| `tests/test_kickoff_defaults.py` | pruned (W4-03: `test_trailing_note_no_longer_claims_ci_runs_the_same_paths`) | Phrases in the KICKOFF-DEFAULTS.md package-tests trailing note | kept structure tests `test_kickoff_defaults.py::test_package_tests_command_uses_the_complete_loom_family_preset`, `::test_package_test_lock_pins_and_hashes_the_complete_graph`; lens facet `incorrect-fact` (the note's claims) |
| `tests/test_principles_ratification.py` | pruned (W4-03: exact amendment literal removed; `test_ratified_by_names_2026_09_15_non_negotiable_2_amendment` renamed `test_exactly_one_ratified_by_line`) | The ratified-by line holds the exact 2026-09-15 amendment entry (not a registered `eval:`, not a grammar check) | kept structure tests `test_principles_ratification.py::test_exactly_one_ratified_by_line`, `::test_pending_ratification_line_absent`; checker rule `standing.product-principles-reject` (signature grammar); lens facet `omission` |

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
| HEAD, W4-03 fix-round tree (clean worktree) | 728 |

HEAD >= base. A per-function name diff of the two trees: two functions disappeared, both W4-03 probes of the deleted hash guard in `loom-workflow/tests/scripts/test_adversarial_description_ab_probes.py` (`test_guard_edited_skill_description_fails_closed`, `test_guard_without_docs_still_collects`); the three additions are `loom-code/tests/test_adversarial_census_gaming.py::test_census_roots_flag_given_is_accepted`, `loom-code/tests/test_adversary_recipe_code.py::test_case_class_check_recipe_row_dropped_goes_red` and `loom-code/tests/test_adversary_routing.py::test_reword_plants_when_prose_pin_exists_synthetic`. The two files deleted in W4-02 held no executing function.

Commands (from the repo root; `<scratch>` is any directory outside the repo):

```
mkdir -p <scratch>/base && git archive 6f3acd78 | tar -x -C <scratch>/base
python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --count-exec <scratch>/base
python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --count-exec .
```

## Batch 2 (deferred)

Files that still carry sentence pins after this batch, left for a second batch (intent A2/A4 as amended). Gate-eval files (7): named by a `docs/loom/evidence/mechanisms.yaml` `eval:` value, so they are a gate's execution evidence.

- `loom-code/tests/test_build_recovery_rules.py` — gate-eval
- `loom-code/tests/test_closing_review_recovery_rules.py` — gate-eval
- `loom-code/tests/test_codex_hook_trust_contract.py` — gate-eval (W4-02 override; pure pin, eval of `write-plan.codex-installed-hook-trust-boundary`)
- `loom-code/tests/test_dispatch_profile_contract.py` — gate-eval
- `loom-workflow/tests/goal-create/test_skill_md.py` — gate-eval
- `loom-workflow/tests/scripts/test_critique_compaction.py` — gate-eval
- `loom-workflow/tests/scripts/test_distill_sessions_compaction.py` — gate-eval (W4-02 override; needle phrases, eval of `distill-sessions`)

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
