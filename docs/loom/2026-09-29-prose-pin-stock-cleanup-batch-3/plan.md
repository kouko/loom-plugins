# Prose-pin stock cleanup, batch 3, and deferred release bump — plan
intent: 2026-09-29-prose-pin-stock-cleanup-batch-3@54d68991
charter: 1.1

## Current State Evidence
- Forward: `docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/census-report.md` "Batch-3 follow-up" lists 7 files with direct sentence pins and their line numbers.
- Reverse: `docs/loom/evidence/mechanisms.yaml` evals may name functions in those files; `check_mechanisms.py` resolves each eval to an existing test node or cold-read file.
- Error: classifier `has_pins` (`classify-test-files.py:345-370`) needs a prose-helper import or the loop form, so `assert "<sentence>" in text` without a helper import is invisible and `sentence-pin = 0` overstates coverage.
- Data: a crude scan at 5704cc23 finds 54 test files with 5+ word string `in`-asserts; many compare checker or CLI output (e.g. `loom-code/tests/test_github_rules.py`), which are behavior checks.
- Boundary: version strings live in 3 manifests per plugin, CHANGELOG, 3 READMEs, root `README.md` and pin tests (`loom-code/tests/test_write_plan_station_text.py`, `loom-design/tests/spec/test_capture_intent_contract.py`, `loom-workflow/tests/scripts/test_release_metadata.py`).

## Task DAG

### Wave 0 — census widening, deletion list, eval re-pointing

**W0-01 Census sees direct sentence pins**  after: —  acceptance: 1, 5
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/test_classify_test_files.py, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/deletion-list.md
- Test: A1 positive: direct-literal-in-md-text-flagged; negative: literal-in-subprocess-output-not-flagged. A5 positive: base-5704cc23-exec-recount-recorded; boundary: short-heading-literal-not-flagged.
- Risk: agent-decided — flag multi-word literals asserted against text read from a skill, agent or reference .md; subprocess, checker and CLI output excluded; widens has_pins only, existing classifier cases preserved.

**W0-02 Re-point affected evals**  after: W0-01  acceptance: 4
- Files: docs/loom/evidence/mechanisms.yaml, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/mapping-evals.md
- Test: A4 positive: every-moved-eval-resolves-before-pruning; negative: check-mechanisms-rejects-dangling-node.
- Risk: agent-decided — evals naming a function on the deletion list move to an existing behavior or structure test or an existing cold-read record; no new cold read; mechanism count unchanged.

### Wave 1 — pruning (parallel; each task writes its own mapping file)

**W1-01 Known 7 files**  after: W0-02  acceptance: 2, 3
- Files: loom-workflow/tests/loom-memory/test_skill_contract.py, loom-workflow/tests/decision-map/test_skill_doc.py, loom-workflow/tests/loom-visualization/test_references.py, loom-workflow/tests/handoff/test_handoff_schema.py, loom-workflow/tests/goal-create/test_goal_shape.py, loom-code/tests/test_architecture_doc_consumers.py, tests/test_loom_skill_description_catalog.py, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/mapping-known.md
- Test: A2 positive: structure-and-grammar-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; negative: no-row-names-deleted-test.
- Risk: agent-decided — kept scans re-anchor only on existing headings or gate markers; catalog description-shape checks stay; polarity checks in test_references.py go unless tagged structural.

**W1-03 Newly flagged loom-code and root files**  after: W0-02  acceptance: 2, 3
- Files: loom-code/tests/test_agent_model_frontmatter.py, loom-code/tests/test_dispatch_profile_resolver.py, loom-code/tests/test_legacy_contract_removed.py, loom-code/tests/test_probes_language_policy.py, loom-code/tests/test_ship_worktree_merge.py, tests/test_loom_plugin_install_layout.py, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/mapping-new-code.md
- Test: A2 positive: behavior-and-structure-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; boundary: output-assert-left-untouched.
- Risk: agent-decided — split by plugin after W0-01 flagged 14 new files; resolver and install-layout behavior checks stay.

**W1-04 Deferred patch release bump**  after: —  acceptance: 6
- Files: loom-*/plugin.json, loom-*/.claude-plugin/plugin.json, loom-*/.codex-plugin/plugin.json, loom-*/CHANGELOG.md, README.md and loom-*/README*.md, loom-code/tests/test_write_plan_station_text.py, loom-design/tests/spec/test_capture_intent_contract.py, loom-workflow/tests/scripts/test_release_metadata.py
- Test: A6 positive: current-release-metadata-synchronized; negative: stale-pin-fails-before-rewrite.
- Risk: agent-decided — loom-code 3.22.2, loom-design 2.6.1, loom-workflow 5.5.2; CHANGELOG entries cover batches 2 and 3; committed in Build so the attestation covers it.

