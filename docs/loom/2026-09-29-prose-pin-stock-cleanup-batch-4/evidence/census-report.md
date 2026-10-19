# Batch 4 census and recount (W2-01)

Every number below comes from a clean detached worktree (`git worktree add --detach <scratchpad>/<wt> <ref>`), removed afterwards (plan Risk 3). HEAD is the W2-01 commit, the one that adds this report. The base is `1ef82fe8`. W3-01 later refreshed the A1 census, the candidate counts and the A5 recount from a clean worktree of its own state; the A4 section is W2-01's run, and W3-01 changed no mapping row. The stitch section is the closing-review round-1 fix's run, from a clean worktree of the fix commit, because that fix changed mapping rows.

A census run from the main checkout gives different counts (`not-prose 59` instead of 54), because nested worktrees under `.claude/worktrees` add files to the scan. Only the clean-worktree numbers count.

## What W2-01 changed

- **Override rows.** The classifier's `MANUAL_OVERRIDES` gained 13 rows. Each is for a file that the W1 prunes left at `has_pins=yes` or in `other`, with a reason that names its current remaining hits. Seven existing rows had reasons that named removed tokens or hits that are no longer there, and W2-01 rewrote them: `test_acceptance_test_report_shape.py`, `test_adversary_layout.py`, `test_architecture_doc_consumers.py` (it named "rule id"), `test_decision_map_intent_binding.py`, `test_templates.py`, `test_architecture_skill.py` and `test_adversarial_batch3_census_misses.py`. Besides the override table and its reasons, W2-01 changed the classifier in one place only, the detector change below.
- **Known miss fixed (plan item 2).** In `loom-workflow/tests/scripts/test_visualization_card_hook.py`, the `SITUATIONS` regex values reach `re.search` through `SITUATIONS.items()` inside a negated comprehension filter, which collects the situations a card does not name. `pin_candidates` now sees that form. The TDD probe is `docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/test_classify_test_files.py::test_regex_values_through_items_collected_when_unmatched_flagged`. It went RED first, and its negative case keeps the un-negated form (collected when present) as an absence. Repo-wide, the change added exactly the 8 `SITUATIONS` rows and nothing else. They were judged prose and deleted, together with `situation_errors`, `_flat_body` and four tests. The decision and mapping rows are in `mapping-containers.md` under `## W2-01 additions`.
- **Stale mapping citations (plan item 5).** Three replacement cells in `mapping-workflow-2.md` cited compaction test names that W1-08 later renamed. They now cite `test_recap_state_compaction.py::test_entrypoint_tokens_and_schema_before_the_ordered_six_section_template` (two rows) and `test_handoff_compaction.py::test_entrypoint_structure_and_schema_before_artifact_steps`. W2-01 read both bodies, and they still check what the rows claim: the schema pointer comes before the template or before step 2, and the heading order holds.
- **`candidate-list.md` regenerated** at HEAD. Every remaining prose row points at its Decisions row.

## What W3-01 changed

W3-01 is the adversary fix round. The build adversary's program (commit `35396265`) found two lookup forms the census missed, both already used by the repository's own tests. Its two probes were red. The program graduated unchanged, except for its import path, to `loom-code/tests/test_adversarial_batch4_census_lookup_forms.py`, and both probes are now green. `pin_candidates` gained two forms:

- **`.find()` presence lookups.** A `.find()`/`.rfind()` lookup of a literal on markdown text counts when an assert compares its result as present (`!= -1`, `>= 0`, `> -1`, `-1 <`, mirrored or chained), either directly or through the name the result is assigned to. It is counted on the lookup line. Negative probe: `test_classify_test_files.py::test_find_in_output_not_flagged` (the same lookup on subprocess output is not a pin).
- **Markdown held on `self`/`cls`.** An attribute that any method sets from markdown text (`self.body = SKILL.read_text()`, or the unparsed position of `self.fm, self.body = _parse_skill_md()`) is markdown text wherever `self.<attr>` or `cls.<attr>` is read. The attribute name is judged file-wide, like a variable name.

The rerun surfaced 13 new candidates, all `structural` (field names, headings, paths, one placeholder) and **no prose row**, so nothing was pruned. The rows are in `mapping-containers.md` under `## W3-01 additions`. `MANUAL_OVERRIDES` gained one row for the graduated program, and the `test_goal_shape.py` reason now names `stop-when` and the `.find()` lookups.

## A1 — census

Command, run from the worktree root:

```
python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py
```

