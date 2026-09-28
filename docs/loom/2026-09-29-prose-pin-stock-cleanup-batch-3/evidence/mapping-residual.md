# Residual-pin mapping for the known files (W1-07)

Defect class: a sentence pin left in a known-7 file after W1-01. That is an assert that passes only while one phrase of runtime prose keeps its exact wording. The census detector cannot see these, because they sit inside a local `*_errors` validator, a `required` list, a regex, or a two-word literal.

Where we searched: every literal and regex in `loom-workflow/tests/loom-visualization/test_references.py`, `loom-workflow/tests/goal-create/test_goal_shape.py` and `loom-workflow/tests/decision-map/test_skill_doc.py`. We read each one and put it in one of two groups. A clause or verb phrase copied from the prose counts as a pin. A heading, label, fixed term, file name, code token, noun used as a concept name, or single word is kept.

"Lens" means `loom-code/skills/closing-review/references/lenses.md`, skill lens, which scores `SKILL.md` and reference prose on the five docs dimensions. Every kept test named below exists after this edit. No row names a deleted function, because no function was deleted.

## Removed pins

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `test_references.py::table_rule_one_errors` (used by `::test_rule_one_key_value_exception_stated` and `::test_rule_one_without_exception_fails`; pruned: "three or more attributes", "label plus one value") | table rule 1 loses its two-column key-value exception | `loom-workflow/tests/loom-visualization/test_references.py::test_rule_one_without_exception_fails`: the validator still requires the term `key-value` in rule 1, and the negative case still goes red | kept structural test |
| `test_references.py::routing_errors` (used by `::test_routing_names_document_types_per_collection`) and the second half of `::test_conversation_reply_routes_to_general_only` (pruned: the sentences "a conversation-situation reply never opens a domain file" and "Read only the one file whose row matches") | a conversation reply opens a domain file, or more than one domain file gets read | `loom-workflow/tests/loom-visualization/test_references.py::test_conversation_reply_routes_to_general_only`: the first half still fails a domain row that names a conversation situation, which guards the conversation-reply half. The read-only-one-file half and the sentence's own wording go to skill lens `inconsistency` (routing sentence against the routing table) | kept structural test |
| `test_references.py::test_node_structure_reference_strips_required_phrases` (pruned from `required`: "expanded into an informative phrase or removed from the diagram", "never drawn with an empty separator", "state nodes stay title-only") | node-structure drops the expand-or-delete content rule, or lets state nodes carry a body | skill lens `omission` (the content rule and the state-node rule). The same function keeps the `## Container rule / content rule` heading term (`container rule`), `diamonds` and the other structure terms, which stay while either rule is dropped | review lens dimension |
| `test_references.py::in_cell_errors` (used by `::test_in_cell_visuals_and_time_axis_guidance_present`; pruned: "not possible" from the heatmap item) | the guide claims a heatmap works in plain Markdown | skill lens, `inconsistency`; `::test_removed_in_cell_section_fails` and the kept `heatmap` term still guard the item | review lens dimension |
| `test_goal_shape.py::test_defines_four_fields_budget_and_surfacing` (pruned: regex `points? (at\|to) a file`; the `not because openai documents` alternative, which the looser `not … openai … documents` check in the same assert already covers) | a goal over the budget inlines detail instead of pointing at a file | skill lens, `omission`. The W1-01 row in `mapping-known.md` lists "the file-pointer rule" among what this function keeps. That rule is now review-only. | review lens dimension |
| `test_goal_shape.py::test_constraints_carries_the_standing_decision_rule` (pruned: `does not pre-decide`, `run's to make`, `by default`) | Constraints stops leaving undecided choices to the run, or SESSION mode stops emitting the entry | skill lens, `omission`; the same function keeps the section anchor `## 2 — \`Constraints\``, the terms `search`/`decide`/`record`/`candidate`/`source`/`named file`, the never-ask polarity check, the `derived` tag and the `irreversible`/`outward-facing` boundary | review lens dimension |
| `test_goal_shape.py::test_stop_when_is_one_bound_written_as_completion` (pruned: negation bound to `a list of`, `the condition` and `releases the run`) | Stop-when becomes a list of exit conditions, or a bare stop clause counts as the condition being met | skill lens, `inconsistency` (the §4 wording against the evaluator behaviour it describes); the same function keeps the `## 4 — \`Stop-when\`` anchor, `one`/`bound`, the report-completes co-occurrence, `failure report`, `permission`, the never-a-`Stop-when branch` polarity check and the `input-floor` pointer | review lens dimension |
| `test_skill_doc.py::test_v3_public_surface_commands_templates_and_version_are_synchronized` (pruned: "machine-measured feasibility", "human evaluates" in `prototype-contract.md`) | the prototype contract stops sorting research from prototype by who judges | skill lens `ambiguity` (the routing criteria). The same function keeps the `research` and `prototype` type names and the `ticket_template` grammar `type: <grilling\|research\|prototype>`, which stay while the criteria go | review lens dimension |

