# Batch 4 candidate list

Every literal that a test in the four test roots asserts against text read from a skill, agent or reference markdown file, in the forms batch 3 could not see. That covers 1-2 word literals and single terms, literals inside local helpers (validators too) whose parameter receives markdown text, `if`-required and returned literals, `.index()` lookups, regex searches run on prose, and needles routed through containers and helper parameters (W1-07). The classifier gives each candidate one of two classes. Only `prose` counts as a pin. `structural` rows are pre-classed with a reason.

**Final state (W2-01).** This list was regenerated at the end of the build, from a clean detached worktree of the W2-01 commit, and it replaces the W0-01 list. Every candidate the W1 tasks pruned or deleted is gone from it. Every `prose` row still listed was judged and kept by a W1 task or by W2-01. Its reason cell ends with `→ <mapping file> Decisions row N`. N counts the data rows of that file's `## Decisions` table, then its `### Decisions` table under `## W2-01 additions`, in order. In `mapping-code.md`, N equals the `#` column. The throwaway script `decide.py` added those pointers, and its text is in `census-report.md`. It found a Decisions row for all 106 prose rows, and none was left undecided.

Command, run from the worktree root:

```
python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --candidates
```

The structural rules live in the `literal_class` docstring, and the detected forms in the `pin_candidates` docstring, both in that script. W2-01 added one form: a negated `re.search` in a comprehension filter over `.items()` values, which collects what a text does not name. Program output is still excluded, as batch-3 W3-01 fixed: subprocess and checker output, parsed json/yaml values, production calls, and temp-dir output other than an installed copy's skill file. Comments are stripped before scanning, so line numbers are source lines.

**Kept by batch 3.** These rows are class `kept-batch3` and out of scope, per the intent's Out of scope:

- the two `pinned_sentence_ok(s, ...)` lines in `loom-workflow/tests/loom-visualization/test_templates.py` that run the three kept gate polarity checks, whose literals `MERMAID_PIN`, `TABLE_ASCII_PIN` and `CHAT_PROCEEDS_PIN` pass through a parameter the detector cannot follow;
- the Codex `defaultPrompt` string in `loom-workflow/tests/decision-map/test_skill_doc.py`.

## A5 — execution-test recount at the base

Command: `python3 <classifier> --count-exec <worktree> --list`. The counting code is the batch-3 method, and no batch-4 task changed it.

