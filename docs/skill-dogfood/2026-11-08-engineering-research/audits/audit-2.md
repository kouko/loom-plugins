# Independent domain audit 2

No substantiated functional defect found in the supplied B01–B03 artifacts and execution trajectories. This is an advisory, bounded assessment, not a global PASS or evidence of automatic routing, host installation, live Git/pytest behavior, CI success, or rendered Mermaid compatibility.

Requested model: `gpt-6.1-sol`, effort `medium`; immutable server revision unknown. Actor receipts record requested first-party OpenAI configuration but `server_confirmed_model: null`.

## Basis and boundaries

Read only the authorized auditor-input tree and audit-rubric.json. Compared frozen rubric R1–R9 against the raw skill, its resources, original prompts, frozen source/provenance, generated notes/answers, complete supplied command/file trajectories, receipts and stderr. No outside sources, prior evaluation, author predictions, root report, activation/cold-reader material, tests, installation, or delegation. Duplicate source/skill copies across cases were byte-compared and identical; shared implementation was read in full. Findings are not inferred from author's intent.

## Requirement assessment

### B01

Artifact: `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/docs/loom/research/2026-11-08-package-runner-exclusions.md`. In evidence below, `note` means this case's saved artifact, and `src/` is relative to this case's frozen `artifacts/`. Event references are JSONL line numbers, not fabricated original timestamps.

| Requirement | Verdict | Evidence |
|---|---|---|
| R1 | supported | prompt.txt:1-3; note:13-31 matches no-active-change, source-only exclusion/failure-order decision. |
| R2 | supported | note:44-84,93-105,155-176; src/scripts/run_package_tests.py:123-149,153-175; src/loom-code/scripts/repo_files.py:73-146; src/loom-code/scripts/git_exec.py:72-88. Correct union, scope, symlink guard, empty exclusion contributions, and fail-fast loop. |
| R3 | supported | note:19-36,88-105,177-181; events.jsonl:7,9,11,13,15,18,20. Reads contract/resources, connected source and definitions; no test execution; hashes identify supplied bytes rather than proving remote/deployment state. |
| R4 | supported | note:140-173: conditional retain recommendation, ignored foreign repository/Git failure/explicit-target limitations, no universal isolation claim. |
| R5 | supported | note:1-9,19-23; events.jsonl:21-22,25,27; receipt.json:44-47. Correct question-based no-change path and flat metadata; every relative target resolves in frozen artifact tree. |
| R6 | supported | note:109-136: source-defined data/order legend, E1-E5 evidence mappings, independent inventory failure contributions, generated queue versus execution, nonzero/zero branches; source runner:123-150,163-167 and repo_files:73-146 agree. Prose explicitly covers symlinks and fixed Mermaid exception. |
| R7 | supported | note:38-84,140-181 gives readable textual findings and limits; requested graph is warranted by branches. |
| R8 | supported | events.jsonl:25 readback exactly matches saved note; :27 confirms resolving paths and unchanged hashes. note:132-136 honestly reports manual graph review and no parser/render execution. No claim of syntax or runtime success. |
| R9 | supported | All command/file events inspected; events.jsonl:21-22 changes only authorized record; receipt.json:44-47 source_unchanged true and one added record. No install/test/network/delegation/publication observed. |

### B02

Artifact: `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/docs/loom/research/2026-11-08-package-test-roots.md`. In evidence below, `note` means this case's saved artifact, and `src/` is relative to this case's frozen `artifacts/`. Event references are JSONL line numbers, not fabricated original timestamps.

