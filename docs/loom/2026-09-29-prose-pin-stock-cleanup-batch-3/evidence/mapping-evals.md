# Eval re-point mapping (W0-02)

These are the `docs/loom/evidence/mechanisms.yaml` evals that name a file or function on the batch-3 deletion list. Each was checked before any pruning. Line numbers are at HEAD `6c746759`. `check_mechanisms.py` prints "all clear" with net 142 both before and after, and exits 0. The mechanism count is unchanged, because only one eval line changed.

| line | mechanism id | old eval | new eval or kept | reason |
|---|---|---|---|---|
| 89 | `decision-map` | `loom-workflow/tests/decision-map/test_decision_map_intent_binding.py` | `loom-workflow/tests/decision-map/test_start_delivery.py::test_creates_intent_and_lists_it_under_the_criterion` | After W1-05's prunes, the old file keeps only format tokens and absences read from `SKILL.md`. The new node runs `start_delivery` and proves it. It writes `docs/loom/intent/<change-id>.md` with `originator: map:<id>`, `map: <id>` and `status: open`. It also lists `- delivery-intent: DA-<n> \| <path>` under the criterion. This is the binding the old file described in prose. The move also takes the old file out of the `gate-eval` class, so W1-05 prunes it like any other file. |
| 113 | `loom-memory` | `loom-workflow/tests/loom-memory/test_skill_contract.py` | kept | W1-01 deletes six pin functions and prunes one, and many checks stay. The four operations stay structured, as Trigger and Steps sections with numbered steps. The station-coupling and host-path absences stay. The flat-folder check runs `git`. The token and description budgets stay. So do the references-exist check, the manifest skills mount, and the Record digest tied to the `evals/record-timing.md` cold-read eval. |
| 50, 53, 56 | `using-loom-code`, `using-loom-design`, `using-loom-workflow` | `tests/test_loom_skill_description_catalog.py` | kept | Only `test_router_tables_preserve_direct_leaf_targets_and_goal_boundary` loses its two `goal-create` sentences. The routing corpus stays. So do the one-router-per-plugin count, the description accounting and the router link checks. |
| 110 | `critique` | `tests/test_loom_skill_description_catalog.py` | kept | The same file as the row above. The routing corpus, which expects `critique` on its held-out case, is untouched. |
| 219 | `UserPromptSubmit::visualization-card` | `loom-workflow/tests/scripts/test_visualization_card_hook.py` | kept | W1-05 prunes only one sentence, "Skip loom-visualization for one-paragraph answers", from `test_coexist_card_skip_sentence_names_the_skill`. The hook subprocess tests stay: coexist card, full card, config-dir override, malformed JSON and stdin, and unreadable card exits 0. |

## Checked and left unchanged

These evals name a single function in a file on the deletion list. None of those functions is on the list, so each one still resolves after pruning.

- L351 `dispatch-profile.relative-routing` names `test_dispatch_profile_resolver.py::test_mechanical_route_computes_each_model_tier`.
- L354 and L357 name `test_templates.py::test_skill_declines_vault_target` and `::test_mermaid_gate_paragraph_present_requires_confirmed_host`.
- L222 names `tests/test_loom_plugin_install_layout.py::test_codex_manifest_points_at_prompt_submit_card_hook`.
- No other eval names a file on the deletion list. The check was a grep of `mechanisms.yaml` for the basename of each of the 21 files.

## Test cases

- **A4 positive, every-moved-eval-resolves-before-pruning.** Command: `python3 loom-code/scripts/check_mechanisms.py`. It exits 0 and prints "all clear" with net 142. The new node passes by itself with pytest: 1 passed.
- **Negative, check-mechanisms-rejects-dangling-node.** The L89 function name was swapped for `test_no_such_function` in the working tree, then restored without a commit. The check exits 1 with: `RED [R4] decision-map: eval names a node loom-workflow/tests/decision-map/test_start_delivery.py does not define: test_no_such_function (not defined in the file and not collected by pytest)`. After the restore it exits 0.
