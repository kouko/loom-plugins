# Batch 3 census and recount (W2-01)

All numbers below come from clean worktrees (`git worktree add --detach <scratchpad>/<wt> <ref>`), each removed afterwards (plan Risk 2). HEAD is this task's commit, the one that adds this report; every command was re-run from a clean worktree of it after the report was added, and nothing changed. The base is `5704cc23`.

A census run from the main checkout gives different counts (`not-prose 59, structure 65, sentence-pin 1` before this task's overrides), because nested worktrees under `.claude/worktrees` add files to the scan. Only the clean-worktree numbers below count.

## A1 — census

Command, run from the worktree root:

```
python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py
```

**Exit 0. Counts at HEAD (a clean worktree of the W4-01 commit): `{'behavior': 109, 'gate-eval': 0, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 0, 'structure': 66}`, with 23 `has_pins=yes` files. sentence-pin = 0, other = 0.**

| point | sentence-pin | gate-eval | structure | other | `has_pins=yes` files | source |
|---|---|---|---|---|---|---|
| base `5704cc23`, batch-2 classifier | 0 | 0 | 66 | 0 | 19 | batch-2 report |
| after W0-01 widened the classifier (`0001ad25` + W0-01) | 9 | 1 | 56 | 0 | 39 | `deletion-list.md` |
| after W1-01 to W1-07 and this task's overrides (`37aabc5d`) | **0** | **0** | **66** | **0** | **22** | this run |
| after W3-01 fixed the output-taint gap (the W3-01 commit) | **0** | **0** | **66** | **0** | **23** | W3-01 run, below |
| HEAD, after W4-01 pruned `VERSION_STEP` (the W4-01 commit) | **0** | **0** | **66** | **0** | **23** | W4-01 run |

**W3-01 rerun.** The build adversary found pins the census missed because their markdown read counted as program output: a helper calling `yaml.safe_load` tainted its whole return, and a skill file read from a plugin copy installed under `tmp_path` counted as a temp-dir file. W3-01 changed the detector so that only a parsed value is output, and a plain read of a skill, agent or reference path is prose even under a temp dir. The rerun from a clean worktree of the W3-01 commit, exit 0, printed `{'behavior': 109, 'gate-eval': 0, 'grammar-invariant': 2, 'not-prose': 54, 'other': 0, 'sentence-pin': 0, 'structure': 66}`. Before the prunes, the fixed detector newly flagged exactly 2 files: `loom-workflow/tests/distill-sessions/test_prompts_parseable.py` and `tests/test_loom_plugin_install_layout.py`. Both were pruned (`deletion-list.md`, "W3-01 output-taint fix round") and now carry no pin. The 23rd `has_pins=yes` file is the graduated adversary program `loom-code/tests/test_adversarial_batch3_census_misses.py` (behavior, new row). Its hit is a synthetic test source string that it feeds to the classifier, not prose.

The widened classifier also sees a direct sentence pin: a literal of three or more words asserted against text read from a skill, agent or reference markdown file, with no prose-helper import needed. Program output does not count (`deletion-list.md`, "Widened census"). So this `sentence-pin = 0` covers the direct form that batch 2's did not.

**Negative case, other-bucket-exits-1.** `main()` ends with:

```python
if counts["other"]:
    print("FAIL: files in `other` belong to no named class; add a MANUAL_OVERRIDES row")
    return 1
```

A scratch run in a throwaway worktree of HEAD, not committed, removed the `MANUAL_OVERRIDES` row of `loom-code/tests/test_adversary_recipe_skill_gate.py`, a file that falls through to `other` without it. The census then printed `other: 1`, listed that file as `other`, printed the FAIL line and **exited 1**. The worktree was removed afterwards.

**Override rows.** The intent allows a file to keep `has_pins=yes` only when the report gives that file a reason. At HEAD, 23 files show `has_pins=yes`, and each one has a visible `MANUAL_OVERRIDES` row in the classifier. That is batch 2's 19, three new ones from W2-01, and the graduated adversary program `loom-code/tests/test_adversarial_batch3_census_misses.py` from W3-01. W2-01 changed four rows:

- New row: `loom-code/tests/test_architecture_doc_consumers.py`. What is left is the `ratified-by: <name> <date>` line grammar.
- New row: `loom-workflow/tests/decision-map/test_decision_map_intent_binding.py`. What is left is the Map line format `- delivery-intent: DA-<n> | …`.
- New row: `loom-workflow/tests/loom-visualization/test_templates.py`. What is left is a table column header. The row also records that the three `pinned_sentence_ok` polarity checks are kept on purpose (agent-decided).
- Rewritten row: `loom-workflow/tests/decision-map/test_skill_doc.py`. Its batch-2 reason said the direct sentence asserts were left for batch 3. W1-01 and W1-07 pruned them, so the row now says what is left.

W3-01 added one row: `loom-code/tests/test_adversarial_batch3_census_misses.py`. Its hit is a synthetic test source string fed to the classifier.

No other override row names a file this change touched (`git diff --name-only 5704cc23...HEAD`), so no other row's text was re-judged.

The reason below is the override text exactly as the census prints it. The only change is that a `|` inside a reason is escaped as `\|` so the table still renders.

| file | auto class | class after override | override reason |
|---|---|---|---|
| `loom-code/tests/test_acceptance_test_report_shape.py` | grammar-invariant | structure | template table columns, rows and markers, the evidence block heading, the template path pointer in the tester contract, a full-suite absence scan fed by split_sentences, no gate marker, and the evidence path pointer outside every gate block; the two station phrases it once looped over were pruned in the batch-2 loop-form fix, so no sentence is asserted present |
| `loom-code/tests/test_adversarial_batch3_census_misses.py` | sentence-pin | behavior | runs this classifier (path-loaded) and asserts on its result; the direct-pin hit is a synthetic test source string fed to direct_pin_lines, and the residual check asserts named files carry no skill sentence, an absence |
| `loom-code/tests/test_adversary_layout.py` | behavior | behavior | loop-form hit is SHARED_HEADINGS asserted in the protocol's parsed heading list: section headings, not prose |
| `loom-code/tests/test_adversary_protocol.py` | behavior | behavior | imports MAX_PROBE_PROGRAMS from loom_checker for the case-count scan; the rest is a one-home absence scan and YAML keys of the return block; no sentence asserted present |
| `loom-code/tests/test_adversary_recipe_shape.py` | sentence-pin | structure | split_sentences feeds a duplicate-sentence check across recipe files; no prose literal is asserted |
| `loom-code/tests/test_adversary_routing.py` | behavior | behavior | runs the adversary tests in repo copies after real add, remove and reword edits; literals are a recipe's link back to the protocol, exception messages and pytest stdout; split_sentences only picks a sentence to reword; no sentence asserted present |
| `loom-code/tests/test_architecture_doc_consumers.py` | sentence-pin | structure | direct-pin hits are the `ratified-by: <name> <date>` line grammar in write-plan Step 5 and the lenses code table; the rest is the Risk line and rule id terms, lens-table row regexes, a heading-bounded N/A bullet check and the reviewer code row; the sentence asserts were pruned in batch 3 (W1-01) |
| `loom-code/tests/test_build_recovery_rules.py` | grammar-invariant | structure | one-home scans only: the build.absence-recovery gate block restates no artifact-to-station mapping, and §1-§2 repeat none of the rule; the block cites the three manifest keys (path pointers); split_sentences feeds the scan, no sentence is asserted present; RL-12 is the eval of build.absence-recovery |
| `loom-code/tests/test_closing_review_recovery_rules.py` | grammar-invariant | structure | one-home scan only: the review.absence-recovery gate block restates no artifact-to-station mapping; split_sentences feeds that scan, no sentence is asserted present; RL-04 is the eval of review.absence-recovery |
| `loom-code/tests/test_loom_publish.py` | behavior | behavior | loop-form hit is CONTEXT_HEADINGS asserted in the reason the checker's validate_contextual_pr_body returns: headings in program output |
| `loom-code/tests/test_plan_simplicity_text.py` | sentence-pin | structure | absence checks, the write-plan step's path pointer to plan-simplicity.md, and a scan that every user sentence of the step is negated (split_sentences); no sentence asserted present |
| `loom-code/tests/test_review_convergence_contract.py` | grammar-invariant | structure | gate-marker presence, heading-anchored sections, and absence or negation scans fed by split_sentences; no sentence asserted present |
| `loom-code/tests/test_ship_station_text.py` | behavior | behavior | recomputes the refusal premise from publish.py source; the rest is headings, absences and gate-region placement; no sentence asserted present |
| `loom-code/tests/test_simplified_station_text.py` | behavior | behavior | imports the checker's STEP_PLAIN_NAMES; the rest is absence and negation scans (split_sentences), summary-table rows and a manifest YAML value; no sentence asserted present |
| `loom-code/tests/test_sync_before_review_text.py` | behavior | behavior | runs sync-trunk on real repositories and asserts its stdout and the digest; the prose half is absences under the §2 heading and a count of sync-trunk; no sentence asserted present |
| `loom-workflow/tests/decision-map/test_decision_map_intent_binding.py` | behavior | behavior | direct-pin hit is the Map line format `- delivery-intent: DA-<n> \| docs/loom/intent/<change-id>.md` in map-format.md: line grammar, not prose; the rest is path and front-matter tokens, status tokens, absences, and the citation checker's scope loaded by path |
| `loom-workflow/tests/decision-map/test_skill_doc.py` | behavior | behavior | loop-form hit is DOCUMENTED_COMMANDS: command shapes, which the same test also runs (start_delivery.py excepted; test_start_delivery.py owns it). The direct sentence asserts batch 2 left were pruned in batch 3 (W1-01, W1-07); the rest is operation headings, fixed terms, re-entry and phase code tokens recomputed from the scripts, the ticket template grammar, schema_version, manifest fields, and the Codex manifest defaultPrompt sentence, kept as an interface string, not skill prose |
| `loom-workflow/tests/goal-create/test_skill_md.py` | gate-eval | structure | mode headings, reference paths resolving, the floor command shape, the session-activation gate blocks, template non-restatement and the offer-site count (its number recomputed from the sites scanned in the repo); eval of goal-create.session-activation, no sentence asserted |
| `loom-workflow/tests/loom-visualization/test_templates.py` | behavior | behavior | direct-pin hit is the client-matrix table column header 'Form in a chat reply'. The three pinned_sentence_ok polarity checks (MERMAID_PIN, TABLE_ASCII_PIN, CHAT_PROCEEDS_PIN) are kept on purpose (agent-decided): they read only sentences inside the mermaid-only-when-confirmed and obsidian-boundary `<!-- gate: -->` blocks, whose mechanisms.yaml evals (L357, L354) sit in this file, and each fails a negated sentence, so they check the rule's polarity, not only its wording |
| `loom-workflow/tests/scripts/test_loom_visualization_compaction.py` | structure | structure | loop-form hit is a list of `## ` headings in SKILL.md |
| `tests/test_agy_install_docs.py` | structure | structure | loop-form hit is agy and git command shapes in the Antigravity CLI section |
| `loom-design/tests/architecture-design/test_architecture_skill.py` | gate-eval | structure | loop-form hit is the four bold field labels of the schema's Guard failure message section (rule id, offending path, conform, change the rule and its guard): schema field labels. The rest is path pointers, the ratified-by line and commit subject shape, the re-design and re-ratify tokens, the two-word terms never required and never blocks, the SKILL.md mention of the Guard failure message section name, and a heading-bounded Step 5 scan; the direct sentence asserts (single answer, re-design procedure) were pruned in closing review round 1 |
| `loom-design/tests/interface/test_design_system_skill.py` | sentence-pin | structure | loop-form hit is the eight canonical DESIGN.md section names in the schema |

## A3 — one stitched mapping table

Sources: `mapping-known.md` (W1-01, with this task's fix), `mapping-new-code.md` (W1-03), `mapping-new-design.md` (W1-06), `mapping-new-workflow.md` (W1-05), `mapping-residual.md` (W1-07). The table keeps every row under a `file::function(s) | defect class it guarded | named replacement | kind` header. The "Kept on purpose" table in `mapping-residual.md` has a different header and lists literals that were kept, not removed, so it is not stitched. `mapping-evals.md` is summarised under A4.

**This task's fix to `mapping-known.md`.** The `test_goal_shape.py::test_defines_four_fields_budget_and_surfacing` row listed "the file-pointer rule" among what the function keeps. W1-07 later pruned that regex (`mapping-residual.md`), so the row now says the rule is review-only.

**W4-01 recount.** Closing review found rows that credited a kept test with a defect class the test does not guard. W4-01 re-read every `kept structural test` and `checker rule id` row against the named body (verdicts in `mapping-residual.md`, "W4-01"), relabelled 11 overclaiming rows to `review lens dimension`, and added one row for the `VERSION_STEP` prune.

**Rows by kind (68 total, 6 of them from W3-01 and 1 from W4-01):**

| kind | rows |
|---|---|
| review lens dimension | 50 |
| kept structural test | 16 |
| checker rule id | 2 |

| source | rows |
|---|---|
| mapping-known | 27 |
| mapping-new-code | 8 |
| mapping-new-design | 6 |
| mapping-new-workflow | 12 |
| mapping-residual | 15 |

**Replacement check.** The throwaway script `stitch_mappings.py` (text below) ran from the HEAD worktree root, with the base `--count-exec --list` output as its second argument. W3-01 and W4-01 re-ran it unchanged from a clean worktree of their commits. At the W4-01 commit it printed:

```
rows: 68
by kind: {'review lens dimension': 50, 'kept structural test': 16, 'checker rule id': 2}
deleted defs in changed test files: 43 (test functions: 41 )
deleted test functions on the base exec list: 0 []
deletion-list rows tagged exec: 2 ; of them deleted at HEAD: 0
problems: 0
```

The deleted-def count rose from 27 (25 test functions) to 43 (41) because W4-02 renamed 16 pruned test functions, and the script reads a rename as a deleted def plus a new one. No further function was deleted.

The script checks these things:

- Every `file::function` named in a replacement cell is a `def` at HEAD. A bare `::name` resolves to the last file named in that cell, else the row's own file, else the `## <path>` section heading. A bare file name resolves by basename.
- None of those names is one of the defs that `5704cc23..HEAD` deleted from the changed test files (27 defs from 24 files at W2-01; 43 defs, renames included, from 26 files at W4-01).
- Every backticked rule id in a `checker rule id` row appears in `loom_checker.py --list-rules`.

The first run reported 1 problem: `test_start_delivery.py::test_writes_no_brief_and_no_ticket_binding` did not resolve, because the script only looked among changed files. After it also looked at tracked test files, the count was 0. No mapping row changed.

<details><summary>stitch_mappings.py</summary>

```python
"""Throwaway (batch-3 W2-01 A3/A5): stitch the five batch-3 mapping files into one table and check it.

Run from a clean worktree root: python3 stitch_mappings.py <out.md> <base-exec-list.txt>
- keeps rows under a `file::function(s) | defect class it guarded | named replacement | kind` header;
  a bare `::name` in the first column resolves to the file of the enclosing `## <path>` heading;
- every `path.py::name` or `::name` token in the replacement cell (bare `::name` resolves to the
  last path named in that cell, else the row's first-column path, else the section path; a bare
  or `…/` file name resolves by basename among the changed test files) must be a def at HEAD, and
  must not be a def that BASE..HEAD deleted from a changed test file;
- every backticked rule id in a `checker rule id` row must be in `loom_checker.py --list-rules`;
- A5: no deleted test function is on the BASE `--count-exec --list` output, and no
  deletion-list row tagged `exec` names a function deleted at HEAD.
"""
import ast
import re
import subprocess
import sys
from collections import Counter

EV = "docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/"
FILES = ["mapping-known", "mapping-new-code", "mapping-new-design", "mapping-new-workflow", "mapping-residual"]
BASE = "5704cc23"


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True)


def defs(ref, path):
    r = git("show", f"{ref}:{path}")
    if r.returncode:
        return None
    return {n.name for n in ast.walk(ast.parse(r.stdout))
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


changed = git("diff", "--name-only", f"{BASE}..HEAD", "--", "loom-code/tests", "loom-workflow/tests",
              "loom-design/tests", "tests").stdout.split()
tracked = git("ls-files", "loom-code/tests", "loom-workflow/tests", "loom-design/tests", "tests").stdout.split()


def full(p):
    p = p.replace("…/", "")
    if "/" in p:
        return p
    same = [f for f in changed if f.rsplit("/", 1)[-1] == p]
    if not same:  # a replacement file this change did not touch
        same = [f for f in tracked if f.rsplit("/", 1)[-1] == p]
    return same[0] if len(same) == 1 else None


deleted = set()
for f in changed:
    b, h = defs(BASE, f) or set(), defs("HEAD", f) or set()
    deleted |= {(f, n) for n in b - h}
rules = {ln.split("\t")[0] for ln in subprocess.run(
    [sys.executable, "loom-code/scripts/loom_checker.py", "--list-rules"],
    capture_output=True, text=True).stdout.splitlines() if ln.strip()}

TOKEN = re.compile(r"([\w./…-]+\.py)?::(\w+)")
rows, problems, kinds = [], [], Counter()
for name in FILES:
    mode, section = None, None
    for line in open(EV + name + ".md", encoding="utf-8"):
        if line.startswith("## "):
            m = re.match(r"## ([\w./-]+\.py)\s*$", line.strip())
            section = m.group(1) if m else None
        if not line.startswith("|"):
            mode = None if not line.strip() else mode
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if cells[0].startswith("file::function"):
            mode = "std" if len(cells) == 4 and "named replacement" in cells[2] else None
            continue
        if set("".join(cells)) <= set("-: ") or mode is None:
            continue
        first, defect, repl, kind = cells[0], cells[1], cells[2], cells[3]
        kinds[kind] += 1
        shown = first.replace("`::", f"`{section}::", 1) if first.startswith("`::") and section else first
        rows.append((name, shown, defect, repl, kind))
        m = re.search(r"([\w./…-]+\.py)", first)
        row_path = full(m.group(1)) if m else section
        last = row_path
        for tok in TOKEN.finditer(repl):
            if tok.group(1):
                last = full(tok.group(1))
            if last is None:
                problems.append(f"{name}: unresolved {tok.group(0)}")
                continue
            have = defs("HEAD", last)
            if have is None or tok.group(2) not in have:
                problems.append(f"{name}: {last}::{tok.group(2)} not a def at HEAD")
            if (last, tok.group(2)) in deleted:
                problems.append(f"{name}: {last}::{tok.group(2)} was deleted")
        if kind == "checker rule id":
            for rid in re.findall(r"`([a-z]+\.[a-z-]+)`", repl):
                if rid not in rules and not rid.endswith((".py", ".md", ".yaml")):
                    problems.append(f"{name}: rule {rid} not in --list-rules")

# A5 negatives
base_exec = {ln.strip() for ln in open(sys.argv[2], encoding="utf-8") if "::" in ln}
deleted_tests = sorted(f"{f}::{n}" for f, n in deleted if n.startswith("test"))
exec_deleted = [t for t in deleted_tests if t in base_exec]
exec_rows = []
for line in open(EV + "deletion-list.md", encoding="utf-8"):
    cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
    if len(cells) == 4 and cells[2] == "exec":
        exec_rows.append(cells[0])
exec_rows_deleted = [r for r in exec_rows
                     if any(r.strip("`").endswith("::" + n) for _, n in deleted)]

with open(sys.argv[1], "w", encoding="utf-8") as out:
    out.write("| source | file::function(s) | defect class it guarded | named replacement | kind |\n"
              "|---|---|---|---|---|\n")
    for r in rows:
        out.write("| " + " | ".join(r) + " |\n")
print("rows:", len(rows))
print("by kind:", dict(kinds.most_common()))
print("deleted defs in changed test files:", len(deleted), "(test functions:", len(deleted_tests), ")")
print("deleted test functions on the base exec list:", len(exec_deleted), exec_deleted)
print("deletion-list rows tagged exec:", len(exec_rows), "; of them deleted at HEAD:", len(exec_rows_deleted))
print("problems:", len(problems))
for p in problems:
    print("  ", p)
```

</details>

### Stitched table

| source | file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|---|
| mapping-known | `loom-workflow/tests/loom-memory/test_skill_contract.py::test_absent_store_and_empty_recall_are_normal_no_memory_results` (deleted) | an absent store or empty recall is reported as an error | skill lens, `inconsistency` (Recall's steps against its result wording) | review lens dimension |
| mapping-known | `loom-workflow/tests/loom-memory/test_skill_contract.py::test_retire_requires_explicit_user_approval_before_deleting` (deleted) | Retire deletes a lesson without the user's approval | skill lens, `omission` (a delete step with no approval input) | review lens dimension |
| mapping-known | `loom-workflow/tests/loom-memory/test_skill_contract.py::test_git_memory_boundary_is_stated` (deleted) | loom-memory and git-memory blur into one store, or one depends on the other | skill lens, `ambiguity`; `::test_no_fixed_station_mandatory_invocation` still bars station coupling | review lens dimension |
| mapping-known | `loom-workflow/tests/loom-memory/test_skill_contract.py::test_no_bare_repo_root_relative_script_path` (pruned: "on any other host" + "levels above") | a file names `${CLAUDE_PLUGIN_ROOT}` with no root for other hosts | skill lens, `omission`; the same function keeps the paragraph check that every script path carries `${CLAUDE_PLUGIN_ROOT}` | review lens dimension |
| mapping-known | `loom-workflow/tests/loom-memory/test_skill_contract.py::test_legacy_store_reported_needing_explicit_migration_without_modification` (deleted) | the skill silently migrates, reads or writes a legacy store | skill lens, `inconsistency` | review lens dimension |
| mapping-known | `loom-workflow/tests/loom-memory/test_skill_contract.py::test_record_section_routes_unfinished_item_to_intent` (deleted) | Record routes an unfinished item somewhere other than an intent | `loom-workflow/tests/loom-memory/test_skill_contract.py::test_record_section_matches_the_digest_the_cold_reader_eval_was_run_against` (any Record edit goes red and re-runs `loom-workflow/skills/loom-memory/evals/record-timing.md`); `::test_backlog_entry_routing_sentence_rejected` keeps the backlog absence | kept structural test |
| mapping-known | `loom-workflow/tests/loom-memory/test_skill_contract.py::test_the_reference_copy_still_carries_both_halves` (deleted) | `references/operations.md` drops Record's timing or scarcity half | skill lens, `inconsistency` (the reference copy against the `SKILL.md` Record section) | review lens dimension |
| mapping-known | `loom-code/tests/test_architecture_doc_consumers.py::test_write_plan_step5_reads_architecture_and_names_rule` (pruned: "Treat an unratified draft as advisory") | write-plan treats an unratified `ARCHITECTURE.md` draft as binding | skill lens, `inconsistency`; the same function keeps the `Risk line`/`rule id` terms and the `ratified-by: <name> <date>` line grammar | review lens dimension |
| mapping-known | `loom-code/tests/test_architecture_doc_consumers.py::test_absent_architecture_doc_adds_no_step` (deleted: "With no ARCHITECTURE.md, nothing changes" regex, "an implementer never changes a rule") | a missing `ARCHITECTURE.md` adds a step or blocks | checker rule `standing.warn` (a missing file prints the WARN and never blocks). The rule covers only the checker's never-block half; the "adds a step" half goes to skill lens `inconsistency` (write-plan's architecture step against the absent-file case) | checker rule id |
| mapping-known | `loom-code/tests/test_architecture_doc_consumers.py::test_code_lens_has_architecture_conformance_na_without_doc` (pruned: "Scored only for ratified rules"; the N/A lookup by the sentence "A dimension with nothing to conform to" re-anchored) | the lens scores unratified rules, or drops `N/A` for an absent doc | the same function: the lens-table row regexes and `ratified-by` grammar stay, and the `N/A` check is now re-anchored on the `## Severity and verdict` heading (some bullet there names both `` `N/A` `` and `` `ARCHITECTURE.md` ``). That guards the `N/A` half; the unratified-rules half goes to skill lens `inconsistency` | kept structural test |
| mapping-known | `loom-code/tests/test_architecture_doc_consumers.py::test_reviewer_lists_it_and_reviewer_count_unchanged` (pruned: "fails closed to two when it cannot classify the whole change") | closing-review's reviewer-count fallback changes | skill lens, `inconsistency` on closing-review; the same function keeps the reviewer `code` row check | review lens dimension |
| mapping-known | `loom-workflow/tests/decision-map/test_skill_doc.py::test_v3_contract_defines_multi_delivery_outcome_loop` (deleted) and the same three phrases in `::test_v3_public_surface_commands_templates_and_version_are_synchronized` | closing a delivery clears or completes the Map | skill lens, `inconsistency` (a close step against the Map-clear transition); no executable test drives a delivery close through to the Map-clear check | review lens dimension |
| mapping-known | `loom-workflow/tests/decision-map/test_skill_doc.py::test_v3_public_surface_commands_templates_and_version_are_synchronized` (pruned: "exactly three ticket closure types", "`grilling`, `research`, and `prototype`", "one outcome-advancing slice", "source of truth", and the route sentences "`destination` is exactly …", "`text` is non-empty after trimming", "only a `ticket` route may carry", "`grilling`, `research`, or `prototype`", "`(destination, text, ticket_slug)` is unique") | the documented ticket types and route rules drift from the code | the same function keeps the `ticket_template` grammar (`type: <grilling\|research\|prototype>`), the route-field names, the slug regex and `unique \`ticket_slug\``, and runs the documented commands. That guards the ticket types; the route rules beyond the field names (the destination set, non-empty text, ticket-only fields) go to skill lens `inconsistency` | kept structural test |
| mapping-known | same function (re-entry and phase sentences, not on the W0-01 list, found by reading) | the documented re-entry states and legacy phases drift from `_implemented_reentry_states()` / `_implemented_delivery_phases()` | the same function now asserts each implemented value appears as a code token in `SKILL.md` and `map-format.md` | kept structural test |
| mapping-known | same function (risk step located by the sentence "Before every close-time gate, run the risk-front-loading pass", not on the list) | the risk pass moves after the validate command | the same function now finds the `risk-front-loading` term under the existing `## Close-time checks` heading and keeps the ordering check | kept structural test |
| mapping-known | `loom-workflow/tests/decision-map/test_skill_doc.py::test_v3_contract_pins_release_boundary_and_metric_definition` (pruned: "Exactly three ticket closure types exist", "Dependencies are graph edges, not ticket types", "A closed delivery alone is never a clear transition") | map-format restates the v3 boundary wrongly | skill lens, `inconsistency`; the same function keeps `schema_version: 3` and the `v1` absence | review lens dimension |
| mapping-known | `loom-workflow/tests/loom-visualization/test_references.py::test_affirmative_option_and_yes_no_rules_accepted`, `::test_negated_option_rule_rejected`, `::test_metaphor_ban_removed_rejected` (deleted), the `polarity_errors` line of `::test_guide_has_seven_rules_and_rewrite_steps` (pruned) | rule 3's metaphor ban or rule 5's option and yes-or-no sentences flip polarity | skill lens, `inconsistency`; `loom-workflow/tests/scripts/test_visualization_card_hook.py` keeps its own `rule_polarity_errors` scan over the card; `::test_guide_has_seven_rules_and_rewrite_steps` keeps `guide_errors` (seven rules, five steps, metaphor check last) | review lens dimension |
| mapping-known | `loom-workflow/tests/loom-visualization/test_references.py::test_option_rule_two_alternatives_and_recommendation`, `::test_yes_no_confirmation_asked_directly`, `::test_each_missed_alternative_included_or_ruled_out` (deleted) | rule 5 loses its alternatives, recommendation, yes-or-no or ruled-out clauses | `loom-workflow/tests/loom-visualization/test_references.py::test_rule_five_example_is_a_table` (rule 5's example is a Decision consequences table with a recommended row); the yes-or-no and ruled-out clauses go to skill lens `omission` | kept structural test |
| mapping-known | `loom-workflow/tests/loom-visualization/test_references.py::test_rule_five_scope_matches_card` (deleted) | the guide's rule 5 scope and the card's inline rule diverge | skill lens, `inconsistency` (guide against card) | review lens dimension |
| mapping-known | `loom-workflow/tests/loom-visualization/test_references.py::test_rewrite_opens_with_conclusion_and_keeps_facts` (pruned: `KEEP_FACTS_PHRASES`, "never what happened") | the rewrite steps stop keeping facts | skill lens, `omission`; the same function keeps the conclusion-first `guide_errors` check | review lens dimension |
| mapping-known | `loom-workflow/tests/loom-visualization/test_references.py::test_reply_keeps_user_script` (deleted) | the guide stops keeping the user's script (Traditional vs Simplified) | skill lens, `omission` | review lens dimension |
| mapping-known | `loom-workflow/tests/loom-visualization/test_references.py::test_skill_md_names_unstructured_multiline_box_failure_mode` (deleted) | `SKILL.md` stops naming the separator-less multi-line box failure | skill lens, `omission` (the failure-mode list against `references/node-structure.md`). `loom-workflow/tests/loom-visualization/test_references.py::test_skill_md_points_to_node_structure_reference` checks only that `SKILL.md` still points at `references/node-structure.md`; it does not fail when the failure mode goes unnamed | review lens dimension |
| mapping-known | `loom-workflow/tests/handoff/test_handoff_schema.py::test_resume_launcher_section_present_and_constrained` (pruned: "thin", "portable", "no stale embeds" anchors) | the launcher spec drops its three constraints | skill lens, `omission`; the same function keeps the Resume Launcher heading and `USER DIRECTIVE` field | review lens dimension |
| mapping-known | same function ("good example — resume launcher", "bad example — resume launcher") | an example goes missing | re-anchored: the same function now matches both as `###` headings | kept structural test |
| mapping-known | `loom-workflow/tests/handoff/test_handoff_schema.py::test_conversation_language_captured_and_propagated` (pruned: "reply to me in the conversation language") | the launcher stops telling the next session which language to reply in | skill lens, `omission`; the same function keeps the `conversation_language` field check | review lens dimension |
| mapping-known | `loom-workflow/tests/goal-create/test_goal_shape.py::test_defines_four_fields_budget_and_surfacing` (pruned: "must not change", "surfaced in the conversation", "runs no commands", "opens no files", "one compression pass", "not an error") | the four-field definitions or the 1,500 advisory lose their meaning | skill lens, `inconsistency`; the same function keeps field order, `goal evaluator`, the budget numbers, `advisory`, the budget-section caveat and the vendor URLs. The file-pointer rule is now review-only: W1-07 pruned its regex (`mapping-residual.md`) | review lens dimension |
| mapping-known | `tests/test_loom_skill_description_catalog.py::test_router_tables_preserve_direct_leaf_targets_and_goal_boundary` (pruned: "must be invoked by name", "Do not select `goal-create` from an inferred need or an unnamed goal request") | goal-create gets selected without being named | skill lens, `inconsistency` and `omission` (goal-create's description and the router table against the explicit-only rule). `tests/test_loom_skill_description_catalog.py::test_routing_corpus_covers_positive_boundary_and_non_trigger_cases` is only a fixture check: it checks the routing-corpus cases against each other and never reads the description or the router table | review lens dimension |
| mapping-new-code | `loom-code/tests/test_agent_model_frontmatter.py::test_module_contract_rejects_retired_dispatch_ledger_wording` (`dispatch-profile.md` "active task context only") | the dispatch profile starts keeping a persisted dispatch ledger again | skill lens, `inconsistency` (a passage that brings back a ledger against the no-ledger rule); the `review.json` and `dispatch[]` absences stay in the same function | review lens dimension |
| mapping-new-code | `loom-code/tests/test_dispatch_profile_resolver.py::test_contract_defines_the_executable_json_boundary` ("on any other host", "pass the resolver's deterministic JSON result to the host-native spawn") | the contract stops telling the caller how to find the plugin root on other hosts and to hand the resolver's JSON to the spawn | skill lens `omission` (a step whose input, the plugin root or the spawn's input, the reader must guess). The same function keeps both command shapes and the JSON event keys. `loom-code/tests/test_dispatch_profile_resolver.py::test_cli_is_deterministic_json_and_rejects_malformed_input` checks only the resolver's own JSON output; it does not fail when the contract drops either instruction | review lens dimension |
| mapping-new-code | `loom-code/tests/test_dispatch_profile_resolver.py::test_contract_defines_the_executable_json_boundary` ("post-execution capability-quality failure", "pre-execution host rejection") | the contract blurs the two escalation kinds | skill lens `ambiguity` (the contract's two escalation kinds). `loom-code/tests/test_dispatch_profile_resolver.py::test_host_rejection_is_not_capability_quality_escalation` and `::test_preexecution_host_rejection_gets_one_override_free_replacement` run the resolver on both kinds, so they guard the code's split, not the contract's wording | review lens dimension |
| mapping-new-code | `loom-code/tests/test_dispatch_profile_resolver.py::test_stations_point_to_the_executable_resolver_contract` ("on any other host it is the directory two levels above this SKILL.md") | the build and closing-review stations lose the other-host plugin-root rule | the same function keeps the `dispatch-profile.md` link and the two absences; the rule's wording is skill lens `omission` (a step whose input the reader must guess) | review lens dimension |
| mapping-new-code | `loom-code/tests/test_legacy_contract_removed.py::test_implementer_runs_focused_tests_not_the_package_suite` ("The complete package suite runs at the end of Build and again in `finalize-review`, never per task.") | the implementer contract starts running the package suite per task | the three absence asserts stay in the same function; the wording is skill lens `inconsistency` against Build's suite step | review lens dimension |
| mapping-new-code | `loom-code/tests/test_probes_language_policy.py::test_reviewer_nitclause_absent` (reviewer.md "style is out of scope") | the docs-lint carve-out paragraph is reworded or dropped | the same function keeps the `docs-lint` presence assert and the single-paragraph compound scan; the carve-out wording is skill lens `omission` | review lens dimension |
| mapping-new-code | `loom-code/tests/test_ship_worktree_merge.py::test_ship_accepted_land_renders_absolute_worktree_in_command` ("never rely on the Bash tool's workdir") | ship lets `land` run in whatever directory the Bash tool happens to use | the same function keeps the command shape `cd '<absolute worktree root>' && python3 <loom-code>/scripts/loom_checker.py land` | kept structural test |
| mapping-new-code | `tests/test_loom_plugin_install_layout.py::test_sibling_lookup_allows_version_subdirectory` ("on any other host", "two levels above this SKILL.md", "may contain one version subdirectory", "use the newest") | the other-host lookup row stops allowing a version subdirectory, or points at the wrong directory | skill lens `inconsistency` (the lookup row against flat and versioned install layouts). `tests/test_loom_plugin_install_layout.py::test_sibling_lookup_resolves_flat_and_versioned_installs` executes a hardcoded model of the lookup; the row wording is review-only. The pruned function itself keeps the five-link count, the one-lookup count and the one Codex/Antigravity row | review lens dimension |
| mapping-new-design | `test_knowledge_triage.py::test_high_bar_shaping_criteria_present` (pruned: `"flow structure"`, `"state machine"`, `"semantic display convention"`, `"color semantic"`, `"sign convention"`, `"period definition"`) | knowledge-triage.md drops or rewords one of the shaping criteria or its worked examples | skill lens `omission`; the same function keeps the SHAPING/DEFERRABLE tier-label presence checks | review lens dimension |
| mapping-new-design | `test_knowledge_triage.py::test_shaping_supplement_present_verbatim` (deleted, with the `SHAPING_SUPPLEMENT` constant) | knowledge-triage.md drops the SHAPING-never-ships-non-blocking supplement sentence | skill lens `omission` | review lens dimension |
| mapping-new-design | `test_knowledge_triage.py::test_shaping_supplement_after_pin_never_inside` (deleted: located `SHAPING_SUPPLEMENT` by `.index()`, a pin form the detector does not see) | the supplement sentence moves before or inside the pin fence | skill lens `inconsistency` (fence-vs-supplement ordering) | review lens dimension |
| mapping-new-design | `test_knowledge_triage.py::test_tier_label_supplement_present_verbatim` (deleted, with the `TIER_LABEL_SUPPLEMENT` constant) | knowledge-triage.md drops the literal-SHAPING/DEFERRABLE-label-on-every-open-question supplement sentence | skill lens `omission` | review lens dimension |
| mapping-new-design | `test_knowledge_triage.py::test_tier_label_supplement_after_first_supplement` (deleted: located both supplements by `.index()`, a pin form the detector does not see) | the tier-label supplement moves before the SHAPING supplement | skill lens `inconsistency` (supplement ordering) | review lens dimension |
| mapping-new-design | `test_principles_ratified_line.py::test_interview_template_referenced_not_copied` (pruned: `"the interview is the same one"`) | PRINCIPLES SKILL.md stops saying the interview it points to is the very one it references, and starts copying its content in | skill lens `omission`; the same function keeps the `contract/templates/PRINCIPLES-interview.md` path-pointer check | review lens dimension |
| mapping-new-workflow | `loom-workflow/tests/decision-map/test_decision_map_intent_binding.py::test_delivery_state_derives_from_the_intent_status` ("Delivery state is derived from the intent's own `status:` field", "The Map is read-only on intents") | the Map starts keeping its own delivery state or writing to intents | skill lens `inconsistency` (a Map step that stores delivery state or edits an intent, against the derived-state rule). The pruned function itself keeps the four status tokens and `retired — <reason>`. `loom-workflow/tests/decision-map/test_start_delivery.py::test_reuse_is_idempotent` guards only the script half: `start_delivery` leaves an existing intent's `status:` alone. No test fails when `SKILL.md` tells the model to keep its own state | review lens dimension |
| mapping-new-workflow | `…/test_decision_map_intent_binding.py::test_map_lists_the_change_id_under_its_criterion` ("opens no second arc", "replacement intent") | a criterion opens a second delivery arc for one intent | `loom-workflow/tests/decision-map/test_start_delivery.py::test_refuses_a_second_criterion_reusing_one_intent` and `::test_reuse_is_idempotent` run the script. The same function keeps the `- delivery-intent:` line shape | kept structural test |
| mapping-new-workflow | `…/test_decision_map_intent_binding.py::test_no_delivery_ticket_is_authored_any_more` ("Exactly three ticket closure types exist") | a delivery closure type comes back | the `\|delivery>` absence stays in the same function, and `test_start_delivery.py::test_writes_no_brief_and_no_ticket_binding` runs the script | kept structural test |
| mapping-new-workflow | `loom-workflow/tests/git-memory/test_loom_delegation.py::test_loom_closeout_delegation_does_not_reconfirm_authorized_publish` (the regex `does not re-confirm`, "initiating request", "privacy gate PASS", "Privacy BLOCK remains a required human stop", "Otherwise", "git-memory never re-confirms a Loom publication", "canonical intent authorization or a single legacy Ship decision", "Do not create a `## Memory` top-level section", the regex `independent non-Loom caller … must confirm`, "direct git-memory invocation") | a delegated close-out asks again for consent it already has, or a direct call stops asking | the same function keeps the delegated heading, its order before the direct-call heading, and the heading's absence from `compose-pr.md`. The wording is skill lens `inconsistency`, where the delegated path and the direct path would disagree. The Memory heading ban is also checker rule `push.contextual-body` | review lens dimension |
| mapping-new-workflow | `…/test_loom_delegation.py::test_privacy_judge_only_runs_for_ambiguous_private_party_text` (the regex `public repository, PR, issue, task, or vendor identifiers`, "do not dispatch", "ambiguous private-party") | the privacy judge runs on public identifiers, or not on ambiguous private-party text | the same function keeps the `Privacy-Bypass-Reason:` trailer label. The wording is skill lens `ambiguity` | review lens dimension |
| mapping-new-workflow | `…/test_loom_delegation.py::test_bypass_never_applies_to_deterministic_secret_findings` ("never bypasses a layer-1 secret finding") | a bypass trailer silences a real secret finding | skill lens `inconsistency` (the bypass rule against the layer-1 secret stop). The pruned function itself keeps the trailer label in both protocols. `loom-workflow/tests/git-memory/test_privacy_scan.py::test_planted_aws_key_exits_3_with_finding` and its sibling planted-secret tests run only the scanner, which never reads a trailer, so they do not fail when a protocol lets the trailer bypass a finding | review lens dimension |
| mapping-new-workflow | `loom-workflow/tests/loom-visualization/test_skill_script_paths.py::test_skill_dir_phrase_defined_and_used_for_every_script_call` ("`<skill-dir>` is this skill's folder", "`${CLAUDE_SKILL_DIR}` on Claude Code", "on any other host, the directory that holds this SKILL.md") | a skill uses `<skill-dir>` without saying what it resolves to on each host | the same function keeps the `<skill-dir>/scripts/` call regex. `::test_bare_scripts_path_left_in_skill_doc` and `::test_every_skill_dir_script_reference_exists` check the paths. The definition wording is skill lens `omission`, a term used but never defined | review lens dimension |
| mapping-new-workflow | `…/test_skill_script_paths.py::test_non_skill_docs_using_the_token_point_to_skill_md` (deleted; "defined in `SKILL.md`") | a reference uses `<skill-dir>` without pointing back to its definition | `::test_every_skill_dir_script_reference_exists` still resolves every token path. The pointer wording is skill lens `omission` | review lens dimension |
| mapping-new-workflow | `loom-workflow/tests/loom-visualization/test_templates.py::test_shaped_content_defaults_to_a_markdown_table` (`pinned_sentence_ok(…, *TABLE_DEFAULT_PIN)`), plus the orphans this made: `TABLE_DEFAULT_PIN`, `::test_table_default_pin_affirmative_example_accepted`, `::test_table_default_pin_negated_example_rejected` (deleted) | `SKILL.md` stops making the markdown table the default form | skill lens `inconsistency` (`SKILL.md` against the client matrix). The same function keeps the client-matrix check that every row's "Form in a chat reply" cell holds a markdown table, and `::test_remote_viewer_no_longer_forces_ascii` still scans for client-driven ASCII rules; neither reads the `SKILL.md` default, so neither fails when it changes | review lens dimension |
| mapping-new-workflow | `…/test_templates.py::test_every_ascii_section_names_its_destination_condition` (deleted; "does not render markdown") | a template's ASCII section stops saying which destination it is for | `::test_eleven_shapes_each_have_table_ascii_mermaid` keeps the section structure, and `::test_remote_viewer_no_longer_forces_ascii` keeps the client-rule absence. The wording is skill lens `omission` | review lens dimension |
| mapping-new-workflow | `loom-workflow/tests/recap-state/test_seven_block_schema.py::test_l3_contract_defines_goal_grounded_natural_output` ("Support counts as known only", and the `required` needles "broader purpose only when explicitly established", "purpose is not yet aligned", "Never output `<thinking>` or `<recap>` tags", "Never expose `Block N` labels") | the L3 recap invents purpose, or leaks planning tags and block labels | the same function keeps the seven section names, the L3 template's two `###` headings, and the absence of `<thinking>`, `<recap>` and `Block ` inside the template. That guards the leak half; the invented-purpose half is skill lens `omission` | kept structural test |
| mapping-new-workflow | `loom-workflow/tests/scripts/test_visualization_card_hook.py::test_coexist_card_skip_sentence_names_the_skill` ("Skip loom-visualization for one-paragraph answers") | the skip sentence goes back to an ambiguous "Skip it" | the "Skip it" absence stays in the same function. The hook subprocess tests stay, for example `::test_enabled_toolkit_prints_coexist_card`. The wording is skill lens `ambiguity` | kept structural test |
| mapping-residual | `test_references.py::table_rule_one_errors` (used by `::test_rule_one_key_value_exception_stated` and `::test_rule_one_without_exception_fails`; pruned: "three or more attributes", "label plus one value") | table rule 1 loses its two-column key-value exception | `loom-workflow/tests/loom-visualization/test_references.py::test_rule_one_without_exception_fails`: the validator still requires the term `key-value` in rule 1, and the negative case still goes red | kept structural test |
| mapping-residual | `test_references.py::routing_errors` (used by `::test_routing_names_document_types_per_collection`) and the second half of `::test_conversation_reply_routes_to_general_only` (pruned: the sentences "a conversation-situation reply never opens a domain file" and "Read only the one file whose row matches") | a conversation reply opens a domain file, or more than one domain file gets read | `loom-workflow/tests/loom-visualization/test_references.py::test_conversation_reply_routes_to_general_only`: the first half still fails a domain row that names a conversation situation, which guards the conversation-reply half. The read-only-one-file half and the sentence's own wording go to skill lens `inconsistency` (routing sentence against the routing table) | kept structural test |
| mapping-residual | `test_references.py::test_node_structure_reference_strips_required_phrases` (pruned from `required`: "expanded into an informative phrase or removed from the diagram", "never drawn with an empty separator", "state nodes stay title-only") | node-structure drops the expand-or-delete content rule, or lets state nodes carry a body | skill lens `omission` (the content rule and the state-node rule). The same function keeps the `## Container rule / content rule` heading term (`container rule`), `diamonds` and the other structure terms, which stay while either rule is dropped | review lens dimension |
| mapping-residual | `test_references.py::in_cell_errors` (used by `::test_in_cell_visuals_and_time_axis_guidance_present`; pruned: "not possible" from the heatmap item) | the guide claims a heatmap works in plain Markdown | skill lens, `inconsistency`; `::test_removed_in_cell_section_fails` and the kept `heatmap` term still guard the item | review lens dimension |
| mapping-residual | `test_goal_shape.py::test_defines_four_fields_budget_and_surfacing` (pruned: regex `points? (at\|to) a file`; the `not because openai documents` alternative, which the looser `not … openai … documents` check in the same assert already covers) | a goal over the budget inlines detail instead of pointing at a file | skill lens, `omission`. The W1-01 row in `mapping-known.md` lists "the file-pointer rule" among what this function keeps. That rule is now review-only. | review lens dimension |
| mapping-residual | `test_goal_shape.py::test_constraints_carries_the_standing_decision_rule` (pruned: `does not pre-decide`, `run's to make`, `by default`) | Constraints stops leaving undecided choices to the run, or SESSION mode stops emitting the entry | skill lens, `omission`; the same function keeps the section anchor `## 2 — \`Constraints\``, the terms `search`/`decide`/`record`/`candidate`/`source`/`named file`, the never-ask polarity check, the `derived` tag and the `irreversible`/`outward-facing` boundary | review lens dimension |
| mapping-residual | `test_goal_shape.py::test_stop_when_is_one_bound_written_as_completion` (pruned: negation bound to `a list of`, `the condition` and `releases the run`) | Stop-when becomes a list of exit conditions, or a bare stop clause counts as the condition being met | skill lens, `inconsistency` (the §4 wording against the evaluator behaviour it describes); the same function keeps the `## 4 — \`Stop-when\`` anchor, `one`/`bound`, the report-completes co-occurrence, `failure report`, `permission`, the never-a-`Stop-when branch` polarity check and the `input-floor` pointer | review lens dimension |
| mapping-residual | `test_skill_doc.py::test_v3_public_surface_commands_templates_and_version_are_synchronized` (pruned: "machine-measured feasibility", "human evaluates" in `prototype-contract.md`) | the prototype contract stops sorting research from prototype by who judges | skill lens `ambiguity` (the routing criteria). The same function keeps the `research` and `prototype` type names and the `ticket_template` grammar `type: <grilling\|research\|prototype>`, which stay while the criteria go | review lens dimension |
| mapping-residual | `loom-workflow/tests/distill-sessions/test_prompts_parseable.py::test_failure_prompt_structure` (pruned: "never mention ground truth") | the failure prompt drops its ground-truth-blind hard constraint | skill lens, `omission`; the rule's frontmatter `hard_constraints` list still has to parse and carry its keys (`::test_both_prompt_files_have_required_sections`) | review lens dimension |
| mapping-residual | `…/test_prompts_parseable.py::test_failure_prompt_structure`, `::test_success_prompt_structure` (pruned: "no more than 3" / "max 3" / "maximum of 3") | a prompt stops capping Memory Items at 3 | skill lens, `omission` | review lens dimension |
| mapping-residual | `…/test_prompts_parseable.py::test_both_prompts_forbid_orchestrator_memory_reference` (pruned: body "never reference the orchestrator's project memory"; redundant "orchestrator's project memory" alternative) | the body stops restating the no-memory-citation rule | skill lens `inconsistency` (body against frontmatter). `loom-workflow/tests/distill-sessions/test_prompts_parseable.py::test_both_prompts_forbid_orchestrator_memory_reference` keeps the frontmatter `hard_constraints` check (`project memory`), which guards the rule itself but never reads the body | review lens dimension |
| mapping-residual | `…/test_prompts_parseable.py::test_advisory_prompt_structure` (pruned: "fenced code block", redundant) | the advisory prompt stops documenting code-block wrapping | `loom-workflow/tests/distill-sessions/test_prompts_parseable.py::test_advisory_prompt_structure`: the `code block` term in the same assert already covered every case | kept structural test |
| mapping-residual | `…/test_prompts_parseable.py::_assert_common_shape`, `::test_success_prompt_structure` (re-anchored: "How the orchestrator dispatches this prompt", "Lean Solution Path") | the dispatch section or the Lean Solution Path section disappears | the same functions, now matching the existing `## How the orchestrator dispatches this prompt` and `## Lean Solution Path output format` headings | kept structural test |
| mapping-residual | `tests/test_loom_plugin_install_layout.py::test_isolated_loom_plugins_are_standalone_and_compose_by_public_contract` (pruned: "positive" + "negative or boundary", "closing-review station once at branch end" in the installed write-plan `SKILL.md`) | write-plan stops asking for test-case pairs per Acceptance line, or stops placing closing review once at branch end | `intake.test-case-pair` recomputes the pair on every newly authored plan; the branch-end review sentence goes to skill lens `inconsistency` (write-plan against the closing-review station) | checker rule id |
| mapping-residual | `tests/test_loom_plugin_install_layout.py::test_sibling_lookup_resolves_flat_and_versioned_installs` (pruned: the `VERSION_STEP` constant, "if its parent directory is named `loom-design`", asserted with `in` against the Codex/Antigravity row) | the other-host row drops its step up out of a versioned `loom-design` directory | skill lens `inconsistency` (the lookup row against a versioned install layout). The same function keeps the `rows == 1` count of the Codex/Antigravity row; its path resolution runs a hardcoded model, not the row | review lens dimension |

## A4 — mechanism census

Command: `python3 loom-code/scripts/check_mechanisms.py`, from the HEAD worktree root.

**Exit 0, all clear.** The net mechanism count is **142**, not counting host-hygiene. That matches the base, so it did not grow. W3-01 re-ran it from a clean worktree of its commit: exit 0, all clear, 142. By kind: skill 23, checker-rule 26, hook 10 (9 in the net count), contract 64, prose-gate 20. One hook is exempt from the net count: `PostToolUse:Skill:language-anchor.py`.

**`mapping-evals.md` summary (W0-02).** One eval moved. L89 `decision-map` pointed at the whole of `test_decision_map_intent_binding.py`. It now points at `loom-workflow/tests/decision-map/test_start_delivery.py::test_creates_intent_and_lists_it_under_the_criterion`, which runs `start_delivery`. Five evals were checked and kept: L113 `loom-memory`, L50/53/56 the three routers, and L110 `critique`. L219, the visualization-card hook, was also kept, because its subprocess tests stay. Three evals name a single function in a file on the deletion list: L351, L354/L357 (`test_templates.py`) and L222. None of those functions was deleted, so they still resolve.

**Negative case, dangling-eval-reported.** A scratch run in a throwaway worktree of HEAD, not committed, changed L357's eval to `test_templates.py::test_no_such_function`. The check **exited 1** and printed:

```
RED [R4] loom-visualization.mermaid-only-when-confirmed: eval names a node loom-workflow/tests/loom-visualization/test_templates.py does not define: test_no_such_function (not defined in the file and not collected by pytest)
```

W0-02 ran the same kind of negative on L89 (`mapping-evals.md`).

## A5 — execution-test recount

Command: `python3 <HEAD wt>/docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py --count-exec <wt> --list`. It was run once with the base worktree and once with the HEAD worktree. This task did not touch the counting code.

| ref | executing test functions |
|---|---|
| base `5704cc23` | **1925** (the baseline in `deletion-list.md`) |
| `37aabc5d` (W2-01) | **1925** |
| the W3-01 commit | **1927** |
| the W4-01 commit | **1927** (same two added lines against the base list, nothing removed) |

**Positive, recount-not-below-base.** 1925 ≥ 1925 at W2-01: the two `--list` outputs are identical (`diff` exits 0), so nothing was removed and nothing was added. At W3-01, 1927 ≥ 1925. The `diff` against the base list shows only two added lines, the two test functions of the graduated `loom-code/tests/test_adversarial_batch3_census_misses.py`, which call the path-loaded classifier. Nothing was removed. W3-01 changed only the direct-pin detector, not the counting code.

**Negative, deleted-function-tagged-exec-fails.** Two checks, both from `stitch_mappings.py`:

- **Is any deleted function on the base exec list?** None. 25 test functions were deleted across 7 files: `test_references.py` 9 (plus the helpers `polarity_errors` and `_sentence_with`), `test_skill_contract.py` 6, `test_knowledge_triage.py` 4, `test_templates.py` 3, and 1 each in `test_architecture_doc_consumers.py`, `decision-map/test_skill_doc.py` and `test_skill_script_paths.py`. None of the 25 is on the base `--count-exec --list` output.
- **Was any `exec`-tagged row deleted?** No. `deletion-list.md` tags two rows `exec`, `decision-map/test_skill_doc.py::test_v3_public_surface_commands_templates_and_version_are_synchronized` and `tests/test_loom_plugin_install_layout.py::test_isolated_loom_plugins_are_standalone_and_compose_by_public_contract` (added in W3-01), and gives both the action `prune`. Both functions are still defined at HEAD and still run their programs.

## Known limits

- **Detector threshold.** A literal counts as prose only when it has three or more words that contain a letter. A two-word phrase copied from the prose, or a single term, is invisible to the census. W1-05 and W1-07 found some of these by reading, for example `"do not dispatch"`, and pruned them.
- **Phrases inside local validators.** `direct_pin_lines` skips literals inside local helpers named `*errors*`, `validate`, `check` and similar, so it does not mistake program output for prose. It also skips `.index()` lookups and sentence regexes. Phrases hidden in these forms are found by reading, not by the script. W1-06 found the `.index()` pins that way, and W1-07 found the pins inside `table_rule_one_errors`, `routing_errors`, `in_cell_errors` and a `required` tuple. `sentence-pin = 0` therefore means no pin the detector can see. It does not mean no pin exists.
- **Output taint (W3-01).** A json or yaml parse now taints only its parsed value. A helper's returned tuple is read position by position, so a body returned beside parsed frontmatter is prose. A plain read of a skill, agent or reference path is prose even under a temp dir. Two heuristic limits remain, and the `direct_pin_lines` docstring records both. A local helper whose name contains a validator word, such as `_checklist()` matching `check`, is taken as output. A variable name is judged across the whole file, so a name that holds README.md in one test and SKILL.md in another counts as non-prose everywhere.
- **Kept gate polarity checks.** `test_templates.py` keeps `pinned_sentence_ok` with `MERMAID_PIN`, `TABLE_ASCII_PIN` and `CHAT_PROCEEDS_PIN` (agent-decided). They read only sentences inside the `loom-visualization.mermaid-only-when-confirmed` and `loom-visualization.obsidian-boundary` `<!-- gate: -->` blocks. Those gates' `mechanisms.yaml` evals are in this file: L357 is `test_mermaid_gate_paragraph_present_requires_confirmed_host`, which calls the first two, and L354 is `test_skill_declines_vault_target`. Each check fails a negated sentence, as its own negative example tests show, so it guards the rule's polarity and not only its wording. A rewording of these gate sentences will still turn them red.
- **Interface string kept.** `decision-map/test_skill_doc.py` keeps `"Use decision-map to start or resume an Outcome Map v3 for this repo." in codex_interface["defaultPrompt"]`. This is a Codex manifest field that the host shows, not skill or reference prose, so it is out of scope (`mapping-residual.md`, "Kept on purpose").
