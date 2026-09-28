# Batch 2 deletion list (W0-01)

**A5 recount with the fixed counter, clean worktrees:**

| ref | executing test functions |
|---|---|
| base `7244374d` | **1922** |
| HEAD `e0d7c58e` | **1922** |

Command: `python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --count-exec <wt> [--list]`. Each `<wt>` came from `git worktree add --detach <scratchpad>/<wt> <ref>` and was removed afterwards. For reference, the old regex counter gives 728 at both refs.

## What the counter counts now

A test function counts when it runs a program:

- It calls `subprocess.run/check_output/check_call/call/Popen`, `os.system` or `os.popen`.
- It calls imported production code. That is a module under a `scripts/` directory outside `tests/` and `docs/`, excluding the test helpers `prose_pin` and `rehearse_probes`, or a module loaded by path (`module_from_spec`, `import_module`, `run_path`).
- It calls a local helper that does either, or takes a fixture parameter that does, followed transitively.

A string literal never counts, so `"loom_checker.py selection show"` in a pinned sentence is no longer an execution. That is why the count rose from 728 to 1922: the old counter missed direct production calls and helper-level runs. Against the old set, the fixed counter drops 47 functions, all false positives such as literals and `pytest.raises` on local helpers. It adds 1241.

The census classification (`classify-test-files.py` with no flags) is byte-identical before and after this fix, so no file changed class. The file-level `executes()` used by the census was not touched. Known limit: conftest fixtures are not followed.

## Tags

- **pin** asserts a literal phrase or sentence of runtime prose.
- **synthetic-partner** is a matcher self-test that exists only to prove a pin can fail. It goes when its pin goes.
- **exec** really runs a program, including through a helper (fixed counter).

Action **delete** removes the function. **prune** removes its pin asserts and keeps the rest of the function (structure, absence, one-home or exec asserts). Per-function facts come from `survey.md` §1, and names were checked against HEAD.

## Flags: exec functions touched

| file::function | action | resolution |
|---|---|---|
| `loom-code/tests/test_sync_before_review_text.py::test_behind_branch_synced_then_attestation_validates_at_head` | prune | Mixed exec and pin. The git + `sync-trunk` run and its digest asserts stay in this function. Only the station-text literal and order asserts go. The exec part does not move. |

No planned deletion is an exec function. The 16 exec functions in these 26 files are listed below. Every one is kept or, in the case above, pruned with its exec part kept.

- `test_adversary_routing.py`: the 11 add, remove and reword machinery tests.
- `test_expert_mode_skill.py::test_suggestion_then_plain_yes_skips_nothing`.
- `test_sync_before_review_text.py`: 2 functions.
- `test_write_spec_contract.py::test_checker_subcommands_named_exist` and `::test_checker_rules_named_exist`.

The old counter counted 21 functions in these files that the fixed counter does not. 18 of them are listed below for deletion or pruning, and 3 are kept (`test_fix_scope_text.py::test_only_the_checkers_own_tests_are_exempt`, plus 2 `pytest.raises` helper synthetics in `test_expert_mode_skill.py`). None of the 21 counts as exec under the fixed counter, so removing them cannot lower 1922.

## Per-file lists

### Gate-eval files (7)

**loom-code/tests/test_build_recovery_rules.py**
| function | action | tag |
|---|---|---|
| test_RL_01_absence_re_enters_end_of_build_checks | delete | pin |
| test_RL_09_build_carries_the_cross_station_bound | delete | pin |
| test_RL_11_no_task_to_implement_is_directed_to_section_3 | delete | pin |
| test_RL_13_recovered_run_names_the_sequence_in_the_handoff | delete | pin |
| test_RL_14_lookup_is_bounded_to_the_three_recovery_items | delete | pin |
| test_self_check_negation_discriminates | delete | synthetic-partner (orphaned once the negation pins go) |

Kept: RL_02 and RL_12 (one-home scans; their `PARAGRAPH_OPENER` locator is a hidden pin, plan Risk 4).

**loom-code/tests/test_closing_review_recovery_rules.py**
| function | action | tag |
|---|---|---|
| test_RL_03_absence_is_distinct_and_the_producer_is_looked_up | delete | pin |
| test_RL_05_unanswered_decision_stops_and_asks | delete | pin |
| test_RL_06_answered_decision_proceeds_and_the_skip_rule_is_untouched | delete | pin |
| test_RL_06_rejects_the_restored_expert_mode_ending | delete | synthetic-partner |
| test_RL_07_failed_recovery_stops_and_reports | delete | pin |
| test_RL_08_failed_recovery_neither_retries_nor_hands_on | delete | pin |
| test_RL_10_the_sequence_is_recorded_and_the_second_entry_is_the_last | delete | pin |
| test_RL_12_the_recorded_sequence_surfaces_at_both_stops_and_the_hand_off | delete | pin |
| test_RL_15_recovery_count_is_independent_of_ordinary_review_rounds | delete | pin |
| test_RL_11_acceptance_test_independence_is_stated_in_its_own_section | delete | pin |
| test_RL_13_lookup_is_bounded_to_the_three_recovery_items | delete | pin |
| test_self_check_negation_discriminates | delete | synthetic-partner |

