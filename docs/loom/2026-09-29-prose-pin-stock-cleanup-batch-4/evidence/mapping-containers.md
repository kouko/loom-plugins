# Prose-pin mapping for container and parameter needles (W1-09)

Scope: the 89 prose candidates that the W1-07 census newly lists outside `loom-workflow/tests/scripts/test_*_compaction.py`. A row counts as new when its (file, function, literal) key is absent from `candidate-list.md`. The rows sit in 11 files. Rows the earlier mappings already decided (`mapping-code.md`, `mapping-design.md`, `mapping-workflow.md`, `mapping-workflow-2.md`) keep those decisions and are marked "prior decision" below.

"Skill lens" and "docs lens" mean the lenses in `loom-code/skills/closing-review/references/lenses.md`. The skill lens scores `SKILL.md` and agent contracts, and the docs lens scores READMEs. Both use the five docs dimensions.

The keep rule is the one in `mapping-workflow.md`. A short literal is kept when it is a heading, a table-header cell or a column-parsed cell value, a bold, list-item or line label, a field name, a code token or path, a proper name, a fixed technical term, or an absence check. Any other word or phrase copied from prose is a pin.

**Classifier change (A1).** `literal_class` now treats two more kinds of literal as structural. The first is a Mermaid diagram keyword, such as `flowchart`, `erDiagram` or `stateDiagram-v2`, optionally followed by direction tokens such as `LR` or `TD`. The second is a single word that is the `<name>` of a `gen_<name>` script on disk (`seq`, `table`, `arch` ...). Two probes in `docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/test_classify_test_files.py` cover this. `::test_mermaid_keyword_and_generator_name_classed_structural` is the positive probe, and `::test_prose_needle_with_a_diagram_word_still_flagged` checks that `flowchart rectangles` and `timeline view` are still prose. The change added two module constants and one helper, `_generator_names`, that only `literal_class` calls.

**Synthetic fixtures (A3 boundary).** None of the 89 rows is a needle asserted against a fixture string written in the test. The census does not list the synthetic self-tests in these files, such as `test_adversary_layout.py::test_marker_helper_synthetic` and `test_visualization_card_hook.py::test_affirmative_card_rule_accepted`. They stay as they are, because they are synthetic fixtures and not skill text. Three synthetic tests in `test_visualization_card_hook.py` were deleted. Each one exercised only a helper deleted below. The same was done for `markdown_table_choice_errors` in `mapping-workflow-2.md`.

Rule 3 citations: `loom-code/tests/test_module_criteria_text.py` cites `test_adversary_layout.py::test_no_kind_rule_appears_outside_its_own_file`, which is kept whole. `docs/loom/evidence/mechanisms.yaml` names `scripts/test_visualization_card_hook.py` as a whole-file eval (line 219). That file stays, and so do its hook subprocess tests. Nothing cites a deleted or renamed function.

## Decisions

