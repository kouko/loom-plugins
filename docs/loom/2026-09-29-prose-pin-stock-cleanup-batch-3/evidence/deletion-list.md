# Batch 3 deletion list (W0-01)

**A5 exec baseline (base-5704cc23-exec-recount-recorded): base `5704cc23` has 1925 executing test functions.**

Command: `python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --count-exec <wt>`, with `<wt>` from `git worktree add --detach <scratchpad>/wt-base 5704cc23`, removed afterwards. The base's own classifier and the W0-01 classifier both print 1925. W0-01 moved the production-name lookup into `_production_names` without changing it. This matches the batch-2 report's HEAD count.

## Widened census

The classifier now also sees a **direct sentence pin**: a literal of three or more words, asserted with `in`, `==`, `.startswith()`, `.endswith()` or `.count(...) >= 1` against text read from a markdown file. The file must name a skill, agent or reference path. No prose-helper import is needed. Program output does not count: subprocess output, `readouterr`, json or yaml parsing, `tmp_path` files, production calls, and local validators named `*errors*`, `validate`, `check` and the like. Headings, table rows, commands and paths do not count either. The full heuristic is in the `direct_pin_lines` docstring.

Census from a clean worktree (HEAD `0001ad25` plus the W0-01 classifier), exit 0:
`{'behavior': 108, 'gate-eval': 1, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 9, 'structure': 56}`. Before W0-01: `sentence-pin 0, gate-eval 0, structure 66`.

- `has_pins=yes`: 19 → 39 files. That is 20 newly flagged files: 6 of the known 7, plus 14 found by the widening. The seventh known file, `decision-map/test_skill_doc.py`, was already flagged through its loop form.
- All 7 known files are flagged now.
- Every newly flagged file has at least one prose literal, so every one is listed below for pruning. **No `MANUAL_OVERRIDES` row was added.**
- The `gate-eval` file is `loom-workflow/tests/decision-map/test_decision_map_intent_binding.py`. A `mechanisms.yaml` eval names that whole file, as it also names `loom-memory/test_skill_contract.py`, `scripts/test_visualization_card_hook.py` and `tests/test_loom_skill_description_catalog.py`. W0-02 checks these before any pruning.

Columns: action is `delete` (every assert is a pin) or `prune` (drop the listed pins and keep the rest). The tag `pin` is a sentence pin. `synthetic-partner` is a test that only exercises a pin helper on edited text. `exec` means the function runs a program, so it is pruned, never deleted. Line numbers are at `0001ad25`.

## Known 7 files