Kept: RL_04 (one-home scan; `LOOKUP_OPENER`/`NEXT_UNRELATED` locators are hidden pins).

**loom-code/tests/test_codex_hook_trust_contract.py**
| function | action | tag |
|---|---|---|
| test_first_contact_new_worktree_does_not_create_loom_trust_work | prune to gate-marker presence (plan W0-02, L315) | pin |
| test_first_contact_keeps_new_or_modified_hook_review_host_owned | delete | pin |
| test_first_contact_checks_a_still_registered_rule_id | delete | pin |

**loom-code/tests/test_dispatch_profile_contract.py**
| function | action | tag |
|---|---|---|
| test_class_relative_route_and_insufficient_evidence_boundary | delete (after W0-02 moves L351) | pin |
| test_capability_quality_transition_is_complete_at_the_model_ceiling | delete | pin |
| test_failure_observations_define_conformance_and_trigger_requirements | delete | pin |
| test_nonconforming_output_retry_keeps_validation_and_retry_ownership_separate | delete | pin |
| test_claude_reviewer_dispatch_is_atomic_and_retry_budgets_do_not_stack | delete (after W0-02 moves L345) | pin |
| test_cost_pilot_sparse_ladder_is_historical_not_normative_routing | delete | pin |
| test_affirmative_sentence_helper_accepts_requirement | delete | synthetic-partner |
| test_affirmative_sentence_helper_rejects_negated_requirement | delete | synthetic-partner |

Edited by W0-02, not deleted: `test_atomic_claude_dispatch_gate_is_registered_with_executable_eval` and `test_shared_routing_gate_is_registered_once_with_executable_eval`, which assert the eval strings. Grey zone, kept unless W1-01 decides otherwise: `test_stations_do_not_restate_the_resolver_invocation` (a one-home `count == 1` over literal phrases, which is a hidden pin).

**loom-workflow/tests/goal-create/test_skill_md.py**
| function | action | tag |
|---|---|---|
| test_declares_two_modes_and_conditional_arc | prune (headings stay) | pin |
| test_floor_invocation_line_names_the_script | prune (command shape stays) | pin |
| test_session_activation_rules_are_one_registered_gate | prune to gate-block presence (eval node L348 survives) | pin |
| test_arc_points_at_the_purpose_template_without_restating_it | prune (non-restatement half stays) | pin |

**loom-workflow/tests/scripts/test_critique_compaction.py**
| function | action | tag |
|---|---|---|
| test_mode_routing_is_declared_before_either_lens | prune (mode tokens and heading order stay) | pin |
| test_shared_discipline_is_stated_once | delete | pin |
| test_proposal_mode_preserves_axes_matrix_fallthrough_and_output | delete | pin |
| test_complexity_mode_preserves_mindset_three_questions_and_verdicts | delete | pin |
| test_routing_boundaries_survive_the_merge | prune (the retired-name `not in` check stays) | pin |

**loom-workflow/tests/scripts/test_distill_sessions_compaction.py**
| function | action | tag |
|---|---|---|
| test_entrypoint_preserves_essence | delete, or prune to token and path needles (W1-01) | pin |

### Adversary, build, fix and budget (6)

**loom-code/tests/test_adversary_protocol.py**
| function | action | tag |
|---|---|---|
| test_adversary_probe_maintenance_rule_stated | delete | pin |
| test_protocol_affirms_the_rule | delete | pin |
| test_protocol_states_the_rule | delete | pin |
| test_agent_contract_states_the_order | delete | pin |
| test_adversary_update_never_weakens_a_case | delete | pin |
| test_adversary_mutation_undo_uses_no_discard_command | delete | pin |
| test_protocol_opening_and_recording_name_build_and_finalize | delete | pin |
| test_protocol_recording_sends_findings_to_the_finalize_input | delete | pin |
| test_procedure_sentence_in_both_files_rejected | prune (second assert only; the one-home first assert stays) | pin |
| test_probe_maintenance_pin_helpers_synthetic | delete | synthetic-partner |
| test_rule_pin_helpers_synthetic | delete | synthetic-partner |
| test_rule_sentence_pin_helpers_synthetic | delete | synthetic-partner |
| test_agent_order_pin_helpers_synthetic | delete | synthetic-partner |
| test_update_no_weakening_helpers_synthetic | delete | synthetic-partner |
| test_no_discard_undo_helpers_synthetic | delete | synthetic-partner |

