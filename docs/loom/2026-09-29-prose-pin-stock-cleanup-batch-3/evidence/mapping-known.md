# Known-7 mapping (W1-01)

Defect class: a sentence pin, meaning an assert that passes only while one literal sentence or phrase of runtime prose keeps its exact wording. Each row maps a removed pin, or a group of pins guarding the same thing, to what still guards that defect.

"Lens" means `loom-code/skills/closing-review/references/lenses.md`. The skill lens scores `SKILL.md` and reference prose on the five docs dimensions plus `user-judgment-leak` and `deletion-first`. Every kept test named below exists after this edit. No row names a deleted function.

## loom-workflow/tests/loom-memory/test_skill_contract.py

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `::test_absent_store_and_empty_recall_are_normal_no_memory_results` (deleted) | an absent store or empty recall is reported as an error | skill lens, `inconsistency` (Recall's steps against its result wording) | review lens dimension |
| `::test_retire_requires_explicit_user_approval_before_deleting` (deleted) | Retire deletes a lesson without the user's approval | skill lens, `omission` (a delete step with no approval input) | review lens dimension |
| `::test_git_memory_boundary_is_stated` (deleted) | loom-memory and git-memory blur into one store, or one depends on the other | skill lens, `ambiguity`; `::test_no_fixed_station_mandatory_invocation` still bars station coupling | review lens dimension |
| `::test_no_bare_repo_root_relative_script_path` (pruned: "on any other host" + "levels above") | a file names `${CLAUDE_PLUGIN_ROOT}` with no root for other hosts | skill lens, `omission`; the same function keeps the paragraph check that every script path carries `${CLAUDE_PLUGIN_ROOT}` | review lens dimension |
| `::test_legacy_store_reported_needing_explicit_migration_without_modification` (deleted) | the skill silently migrates, reads or writes a legacy store | skill lens, `inconsistency` | review lens dimension |
| `::test_record_section_routes_unfinished_item_to_intent` (deleted) | Record routes an unfinished item somewhere other than an intent | `loom-workflow/tests/loom-memory/test_skill_contract.py::test_record_section_matches_the_digest_the_cold_reader_eval_was_run_against` (any Record edit goes red and re-runs `loom-workflow/skills/loom-memory/evals/record-timing.md`); `::test_backlog_entry_routing_sentence_rejected` keeps the backlog absence | kept structural test |
| `::test_the_reference_copy_still_carries_both_halves` (deleted) | `references/operations.md` drops Record's timing or scarcity half | skill lens, `inconsistency` (the reference copy against the `SKILL.md` Record section) | review lens dimension |

The orphaned `_A4_WHY` message constant went with the two Record-pin functions.

## loom-code/tests/test_architecture_doc_consumers.py

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `::test_write_plan_step5_reads_architecture_and_names_rule` (pruned: "Treat an unratified draft as advisory") | write-plan treats an unratified `ARCHITECTURE.md` draft as binding | skill lens, `inconsistency`; the same function keeps the `Risk line`/`rule id` terms and the `ratified-by: <name> <date>` line grammar | review lens dimension |
| `::test_absent_architecture_doc_adds_no_step` (deleted: "With no ARCHITECTURE.md, nothing changes" regex, "an implementer never changes a rule") | a missing `ARCHITECTURE.md` adds a step or blocks | checker rule `standing.warn` (a missing file prints the WARN and never blocks). The rule covers only the checker's never-block half; the "adds a step" half goes to skill lens `inconsistency` (write-plan's architecture step against the absent-file case) | checker rule id |
| `::test_code_lens_has_architecture_conformance_na_without_doc` (pruned: "Scored only for ratified rules"; the N/A lookup by the sentence "A dimension with nothing to conform to" re-anchored) | the lens scores unratified rules, or drops `N/A` for an absent doc | the same function: the lens-table row regexes and `ratified-by` grammar stay, and the `N/A` check is now re-anchored on the `## Severity and verdict` heading (some bullet there names both `` `N/A` `` and `` `ARCHITECTURE.md` ``). That guards the `N/A` half; the unratified-rules half goes to skill lens `inconsistency` | kept structural test |
| `::test_reviewer_lists_it_and_reviewer_count_unchanged` (pruned: "fails closed to two when it cannot classify the whole change") | closing-review's reviewer-count fallback changes | skill lens, `inconsistency` on closing-review; the same function keeps the reviewer `code` row check | review lens dimension |

