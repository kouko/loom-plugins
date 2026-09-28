# Prose-pin stock cleanup, batch 4: short phrases and hidden pins — plan
intent: 2026-09-29-prose-pin-stock-cleanup-batch-4@9aa148d7
charter: 1.1

## Current State Evidence
- Forward: `docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/census-report.md` "Known limits" names the forms the census cannot see: literals under three words, literals inside local validator helpers, `.index()` lookups and sentence regexes.
- Reverse: `docs/loom/evidence/mechanisms.yaml` evals name test files and functions; `check_mechanisms.py` resolves each eval to an existing test node or cold-read file.
- Error: `direct_pin_lines` in `docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py` requires three letter-bearing words and skips validator-named helpers, so `sentence-pin = 0` overstates coverage.
- Data: a crude grep at 1ef82fe8 finds ~512 short-literal `in`-asserts in 119 test files and ~309 `.index()` or `re.` calls; most check output, fields or headings.
- Boundary: versions live in 3 manifests per plugin, CHANGELOGs, READMEs and pin tests (`loom-code/tests/test_write_plan_station_text.py`, `loom-design/tests/spec/test_capture_intent_contract.py`, `loom-workflow/tests/scripts/test_release_metadata.py`); current 3.22.2, 2.6.1, 5.5.2.

## Task DAG

### Wave 0 — census widening, candidate list, eval re-pointing

**W0-01 Census sees short and hidden pins**  after: —  acceptance: 1, 5
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/test_classify_test_files.py, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-4/evidence/candidate-list.md
- Test: A1 positive: two-word-literal-against-skill-text-flagged; negative: short-literal-in-checker-output-not-flagged. A5 positive: base-1ef82fe8-exec-recount-recorded; boundary: heading-marker-field-key-classed-structural.
- Risk: agent-decided — widens direct_pin_lines to 1-2 word literals, validator helpers fed prose, .index() and regex on prose; structural tokens auto-classed; batch-3 classifier cases preserved.

**W0-02 Re-point affected evals**  after: W0-01  acceptance: 4
- Files: docs/loom/evidence/mechanisms.yaml
- Test: A4 positive: every-moved-eval-resolves-before-pruning; negative: check-mechanisms-rejects-dangling-node.
- Risk: agent-decided — at 879b189a no eval cites a candidate function; re-point only if a W1 task deletes a whole file; mechanism count unchanged.

### Wave 1 — pruning (parallel by plugin; each task writes its own mapping file)

**W1-01 loom-code and root test files**  after: W0-02  acceptance: 2, 3
- Files: loom-code/tests/test_*.py and tests/test_*.py flagged in candidate-list.md, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-4/evidence/mapping-code.md
- Test: A2 positive: behavior-and-structure-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; boundary: output-assert-left-untouched.
- Risk: agent-decided — pruned functions are renamed to what their bodies still check; names cited by mechanisms.yaml keep their name and get a docstring fix.

**W1-02 loom-design test files**  after: W0-02  acceptance: 2, 3
- Files: loom-design/tests/**/test_*.py flagged in candidate-list.md, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-4/evidence/mapping-design.md
- Test: A2 positive: behavior-and-structure-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; boundary: index-lookup-pin-judged.
- Risk: agent-decided — same pruning and rename rules as W1-01.

**W1-03 loom-workflow test files**  after: W0-02  acceptance: 2, 3
- Files: loom-workflow/tests/{goal-create,loom-visualization,decision-map,loom-memory,independent-advisor}/test_*.py flagged in candidate-list.md, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-4/evidence/mapping-workflow.md
- Test: A2 positive: behavior-and-structure-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; boundary: validator-wrapped-phrase-judged.
- Risk: agent-decided — split from W1-06 after W0-01 found 149 workflow candidates; batch-3 kept gate polarity checks and defaultPrompt stay out of scope.

**W1-04 Patch release bump**  after: —  acceptance: 6
- Files: loom-*/plugin.json, loom-*/.claude-plugin/plugin.json, loom-*/.codex-plugin/plugin.json, loom-*/CHANGELOG.md, README.md and loom-*/README*.md, loom-code/tests/test_write_plan_station_text.py, loom-design/tests/spec/test_capture_intent_contract.py, loom-workflow/tests/scripts/test_release_metadata.py
- Test: A6 positive: current-release-metadata-synchronized; negative: stale-pin-fails-before-rewrite.
- Risk: agent-decided — loom-code 3.22.3, loom-design 2.6.2, loom-workflow 5.5.3; committed in Build so the attestation covers it.

**W1-06 loom-workflow test files, second half**  after: W0-02  acceptance: 2, 3
- Files: loom-workflow/tests/{distill-sessions,handoff,recap-state,scripts}/test_*.py flagged in candidate-list.md, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-4/evidence/mapping-workflow-2.md
- Test: A2 positive: behavior-and-structure-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; boundary: compaction-output-assert-left-untouched.
- Risk: agent-decided — same pruning and rename rules as W1-01; compaction scripts' output asserts are behavior checks.

### Wave 2 — close-out

**W2-01 Census and recount**  after: W1-01, W1-02, W1-03, W1-04, W1-06  acceptance: 1, 4, 5
- Files: docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-4/evidence/census-report.md, docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-4/evidence/candidate-list.md
- Test: A1 positive: clean-worktree-census-zero-pins; negative: other-bucket-exits-1. A4 positive: check-mechanisms-all-clear; negative: dangling-eval-reported. A5 positive: recount-not-below-base; negative: deleted-function-tagged-exec-fails.
- Risk: agent-decided — every remaining flagged file has a visible override row with its reason; each moved eval is listed old -> new beside the check_mechanisms result; runs from a clean worktree.

## Simplicity check
- Drop the memory-entry task, which owns no Acceptance line and breaks the file Constraint; the lesson rides a later change — taken
- Drop mapping-evals.md; record moved evals in census-report.md — taken

## Questions asked
① — consequence — 用什麼方法找剩下的短語比對：A 擴大腳本列出所有候選逐一處理（可重算）；B 只逐檔閱讀（無法重算）；C 只做位置查找、正規表示式和檢查小工具，不做兩個字的短語 → 對，選 A
① — what — 覆述：清掉第三批腳本看不到的短語與藏起來的比對，並升三個 plugin 版號，含自動發布授權 → 對

## Risks
1. user-decided — option A: the census is widened to list every candidate of the batch-3 invisible forms; each is pruned or given a written reason, and the result is recomputable.
2. The candidate list may run to hundreds of rows; structural tokens (headings, gate markers, field keys, paths, code identifiers, rule ids) are auto-classed so manual triage covers only prose candidates.
3. Nested worktrees under .claude/worktrees skew repo-wide scans; every census and count runs from a clean git worktree.
4. Kept scans re-anchor only on existing headings or gate markers; no heading or marker is added to production prose.
5. The release bump is functional content; it lands in Build, before finalize-review.