| Requirement | Verdict | Evidence |
|---|---|---|
| R1 | supported | prompt.txt:1-3; note:11-17: exact root/local exclusion question with supplied revision and no active change. |
| R2 | supported | note:21-24; src/scripts/run_package_tests.py:53,76-113,124-137,168-175. Exact four roots and direct root/local exclusion; explicit-argument mode correctly bounded. |
| R3 | supported | note:15-26,34; events.jsonl:7,9,11,13. Static runner/test inspection and actual read-only hashes; definitions are explicitly not run. Not reading Git helpers is proportionate to this question. |
| R4 | supported | note:28-34: placing ordinary-suite tests outside excluded local directory and adding a new standalone root follows TEST_ROOTS and code_roots source; no CI/deployment claim. |
| R5 | supported | note:1-9,13; events.jsonl:14-15,17; receipt.json:44-47. Correct no-change record path, flat metadata, creation date; all three relative links resolve. |
| R6 | not-applicable | No graph requested or useful for the simple list/exclusion question; none emitted. |
| R7 | supported | note:11-34 is a concise source record with no structural placeholder or Mermaid. Reads one runner and supporting definitions rather than expanding research. |
| R8 | supported | events.jsonl:17 readback exactly matches frozen saved note; :13 contains hash output matching provenance. No extra renderer/parser claim. |
| R9 | supported | All command/file events inspected; only authorized record added; receipt.json:44-47 confirms unchanged source and single added file. No tests, install, network, publication or delegation. |

### B03

Artifact: `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/answer.txt`. In evidence below, `note` means this case's saved artifact, and `src/` is relative to this case's frozen `artifacts/`. Event references are JSONL line numbers, not fabricated original timestamps.

| Requirement | Verdict | Evidence |
|---|---|---|
| R1 | supported | prompt.txt:1-3; answer.txt:1,15-23,55-63: exact recorded HEAD/full-CI labeling question, explicit no-write and missing execution outputs preserved. |
| R2 | supported | answer.txt:29-36; source runner:123-167 and tests:49-101,187-197. Five groups, conditional empty groups, fail-fast behavior and references to unsupplied workflows are accurate. |
| R3 | supported | events.jsonl:7,9,11,13,16,18; answer.txt:19,23,29-36: source inspection and read-only hash comparison separated from CI outcome, remote freshness, actual commit membership and deployment. |
| R4 | supported | answer.txt:40-53: refuses unsupported CI-pass designation; missing evidence distinguished from failed CI; later run cannot recover historical outcomes. |
| R5 | supported | answer.txt:55-63 explicitly identifies unsaved record; receipt.json:44-45 confirms no added project files. No-write exception takes precedence, so saved path/metadata/readback requirements are inapplicable. |
| R6 | not-applicable | No diagram needed or emitted for insufficient historical CI evidence. |
| R7 | supported | answer.txt:25-59 has readable evidence table and specific missing evidence; no empty structural section. |
| R8 | supported | events.jsonl:13,16,18 shows source evidence inspected and hashes measured before final answer; no saved-artifact completion claim requiring readback. Renderer not applicable. |
| R9 | supported | Full supplied command trajectory is read-only; receipt.json:44-45 source_unchanged true, added_project_files []; no tests/network/install/intent/record writes. |

## Semantic and provenance checks

B01 note lines 40–42 state: “The design combines two complementary Git inventories” and “The runner stops at the first failing command; subsequent groups do not run.” Runner source line 123 constructs `foreign = sorted({p.resolve() for p in (*nested_repositories(repo), *nested_worktrees(repo))})`; lines 163–166 call each command and immediately `return code` for nonzero. Note lines 109–111 identify arrows as “source-defined data flow or execution order” and relationships as “source-supported, not measured.” Graph B/C independently feed the exclusion union, missing inventories contribute empty sets, pytest ignores and shell filtering feed command construction, then execution branches into immediate failure or continuation. These are accurate semantic relations. Symlink omission, same-repository strict descendants, fail-open queries, discovery cost, fixed Mermaid commands and explicitly targeted workflow paths are bounded in prose. Compactness does not require duplicating every prose detail as an extra diagram node.

B01 note lines 33–36 correctly describe matching hashes as snapshot identity against the supplied manifest, “not the original repository or remote freshness.” Event line 20 actually prints nine `MATCH` results. Note lines 134–136 report: “No Mermaid parser or renderer was run; rendering remains unverified.” The command trajectory contains no parser call; this is an honestly reported validation limitation, not a false success claim. Event line 25's complete readback equals the frozen saved record; line 27 prints eight `LINK OK` lines and confirms unchanged supplied sources/skill.

