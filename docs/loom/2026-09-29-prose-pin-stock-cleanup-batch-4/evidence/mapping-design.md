# W1-02 mapping — loom-design test files

Defect class: a prose pin against a loom-design runtime markdown file (`SKILL.md` or a
`references/*.md`) — an assert that passes only while one word or phrase of prose keeps
its wording. Files: `loom-design/tests/architecture-design/test_architecture_skill.py`,
`loom-design/tests/interface/test_design_md_schema_keys.py`,
`loom-design/tests/interface/test_design_system_skill.py`,
`loom-design/tests/interface/test_knowledge_triage.py`. "Lens" means
`loom-code/skills/closing-review/references/lenses.md`; a `SKILL.md` is scored on the
skill lens, a reference on the docs lens (same five dimensions).

## Decisions

One row per candidate in `candidate-list.md` for these files that is class `prose`, plus
the structural rows re-checked under P1 and the pins the detector missed.

| file:line | function | literal(s) | decision | reason |
|---|---|---|---|---|
| test_architecture_skill.py:71 | test_never_blocks_language_present | `never blocks`, `never required` | delete | prose pin; the skill carries no gate marker to re-anchor on (`test_no_gate_marker`) |
| test_architecture_skill.py:82-83 | test_skill_states_redesign_updates_decisions_rules_guards | `re-design`, `re-ratify` | delete | prose pin; the function holds nothing else |
| test_architecture_skill.py:89-90 | test_guard_failure_message_fields_stated | `rule id`, `offending path`, `conform`, `change the rule and its guard`, `guard failure message` | delete | prose pin; the function holds nothing else |
| test_architecture_skill.py:97 | test_skill_records_package_tests_when_absent_and_commits_edited_config | `Step 3 edited` (pre-classed structural, capitalized label) | prune | re-checked: a prose phrase ("every file Step 3 edited"), not a heading; the `package-tests` line grammar, the `## Step 5` / `## Downstream` heading slice and the `KICKOFF-DEFAULTS.md` path stay |
| test_architecture_skill.py:42 | test_description_within_codex_limit_and_carries_triggers | `架構規則`, `アーキテクチャ` (pre-classed structural) | keep-structural | re-checked: frontmatter description trigger keywords, the skill's routing surface, not body prose |
| test_design_md_schema_keys.py:259-260 | test_non_spec_keys_are_labelled_and_token_groups_named | `extension`, `export` | prune | prose words in each extension key's bullet; the bullet for each key (`_bullet_line`), the spec-meta absence check, the version stamp and the five-group roster stay |
| test_design_md_schema_keys.py:515 | test_elevation_section_disambiguates_non_spec_keys | `confirm`, `spec` | keep-absence | `assert not (...)`: an absence check of a removed header; rewording prose cannot turn it red |
| test_design_md_schema_keys.py:758 | test_derivation_contract_excludes_elevation | regex `every token in (.+?) MUST be derivable` | delete | P2: the roster is located by a literal sentence; the only anchor is the bold label `**Derivation contract:**`, which is neither a heading nor a gate marker |
| test_design_md_schema_keys.py:774 | test_derivation_contract_roster_catches_elevation_readded | same regex | delete | probe of the deleted check; also locates by the same sentence |
| (not listed) | test_derivation_contract_tolerates_clarifying_elevation_note_outside_roster | calls the deleted check | delete | probe of the deleted check |
| test_design_md_schema_keys.py:830 | test_component_properties_header_not_claimed_closed | `confirm`, `spec` | keep-absence | `assert not (...)`: absence check |
| test_design_md_schema_keys.py:837 | test_component_properties_header_not_claimed_closed | `closed` (positive, Typography header) | prune | prose word required present; the Components header absence checks stay |
| test_design_md_schema_keys.py:862 | test_shapes_rounded_bullet_states_not_radius | `not`, `radius` | prune | prose correction phrase; the `rounded` key bullet in `## Shapes` stays |
| test_design_md_schema_keys.py:879 | test_shapes_header_distinguishes_extension_bullets_from_spec_keys | `extension` | delete | prose word in a header; nothing else in the function |
| test_design_md_schema_keys.py:895 | test_overview_brand_header_distinguishes_extension_bullets_from_spec_keys | `extension` | delete | prose word in a header; nothing else in the function |
| test_design_md_schema_keys.py:977-981 | test_grounding_note_covers_the_consumer_behavior_claim | `verified against`, `warning`, `component property`, `consumer behavior` | delete | prose pins; the one remaining assert (`0.4.0` in the note) is already made by the renamed `test_schema_keys_documented_and_token_groups_named` (c) |
| test_design_md_schema_keys.py:994 | test_grounding_note_catches_reverted_key_sets_only_scope | calls the deleted check; its own regex `The frozen key sets\n> this reference checks against` | delete | probe of the deleted check, and itself a sentence pin |
| (missed by detector) :927-935 | test_generation_checklist_lint_step_does_not_require_stripping_warned_extension_properties | `warning`, `expected`, `legitimate`, `fail`, `blocker` via helper `_generation_checklist_step` | delete | prose words passed through a helper the detector does not follow; judged a pin (P1) |
| test_design_md_schema_keys.py:945 | test_generation_checklist_lint_step_catches_reverted_unconditional_resolve | calls the deleted check | delete | probe of the deleted check |
| (orphan) | `_generation_checklist_step` helper | — | delete | orphaned by the two deletions above (rule 5) |
| test_design_md_schema_keys.py:46, 128, 380, 532, 849, 906, 974 | helpers / mutation tests | fence, bullet, numbered-step and blockquote regexes, `` `spacing` (Layout) `` count | keep-structural | re-checked: markdown structure (fences, bullets, numbered steps) or a key token; 906 and 974 go with their deleted functions |
| (not listed) | test_prose_scope_clause_removed_at_both_loci, test_non_spec... (d) | regex / literal absence | keep-absence | absence checks |
| (not listed) | test_component_sub_tokens_docstring_*, test_module_docstring_not_claimed_closed, test_update_procedure_* | docstring of `design_md_spec_keys.py` | out of scope | they read a Python module docstring, not skill/agent/reference markdown |
| test_design_system_skill.py:84 | test_never_blocks_language_present | `never blocks`, `never required` | prune | prose pin; the `standing.product-principles-reject` rule id stays; the gate marker `design-system.never-blocks` is kept by `test_gate_marker_registered` |
| test_design_system_skill.py:64 | test_description_within_codex_limit_and_carries_triggers | `視覺設計系統`, `デザインシステム` | keep-structural | frontmatter trigger keywords |
| test_design_system_skill.py:138 | test_schema_reference_still_names_eight_canonical_sections | eight section names (capitalized label) | keep-structural | re-checked: each is a `##` heading of `design-md-schema.md` |
| test_knowledge_triage.py:102-103 | test_triage_names_shaping_and_deferrable_tiers | `shaping`, `deferrable` | keep-structural | the literal `SHAPING` / `DEFERRABLE` tier labels the reference requires on every tagged open question — label vocabulary written into artifacts, not prose |
| test_knowledge_triage.py:108, 111 | test_rationale_bar_higher_than_spec_present | `spec`, `gate`, `higher`, `narrower` | delete | prose pin; nothing else in the function |
| test_knowledge_triage.py:125 | test_shaping_route_cites_the_review_verdict_timing | `design-conformance` | keep-structural | a review lens dimension name (identifier) |
| test_knowledge_triage.py:128, 131 | test_shaping_route_cites_the_review_verdict_timing | `before`, `verdict`, `routed`, `routed research` | prune | prose words |
| test_knowledge_triage.py:141, 144 | test_never_websearch_restated | `never`, `websearch`, `closed-world` | delete | prose pin; nothing else in the function |
| test_knowledge_triage.py:182 | test_cross_severing_guard_restates_review_verdict_vocabulary | `unchanged` | prune | prose word; the `PASS_WITH_NOTES` / `NEEDS_REVISION` verdict tokens stay |
| test_knowledge_triage.py:266 | test_carrier_contains_all_three_bucket_names | `craft`, `domain-convention`, `project-local` | keep-structural | bucket vocabulary: the values of the `evidence_needed:` tag, also byte-pinned in the plan's fence |

