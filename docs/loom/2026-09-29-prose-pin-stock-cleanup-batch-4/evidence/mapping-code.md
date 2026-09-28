# Prose-candidate mapping for loom-code and root tests (W1-01)

Scope: every prose candidate `candidate-list.md` gives for a file under `loom-code/tests/` or root `tests/`, 38 rows in 14 files. Each is judged below before any edit. The structural rows of these files classed "capitalized label" or "1-2 word" were re-checked as well. They are `Recording` and `Reuse first, update with evidence` (`## ` headings in `adversarial.md`), `Antigravity CLI` (a table header in `antigravity-tools.md`), `TypeName: "self"` (a code token), `Risk line` (the plan's task field) and `→ Acceptance #` (the REQ suffix grammar). All six stay structural.

"Skill lens" and "docs lens" mean `loom-code/skills/closing-review/references/lenses.md`. The skill lens scores `SKILL.md`, agent and reference prose on the five docs dimensions.

## Decisions

| # | file:line | function | literal / form | decision | reason |
|---|---|---|---|---|---|
| 1 | tests/test_loom_skill_description_catalog.py:165 | test_router_tables_preserve_direct_leaf_targets | `'direct'` | prune | the word "direct" in router prose; the link-set checks in the same function stay |
| 2 | loom-code/tests/test_acceptance_test_report_shape.py:73 | test_template_has_one_row_per_criterion_and_evidence_file_path | `works\|partly\|not verified\|fails` | keep-structural | the enum values of the Verdict column, the same value set as the tester's `result:` field grammar (acceptance-tester.md:94) |
| 3 | loom-code/tests/test_acceptance_test_report_shape.py:118 | test_row_has_carried_over_marker_with_reason | `^carried over — \S.*$` | keep-structural | Re-run cell grammar `carried over — <reason>`, a fixed value the tester writes (backticked at acceptance-tester.md:68) |
| 4 | loom-code/tests/test_acceptance_test_report_shape.py:127 | test_retested_row_has_no_carry_reason | `'re-tested'` | keep-structural | the other enum value of the Re-run column |
| 5 | loom-code/tests/test_acceptance_test_report_shape.py:231 | _template_verdicts | `Verdict is one of ...` | delete | the scan locates the list by a sentence, and no heading or gate marker encloses it (P2). Its only user, `test_verdictvocabulary_returnedset_equalstemplateset`, and the orphaned `_norm` go too |
| 6 | loom-code/tests/test_acceptance_test_report_shape.py:247 | test_verdictvocabulary_untriedline_usestemplateword | `An Acceptance line you could not try is ...` | delete | sentence anchor, no heading or gate marker (P2) |
| 7 | loom-code/tests/test_adversary_layout.py:152 | _base_commit | `at commit \`<sha>\`` | keep-structural | reads the frozen evidence record `rule-correspondence.md` under `docs/loom/`, not skill, agent or reference prose; the sha feeds a `git show` subprocess (rule 4) |
| 8 | loom-code/tests/test_adversary_layout.py:162 | _split_commit | `at split commit \`<sha>\`` | keep-structural | same as row 7 |
| 9 | loom-code/tests/test_adversary_layout.py:321 | test_protocol_keeps_no_recipe_body | `'Reuse first, update with evidence'` | keep-structural | heading text: `## Reuse first, update with evidence` in adversarial.md:73 |
| 10 | loom-code/tests/test_adversary_layout.py:409 | test_correspondence_note_maps_every_rule_to_a_file_that_exists | `'(preamble)'` | keep-structural | a sentinel cell value in the frozen correspondence note table, not runtime prose |
| 11 | loom-code/tests/test_adversary_protocol.py:73 | test_agent_return_block_carries_the_three_counts | `'committed'` | keep-structural | a YAML key of the return block `attack_points: {found:, earned_a_program:, committed:}` (adversary.md:58) |
| 12 | loom-code/tests/test_adversary_protocol.py:73 | test_agent_return_block_carries_the_three_counts | `'found'` | keep-structural | same as row 11 |
| 13 | loom-code/tests/test_adversary_protocol.py:193 | _head_is_a_case | `\bcases?\b\|\bprobes?\b\|...` | keep-structural | head-noun vocabulary of the case-count scan. The scan flags a restated floor anywhere and a ceiling outside its one home, and holds the number to `MAX_PROBE_PROGRAMS`. It is absence and one-home, so rewording the prose keeps it green |
| 14 | loom-code/tests/test_architecture_doc_consumers.py:31 | test_write_plan_step5_reads_architecture_and_names_rule | `'rule id'` | prune | a two-word phrase of Step 5 prose. `Risk line` (plan field) and `ratified-by: <name> <date>` (grammar) stay |
| 15 | loom-code/tests/test_architecture_doc_consumers.py:51 | test_reviewer_code_row_lists_architecture_conformance | `'architecture-conformance'` | keep-structural | a dimension id: the first cell of a row in the lenses.md code table |
| 16 | loom-code/tests/test_build_mechanical_checks.py:46 | _other_role_program_edit_sentences | `'adversarial program'` | keep-absence | absence scan: flags an added sentence in which another role edits a program; rewording existing prose cannot turn it red |
| 17 | loom-code/tests/test_build_mechanical_checks.py:114 | _implementer_floor_sentences | `'floor'` | keep-absence | absence scan (no un-negated implementer-floor sentence) |
| 18 | loom-code/tests/test_build_mechanical_checks.py:158 | _dead_pointer_hits | `attack[- ]catalogue\|...` | keep-absence | absence scan for retired pointers |
| 19 | loom-code/tests/test_build_recovery_rules.py:121 | _mapping_restatements | artifact-noun regex | keep-absence | one-home absence scan: no second copy of the artifact-to-station mapping inside the gate block |
| 20 | loom-code/tests/test_build_recovery_rules.py:122 | _mapping_restatements | producer-phrase regex | keep-absence | same as row 19 |
| 21 | loom-code/tests/test_closing_review_recovery_rules.py:102 | _mapping_restatements | artifact-noun regex | keep-absence | same as row 19 |
| 22 | loom-code/tests/test_closing_review_recovery_rules.py:103 | _mapping_restatements | producer-phrase regex | keep-absence | same as row 19 |
| 23 | loom-code/tests/test_dispatch_profile_resolver.py:471 | test_contract_defines_the_executable_json_boundary | `'capabilities'` | keep-structural | a JSON input key of the resolver boundary (`"capabilities": {` at dispatch-profile.md:49), next to the kept `"event"` keys |
| 24 | loom-code/tests/test_lenses_deletion_first.py:22 | test_reviewer_docs_row_ends_with_deletion_first | `'deletion-first'` | keep-structural | the dimension token that ends a table row |
| 25 | loom-code/tests/test_lenses_deletion_first.py:34 | test_reviewer_skill_row_ends_with_deletion_first | `'deletion-first'` | keep-structural | same as row 24 |
| 26 | loom-code/tests/test_probes_language_policy.py:137 | test_reviewer_nitclause_absent | `'docs-lint'` | keep-structural | a KICKOFF-DEFAULTS field key `docs-lint: <command>` (reviewer.md:81) |
| 27 | loom-code/tests/test_probes_language_policy.py:227 | _has_negation | `\b(?:not\|never\|no)\b\|n't` | keep-structural | the negation token set of a polarity check |
| 28 | loom-code/tests/test_probes_language_policy.py:238 | _sentence_affirmatively_names_shape | `'is named'` | prune | a naming-verb phrase; the literal shape plus the no-negation polarity stay |
| 29 | loom-code/tests/test_probes_language_policy.py:238 | _sentence_affirmatively_names_shape | `'must be named'` | prune | same as row 28 |
| 30 | loom-code/tests/test_probes_language_policy.py:238 | _sentence_affirmatively_names_shape | `'name is'` | prune | same as row 28 |
| 31 | loom-code/tests/test_probes_language_policy.py:238 | _sentence_affirmatively_names_shape | `'named'` | prune | same as row 28 |
| 32 | loom-code/tests/test_probes_language_policy.py:245 | _sentence_affirmatively_requires_english | `'are in english'` | prune | phrase form. The helper goes, and English stays as the concept noun `english` in the same paragraph, the form `test_stations_english_absent` uses |
| 33 | loom-code/tests/test_probes_language_policy.py:245 | _sentence_affirmatively_requires_english | `'in english'` | prune | same as row 32 |
| 34 | loom-code/tests/test_probes_language_policy.py:245 | _sentence_affirmatively_requires_english | `'is in english'` | prune | same as row 32 |
| 35 | loom-code/tests/test_reviewer_mechanical_evidence.py:156 | test_no_reviewer_or_lens_text_requires_suite_run_or_downgrade | `\b(never\|not\|no)\b` | keep-structural | the negation token set of a polarity check (a sentence naming the suite must keep it out of the reviewer's hands) |
| 36 | loom-code/tests/test_sync_before_review_text.py:126 | test_no_op_sync_dispatches_without_rerun | `'sync-trunk'` | keep-structural | a script subcommand name, counted for one home |
| 37 | loom-code/tests/test_write_plan_station_text.py:110 | lane_hits | lane regex | keep-absence | absence scan (no runtime file names a lane) |
| 38 | loom-code/tests/test_write_plan_station_text.py:157 | test_suggest_station_names_every_policy_input_key | `with exactly these keys:(.*?)\bto:` | prune | re-anchored on the existing heading `### Resolve \`second-vendor: suggest\`` (P2). Every backticked key in that section is now read, and the policy's accepted fields must all be among them |

| 39 | loom-code/tests/test_probes_language_policy.py:231 | _paragraph_names_shape_and_english | `'english'` | keep-structural | new after the edit: the replacement for rows 32-34. It is the concept noun naming the language the policy requires, not a clause, and the same word `test_stations_english_absent` already checks |

Totals over the 38 listed rows: pruned 10 rows (4 functions pruned, and the helper `_sentence_affirmatively_requires_english` deleted with rows 32-34), deleted 2 rows (2 test functions, 2 helpers), kept 26 rows (18 structural, 8 absence). Row 39 is the one candidate the edit adds. After the edit the classifier shows 27 prose candidates in these files, rows 2-4, 7-13, 15-27, 35-37 and 39, each kept for the reason above.

## Mapping

One row per removed pin, or per group of pins that guarded the same thing.

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `tests/test_loom_skill_description_catalog.py::test_router_tables_preserve_direct_leaf_targets` (pruned `"direct" in router`) | the router stops presenting its leaf links as direct targets | `tests/test_loom_skill_description_catalog.py::test_router_tables_preserve_direct_leaf_targets`: every leaf is still linked exactly once as `](../<leaf>/SKILL.md)`, the router links nothing else, and no link repeats | kept structural test |
| `loom-code/tests/test_acceptance_test_report_shape.py::test_verdictvocabulary_returnedset_equalstemplateset`, `::test_verdictvocabulary_untriedline_usestemplateword`, `::_template_verdicts`, `::_norm` (deleted) | the template's verdict list, the tester's `result:` values and the untried-line verdict drift apart | docs lens `inconsistency` (tester contract against the report template). The Verdict cells of the template rows still have to be one of the four enum values in `::test_template_has_one_row_per_criterion_and_evidence_file_path` | review lens dimension |
| `loom-code/tests/test_architecture_doc_consumers.py::test_write_plan_step5_reads_architecture_and_names_rule` (pruned `"rule id" in para`; renamed) | write-plan Step 5 stops asking for the ARCHITECTURE.md rule id on the Risk line | skill lens `omission`. `loom-code/tests/test_architecture_doc_consumers.py::test_write_plan_step5_names_architecture_risk_line_and_ratification` still requires the Step 5 ARCHITECTURE.md paragraph, `Risk line` and `ratified-by: <name> <date>` | review lens dimension |
| `loom-code/tests/test_probes_language_policy.py::_sentence_affirmatively_names_shape` (pruned the naming-verb phrases; renamed), `::_sentence_affirmatively_requires_english` (deleted), `::_paragraph_names_shape_and_requires_english` (renamed) | the agents stop naming the probe shape affirmatively, or stop requiring English docstrings and evidence | `loom-code/tests/test_probes_language_policy.py::test_agents_probename_absent`: a paragraph still needs an un-negated sentence carrying `test_<unit>_<state>_<expected>` plus the word English. The verb wording and the polarity of the English half go to skill lens `ambiguity` | kept structural test |
| `loom-code/tests/test_probes_language_policy.py::test_ProbenameHelper_SyntheticParagraphs_Discriminates` (pruned the no-naming-verb case) | the helper accepts the literal with no naming verb | skill lens `ambiguity`. The same function keeps the real-sentence and the negated-paragraph cases | review lens dimension |
| `loom-code/tests/test_write_plan_station_text.py::test_suggest_station_names_every_policy_input_key` (pruned the `with exactly these keys:` sentence anchor) | the station's key list drifts from `second_vendor_policy.py`'s accepted fields | `loom-code/tests/test_write_plan_station_text.py::test_suggest_station_names_every_policy_input_key`: every accepted field must still be a backticked key under the `### Resolve \`second-vendor: suggest\`` heading. The "exactly, no extra key" half goes to skill lens `inconsistency` | kept structural test |

## Renames

- `test_write_plan_step5_reads_architecture_and_names_rule` -> `test_write_plan_step5_names_architecture_risk_line_and_ratification` (loom-code/tests/test_architecture_doc_consumers.py)
- `_sentence_affirmatively_names_shape` -> `_sentence_names_shape_unnegated` (loom-code/tests/test_probes_language_policy.py)
- `_paragraph_names_shape_and_requires_english` -> `_paragraph_names_shape_and_english` (loom-code/tests/test_probes_language_policy.py)

No renamed or deleted function is cited in `docs/loom/evidence/mechanisms.yaml`, `AGENTS.md` or `loom-code/tests/test_module_criteria_text.py`.