| file::function | literal(s) | decision | reason |
|---|---|---|---|
| loom-code/tests/test_adversary_layout.py::test_no_kind_rule_appears_outside_its_own_file | the 8 `KIND_MARKERS` fragments (`a surviving mutant is a test that asserts nothing`, `path traversal`, `Prefer cases that live as real tests afterwards.`, `name a behaviour the requirement permits`, `the migration from what exists today`, `Read the instruction as an agent under time pressure`, `Attempt the prose temptations verbatim`, `the same input one character different`) | keep-structural | a one-home absence check. The fragments are asserted to be absent from every file except the one that owns their kind, so rewriting the owning file cannot turn the test red. `test_module_criteria_text.py` cites this function |
| loom-code/tests/test_probes_language_policy.py::test_reviewer_nitclause_absent | `english`, `ears`, `conventional comments`, `nit` | keep-structural, tightened to case-sensitive `English`, `EARS`, `Conventional Comments` and `` `nit` `` | proper names (the language, the requirements syntax, the comment convention) and the `nit` severity value, which is written as a code token in reviewer.md |
| loom-code/tests/test_probes_language_policy.py::test_reviewer_nitclause_absent | `shall`, `label`, `regardless` | prune | ordinary words. `shall` and `label` were fallback alternatives, and `regardless` is the docs-lint-independence word of the clause |
| loom-code/tests/test_probes_language_policy.py::_paragraph_names_shape_and_english | `english` | keep (prior decision) | `mapping-code.md` row 39 |
| loom-code/tests/test_write_plan_station_text.py::test_ask_is_host_aware_and_has_complete_fallbacks | `On Antigravity CLI,` | prune; the scan was deleted and the check is now review-only (P2) | the scan found its sentence by an opening phrase. The only heading above that sentence is `## Availability probe`, and that section names `codex` and `gemini` legitimately, so the vendor-absence check cannot re-anchor on it |
| loom-design/tests/interface/test_design_md_schema_keys.py::test_schema_keys_documented_and_token_groups_named | `> **Grounding.**`, `> **Scope` | keep-structural | blockquote bold labels that bound the grounding note |
| loom-design/tests/interface/test_design_md_schema_keys.py::test_component_completeness_scoping_catches_deleted_bullet | `size`, `height`, `padding`, `width` | keep-structural | component sub-token keys (the `- \`size\`` bullets and the YAML keys). The assert is a sanity precondition of a mutation test |
| loom-design/tests/interface/test_knowledge_triage.py::test_shaping_route_names_the_design_conformance_lens | `design-conformance` | keep (prior decision) | `mapping-design.md` row 47. The function has been renamed since, which is why the census lists the row as new |
| loom-workflow/tests/goal-create/test_readmes.py::test_tri_language_discovery_promises_activation_and_honest_fallback | `when accepted`, `recovery`; (miss) `受理された場合`, `復旧`, `接受時`, `復原` in `PLUGIN_READMES` and the same six in `SKILL_ACTIVATION_TERMS` | prune | ordinary phrases in three languages. The `create_goal` / `ProposeGoal` / `/goal` code-token regexes and the goal-create row lookup stay |
| loom-workflow/tests/loom-visualization/test_references.py::table_errors | `Before and after`, `Confirmed, unconfirmed, to decide`, `Findings and recommendations` | keep-structural | H3 situation titles (`### N. <name>`), matched against the parsed heading list |
| loom-workflow/tests/loom-visualization/test_references.py::in_cell_errors | `heatmap`, `rule 6` | keep (prior decision) | `mapping-workflow.md`, `IN_CELL_ITEMS` kept row |
| loom-workflow/tests/loom-visualization/test_references.py::table_criteria_errors | `two directions`, `text alternative`, `flowchart`, `org chart`, `numbered steps` | prune | concept phrases copied from bullets. The subsection headings, the source names (`Datawrapper`, `W3C WAI`, `Google`) and the source URLs stay. The duplicate count keyed on the first phrase went too, because it had no heading or marker to anchor on (P2) |
| loom-workflow/tests/loom-visualization/test_references.py::domain_errors | `Before and after`, `Confirmed, unconfirmed, to decide` | keep-structural | a situation-heading cross-reference in the `Pointer:` line. The `GENERAL_POINTERS` values are H3 situation titles |
| loom-workflow/tests/loom-visualization/test_references.py::routing_errors | `incident postmortem`, `test plan`, `runbook`, `heuristic evaluation`, `design tokens`, `journey map`, `roadmap` | keep-structural | document-type names read as column-parsed cells of SKILL.md's `Need \| Read` routing table, and from the `Load this when:` line. This is the same class as the prior `progress` decision |
| loom-workflow/tests/loom-visualization/test_templates.py::test_eleven_shapes_each_have_table_ascii_mermaid | `flowchart`, `flowchart LR`, `flowchart TD`, `erDiagram`, `mindmap`, `quadrantChart`, `sequenceDiagram`, `timeline`, `xychart-beta` | keep-structural (now auto-classed) | the Mermaid diagram keyword on a block's first line |
| loom-workflow/tests/loom-visualization/test_templates.py::test_generator_examples_reproduce_their_output | `arch`, `bar`, `flow`, `seq`, `table`, `tree` | keep-structural (now auto-classed) | generator names (`gen_<name>.py`, `scripts/generate.py <name>`) |
| loom-workflow/tests/recap-state/test_readmes.py::test_tri_lang_readmes_consistent | `where were we`, `recap`, `bring me back`, `what are we doing` (via `_skill_description_contains`); (miss) `JA_TRIGGERS_IN_SKILL` and `ZHTW_TRIGGERS_IN_SKILL` counted in the SKILL.md text | prune | trigger phrases matched against the raw SKILL.md text. The parsed-description check in `recap-state/test_skill_md.py` covers the same thing. The README-side trigger checks stay, because README prose is not skill text |
| loom-workflow/tests/scripts/test_readme_card_timing.py::test_readmes_state_unreached_hosts_and_loom_code_only | the 9 prose `LIMIT_PHRASES` (`Codex IDE extension`, `Antigravity desktop app or IDE`, `` `loom-code` without `loom-workflow` `` and their JA and zh-TW forms), plus the structural-classed `Codex app` / `Codex アプリ` siblings | prune | install-limit phrases in three languages. `UserPromptSubmit` (a code token) stays |
| loom-workflow/tests/scripts/test_visualization_card_hook.py::test_negated_card_rule_rejected | `in their language.`, `4) Use tables or`, `; no metaphors, analogies, "like" or "imagine".` | keep | mutation sites of the kept `rule_polarity_errors` gate. Batch 3 cited that gate as a replacement, and `mapping-workflow-2.md` row 33 kept it. The `old in flat` assert keeps each mutation from being vacuous |
| loom-workflow/tests/scripts/test_visualization_card_hook.py::inline_decision_rule_errors | `asking or answering how to do something`, `2+ workable options`, `in a table`, `recommend` | prune: the helper was deleted, the path check was kept | a sentence-pin helper. The `references/plain-language.md` path stays |
| loom-workflow/tests/scripts/test_visualization_card_hook.py::missed_alternative_errors, ::missed_alternative_verb_errors | `asking or answering how to do something`, `doing nothing or later`, `a smaller version`, `combining two`, `list or rule out` | delete | sentence-pin helpers. Their five tests exercised only these helpers |