Constants kept for importers: `NO_DISCARD_UNDO`, `UPDATE_NO_WEAKENING`, `case_counts`, `CAP_BOUND`, `FLOOR_BOUND`.

**loom-code/tests/test_adversary_routing.py**
| function | action | tag |
|---|---|---|
| test_contract_routes_through_the_protocol_to_each_recipe | prune (the path-literal link half stays) | pin |
| test_affirms_helper_synthetic | delete | synthetic-partner |

Kept: every exec function, and every name in `test_module_criteria_text.py` `ENFORCED_BY`.

**loom-code/tests/test_build_mechanical_checks.py**
| function | action | tag |
|---|---|---|
| test_build_dispatches_fresh_adversary_then_suite_after_tasks | delete | pin |
| test_adversary_prompt_carries_no_implementer_explanation | prune (leak-word absences may stay) | pin |
| test_build_allows_complete_suite_at_end | delete | pin |
| test_adversary_findings_fixed_or_handed_off | delete | pin |
| test_rerun_trigger_covers_every_fix | delete | pin |
| test_build_redispatches_adversary_for_stale_programs | delete | pin |
| test_no_other_role_edits_adversarial_program | delete | pin |
| test_ordinary_fix_reruns_programs_without_redispatch | delete | pin |
| test_suite_command_names_package_tests_declaration | delete | pin |
| test_plain_words_skip_reaches_ship_unattested | delete | pin |
| test_skipped_selection_step_omits_that_check | delete | pin (old-counter false exec: literal `loom_checker.py selection show`) |
| test_adversary_probe_maintenance_rule_stated | delete | pin |
| test_adversary_redispatch_update_is_new_commit | delete | pin |
| test_build_verify_step_links_adversarial_recipes_in_place | prune (link resolution stays) | pin |
| test_adversary_md_keeps_role_inputs_return_format | delete | pin |
| test_probe_maintenance_pin_helpers_synthetic | delete | synthetic-partner |
| test_stale_program_redispatch_helpers_synthetic | delete | synthetic-partner |
| test_redispatch_update_new_commit_helpers_synthetic | delete | synthetic-partner |
| test_suite_step_without_command_source_fails | delete | synthetic-partner |
| test_dead_pointer_helpers_catalogue_link_reintroduced_fails | prune (affirms half) | synthetic-partner |
| test_handoff_helpers_synthetic | delete | synthetic-partner |

Judgement call, kept by default: `test_no_speculative_preflight_ban_remains` and `test_returned_change_only_trigger_absent` (absence checks of retired wording). `test_added_sentence_scans_synthetic` needs its borrowed fixtures inlined.

**loom-code/tests/test_fix_handoff_text.py** (whole file deleted)
| function | action | tag |
|---|---|---|
| test_every_rule_sentence_is_pinned_exactly_and_record_kept_verbatim | delete | pin |
| test_weakened_or_inserted_paragraph_fails_the_pins | delete | synthetic-partner |
| test_no_gate_marker_or_dispatch_words | delete | pin (its paragraph locator is the `RECORD` literal; the no-gate property is recomputed by `check_mechanisms.py` R1) |

**loom-code/tests/test_fix_scope_text.py**
| function | action | tag |
|---|---|---|
| test_rule_names_class_search_and_acceptance_surfaces | delete | pin |
| test_record_states_class_and_places_searched_even_when_none_found | delete | pin |
| test_pointers_reach_every_fix_path | delete | pin |
| test_one_class_many_instances_is_one_task | delete | pin |
| test_weakened_rule_fails_the_pins | delete | synthetic-partner |
| test_blocked_for_instances_rewrite_fails_the_pin | delete | synthetic-partner |

Kept: the rule-count guard and its self-tests, `test_only_the_checkers_own_tests_are_exempt` (not exec under the fixed counter) and `test_no_gate_marker_or_dispatch_wording`.

**loom-code/tests/test_test_budget_text.py**
| function | action | tag |
|---|---|---|
| test_implementer_states_budget_and_net_lines | delete | pin |
| test_adversarial_probe_small_reuses_helpers | delete | pin |
| test_five_program_cap_unchanged | delete | pin |
| test_tests_dimension_overbuilt_is_finding | delete | pin |
| test_fix_adds_at_most_one_test | delete | pin |
| test_tests_dimension_names_prose_evidence | delete | pin |
| test_behaviour_changes_still_require_executable_evidence | delete | pin |