## Kept on purpose (not prose pins)

| file::function | literal | reason |
|---|---|---|
| `test_references.py::guide_errors` | `conclusion`, `announcement`, `heading`, `background`, `metaphor` | vocabulary: single words, not a clause |
| `test_references.py::test_node_structure_reference_strips_required_phrases` | `title line`, `separator row`, `wrapped prose`, `bullet lines`, `left-aligned`, `left alignment`, `container rule`, `width budget`, `box-drawn nodes`, `flow steps`, `edge labels`, `sequence participants`, `single-line`, `flowchart rectangles`, `diamonds`, the glyph and HTML tokens, `references/mermaid-cot-spec.md` | structure/label: `node-structure.md` headings (`## Left alignment`, `## Container rule / content rule`, `## Width budget`), body-form labels, scope-list terms and code tokens |
| `test_references.py::in_cell_errors` | `same cell`, `column axis`, `cell value`, `confidence`, `8 levels`, source names (`Tufte`, `WCAG 1.4.1`, `WHATWG`) | vocabulary: concept nouns, the lead labels of the time bullets, and citations |
| `test_references.py::table_criteria_errors` | `two directions`, `text alternative`, `numbered steps` plus source names | vocabulary: concept nouns that anchor the one-home (duplicate) check, and citations |
| `test_references.py::test_node_structure_reference_does_not_restate_skills_width_table` | `width rules` / `width table` | vocabulary: the name of the `SKILL.md` table it points to |
| `test_goal_shape.py::test_defines_four_fields_budget_and_surfacing` | `**attribution accuracy**`, `first-class`, `this skill` + `own choice`, `optional`/`suggested`, the `named by both\|both vendors name` absence, `no … limit` | label (the bold lead label), concept nouns, an absence check, and word co-occurrence, not a clause |
| `test_skill_doc.py::test_v3_public_surface_commands_templates_and_version_are_synchronized` | `"Use decision-map to start or resume an Outcome Map v3 for this repo."` | out of scope: a manifest `defaultPrompt` field, not skill or reference prose |
| `test_skill_doc.py::test_v3_public_surface_commands_templates_and_version_are_synchronized` | operation names (`Update blockers`, `Close and re-chart`, `Migrate v2 to v3` …), `zero-write preview`, `Map clear` | label: `###` operation headings in `SKILL.md`, and fixed terms |
| `test_skill_doc.py::V2_RETIRED_WRITEBACK_PHRASES` | retired v2 phrases | absence check, not a presence pin |

## Test cases

- **A2 positive, structure-checks-kept.** The kept structure, label and term checks are listed in both tables. The 3 files pass alone: 35 passed.
- **A2 negative, suite-green-after-prune.** See the W1-07 report for the `loom-workflow/tests` run.
- **A3 positive, mapping-row-per-removed-pin.** Every pruned literal or regex has a row in "Removed pins".
- **A3 boundary, validator-wrapped-phrase-judged.** The phrases inside `table_rule_one_errors`, `routing_errors`, `in_cell_errors` and the `required` list were judged one by one. The validators and their negative partners stay: `::test_rule_one_without_exception_fails` still goes red when rule 1 loses `key-value`.

## W3-01: pins hidden by the output-taint gap

