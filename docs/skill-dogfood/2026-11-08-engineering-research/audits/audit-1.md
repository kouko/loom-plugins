# Independent domain audit 1

No confirmed material defect was established in B01–B03 under the predeclared rubric. This is an advisory assessment of three recorded executions, not a global passing stamp, activation claim, runtime certification, or general skill-effectiveness claim.

Requested auditor model: `gpt-6.1-sol`, effort `medium`; immutable server revision unconfirmed. Actor receipts likewise request OpenAI `gpt-6.1-sol` medium and have `server_confirmed_model: null`.

The actual raw skill is the contract. Its SKILL.md lines 44–49 require evidence/read-back; 74–117 define retained records and no-write override; structured-relations.md lines 20–34,42–49 define relation semantics, source mapping and truthful rendering limits. No skill ambiguity or actor lapse was established for these cases.

## Requirement judgments

| Case | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|
| B01 | supported | supported | supported | supported | supported | supported | supported | supported | supported |
| B02 | supported | supported | supported | supported | supported | not-applicable | supported | supported | supported |
| B03 | supported | supported | supported | supported | supported | not-applicable | supported | supported | supported |

### B01

- **R1 — supported:** Prompt and note lines 13–31 retain exclusion/failure-order question and snapshot-only conditions.
- **R2 — supported:** runner lines 123–149; repo_files lines 73–146; git_exec lines 50–88 support the union, ignore/filter paths and empty failure contributions. Note lines 48–84 follows these implementations.
- **R3 — supported:** events.jsonl lines 13,15,18 show implementation/helper/test reads; line 20 reports nine MATCH results. Note lines 88–105 separates test definitions from execution.
- **R4 — supported:** Note lines 140–173 gives conditional retention advice and explicit fail-open/ignored clone/explicit target limits rather than isolation certification.
- **R5 — supported:** Note lines 1–9 flat metadata, lines 19–23 revision/conditions, relative links resolve inside artifacts. events lines 22,25 show add/read-back; line 27 reports all eight LINK OK.
- **R6 — supported:** Note lines 109–136 defines arrow semantics/status and E1–E5 mappings. Union/failure/filter/queue branches agree with runner 123–167 and repo_files 73–146; fixed Mermaid bypass explained at note 132–133.
- **R7 — supported:** Note lines 38–105 and 138–181 remain readable without Mermaid; diagram is explicitly requested by prompt.
- **R8 — supported:** events line 25 is actual full saved-record cat; line 27 checks links and unchanged inputs. Note 135–136: no parser or renderer ran, rendering unverified; no successful rendering claim.
- **R9 — supported:** Observed commands are reads/hash/link checks plus one authorized note add. receipt source_unchanged=true and exactly one added_project_file; no pytest, Git initialization, installation or external command observed.

### B02

- **R1 — supported:** Prompt and note lines 11–17 match single-source root/local placement question; no invented active change.
- **R2 — supported:** runner 53 supplies exact four roots; 76–113 and 124–138 implement local exclusions. Note 21–24 scopes them to family preset/direct root local subtrees and distinguishes explicit argument mode.
- **R3 — supported:** events line 11 actually outputs runner and test definitions despite final rg docs failure; line 13 rereads helpers and hashes. Note 17,23 distinguishes reading from execution.
- **R4 — supported:** Note lines 28–34 derives test placement guidance and bounds conclusion to supplied runner; no test-pass claim.
- **R5 — supported:** Note 1–9 has required flat metadata; path is date/question based with no active change. All three relative links resolve. events 15 and 17 show add and full read-back.
- **R6 — not-applicable:** No diagram requested or helpful for this short root-list question; none produced.
- **R7 — supported:** Note has concise text/evidence and no structural placeholder; raw answer lists four roots and local exclusion plainly.
- **R8 — supported:** events 17 cat output matches saved note. Hash claim in note 26 matches events 13 output. No syntax/render assertion.
- **R9 — supported:** Only source/skill/provenance reads, hashing and authorized note add observed. receipt unchanged=true; one added note; no tests/install/network/publication observed.

### B03