Kept: `test_budget_not_a_number_threshold`, `test_no_new_gate_marker`.

### Station-text files (7)

**loom-code/tests/test_expert_mode_skill.py**
| function | action | tag |
|---|---|---|
| test_frontmatter_disables_model_invocation_and_openai_yaml_blocks_implicit | prune (frontmatter and yaml keys stay) | pin |
| test_skill_text_evaluates_no_gate | prune (gate absence and command-set regex stay) | pin |
| test_skill_procedure_maps_proposes_reports_withdraws_and_relapses | delete (after W0-02 moves L116) | pin |
| test_skill_round1_boundary_intent_skip_and_withdrawal_split | prune (the `not in` negatives stay) | pin |
| test_readme_lists_expert_mode | delete | pin |
| test_changelog_names_failure_sources_and_limits | delete | pin |
| test_expert_mode_keeps_its_typed_confirmation | prune (negatives stay) | pin |
| test_expert_mode_holds_the_suggestion_rules_once | prune (the `count == 1` one-home checks stay) | pin |
| test_station_one_sentence_points_to_expert_mode | prune (the MOVED_RULES absence stays) | pin |

Kept: `test_suggestion_then_plain_yes_skips_nothing` (**exec**), helper synthetics and pointer-helper mutants. W1-04 decides whether they orphan once the pins go.

**loom-code/tests/test_plan_simplicity_text.py**
| function | action | tag |
|---|---|---|
| test_a1_write_plan_dispatches_fresh_plan_lens_reviewer | delete | pin |
| test_a3_plan_lens_is_loom_code_reviewer | delete | pin |
| test_a5_adoption_is_recorded_agent_decided | delete | pin |
| test_a1_step_runs_before_the_checker_commands | delete | pin |
| test_a5_lens_maps_shapes_to_deletion_first_findings | delete | pin |
| test_a5_plan_lens_has_no_fix_round | prune (the negative stays) | pin |

**loom-code/tests/test_review_convergence_contract.py**
| function | action | tag |
|---|---|---|
| test_review_episode_has_three_distinct_content_rounds_and_no_identity_reset | prune (gate-marker presence stays) | pin |
| test_round_roles_name_three_rounds_and_relook_term | delete | pin |
| test_stuck_review_stops_local_patching | delete | pin |
| test_agent_owns_technical_choices_until_product_contract_changes | delete | pin |
| test_same_content_executor_retry_is_bounded_and_not_a_round | delete | pin |
| test_round_four_is_forbidden_in_context | delete | pin |
| test_station_commits_report_before_finalize | delete | pin |
| test_report_committed_before_reviewers_read_final_digest | delete | pin |
| test_reviewer_yaml_is_converted_to_finalization_json | delete | pin |
| test_convergence_states_the_recording_moment | delete | pin (the do-not-delete comment goes with it, plan W1-04) |
| test_convergence_forbids_spending_an_extra_digest_on_a_lesson | delete | pin |
| test_convergence_states_the_scarcity_bar | delete | pin |
| test_recording_passage_invokes_nothing_and_registers_no_mechanism | prune (negatives stay) | pin |
| test_acceptance_test_before_first_reviewer_dispatch | delete | pin |
| test_reviewers_dispatched_after_build_checks | prune (negation and antecedent loops stay) | pin |
| test_probe_graduation_gate_states_both_halves | delete (after W0-02 moves L342) | pin |
| test_finalize_failure_fix_needs_next_round | delete | pin |
| test_finalize_failure_without_round_is_non_convergent | delete | pin |
| test_earlier_verdicts_not_reused | prune (negation scan stays) | pin |
| test_unresolved_adversarial_findings_reach_finalize_input | delete | pin |
| test_round2_blockers_still_require_relook_before_round3 | delete | pin |
| test_finalize_failure_round_states_no_relook_unless_stuck | delete | pin |

**loom-code/tests/test_ship_station_text.py**
| function | action | tag |
|---|---|---|
| test_ship_publish_title_type_equals_branch_type | delete | pin |
| test_ship_text_runs_land_after_acceptance | delete | pin |
| test_ship_text_separates_authorization_from_acceptance | prune (heading regexes stay) | pin |
| test_ship_prose_forbids_handing_the_command_over | delete | pin |
| test_ship_prose_covers_the_refusals_that_name_no_remedy | prune (the AST premise over `publish.py` stays) | pin |
| test_ship_runs_github_rules_before_publish | delete | pin |
| test_ship_never_runs_setup_unasked | prune (the consent loop stays) | pin |
| test_ship_template_missing_waits_for_consent_and_its_own_change | delete | pin |
| test_ship_asks_setup_consent_in_consequence_form | prune (gate absence stays) | pin |
| test_ship_names_every_publish_refusal | delete | pin |
| test_ship_lands_from_the_change_branch_worktree_and_reports_status | delete | pin |