## Mapping

One row per removed pin or group of pins guarding the same thing. Every kept structural test named here exists after this edit, and no row names a deleted function as its replacement.

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| loom-code/tests/test_probes_language_policy.py::test_reviewer_nitclause_absent (pruned: `shall`, `label`, `regardless`) | the nit clause stops holding regardless of `docs-lint`, or drops the label list | skill lens, `omission`. The same function still requires one paragraph that names `English`, `EARS`, `Conventional Comments` and `` `nit` ``, and requires the `docs-lint` key | review lens dimension |
| loom-code/tests/test_write_plan_station_text.py::test_ask_is_host_aware_and_has_complete_fallbacks -> ::test_second_vendor_reference_drops_second_reader_wording (scan deleted: vendor absence in the Antigravity sentence) | the Antigravity CLI probe line offers a CLI runner | skill lens, `incorrect-fact` (a host claim against `second_vendor_policy.py`) | review-only |
| loom-workflow/tests/goal-create/test_readmes.py::test_tri_language_discovery_promises_activation_and_honest_fallback -> ::test_tri_language_discovery_names_host_goal_tools (pruned: activation and fallback phrases in three languages) | a README stops promising activation when accepted, or stops offering a manual recovery | `loom-workflow/tests/goal-create/test_readmes.py::test_tri_language_discovery_names_host_goal_tools` still requires the `create_goal` and `ProposeGoal` … `/goal` tokens and the goal-create row with `` `Why` `` / `` `Done when` ``. The promise wording goes to docs lens `omission` | kept structural test |
| loom-workflow/tests/loom-visualization/test_references.py::table_criteria_errors (pruned: concept phrases, duplicate count); ::test_removed_criterion_fails -> ::test_removed_criterion_source_url_fails | an earlier table criterion loses its bullet or is stated twice | `loom-workflow/tests/loom-visualization/test_references.py::test_three_earlier_criteria_present` still requires each subsection to name the criterion's source and each source URL to appear under Sources. The duplication goes to skill lens `inconsistency` | kept structural test |
| loom-workflow/tests/recap-state/test_readmes.py::test_tri_lang_readmes_consistent (pruned: the EN any-of phrases and the JA and zh-TW >=3 counts against the SKILL.md text; `_skill_description_contains` and `SKILL_MD` removed) | the SKILL.md description drops its trigger phrases | `loom-workflow/tests/recap-state/test_skill_md.py::TestFrontmatterAndRouting::test_b_multilingual_triggers` checks the parsed description for an EN, a JA and a zh-TW trigger | kept structural test |
| loom-workflow/tests/scripts/test_readme_card_timing.py::test_readmes_state_unreached_hosts_and_loom_code_only -> ::test_readmes_name_the_userpromptsubmit_hook (pruned: `LIMIT_PHRASES`, `_missing_limits`); ::test_checks_catch_stale_and_missing_wording -> ::test_checks_catch_stale_wording_and_old_name (its `_missing_limits` assert removed) | a README stops naming the hosts the per-turn card does not reach, or the loom-code-only install | docs lens, `omission`. `::test_readmes_name_the_userpromptsubmit_hook` still requires the hook name in every README | review lens dimension |
| loom-workflow/tests/scripts/test_visualization_card_hook.py::inline_decision_rule_errors (deleted), ::test_both_cards_state_inline_decision_rule -> ::test_both_cards_point_at_the_plain_language_guide, ::test_card_without_inline_decision_rule_fails (deleted) | a card stops stating the decision rule inline, or negates it | `loom-workflow/tests/scripts/test_visualization_card_hook.py::test_both_cards_point_at_the_plain_language_guide` still requires the guide path in both cards. The inline rule and its polarity go to skill lens `omission` and `inconsistency` (card against rule 5 of the guide) | kept structural test |
| loom-workflow/tests/scripts/test_visualization_card_hook.py::missed_alternative_errors, ::missed_alternative_verb_errors, ::test_both_cards_name_the_three_missed_alternatives, ::test_card_missing_one_missed_alternative_fails, ::test_both_cards_list_or_rule_out_each_missed_alternative, ::test_weaker_verb_over_missed_alternatives_rejected, ::test_negated_missed_alternatives_rejected (all deleted) | a card drops one of the three missed alternatives, or names them under a weaker verb or in a negated clause | skill lens, `omission` (a dropped alternative) and `ambiguity` (a weaker verb). `::test_cards_at_most_181_words` and the hook subprocess tests stay | review lens dimension |