**Exit 0. Counts at HEAD (W3-01): `{'behavior': 110, 'gate-eval': 0, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 0, 'structure': 66}`. 34 files show `has_pins=yes`, and every one has an override row (50 override rows in all).** The one extra `behavior` file is the graduated adversary program. At W2-01 the counts were the same except `behavior: 109`, with 49 override rows.

| point | sentence-pin | gate-eval | structure | other | `has_pins=yes` files | source |
|---|---|---|---|---|---|---|
| batch-3 HEAD (batch-3 classifier) | 0 | 0 | 66 | 0 | 23 | batch-3 report |
| `4d81b1c0`, after W1-09, before W2-01 | 6 | 0 | 58 | 2 | 34 (13 without an override row) | this task's first run |
| W2-01 | 0 | 0 | 66 | 0 | 34 (all with an override row) | W2-01 run |
| HEAD (W3-01) | **0** | **0** | **66** | **0** | **34 (all with an override row)** | this run |

**Negative case, other-bucket-exits-1.** In a throwaway worktree of HEAD, not committed, the key of the `test_git_memory_compaction.py` override row was changed so that it no longer matched. The census printed `other: 1`, listed that file as `other`, printed `FAIL: files in \`other\` belong to no named class; add a MANUAL_OVERRIDES row` and **exited 1**.

**Override rows.** The intent lets a file keep `has_pins=yes` only when the report gives that file a reason. Each reason below is the override text as the census prints it. The only change is that a `|` inside a reason is escaped as `\|`.