Names kept for `test_adversarial_blocked_publish_routes.py`: `NO_HANDOVER`, `SHIP`, `_gate_regions`, `_occurrences`, `_gate_marked_occurrences`.

**loom-code/tests/test_simplified_station_text.py**

Every function below pins literal phrases. Where a function also holds `not in` absences or counts, W1-04 may prune it instead of deleting it.

| function | action | tag |
|---|---|---|
| test_review_uses_one_computed_reviewer_floor_without_prose_allowlist | delete/prune | pin |
| test_station_summaries_do_not_duplicate_reviewer_counts | prune (absences stay) | pin |
| test_principles_require_the_mechanically_computed_reviewer_floor | prune ("zero reviewers" absence stays) | pin |
| test_review_generates_attestation_without_ledger_ceremony | prune (`review.json` absence stays) | pin |
| test_ship_validates_without_replaying_functional_work | delete | pin |
| test_ship_keeps_publication_safety | delete | pin |
| test_ci_failure_continues_without_new_recovery_machinery | delete/prune | pin |
| test_review_uses_one_observable_claude_attempt_and_existing_retry | delete/prune | pin |
| test_review_consumes_every_second_vendor_selection_source | delete | pin |
| test_ship_uses_one_publish_command_after_acceptance | delete | pin |
| test_ship_owns_one_self_contained_contextual_pr_body | prune (9-heading count stays) | pin |
| test_ship_requires_auditable_decisions_without_hidden_reasoning | delete/prune | pin |
| test_ship_uses_mermaid_only_when_relationships_carry_information | delete | pin |
| test_git_memory_contributes_without_competing_top_level_schema | prune (absences and heading check stay) | pin |
| test_ship_diagram_contract_has_mutually_exclusive_outcomes | delete | pin |
| test_git_memory_defers_loom_consent_and_schema_to_ship | delete/prune | pin |
| test_intent_confirmation_discloses_publication_and_separate_merge | delete | pin |
| test_host_specific_skill_guidance_uses_each_native_contract | delete/prune | pin |
| test_principles_name_installed_hooks_for_both_hosts | delete | pin |
| test_station_summaries_distinguish_current_and_legacy_ship_ownership | delete/prune | pin |
| test_build_has_no_evidence_accounting | prune (`review.json` absence stays) | pin |
| test_build_and_plan_require_implementer_dispatch_without_requiring_parallelism | delete/prune | pin |
| test_capture_intent_boundaries_are_shared_with_code_only_intake | delete | pin |
| test_shared_intent_contract_names_altitude_without_new_schema | prune (id absences stay) | pin |
| test_code_only_field_boundaries_keep_problem_and_value_semantics | delete | pin |
| test_stations_read_the_bound_selection_at_entry | delete/prune | pin |
| test_build_obligations_yield_to_a_bound_selection | delete/prune | pin |
| test_review_dispatches_nothing_for_skipped_steps | prune (heading absence stays) | pin |
| test_review_hands_reviewer_failures_and_scopes_the_waiver | delete/prune | pin |
| test_ship_step_names_example_matches_the_checker_mapping | prune (only the `STEP_NAMES_SENTENCE` count half; the `STEP_PLAIN_NAMES` cross-check stays) | pin |
| test_ship_renders_selection_disclosure_and_skipped_intent_decision | delete/prune | pin |
| test_code_only_surface_routing_matches_capture_intent | delete/prune | pin |
| test_station_summary_rows_name_builds_mechanical_checks | prune (row shape stays) | pin |
| test_spec_review_dispatches_reviewer_directly | delete | pin |
| test_spec_review_names_the_spec_commits_parent_as_reviewed_sha | prune (absence stays) | pin |
| test_plan_questions_asked_claims_no_reader_or_design_record | prune (absences stay) | pin |
| test_acceptance_tester_names_current_artifacts_and_package_suite_owners | delete/prune | pin |
| test_skip_announced_in_one_line | delete | pin |
| test_no_generated_code_requested | delete/prune | pin |
| test_each_station_names_the_narrow_auto_skip_to_the_user | delete | pin |
| test_ship_lists_the_narrow_auto_skip_in_the_pr_body | delete | pin |
| test_each_station_records_a_plain_words_skip_in_the_plan | delete | pin |
| test_ship_writes_a_plain_words_skip_into_the_body_not_the_plan | delete | pin |
| test_review_commits_the_skip_record_before_the_final_digest | delete | pin |
| test_review_plain_words_skip_reaches_ship_without_finalize | delete | pin |
| test_ship_builds_skipped_by_instruction_from_recorded_lines | delete | pin |
| test_review_floor_mismatch_surfaces_as_stale | prune (absence stays) | pin |
| test_readmes_name_the_hook_a_publication_reminder | prune (absences stay) | pin |
| test_changelog_3_8_0_names_skip_record_and_setup_consent | delete | pin |