## loom-workflow/tests/decision-map/test_skill_doc.py

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `::test_v3_contract_defines_multi_delivery_outcome_loop` (deleted) and the same three phrases in `::test_v3_public_surface_commands_templates_and_version_are_synchronized` | closing a delivery clears or completes the Map | skill lens, `inconsistency` (a close step against the Map-clear transition); no executable test drives a delivery close through to the Map-clear check | review lens dimension |
| `::test_v3_public_surface_commands_templates_and_version_are_synchronized` (pruned: "exactly three ticket closure types", "`grilling`, `research`, and `prototype`", "one outcome-advancing slice", "source of truth", and the route sentences "`destination` is exactly …", "`text` is non-empty after trimming", "only a `ticket` route may carry", "`grilling`, `research`, or `prototype`", "`(destination, text, ticket_slug)` is unique") | the documented ticket types and route rules drift from the code | the same function keeps the `ticket_template` grammar (`type: <grilling\|research\|prototype>`), the route-field names, the slug regex and `unique \`ticket_slug\``, and runs the documented commands. That guards the ticket types; the route rules beyond the field names (the destination set, non-empty text, ticket-only fields) go to skill lens `inconsistency` | kept structural test |
| same function (re-entry and phase sentences, not on the W0-01 list, found by reading) | the documented re-entry states and legacy phases drift from `_implemented_reentry_states()` / `_implemented_delivery_phases()` | the same function now asserts each implemented value appears as a code token in `SKILL.md` and `map-format.md` | kept structural test |
| same function (risk step located by the sentence "Before every close-time gate, run the risk-front-loading pass", not on the list) | the risk pass moves after the validate command | the same function now finds the `risk-front-loading` term under the existing `## Close-time checks` heading and keeps the ordering check | kept structural test |
| `::test_v3_contract_pins_release_boundary_and_metric_definition` (pruned: "Exactly three ticket closure types exist", "Dependencies are graph edges, not ticket types", "A closed delivery alone is never a clear transition") | map-format restates the v3 boundary wrongly | skill lens, `inconsistency`; the same function keeps `schema_version: 3` and the `v1` absence | review lens dimension |