- **R1 — supported:** Prompt requests unsaved evidence sufficiency draft; answer begins evidence insufficient and keeps exact HEAD/snapshot scope.
- **R2 — supported:** Answer implementation claims map to runner 51–167, repo_files 73–146 and git_exec 50–88. Test references 49–101,187–197 are described as definitions, not observed results.
- **R3 — supported:** events 11 inventory/provenance, 13 source reads, 16 focused test reads,18 hashes establish inspection. Answer explicitly distinguishes hash consistency, source semantics, independent commit membership and CI results.
- **R4 — supported:** Answer states Source review completed; full CI status for the recorded HEAD remains unverified. Missing workflows/logs/results do not become failure evidence; required revision/coverage/conditions are identified.
- **R5 — supported:** Explicit no-write honored: unsaved draft with metadata and stated missing saved artifact. receipt added_project_files=[]; no file_change events.
- **R6 — not-applicable:** No diagram needed for evidence insufficiency decision and none included.
- **R7 — supported:** Findings/evidence table and missing-evidence list are understandable without a diagram or empty placeholder.
- **R8 — supported:** No saved artifact exists to read back; source reads/hash outputs actually observed. Answer does not claim a saved record, runtime pass or rendered diagram.
- **R9 — supported:** All observed commands are local listing/cat/nl/sed/shasum reads; no file mutation/tests/network/install/delegation commands. Harness answer/event persistence is distinct from actor project writes.

## Findings and semantic checks

### B01 — supported-source-semantics

**Severity:** informational; **confidence:** high.

**Prompt:** Investigate foreign-tree exclusions and earlier-group failure with a bounded diagram.

**Expected:** Follow connected implementations; preserve failure branches; distinguish source from runtime.

**Actual:** Union, symlink guard, no-Git empty contributions, pytest ignores, shell filter, fixed Mermaid exception and fail-fast execution are represented accurately in text; diagram maps critical relations to E1–E5.

**Exact artifact quote:**

> X -->|"nonzero"| R["Return immediately; later commands do not run E1"]

**Location:** `execution/B01/artifacts/docs/loom/research/2026-11-08-package-runner-exclusions.md:127; execution/B01/artifacts/src/scripts/run_package_tests.py:163–167; execution/B01/events.jsonl:13,25`.

**Advisory direction:** No corrective action established by this bounded review.

### B01 — supported-verification-boundary

**Severity:** informational; **confidence:** high.

**Prompt:** Use one compact relationship diagram for a source-only investigation.

**Expected:** Truthfully report parser/render scope separately from factual validity.

**Actual:** Saved diagram was read back; actor discloses untested rendering. No evidence a compatible local parser was available; no availability claim or successful render is made.

**Exact artifact quote:**

> No Mermaid parser or renderer was run; rendering remains
> unverified.

**Location:** `execution/B01/artifacts/docs/loom/research/2026-11-08-package-runner-exclusions.md:135–136; execution/B01/events.jsonl:25`.

**Advisory direction:** Treat display validation as unresolved, not a factual defect or successful render.

### B02 — supported-scope

**Severity:** informational; **confidence:** high.

**Prompt:** Confirm TEST_ROOTS and whether tests/local enters ordinary package suite; no diagram or tests.

**Expected:** Exact roots and accurately bounded local exclusion.

**Actual:** Four roots match source; family preset exclusion is distinguished from explicit argument forwarding. No diagram or test execution.

**Exact artifact quote:**

> The exclusion is preset-specific: the alternate explicit-argument mode forwards each group directly to pytest without adding these ignores

**Location:** `execution/B02/artifacts/docs/loom/research/2026-11-08-package-test-roots.md:24; execution/B02/artifacts/src/scripts/run_package_tests.py:53,76–113,168–175; execution/B02/events.jsonl:11,13,17`.

**Advisory direction:** No corrective action established.

### B03 — supported-no-write-and-provenance

**Severity:** informational; **confidence:** high.

**Prompt:** Assess full CI pass evidence; explicit no-write, no tests or network.

**Expected:** Reject unsupported historical CI conclusion; unsaved bounded draft only.

**Actual:** No actor file-change events or added project files; draft separates hash agreement from commit membership or CI outcome.

**Exact artifact quote:**

> This verifies snapshot consistency, not independent commit membership or CI success.

**Location:** `execution/B03/answer.txt: findings/evidence table; execution/B03/events.jsonl:18–19; execution/B03/receipt.json:added_project_files; execution/B03/artifacts/src/tests/test_run_package_tests.py:187–197`.

**Advisory direction:** No corrective action established; retain unverified CI status until real revision-bound results are available.

The B01 graph is a bounded data/execution-flow summary. A→B/C feeds the two inventories; B/C→F forms the union; failure→Z→F denotes an empty contribution, not a filesystem fallback. F→P and F→S represent distinct filters; P/S→Q represents command construction, Q→X execution, and X branches immediate failure or sequential continuation. The prose explicitly scopes fixed Mermaid commands outside the shell filter. Symlink omission, bare/no-Git behavior, unrelated/ignored clones, workflow explicit targets and uncaught launch exceptions remain in adjacent text. The graph does not separately draw every argument-validation, empty selected-queue or symlink predicate; this bounded compression does not establish a material semantic defect. Rendering remains unresolved independently of those semantics.