Kept: `test_current_surfaces_do_not_restore_legacy_publication_ledgers`, `test_closing_review_scope_spec_rejected`, `test_no_skip_condition_reads_selection_show_alone`, `test_selection_only_detector_rejects_the_old_forms` and `test_attestation_readers_name_the_pr_floor_check`.

**loom-code/tests/test_sync_before_review_text.py**
| function | action | tag |
|---|---|---|
| test_behind_branch_synced_then_attestation_validates_at_head | prune (run and digest asserts stay) | **exec** + pin (see Flags) |
| test_merged_sync_returns_to_build_checks_before_dispatch | delete | pin |
| test_no_op_sync_dispatches_without_rerun | prune (negatives and count stay) | pin |

Kept: `test_sync_after_finalize_invalidates_attestation` (**exec**).

**loom-code/tests/test_write_plan_station_text.py**
| function | action | tag |
|---|---|---|
| test_skill_runs_the_plan_checker_before_commit | delete | pin |
| test_template_states_the_spec_change_path | delete | pin |
| test_skill_names_the_engineering_spec_path | delete | pin |
| test_suggest_runs_policy_after_plan_risk_evidence_exists | delete | pin |
| test_suggest_is_non_blocking_and_has_no_background_listener | delete | pin |
| test_ask_still_asks_once_per_change | delete | pin |
| test_ask_is_host_aware_and_has_complete_fallbacks | prune (negatives stay) | pin |
| test_suggest_uses_one_cell_markdown_table_with_spacing | delete | pin |
| test_second_vendor_reference_keeps_next_change_only_notice | delete | pin |
| test_confirmed_selection_is_recorded_for_closing_review | delete | pin |
| test_write_plan_names_typed_branch_and_types | prune (type-set equality stays) | pin |
| test_changelog_3_4_1_session_limit_names_publication | delete | pin |
| test_agy_host_passes_empty_usable_vendors | delete | pin |
| test_decision_boundary_owns_implementation_not_product_behaviour | prune (word cap stays) | pin |
| test_matcher_spec_change_sentence_negated_rejected | delete | synthetic-partner |
| test_matcher_engineering_spec_sentence_negated_rejected | delete | synthetic-partner |

Kept, and required: `test_current_release_metadata_is_synchronized` and `CURRENT_VERSION`, the three README version tests, `test_runtime_tree_names_no_lane` (its name is cited elsewhere), and the matcher and synthetic tests not listed above.

### loom-design contracts (2)