Defect class: a direct prose pin hidden from the census because its markdown read is misclassified as program output (a yaml-parsing frontmatter helper, or a skill file read from an installed plugin copy under `tmp_path`). Where we searched: the build adversary's findings over all changed files, then a census rerun with the fixed detector from a clean worktree over the four test roots. The rerun newly flags only the two files below. Every kept test named here exists after this edit. No function was deleted.

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `loom-workflow/tests/distill-sessions/test_prompts_parseable.py::test_failure_prompt_structure` (pruned: "never mention ground truth") | the failure prompt drops its ground-truth-blind hard constraint | skill lens, `omission`; the rule's frontmatter `hard_constraints` list still has to parse and carry its keys (`::test_both_prompt_files_have_required_sections`) | review lens dimension |
| `…/test_prompts_parseable.py::test_failure_prompt_structure`, `::test_success_prompt_structure` (pruned: "no more than 3" / "max 3" / "maximum of 3") | a prompt stops capping Memory Items at 3 | skill lens, `omission` | review lens dimension |
| `…/test_prompts_parseable.py::test_both_prompts_forbid_orchestrator_memory_reference` (pruned: body "never reference the orchestrator's project memory"; redundant "orchestrator's project memory" alternative) | the body stops restating the no-memory-citation rule | skill lens `inconsistency` (body against frontmatter). `loom-workflow/tests/distill-sessions/test_prompts_parseable.py::test_both_prompts_forbid_orchestrator_memory_reference` keeps the frontmatter `hard_constraints` check (`project memory`), which guards the rule itself but never reads the body | review lens dimension |
| `…/test_prompts_parseable.py::test_advisory_prompt_structure` (pruned: "fenced code block", redundant) | the advisory prompt stops documenting code-block wrapping | `loom-workflow/tests/distill-sessions/test_prompts_parseable.py::test_advisory_prompt_structure`: the `code block` term in the same assert already covered every case | kept structural test |
| `…/test_prompts_parseable.py::_assert_common_shape`, `::test_success_prompt_structure` (re-anchored: "How the orchestrator dispatches this prompt", "Lean Solution Path") | the dispatch section or the Lean Solution Path section disappears | the same functions, now matching the existing `## How the orchestrator dispatches this prompt` and `## Lean Solution Path output format` headings | kept structural test |
| `tests/test_loom_plugin_install_layout.py::test_isolated_loom_plugins_are_standalone_and_compose_by_public_contract` (pruned: "positive" + "negative or boundary", "closing-review station once at branch end" in the installed write-plan `SKILL.md`) | write-plan stops asking for test-case pairs per Acceptance line, or stops placing closing review once at branch end | `intake.test-case-pair` recomputes the pair on every newly authored plan; the branch-end review sentence goes to skill lens `inconsistency` (write-plan against the closing-review station) | checker rule id |

### Test cases

- **A1 positive, yaml-helper-body-pin-flagged; negative, parsed-frontmatter-value-not-flagged.** `docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/test_classify_test_files.py::test_yaml_helper_body_pin_flagged` (red before the fix) and `::test_parsed_frontmatter_value_not_flagged`.
- **A2 positive, behavior-checks-kept.** `find_boundary_violations`, the dependency checks and the frontmatter checks stay; the two files pass alone.
- **A2 negative, suite-green-after-prune.** See the W3-01 report for the `loom-code/tests`, `loom-workflow/tests` and root `tests` runs.
- **A3 positive, mapping-row-per-removed-pin.** Every pruned or re-anchored literal has a row above.
- **A3 boundary, installed-copy-skill-read-counts-as-prose.** `…/test_classify_test_files.py::test_installed_copy_skill_read_counts_as_prose`: a `SKILL.md` read from a `tmp_path` install is prose. The census sees it soundly: the rerun adds only the install-layout file.

## W4-01: rows that overclaimed automated cover

Defect class: a mapping row claims a kept automated test guards a defect class that the test does not actually guard, or a residual sentence pin remains in a pruned file. Where we searched: every row of the five mapping files whose kind is `kept structural test` or `checker rule id`, by reading the named test's body or the rule's `--list-rules` text, and the test files those rows name.

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `tests/test_loom_plugin_install_layout.py::test_sibling_lookup_resolves_flat_and_versioned_installs` (pruned: the `VERSION_STEP` constant, "if its parent directory is named `loom-design`", asserted with `in` against the Codex/Antigravity row) | the other-host row drops its step up out of a versioned `loom-design` directory | skill lens `inconsistency` (the lookup row against a versioned install layout). The same function keeps the `rows == 1` count of the Codex/Antigravity row; its path resolution runs a hardcoded model, not the row | review lens dimension |

The helper `_resolve_loom_code_by_row` never parsed the row, so its docstring now says it is a hardcoded model.

**Verdict per row.** "Guards" means the named test or rule fails when the row's defect occurs. "Partial" means it guards one half, and the row now names a lens for the other half. "Overclaim" means it does not fail, and the row was relabelled to `review lens dimension`.