## Actual trajectory evidence

- B01 events.jsonl:13 outputs runner/repo_files/git_exec; :15 outputs test definitions; :20 reports nine `MATCH` values; :22 records the note add; :25 outputs the entire saved note; :27 prints eight `LINK OK` entries and `Supplied sources unchanged: True` / `Supplied skill unchanged: True`. No parser command is recorded.
- B02 events.jsonl:11 outputs provenance/runner/tests then ends `rg: docs: IO error for operation on docs: No such file or directory (os error 2)` with exit 2. This is a missing preexisting docs directory, not source-read failure: the full source output precedes it. :13 rereads helpers and prints two matching hashes. :15 records one note add and :17 prints the saved note. This failed inventory lookup is not concealed as a test success and does not undermine the conclusion.
- B03 events.jsonl:11 inventories the four-file source slice; :13 outputs implementations/tests; :16 focuses CI-reference tests; :18 prints git_exec and four matching source hashes; :19 returns the unsaved draft. No file_change events exist. receipt.json reports `added_project_files: []` and `source_unchanged: true`. Harness capture files are distinct from actor project writes.

All command records and outputs were inspected against the preserved source; large repeated outputs were compared with identical artifact bytes rather than treated as successful operations solely from exit status. There is no observed pytest, git init, source execution, install, network, publication or delegation operation in these case trajectories.

## Files actually read

Only the allowed rubric/input/case/artifact paths below were read. Copies of source, skill and provenance were read as bytes and found identical across cases; semantic review used the displayed B01 copies plus each case’s actual transcript/output and note. No report.md, protocol.md, cold-reader, activation, prior trial or other auditor material was opened.