**loom-design/tests/spec/test_capture_intent_contract.py**
| function | action | tag |
|---|---|---|
| test_intent_fields_admit_only_user_supported_product_claims | delete | pin |
| test_unsupported_claims_and_open_questions_have_operational_boundaries | delete | pin |
| test_workflow_authorisation_names_its_existing_carriers | delete | pin |
| test_unknown_observable_surface_still_routes_to_write_spec | delete | pin |
| test_semantic_inversions_are_rejected | delete | pin |
| test_locate_loom_code_reference_keeps_every_obligation | delete | pin |
| test_what_you_will_be_asked_list_present | delete | pin |
| test_task_b_worked_example_present | delete | pin |
| test_ui_flow_six_sentence_present | delete | pin |
| test_second_vendor_evidence_number_present | delete | pin |
| test_suggest_skips_the_intent_decision_point | delete | pin |
| test_ask_keeps_the_question_on_every_change | delete | pin |
| test_ask_excludes_host_and_defines_unavailable_paths | delete | pin |
| test_ask_and_fixed_never_silently_substitute_the_host | delete | pin |
| test_antigravity_host_is_never_told_to_probe_gemini | delete | pin |
| test_second_vendor_modes_match_loom_code_contract | delete | pin |
| test_capture_intent_does_not_call_loom_code_policy | delete/prune | pin |
| test_capture_intent_names_typed_branch | delete | pin |
| test_user_decided_forks_require_an_explicit_answer | delete | pin |
| test_existing_intent_fields_have_explicit_altitude_boundaries | delete | pin |
| test_interview_is_gap_driven_and_draft_is_reduced_after_writing | delete | pin |
| test_material_choice_rules_live_inside_existing_confirmation_gates | delete | pin |
| test_hand_off_lists_agreed_details_and_requires_spec | delete | pin |
| test_no_details_no_forced_spec | delete | pin |
| test_only_explicit_yes_is_carried | delete | pin |
| test_unanswered_or_deferred_proposal_dropped | delete | pin |
| test_carried_detail_quotes_user_or_agreed_proposal | delete | pin |
| test_background_context_and_inference_not_carried | delete | pin |
| test_engineering_restatement_shows_carried_details_table | delete | pin |
| test_intent_confirmation_table_engineering_only | delete | pin |
| test_product_needs_design_no_not_shown_at_intent_confirmation | delete | pin |
| test_later_stops_name_both_spec_writing_stations | delete | pin |
| test_asked_list_admits_exception_stops | delete | pin |
| test_nothing_agreed_shows_no_table | delete | pin |
| test_intent_sections_may_use_tables_and_diagrams | delete | pin |
| test_intent_diagram_form_is_flowchart_or_table | delete | pin |
| test_acceptance_stays_numbered_list_and_flows_stay_out | delete | pin |
| test_altitude_pass_runs_after_the_fill_in_list_exists | delete | pin |
| test_loom_design_version_2_2_0_consistent | prune (README sentence only; the manifest-version half stays) | pin |
| test_openingLinePin_negatedInstruction_rejected | delete | synthetic-partner |
| test_askPin_syntheticAffirmative_accepted | delete | synthetic-partner |
| test_askPin_syntheticNegated_rejected | delete | synthetic-partner |
| test_affirmedPin_syntheticAffirmativeSentence_accepted | delete | synthetic-partner |
| test_affirmedPin_syntheticNegatedSentence_rejected | delete | synthetic-partner |
| test_affirmedPin_syntheticCodeSpanNo_notNegation | delete | synthetic-partner |

No function in this file is exec. The file is `behavior` only through the `CONTRACT_COMMAND` literal.

**loom-design/tests/spec/test_write_spec_contract.py**
| function | action | tag |
|---|---|---|
| test_requirements_preserve_acceptance_ownership_without_invented_state | delete | pin |
| test_out_of_scope_is_not_promoted_to_product_prohibition | delete | pin |
| test_ui_flows_do_not_invent_visible_reactions | delete | pin |
| test_semantic_inversions_are_rejected | delete | pin |
| test_what_you_will_be_asked_list_present | delete | pin |
| test_ui_flow_two_sentence_present | delete | pin |
| test_intake_station_argument_is_this_station | delete | pin |
| test_risk_triggered_spec_review_contract | prune (the `loom-code:closing-review` absence stays) | pin |
| test_one_way_door_copy_states_it_is_deliberate | delete | pin |
| test_spec_risk_classes_are_explicit | delete | pin |
| test_spec_records_each_carried_detail | delete | pin |
| test_product_carried_detail_recorded_where_decision_point_two_shows | delete | pin |
| test_non_visible_detail_never_new_req | delete | pin |
| test_asked_list_leads_branching_flow_with_table_or_diagram | delete | pin |
| test_agent_proposal_not_agreed_not_recorded | delete | pin |
| test_parallel_cases_table_branching_diagram | delete | pin |
| test_short_flow_stays_lines | delete | pin |
| test_readback_leads_with_table_or_text_diagram | delete | pin |
| test_chat_readback_has_no_mermaid | prune (the mermaid-fence absence stays) | pin |
| test_affirmedPin_syntheticAffirmativeSentence_accepted | delete | synthetic-partner |
| test_affirmedPin_syntheticNegatedSentence_rejected | delete | synthetic-partner |

Kept: `test_checker_subcommands_named_exist` and `test_checker_rules_named_exist` (both **exec**).

### Grammar-invariant files (4)