| file::function | action | tag | pinned literal(s) |
|---|---|---|---|
| `loom-workflow/tests/loom-memory/test_skill_contract.py::test_absent_store_and_empty_recall_are_normal_no_memory_results` | delete | pin | "normal no-memory result" (117) |
| `…/test_skill_contract.py::test_retire_requires_explicit_user_approval_before_deleting` | delete | pin | "explicit user approval before deleting" (122) |
| `…/test_skill_contract.py::test_git_memory_boundary_is_stated` | delete | pin | "commit- and pull-request-bound", "outlive a change", "runtime dependency of the other" (164-166) |
| `…/test_skill_contract.py::test_no_bare_repo_root_relative_script_path` | prune | pin | "on any other host" + "levels above" (215); `${CLAUDE_PLUGIN_ROOT}` check stays |
| `…/test_skill_contract.py::test_legacy_store_reported_needing_explicit_migration_without_modification` | delete | pin | "without modifying any file", "never reads or writes that legacy format itself" (233-234) |
| `…/test_skill_contract.py::test_record_section_routes_unfinished_item_to_intent` | delete | pin | "an unfinished item belongs in an intent." (358) |
| `…/test_skill_contract.py::test_the_reference_copy_still_carries_both_halves` | delete | pin | operations.md "before the branch closes", "not a durable lesson" (379, 382) |
| `loom-code/tests/test_architecture_doc_consumers.py::test_write_plan_step5_reads_architecture_and_names_rule` | prune | pin | "Treat an unratified draft as advisory" (34); `ratified-by: <name> <date>` (33) is line grammar, W1 judges |
| `…/test_architecture_doc_consumers.py::test_absent_architecture_doc_adds_no_step` | delete | pin | "an implementer never changes a rule" (40), plus the "With no ARCHITECTURE.md, nothing changes" regex |
| `…/test_architecture_doc_consumers.py::test_code_lens_has_architecture_conformance_na_without_doc` | prune | pin | "Scored only for ratified rules" (50); lens-table row regexes stay |
| `…/test_architecture_doc_consumers.py::test_reviewer_code_row_lists_architecture_conformance` (was `test_reviewer_lists_it_and_reviewer_count_unchanged`) | prune | pin | "fails closed to two when it cannot classify the whole change" (61); reviewer row token stays |
| `loom-workflow/tests/decision-map/test_skill_doc.py::test_v3_contract_defines_multi_delivery_outcome_loop` | delete | pin | "one persistent outcome-control loop", "multiple independently closed delivery arcs", "Closing a delivery arc must not clear the Map." (181-183) |
| `…/test_skill_doc.py::test_v3_public_surface_commands_templates_and_version_are_synchronized` | prune | exec | map-format route sentences (216-221, e.g. "`text` is non-empty after trimming"), public-contract phrases (281-287); commands, manifests, version and route-field checks stay |
| `…/test_skill_doc.py::test_map_format_declares_schema_version_3_without_v1` (was `test_v3_contract_pins_release_boundary_and_metric_definition`) | prune | pin | "Exactly three ticket closure types exist", "Dependencies are graph edges, not ticket types", "A closed delivery alone is never a clear transition" (310-312); `schema_version: 3` and the `v1` absence stay |
| `loom-workflow/tests/loom-visualization/test_references.py::test_affirmative_option_and_yes_no_rules_accepted` | delete | pin | `polarity_errors` finds rule sentences by their opening words (117-125): "Do not use metaphors or analogies, and do not reach for", "is asked directly", "lists at least two workable alternatives…" |
| `…/test_references.py::test_negated_option_rule_rejected` | delete | synthetic-partner | `polarity_errors` on a flipped rule 5 |
| `…/test_references.py::test_metaphor_ban_removed_rejected` | delete | synthetic-partner | `polarity_errors` on a removed rule 3 ban (154) |
| `…/test_references.py::test_guide_has_seven_rules_and_rewrite_steps` | prune | pin | the `polarity_errors` line (160); `guide_errors` and the section checks stay |
| `…/test_references.py::test_option_rule_two_alternatives_and_recommendation` | delete | pin | `DECISION_PHRASES` (174, e.g. "do nothing or later", "why there is no third"), "Nutt"/"Chernev" |
| `…/test_references.py::test_rule_five_scope_matches_card` | delete | pin | `DECISION_SCOPE` "asking or answering how to do something" in the guide and the trigger card (229, 231) |
| `…/test_references.py::test_yes_no_confirmation_asked_directly` | delete | pin | "no invented alternatives" + "asked directly" (282) |
| `…/test_references.py::test_rewrite_opens_with_conclusion` (was `test_rewrite_opens_with_conclusion_and_keeps_facts`) | prune | pin | `KEEP_FACTS_PHRASES` (301), "never what happened" (304); the `guide_errors` check stays |
| `…/test_references.py::test_each_missed_alternative_included_or_ruled_out` | delete | pin | "For each of the three", "one short clause", not "If only two" (319-320) |
| `…/test_references.py::test_reply_keeps_user_script` | delete | pin | "Reply in the user's language and script: Traditional Chinese stays…" (325) |
| `…/test_references.py::test_skill_md_names_unstructured_multiline_box_failure_mode` | delete | pin | "without a separator" / "no separator", "unstructured" (735) |
| `loom-workflow/tests/handoff/test_handoff_schema.py::test_resume_launcher_section_has_directive_and_example_headings` (was `test_resume_launcher_section_present_and_constrained`) | prune | pin | ("thin", "portable", "no stale embeds") anchors (167); "good example — resume launcher", "bad example — resume launcher" (175, 178; example labels, W1 judges); the heading regex stays |
| `…/test_handoff_schema.py::test_conversation_language_captured_in_frontmatter` (was `test_conversation_language_captured_and_propagated`) | prune | pin | "reply to me in the conversation language" (207); the `conversation_language` field check stays |
| `tests/test_loom_skill_description_catalog.py::test_router_tables_preserve_direct_leaf_targets` (was `test_router_tables_preserve_direct_leaf_targets_and_goal_boundary`) | prune | pin | "must be invoked by name", "Do not select `goal-create` from an inferred need or an unnamed goal request" (167-168); router link checks stay |
| `loom-workflow/tests/goal-create/test_goal_shape.py::test_defines_four_fields_and_budget` (was `test_defines_four_fields_budget_and_surfacing`) | prune | pin | "must not change", "surfaced in the conversation", "runs no commands", "opens no files", "one compression pass", "not an error" (73, 78, 84, 87, 107-108) |

When the four `test_references.py` rows above are deleted, the `polarity_errors` helper is left orphaned.

## Newly flagged