| file | auto class | class after override | override reason |
|---|---|---|---|
| `loom-code/tests/test_acceptance_test_report_shape.py` | grammar-invariant | structure | template table columns, rows and markers, the evidence block heading, the template path pointer in the tester contract, a full-suite absence scan fed by split_sentences, no gate marker, and the evidence path pointer outside every gate block; the remaining hits are the Verdict column enum (works\|partly\|not verified\|fails) and the Re-run cell grammar (`carried over — <reason>`, `re-tested`); the two sentence-anchored verdict scans were deleted in batch 4 (W1-01), so no sentence is asserted present |
| `loom-code/tests/test_adversarial_batch3_census_misses.py` | sentence-pin | behavior | runs this classifier (path-loaded) and asserts on its result; the sentence-assert hit is a synthetic test source string fed to direct_pin_lines, and the residual check asserts named files carry no skill sentence, an absence |
| `loom-code/tests/test_adversarial_batch4_census_lookup_forms.py` | other | behavior | runs this classifier (path-loaded) and asserts on its result; the sentence-assert hits are synthetic test source strings fed to direct_pin_lines |
| `loom-code/tests/test_adversary_layout.py` | behavior | behavior | loop-form hit is SHARED_HEADINGS asserted in the protocol's parsed heading list: section headings, not prose. The batch-4 hits are the KIND_MARKERS fragments of a one-home absence check (each asserted absent outside its own file), the `at commit`/`at split commit` sha lines of the frozen correspondence note fed to git show, the `(preamble)` sentinel cell, and the `Reuse first, update with evidence` heading |
| `loom-code/tests/test_adversary_protocol.py` | behavior | behavior | imports MAX_PROBE_PROGRAMS from loom_checker for the case-count scan; the rest is a one-home absence scan and YAML keys of the return block; no sentence asserted present |
| `loom-code/tests/test_adversary_recipe_shape.py` | sentence-pin | structure | split_sentences feeds a duplicate-sentence check across recipe files; no prose literal is asserted |
| `loom-code/tests/test_adversary_routing.py` | behavior | behavior | runs the adversary tests in repo copies after real add, remove and reword edits; literals are a recipe's link back to the protocol, exception messages and pytest stdout; split_sentences only picks a sentence to reword; no sentence asserted present |
| `loom-code/tests/test_architecture_doc_consumers.py` | sentence-pin | structure | remaining hit is the `architecture-conformance` dimension id in the reviewer code row; the rest is the `ratified-by: <name> <date>` line grammar in write-plan Step 5 and the lenses code table, the Risk line field name, a lens-table row regex and a heading-bounded N/A bullet check; the sentence asserts were pruned in batch 3 (W1-01) and the 'rule id' phrase in batch 4 (W1-01) |
| `loom-code/tests/test_build_mechanical_checks.py` | sentence-pin | structure | remaining hits are absence scans: no added sentence in which another role edits an `adversarial program`, no un-negated implementer `floor` sentence, and no retired attack-catalogue or trailer pointer; no sentence asserted present |
| `loom-code/tests/test_build_recovery_rules.py` | grammar-invariant | structure | one-home scans only: the build.absence-recovery gate block restates no artifact-to-station mapping, and §1-§2 repeat none of the rule; the block cites the three manifest keys (path pointers); split_sentences feeds the scan, no sentence is asserted present; RL-12 is the eval of build.absence-recovery |
| `loom-code/tests/test_closing_review_recovery_rules.py` | grammar-invariant | structure | one-home scan only: the review.absence-recovery gate block restates no artifact-to-station mapping; split_sentences feeds that scan, no sentence is asserted present; RL-04 is the eval of review.absence-recovery |
| `loom-code/tests/test_dispatch_profile_resolver.py` | behavior | behavior | runs the dispatch-profile resolver; the prose-side hit is the `capabilities` JSON input key of the resolver boundary in dispatch-profile.md, next to the `event` keys |
| `loom-code/tests/test_lenses_deletion_first.py` | sentence-pin | structure | reviewer.md lens table rows end with the deletion-first dimension token; no sentence asserted |
| `loom-code/tests/test_loom_publish.py` | behavior | behavior | loop-form hit is CONTEXT_HEADINGS asserted in the reason the checker's validate_contextual_pr_body returns: headings in program output |
| `loom-code/tests/test_plan_simplicity_text.py` | sentence-pin | structure | absence checks, the write-plan step's path pointer to plan-simplicity.md, and a scan that every user sentence of the step is negated (split_sentences); no sentence asserted present |
| `loom-code/tests/test_probes_language_policy.py` | sentence-pin | structure | remaining hits are the `docs-lint` KICKOFF-DEFAULTS key, the negation token set of a polarity check, and the concept noun `english` in the paragraph that names the probe file shape; the nit clause keeps only proper names (English, EARS, Conventional Comments) and the `nit` value |
| `loom-code/tests/test_review_convergence_contract.py` | grammar-invariant | structure | gate-marker presence, heading-anchored sections, and absence or negation scans fed by split_sentences; no sentence asserted present |
| `loom-code/tests/test_reviewer_mechanical_evidence.py` | sentence-pin | structure | the lenses path pointer count in reviewer.md and absence or negation scans; no sentence asserted present |
| `loom-code/tests/test_ship_station_text.py` | behavior | behavior | recomputes the refusal premise from publish.py source; the rest is headings, absences and gate-region placement; no sentence asserted present |
| `loom-code/tests/test_simplified_station_text.py` | behavior | behavior | imports the checker's STEP_PLAIN_NAMES; the rest is absence and negation scans (split_sentences), summary-table rows and a manifest YAML value; no sentence asserted present |
| `loom-code/tests/test_sync_before_review_text.py` | behavior | behavior | runs sync-trunk on real repositories and asserts its stdout and the digest; the prose half is absences under the §2 heading and a count of sync-trunk; no sentence asserted present |
| `loom-code/tests/test_write_plan_station_text.py` | grammar-invariant | grammar-invariant | remaining hit is LANE_WORDING_RE in lane_hits, an absence scan (no runtime file names a lane); the rest is release-metadata pins, heading-anchored key scans and grammar checks |
| `loom-workflow/tests/decision-map/test_skill_doc.py` | behavior | behavior | loop-form hit is DOCUMENTED_COMMANDS: command shapes, which the same test also runs (start_delivery.py excepted; test_start_delivery.py owns it). The direct sentence asserts batch 2 left were pruned in batch 3 (W1-01, W1-07); the rest is operation headings, fixed terms, re-entry and phase code tokens recomputed from the scripts, the ticket template grammar, schema_version, manifest fields, and the Codex manifest defaultPrompt sentence, kept as an interface string, not skill prose |
| `loom-workflow/tests/goal-create/test_goal_shape.py` | sentence-pin | structure | remaining hits are the vendor names openai and anthropic in the paragraphs located by the `## The 4,000-character budget` heading and the `**Attribution accuracy**` bold label, and the four-field names outcome, constraints, verification and stop-when (also required in order through `.find()` lookups, W3-01) |
| `loom-workflow/tests/goal-create/test_skill_md.py` | gate-eval | structure | mode headings, reference paths resolving, the floor command shape, the session-activation gate blocks, template non-restatement and the offer-site count (its number recomputed from the sites scanned in the repo); eval of goal-create.session-activation, no sentence asserted |
| `loom-workflow/tests/independent-advisor/test_independent_advisor_readmes.py` | sentence-pin | structure | remaining hit is OVERCLAIM_PATTERN, an absence (asserted to find nothing in the READMEs); the concept matchers left are the skill name, the sibling skill name and the mode identifiers |
| `loom-workflow/tests/loom-visualization/test_references.py` | sentence-pin | structure | remaining hits are H3 situation titles matched against the parsed heading list and in `Pointer:` lines, the `Load this when:` line label, document-type names read as cells of SKILL.md's routing table, the `key-value` table-form term, the IN_CELL_ITEMS glyph, source and cross-reference tokens, and the node-structure reference's headings and bold labels |
| `loom-workflow/tests/loom-visualization/test_templates.py` | behavior | behavior | direct-pin hits are the client-matrix table column header 'Form in a chat reply' and its column-parsed cell value 'markdown table', the template heading 'When to use', the `title`/`body` keys of the templates' JSON examples, and the ASCII_BY_CLIENT regex, an absence (asserted to find nothing). The three pinned_sentence_ok polarity checks (MERMAID_PIN, TABLE_ASCII_PIN, CHAT_PROCEEDS_PIN) are kept on purpose (agent-decided): they read only sentences inside the mermaid-only-when-confirmed and obsidian-boundary `<!-- gate: -->` blocks, whose mechanisms.yaml evals (L357, L354) sit in this file, and each fails a negated sentence, so they check the rule's polarity, not only its wording |
| `loom-workflow/tests/scripts/test_loom_visualization_compaction.py` | structure | structure | loop-form hit is a list of `## ` headings in SKILL.md |
| `loom-workflow/tests/scripts/test_readme_card_timing.py` | sentence-pin | structure | remaining hit is `visualization card`, the component's own current name, required in the README descriptions and the hook docstring |
| `loom-workflow/tests/scripts/test_visualization_card_hook.py` | behavior | behavior | runs the hook as a subprocess; the prose-side hits are the kept rule_polarity_errors gate (batch 3's named replacement) with its mutation sites, and the `ascii-graph` skill name; the SITUATIONS phrases were deleted in batch 4 (W2-01) |
| `tests/test_agy_install_docs.py` | structure | structure | loop-form hit is agy and git command shapes in the Antigravity CLI section |
| `loom-design/tests/interface/test_design_md_schema_keys.py` | behavior | behavior | imports the design_md_spec_keys script; remaining hits are the `> **Grounding.**` and `> **Scope` blockquote labels that bound the grounding note, component sub-token keys (size, height, padding, width) as a mutation precondition, and a confirm-and-spec header check that is asserted absent; docstring pins are out of scope |
| `loom-design/tests/interface/test_design_system_skill.py` | structure | structure | loop-form hit is the eight canonical DESIGN.md section names in the schema |
| `loom-design/tests/interface/test_knowledge_triage.py` | behavior | behavior | runs git show as a subprocess; remaining hits are the tier labels shaping and deferrable, the `design-conformance` lens name, and the bucket names craft, domain-convention and project-local |

## A1 — candidates (`--candidates`)

Command: the same script with `--candidates`. It exited 0.

| plugin | prose | structural | kept-batch3 | files with >=1 prose candidate |
|---|---|---|---|---|
| root tests | 0 | 16 | 0 | 0 |
| loom-code | 35 | 130 | 0 | 13 |
| loom-design | 16 | 105 | 0 | 2 |
| loom-workflow | 55 | 374 | 3 | 7 |
| **total** | **106** | 625 | 3 | 22 |

These are the closing-review round-1 counts. W2-01 listed 609 structural rows; the two W3-01 forms added 13 structural rows (all in loom-workflow) and no prose row, and `decide.py` rerun on the W3-01 list printed `prose rows: 106; undecided: 0`. The closing-review round-1 fix adds 3 structural rows and no prose row (structural 625, prose 106): the `result:` field-key regex in `test_acceptance_test_report_shape.py`, and the `**Derivation contract:**` bold label and its slash-roster regex in `test_design_md_schema_keys.py`. `candidate-list.md` was regenerated for them from a clean worktree, and its 106 prose-row pointers carried over unchanged.

W0-01 counted 233 prose rows. **All 106 prose rows left are decided.** The throwaway script `decide.py` (text below) found a W1 or W2-01 `Decisions` row for each of them, and printed `prose rows: 106; undecided: 0`. None of the 106 is decided `prune` or `delete`. Each is a keep with a reason: heading, label, field key, column cell, proper name, absence or one-home scan, or kept gate. W2-01 also read all 106 pointers and checked that each one lands on the row that judges that literal. The pointers are in `candidate-list.md`.

## A4 — mechanism census

Command: `python3 loom-code/scripts/check_mechanisms.py`, from the HEAD worktree root.

**Exit 0, all clear. The net mechanism count is 142, unchanged from the base.** By class: skill 23, checker-rule 26, hook 10 (9 in the net count, because `PostToolUse:Skill:language-anchor.py` is exempt), contract 64, prose-gate 20.

**Moved evals: none.** `git diff 1ef82fe8..HEAD -- docs/loom/evidence/mechanisms.yaml` is empty. No batch-4 task deleted a whole test file or a function that an eval names. `mechanisms.yaml` line 219 names the whole of `test_visualization_card_hook.py`, and that file keeps its hook subprocess tests.

**Negative case, dangling-eval-reported.** In a throwaway worktree of HEAD, not committed, line 219's eval was changed to name `test_visualization_card_hook.py::test_both_cards_name_the_conversation_situations`, a function W2-01 deleted. The check **exited 1** and printed:

```
RED [R4] UserPromptSubmit::visualization-card: eval names a node loom-workflow/tests/scripts/test_visualization_card_hook.py does not define: test_both_cards_name_the_conversation_situations (not defined in the file and not collected by pytest)
```

## A5 — execution-test recount

Command: `python3 <HEAD wt>/docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --count-exec <wt> --list`, run once on the base worktree and once on the HEAD worktree. No batch-4 task changed the counting code.

| ref | executing test functions |
|---|---|
| base `1ef82fe8` | **1927** |
| HEAD (W2-01) | **1927** |
| HEAD (W3-01) | **1929** |

**Positive, recount-not-below-base.** 1927 ≥ 1927. The two `--list` outputs are identical: nothing was removed and nothing was added. At W3-01 (run with the W3-01 classifier, whose counting code is unchanged) the count is 1929 ≥ 1927: the `--list` diff against the base adds exactly the two tests of the graduated adversary program, which load and run the classifier, and removes nothing.

**Negative, deleted-function-tagged-exec-fails.** `stitch4.py` (below) lists every def that `1ef82fe8..HEAD` removed from a changed test file. There are 81, 64 of them test functions, and a rename counts as a removal. **None of the 64 is on the base `--list` output.** In a throwaway worktree, `test_visualization_card_hook.py::test_enabled_toolkit_prints_coexist_card`, which runs the hook, was deleted and the deletion committed there. The recount printed 1926, and the `--list` diff named that function. `stitch4.py` reported it under "deleted test functions on the base exec list". The worktree and its commit were thrown away. That scratch commit used `--no-verify`, because it lived only in a detached throwaway worktree and never on the branch.

## Mapping files, stitched

Sources: `mapping-code.md` (W1-01), `mapping-design.md` (W1-02), `mapping-workflow.md` (W1-03), `mapping-workflow-2.md` (W1-06), `mapping-compaction.md` (W1-08) and `mapping-containers.md` (W1-09, plus `## W2-01 additions`). The stitch keeps every row under a `file::function(s) | defect class it guarded | named replacement | kind` header.

These counts are from the closing-review round-1 fix, rerun from a clean worktree of the fix commit. That fix audited all 28 rows marked `kept structural test` against the test each one cites. 23 cited a test that stays green when the row's defect class happens, and they are now `review lens dimension`, with the test kept as a side note. It restored two field-key and roster set checks, so two rows became `kept structural test`: mapping-code's `result:` row and mapping-design's Derivation contract row, which was `review-only`. It also split mapping-code's verdict-vocabulary row in two. At W2-01 the stitch counted 72 rows: 41 review lens dimension, 28 kept structural test, 2 review-only, 1 checker rule id.

**73 rows in all.**

| kind | rows |
|---|---|
| review lens dimension | 64 |
| kept structural test | 7 |
| review-only | 1 |
| checker rule id | 1 |

| source | rows |
|---|---|
| mapping-code | 7 |
| mapping-design | 16 |
| mapping-workflow | 21 |
| mapping-workflow-2 | 13 |
| mapping-compaction | 7 |
| mapping-containers | 9 (8 from W1-09, 1 from W2-01) |

**Replacement check (plan item 5).** `stitch4.py`, run from the HEAD worktree root, printed:

```
rows: 73
by kind: {'kept structural test': 7, 'review lens dimension': 64, 'checker rule id': 1, 'review-only': 1}
by file: {'mapping-code': 7, 'mapping-design': 16, 'mapping-workflow': 21, 'mapping-workflow-2': 13, 'mapping-compaction': 7, 'mapping-containers': 9}
replacement defs cited and resolved: 43
deleted defs in changed test files: 81 (test functions: 64 )
exec base: 1927 head: 1929 removed from list: [] added: ['loom-code/tests/test_adversarial_batch4_census_lookup_forms.py::test_census_find_presence_lookup_flags_pin', 'loom-code/tests/test_adversarial_batch4_census_lookup_forms.py::test_census_self_attribute_markdown_flags_pin']
deleted test functions on the base exec list: []
problems: 0
```

The first run, before this task's fix, reported the three stale `mapping-workflow-2.md` citations named above. After the fix it reported 0 problems. Every `file::function` in a replacement cell is a function or class defined at HEAD, and none of them is a def the branch deleted. The one `checker rule id` row cites `standing.warn`, which `loom_checker.py --list-rules` lists.

## Known limits

- **Two-level helper passing.** A needle passed through two local helpers before it meets markdown text is not seen. The `pin_candidates` docstring records this.
- **Subscripts and non-literal regexes.** A needle read by subscript (`phrases[0]`), or held in a regex that is not a literal, is not seen.
- **Single-word generator names.** Since W1-09, a single word that is the `<name>` of a `gen_<name>` script on disk is classed structural. A prose word that happens to match a generator's name would pass as structural.
- **Capitalized-label heuristic.** A short capitalized literal is classed as a heading, table-header cell, bold label or name, without checking the markdown. The W1 tasks re-checked the `capitalized label` and `1-2 word` structural rows of their own files by hand (P1) and pruned the prose phrases they found there. Files outside the W1 lists were not re-checked.
- **Python docstring pins.** The docstrings of `loom-design/tests/interface/test_design_md_schema_keys.py` quote prose, and the census does not read docstrings. They are out of scope.
- **`has_pins` is partly regex-level.** Some files show `has_pins=yes` even when `--candidates` lists no prose row for them, for example `test_adversary_recipe_shape.py` and `test_plan_simplicity_text.py`. That happens for a file whose auto class is `sentence-pin` or `grammar-invariant`, and for a behavior file that matches `SENTENCE_ASSERT` and imports a prose helper. Each such file carries an override row that says what the regex hit.
- **The W2-01 detector form is narrow.** It sees a negated `re.search`, `re.match` or `re.fullmatch` in a comprehension filter, whose pattern is bound by that comprehension's target. A negated search through a `re.compile`-bound name in the same position is not covered.
- **Frozen probe of an earlier change.** `docs/loom/2026-09-16-plain-language-follow-ups/evidence/probes/test_probe_card_guard_bypasses.py` imports `missed_alternative_errors` and `missed_alternative_verb_errors`, which W1-09 deleted, and `situation_errors` and `SITUATIONS`, which W2-01 deleted. It no longer imports cleanly. It is not in the package suite, and only that change's own `attestation.json` names it.
- **Decision pointers are machine-matched.** `decide.py` matches on the file's basename, then the literal as a token, then the function name. W2-01 read all 106 matches. Where one Decisions row covers several functions or literals, the pointer names that shared row.
- **Synthetic-only lookup forms (W3-01).** The batch-4 adversary also listed forms that no test in the repository uses, and W3-01 did no detector work for them: `md.count(x)` bare or `!= 0`, `md.partition(x)[1]`, `len(md.split(x)) == 2`, an annotated module constant (`X: str = "..."`), a `frozenset({...})` collection, a `'a ' + 'b'` concatenated constant, and `parametrize(..., argvalues=[...])` passed by keyword. A needle in any of these forms is not seen.
- **`.find()` in a file that reads no skill markdown.** The W3-01 `.find()` form follows the same file rule as every other form. `tests/test_agy_install_docs.py:61` compares `-1 < body.find(...)`, but `body` is a README section and the file names no skill, agent or reference markdown path, so the census does not scan it. Its needle, an `agy plugin install` command, would be classed structural anyway.
- **`.find()` markers with no letter.** `test_prompts_parseable.py:120` looks up the step markers `1.` to `4.` through `.find()`. The form is seen, but a literal with no letter is never a candidate.
- **A behavior file can gain a pin without an override and still exit 0.** A file whose auto class is `behavior` (it also runs a program) can gain a new prose pin and show `has_pins=yes` without an override reason, yet the headline sentence-pin count stays 0 and the census exits 0. Such a file is caught only by reading the `has_pins` column or the candidate list, not by the exit code.
- **Kept by batch 3** (out of scope): the three `pinned_sentence_ok` gate polarity checks in `test_templates.py`, and the Codex `defaultPrompt` string in `decision-map/test_skill_doc.py`.

## Package suite

`env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`, run on the W2-01 code state. **EXIT=0**: 3211 pytest tests passed, 0 failed, and every shell test printed PASS. Rerun on the W3-01 code state: **EXIT=0**, 3213 pytest tests passed (the two added are the graduated adversary program), 0 failed, and every shell test printed PASS.

<details><summary>decide.py</summary>

```python
"""Throwaway (batch-4 W2-01): link every prose row of `--candidates` output to a Decisions row.

Usage (from a clean worktree root): python3 decide.py <candidates.md> [<out.md>]
Decisions rows are the data rows of each mapping file's `## Decisions` table (and the
`### Decisions` table under `## W2-01 additions`), numbered in order. The table header names
the columns: a `file::function` column, or `file:line` plus `function`, and a literal column.
A prose row is decided by the first Decisions row, among rows naming the candidate's file
(by basename), that:
  1. names the candidate's function and holds the literal as a whole backticked or quoted token;
  2. else holds the literal as such a token (literal column first, then the whole row);
  3. else contains the literal (backslashes and backticks normalized);
  4. else names the candidate's function.