## Mapping

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `test_architecture_skill.py::test_never_blocks_language_present` (deleted) | architecture-design stops saying a missing ARCHITECTURE.md never blocks | `standing.warn` | checker rule id |
| `test_architecture_skill.py::test_skill_states_redesign_updates_decisions_rules_guards` (deleted) | the re-design / re-ratify procedure drops out of the skill | skill lens `omission` | review lens dimension |
| `test_architecture_skill.py::test_guard_failure_message_fields_stated` (deleted) | the guard failure message loses a field (rule id, offending path, conform / change the rule and its guard) | skill lens `omission` | review lens dimension |
| `test_architecture_skill.py::test_skill_records_package_tests_when_absent_and_commits_edited_config` (pruned `Step 3 edited`) | Step 5 stops committing the files Step 3 edited | the same function keeps `KICKOFF-DEFAULTS.md` inside `## Step 5`; skill lens `omission` | kept structural test |
| `test_design_md_schema_keys.py::test_non_spec_keys_are_labelled_and_token_groups_named` (pruned `extension`, `export`; renamed) | an extension key's bullet stops calling it an extension that export omits | `test_design_md_schema_keys.py::test_schema_keys_documented_and_token_groups_named` keeps each extension key's bullet and the spec-meta no-label absence check; docs lens `omission` | kept structural test |
| `test_design_md_schema_keys.py::test_derivation_contract_excludes_elevation`, `::test_derivation_contract_roster_catches_elevation_readded`, `::test_derivation_contract_tolerates_clarifying_elevation_note_outside_roster` (deleted) | the Derivation contract roster names more or fewer than the five token groups | review-only (P2: no heading or gate marker to re-anchor on); docs lens `inconsistency` | review-only |
| `test_design_md_schema_keys.py::test_component_properties_header_not_claimed_closed` (pruned Typography `closed`) | `## Typography` stops calling its property set closed | docs lens `omission`; the same function keeps the Components-header absence checks | review lens dimension |
| `test_design_md_schema_keys.py::test_shapes_rounded_bullet_states_not_radius` (pruned `not`, `radius`; renamed) | the `rounded` bullet loses its not-`radius` correction | `test_design_md_schema_keys.py::test_shapes_documents_rounded_bullet`; docs lens `omission` | kept structural test |
| `test_design_md_schema_keys.py::test_shapes_header_distinguishes_extension_bullets_from_spec_keys`, `::test_overview_brand_header_distinguishes_extension_bullets_from_spec_keys` (deleted) | a section header folds extension keys under a spec-confirmation hedge | docs lens `inconsistency` | review lens dimension |
| `test_design_md_schema_keys.py::test_grounding_note_covers_the_consumer_behavior_claim`, `::test_grounding_note_catches_reverted_key_sets_only_scope` (deleted) | the grounding note stops covering the accept-with-warning behaviour claim | docs lens `incorrect-fact`; the version stamp stays in `test_schema_keys_documented_and_token_groups_named` (c) | review lens dimension |
| `test_design_md_schema_keys.py::test_generation_checklist_lint_step_does_not_require_stripping_warned_extension_properties`, `::test_generation_checklist_lint_step_catches_reverted_unconditional_resolve`, helper `_generation_checklist_step` (deleted) | checklist step 5 goes back to an unconditional "resolve violations" | docs lens `inconsistency` (step 5 against `## Components`) | review lens dimension |
| `test_design_system_skill.py::test_never_blocks_language_present` (pruned `never blocks`, `never required`; renamed) | design-system stops saying a missing DESIGN.md never blocks | `test_design_system_skill.py::test_gate_marker_registered` (marker `design-system.never-blocks`) and checker rule `standing.warn` | kept structural test |
| `test_knowledge_triage.py::test_rationale_bar_higher_than_spec_present` (deleted) | the SHAPING bar stops being stated as narrower than spec's gate | skill lens `omission` | review lens dimension |
| `test_knowledge_triage.py::test_shaping_route_cites_the_review_verdict_timing` (pruned `before`, `verdict`, `routed`; renamed) | SHAPING research stops being routed before the verdict | `test_knowledge_triage.py::test_shaping_route_names_the_design_conformance_lens`; skill lens `omission` | kept structural test |
| `test_knowledge_triage.py::test_never_websearch_restated` (deleted) | the extracted reference stops restating the closed-world, never-WebSearch constraint | skill lens `omission` | review lens dimension |
| `test_knowledge_triage.py::test_cross_severing_guard_restates_review_verdict_vocabulary` (pruned `unchanged`) | the reference stops saying the verdict vocabulary is unchanged | the same function keeps the verdict tokens; skill lens `inconsistency` | kept structural test |

## Classifier after the edit (P7)

`python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py`:

| file | class | has_pins | remaining hits |
|---|---|---|---|
| test_architecture_skill.py | structure (override) | no | none; the file's existing override reason still names the removed tokens and needs W2-01's rewrite |
| test_design_md_schema_keys.py | behavior | yes | the two `confirm`/`spec` absence collocations (keep-absence above) |
| test_design_system_skill.py | structure (override) | yes | the eight `##` section names (keep-structural above) |
| test_knowledge_triage.py | behavior | yes | tier labels, `design-conformance`, bucket names (keep-structural above) |

With `--candidates`, the remaining prose rows are exactly those ten literals, each with a keep row in Decisions.

## Renames

- `test_design_md_schema_keys.py::test_non_spec_keys_are_labelled_and_token_groups_named` -> `test_schema_keys_documented_and_token_groups_named`
- `test_design_md_schema_keys.py::test_shapes_rounded_bullet_states_not_radius` -> `test_shapes_documents_rounded_bullet`
- `test_design_system_skill.py::test_never_blocks_language_present` -> `test_names_product_principles_reject_rule`
- `test_knowledge_triage.py::test_shaping_route_cites_the_review_verdict_timing` -> `test_shaping_route_names_the_design_conformance_lens`