| mapping row | named test or rule | verdict |
|---|---|---|
| `mapping-known.md:16` | `test_record_section_matches_the_digest_the_cold_reader_eval_was_run_against` | guards: any Record edit changes the digest |
| `mapping-known.md:26` | `standing.warn` | partial: the checker never blocks; the "adds a step" half is lens |
| `mapping-known.md:27` | `test_code_lens_has_architecture_conformance_na_without_doc` | partial: the `N/A` bullet check; unratified scoring is lens |
| `mapping-known.md:35` | `test_v3_public_surface_commands_templates_and_version_are_synchronized` | partial: the ticket template; route rules beyond field names are lens |
| `mapping-known.md:36` | same function | guards: each implemented state and phase must be a code token in both docs |
| `mapping-known.md:37` | same function | guards: `risk-front-loading` must precede the validate command under `## Close-time checks` |
| `mapping-known.md:45` | `test_rule_five_example_is_a_table` | partial: alternatives and the recommended row; yes-or-no and ruled-out clauses are lens |
| `mapping-known.md:49` | `test_skill_md_points_to_node_structure_reference` | overclaim: checks only the pointer; relabelled |
| `mapping-known.md:58` | `test_resume_launcher_section_present_and_constrained` | guards: both examples must be `###` headings |
| `mapping-known.md:71` | `test_routing_corpus_covers_positive_boundary_and_non_trigger_cases` | overclaim: a fixture check that never reads the description or router; relabelled |
| `mapping-new-code.md:14` | `test_cli_is_deterministic_json_and_rejects_malformed_input` | overclaim: runs the resolver, never reads the contract; relabelled |
| `mapping-new-code.md:15` | `test_host_rejection_is_not_capability_quality_escalation`, `test_preexecution_host_rejection_gets_one_override_free_replacement` | overclaim: guard the code's split, not the contract; relabelled |
| `mapping-new-code.md:19` | `test_ship_accepted_land_renders_absolute_worktree_in_command` | guards: the command must `cd` to the absolute worktree root |
| `mapping-new-code.md:20` | `test_sibling_lookup_resolves_flat_and_versioned_installs` | overclaim: a hardcoded model, never parses the row; relabelled, and its `VERSION_STEP` pin pruned (row above) |
| `mapping-new-workflow.md:13` | `test_creates_intent_and_lists_it_under_the_criterion` | overclaim: checks what the script writes, not the derived-state rule; relabelled |
| `mapping-new-workflow.md:14` | `test_refuses_a_second_criterion_reusing_one_intent`, `test_reuse_is_idempotent` | guards: the script refuses a second criterion for one intent |
| `mapping-new-workflow.md:15` | `test_no_delivery_ticket_is_authored_any_more`, `test_writes_no_brief_and_no_ticket_binding` | guards: the `\|delivery>` absence and a script run that writes no ticket |
| `mapping-new-workflow.md:18` | `test_planted_aws_key_exits_3_with_finding` and siblings | overclaim: the scanner never reads a trailer; relabelled |
| `mapping-new-workflow.md:21` | `test_shaped_content_defaults_to_a_markdown_table` | overclaim: reads the client matrix, not the `SKILL.md` default; relabelled |
| `mapping-new-workflow.md:23` | `test_l3_contract_defines_goal_grounded_natural_output` | partial: tag and label leaks in the template; invented purpose is lens |
| `mapping-new-workflow.md:24` | `test_coexist_card_skip_sentence_names_the_skill` | guards: the "Skip it" absence |
| `mapping-residual.md:13` | `test_rule_one_without_exception_fails` | guards: rule 1 without `key-value` goes red |
| `mapping-residual.md:14` | `test_conversation_reply_routes_to_general_only` | partial: a domain row naming a conversation situation; the one-file rule is lens |
| `mapping-residual.md:15` | `test_node_structure_reference_strips_required_phrases` | overclaim: the kept terms stay while either rule goes; relabelled |
| `mapping-residual.md:20` | `test_v3_public_surface_commands_templates_and_version_are_synchronized` | overclaim: type names stay while the criteria go; relabelled |
| `mapping-residual.md:51` | `test_both_prompts_forbid_orchestrator_memory_reference` | overclaim: reads only the frontmatter, not the body; relabelled |
| `mapping-residual.md:52` | `test_advisory_prompt_structure` | guards: the `code block` term |
| `mapping-residual.md:53` | `_assert_common_shape`, `test_success_prompt_structure` | guards: both headings |
| `mapping-residual.md:54` | `intake.test-case-pair` | guards the effect: a newly authored plan without the pairs fails the checker |

`mapping-new-design.md` has no `kept structural test` or `checker rule id` row.

**Residual pin search.** The test files these rows name were scanned for a presence assert of a literal of four or more words. Every hit is a validator error message or program output. `VERSION_STEP` was the only residual sentence pin found, and it is pruned above.

### Test cases

- **A1 positive, version-step-pin-pruned.** `VERSION_STEP` no longer occurs in `tests/test_loom_plugin_install_layout.py`.
- **A1 negative, row-count-check-kept.** `test_sibling_lookup_resolves_flat_and_versioned_installs` still asserts `rows == 1` and passes.
- **A3 positive, every-kept-test-row-verified.** Every row above has a verdict from reading the named body.
- **A3 negative, fixture-only-test-not-cited-as-cover.** `mapping-known.md:71` no longer cites the routing-corpus fixture check as cover.