Writes <out.md> = the input with `→ <mapping file> Decisions row N` appended to the reason of
each decided prose row; prints undecided rows and exits 1 if any.
"""
import ast
import glob
import re
import sys

EV = "docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-4/evidence/"
rows = []  # (mapping, n, first cell incl. function, whole row text, literal cell)
for m in sorted(glob.glob(EV + "mapping-*.md")):
    name = m.rsplit("/", 1)[-1]
    on, n, layout = False, 0, None
    for line in open(m, encoding="utf-8"):
        if line.startswith("## "):
            on = line.strip().startswith("## Decisions")
            continue
        if line.startswith("### "):  # only the `### Decisions` table under `## W2-01 additions`
            on = line.strip() == "### Decisions"
            continue
        if not (on and line.startswith("|")):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if set("".join(cells)) <= set("-: "):
            continue
        low = [c.lower() for c in cells]
        if any(c.startswith(("file", "#")) for c in low[:2]):  # a header row: record the layout
            f = next(i for i, c in enumerate(low) if c.startswith("file"))
            fn = low.index("function") if "function" in low else None
            lit = next((i for i, c in enumerate(low) if "literal" in c), f + 1)
            layout = (f, fn, lit)
            continue
        if layout is None or len(cells) <= max(i for i in layout if i is not None):
            continue
        f, fn, lit = layout
        first = cells[f] + ("::" + cells[fn] if fn is not None else "")
        if ".py" not in cells[f] and rows and rows[-1][0] == name:  # `same`: the row above's file
            first = rows[-1][2] + " / " + first
        n += 1
        rows.append((name, n, first, " | ".join(cells), cells[lit]))


def norm(s):
    return s.replace("\\|", "|").replace("\\\\", "\\").replace("`", "")


def tokens(text):
    got = {norm(a or b) for a, b in re.findall(r"`([^`]+)`|'([^']+)'", text.replace("\\|", "|"))}
    return got | {t.strip("'") for t in got}


def decided(path, func, lit):
    base = path.rsplit("/", 1)[-1]
    mine = [r for r in rows if base in r[2]]
    names = lambda r: re.search(r"\b" + re.escape(func) + r"\b", r[3])
    lit_n = norm(lit)
    for pool, cells in (([r for r in mine if names(r)], (4, 3)), (mine, (4, 3))):
        for cell in cells:
            for r in pool:
                if lit_n and lit_n in tokens(r[cell]):
                    return r
    for r in mine:
        if lit_n and lit_n in norm(r[3]):
            return r
    for r in mine:
        if names(r):
            return r
    return None


out, bad, total = [], [], 0
for line in open(sys.argv[1], encoding="utf-8"):
    cells = line.rstrip("\n").split(" | ")
    if len(cells) == 5 and cells[3] == "prose":
        total += 1
        path = cells[0].lstrip("| ").rsplit(":", 1)[0]
        lit = ast.literal_eval(cells[2].rsplit(" (", 1)[0].replace("\\|", "|"))  # `repr(literal) (form)`
        r = decided(path, cells[1], lit)
        if r is None:
            bad.append(line.strip())
        else:
            line = line.rstrip("\n").rstrip(" |") + f" → `{r[0]}` Decisions row {r[1]} |\n"
    out.append(line)
if len(sys.argv) > 2:
    open(sys.argv[2], "w", encoding="utf-8").write("".join(out))
print(f"prose rows: {total}; undecided: {len(bad)}")
for b in bad:
    print("  ", b[:220])
sys.exit(1 if bad else 0)
```

</details>

<details><summary>stitch4.py</summary>

```python
"""Throwaway (batch-4 W2-01 A3/A5): stitch the six batch-4 mapping files and check them.