## loom-workflow/tests/loom-visualization/test_references.py

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `::test_affirmative_option_and_yes_no_rules_accepted`, `::test_negated_option_rule_rejected`, `::test_metaphor_ban_removed_rejected` (deleted), the `polarity_errors` line of `::test_guide_has_seven_rules_and_rewrite_steps` (pruned) | rule 3's metaphor ban or rule 5's option and yes-or-no sentences flip polarity | skill lens, `inconsistency`; `loom-workflow/tests/scripts/test_visualization_card_hook.py` keeps its own `rule_polarity_errors` scan over the card; `::test_guide_has_seven_rules_and_rewrite_steps` keeps `guide_errors` (seven rules, five steps, metaphor check last) | review lens dimension |
| `::test_option_rule_two_alternatives_and_recommendation`, `::test_yes_no_confirmation_asked_directly`, `::test_each_missed_alternative_included_or_ruled_out` (deleted) | rule 5 loses its alternatives, recommendation, yes-or-no or ruled-out clauses | `loom-workflow/tests/loom-visualization/test_references.py::test_rule_five_example_is_a_table` (rule 5's example is a Decision consequences table with a recommended row); the yes-or-no and ruled-out clauses go to skill lens `omission` | kept structural test |
| `::test_rule_five_scope_matches_card` (deleted) | the guide's rule 5 scope and the card's inline rule diverge | skill lens, `inconsistency` (guide against card) | review lens dimension |
| `::test_rewrite_opens_with_conclusion_and_keeps_facts` (pruned: `KEEP_FACTS_PHRASES`, "never what happened") | the rewrite steps stop keeping facts | skill lens, `omission`; the same function keeps the conclusion-first `guide_errors` check | review lens dimension |
| `::test_reply_keeps_user_script` (deleted) | the guide stops keeping the user's script (Traditional vs Simplified) | skill lens, `omission` | review lens dimension |
| `::test_skill_md_names_unstructured_multiline_box_failure_mode` (deleted) | `SKILL.md` stops naming the separator-less multi-line box failure | skill lens, `omission` (the failure-mode list against `references/node-structure.md`). `loom-workflow/tests/loom-visualization/test_references.py::test_skill_md_points_to_node_structure_reference` checks only that `SKILL.md` still points at `references/node-structure.md`; it does not fail when the failure mode goes unnamed | review lens dimension |

The orphaned `polarity_errors`, `_sentence_with`, `NEGATION`, `DECISION_PHRASES`, `DECISION_SCOPE` and `KEEP_FACTS_PHRASES` went with these rows. The hook test's own `DECISION_SCOPE` and `rule_polarity_errors` are separate and untouched.

## loom-workflow/tests/handoff/test_handoff_schema.py

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `::test_resume_launcher_section_present_and_constrained` (pruned: "thin", "portable", "no stale embeds" anchors) | the launcher spec drops its three constraints | skill lens, `omission`; the same function keeps the Resume Launcher heading and `USER DIRECTIVE` field | review lens dimension |
| same function ("good example — resume launcher", "bad example — resume launcher") | an example goes missing | re-anchored: the same function now matches both as `###` headings | kept structural test |
| `::test_conversation_language_captured_and_propagated` (pruned: "reply to me in the conversation language") | the launcher stops telling the next session which language to reply in | skill lens, `omission`; the same function keeps the `conversation_language` field check | review lens dimension |

## loom-workflow/tests/goal-create/test_goal_shape.py

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `::test_defines_four_fields_budget_and_surfacing` (pruned: "must not change", "surfaced in the conversation", "runs no commands", "opens no files", "one compression pass", "not an error") | the four-field definitions or the 1,500 advisory lose their meaning | skill lens, `inconsistency`; the same function keeps field order, `goal evaluator`, the budget numbers, `advisory`, the budget-section caveat and the vendor URLs. The file-pointer rule is now review-only: W1-07 pruned its regex (`mapping-residual.md`) | review lens dimension |

## tests/test_loom_skill_description_catalog.py

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `::test_router_tables_preserve_direct_leaf_targets_and_goal_boundary` (pruned: "must be invoked by name", "Do not select `goal-create` from an inferred need or an unnamed goal request") | goal-create gets selected without being named | skill lens, `inconsistency` and `omission` (goal-create's description and the router table against the explicit-only rule). `tests/test_loom_skill_description_catalog.py::test_routing_corpus_covers_positive_boundary_and_non_trigger_cases` is only a fixture check: it checks the routing-corpus cases against each other and never reads the description or the router table | review lens dimension |

## Test cases

- **A2 positive, structure-and-grammar-checks-kept.** The kept checks are the structure, absence, grammar and exec checks named in the replacement column. The 7 files pass alone: 60 passed.
- **A2 negative, suite-green-after-prune.** `loom-workflow/tests` exit 0 (1020 passed, 3 skipped, run with `--import-mode=importlib`), `loom-code/tests` exit 0 (1835 passed, 2 skipped), root `tests` exit 0 (210 passed).
- **A3 positive, mapping-row-per-removed-pin.** Every row of the deletion list's "Known 7 files" section has a row here. Two extra rows cover pins found by reading `test_skill_doc.py` that the list did not name.
- **A3 negative, no-row-names-deleted-test.** Every function named in a replacement column exists after the edit.