**W1-05 Newly flagged loom-workflow files**  after: W0-02, W1-01  acceptance: 2, 3
- Files: loom-workflow/tests/decision-map/test_decision_map_intent_binding.py, loom-workflow/tests/git-memory/test_loom_delegation.py, loom-workflow/tests/loom-visualization/test_skill_script_paths.py, loom-workflow/tests/loom-visualization/test_templates.py, loom-workflow/tests/recap-state/test_seven_block_schema.py, loom-workflow/tests/scripts/test_visualization_card_hook.py, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/mapping-new-workflow.md
- Test: A2 positive: behavior-and-structure-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; boundary: table-header-assert-gets-override.
- Risk: agent-decided — after W1-01 because both touch loom-visualization tests; misses the detector named (regex, pinned_sentence_ok) are judged per row.

**W1-06 Newly flagged loom-design files**  after: W0-02  acceptance: 2, 3
- Files: loom-design/tests/interface/test_knowledge_triage.py, loom-design/tests/principles/test_principles_ratified_line.py, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/mapping-new-design.md
- Test: A2 positive: behavior-and-structure-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; boundary: index-lookup-pin-judged.
- Risk: agent-decided — count-form and index-form sentence lookups in test_knowledge_triage.py are pins unless tagged structural.

**W1-07 Undetected residual pins in known files**  after: W1-01  acceptance: 2, 3
- Files: loom-workflow/tests/loom-visualization/test_references.py, loom-workflow/tests/goal-create/test_goal_shape.py, loom-workflow/tests/decision-map/test_skill_doc.py, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/mapping-residual.md
- Test: A2 positive: structure-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; boundary: validator-wrapped-phrase-judged.
- Risk: agent-decided — W1-01 found phrases hidden in local validators, required lists, regexes and two-word literals; Acceptance 1 covers the known files, so they are judged here, not deferred.

### Wave 2 — close-out

**W2-01 Census and recount**  after: W1-01, W1-03, W1-04, W1-05, W1-06, W1-07  acceptance: 1, 4, 5
- Files: docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/census-report.md, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/mapping-known.md
- Test: A1 positive: clean-worktree-census-zero-pins; negative: other-bucket-exits-1. A4 positive: check-mechanisms-all-clear; negative: dangling-eval-reported. A5 positive: recount-not-below-base; negative: deleted-function-tagged-exec-fails.
- Risk: agent-decided — stitches the mapping files into one table; every remaining has_pins=yes file has a visible override row with its reason; runs from a clean worktree.

### Wave 3 — adversary fix round

**W3-01 Census output-taint gap and residual pins**  after: W2-01  acceptance: 1, 2, 3
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py, loom-workflow/tests/distill-sessions/test_prompts_parseable.py, tests/test_loom_plugin_install_layout.py, loom-code/tests/test_adversarial_batch3_census_misses.py, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/probes/test_adversarial_census_misses.py, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/deletion-list.md, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/mapping-residual.md, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/census-report.md
- Test: A1 positive: yaml-helper-body-pin-flagged; negative: parsed-frontmatter-value-not-flagged. A2 positive: behavior-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; boundary: installed-copy-skill-read-counts-as-prose.
- Risk: agent-decided — only the parsed value of a helper is output; the adversary program graduates to loom-code/tests; newly flagged files are pruned here and the census rerun.

## Simplicity check
- Merge the two known-file tasks into one W1-01 with one mapping file — taken
- Split W1-03 before W0-01 runs — declined: the newly flagged file count is unknown until the widened census exists

## Questions asked
① — what — 覆述：清掉剩下直接寫死散文的測試並補升三個 plugin 版號，含自動發布授權 → B（視為同意覆述）
① — consequence — 範圍 A（只清已知 7 個檔）／B（擴大普查只抓比對 skill／reference 內容的並一起清，建議）／C（只偵測列出、清理留下一批）？ → B

## Risks
1. user-decided — scope B: the census is widened and newly found files are cleaned in this batch; the final file count is known only after W0-01.
2. Nested worktrees under .claude/worktrees skew repo-wide scans; every census and count runs from a clean git worktree.
3. Kept scans that locate paragraphs by a literal sentence re-anchor only on existing headings or gate markers; where none exists the scan is deleted and marked review-only. No heading or marker is added to production prose.
4. The release bump is functional content; it lands in Build, before finalize-review.
