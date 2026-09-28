# Residual-pin mapping (residual fix before W2-01)

Defect class: a sentence pin left in a pruned batch-2 file. That is an assert that passes only while one literal sentence or phrase of runtime prose keeps its exact wording. It includes a scan that skips or finds exactly one rule sentence by its wording.

Where we searched: every batch-2 file that the census showed as `sentence-pin`, `other` or `has_pins=yes` after W1-01 to W1-06. Each remaining literal assert in those files was read and classified.

All paths are under `loom-code/tests/` unless stated otherwise. "Lens" means `loom-code/skills/closing-review/references/lenses.md`. Every kept test named below exists after this edit, and checker rule ids were checked against `python3 loom-code/scripts/loom_checker.py --list-rules`.

## Removed or re-anchored pins

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `test_build_mechanical_checks.py::test_no_speculative_preflight_ban_remains` (phrase loop: a negated package-suite sentence must say `does not hand off` or `skipped`) | a station sentence that stops Build from running the complete package suite | skill lens, `inconsistency` (a sentence contradicting Build's suite step); the two absence asserts stay in the same function | review lens dimension |
| `test_build_mechanical_checks.py::_is_pinned_floor_sentence`, `_FLOOR_PINS`, `RECIPE_PINS`, the `_affirms` import; `test_adversary_routing.py::recipe_pins` and the pin-reader half of `::test_recipe_test_module_and_pin_reader_synthetic` (now `::test_recipe_test_module_synthetic`) | a recipe's own pinned floor sentence was exempt from the implementer-floor scan. This code was dead, because `recipe_pins()` returned `{}` | `test_build_mechanical_checks.py::test_no_added_sentence_overrides_pinned_rules` still runs the implementer-floor scan, and its only exemption is negation | kept structural test |
| `test_build_mechanical_checks.py::_discard_literals_outside_rule` (it skipped exactly `NO_DISCARD_UNDO`) and the `NO_DISCARD_UNDO` constant in `test_adversary_protocol.py` | a sentence that tells an agent to undo with a discard command (`git restore`, `git clean` …). Rewording the rule sentence turned this scan red | `test_build_mechanical_checks.py::test_no_added_sentence_overrides_pinned_rules`: the scan now skips any negated sentence, not one sentence found by its wording | kept structural test |
| `test_build_mechanical_checks.py::_other_role_program_edit_sentences` (it skipped exactly `NO_OTHER_ROLE_EDITS_PROGRAM`) | an implementer or the orchestrator told to edit an adversarial program | `test_build_mechanical_checks.py::test_no_other_role_edits_adversarial_program`: the scan now skips any negated sentence | kept structural test |
| `test_build_mechanical_checks.py::_redispatch_for_caught_defect_sentences` and `ORDINARY_FIX_NO_REDISPATCH` (it skipped the sentence carrying `rather than for a product defect`) | Build re-dispatches the adversary for a program that correctly caught a product defect | skill lens, `inconsistency` on build §3. There is no heading or gate marker to re-anchor on (Risk 4) | review lens dimension |
| `test_plan_simplicity_text.py::test_a5_plan_step_asks_the_user_nothing` (the presence half: some sentence of the step must mention the user) | the Simplicity check step stops saying that it never asks the user | skill lens, `user-judgment-leak`; the scan that every user sentence of the step is negated stays in the same function | review lens dimension |
| `test_review_convergence_contract.py::test_finalize_failure_round_requires_no_relook` (`"unless the episode is stuck" in sentence`) | finalize's re-look sentence loses its stuck-episode condition | skill lens, `inconsistency` against §4; the same function keeps the negation scan and the Round 3 absences | review lens dimension |
| `test_acceptance_test_report_shape.py::test_template_has_one_row_per_criterion_and_evidence_file_path` (the `works / partly / not verified / fails` legend) | the template's verdict vocabulary drifts | the same function keeps the per-row Verdict-column check against the four verdicts | kept structural test |
| `test_acceptance_test_report_shape.py::test_evidence_file_shape_is_given_and_is_plain_markdown` (`never … \`#!\``) | the template stops forbidding executable evidence | the same function keeps the check that the evidence block does not start with `#!`; the wording of the ban is docs lens `omission` | kept structural test |
| `test_ship_station_text.py::test_ship_prose_rule_is_not_marked_as_a_gate` (the presence half: `NO_HANDOVER` must occur) | the no-handover rule drops out of ship | checker rule `publish.preconditions` (the refusal is the enforceable carrier); the same function keeps the not-gate-marked half | checker rule id |
| `test_ship_station_text.py::test_ship_never_runs_setup_unasked`, `AGREES`, `_sentences` (an un-negated setup-run sentence had to carry the `AGREES` phrase) | ship runs the setup command without the user's consent | skill lens, `omission` (a setup run with no consent input). No heading or gate marker isolates the sentence | review lens dimension |
| `test_sync_before_review_text.py::test_no_op_sync_dispatches_without_rerun` (`_sentence` found one sentence by `reports \`up to date\``) | the `up to date` branch starts a re-run | re-anchored on the `## 2. Compute review depth` heading: `test_sync_before_review_text.py::test_no_op_sync_dispatches_without_rerun` now scans every §2 sentence that names the checker output `` `up to date` `` | kept structural test |

The W1-04 row in `mapping-station.md` named `test_ship_never_runs_setup_unasked` as a kept test. That row now names skill lens `omission`, so no mapping row names a deleted function.

## False positives: code left as it is, with an override row

Each of these files got a `MANUAL_OVERRIDES` row in `classify-test-files.py`. The row says what the file asserts and that no sentence is asserted present:

| file | what its remaining literals are |
|---|---|
| `test_acceptance_test_report_shape.py` | table columns and markers, the evidence-block heading, the template path pointer, a full-suite absence scan |
| `test_adversary_protocol.py` | `loom_checker` import for the case-count scan, a one-home absence scan, YAML keys of the return block |
| `test_adversary_routing.py` | recipe link back to the protocol, exception messages, pytest stdout, `split_sentences` used only to pick a sentence to reword |
| `test_lenses_deletion_first.py` | lens table rows end with the `deletion-first` token |
| `test_plan_simplicity_text.py` | absences, the `references/plan-simplicity.md` path pointer, a negation scan |
| `test_review_convergence_contract.py` | gate-marker presence, heading-anchored sections, absence and negation scans |
| `test_reviewer_mechanical_evidence.py` | the lenses path pointer count, absence and negation scans |
| `test_ship_station_text.py` | AST recompute over `publish.py`, headings, absences, gate-region placement |
| `test_simplified_station_text.py` | checker import, absence and negation scans, summary-table rows, a manifest YAML value |
| `test_sync_before_review_text.py` | `sync-trunk` stdout and digest on real repositories, §2 absences, a `sync-trunk` count |
| `test_test_budget_text.py` | no line-number threshold, a gate-marker count |

Two existing rows got more precise reasons: `test_build_recovery_rules.py` (it also cites the three manifest keys) and `loom-workflow/tests/goal-create/test_skill_md.py` (the offer-site number is recomputed from the repository).

## Judged not pins, and kept

- `loom-workflow/tests/goal-create/test_skill_md.py::test_invocation_section_counts_the_offer_sites_that_exist`: the phrase `exactly <n> point(s)` is built from the number of offer sites scanned in the repository. The survey classed it as a recompute, and batch-1 rows cite it. It is a judgment call, and it is listed as a concern.
- `test_simplified_station_text.py::_selection_only_skip_conditions`: the `"plain words"` exemption is a two-word term for the second skip source, not a rule sentence.
- Label anchors `**Simplicity check.**` (`test_plan_simplicity_text.py::_step`) and `- **Round 3` (`test_review_convergence_contract.py::_round_three_bullet`): these are step and bullet labels, and the asserts on them are absences.
- `test_review_convergence_contract.py::test_reviewers_dispatched_after_build_checks`: `_BRANCH_ANTECEDENT` finds sentences by phrase. A rewording makes the scan find nothing, and it does not turn red.