Run from a clean worktree root: python3 stitch4.py <base-exec-list.txt> <head-exec-list.txt>
- keeps rows of every table headed `file::function... | defect class it guarded | named replacement | kind`;
- every `path.py::name` or `::name` token in the replacement cell (a bare `::name` resolves to the
  last path named in that cell, else the row's first-column path; a partial path resolves by
  suffix among tracked test files) must be a def (function or class) at HEAD, and must not be a
  def that BASE..HEAD deleted from a changed test file;
- every backticked rule id in a `checker rule id` row must be in `loom_checker.py --list-rules`;
- A5: head exec count >= base; no deleted test function is on the base exec list.
"""
import ast
import re
import subprocess
import sys
from collections import Counter

EV = "docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-4/evidence/"
FILES = ["mapping-code", "mapping-design", "mapping-workflow", "mapping-workflow-2",
         "mapping-compaction", "mapping-containers"]
BASE = "1ef82fe8"
ROOTS = ["loom-code/tests", "loom-workflow/tests", "loom-design/tests", "tests"]


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True)


def defs(ref, path):
    r = git("show", f"{ref}:{path}")
    if r.returncode:
        return None
    return {n.name for n in ast.walk(ast.parse(r.stdout))
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}


changed = git("diff", "--name-only", f"{BASE}..HEAD", "--", *ROOTS).stdout.split()
tracked = git("ls-files", *ROOTS).stdout.split()


def full(p):
    p = p.replace("…/", "").strip("`")
    same = [f for f in tracked if f == p or f.endswith("/" + p)]
    return same[0] if len(same) == 1 else None


deleted = set()
for f in changed:
    if f.endswith(".py"):
        deleted |= {(f, n) for n in (defs(BASE, f) or set()) - (defs("HEAD", f) or set())}
rules = {ln.split("\t")[0].split()[0] for ln in subprocess.run(
    [sys.executable, "loom-code/scripts/loom_checker.py", "--list-rules"],
    capture_output=True, text=True).stdout.splitlines() if ln.strip()}

TOKEN = re.compile(r"([\w./…-]+\.py)?::(\w+)")
problems, kinds, per_file, cited = [], Counter(), Counter(), set()
for name in FILES:
    mode = False
    for line in open(EV + name + ".md", encoding="utf-8"):
        if not line.startswith("|"):
            mode = False  # any non-table line ends the table
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if cells[0].startswith("file::function"):
            mode = len(cells) == 4 and "named replacement" in cells[2]
            continue
        if not mode or set("".join(cells)) <= set("-: "):
            continue
        first, repl, kind = cells[0], cells[2], cells[3]
        kinds[kind] += 1
        per_file[name] += 1
        m = re.search(r"([\w./…-]+\.py)", first)
        last = full(m.group(1)) if m else None
        for tok in TOKEN.finditer(repl):
            if tok.group(1):
                last = full(tok.group(1))
            if last is None:
                problems.append(f"{name}: unresolved {tok.group(0)}")
                continue
            have = defs("HEAD", last)
            if have is None or tok.group(2) not in have:
                problems.append(f"{name}: {last}::{tok.group(2)} not a def at HEAD")
            elif (last, tok.group(2)) in deleted:
                problems.append(f"{name}: {last}::{tok.group(2)} was deleted")
            else:
                cited.add(f"{last}::{tok.group(2)}")
        if kind == "checker rule id":
            for rid in re.findall(r"`([a-z]+\.[a-z-]+)`", repl):
                if rid not in rules and not rid.endswith((".py", ".md", ".yaml")):
                    problems.append(f"{name}: rule {rid} not in --list-rules")

base_exec = {ln.strip() for ln in open(sys.argv[1], encoding="utf-8") if "::" in ln}
head_exec = {ln.strip() for ln in open(sys.argv[2], encoding="utf-8") if "::" in ln}
deleted_tests = sorted(f"{f}::{n}" for f, n in deleted if n.startswith("test"))
print("rows:", sum(kinds.values()))
print("by kind:", dict(kinds))
print("by file:", dict(per_file))
print("replacement defs cited and resolved:", len(cited))
print("deleted defs in changed test files:", len(deleted), "(test functions:", len(deleted_tests), ")")
print("exec base:", len(base_exec), "head:", len(head_exec),
      "removed from list:", sorted(base_exec - head_exec), "added:", sorted(head_exec - base_exec))
print("deleted test functions on the base exec list:", [t for t in deleted_tests if t in base_exec])
print("problems:", len(problems))
for p in problems:
    print("  ", p)
```

</details>