B02 note line 24 says the exclusion is “preset-specific”; source lines 168–175 forward explicit pytest argument groups without generating ignores. This avoids asserting that arbitrary pytest invocations or every directory named local is excluded. Root list matches source line 53 exactly. The short record uses no unnecessary graph or structural placeholder. Event line 17's complete readback equals the frozen record; its three relative references resolve. Event line 11 exits 2 because `rg --files docs` encounters an absent docs directory; the actual runner/test content remains present, the actor re-reads relevant source at event line 13, and no test outcome is inferred from that exit.

B03 answer line 29 explicitly bounds hash checks: “This verifies snapshot consistency, not independent commit membership or CI success.” Answer line 44 states: “This is an evidence limitation, not evidence that CI failed.” Lines 48–53 request scope and results tied to the actual revision rather than substituting source or a later run for historical CI. Source tests lines 187–197 merely read three workflow paths and assert command text; they cannot prove workflow execution. Event line 18 contains the read-only hash command and four matching digest outputs. No actor file-change event appears, receipt lines 44–45 report `source_unchanged: true` and `added_project_files: []`, and answer line 59 identifies the intentionally missing saved artifact. Harness capture of the answer is not an actor breach of no-write.

## Findings and attribution

No actionable findings; the JSON `findings` array is empty. No skill gap, actor lapse or harness defect is established. R6 is not applicable for B02/B03 because no diagram is needed. R5 remains supported for B03 through the explicit no-write exception, while saved-file metadata/path/readback obligations do not apply there. Optional presentation preferences, lack of a parser run honestly disclosed, and absent runtime verification in explicitly source-only work are not promoted to defects.

## Limits

- No global passing stamp; support is limited to these three explicit-invocation isolated source-only trials.
- Requested model/provider configuration is recorded in execution receipts, but server-confirmed model is null; immutable server revision unknown.
- B01 manually reviewed Mermaid semantic relations and read back source; parser/render validation was explicitly not performed. No compatible renderer availability or display behavior is established.
- Observed behavior means the supplied filtered event trajectory and receipts, not independent live execution or recovery of historical CI.
- Source attribution to original HEAD is manifest-provided; supplied hashes and identical copies support byte consistency, not independently verified repository history or remote freshness.

## Files read

- `docs/skill-dogfood/2026-11-08-engineering-research/audit-rubric.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/answer.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/docs/loom/research/2026-11-08-package-runner-exclusions.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/provenance.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/skill/engineering-research/SKILL.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/skill/engineering-research/references/research-methods.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/skill/engineering-research/references/source-policy.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/skill/engineering-research/references/structured-relations.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/skill/engineering-research/templates/research.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/src/loom-code/scripts/git_exec.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/src/loom-code/scripts/repo_files.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/src/scripts/run_package_tests.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/artifacts/src/tests/test_run_package_tests.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/events.jsonl`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/prompt.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/receipt.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B01/stderr.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/answer.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/docs/loom/research/2026-11-08-package-test-roots.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/provenance.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/skill/engineering-research/SKILL.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/skill/engineering-research/references/research-methods.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/skill/engineering-research/references/source-policy.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/skill/engineering-research/references/structured-relations.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/skill/engineering-research/templates/research.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/src/loom-code/scripts/git_exec.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/src/loom-code/scripts/repo_files.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/src/scripts/run_package_tests.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/artifacts/src/tests/test_run_package_tests.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/events.jsonl`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/prompt.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/receipt.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B02/stderr.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/answer.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/artifacts/provenance.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/artifacts/skill/engineering-research/SKILL.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/artifacts/skill/engineering-research/references/research-methods.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/artifacts/skill/engineering-research/references/source-policy.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/artifacts/skill/engineering-research/references/structured-relations.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/artifacts/skill/engineering-research/templates/research.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/artifacts/src/loom-code/scripts/git_exec.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/artifacts/src/loom-code/scripts/repo_files.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/artifacts/src/scripts/run_package_tests.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/artifacts/src/tests/test_run_package_tests.py`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/events.jsonl`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/prompt.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/receipt.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/B03/stderr.txt`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/provenance.json`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/rubric.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/skill-contract/engineering-research/SKILL.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/skill-contract/engineering-research/references/research-methods.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/skill-contract/engineering-research/references/source-policy.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/skill-contract/engineering-research/references/structured-relations.md`
- `docs/skill-dogfood/2026-11-08-engineering-research/execution/auditor-input/skill-contract/engineering-research/templates/research.md`