There are 14 files, which is more than ~10, so they are grouped into disjoint per-plugin buckets for W1-05 onward. Every row is a prose literal read from a skill, agent or reference file. No function runs a program.

### Bucket loom-code (5 files)

| file::function | action | tag | pinned literal(s) |
|---|---|---|---|
| `loom-code/tests/test_agent_model_frontmatter.py::test_module_contract_rejects_retired_dispatch_ledger_wording` | prune | pin | dispatch-profile.md "active task context only" (48); the two absences stay |
| `loom-code/tests/test_dispatch_profile_resolver.py::test_contract_defines_the_executable_json_boundary` | prune | pin | "on any other host", "pass the resolver's deterministic JSON result to the host-native spawn", "post-execution capability-quality failure", "pre-execution host rejection" (467-477); command shapes and JSON event keys stay |
| `…/test_dispatch_profile_resolver.py::test_stations_point_to_the_executable_resolver_contract` | prune | pin | "on any other host it is the directory two levels above this SKILL.md" (485); the link and absences stay |
| `loom-code/tests/test_legacy_contract_removed.py::test_implementer_has_no_per_task_package_suite_wording` (was `test_implementer_runs_focused_tests_not_the_package_suite`) | prune | pin | "The complete package suite runs at the end of Build and again in `finalize-review`, never per task." (175); absences stay |
| `loom-code/tests/test_probes_language_policy.py::test_reviewer_nitclause_absent` | prune | pin | reviewer.md "style is out of scope" (138) |
| `loom-code/tests/test_ship_worktree_merge.py::test_ship_accepted_land_renders_absolute_worktree_in_command` | prune | pin | "never rely on the Bash tool's workdir" (20); the command shape stays |

### Bucket loom-design (2 files)

| file::function | action | tag | pinned literal(s) |
|---|---|---|---|
| `loom-design/tests/interface/test_knowledge_triage.py::test_triage_names_shaping_and_deferrable_tiers` (was `test_high_bar_shaping_criteria_present`) | prune | pin | "semantic display convention" (105; a criterion term, and the two-word needles beside it are the same kind, so W1 judges the whole function) |
| `…/test_knowledge_triage.py::test_shaping_supplement_present_verbatim` | delete | pin | `SHAPING_SUPPLEMENT` "SHAPING never ships as non-blocking…", count == 1 (229) |
| `…/test_knowledge_triage.py::test_tier_label_supplement_present_verbatim` | delete | pin | `TIER_LABEL_SUPPLEMENT` "Every tagged open question written into DESIGN.md must carry…", count == 1 (290) |
| `…/test_knowledge_triage.py::test_shaping_supplement_after_pin_never_inside`, `::test_tier_label_supplement_after_first_supplement` | W1 judges | pin | locate the same two sentences by `.index()`; the detector does not see this form; they break when the supplements go |
| `loom-design/tests/principles/test_principles_ratified_line.py::test_interview_template_path_is_referenced` (was `test_interview_template_referenced_not_copied`) | prune | pin | "the interview is the same one" (153); the template path pointer stays |

### Bucket loom-workflow (6 files)