**loom-code/tests/test_acceptance_test_report_shape.py**
| function | action | tag |
|---|---|---|
| test_suite_criterion_cites_finalize_review_command | delete | pin |
| test_station_hands_tester_its_dismissals | delete | pin |
| test_late_dismissals_reach_the_pull_request | delete | pin |
| test_ship_lists_late_dismissals_in_verification | delete | pin |
| test_ship_names_handoff_as_late_dismissal_source | delete | pin |
| test_closing_review_handoff_reports_late_dismissals | delete | pin |
| test_dismissal_source_agrees_across_tester_and_template | delete | pin |
| test_rerun_retests_every_named_surface | delete | pin |
| test_partial_surface_retest_forbidden | delete | pin |
| test_rerun_dispatch_passes_earlier_report_evidence_and_fix_range | delete | pin |
| test_identifiers_confined_to_evidence_file_apart_from_pointer | delete | pin |
| test_rules_live_in_contract_and_template | prune (path pointers stay) | pin |
| test_no_full_suite_run_instruction | prune (last assert only; the absence half stays) | pin |

**loom-code/tests/test_lenses_deletion_first.py**
| function | action | tag |
|---|---|---|
| test_docs_lens_table_names_deletion_first | delete, or regex-ify the token | pin |
| test_skill_lens_paragraph_names_deletion_first | delete, or regex-ify the token | pin |
| test_deletion_first_definition_requires_the_smaller_shape_affirmatively | delete | pin |
| test_consecutive_cap_bumps_sentence_names_a_deletion_candidate | delete | pin |
| test_matcher_smaller_shape_sentence_affirmative_accepted | delete | synthetic-partner |
| test_matcher_smaller_shape_sentence_negated_rejected | delete | synthetic-partner |
| test_matcher_cap_bump_sentence_affirmative_accepted | delete | synthetic-partner |
| test_matcher_cap_bump_sentence_negated_rejected | delete | synthetic-partner |

**loom-code/tests/test_reviewer_mechanical_evidence.py**
| function | action | tag |
|---|---|---|
| test_reviewer_text_runs_changed_test_files_and_flags_skips | delete | pin |
| test_run_rule_excludes_adversarial_programs | delete | pin |
| test_skipped_changed_test_stays_a_finding | delete | pin |
| test_skipped_test_names_the_file_the_reviewer_ran | delete | pin |
| test_shell_builtin_adversarial_artifact_scores_tests_needs_revision | delete | pin |
| test_prose_evidence_sentence_present | delete | pin |
| test_prose_does_not_eliminate_behavior_evidence | prune (absences stay) | pin |
| test_severity_verdict_rules_once_in_lenses | delete | pin |
| test_suite_ban_holds_in_every_round | prune (the round-scope scan stays) | pin |
| test_ship_folds_nits_sentence_rejected | prune (the old-promise scan stays) | pin |
| test_no_reviewer_or_lens_text_requires_suite_run_or_downgrade | prune (the `"not grounds"` literal only) | pin |
| test_prose_pin_helpers_synthetic | prune (the `_skipped_test_is_finding` half) | synthetic-partner |

**loom-code/tests/test_write_plan_shape_text.py**
| function | action | tag |
|---|---|---|
| test_task_ids_use_one_numeric_form_without_reserved_process_tasks | prune (the `W<n>-memory` absence stays) | pin |
| test_confirmedIntent_skipsReferenceLoad | prune (file-exists check stays) | pin |
| test_questionsAsked_coversDecisionPointTwo | delete | pin |
| test_carried_details_force_minimal_spec | delete | pin |
| test_no_details_keeps_evidence_only_plan | delete | pin |
| test_write_plan_readback_leads_with_table_or_text_diagram | delete | pin |
| test_write_plan_readback_has_no_mermaid | prune (absence stays) | pin |
| test_both_stations_share_form_rules | delete | pin |
| test_template_placeholder_names_table_and_diagram | prune (placeholder shape stays) | pin |
| test_write_plan_confirmation_table_engineering_only | delete | pin |
| test_write_plan_no_details_no_table | delete | pin |
| test_write_plan_product_details_not_at_intent_confirmation | delete | pin |
| test_write_plan_only_explicit_yes_is_carried | delete | pin |
| test_write_plan_unanswered_proposal_dropped | delete | pin |
| test_write_plan_quotes_user_words | delete | pin |
| test_write_plan_background_context_and_inference_not_carried | delete | pin |
| test_product_non_visible_detail_on_requirement_line | delete | pin |
| test_write_plan_no_branch_ui_flows_not_forced_na | delete | pin |
| test_product_detail_not_on_design_decision | delete | pin |
| test_noPlanGate_forbidsConfirmingOnUsersBehalf | delete | pin |
| test_noConfirmOnUsersBehalf_pinHelper_synthetic | delete | synthetic-partner |
| test_affirmedPin_syntheticAffirmativeSentence_accepted | delete | synthetic-partner |
| test_affirmedPin_syntheticNegatedSentence_rejected | delete | synthetic-partner |
| test_affirmedPin_syntheticCodeSpanNo_notNegation | delete | synthetic-partner |
