# Newly flagged loom-code and root files: pin mapping (W1-03)

Defect class: a direct sentence pin. That is an assert that passes only while one literal sentence or phrase of runtime prose (a skill, agent or reference file) keeps its exact wording.

Where we searched: the six files in the "Bucket loom-code" and "Bucket root tests" tables of `deletion-list.md`. Every row there was a prune, and each was pruned as listed. No function was deleted, so no function name cited in `docs/loom/evidence/mechanisms.yaml`, `AGENTS.md` or `loom-code/tests/test_module_criteria_text.py` went away.

"Lens" means `loom-code/skills/closing-review/references/lenses.md`. The skill lens scores an agent contract or `SKILL.md` on the five docs dimensions. Every kept test named below exists after this edit.

## Removed pins

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `loom-code/tests/test_agent_model_frontmatter.py::test_module_contract_rejects_retired_dispatch_ledger_wording` (`dispatch-profile.md` "active task context only") | the dispatch profile starts keeping a persisted dispatch ledger again | skill lens, `inconsistency` (a passage that brings back a ledger against the no-ledger rule); the `review.json` and `dispatch[]` absences stay in the same function | review lens dimension |
| `loom-code/tests/test_dispatch_profile_resolver.py::test_contract_defines_the_executable_json_boundary` ("on any other host", "pass the resolver's deterministic JSON result to the host-native spawn") | the contract stops telling the caller how to find the plugin root on other hosts and to hand the resolver's JSON to the spawn | skill lens `omission` (a step whose input, the plugin root or the spawn's input, the reader must guess). The same function keeps both command shapes and the JSON event keys. `loom-code/tests/test_dispatch_profile_resolver.py::test_cli_is_deterministic_json_and_rejects_malformed_input` checks only the resolver's own JSON output; it does not fail when the contract drops either instruction | review lens dimension |
| `loom-code/tests/test_dispatch_profile_resolver.py::test_contract_defines_the_executable_json_boundary` ("post-execution capability-quality failure", "pre-execution host rejection") | the contract blurs the two escalation kinds | skill lens `ambiguity` (the contract's two escalation kinds). `loom-code/tests/test_dispatch_profile_resolver.py::test_host_rejection_is_not_capability_quality_escalation` and `::test_preexecution_host_rejection_gets_one_override_free_replacement` run the resolver on both kinds, so they guard the code's split, not the contract's wording | review lens dimension |
| `loom-code/tests/test_dispatch_profile_resolver.py::test_stations_point_to_the_executable_resolver_contract` ("on any other host it is the directory two levels above this SKILL.md") | the build and closing-review stations lose the other-host plugin-root rule | the same function keeps the `dispatch-profile.md` link and the two absences; the rule's wording is skill lens `omission` (a step whose input the reader must guess) | review lens dimension |
| `loom-code/tests/test_legacy_contract_removed.py::test_implementer_has_no_per_task_package_suite_wording` ("The complete package suite runs at the end of Build and again in `finalize-review`, never per task.") | the implementer contract starts running the package suite per task | the three absence asserts stay in the same function; the wording is skill lens `inconsistency` against Build's suite step | review lens dimension |
| `loom-code/tests/test_probes_language_policy.py::test_reviewer_nitclause_absent` (reviewer.md "style is out of scope") | the docs-lint carve-out paragraph is reworded or dropped | the same function keeps the `docs-lint` presence assert and the single-paragraph compound scan; the carve-out wording is skill lens `omission` | review lens dimension |
| `loom-code/tests/test_ship_worktree_merge.py::test_ship_accepted_land_renders_absolute_worktree_in_command` ("never rely on the Bash tool's workdir") | ship lets `land` run in whatever directory the Bash tool happens to use | the same function keeps the command shape `cd '<absolute worktree root>' && python3 <loom-code>/scripts/loom_checker.py land` | kept structural test |
| `tests/test_loom_plugin_install_layout.py::test_lookup_table_lives_in_one_place_and_every_skill_links_it` ("on any other host", "two levels above this SKILL.md", "may contain one version subdirectory", "use the newest") | the other-host lookup row stops allowing a version subdirectory, or points at the wrong directory | skill lens `inconsistency` (the lookup row against flat and versioned install layouts). `tests/test_loom_plugin_install_layout.py::test_sibling_lookup_resolves_flat_and_versioned_installs` executes a hardcoded model of the lookup; the row wording is review-only. The pruned function itself keeps the five-link count, the one-lookup count and the one Codex/Antigravity row | review lens dimension |

## Output asserts left untouched

Asserts on program output are behavior checks and stay. For example, `loom-code/tests/test_dispatch_profile_resolver.py::test_cli_is_deterministic_json_and_rejects_malformed_input` still asserts `bad.returncode == 2` and `bad.stdout == ""` on the resolver CLI, and the resolver tests above still assert on `dispatch_profile.resolve` results. None of these was edited.

## Classifier after the edit

| file | class | has_pins |
|---|---|---|
| `loom-code/tests/test_agent_model_frontmatter.py` | structure | no (no phrase pin) |
| `loom-code/tests/test_dispatch_profile_resolver.py` | behavior | no |
| `loom-code/tests/test_legacy_contract_removed.py` | behavior | no |
| `loom-code/tests/test_probes_language_policy.py` | structure | no (no phrase pin) |
| `loom-code/tests/test_ship_worktree_merge.py` | behavior | no |
| `tests/test_loom_plugin_install_layout.py` | behavior | no |