| ref | executing test functions |
|---|---|
| base `1ef82fe8` (with that commit's own classifier) | **1927** |
| base `1ef82fe8` (with the W0-01 classifier) | **1927** |
| `b13e646d` (branch HEAD before W0-01) | **1927** (the `--list` output is identical to the base's) |

The batch-3 HEAD figure was 1927. It is confirmed at `1ef82fe8`, so 1927 is this batch's baseline. The count at the end of the build is in `census-report.md`.

## Counts

A file is listed when it has at least one candidate. W0-01 counted 233 prose, 373 structural and 3 kept-batch3 rows in 33 files with a prose candidate. The widened census of W1-07 and W2-01 lists more structural rows, because it sees more forms.

| plugin | prose | structural | kept-batch3 | files with >=1 prose candidate |
|---|---|---|---|---|
| root tests | 0 | 16 | 0 | 0 |
| loom-code | 35 | 129 | 0 | 13 |
| loom-design | 16 | 103 | 0 | 2 |
| loom-workflow | 55 | 361 | 3 | 7 |
| **total** | 106 | 609 | 3 | 22 |

## root tests

### tests/test_loom_plugin_install_layout.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| tests/test_loom_plugin_install_layout.py:124 | test_agy_install_every_skill_folder_discoverable | '^name:\\s*{}\\s*$' (re.search) | structural | line grammar placeholder |
| tests/test_loom_plugin_install_layout.py:198 | _resolve_local_contract | '\\[([^]\\n]+)\\]\\(([^)]+)\\)' (re.findall) | structural | code identifier |
| tests/test_loom_plugin_install_layout.py:215 | _resolve_local_contract | '(?:follows?\|following\|load\|read\|check\|reference\|criteria table\|builds on\|(?:are\|is\|live\|lives) in)[^.]{0,180}`{}`\|`{}`[^.]{0,180}(?:load\|reference\|on demand\|pull)' (re.search) | structural | line grammar placeholder |
| tests/test_loom_plugin_install_layout.py:262 | _assert_local_contract_graph | 'one-way-door.md' (stored in via _resolve_local_contract()) | structural | path |
| tests/test_loom_plugin_install_layout.py:422 | test_isolated_loom_plugins_are_standalone_and_compose_by_public_contract | 'loom-code' (assert in) | structural | names a skill, plugin or script (a hyphenated repo name) |
| tests/test_loom_plugin_install_layout.py:425 | test_isolated_loom_plugins_are_standalone_and_compose_by_public_contract | 'docs/loom/intent/<change-id>.md' (assert in) | structural | line grammar placeholder |
| tests/test_loom_plugin_install_layout.py:426 | test_isolated_loom_plugins_are_standalone_and_compose_by_public_contract | 'PRINCIPLES.md' (assert in) | structural | path |
| tests/test_loom_plugin_install_layout.py:427 | test_isolated_loom_plugins_are_standalone_and_compose_by_public_contract | 'DESIGN.md' (assert in) | structural | path |
| tests/test_loom_plugin_install_layout.py:428 | test_isolated_loom_plugins_are_standalone_and_compose_by_public_contract | 'docs/loom/<change-id>/' (assert in) | structural | line grammar placeholder |
| tests/test_loom_plugin_install_layout.py:429 | test_isolated_loom_plugins_are_standalone_and_compose_by_public_contract | 'docs/loom/<change-id>/' (assert in) | structural | line grammar placeholder |
| tests/test_loom_plugin_install_layout.py:618 | test_lookup_table_lives_in_one_place_and_every_skill_links_it | 'locate-loom-code.md`' (assert in) | structural | path |

### tests/test_loom_skill_description_catalog.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| tests/test_loom_skill_description_catalog.py:67 | _baseline | '```json description-baseline\\n(.*?)\\n```' (re.search) | structural | code identifier |
| tests/test_loom_skill_description_catalog.py:87 | _routing_cases | '```json routing-cases\\n(?P<body>.*?)\\n```' (re.search) | structural | line grammar placeholder |
| tests/test_loom_skill_description_catalog.py:162 | test_router_tables_preserve_direct_leaf_targets | '\\]\\(\\.\\./([^/]+)/SKILL\\.md\\)' (re.findall) | structural | path |

### tests/test_tests_folder_convention.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| tests/test_tests_folder_convention.py:147 | test_ci_runs_the_same_groups_as_the_inventory | 'run_package_tests\\.py --loom-family --only (\\S+)' (re.findall) | structural | command |
| tests/test_tests_folder_convention.py:157 | test_guidance_and_workflows_name_no_old_test_path | '(loom-code\|loom-design\|loom-workflow)/scripts/[^ ]*test_\|skills/[a-z-]*/(scripts\|probes)/test_\|(^\|[^/])scripts/test_\|\\.claude/hooks/test_' (re.finditer) | structural | path |

### Decisions — root tests

The decisions live in the mapping files. Each prose row above ends with a pointer to its Decisions row.

## loom-code

### loom-code/tests/test_acceptance_test_report_shape.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_acceptance_test_report_shape.py:39 | _fenced_blocks | '^```markdown\\n(.*?)^```$' (re.findall) | structural | code identifier |
| loom-code/tests/test_acceptance_test_report_shape.py:50 | _criterion_table | '## What you asked for, one line at a time' (assert in) | structural | markdown heading |
| loom-code/tests/test_acceptance_test_report_shape.py:73 | test_template_has_one_row_per_criterion_and_evidence_file_path | 'works\|partly\|not verified\|fails' (re.search) | prose | regex alternative 'works' is prose → `mapping-code.md` Decisions row 2 |
| loom-code/tests/test_acceptance_test_report_shape.py:76 | test_template_has_one_row_per_criterion_and_evidence_file_path | 'docs/loom/<change-id>/evidence/acceptance-test-evidence.md' (assert in) | structural | line grammar placeholder |
| loom-code/tests/test_acceptance_test_report_shape.py:118 | test_row_has_carried_over_marker_with_reason | '^carried over — \\S.*$' (re.match) | prose | phrase of 3+ words → `mapping-code.md` Decisions row 3 |
| loom-code/tests/test_acceptance_test_report_shape.py:127 | test_retested_row_has_no_carry_reason | 're-tested' (assert ==) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 4 |
| loom-code/tests/test_acceptance_test_report_shape.py:192 | test_rules_live_in_contract_and_template | 'docs/loom/<change-id>/evidence/acceptance-test-evidence.md' (assert in) | structural | line grammar placeholder |
| loom-code/tests/test_acceptance_test_report_shape.py:202 | test_no_new_gate_marker | 'docs/loom/<change-id>/evidence/acceptance-test-evidence.md' (assert in) | structural | line grammar placeholder |

### loom-code/tests/test_adversary_layout.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_adversary_layout.py:152 | _base_commit | 'at commit `([0-9a-f]{7,40})`' (re.search) | prose | phrase of 3+ words → `mapping-code.md` Decisions row 7 |
| loom-code/tests/test_adversary_layout.py:162 | _split_commit | 'at split commit `([0-9a-f]{7,40})`' (re.search) | prose | phrase of 3+ words → `mapping-code.md` Decisions row 8 |
| loom-code/tests/test_adversary_layout.py:321 | test_protocol_keeps_no_recipe_body | 'Recording' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-code/tests/test_adversary_layout.py:321 | test_protocol_keeps_no_recipe_body | 'Reuse first, update with evidence' (assert in) | prose | phrase of 3+ words → `mapping-code.md` Decisions row 9 |
| loom-code/tests/test_adversary_layout.py:346 | test_no_kind_rule_appears_outside_its_own_file | 'Attempt the prose temptations verbatim' (return in via _markers_found()) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 1 |
| loom-code/tests/test_adversary_layout.py:346 | test_no_kind_rule_appears_outside_its_own_file | 'Prefer cases that live as real tests afterwards.' (return in via _markers_found()) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 1 |
| loom-code/tests/test_adversary_layout.py:346 | test_no_kind_rule_appears_outside_its_own_file | 'Read the instruction as an agent under time pressure' (return in via _markers_found()) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 1 |
| loom-code/tests/test_adversary_layout.py:346 | test_no_kind_rule_appears_outside_its_own_file | 'Red-team it' (return in via _markers_found()) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-code/tests/test_adversary_layout.py:346 | test_no_kind_rule_appears_outside_its_own_file | 'a surviving mutant is a test that asserts nothing' (return in via _markers_found()) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 1 |
| loom-code/tests/test_adversary_layout.py:346 | test_no_kind_rule_appears_outside_its_own_file | 'name a behaviour the requirement permits' (return in via _markers_found()) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 1 |
| loom-code/tests/test_adversary_layout.py:346 | test_no_kind_rule_appears_outside_its_own_file | 'path traversal' (return in via _markers_found()) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 1 |
| loom-code/tests/test_adversary_layout.py:346 | test_no_kind_rule_appears_outside_its_own_file | 'the migration from what exists today' (return in via _markers_found()) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 1 |
| loom-code/tests/test_adversary_layout.py:346 | test_no_kind_rule_appears_outside_its_own_file | 'the same input one character different' (return in via _markers_found()) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 1 |
| loom-code/tests/test_adversary_layout.py:409 | test_correspondence_note_maps_every_rule_to_a_file_that_exists | '(preamble)' (assert ==) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 10 |

### loom-code/tests/test_adversary_protocol.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_adversary_protocol.py:71 | test_agent_return_block_carries_the_three_counts | 'attack_points:' (assert in) | structural | field key or label |
| loom-code/tests/test_adversary_protocol.py:73 | test_agent_return_block_carries_the_three_counts | 'committed' (assert in) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 11 |
| loom-code/tests/test_adversary_protocol.py:73 | test_agent_return_block_carries_the_three_counts | 'earned_a_program' (assert in) | structural | code identifier |
| loom-code/tests/test_adversary_protocol.py:73 | test_agent_return_block_carries_the_three_counts | 'found' (assert in) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 12 |
| loom-code/tests/test_adversary_protocol.py:193 | _head_is_a_case | '\\bcases?\\b\|\\bprobes?\\b\|\\bprograms?\\b\|ケース\|案例' (re.search) | prose | regex alternative '\\bcases?\\b' is prose → `mapping-code.md` Decisions row 13 |
| loom-code/tests/test_adversary_protocol.py:195 | _head_is_a_case | '[A-Za-z][\\w-]*' (re.match) | structural | code identifier |
| loom-code/tests/test_adversary_protocol.py:226 | case_counts | '(?P<pre>{})\\s*\\**\\s*(?P<n1>{})\|(?P<n2>{})\\s*(?:つ\|個\|件\|の)?\\s*(?P<post>{})\|\\b(?P<n3>{})\\b(?:\\s+[A-Za-z][\\w-]*){0,3}\\s+(?P<post_en>{})\\b' (re.finditer) | structural | line grammar placeholder |
| loom-code/tests/test_adversary_protocol.py:329 | test_body_and_frontmatter_helpers_synthetic | 'name: adversary' (assert .startswith()) | structural | field key or label |
| loom-code/tests/test_adversary_protocol.py:331 | test_body_and_frontmatter_helpers_synthetic | '# adversary subagent' (assert .startswith()) | structural | markdown heading |

### loom-code/tests/test_adversary_recipe_shape.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_adversary_recipe_shape.py:253 | _without_routing | '## Which recipe to read' (if requires) | structural | markdown heading |
| loom-code/tests/test_adversary_recipe_shape.py:315 | shape_violations | '\\[[^\\]]*\\]\\((?P<target>[^)#][^)]*)\\)' (re.finditer) | structural | line grammar placeholder |
| loom-code/tests/test_adversary_recipe_shape.py:316 | shape_violations | 'adversarial.md' (if requires) | structural | path |

### loom-code/tests/test_adversary_routing.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_adversary_routing.py:157 | _cell | '\\[.*?\\]\\((?P<target>[^)]+)\\)' (re.search) | structural | line grammar placeholder |
| loom-code/tests/test_adversary_routing.py:165 | _routing_rows | '## Which recipe to read' (if requires) | structural | markdown heading |
| loom-code/tests/test_adversary_routing.py:170 | _routing_rows | '^\\\|(?P<cells>.+)\\\|$' (re.match) | structural | table row or cell |
| loom-code/tests/test_adversary_routing.py:222 | recipe_kind | '.md' (assert .endswith()) | structural | path |
| loom-code/tests/test_adversary_routing.py:222 | recipe_kind | 'adversarial-' (assert .startswith()) | structural | code identifier |
| loom-code/tests/test_adversary_routing.py:368 | test_contract_routes_through_the_protocol_to_each_recipe | '`loom-code/skills/closing-review/references/adversarial.md`' (assert in) | structural | path |
| loom-code/tests/test_adversary_routing.py:382 | test_protocol_plus_the_matching_recipe_is_the_whole_procedure | '[`adversarial.md`](adversarial.md)' (assert in) | structural | path |
| loom-code/tests/test_adversary_routing.py:383 | test_protocol_plus_the_matching_recipe_is_the_whole_procedure | '\\[.*?\\]\\((?P<target>[^)]+)\\)' (re.finditer) | structural | line grammar placeholder |

### loom-code/tests/test_agy_tool_mapping.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_agy_tool_mapping.py:50 | _claude_only_violations | 'Antigravity CLI' (.index()) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-code/tests/test_agy_tool_mapping.py:85 | _role_dispatch_ok | '`self`' (return in) | structural | code identifier |
| loom-code/tests/test_agy_tool_mapping.py:116 | test_reference_dispatches_every_role_as_self_reading_its_contract | 'TypeName: "self"' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |

### loom-code/tests/test_architecture_doc_consumers.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_architecture_doc_consumers.py:21 | _step5_architecture_paragraph | '## Step 5' (.index()) | structural | markdown heading |
| loom-code/tests/test_architecture_doc_consumers.py:31 | test_write_plan_step5_names_architecture_risk_line_and_ratification | 'Risk line' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-code/tests/test_architecture_doc_consumers.py:32 | test_write_plan_step5_names_architecture_risk_line_and_ratification | 'ratified-by: <name> <date>' (assert in) | structural | line grammar placeholder |
| loom-code/tests/test_architecture_doc_consumers.py:37 | test_code_lens_has_architecture_conformance_na_without_doc | '## Code — twelve dimensions' (.index()) | structural | markdown heading |
| loom-code/tests/test_architecture_doc_consumers.py:37 | test_code_lens_has_architecture_conformance_na_without_doc | '## Docs' (.index()) | structural | markdown heading |
| loom-code/tests/test_architecture_doc_consumers.py:38 | test_code_lens_has_architecture_conformance_na_without_doc | '^\\\| architecture-conformance \\\|.*at least `important`' (re.search) | structural | table row or cell |
| loom-code/tests/test_architecture_doc_consumers.py:39 | test_code_lens_has_architecture_conformance_na_without_doc | '^\\\| architecture \\\| .*SOLID' (re.search) | structural | table row or cell |
| loom-code/tests/test_architecture_doc_consumers.py:40 | test_code_lens_has_architecture_conformance_na_without_doc | '## Code' (.index()) | structural | markdown heading |
| loom-code/tests/test_architecture_doc_consumers.py:40 | test_code_lens_has_architecture_conformance_na_without_doc | '## Severity and verdict' (.index()) | structural | markdown heading |
| loom-code/tests/test_architecture_doc_consumers.py:42 | test_code_lens_has_architecture_conformance_na_without_doc | '`ARCHITECTURE.md`' (assert in) | structural | path |
| loom-code/tests/test_architecture_doc_consumers.py:42 | test_code_lens_has_architecture_conformance_na_without_doc | '`N/A`' (assert in) | structural | path |
| loom-code/tests/test_architecture_doc_consumers.py:43 | test_code_lens_has_architecture_conformance_na_without_doc | 'ratified-by: <name> <date>' (assert in) | structural | line grammar placeholder |
| loom-code/tests/test_architecture_doc_consumers.py:51 | test_reviewer_code_row_lists_architecture_conformance | 'architecture-conformance' (assert in) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 15 |

### loom-code/tests/test_build_mechanical_checks.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_build_mechanical_checks.py:46 | _other_role_program_edit_sentences | 'adversarial program' (return in) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 16 |
| loom-code/tests/test_build_mechanical_checks.py:107 | _discard_literals_outside_rule | 'git checkout --' (return in) | structural | command |
| loom-code/tests/test_build_mechanical_checks.py:107 | _discard_literals_outside_rule | 'git clean' (return in) | structural | command |
| loom-code/tests/test_build_mechanical_checks.py:107 | _discard_literals_outside_rule | 'git reset --hard' (return in) | structural | command |
| loom-code/tests/test_build_mechanical_checks.py:107 | _discard_literals_outside_rule | 'git restore' (return in) | structural | command |
| loom-code/tests/test_build_mechanical_checks.py:107 | _discard_literals_outside_rule | 'git worktree remove --force' (return in) | structural | command |
| loom-code/tests/test_build_mechanical_checks.py:114 | _implementer_floor_sentences | 'floor' (return in) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 17 |
| loom-code/tests/test_build_mechanical_checks.py:158 | _dead_pointer_hits | 'attack[- ]catalogue\|\\bcatalogue\\b\|\\btrailer\\b' (re.findall) | prose | regex alternative 'attack[- ]catalogue' is prose → `mapping-code.md` Decisions row 18 |
| loom-code/tests/test_build_mechanical_checks.py:179 | test_build_verify_step_links_adversarial_recipes_in_place | '[`adversarial.md`](../closing-review/references/adversarial.md)' (assert in) | structural | path |
| loom-code/tests/test_build_mechanical_checks.py:193 | test_adversary_return_format_marks_probe_status | '^probes: \\[\\{artifact: .+, status: reused \\\| modified \\\| new, reason: .+\\}\\]$' (re.search) | structural | table row or cell |
| loom-code/tests/test_build_mechanical_checks.py:194 | test_adversary_return_format_marks_probe_status | '^adversarial: \\[\\{command: ' (re.search) | structural | field key or label |
| loom-code/tests/test_build_mechanical_checks.py:195 | test_adversary_return_format_marks_probe_status | '^findings: \\[\\{severity: ' (re.search) | structural | field key or label |

### loom-code/tests/test_build_recovery_rules.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_build_recovery_rules.py:90 | _early_sections | '## 1. Establish scope' (.index()) | structural | markdown heading |
| loom-code/tests/test_build_recovery_rules.py:91 | _early_sections | '## 3. Verify integration' (.index()) | structural | markdown heading |
| loom-code/tests/test_build_recovery_rules.py:100 | _recovery_passage | '<!-- gate: build.absence-recovery -->' (.index()) | structural | gate or HTML marker |
| loom-code/tests/test_build_recovery_rules.py:101 | _recovery_passage | '<!-- /gate -->' (.index()) | structural | gate or HTML marker |
| loom-code/tests/test_build_recovery_rules.py:121 | _mapping_restatements | '(?<![\\w-])(?:intents?\|specs?\|plans?\|diffs?\|attestations?\|acceptance[- ]test reports?\|adversarial programs?)(?![\\w-])' (re.search) | prose | phrase of 3+ words → `mapping-code.md` Decisions row 19 |
| loom-code/tests/test_build_recovery_rules.py:122 | _mapping_restatements | '(?<![\\w-])(?:capture-intent\|write-spec\|write-plan\|closing-review)(?![\\w-])\|(?<![\\w-])(?:Ship\|Maintain)(?![\\w-])' (re.search) | structural | code identifier |
| loom-code/tests/test_build_recovery_rules.py:122 | _mapping_restatements | '(?<![\\w-])(?:produce[ds]?\|produces\|producing\|producer\|owns\|owned\|owner\|owes\|upstream\|downstream\|comes from\|belongs to\|responsible for)(?![\\w-])' (re.search) | prose | phrase of 3+ words → `mapping-code.md` Decisions row 19 |
| loom-code/tests/test_build_recovery_rules.py:134 | test_RL_02_no_second_copy_of_the_artifact_station_mapping | 'actions[].owner' (if requires) | structural | code identifier |
| loom-code/tests/test_build_recovery_rules.py:134 | test_RL_02_no_second_copy_of_the_artifact_station_mapping | 'loom-code/contract/manifest.yaml' (if requires) | structural | path |
| loom-code/tests/test_build_recovery_rules.py:134 | test_RL_02_no_second_copy_of_the_artifact_station_mapping | 'stations[].produces' (if requires) | structural | code identifier |
| loom-code/tests/test_build_recovery_rules.py:177 | test_RL_12_the_pointer_is_not_a_second_copy_of_the_rule | '(?<![\\w-])(?:capture-intent\|write-spec\|write-plan\|closing-review)(?![\\w-])\|(?<![\\w-])(?:Ship\|Maintain)(?![\\w-])' (re.findall) | structural | code identifier |

### loom-code/tests/test_closing_review_recovery_rules.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_closing_review_recovery_rules.py:81 | _recovery_passage | '<!-- gate: review.absence-recovery -->' (.index()) | structural | gate or HTML marker |
| loom-code/tests/test_closing_review_recovery_rules.py:82 | _recovery_passage | '<!-- /gate -->' (.index()) | structural | gate or HTML marker |
| loom-code/tests/test_closing_review_recovery_rules.py:102 | _mapping_restatements | '(?<![\\w-])(?:intents?\|specs?\|plans?\|diffs?\|attestations?\|acceptance[- ]test reports?\|adversarial programs?)(?![\\w-])' (re.search) | prose | phrase of 3+ words → `mapping-code.md` Decisions row 21 |
| loom-code/tests/test_closing_review_recovery_rules.py:103 | _mapping_restatements | '(?<![\\w-])(?:capture-intent\|write-spec\|write-plan\|closing-review)(?![\\w-])\|(?<![\\w-])(?:Build\|Ship\|Maintain)(?![\\w-])' (re.search) | structural | code identifier |
| loom-code/tests/test_closing_review_recovery_rules.py:103 | _mapping_restatements | '(?<![\\w-])(?:produce[ds]?\|produces\|producing\|producer\|owns\|owned\|owner\|owes\|upstream\|downstream\|comes from\|belongs to\|responsible for)(?![\\w-])' (re.search) | prose | phrase of 3+ words → `mapping-code.md` Decisions row 21 |

### loom-code/tests/test_codex_hook_trust_contract.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_codex_hook_trust_contract.py:16 | test_first_contact_new_worktree_does_not_create_loom_trust_work | '<!-- gate: write-plan.codex-installed-hook-trust-boundary -->' (assert count) | structural | gate or HTML marker |

### loom-code/tests/test_contract_manifest.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_contract_manifest.py:169 | test_manifest_templates_and_mechanisms_agree_without_lane | '(?m)^Removed `default-lane` — .+ \\(\\d{4}-\\d{2}-\\d{2}\\)$' (re.search) | structural | line grammar placeholder |
| loom-code/tests/test_contract_manifest.py:187 | test_second_vendor_modes_remove_none_and_default_to_suggest | 'second-vendor: suggest' (assert in) | structural | field key or label |
| loom-code/tests/test_contract_manifest.py:242 | test_manifest_station_equals_closing_review_folder | '^name: closing-review$' (re.search) | structural | field key or label |
| loom-code/tests/test_contract_manifest.py:273 | test_finalize_review_command_and_gate_ids_unchanged | '<!-- gate: {} -->' (assert in) | structural | gate or HTML marker |

### loom-code/tests/test_dispatch_profile_contract.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_dispatch_profile_contract.py:58 | test_atomic_claude_dispatch_gate_is_registered_with_executable_eval | '<!-- gate: {} -->' (assert count) | structural | gate or HTML marker |
| loom-code/tests/test_dispatch_profile_contract.py:59 | test_atomic_claude_dispatch_gate_is_registered_with_executable_eval | '<!-- /gate -->' (assert count) | structural | gate or HTML marker |

### loom-code/tests/test_dispatch_profile_resolver.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_dispatch_profile_resolver.py:465 | test_contract_defines_the_executable_json_boundary | 'python3 ${CLAUDE_PLUGIN_ROOT}/scripts/dispatch_profile.py' (assert in) | structural | line grammar placeholder |
| loom-code/tests/test_dispatch_profile_resolver.py:466 | test_contract_defines_the_executable_json_boundary | 'python3 <loom-code>/scripts/dispatch_profile.py' (assert in) | structural | line grammar placeholder |
| loom-code/tests/test_dispatch_profile_resolver.py:468 | test_contract_defines_the_executable_json_boundary | '"event": "initial"' (assert in) | structural | field key or label |
| loom-code/tests/test_dispatch_profile_resolver.py:469 | test_contract_defines_the_executable_json_boundary | '"event": "after-execution"' (assert in) | structural | field key or label |
| loom-code/tests/test_dispatch_profile_resolver.py:470 | test_contract_defines_the_executable_json_boundary | '"event": "host-rejection"' (assert in) | structural | field key or label |
| loom-code/tests/test_dispatch_profile_resolver.py:471 | test_contract_defines_the_executable_json_boundary | 'capabilities' (assert in) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 23 |
| loom-code/tests/test_dispatch_profile_resolver.py:472 | test_contract_defines_the_executable_json_boundary | 'completed_redispatches' (assert in) | structural | code identifier |
| loom-code/tests/test_dispatch_profile_resolver.py:478 | test_stations_point_to_the_executable_resolver_contract | '](../../references/dispatch-profile.md)' (assert in) | structural | path |

### loom-code/tests/test_expert_mode_skill.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_expert_mode_skill.py:72 | test_skill_text_evaluates_no_gate | 'loom_checker\\.py (selection [\\w-]+\|[\\w-]+)' (re.findall) | structural | path |
| loom-code/tests/test_expert_mode_skill.py:89 | test_skill_round1_boundary_intent_skip_and_withdrawal_split | 'selection cancel <change-id>' (stored in) | structural | line grammar placeholder |
| loom-code/tests/test_expert_mode_skill.py:166 | test_expert_mode_holds_the_suggestion_rules_once | '--origin agent' (assert count) | structural | command |

### loom-code/tests/test_legacy_contract_removed.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_legacy_contract_removed.py:169 | test_live_consumers_require_contract_two | 'contract --require {}' (assert in) | structural | line grammar placeholder |

### loom-code/tests/test_lenses_deletion_first.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_lenses_deletion_first.py:22 | test_reviewer_docs_row_ends_with_deletion_first | 'deletion-first' (assert .endswith()) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 24 |
| loom-code/tests/test_lenses_deletion_first.py:34 | test_reviewer_skill_row_ends_with_deletion_first | 'deletion-first' (assert .endswith()) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 25 |

### loom-code/tests/test_one_way_door_copies.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_one_way_door_copies.py:55 | class_titles | '\\s*-\\s*\\*\\*\\(([a-e])\\)\\s*(.+?)\\*\\*\\s*—' (re.match) | structural | code identifier |

### loom-code/tests/test_plan_simplicity_text.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_plan_simplicity_text.py:26 | _step | '\\*\\*Simplicity check\\.\\*\\*(.*?)\\n\\n' (re.search) | structural | code identifier |
| loom-code/tests/test_plan_simplicity_text.py:28 | _step | 'references/plan-simplicity.md' (assert in) | structural | path |
| loom-code/tests/test_plan_simplicity_text.py:29 | _step | '\\*\\*Simplicity check\\.\\*\\*(.*?)(?:\\n\\n\|\\Z)' (re.search) | structural | code identifier |
| loom-code/tests/test_plan_simplicity_text.py:50 | _plan_lens | '^## Plan lens\\n(.*?)(?=^## \|\\Z)' (re.search) | structural | markdown heading |

### loom-code/tests/test_probes_cumulative_boundary_reassessment.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_probes_cumulative_boundary_reassessment.py:88 | _fenced_json | '```json {}\\n(.*?)\\n```' (re.search) | structural | line grammar placeholder |
| loom-code/tests/test_probes_cumulative_boundary_reassessment.py:98 | _frozen_rubric | '<!-- BEGIN frozen-rubric -->\\n(.*?)\\n<!-- END frozen-rubric -->' (re.search) | structural | gate or HTML marker |
| loom-code/tests/test_probes_cumulative_boundary_reassessment.py:258 | test_fixture_spec_is_complete_and_bounded | 'sha1' (assert ==) | structural | code identifier |

### loom-code/tests/test_probes_language_policy.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_probes_language_policy.py:92 | test_templates_cjk_absent | '[一-鿿]' (re.findall) | structural | ALL_CAPS token, rule id or verdict |
| loom-code/tests/test_probes_language_policy.py:132 | test_reviewer_nitclause_absent | 'docs-lint' (assert in) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 26 |
| loom-code/tests/test_probes_language_policy.py:136 | test_reviewer_nitclause_absent | 'Conventional Comments' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-code/tests/test_probes_language_policy.py:136 | test_reviewer_nitclause_absent | 'EARS' (assert in) | structural | ALL_CAPS token, rule id or verdict |
| loom-code/tests/test_probes_language_policy.py:136 | test_reviewer_nitclause_absent | 'English' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-code/tests/test_probes_language_policy.py:136 | test_reviewer_nitclause_absent | '`nit`' (assert in) | structural | code identifier |
| loom-code/tests/test_probes_language_policy.py:160 | test_specminimal_ears_absent | '→ Acceptance #' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-code/tests/test_probes_language_policy.py:163 | test_specminimal_ears_absent | '^\\s*(WHEN\\b\|WHILE\\b\|WHERE\\b\|IF\\b.*\\bTHEN\\b\|The\\s+\\S+.*\\bshall\\b)' (re.match) | structural | code identifier |
| loom-code/tests/test_probes_language_policy.py:189 | _has_negation | "\\b(?:not\|never\|no)\\b\|n't" (re.search) | prose | regex alternative '\\b(?:not|never|no)\\b' is prose → `mapping-code.md` Decisions row 27 |
| loom-code/tests/test_probes_language_policy.py:195 | _sentence_names_shape_unnegated | 'test_<unit>_<state>_<expected>' (return in) | structural | line grammar placeholder |
| loom-code/tests/test_probes_language_policy.py:199 | _paragraph_names_shape_and_english | 'english' (if requires) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 39 |
| loom-code/tests/test_probes_language_policy.py:212 | test_agents_probename_absent | 'test_<unit>_<state>_<expected>' (assert in) | structural | line grammar placeholder |

### loom-code/tests/test_review_convergence_contract.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_review_convergence_contract.py:18 | test_review_episode_has_three_distinct_content_rounds_and_no_identity_reset | '<!-- gate: review.bounded-episode -->' (assert in) | structural | gate or HTML marker |
| loom-code/tests/test_review_convergence_contract.py:19 | test_review_episode_has_three_distinct_content_rounds_and_no_identity_reset | '<!-- /gate -->' (assert in) | structural | gate or HTML marker |
| loom-code/tests/test_review_convergence_contract.py:24 | test_contract_adds_no_review_round_ledger_or_schema | 'review-round.json' (assert in) | structural | path |
| loom-code/tests/test_review_convergence_contract.py:24 | test_contract_adds_no_review_round_ledger_or_schema | 'review_episode.json' (assert in) | structural | path |
| loom-code/tests/test_review_convergence_contract.py:24 | test_contract_adds_no_review_round_ledger_or_schema | 'rounds.json' (assert in) | structural | path |
| loom-code/tests/test_review_convergence_contract.py:69 | _recording_passage | '\n## 5. Finalize' (.index()) | structural | markdown heading |
| loom-code/tests/test_review_convergence_contract.py:70 | _recording_passage | '<!-- /gate -->' (.rindex()) | structural | gate or HTML marker |
| loom-code/tests/test_review_convergence_contract.py:183 | _round_three_bullet | '- **Round 3' (.index()) | structural | code identifier |

### loom-code/tests/test_reviewer_mechanical_evidence.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_reviewer_mechanical_evidence.py:35 | test_reviewer_spells_the_lenses_path_one_way | '`loom-code/skills/closing-review/references/lenses.md`' (assert count) | structural | path |
| loom-code/tests/test_reviewer_mechanical_evidence.py:156 | test_no_reviewer_or_lens_text_requires_suite_run_or_downgrade | '\\b(never\|not\|no)\\b' (re.search) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 35 |

### loom-code/tests/test_ship_station_text.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_ship_station_text.py:22 | test_ship_text_separates_authorization_from_acceptance | '^## 1\\. Confirm publication authorization$' (re.search) | structural | markdown heading |
| loom-code/tests/test_ship_station_text.py:48 | _gate_regions | '<!--\\s*gate:\\s*[A-Za-z0-9._-]+\\s*-->' (re.finditer) | structural | gate or HTML marker |

### loom-code/tests/test_ship_worktree_merge.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_ship_worktree_merge.py:19 | test_ship_accepted_land_renders_absolute_worktree_in_command | "cd '<absolute worktree root>' && python3 <loom-code>/scripts/loom_checker.py land" (assert in) | structural | line grammar placeholder |

### loom-code/tests/test_simplified_station_text.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_simplified_station_text.py:82 | test_ship_owns_one_self_contained_contextual_pr_body | '## Behaviour change' (assert count) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:82 | test_ship_owns_one_self_contained_contextual_pr_body | '## Context' (assert count) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:82 | test_ship_owns_one_self_contained_contextual_pr_body | '## Decisions' (assert count) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:82 | test_ship_owns_one_self_contained_contextual_pr_body | '## Follow-ups' (assert count) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:82 | test_ship_owns_one_self_contained_contextual_pr_body | '## Implementation' (assert count) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:82 | test_ship_owns_one_self_contained_contextual_pr_body | '## Intended outcome' (assert count) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:82 | test_ship_owns_one_self_contained_contextual_pr_body | '## Risks and rollback' (assert count) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:82 | test_ship_owns_one_self_contained_contextual_pr_body | '## Scope' (assert count) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:82 | test_ship_owns_one_self_contained_contextual_pr_body | '## Verification' (assert count) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:92 | test_git_memory_contributes_without_competing_top_level_schema | '## Behaviour change' (assert ==) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:92 | test_git_memory_contributes_without_competing_top_level_schema | '## Context' (assert ==) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:92 | test_git_memory_contributes_without_competing_top_level_schema | '## Decisions' (assert ==) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:92 | test_git_memory_contributes_without_competing_top_level_schema | '## Follow-ups' (assert ==) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:92 | test_git_memory_contributes_without_competing_top_level_schema | '## Implementation' (assert ==) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:92 | test_git_memory_contributes_without_competing_top_level_schema | '## Intended outcome' (assert ==) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:92 | test_git_memory_contributes_without_competing_top_level_schema | '## Risks and rollback' (assert ==) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:92 | test_git_memory_contributes_without_competing_top_level_schema | '## Scope' (assert ==) | structural | markdown heading |
| loom-code/tests/test_simplified_station_text.py:92 | test_git_memory_contributes_without_competing_top_level_schema | '## Verification' (assert ==) | structural | markdown heading |

### loom-code/tests/test_sync_before_review_text.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_sync_before_review_text.py:126 | test_no_op_sync_dispatches_without_rerun | 'sync-trunk' (assert count) | prose | 1-2 word phrase or term → `mapping-code.md` Decisions row 36 |

### loom-code/tests/test_write_plan_shape_text.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_write_plan_shape_text.py:34 | _body_words | '---\\n.*?\\n---\\n' (re.match) | structural | command |

### loom-code/tests/test_write_plan_station_text.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-code/tests/test_write_plan_station_text.py:106 | lane_hits | '(?i)\\b(small\|full)[- ]lanes?\\b\|\\blanes?\\b' (re.finditer) | prose | regex alternative '(?i)\\b(small|full)[- ]lanes?\\b' is prose → `mapping-code.md` Decisions row 37 |
| loom-code/tests/test_write_plan_station_text.py:152 | test_suggest_station_names_every_policy_input_key | '`([a-z_]+)`' (re.findall) | structural | code identifier |
| loom-code/tests/test_write_plan_station_text.py:172 | test_write_plan_names_typed_branch_and_types | '`([a-z]+)`' (re.findall) | structural | code identifier |
| loom-code/tests/test_write_plan_station_text.py:275 | test_readme_version_matches_manifest | '^{}(\\d+\\.\\d+\\.\\d+)' (re.search) | structural | line grammar placeholder |

### Decisions — loom-code

The decisions live in the mapping files. Each prose row above ends with a pointer to its Decisions row.

## loom-design

### loom-design/tests/architecture-design/test_architecture_skill.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-design/tests/architecture-design/test_architecture_skill.py:33 | test_frontmatter_declares_name_and_version | '^name: (.+)$' (re.findall) | structural | field key or label |
| loom-design/tests/architecture-design/test_architecture_skill.py:34 | test_frontmatter_declares_name_and_version | 'version: 1.0.0' (assert in) | structural | field key or label |
| loom-design/tests/architecture-design/test_architecture_skill.py:43 | test_description_within_codex_limit_and_carries_triggers | 'アーキテクチャ' (assert in) | structural | ALL_CAPS token, rule id or verdict |
| loom-design/tests/architecture-design/test_architecture_skill.py:43 | test_description_within_codex_limit_and_carries_triggers | '架構規則' (assert in) | structural | ALL_CAPS token, rule id or verdict |
| loom-design/tests/architecture-design/test_architecture_skill.py:48 | test_referenced_relative_paths_exist | '`(\\.\\./[\\w./-]+\|references/[\\w./-]+)`' (re.finditer) | structural | path |
| loom-design/tests/architecture-design/test_architecture_skill.py:54 | test_referenced_relative_paths_exist | '`architecture-design`' (assert in) | structural | names a skill, plugin or script (a hyphenated repo name) |
| loom-design/tests/architecture-design/test_architecture_skill.py:57 | test_referenced_relative_paths_exist | '[`architecture-design`](skills/architecture-design/SKILL.md)' (assert in) | structural | path |
| loom-design/tests/architecture-design/test_architecture_skill.py:58 | test_referenced_relative_paths_exist | '\\]\\((skills/[^)]+)\\)' (re.findall) | structural | path |
| loom-design/tests/architecture-design/test_architecture_skill.py:64 | test_references_schema_validator_ratify_and_commit | 'references/architecture-md-schema.md' (assert in) | structural | path |
| loom-design/tests/architecture-design/test_architecture_skill.py:65 | test_references_schema_validator_ratify_and_commit | 'scripts/architecture-design/validate_architecture_output.py' (assert in) | structural | path |
| loom-design/tests/architecture-design/test_architecture_skill.py:66 | test_references_schema_validator_ratify_and_commit | 'ratified-by:' (assert in) | structural | field key or label |
| loom-design/tests/architecture-design/test_architecture_skill.py:67 | test_references_schema_validator_ratify_and_commit | 'docs(loom): ARCHITECTURE.md ratified' (assert in) | structural | commit subject grammar |
| loom-design/tests/architecture-design/test_architecture_skill.py:73 | test_skill_reads_code_and_proposes_two_options_per_choice | '## decisions' (assert in) | structural | markdown heading |
| loom-design/tests/architecture-design/test_architecture_skill.py:73 | test_skill_reads_code_and_proposes_two_options_per_choice | 'references/design-know-how.md' (assert in) | structural | path |
| loom-design/tests/architecture-design/test_architecture_skill.py:78 | test_skill_records_package_tests_when_absent_and_commits_edited_config | '- package-tests: <command> — <reason> (<date>)' (assert in) | structural | line grammar placeholder |
| loom-design/tests/architecture-design/test_architecture_skill.py:80 | test_skill_records_package_tests_when_absent_and_commits_edited_config | 'KICKOFF-DEFAULTS.md' (assert in) | structural | path |

### loom-design/tests/interface/test_design_md_schema_keys.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-design/tests/interface/test_design_md_schema_keys.py:46 | _fenced_yaml_block | '```yaml\\n(.*?)```' (re.search) | structural | code identifier |
| loom-design/tests/interface/test_design_md_schema_keys.py:128 | _header_before_first_bullet | '\\n- `' (re.search) | structural | code identifier |
| loom-design/tests/interface/test_design_md_schema_keys.py:197 | test_typography_properties_are_all_spec_recognised | '## Layout' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:197 | test_typography_properties_are_all_spec_recognised | '## Typography' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:227 | _five_group_section | '## Overview / Brand' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:227 | _five_group_section | '## The 8 canonical sections (in order)' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:269 | test_schema_keys_documented_and_token_groups_named | '> **Grounding.**' (.index() via _section()) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 6 |
| loom-design/tests/interface/test_design_md_schema_keys.py:269 | test_schema_keys_documented_and_token_groups_named | '> **Scope' (.index() via _section()) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 6 |
| loom-design/tests/interface/test_design_md_schema_keys.py:291 | test_component_sub_tokens_are_complete_and_exclusive | '## Components' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:291 | test_component_sub_tokens_are_complete_and_exclusive | "## Do's & Don'ts" (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:342 | test_five_group_scoping_catches_blanket_paragraph_replacement | '## Overview / Brand' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:342 | test_five_group_scoping_catches_blanket_paragraph_replacement | '## The 8 canonical sections (in order)' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:358 | test_five_group_scoping_catches_all_eight_rewrite | '## Overview / Brand' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:358 | test_five_group_scoping_catches_all_eight_rewrite | '## The 8 canonical sections (in order)' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:377 | test_five_group_scoping_catches_group_rename | '`spacing` (Layout)' (assert count) | structural | code identifier |
| loom-design/tests/interface/test_design_md_schema_keys.py:393 | test_component_completeness_scoping_catches_deleted_bullet | '## Components' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:393 | test_component_completeness_scoping_catches_deleted_bullet | "## Do's & Don'ts" (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:397 | test_component_completeness_scoping_catches_deleted_bullet | 'height' (assert in) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 7 |
| loom-design/tests/interface/test_design_md_schema_keys.py:397 | test_component_completeness_scoping_catches_deleted_bullet | 'padding' (assert in) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 7 |
| loom-design/tests/interface/test_design_md_schema_keys.py:397 | test_component_completeness_scoping_catches_deleted_bullet | 'size' (assert in) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 7 |
| loom-design/tests/interface/test_design_md_schema_keys.py:397 | test_component_completeness_scoping_catches_deleted_bullet | 'width' (assert in) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 7 |
| loom-design/tests/interface/test_design_md_schema_keys.py:490 | test_elevation_section_disambiguates_non_spec_keys | '## Elevation & Depth' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:490 | test_elevation_section_disambiguates_non_spec_keys | '## Shapes' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:496 | test_elevation_section_disambiguates_non_spec_keys | 'confirm' (assert in) | prose | 1-2 word phrase or term → `mapping-design.md` Decisions row 7 |
| loom-design/tests/interface/test_design_md_schema_keys.py:496 | test_elevation_section_disambiguates_non_spec_keys | 'spec' (assert in) | prose | 1-2 word phrase or term → `mapping-design.md` Decisions row 7 |
| loom-design/tests/interface/test_design_md_schema_keys.py:512 | test_elevation_disambiguation_catches_reintroduced_spec_confirmation_header | '## Elevation & Depth' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:512 | test_elevation_disambiguation_catches_reintroduced_spec_confirmation_header | '## Shapes' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:513 | test_elevation_disambiguation_catches_reintroduced_spec_confirmation_header | '\\n- `' (re.search) | structural | code identifier |
| loom-design/tests/interface/test_design_md_schema_keys.py:538 | test_elevation_disambiguation_tolerates_meaning_preserving_reword | '## Elevation & Depth' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:538 | test_elevation_disambiguation_tolerates_meaning_preserving_reword | '## Shapes' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:578 | test_elevation_mirror_probe_survives_document_already_using_new_wording | '## Elevation & Depth' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:578 | test_elevation_mirror_probe_survives_document_already_using_new_wording | '## Shapes' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:620 | test_prose_scope_clause_removed_at_both_loci | '## Components' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:620 | test_prose_scope_clause_removed_at_both_loci | '## Shapes' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:632 | test_prose_scope_clause_catches_determiner_reword | '## Overview / Brand' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:632 | test_prose_scope_clause_catches_determiner_reword | '## The 8 canonical sections (in order)' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:741 | test_component_properties_header_not_claimed_closed | '## Components' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:741 | test_component_properties_header_not_claimed_closed | "## Do's & Don'ts" (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:746 | test_component_properties_header_not_claimed_closed | 'confirm' (assert in) | prose | 1-2 word phrase or term → `mapping-design.md` Decisions row 11 |
| loom-design/tests/interface/test_design_md_schema_keys.py:746 | test_component_properties_header_not_claimed_closed | 'spec' (assert in) | prose | 1-2 word phrase or term → `mapping-design.md` Decisions row 11 |
| loom-design/tests/interface/test_design_md_schema_keys.py:757 | test_generation_checklist_step3_names_all_token_groups | '## Anti-patterns' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:757 | test_generation_checklist_step3_names_all_token_groups | '## Generation checklist' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:758 | test_generation_checklist_step3_names_all_token_groups | '\\n3\\.\\s.*?(?=\\n\\d\\.\|\\Z)' (re.search) | structural | code identifier |
| loom-design/tests/interface/test_design_md_schema_keys.py:768 | test_shapes_documents_rounded_bullet | '## Components' (.index() via _section()) | structural | markdown heading |
| loom-design/tests/interface/test_design_md_schema_keys.py:768 | test_shapes_documents_rounded_bullet | '## Shapes' (.index() via _section()) | structural | markdown heading |

### loom-design/tests/interface/test_design_system_skill.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-design/tests/interface/test_design_system_skill.py:54 | test_frontmatter_declares_name_and_version | 'name: design-system' (assert in) | structural | field key or label |
| loom-design/tests/interface/test_design_system_skill.py:55 | test_frontmatter_declares_name_and_version | 'version: 1.0.0' (assert in) | structural | field key or label |
| loom-design/tests/interface/test_design_system_skill.py:64 | test_description_within_codex_limit_and_carries_triggers | 'デザインシステム' (assert in) | structural | ALL_CAPS token, rule id or verdict |
| loom-design/tests/interface/test_design_system_skill.py:64 | test_description_within_codex_limit_and_carries_triggers | '視覺設計系統' (assert in) | structural | ALL_CAPS token, rule id or verdict |
| loom-design/tests/interface/test_design_system_skill.py:73 | test_tool_carries_no_station_summary | '## Station summary' (assert in) | structural | markdown heading |
| loom-design/tests/interface/test_design_system_skill.py:79 | test_gate_marker_registered | '<!-- gate: design-system.never-blocks -->' (assert in) | structural | gate or HTML marker |
| loom-design/tests/interface/test_design_system_skill.py:83 | test_names_product_principles_reject_rule | 'standing.product-principles-reject' (assert in) | structural | code identifier |
| loom-design/tests/interface/test_design_system_skill.py:88 | test_token_groups_cited_from_script_not_retyped | 'design_md_spec_keys.py' (assert in) | structural | path |
| loom-design/tests/interface/test_design_system_skill.py:89 | test_token_groups_cited_from_script_not_retyped | 'TOKEN_GROUPS' (assert in) | structural | code identifier |
| loom-design/tests/interface/test_design_system_skill.py:102 | test_references_schema_and_the_interview_flow | 'references/design-md-schema.md' (assert in) | structural | path |
| loom-design/tests/interface/test_design_system_skill.py:103 | test_references_schema_and_the_interview_flow | 'references/knowledge-triage.md' (assert in) | structural | path |
| loom-design/tests/interface/test_design_system_skill.py:104 | test_references_schema_and_the_interview_flow | 'ratified-by:' (assert in) | structural | field key or label |
| loom-design/tests/interface/test_design_system_skill.py:105 | test_references_schema_and_the_interview_flow | 'docs(loom): DESIGN.md ratified' (assert in) | structural | commit subject grammar |
| loom-design/tests/interface/test_design_system_skill.py:124 | test_referenced_relative_paths_exist | '`(references/[\\w./-]+)`' (re.finditer) | structural | path |
| loom-design/tests/interface/test_design_system_skill.py:136 | test_schema_reference_still_names_eight_canonical_sections | 'Colors' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-design/tests/interface/test_design_system_skill.py:136 | test_schema_reference_still_names_eight_canonical_sections | 'Components' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-design/tests/interface/test_design_system_skill.py:136 | test_schema_reference_still_names_eight_canonical_sections | "Do's & Don'ts" (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-design/tests/interface/test_design_system_skill.py:136 | test_schema_reference_still_names_eight_canonical_sections | 'Elevation & Depth' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-design/tests/interface/test_design_system_skill.py:136 | test_schema_reference_still_names_eight_canonical_sections | 'Layout' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-design/tests/interface/test_design_system_skill.py:136 | test_schema_reference_still_names_eight_canonical_sections | 'Overview / Brand' (assert in) | structural | path |
| loom-design/tests/interface/test_design_system_skill.py:136 | test_schema_reference_still_names_eight_canonical_sections | 'Shapes' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-design/tests/interface/test_design_system_skill.py:136 | test_schema_reference_still_names_eight_canonical_sections | 'Typography' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |

### loom-design/tests/interface/test_knowledge_triage.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-design/tests/interface/test_knowledge_triage.py:53 | _fenced_block | '```\\n(.*?)\\n```' (re.finditer) | structural | code identifier |
| loom-design/tests/interface/test_knowledge_triage.py:90 | test_pin_precedes_station_doctrine | '```\\n.*?\\n```' (re.search) | structural | code identifier |
| loom-design/tests/interface/test_knowledge_triage.py:103 | test_triage_names_shaping_and_deferrable_tiers | 'shaping' (assert in) | prose | 1-2 word phrase or term → `mapping-design.md` Decisions row 27 |
| loom-design/tests/interface/test_knowledge_triage.py:104 | test_triage_names_shaping_and_deferrable_tiers | 'deferrable' (assert in) | prose | 1-2 word phrase or term → `mapping-design.md` Decisions row 27 |
| loom-design/tests/interface/test_knowledge_triage.py:114 | test_shaping_route_names_the_design_conformance_lens | 'design-conformance' (assert in) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 8 |
| loom-design/tests/interface/test_knowledge_triage.py:125 | test_deferrable_route_names_loom_design_without_cross_plugin_path | 'evidence_needed: domain-convention' (assert in) | structural | field key or label |
| loom-design/tests/interface/test_knowledge_triage.py:128 | test_deferrable_route_names_loom_design_without_cross_plugin_path | 'loom-design' (assert in) | structural | names a skill, plugin or script (a hyphenated repo name) |
| loom-design/tests/interface/test_knowledge_triage.py:128 | test_deferrable_route_names_loom_design_without_cross_plugin_path | 'write-spec' (assert in) | structural | names a skill, plugin or script (a hyphenated repo name) |
| loom-design/tests/interface/test_knowledge_triage.py:140 | test_deferrable_target_artifact_matches_station | 'DESIGN.md' (assert in) | structural | path |
| loom-design/tests/interface/test_knowledge_triage.py:148 | test_cross_severing_guard_restates_review_verdict_vocabulary | 'NEEDS_REVISION' (assert in) | structural | code identifier |
| loom-design/tests/interface/test_knowledge_triage.py:148 | test_cross_severing_guard_restates_review_verdict_vocabulary | 'PASS_WITH_NOTES' (assert in) | structural | code identifier |
| loom-design/tests/interface/test_knowledge_triage.py:158 | test_design_system_skill_mounts_its_own_reference | 'references/knowledge-triage.md' (assert in) | structural | path |
| loom-design/tests/interface/test_knowledge_triage.py:232 | test_carrier_contains_all_three_bucket_names | 'craft' (assert in) | prose | 1-2 word phrase or term → `mapping-design.md` Decisions row 33 |
| loom-design/tests/interface/test_knowledge_triage.py:232 | test_carrier_contains_all_three_bucket_names | 'domain-convention' (assert in) | prose | 1-2 word phrase or term → `mapping-design.md` Decisions row 33 |
| loom-design/tests/interface/test_knowledge_triage.py:232 | test_carrier_contains_all_three_bucket_names | 'project-local' (assert in) | prose | 1-2 word phrase or term → `mapping-design.md` Decisions row 33 |

### loom-design/tests/principles/test_principles_ratified_line.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-design/tests/principles/test_principles_ratified_line.py:49 | _station_summary_table | '## Station summary' (.index()) | structural | markdown heading |
| loom-design/tests/principles/test_principles_ratified_line.py:127 | test_gate_marker_registered | '<!-- gate: product-principles.ratified-requires-user-yes -->' (assert in) | structural | gate or HTML marker |
| loom-design/tests/principles/test_principles_ratified_line.py:145 | test_referenced_paths_exist | '`(references/[\\w./-]+)`' (re.finditer) | structural | path |
| loom-design/tests/principles/test_principles_ratified_line.py:152 | test_interview_template_path_is_referenced | 'contract/templates/PRINCIPLES-interview.md' (assert in) | structural | path |

### loom-design/tests/spec/test_capture_intent_contract.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-design/tests/spec/test_capture_intent_contract.py:93 | test_frontmatter_name_and_version | '^name: capture-intent$' (re.search) | structural | field key or label |
| loom-design/tests/spec/test_capture_intent_contract.py:94 | test_frontmatter_name_and_version | '^version: 1\\.0\\.0$' (re.search) | structural | field key or label |
| loom-design/tests/spec/test_capture_intent_contract.py:98 | test_description_within_cap | '^description: \\\|\\n((?:  .*\\n)+)' (re.search) | structural | field key or label |
| loom-design/tests/spec/test_capture_intent_contract.py:123 | _carries_station_table | '## Station summary' (return in) | structural | markdown heading |
| loom-design/tests/spec/test_capture_intent_contract.py:123 | _carries_station_table | '\| station \| artifact \| who decides \| checker \| checkpoint \|' (return in) | structural | table row or cell |
| loom-design/tests/spec/test_capture_intent_contract.py:147 | test_four_skills_link_one_locate_loom_code_reference | 'python3 <loom-code>/scripts/loom_checker.py contract --require 2.1' (assert in) | structural | line grammar placeholder |
| loom-design/tests/spec/test_capture_intent_contract.py:161 | test_gate_markers_present | '<!-- gate: {} -->' (assert in) | structural | gate or HTML marker |
| loom-design/tests/spec/test_capture_intent_contract.py:179 | test_referenced_relative_paths_exist | '`((?:references\|assets\|scripts)/[^`]+)`' (re.findall) | structural | path |
| loom-design/tests/spec/test_capture_intent_contract.py:206 | test_loom_design_version_2_2_0_consistent | '**Version**: 2.6.2' (assert in) | structural | code identifier |
| loom-design/tests/spec/test_capture_intent_contract.py:206 | test_loom_design_version_2_2_0_consistent | '\| [`loom-design`](loom-design/) \| 2.6.2 \|' (assert in) | structural | table row or cell |

### loom-design/tests/spec/test_write_spec_contract.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-design/tests/spec/test_write_spec_contract.py:147 | test_frontmatter_name_and_version | '^name: write-spec$' (re.search) | structural | field key or label |
| loom-design/tests/spec/test_write_spec_contract.py:148 | test_frontmatter_name_and_version | '^version: 1\\.0\\.0$' (re.search) | structural | field key or label |
| loom-design/tests/spec/test_write_spec_contract.py:152 | test_description_within_cap | '^description: \\\|\\n((?:  .*\\n)+)' (re.search) | structural | field key or label |
| loom-design/tests/spec/test_write_spec_contract.py:190 | test_gate_markers_present | '<!-- gate: {} -->' (assert in) | structural | gate or HTML marker |
| loom-design/tests/spec/test_write_spec_contract.py:208 | test_referenced_relative_paths_exist | '`((?:references\|assets\|scripts)/[^`]+)`' (re.findall) | structural | path |
| loom-design/tests/spec/test_write_spec_contract.py:216 | test_checker_subcommands_named_exist | 'loom_checker\\.py (\\w[\\w-]*)' (re.findall) | structural | path |
| loom-design/tests/spec/test_write_spec_contract.py:224 | test_checker_rules_named_exist | '`((?:intake\|intent\|push\|standing\|contract)\\.[a-z-]+)`' (re.findall) | structural | code identifier |

### Decisions — loom-design

The decisions live in the mapping files. Each prose row above ends with a pointer to its Decisions row.

## loom-workflow

### loom-workflow/tests/decision-map/test_decision_map_intent_binding.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py:31 | test_start_delivery_writes_an_intent_not_a_brief | 'docs/loom/intent/<change-id>.md' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py:32 | test_start_delivery_writes_an_intent_not_a_brief | 'originator: map:<map-id>' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py:33 | test_start_delivery_writes_an_intent_not_a_brief | 'map: <map-id>' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py:34 | test_start_delivery_writes_an_intent_not_a_brief | 'start_delivery.py' (assert in) | structural | path |
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py:40 | test_skill_lists_the_intent_status_values | '`closed`' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py:40 | test_skill_lists_the_intent_status_values | '`confirmed <date>`' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py:40 | test_skill_lists_the_intent_status_values | '`open`' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py:40 | test_skill_lists_the_intent_status_values | '`withdrawn' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py:41 | test_skill_lists_the_intent_status_values | 'retired — <reason>' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_decision_map_intent_binding.py:47 | test_map_lists_the_change_id_under_its_criterion | '`- delivery-intent: DA-<n> \| docs/loom/intent/<change-id>.md`' (assert in) | structural | table row or cell |

### loom-workflow/tests/decision-map/test_map_progress.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/decision-map/test_map_progress.py:98 | test_progress_resolves_ticket_brief_plan_without_writes | 'map_progress.py' (assert in) | structural | path |
| loom-workflow/tests/decision-map/test_map_progress.py:100 | test_progress_resolves_ticket_brief_plan_without_writes | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/map_progress.py" "<target>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |

### loom-workflow/tests/decision-map/test_skill_doc.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/decision-map/test_skill_doc.py:66 | _script_commands | '`([^`\\n]+)`' (re.findall) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:199 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'in codex_interface["defaultPrompt"]' (kept line) | kept-batch3 | batch-3 kept interface string: the Codex manifest defaultPrompt, not skill prose |
| loom-workflow/tests/decision-map/test_skill_doc.py:202 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'v3.0.0' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:205 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'Map clear' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/decision-map/test_skill_doc.py:206 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'schema_version: 3' (assert in) | structural | field key or label |
| loom-workflow/tests/decision-map/test_skill_doc.py:208 | test_v3_public_surface_commands_templates_and_version_are_synchronized | '`research`' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:209 | test_v3_public_surface_commands_templates_and_version_are_synchronized | '`prototype`' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:221 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'Archive' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/decision-map/test_skill_doc.py:221 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'Claim' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/decision-map/test_skill_doc.py:221 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'Close and re-chart' (assert in) | prose | phrase of 3+ words → `mapping-workflow.md` Decisions row 15 |
| loom-workflow/tests/decision-map/test_skill_doc.py:221 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'Migrate v2 to v3' (assert in) | prose | phrase of 3+ words → `mapping-workflow.md` Decisions row 15 |
| loom-workflow/tests/decision-map/test_skill_doc.py:221 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'Resume' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/decision-map/test_skill_doc.py:221 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'Start' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/decision-map/test_skill_doc.py:221 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'Update blockers' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/decision-map/test_skill_doc.py:222 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'preview_migration(map_dir)' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:223 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'apply_migration(map_dir, preview)' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:226 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/check_map_fog.py" "<map-dir>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:226 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/check_map_links.py" "<map-dir>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:226 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/map_init.py" "<map-id>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:226 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/map_progress.py" "<target>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:226 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/map_store.py" validate "<map-dir>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:226 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/start_delivery.py" "<map-dir>" "<DA-id>" "<change-id>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:227 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/check_map_fog.py" "<map-dir>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:227 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/check_map_links.py" "<map-dir>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:227 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/map_init.py" "<map-id>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:227 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/map_progress.py" "<target>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:227 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/map_store.py" validate "<map-dir>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:227 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/decision-map/scripts/start_delivery.py" "<map-dir>" "<DA-id>" "<change-id>" --repo-root "<path>"' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/decision-map/test_skill_doc.py:248 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'map_transaction.UnknownRoute' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:249 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'map_transaction.UnknownRoute' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:250 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'ticket_slug' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:250 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'ticket_type' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:251 | test_v3_public_surface_commands_templates_and_version_are_synchronized | '[a-z0-9]+(?:-[a-z0-9]+)*' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:252 | test_v3_public_surface_commands_templates_and_version_are_synchronized | 'unique `ticket_slug`' (assert in) | structural | code identifier |
| loom-workflow/tests/decision-map/test_skill_doc.py:271 | test_map_format_declares_schema_version_3_without_v1 | 'schema_version: 3' (assert in) | structural | field key or label |

### loom-workflow/tests/distill-sessions/test_prompts_parseable.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:125 | _assert_common_shape | 'Memory Item' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:129 | _assert_common_shape | 'Content' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:129 | _assert_common_shape | 'Description' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:129 | _assert_common_shape | 'Title' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:134 | _assert_common_shape | '## How the orchestrator dispatches this prompt' (assert in) | structural | markdown heading |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:161 | test_success_prompt_structure | '## Lean Solution Path' (assert in) | structural | markdown heading |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:253 | test_advisory_prompt_structure | 'Summary numbers' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:253 | test_advisory_prompt_structure | '数値サマリ' (assert in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:253 | test_advisory_prompt_structure | '數字摘要' (assert in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:259 | test_advisory_prompt_structure | '{{lang}}' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:282 | test_advisory_prompt_forbids_orchestrator_memory_reference | 'feedback_' (assert in) | structural | code identifier |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:282 | test_advisory_prompt_forbids_orchestrator_memory_reference | 'project_' (assert in) | structural | code identifier |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:307 | test_advisory_prompt_defines_skill_dir_before_first_use | 'skill.md' (assert in) | structural | path |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:330 | test_advisory_prompt_declares_skill_dir_input | '^- `skill_dir`' (re.search) | structural | code identifier |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:354 | test_skill_md_advisory_dispatch_names_skill_dir_key | '`skill_dir`' (assert in) | structural | code identifier |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:354 | test_skill_md_advisory_dispatch_names_skill_dir_key | 'dispatch_payload.input' (assert in) | structural | path |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:368 | test_host_advisory_dispatch_template_passes_skill_dir | 'dispatch_payload.input' (assert in) | structural | path |
| loom-workflow/tests/distill-sessions/test_prompts_parseable.py:368 | test_host_advisory_dispatch_template_passes_skill_dir | 'skill_dir' (assert in) | structural | code identifier |

### loom-workflow/tests/git-memory/test_loom_delegation.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/git-memory/test_loom_delegation.py:36 | test_privacy_spec_names_the_bypass_trailer | 'Privacy-Bypass-Reason:' (assert in) | structural | field key or label |
| loom-workflow/tests/git-memory/test_loom_delegation.py:42 | test_both_protocols_name_the_bypass_trailer | 'Privacy-Bypass-Reason:' (assert in) | structural | field key or label |

### loom-workflow/tests/goal-create/test_goal_lint.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/goal-create/test_goal_lint.py:224 | test_field_labels_match_the_shape_reference | '^\\d+\\.\\s+`([^`]+)`$' (re.findall) | structural | code identifier |

### loom-workflow/tests/goal-create/test_goal_shape.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/goal-create/test_goal_shape.py:69 | test_defines_four_fields_and_budget | '## The 4,000-character budget\\n\\n.*?\\n\\n(.*?)(?=\\n---\|\\Z)' (re.search) | structural | markdown heading |
| loom-workflow/tests/goal-create/test_goal_shape.py:76 | test_defines_four_fields_and_budget | 'anthropic' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 3 |
| loom-workflow/tests/goal-create/test_goal_shape.py:76 | test_defines_four_fields_and_budget | 'openai' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 3 |
| loom-workflow/tests/goal-create/test_goal_shape.py:81 | test_defines_four_fields_and_budget | 'https://code.claude.com/docs/en/goal' (collected when not in) | structural | path |
| loom-workflow/tests/goal-create/test_goal_shape.py:81 | test_defines_four_fields_and_budget | 'https://learn.chatgpt.com/docs/long-running-work' (collected when not in) | structural | path |
| loom-workflow/tests/goal-create/test_goal_shape.py:81 | test_defines_four_fields_and_budget | 'https://learn.chatgpt.com/use-cases/follow-goals' (collected when not in) | structural | path |
| loom-workflow/tests/goal-create/test_goal_shape.py:111 | test_defines_four_fields_and_budget | 'constraints' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 4 |
| loom-workflow/tests/goal-create/test_goal_shape.py:111 | test_defines_four_fields_and_budget | 'outcome' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 4 |
| loom-workflow/tests/goal-create/test_goal_shape.py:111 | test_defines_four_fields_and_budget | 'verification' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 4 |
| loom-workflow/tests/goal-create/test_goal_shape.py:115 | test_defines_four_fields_and_budget | 'anthropic' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 3 |
| loom-workflow/tests/goal-create/test_goal_shape.py:115 | test_defines_four_fields_and_budget | 'openai' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 3 |
| loom-workflow/tests/goal-create/test_goal_shape.py:144 | _section_four | '## 4 — `Stop-when`\\n\\n(.*?)(?=\\n---\|\\Z)' (re.search) | structural | markdown heading |
| loom-workflow/tests/goal-create/test_goal_shape.py:161 | _section_two | '## 2 — `Constraints`\\n\\n(.*?)(?=\\n## 3\|\\Z)' (re.search) | structural | markdown heading |
| loom-workflow/tests/goal-create/test_goal_shape.py:175 | test_constraints_section_names_derived_tag_and_outcome | '`derived`' (assert in) | structural | code identifier |
| loom-workflow/tests/goal-create/test_goal_shape.py:178 | test_constraints_section_names_derived_tag_and_outcome | '`outcome`' (assert in) | structural | code identifier |
| loom-workflow/tests/goal-create/test_goal_shape.py:187 | test_stop_when_section_points_at_input_floor | '`input-floor.md`' (assert in) | structural | path |

### loom-workflow/tests/goal-create/test_input_floor.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/goal-create/test_input_floor.py:75 | _field_names_from_shape_reference | '^## \\d+ — `([\\w-]+)`' (re.findall) | structural | markdown heading |
| loom-workflow/tests/goal-create/test_input_floor.py:115 | test_slot_mapping_uses_the_shape_reference_field_names | '## 2 — Slot-to-field mapping\\n\\n(.*?)(?=\\n## )' (re.search) | structural | markdown heading |

### loom-workflow/tests/goal-create/test_readmes.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/goal-create/test_readmes.py:61 | test_tri_language_set_exists_and_names_both_modes | 'ARC' (assert in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/goal-create/test_readmes.py:61 | test_tri_language_set_exists_and_names_both_modes | 'SESSION' (assert in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/goal-create/test_readmes.py:65 | test_tri_language_set_exists_and_names_both_modes | 'Constraints' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/goal-create/test_readmes.py:65 | test_tri_language_set_exists_and_names_both_modes | 'Outcome' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/goal-create/test_readmes.py:65 | test_tri_language_set_exists_and_names_both_modes | 'Stop-when' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/goal-create/test_readmes.py:65 | test_tri_language_set_exists_and_names_both_modes | 'Verification' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/goal-create/test_readmes.py:72 | test_tri_language_set_exists_and_names_both_modes | 'Done when' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/goal-create/test_readmes.py:72 | test_tri_language_set_exists_and_names_both_modes | 'Why' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/goal-create/test_readmes.py:77 | test_tri_language_set_exists_and_names_both_modes | 'SKILL.md' (assert in) | structural | path |
| loom-workflow/tests/goal-create/test_readmes.py:85 | test_tri_language_discovery_names_host_goal_tools | 'Codex[^.!?。]*`create_goal`' (re.search) | structural | code identifier |
| loom-workflow/tests/goal-create/test_readmes.py:86 | test_tri_language_discovery_names_host_goal_tools | 'Claude Code[^.!?。]*`ProposeGoal`[^.!?。]*`/goal`' (re.search) | structural | path |
| loom-workflow/tests/goal-create/test_readmes.py:90 | test_tri_language_discovery_names_host_goal_tools | '[`goal-create`]' (stored in) | structural | code identifier |
| loom-workflow/tests/goal-create/test_readmes.py:104 | test_invocation_documents_only_the_handoff_offer_site | '`(loom-[^`]+)`' (re.findall) | structural | code identifier |

### loom-workflow/tests/goal-create/test_skill_md.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/goal-create/test_skill_md.py:103 | test_reference_pointers_resolve | '(?:references\|scripts)/[^`\\s)\\"]+' (re.findall) | structural | path |
| loom-workflow/tests/goal-create/test_skill_md.py:130 | test_floor_invocation_line_names_the_script | '```\\n(.*?)\\n```' (re.findall) | structural | code identifier |
| loom-workflow/tests/goal-create/test_skill_md.py:135 | test_floor_invocation_line_names_the_script | 'python3 <skill-dir>/scripts/goal_lint.py' (assert in) | structural | line grammar placeholder |

### loom-workflow/tests/handoff/test_handoff_schema.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/handoff/test_handoff_schema.py:99 | test_all_ten_blocks_and_five_principles_present | '^#{2,3}\\s+.*good example' (re.search) | structural | markdown heading |
| loom-workflow/tests/handoff/test_handoff_schema.py:105 | test_all_ten_blocks_and_five_principles_present | '^#{2,3}\\s+.*bad example' (re.search) | structural | markdown heading |
| loom-workflow/tests/handoff/test_handoff_schema.py:145 | test_resume_launcher_section_has_directive_and_example_headings | 'USER DIRECTIVE' (assert in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/handoff/test_handoff_schema.py:175 | test_conversation_language_captured_in_frontmatter | 'conversation_language' (assert in) | structural | code identifier |

### loom-workflow/tests/handoff/test_handoff_skill_md.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/handoff/test_handoff_skill_md.py:153 | test_frontmatter_and_routing | 'references/handoff-schema.md' (assert in) | structural | path |
| loom-workflow/tests/handoff/test_handoff_skill_md.py:164 | test_frontmatter_and_routing | '## Prepare mode' (assert in) | structural | markdown heading |
| loom-workflow/tests/handoff/test_handoff_skill_md.py:165 | test_frontmatter_and_routing | '## Resume mode' (assert in) | structural | markdown heading |
| loom-workflow/tests/handoff/test_handoff_skill_md.py:168 | test_frontmatter_and_routing | '.claude/handoffs/' (assert in) | structural | path |

### loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py:75 | test_all_three_language_readmes_exist_and_agree | 'comprehensive\|exhaustive\|complete coverage\|網羅的\|完全な網羅\|完整涵蓋\|全面涵蓋' (re.search) | prose | regex alternative 'comprehensive' is prose → `mapping-workflow.md` Decisions row 17 |

### loom-workflow/tests/loom-memory/test_skill_contract.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/loom-memory/test_skill_contract.py:89 | _section | '^#{1,{}}\\s+\\S' (re.search) | structural | markdown heading |
| loom-workflow/tests/loom-memory/test_skill_contract.py:103 | test_four_operations_contract | 'Trigger' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-memory/test_skill_contract.py:104 | test_four_operations_contract | 'Steps' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-memory/test_skill_contract.py:105 | test_four_operations_contract | '^\\d+\\.\\s' (re.search) | structural | code identifier |
| loom-workflow/tests/loom-memory/test_skill_contract.py:175 | test_no_bare_repo_root_relative_script_path | '${CLAUDE_PLUGIN_ROOT}' (assert in) | structural | line grammar placeholder |
| loom-workflow/tests/loom-memory/test_skill_contract.py:249 | test_references_exist_and_are_referenced | 'references/okf-profile.md' (assert in) | structural | path |
| loom-workflow/tests/loom-memory/test_skill_contract.py:250 | test_references_exist_and_are_referenced | 'references/operations.md' (assert in) | structural | path |
| loom-workflow/tests/loom-memory/test_skill_contract.py:310 | test_record_section_matches_the_digest_the_cold_reader_eval_was_run_against | '945a9cb29dfb5a9090e4ad036e5f980accf19fe94b22ff3014c1c066635ddcc9' (assert ==) | structural | code identifier |

### loom-workflow/tests/loom-visualization/test_references.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/loom-visualization/test_references.py:38 | numbered | '^\\d+\\. (.+)$' (re.findall) | structural | code identifier |
| loom-workflow/tests/loom-visualization/test_references.py:45 | rule_titles | '^### (\\d+)\\. [^\\n]+\\n(.*?)(?=^### \|\\Z)' (re.finditer) | structural | markdown heading |
| loom-workflow/tests/loom-visualization/test_references.py:51 | header_row | '^\\\|(.+)\\\|\\s*$\\n^\\\|[\\s:\|-]+\\\|\\s*$' (re.search) | structural | table row or cell |
| loom-workflow/tests/loom-visualization/test_references.py:73 | table_errors | 'Acceptance checklist' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:73 | table_errors | 'Before and after' (if requires) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 10 |
| loom-workflow/tests/loom-visualization/test_references.py:73 | table_errors | 'Confirmed, unconfirmed, to decide' (if requires) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 10 |
| loom-workflow/tests/loom-visualization/test_references.py:73 | table_errors | 'Decision consequences' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:73 | table_errors | 'Findings and recommendations' (if requires) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 10 |
| loom-workflow/tests/loom-visualization/test_references.py:73 | table_errors | 'Progress report' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:73 | table_errors | 'Risks' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:73 | table_errors | 'Support matrix' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:92 | test_guide_has_seven_rules_and_rewrite_steps | 'Scope' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:93 | test_guide_has_seven_rules_and_rewrite_steps | 'Internal terms' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:103 | all_header_rows | '^\\\|(.+)\\\|\\s*$\\n^\\\|[\\s:\|-]+\\\|\\s*$' (re.finditer) | structural | table row or cell |
| loom-workflow/tests/loom-visualization/test_references.py:112 | rule5_example_errors | '^\\\| [^\|\\n]*\\(recommended\\) \\\|' (re.search) | structural | table row or cell |
| loom-workflow/tests/loom-visualization/test_references.py:143 | table_rule_one_errors | 'key-value' (if requires) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 24 |
| loom-workflow/tests/loom-visualization/test_references.py:187 | test_eight_conversation_situations_present | 'templates/01-option-comparison.md' (assert in) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:219 | in_cell_errors | '<meter>' (if requires) | structural | line grammar placeholder |
| loom-workflow/tests/loom-visualization/test_references.py:219 | in_cell_errors | '<progress>' (if requires) | structural | line grammar placeholder |
| loom-workflow/tests/loom-visualization/test_references.py:219 | in_cell_errors | '<svg>' (if requires) | structural | line grammar placeholder |
| loom-workflow/tests/loom-visualization/test_references.py:219 | in_cell_errors | 'GitHub' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:219 | in_cell_errors | 'Status symbols' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:219 | in_cell_errors | 'Tufte' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:219 | in_cell_errors | 'WCAG 1.4.1' (if requires) | structural | code identifier |
| loom-workflow/tests/loom-visualization/test_references.py:219 | in_cell_errors | 'WHATWG' (if requires) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/loom-visualization/test_references.py:219 | in_cell_errors | 'heatmap' (if requires) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 11 |
| loom-workflow/tests/loom-visualization/test_references.py:219 | in_cell_errors | 'rule 6' (if requires) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 11 |
| loom-workflow/tests/loom-visualization/test_references.py:219 | in_cell_errors | 'shields.io' (if requires) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:225 | in_cell_errors | 'B22' (collected when not in) | structural | code identifier |
| loom-workflow/tests/loom-visualization/test_references.py:225 | in_cell_errors | 'templates/10-timeline.md' (collected when not in) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:262 | table_criteria_errors | 'Datawrapper' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:262 | table_criteria_errors | 'Google' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:262 | table_criteria_errors | 'W3C WAI' (if requires) | structural | code identifier |
| loom-workflow/tests/loom-visualization/test_references.py:264 | table_criteria_errors | 'https://developers.google.com/style/tables' (if requires) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:264 | table_criteria_errors | 'https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables' (if requires) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:264 | table_criteria_errors | 'https://www.w3.org/WAI/tutorials/images/complex/' (if requires) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:319 | entries | '^### ([SDB])(\\d+)\\. (.+)$' (re.finditer) | structural | markdown heading |
| loom-workflow/tests/loom-visualization/test_references.py:331 | domain_errors | '^Load this when: .+$' (re.search) | prose | phrase of 3+ words → `mapping-workflow.md` Decisions row 28 |
| loom-workflow/tests/loom-visualization/test_references.py:334 | domain_errors | '^Load this when: (.+)$' (re.search) | prose | phrase of 3+ words → `mapping-workflow.md` Decisions row 28 |
| loom-workflow/tests/loom-visualization/test_references.py:337 | domain_errors | '^### ([SDB])(\\d+)\\. (.+)$' (re.findall) | structural | markdown heading |
| loom-workflow/tests/loom-visualization/test_references.py:345 | domain_errors | '^Pointer: (.+)$' (re.search) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:345 | domain_errors | 'https://' (if requires) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:353 | domain_errors | '^Pointer: (.+)$' (re.search) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:356 | domain_errors | 'references/plain-language.md' (if requires) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:357 | domain_errors | 'Acceptance checklist' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:357 | domain_errors | 'Before and after' (if requires) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 13 |
| loom-workflow/tests/loom-visualization/test_references.py:357 | domain_errors | 'Confirmed, unconfirmed, to decide' (if requires) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 13 |
| loom-workflow/tests/loom-visualization/test_references.py:357 | domain_errors | 'Decision consequences' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:357 | domain_errors | 'Progress report' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:357 | domain_errors | 'Support matrix' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:368 | risk_register_placement | '^Pointer: (.+)$' (re.search) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_references.py:375 | routing_errors | '^\\\| (.+?) \\\| `(references/[\\w.-]+)` \\\|$' (re.findall) | structural | table row or cell |
| loom-workflow/tests/loom-visualization/test_references.py:378 | routing_errors | 'references/{}.md' (if requires) | structural | line grammar placeholder |
| loom-workflow/tests/loom-visualization/test_references.py:383 | routing_errors | 'RACI' (if requires) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/loom-visualization/test_references.py:383 | routing_errors | 'RICE' (if requires) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/loom-visualization/test_references.py:383 | routing_errors | 'SWOT' (if requires) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/loom-visualization/test_references.py:383 | routing_errors | 'design tokens' (if requires) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 14 |
| loom-workflow/tests/loom-visualization/test_references.py:383 | routing_errors | 'go/no-go' (if requires) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:383 | routing_errors | 'heuristic evaluation' (if requires) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 14 |
| loom-workflow/tests/loom-visualization/test_references.py:383 | routing_errors | 'incident postmortem' (if requires) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 14 |
| loom-workflow/tests/loom-visualization/test_references.py:383 | routing_errors | 'journey map' (if requires) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 14 |
| loom-workflow/tests/loom-visualization/test_references.py:383 | routing_errors | 'roadmap' (if requires) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 14 |
| loom-workflow/tests/loom-visualization/test_references.py:383 | routing_errors | 'runbook' (if requires) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 14 |
| loom-workflow/tests/loom-visualization/test_references.py:383 | routing_errors | 'test plan' (if requires) | prose | 1-2 word phrase or term → `mapping-containers.md` Decisions row 14 |
| loom-workflow/tests/loom-visualization/test_references.py:388 | routing_errors | 'progress' (if requires) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 29 |
| loom-workflow/tests/loom-visualization/test_references.py:422 | _has_term | '(?<!\\w){}(?!\\w)' (re.search) | structural | line grammar placeholder |
| loom-workflow/tests/loom-visualization/test_references.py:428 | held_type_routing_errors | '^\\\| (.+?) \\\| `(references/[\\w.-]+)` \\\|$' (re.findall) | structural | table row or cell |
| loom-workflow/tests/loom-visualization/test_references.py:433 | held_type_routing_errors | '^### ([SDB])(\\d+)\\. (.+)$' (re.finditer) | structural | markdown heading |
| loom-workflow/tests/loom-visualization/test_references.py:439 | held_type_routing_errors | '^Load this when: (.+)$' (re.search) | prose | phrase of 3+ words → `mapping-workflow.md` Decisions row 28 |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | '<br/>━━━━━━<br/>' (collected when not in) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | "<div style='text-align:left'>" (collected when not in) | structural | code identifier |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | 'bullet lines' (collected when not in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 31 |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | 'container rule' (collected when not in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 31 |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | 'edge labels' (collected when not in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 31 |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | 'flow steps' (collected when not in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 31 |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | 'left alignment' (collected when not in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 31 |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | 'references/mermaid-cot-spec.md' (collected when not in) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | 'separator row' (collected when not in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 31 |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | 'sequence participants' (collected when not in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 31 |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | 'title line' (collected when not in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 31 |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | 'width budget' (collected when not in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 31 |
| loom-workflow/tests/loom-visualization/test_references.py:536 | test_node_structure_reference_strips_required_phrases | 'wrapped prose' (collected when not in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 31 |
| loom-workflow/tests/loom-visualization/test_references.py:548 | test_node_structure_reference_points_at_skill_md | 'SKILL.md' (assert in) | structural | path |
| loom-workflow/tests/loom-visualization/test_references.py:554 | test_skill_md_points_to_node_structure_reference | 'references/node-structure.md' (assert in) | structural | path |

### loom-workflow/tests/loom-visualization/test_skill_script_paths.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/loom-visualization/test_skill_script_paths.py:30 | test_each_skill_calls_a_script_through_skill_dir | '<skill-dir>/scripts/([\\w.-]+)' (re.search) | structural | line grammar placeholder |
| loom-workflow/tests/loom-visualization/test_skill_script_paths.py:51 | test_every_skill_dir_script_reference_exists | '<skill-dir>/scripts/([\\w.-]+)' (re.findall) | structural | line grammar placeholder |

### loom-workflow/tests/loom-visualization/test_templates.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/loom-visualization/test_templates.py:57 | fences | '^```([\\w-]*)[^\\n]*\\n(.*?)^```\\s*$' (re.finditer) | structural | code identifier |
| loom-workflow/tests/loom-visualization/test_templates.py:67 | validate_template | 'ASCII' (if requires) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/loom-visualization/test_templates.py:67 | validate_template | 'Common mistakes' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_templates.py:67 | validate_template | 'Mermaid' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_templates.py:67 | validate_template | 'Table' (if requires) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/loom-visualization/test_templates.py:67 | validate_template | 'When to use' (if requires) | prose | phrase of 3+ words → `mapping-workflow.md` Decisions row 34 |
| loom-workflow/tests/loom-visualization/test_templates.py:100 | generator_examples | 'scripts/generate\\.py (\\w+)' (re.findall) | structural | path |
| loom-workflow/tests/loom-visualization/test_templates.py:119 | test_eleven_shapes_each_have_table_ascii_mermaid | '^\\\|.*\\\|\\s*$\\n^\\\|[\\s:\|-]+\\\|\\s*$' (re.search) | structural | table row or cell |
| loom-workflow/tests/loom-visualization/test_templates.py:121 | test_eleven_shapes_each_have_table_ascii_mermaid | 'erDiagram' (assert .startswith()) | structural | Mermaid diagram keyword |
| loom-workflow/tests/loom-visualization/test_templates.py:121 | test_eleven_shapes_each_have_table_ascii_mermaid | 'flowchart' (assert .startswith()) | structural | Mermaid diagram keyword |
| loom-workflow/tests/loom-visualization/test_templates.py:121 | test_eleven_shapes_each_have_table_ascii_mermaid | 'flowchart LR' (assert .startswith()) | structural | Mermaid diagram keyword |
| loom-workflow/tests/loom-visualization/test_templates.py:121 | test_eleven_shapes_each_have_table_ascii_mermaid | 'flowchart TD' (assert .startswith()) | structural | Mermaid diagram keyword |
| loom-workflow/tests/loom-visualization/test_templates.py:121 | test_eleven_shapes_each_have_table_ascii_mermaid | 'mindmap' (assert .startswith()) | structural | Mermaid diagram keyword |
| loom-workflow/tests/loom-visualization/test_templates.py:121 | test_eleven_shapes_each_have_table_ascii_mermaid | 'quadrantChart' (assert .startswith()) | structural | Mermaid diagram keyword |
| loom-workflow/tests/loom-visualization/test_templates.py:121 | test_eleven_shapes_each_have_table_ascii_mermaid | 'sequenceDiagram' (assert .startswith()) | structural | Mermaid diagram keyword |
| loom-workflow/tests/loom-visualization/test_templates.py:121 | test_eleven_shapes_each_have_table_ascii_mermaid | 'stateDiagram-v2' (assert .startswith()) | structural | Mermaid diagram keyword |
| loom-workflow/tests/loom-visualization/test_templates.py:121 | test_eleven_shapes_each_have_table_ascii_mermaid | 'timeline' (assert .startswith()) | structural | Mermaid diagram keyword |
| loom-workflow/tests/loom-visualization/test_templates.py:121 | test_eleven_shapes_each_have_table_ascii_mermaid | 'xychart-beta' (assert .startswith()) | structural | Mermaid diagram keyword |
| loom-workflow/tests/loom-visualization/test_templates.py:161 | test_generator_examples_reproduce_their_output | 'arch' (assert ==) | structural | generator name (a gen_<name> script on disk) |
| loom-workflow/tests/loom-visualization/test_templates.py:161 | test_generator_examples_reproduce_their_output | 'bar' (assert ==) | structural | generator name (a gen_<name> script on disk) |
| loom-workflow/tests/loom-visualization/test_templates.py:161 | test_generator_examples_reproduce_their_output | 'flow' (assert ==) | structural | generator name (a gen_<name> script on disk) |
| loom-workflow/tests/loom-visualization/test_templates.py:161 | test_generator_examples_reproduce_their_output | 'seq' (assert ==) | structural | generator name (a gen_<name> script on disk) |
| loom-workflow/tests/loom-visualization/test_templates.py:161 | test_generator_examples_reproduce_their_output | 'table' (assert ==) | structural | generator name (a gen_<name> script on disk) |
| loom-workflow/tests/loom-visualization/test_templates.py:161 | test_generator_examples_reproduce_their_output | 'tree' (assert ==) | structural | generator name (a gen_<name> script on disk) |
| loom-workflow/tests/loom-visualization/test_templates.py:181 | test_skill_declines_vault_target | 'scripts/detect_client.py --target' (assert in) | structural | command |
| loom-workflow/tests/loom-visualization/test_templates.py:182 | test_skill_declines_vault_target | 'obsidian:obsidian-mermaid-visualizer' (assert in) | structural | code identifier |
| loom-workflow/tests/loom-visualization/test_templates.py:235 | test_mermaid_gate_paragraph_present_requires_confirmed_host | '<!--\\s*gate:\\s*{}\\s*-->(.*?)<!--\\s*/gate\\s*-->' (re.search) | structural | gate or HTML marker |
| loom-workflow/tests/loom-visualization/test_templates.py:242 | test_mermaid_gate_paragraph_present_requires_confirmed_host | 'assert any(pinned_sentence_ok(s, verb, literals) for s in sentences), (' (kept line) | kept-batch3 | batch-3 kept gate polarity check (MERMAID_PIN, TABLE_ASCII_PIN, CHAT_PROCEEDS_PIN): reads only sentences in the mermaid-only-when-confirmed and obsidian-boundary gate blocks and fails a negated sentence; the literals pass through a parameter |
| loom-workflow/tests/loom-visualization/test_templates.py:266 | test_obsidian_gate_paragraph_chat_in_vault_cwd_proceeds | '<!--\\s*gate:\\s*{}\\s*-->(.*?)<!--\\s*/gate\\s*-->' (re.search) | structural | gate or HTML marker |
| loom-workflow/tests/loom-visualization/test_templates.py:272 | test_obsidian_gate_paragraph_chat_in_vault_cwd_proceeds | '--target' (assert in) | structural | command |
| loom-workflow/tests/loom-visualization/test_templates.py:273 | test_obsidian_gate_paragraph_chat_in_vault_cwd_proceeds | 'assert any(pinned_sentence_ok(s, *CHAT_PROCEEDS_PIN) for s in gate_sentences(block)), (' (kept line) | kept-batch3 | batch-3 kept gate polarity check (MERMAID_PIN, TABLE_ASCII_PIN, CHAT_PROCEEDS_PIN): reads only sentences in the mermaid-only-when-confirmed and obsidian-boundary gate blocks and fails a negated sentence; the literals pass through a parameter |
| loom-workflow/tests/loom-visualization/test_templates.py:299 | test_shaped_content_defaults_to_a_markdown_table | 'Form in a chat reply' (assert in) | prose | phrase of 3+ words → `mapping-workflow.md` Decisions row 36 |
| loom-workflow/tests/loom-visualization/test_templates.py:300 | test_shaped_content_defaults_to_a_markdown_table | 'Form in a chat reply' (.index()) | prose | phrase of 3+ words → `mapping-workflow.md` Decisions row 36 |
| loom-workflow/tests/loom-visualization/test_templates.py:303 | test_shaped_content_defaults_to_a_markdown_table | 'markdown table' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 37 |
| loom-workflow/tests/loom-visualization/test_templates.py:320 | test_remote_viewer_no_longer_forces_ascii | '(?:remote[ _]viewer\|terminal client\|because of the client)[^.]*\\bASCII\\b\|\\bstay ASCII\\b' (re.search) | prose | regex alternative '(?:remote[ _]viewer|terminal client|because of the client)[^.]*\\bASCII\\b' is prose → `mapping-workflow.md` Decisions row 38 |
| loom-workflow/tests/loom-visualization/test_templates.py:331 | test_w2_02_templates_adopt_node_structure | 'body' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 39 |
| loom-workflow/tests/loom-visualization/test_templates.py:331 | test_w2_02_templates_adopt_node_structure | 'title' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 39 |
| loom-workflow/tests/loom-visualization/test_templates.py:354 | test_w2_02_templates_adopt_node_structure | 'body' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 39 |
| loom-workflow/tests/loom-visualization/test_templates.py:354 | test_w2_02_templates_adopt_node_structure | 'title' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow.md` Decisions row 39 |

### loom-workflow/tests/recap-state/test_seven_block_schema.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/recap-state/test_seven_block_schema.py:137 | test_l3_contract_defines_goal_grounded_natural_output | '## L3 user-visible template' (.index()) | structural | markdown heading |
| loom-workflow/tests/recap-state/test_seven_block_schema.py:150 | test_l3_contract_defines_goal_grounded_natural_output | '### Align purpose and next step' (collected when not in) | structural | markdown heading |
| loom-workflow/tests/recap-state/test_seven_block_schema.py:150 | test_l3_contract_defines_goal_grounded_natural_output | '### Essential background' (collected when not in) | structural | markdown heading |
| loom-workflow/tests/recap-state/test_seven_block_schema.py:150 | test_l3_contract_defines_goal_grounded_natural_output | '### Gap and current assessment' (collected when not in) | structural | markdown heading |
| loom-workflow/tests/recap-state/test_seven_block_schema.py:150 | test_l3_contract_defines_goal_grounded_natural_output | '### Pending work' (collected when not in) | structural | markdown heading |
| loom-workflow/tests/recap-state/test_seven_block_schema.py:150 | test_l3_contract_defines_goal_grounded_natural_output | '### Purpose and current position' (collected when not in) | structural | markdown heading |
| loom-workflow/tests/recap-state/test_seven_block_schema.py:150 | test_l3_contract_defines_goal_grounded_natural_output | '### Why confirmation is needed now' (collected when not in) | structural | markdown heading |
| loom-workflow/tests/recap-state/test_seven_block_schema.py:157 | test_l3_contract_defines_goal_grounded_natural_output | '`loom-workflow:recap-state`' (assert in) | structural | code identifier |
| loom-workflow/tests/recap-state/test_seven_block_schema.py:158 | test_l3_contract_defines_goal_grounded_natural_output | 'loom-workflow/skills/recap-state/scripts/' (assert in) | structural | path |

### loom-workflow/tests/recap-state/test_skill_md.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/recap-state/test_skill_md.py:135 | test_frontmatter_and_routing | 'references/seven-block-schema.md' (assert in) | structural | path |

### loom-workflow/tests/scripts/test_critique_compaction.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_critique_compaction.py:18 | test_mode_routing_is_declared_before_either_lens | 'mode: proposal' (assert in) | structural | field key or label |
| loom-workflow/tests/scripts/test_critique_compaction.py:19 | test_mode_routing_is_declared_before_either_lens | 'mode: complexity' (assert in) | structural | field key or label |
| loom-workflow/tests/scripts/test_critique_compaction.py:21 | test_mode_routing_is_declared_before_either_lens | '## Choosing the mode' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_critique_compaction.py:21 | test_mode_routing_is_declared_before_either_lens | '## Mode: complexity' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_critique_compaction.py:21 | test_mode_routing_is_declared_before_either_lens | '## Mode: proposal' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_critique_compaction.py:21 | test_mode_routing_is_declared_before_either_lens | '## Shared discipline' (.index()) | structural | markdown heading |

### loom-workflow/tests/scripts/test_dbt_model_style_compaction.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:35 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'checklists/dbt-model-self-check.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:35 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'references/dotstar-passthrough.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:35 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'scripts/validate_header.py' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:37 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'Consumer layers' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:37 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'LISTAGG' (collected when not in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:37 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'UNION ALL' (collected when not in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:37 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'UPPERCASE' (collected when not in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:37 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'USING (key)' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:37 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'YAML frontmatter' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:37 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'not `materialization`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:37 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'python <skill-dir>/scripts/validate_header.py --manifest target/manifest.json models/' (collected when not in) | structural | line grammar placeholder |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:37 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'python <skill-dir>/scripts/validate_header.py models/' (collected when not in) | structural | line grammar placeholder |
| loom-workflow/tests/scripts/test_dbt_model_style_compaction.py:37 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | "target.type=='redshift'" (collected when not in) | structural | path |

### loom-workflow/tests/scripts/test_distill_sessions_compaction.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_distill_sessions_compaction.py:19 | test_entrypoint_preserves_essence | '--approved' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_distill_sessions_compaction.py:19 | test_entrypoint_preserves_essence | 'merged.json' (collected when not in) | structural | path |
| loom-workflow/tests/scripts/test_distill_sessions_compaction.py:19 | test_entrypoint_preserves_essence | 'references/runtime-protocol.md' (collected when not in) | structural | path |
| loom-workflow/tests/scripts/test_distill_sessions_compaction.py:19 | test_entrypoint_preserves_essence | 'top.json' (collected when not in) | structural | path |

### loom-workflow/tests/scripts/test_git_memory_compaction.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_git_memory_compaction.py:33 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'protocols/compose-commit.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:33 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'protocols/compose-pr.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:33 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'protocols/recall.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:33 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'standards/memory-conventions.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:35 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'BLOCKED' (collected when not in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:35 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | '`git log --grep`' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:35 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'memory-grep.sh --verify <ref>' (collected when not in) | structural | line grammar placeholder |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:39 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | '--history' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:39 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | '--match' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:39 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | '--path' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:39 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | '--top' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:39 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'Decision:' (collected when not in) | structural | field key or label |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:39 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'Gotcha:' (collected when not in) | structural | field key or label |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:39 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'Learning:' (collected when not in) | structural | field key or label |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:39 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'Privacy-Bypass-Reason:' (collected when not in) | structural | field key or label |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:39 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'Supersedes:' (collected when not in) | structural | field key or label |
| loom-workflow/tests/scripts/test_git_memory_compaction.py:39 | test_entrypoint_pointers_resolve_and_structural_tokens_stay | 'gh pr create' (collected when not in) | structural | command |

### loom-workflow/tests/scripts/test_handoff_compaction.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'Confidence flags' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'Prepare mode' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'Recent decisions' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'Resume Launcher' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'Resume mode' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'Synthesis-check' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'USER DIRECTIVE:' (collected when not in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'Verification commands' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | '[T1]' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | '[T2]' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'claude --version' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'conversation_language' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'git log --oneline -5' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'git rev-parse --abbrev-ref HEAD' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'git rev-parse HEAD' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'git status --short' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'ls -t .claude/handoffs/ \| head -1' (collected when not in) | structural | table row or cell |
| loom-workflow/tests/scripts/test_handoff_compaction.py:37 | test_entrypoint_structure_and_schema_before_artifact_steps | 'recap-state' (collected when not in) | structural | names a skill, plugin or script (a hyphenated repo name) |
| loom-workflow/tests/scripts/test_handoff_compaction.py:40 | test_entrypoint_structure_and_schema_before_artifact_steps | '## Prepare mode' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_handoff_compaction.py:41 | test_entrypoint_structure_and_schema_before_artifact_steps | 'references/handoff-schema.md' (.index()) | structural | path |
| loom-workflow/tests/scripts/test_handoff_compaction.py:42 | test_entrypoint_structure_and_schema_before_artifact_steps | '2. Write' (.index()) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_handoff_compaction.py:45 | test_entrypoint_structure_and_schema_before_artifact_steps | '## Resume mode' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_handoff_compaction.py:46 | test_entrypoint_structure_and_schema_before_artifact_steps | 'references/handoff-schema.md' (.index()) | structural | path |
| loom-workflow/tests/scripts/test_handoff_compaction.py:47 | test_entrypoint_structure_and_schema_before_artifact_steps | '2. Read' (.index()) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_handoff_compaction.py:58 | test_prepare_mode_names_goal_create | '## Prepare mode' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_handoff_compaction.py:59 | test_prepare_mode_names_goal_create | '## Resume mode' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_handoff_compaction.py:62 | test_prepare_mode_names_goal_create | 'loom-workflow:goal-create' (assert in) | structural | code identifier |

### loom-workflow/tests/scripts/test_independent_advisor_compaction.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:73 | test_entrypoint_points_to_references_that_resolve | 'references/dispatch-protocol.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:73 | test_entrypoint_points_to_references_that_resolve | 'references/executor-detection.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:73 | test_entrypoint_points_to_references_that_resolve | 'references/report-contract.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`actual_cost`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`audit`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`blind judge`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`corroborated_by`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`coverage_disclaimer`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`degraded_legs`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`early_stopped`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`explore`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`known_weaknesses`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`leg_count`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`mode_basis`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`mode_override`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`normalizer`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`proposer`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`scope_boundary`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`verified_effort`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | '`verified_model`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | 'name: independent-advisor' (collected when not in) | structural | field key or label |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:82 | test_entrypoint_and_references_keep_structural_tokens | 'version: 0.1.0' (collected when not in) | structural | field key or label |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | '--sandbox read-only' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | '--skip-git-repo-check' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | '< /dev/null' (collected when not in) | structural | path |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | '`empty-output`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | '`missing-field`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | '`no-reasoning-trace`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | '`normalized_by_is_incumbent_author`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | '`refusal`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | '`restates-input`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | '`unbacked-claim`' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | 'codex exec' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | 'coverage_disclaimer' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | 'degraded_legs' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | 'divergence_points' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | 'known_weaknesses' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | 'model_reasoning_effort=' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | "sh -c 'command -v claude'" (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_independent_advisor_compaction.py:86 | test_entrypoint_and_references_keep_structural_tokens | "sh -c 'command -v codex'" (collected when not in) | structural | command |

### loom-workflow/tests/scripts/test_independent_advisor_plugin_readmes.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_independent_advisor_plugin_readmes.py:40 | test_skill_is_listed_in_every_readme | '^\\\|\\s*\\[`{}`\\]\\(skills/{}/\\)\\s*\\\|' (re.search) | structural | table row or cell |

### loom-workflow/tests/scripts/test_loom_visualization_compaction.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:59 | test_entrypoint_has_required_sections_and_routes | '---\nname: loom-visualization\n' (assert .startswith()) | structural | command |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:69 | test_entrypoint_has_required_sections_and_routes | '## Boundary' (assert in) | structural | markdown heading |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:69 | test_entrypoint_has_required_sections_and_routes | '## Failure modes to refuse' (assert in) | structural | markdown heading |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:69 | test_entrypoint_has_required_sections_and_routes | '## Page mode' (assert in) | structural | markdown heading |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:69 | test_entrypoint_has_required_sections_and_routes | '## Step 1' (assert in) | structural | markdown heading |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:69 | test_entrypoint_has_required_sections_and_routes | '## Step 2' (assert in) | structural | markdown heading |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:69 | test_entrypoint_has_required_sections_and_routes | '## Step 3' (assert in) | structural | markdown heading |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:69 | test_entrypoint_has_required_sections_and_routes | '## Step 4' (assert in) | structural | markdown heading |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:72 | test_entrypoint_has_required_sections_and_routes | 'assets/cot-report-template.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:72 | test_entrypoint_has_required_sections_and_routes | 'references/client-matrix.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:72 | test_entrypoint_has_required_sections_and_routes | 'references/fidelity-check.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:72 | test_entrypoint_has_required_sections_and_routes | 'references/page-mode.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:72 | test_entrypoint_has_required_sections_and_routes | 'references/plain-language.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:72 | test_entrypoint_has_required_sections_and_routes | 'scripts/align.py' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:72 | test_entrypoint_has_required_sections_and_routes | 'scripts/detect_client.py' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:72 | test_entrypoint_has_required_sections_and_routes | 'scripts/generate.py' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:74 | test_entrypoint_has_required_sections_and_routes | 'obsidian:obsidian-mermaid-visualizer' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:74 | test_entrypoint_has_required_sections_and_routes | 'scripts/detect_client.py --target' (collected when not in) | structural | command |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | '${TMPDIR:-/tmp}/loom-visualization/' (collected when not in) | structural | path |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | '<name>.fidelity.md' (collected when not in) | structural | line grammar placeholder |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | 'Assumptions' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | 'Co-premises' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | 'Conversation mode' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | 'File mode' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | 'Open questions' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | 'Rejected options' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | 'r1 -->\|' (collected when not in) | structural | gate or HTML marker |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | 'reviewed_md_sha256:' (collected when not in) | structural | field key or label |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | 'think-orbit:break-assumption' (collected when not in) | structural | code identifier |
| loom-workflow/tests/scripts/test_loom_visualization_compaction.py:90 | test_page_mode_keeps_structural_tokens_and_render_verify_commands | 'think-orbit:thinking-session' (collected when not in) | structural | code identifier |

### loom-workflow/tests/scripts/test_no_retired_loom_code_skill_names.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_no_retired_loom_code_skill_names.py:51 | find_retired_names | 'loom-code:([a-z][a-z0-9-]*)' (re.finditer) | structural | code identifier |

### loom-workflow/tests/scripts/test_readme_card_timing.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_readme_card_timing.py:68 | test_current_descriptions_use_the_cards_own_name | 'visualization card' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow-2.md` Decisions row 18 |
| loom-workflow/tests/scripts/test_readme_card_timing.py:75 | test_current_descriptions_use_the_cards_own_name | 'visualization card' (assert in) | prose | 1-2 word phrase or term → `mapping-workflow-2.md` Decisions row 18 |
| loom-workflow/tests/scripts/test_readme_card_timing.py:89 | test_readmes_name_the_userpromptsubmit_hook | 'UserPromptSubmit' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |

### loom-workflow/tests/scripts/test_recap_state_compaction.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_recap_state_compaction.py:21 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | 'ASCII' (collected when not in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:21 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | 'HANDOFF' (collected when not in) | structural | ALL_CAPS token, rule id or verdict |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:21 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | 'Synthesis-check' (collected when not in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:24 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | '## What to do' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:25 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | 'references/seven-block-schema.md' (.index()) | structural | path |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:26 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | '### Purpose and current position' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:27 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | '3. Apply' (.index()) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:37 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | '### Align purpose and next step' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:37 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | '### Essential background' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:37 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | '### Gap and current assessment' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:37 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | '### Pending work' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:37 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | '### Purpose and current position' (.index()) | structural | markdown heading |
| loom-workflow/tests/scripts/test_recap_state_compaction.py:37 | test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template | '### Why confirmation is needed now' (.index()) | structural | markdown heading |

### loom-workflow/tests/scripts/test_visualization_card_hook.py

| file:line | function | literal / form | class | reason |
|---|---|---|---|---|
| loom-workflow/tests/scripts/test_visualization_card_hook.py:157 | test_hook_is_executable_python3_script | '#!/usr/bin/env python3' (assert ==) | structural | markdown heading |
| loom-workflow/tests/scripts/test_visualization_card_hook.py:296 | rule_polarity_errors | 'no metaphors, analogies, "like" or "imagine"' (if requires) | prose | phrase of 3+ words → `mapping-workflow-2.md` Decisions row 19 |
| loom-workflow/tests/scripts/test_visualization_card_hook.py:333 | test_negated_card_rule_rejected | '3) Be literal:' (assert in) | structural | capitalized label (heading text, table-header cell, bold label or name) |
| loom-workflow/tests/scripts/test_visualization_card_hook.py:333 | test_negated_card_rule_rejected | '4) Use tables or' (assert in) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 19 |
| loom-workflow/tests/scripts/test_visualization_card_hook.py:333 | test_negated_card_rule_rejected | '; no metaphors, analogies, "like" or "imagine".' (assert in) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 19 |
| loom-workflow/tests/scripts/test_visualization_card_hook.py:333 | test_negated_card_rule_rejected | 'in their language.' (assert in) | prose | phrase of 3+ words → `mapping-containers.md` Decisions row 19 |
| loom-workflow/tests/scripts/test_visualization_card_hook.py:413 | test_both_cards_point_at_the_plain_language_guide | 'references/plain-language.md' (assert in) | structural | path |
| loom-workflow/tests/scripts/test_visualization_card_hook.py:424 | test_full_card_names_skill_and_comparison_and_flow_triggers | 'loom-visualization' (assert in) | structural | names a skill, plugin or script (a hyphenated repo name) |
| loom-workflow/tests/scripts/test_visualization_card_hook.py:438 | test_coexist_card_trigger_phrases_do_not_overlap_toolkit | 'loom-visualization' (assert in) | structural | names a skill, plugin or script (a hyphenated repo name) |
| loom-workflow/tests/scripts/test_visualization_card_hook.py:444 | test_coexist_card_trigger_phrases_do_not_overlap_toolkit | 'ascii-graph' (re.search) | prose | 1-2 word phrase or term → `mapping-workflow-2.md` Decisions row 22 |

### Decisions — loom-workflow

The decisions live in the mapping files. Each prose row above ends with a pointer to its Decisions row.