## Renames

- `loom-code/tests/test_write_plan_station_text.py::test_ask_is_host_aware_and_has_complete_fallbacks` -> `test_second_vendor_reference_drops_second_reader_wording`
- `loom-workflow/tests/goal-create/test_readmes.py::test_tri_language_discovery_promises_activation_and_honest_fallback` -> `test_tri_language_discovery_names_host_goal_tools`
- `loom-workflow/tests/loom-visualization/test_references.py::test_removed_criterion_fails` -> `test_removed_criterion_source_url_fails`
- `loom-workflow/tests/scripts/test_readme_card_timing.py::test_readmes_state_unreached_hosts_and_loom_code_only` -> `test_readmes_name_the_userpromptsubmit_hook`
- `loom-workflow/tests/scripts/test_readme_card_timing.py::test_checks_catch_stale_and_missing_wording` -> `test_checks_catch_stale_wording_and_old_name`
- `loom-workflow/tests/scripts/test_visualization_card_hook.py::test_both_cards_state_inline_decision_rule` -> `test_both_cards_point_at_the_plain_language_guide`

The name `test_reviewer_nitclause_absent` is kept, because it is the probe's attack name and the body still checks the nit clause. Only its docstring was corrected. The module docstring of `test_readme_card_timing.py` was corrected to match the pruned body.

## Classifier result after the edit (P7)

`--candidates` lists 0 undecided prose candidates in these files. Every remaining prose row is one of the keeps above or a prior decision.

| file | class | has_pins | remaining hits |
|---|---|---|---|
| loom-code/tests/test_adversary_layout.py | behavior (override) | — | one-home absence markers |
| loom-code/tests/test_probes_language_policy.py | sentence-pin | yes | the `docs-lint` key, the negation token set and `english`, all kept earlier |
| loom-code/tests/test_write_plan_station_text.py | grammar-invariant | yes | the `LANE_WORDING_RE` regex in `lane_hits` (prior, not a new row) |
| loom-design/tests/interface/test_design_md_schema_keys.py | behavior | yes | bold labels and sub-token keys (kept above), plus earlier rows |
| loom-design/tests/interface/test_knowledge_triage.py | behavior | yes | tier labels, lens name and bucket names (prior) |
| loom-workflow/tests/goal-create/test_readmes.py | structure | — | none |
| loom-workflow/tests/loom-visualization/test_references.py | sentence-pin | yes | headings, column cells and labels (kept) |
| loom-workflow/tests/loom-visualization/test_templates.py | behavior (override) | — | none new |
| loom-workflow/tests/recap-state/test_readmes.py | structure | — | none |
| loom-workflow/tests/scripts/test_readme_card_timing.py | sentence-pin | yes | `visualization card`, the component's own name (prior) |
| loom-workflow/tests/scripts/test_visualization_card_hook.py | behavior | yes | the `rule_polarity_errors` gate, its mutation sites and `ascii-graph` (kept) |

W2-01 adds the override rows for these heading, label and name hits.

## W2-01 additions