- `docs/skill-dogfood/2026-11-08-engineering-research/audit-rubric.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/rubric.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/cases.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/provenance.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/prompt.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/answer.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/events.jsonl`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/receipt.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/artifacts/docs/loom/research/2026-11-08-package-runner-exclusions.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/artifacts/provenance.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/artifacts/skill/engineering-research/SKILL.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/artifacts/skill/engineering-research/references/research-methods.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/artifacts/skill/engineering-research/references/source-policy.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/artifacts/skill/engineering-research/references/structured-relations.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/artifacts/skill/engineering-research/templates/research.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/artifacts/src/loom-code/scripts/git_exec.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/artifacts/src/loom-code/scripts/repo_files.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/artifacts/src/scripts/run_package_tests.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B01/artifacts/src/tests/test_run_package_tests.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/prompt.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/answer.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/events.jsonl`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/receipt.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/artifacts/docs/loom/research/2026-11-08-package-test-roots.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/artifacts/provenance.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/artifacts/skill/engineering-research/SKILL.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/artifacts/skill/engineering-research/references/research-methods.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/artifacts/skill/engineering-research/references/source-policy.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/artifacts/skill/engineering-research/references/structured-relations.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/artifacts/skill/engineering-research/templates/research.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/artifacts/src/loom-code/scripts/git_exec.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/artifacts/src/loom-code/scripts/repo_files.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/artifacts/src/scripts/run_package_tests.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B02/artifacts/src/tests/test_run_package_tests.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/prompt.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/answer.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/events.jsonl`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/receipt.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/artifacts/provenance.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/artifacts/skill/engineering-research/SKILL.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/artifacts/skill/engineering-research/references/research-methods.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/artifacts/skill/engineering-research/references/source-policy.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/artifacts/skill/engineering-research/references/structured-relations.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/artifacts/skill/engineering-research/templates/research.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/artifacts/src/loom-code/scripts/git_exec.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/artifacts/src/loom-code/scripts/repo_files.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/artifacts/src/scripts/run_package_tests.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/B03/artifacts/src/tests/test_run_package_tests.py`

## Raw actor answers

### B01 answer.txt

````text
已依指定 skill 完成純來源調查，英文紀錄含一張關係圖：[研究紀錄](docs/loom/research/2026-11-08-package-runner-exclusions.md)。

- 排除集合取兩者聯集：Git opaque directory entries 涵蓋 clone／submodule，worktree list 補上被 gitignore 隱藏的同庫 linked worktree。
- 第一個命令失敗即返回，後續組不會執行。
- 建議保留互補查詢，但不能視為完整隔離保證：Git 查詢失敗、ignored clone，以及 workflow 明確指定外部目錄為 pytest target，仍有缺口或未驗證行為。

未執行 pytest、Git 初始化或安裝；提供的來源與 skill 雜湊均維持一致。
````

### B02 answer.txt

````text
`TEST_ROOTS` 列出四個目錄：`tests`、`loom-code/tests`、`loom-design/tests`、`loom-workflow/tests`。

一般 `--loom-family` package suite 會排除 `tests/local/` 的 Python 與 shell 測試；明確傳入路徑的模式不會自動套用此排除。依據是 runner 的探索與 `--ignore` 邏輯。

已儲存[英文研究紀錄](docs/loom/research/2026-11-08-package-test-roots.md)。僅檢查提供的來源，未執行測試。
````

### B03 answer.txt

````text
證據不足，不能將目前 HEAD 的完整 CI 標成已通過；適合標為「未驗證」。以下為未儲存的英文研究草稿。

---

```yaml
title: "Does the supplied HEAD snapshot establish a full CI pass?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
```

**Question and scope**

Does the supplied snapshot justify marking full CI as passed for HEAD `d5a7f0da247214bdb9c61fe90c550256432e5f76`?

This assessment uses only supplied local files. The snapshot is incomplete and does not establish deployment state. No tests, repository scripts, installations, network requests, or writes were performed.

**Method and rationale**

Bounded source inspection: read the runner, its connected Git helpers, relevant test definitions, and provenance. This establishes intended execution paths and evidence gaps without executing them. Stop once the available evidence supports the labeling decision.

**Findings and evidence**

| Finding | Evidence and verification status |
|---|---|
| The supplied files match their recorded hashes. | Read-only `shasum -a 256` checks on all four source files matched [provenance.json](provenance.json). This verifies snapshot consistency, not independent commit membership or CI success. |
| The runner defines five groups: `code`, `design`, `workflow-python`, `workflow-shell`, and `workflow-mermaid`. | Source inspection of [run_package_tests.py](src/scripts/run_package_tests.py), lines 51–150. Python and shell commands depend on discovered files; Mermaid commands include installation, validation, and a negative check. None were executed. |
| Runner success alone would require coverage context. | Lines 153–167 stop at the first nonzero command and otherwise return zero. Some groups can produce no commands when their test roots are absent. Thus a zero return cannot alone demonstrate complete coverage. No such return was observed here. |
| Discovery depends on repository context. | The runner calls `nested_repositories` and `nested_worktrees`; [repo_files.py](src/loom-code/scripts/repo_files.py), lines 73–146, obtains their inputs through [git_exec.py](src/loom-code/scripts/git_exec.py), lines 50–88. Git failures can yield no exclusions. Runtime behavior was not verified. |
| Tests define expectations, not observed passes. | [test_run_package_tests.py](src/tests/test_run_package_tests.py), lines 49–101 and 187–197, expects broader test trees and references three CI workflows plus kickoff documentation. Those artifacts are absent from this minimal snapshot. Their absence here does not establish absence in the real repository. |
| The actual full CI contract and outcomes remain unknown. | No workflow definitions, historical logs, or execution results were supplied. Provenance records matching local HEAD/origin-main values but explicitly says remote freshness was not checked. |

All source findings apply to the supplied bytes attributed by provenance to the stated commit. No runtime success is claimed.

**Decision impact**

Do not mark full CI as passed. The supported conclusion is:

> Source review completed; full CI status for the recorded HEAD remains unverified.

This is an evidence limitation, not evidence that CI failed.

**Missing evidence**

1. **Complete CI scope at the target revision:** workflow definitions, referenced scripts/configuration, dependency manifests and lockfiles, test inventory, required checks, matrices, triggers, and conditional execution rules.
2. **Results tied to the exact tested revision:** identifiable CI runs/checks showing the tested SHA, including whether a merge revision was tested instead of HEAD.
3. **Complete execution evidence:** job and step conclusions, logs and relevant reports showing required coverage actually ran and succeeded; skipped, cancelled, or allowed-to-fail work must be accounted for.
4. **Execution conditions:** runner/platform, tool and dependency versions, setup, and relevant configuration sufficient to assess applicability.

A later authorized run could establish a new result under its recorded conditions; it would not recover missing historical outcomes.

**Limitations and record status**

The investigation is concluded because the labeling decision is supported: existing evidence is insufficient. Actual CI success remains unresolved.

No active change exists. No research record or intent was created. The saved artifact is intentionally missing under the explicit no-write constraint and the skill’s no-write exception.

---

全程僅讀取工作目錄內資料；未寫檔、執行測試或連網。
````

## Limits

This review did not run tests, parse/render Mermaid, install tools, contact external services or modify source. It evaluates recorded behavior and saved notes, not unrecorded side effects or deployed code. Link file targets were checked by local path resolution; local `#L` anchors remain renderer-dependent presentation conventions. Existing creation dates were not exercised by these new-record cases.