| file::function | action | tag | pinned literal(s) |
|---|---|---|---|
| `loom-workflow/tests/decision-map/test_decision_map_intent_binding.py::test_skill_lists_the_intent_status_values` (was `test_delivery_state_derives_from_the_intent_status`) | prune | pin | "Delivery state is derived from the intent's own `status:` field", "The Map is read-only on intents" (39, 42); the status tokens stay |
| `…/test_decision_map_intent_binding.py::test_map_lists_the_change_id_under_its_criterion` | prune | pin | "opens no second arc" (51); the `- delivery-intent:` line shape (49) is a format label and stays |
| `…/test_decision_map_intent_binding.py::test_no_delivery_ticket_is_authored_any_more` | prune | pin | "Exactly three ticket closure types exist" (58); the `\|delivery>` absence stays |
| `loom-workflow/tests/git-memory/test_loom_delegation.py::test_delegated_heading_precedes_direct_heading_in_commit_protocol_only` (was `test_loom_closeout_delegation_does_not_reconfirm_authorized_publish`) | prune | pin | "privacy gate PASS", "Privacy BLOCK remains a required human stop", "git-memory never re-confirms a Loom publication", "canonical intent authorization or a single legacy Ship decision", "Do not create a `## Memory` top-level section", "direct git-memory invocation" (30-46), plus two sentence regexes the detector does not see; heading order stays |
| `…/test_loom_delegation.py::test_privacy_spec_names_the_bypass_trailer` (was `test_privacy_judge_only_runs_for_ambiguous_private_party_text`) | prune | pin | "do not dispatch" (52); the `Privacy-Bypass-Reason:` trailer label stays |
| `…/test_loom_delegation.py::test_both_protocols_name_the_bypass_trailer` (was `test_bypass_never_applies_to_deterministic_secret_findings`) | prune | pin | "never bypasses a layer-1 secret finding" (61); the trailer label stays |
| `loom-workflow/tests/loom-visualization/test_skill_script_paths.py::test_each_skill_calls_a_script_through_skill_dir` (was `test_skill_dir_phrase_defined_and_used_for_every_script_call`) | prune | pin | "`<skill-dir>` is this skill's folder", "`${CLAUDE_SKILL_DIR}` on Claude Code", "on any other host, the directory that holds this SKILL.md" (30-32); the script-call regex stays |
| `…/test_skill_script_paths.py::test_non_skill_docs_using_the_token_point_to_skill_md` | delete | pin | "defined in `SKILL.md`" (63; a pointer phrase, W1 judges) |
| `loom-workflow/tests/loom-visualization/test_templates.py::test_shaped_content_defaults_to_a_markdown_table` | prune | pin | `pinned_sentence_ok(…, *TABLE_DEFAULT_PIN)`, which the detector does not see. "Form in a chat reply" (323) is a table column header and stays. If it is kept, the file needs an override row after pruning |
| `…/test_templates.py::test_every_ascii_section_names_its_destination_condition` | delete | pin | "does not render markdown" (406) |
| `loom-workflow/tests/recap-state/test_seven_block_schema.py::test_l3_contract_defines_goal_grounded_natural_output` | prune | pin | "Support counts as known only" (190); headings, absences and path pointers stay |
| `loom-workflow/tests/scripts/test_visualization_card_hook.py::test_coexist_card_has_no_bare_skip_it` (was `test_coexist_card_skip_sentence_names_the_skill`) | prune | pin | "Skip loom-visualization for one-paragraph answers" (558); the "Skip it" absence stays |

### Bucket root tests (1 file)

| file::function | action | tag | pinned literal(s) |
|---|---|---|---|
| `tests/test_loom_plugin_install_layout.py::test_lookup_table_lives_in_one_place_and_every_skill_links_it` (was `test_sibling_lookup_allows_version_subdirectory`) | prune | pin | "on any other host", "two levels above this SKILL.md", "may contain one version subdirectory", "use the newest" (640-643); the link counts and pointer stay |

## W3-01 output-taint fix round

Defect class: a direct prose pin hidden from the census because its markdown read is misclassified as program output. Two gaps: a helper that calls `yaml.safe_load` anywhere made its whole return value output, so a body sentence asserted against that helper's return was not flagged; and a skill file read from a plugin copy installed under `tmp_path` counted as temp-dir output. After the fix, only a parsed value is output, and a plain read of a skill, agent or reference path is prose even under a temp dir. A census rerun from a clean worktree newly flags exactly these 2 files, plus the graduated adversary program, which gets a `MANUAL_OVERRIDES` row because its hit is a synthetic source string, not prose. No function was deleted. Line numbers are at `9b6579c2`.

| file::function | action | tag | pinned literal(s) |
|---|---|---|---|
| `loom-workflow/tests/distill-sessions/test_prompts_parseable.py::test_failure_prompt_structure` | prune | pin | "never mention ground truth" (156), "no more than 3" / "max 3" / "maximum of 3" (163-165); the common shape and role check stay |
| `…/test_prompts_parseable.py::test_success_prompt_structure` | prune | pin | "no more than 3" / "max 3" / "maximum of 3" (194-196); "Lean Solution Path" (179) is re-anchored on its existing `## Lean Solution Path output format` heading; the dead-end marker words stay |
| `…/test_prompts_parseable.py::_assert_common_shape` | prune | pin | "How the orchestrator dispatches this prompt" (135) is re-anchored on its existing `## ` heading; frontmatter keys, model, step markers and Memory Item fields stay |
| `…/test_prompts_parseable.py::test_advisory_prompt_structure` | prune | pin | "fenced code block" (292), redundant with the kept `code block` term in the same assert |
| `…/test_prompts_parseable.py::test_both_prompts_forbid_orchestrator_memory_reference` | prune | pin | "never reference the orchestrator's project memory" (454) in the body; "orchestrator's project memory" (447), redundant with the kept frontmatter `project memory` check in the same assert |
| `tests/test_loom_plugin_install_layout.py::test_isolated_loom_plugins_are_standalone_and_compose_by_public_contract` | prune | exec | "negative or boundary" with "positive" (430), "closing-review station once at branch end" (431), read from the installed write-plan `SKILL.md`; the boundary-violation run, dependency checks and `docs/loom/` path pointers stay |