The W1-09 census could not see the `SITUATIONS` regex values in `loom-workflow/tests/scripts/test_visualization_card_hook.py`. They reach `re.search` through `SITUATIONS.items()` inside a negated comprehension filter, which collects the situations a card does not name. W2-01 taught `pin_candidates` that form (probe `docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/test_classify_test_files.py::test_regex_values_through_items_collected_when_unmatched_flagged`). The census then listed 8 new prose rows, all of them in `situation_errors`.

Rule 3: no mechanisms.yaml eval, AGENTS.md line or `test_module_criteria_text.py` line names the deleted functions. `mechanisms.yaml` line 219 names the whole file, and its hook subprocess tests stay. None of the deleted functions runs a program. A frozen probe of an earlier change, `docs/loom/2026-09-16-plain-language-follow-ups/evidence/probes/test_probe_card_guard_bypasses.py`, imports `situation_errors` and `SITUATIONS`. It also imports the `missed_alternative_*` helpers that W1-09 deleted. It is not in the package suite (`census-report.md`, Known limits).

### Decisions

| file::function | literal(s) | decision | reason |
|---|---|---|---|
| loom-workflow/tests/scripts/test_visualization_card_hook.py::situation_errors | the 8 `SITUATIONS` regexes (`\bprogress\b`, `\bbefore and after\b`, `what each choice means`, `\breadiness\b`, `confirmed against unconfirmed`, `\bfindings\b`, `\brisks\b`, `supported environments`) | delete | situation phrases matched against the card's prose. Rewording a card sentence turns it red, and no heading or gate marker bounds the trigger sentence (P2) |

### Mapping

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| loom-workflow/tests/scripts/test_visualization_card_hook.py::situation_errors, `SITUATIONS`, `_flat_body`, ::test_both_cards_name_the_conversation_situations, ::test_card_naming_only_data_shapes_fails, ::test_card_missing_one_situation_fails, ::test_situations_named_in_a_negated_sentence_do_not_count (all deleted) | a card drops one of the conversation situations, or names them only inside a negated trigger sentence | skill lens, `omission` (a dropped situation) and `inconsistency` (a negated sentence against the guide's situation tables). `::test_both_cards_point_at_the_plain_language_guide` still requires the guide path in both cards | review lens dimension |

## W3-01 additions

W3-01 taught `pin_candidates` two forms the batch-4 adversary found: a `.find()`/`.rfind()` lookup whose result an assert compares as present, and markdown held on `self.<attr>`/`cls.<attr>`. The probes are `loom-code/tests/test_adversarial_batch4_census_lookup_forms.py` (graduated) and `test_classify_test_files.py::test_find_in_output_not_flagged`. Rerun from a clean worktree, the census surfaced 13 new candidates, all `structural`, and **no prose candidate**. So nothing was pruned and this section has no mapping rows. W3-01 re-read each row, including the four `capitalized label` rows, and kept all 13 as structural:

| file:line | function | literal(s) | kept because |
|---|---|---|---|
| loom-workflow/tests/goal-create/test_goal_shape.py:52 | test_defines_four_fields_and_budget | `Outcome`, `Constraints`, `Verification`, `Stop-when` (`.find()` present, in order) | the four field names, each a `## N — \`<name>\`` heading and a numbered list item of goal-shape.md |
| loom-workflow/tests/handoff/test_handoff_skill_md.py:98, 127 | test_d_relative_path_reference, test_h_handoffs_path | `references/handoff-schema.md`, `.claude/handoffs/` (on `self.body`) | paths |
| loom-workflow/tests/handoff/test_handoff_skill_md.py:118, 121 | test_g_prepare_and_resume_modes | `## Prepare mode`, `## Resume mode` (on `self.body`) | headings |
| loom-workflow/tests/recap-state/test_skill_md.py:93 | test_d_relative_path_reference | `references/seven-block-schema.md` (on `self.body`) | path |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:301, 326, 350, 364 | test_advisory_prompt_defines_skill_dir_before_first_use, test_advisory_prompt_declares_skill_dir_input, test_skill_md_advisory_dispatch_names_skill_dir_key, test_host_advisory_dispatch_template_passes_skill_dir | `<skill-dir>`, `## Context you will receive`, `## Optional advisory report`, `## Stage 5c single dispatch` (`.find()` present) | a placeholder and headings that locate a section |

The goal-create override row's reason now names `stop-when` and the `.find()` lookups. `test_goal_shape.py` keeps its override row, and the other three files stay `structure` with no override row.
