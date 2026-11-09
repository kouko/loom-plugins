# Independent audit 2 — masked actors

Requested model: `gpt-6.1-sol`; requested effort: `medium`. Receipts leave backend model unconfirmed. This is an independent within-contract/domain assessment, not a global pass or an arm comparison.

## Coverage observed so far

- **X001 / C02**: Builder reuse, single real import/empty-directory Mermaid call, exact three argv arrays, Git subprocess and sys.path qualifications; narrow experimental limit. Evidence: `execution/X001/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md`; actual operations/readback: `execution/X001/events.jsonl:12-30`.
- **X002 / C06**: Rejects current-HEAD CI/release approval from source and test definitions; identifies revision-linked full-run/inventory/environment/artifact evidence. Evidence: `execution/X002/artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md`; actual operations/readback: `execution/X002/events.jsonl:7-21`.
- **X003 / C03**: Separate trust-boundary and Git-failure records; traces union, ignores, shell filtering, silent None-to-empty failure, timeout omission, partial discovery; actual pytest remains untested. Evidence: `execution/X003/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md`; actual operations/readback: `execution/X003/events.jsonl:7-22`.
- **X004 / C02**: Mandatory no-execution/shared-discovery criteria; direct reuse vs CLI extension/rewrite; actual permitted probe only; Git and sys.path side effects, environment/dependency limits. Evidence: `execution/X004/artifacts/docs/loom/research/2026-11-08-package-suite-command-preview.md`; actual operations/readback: `execution/X004/events.jsonl:7-29`.
- **X005 / C03**: Both foreign-tree trust and Git failure paths addressed; no filesystem inventory fallback confused with exclusions; ignored/unrelated-tree and explicit-target limits retained. Evidence: `execution/X005/artifacts/docs/loom/research/2026-11-08-package-runner-foreign-tests.md`; actual operations/readback: `execution/X005/events.jsonl:5-18`.
- **X006 / C05**: Computes all seven old/new links; unchanged move resolves under docs/src and fails, added parent repairs paths; checks actual source lines/hashes, excerpt/full provenance, staged acceptance and rollback. Evidence: `execution/X006/artifacts/docs/loom/research/2026-11-08-research-note-migration-traceability.md`; actual operations/readback: `execution/X006/events.jsonl:9-21`.
- **X008 / C01**: Exact four TEST_ROOTS in source order, direct inspection/hash, concise 42-line templated record and short final; no framework/matrix/diagram/experiment or CI inference. Evidence: `execution/X008/artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md`; actual operations/readback: `execution/X008/events.jsonl:7-14`.

## Findings and bounded observations

No material functional defect established in the first seven completed actors. X001, X002, X003 and X008 read initial source/provenance before methods/source policy, while their raw `SKILL.md:53–56` requires those resources before evidence gathering. All subsequently read the resources. R9 records this as a literal partial, not a method-selection failure or demonstrated functional defect. No requirement for framework names, diagrams, scores or a new experiment was imposed.

Key source checks: `fixtures/src/scripts/run_package_tests.py:53` defines the exact tuple; `:116–150` constructs command lists, `:153–176` executes; `fixtures/src/loom-code/scripts/repo_files.py:73–146` can return empty exclusion lists; `fixtures/src/loom-code/scripts/git_exec.py:50–88` converts handled errors to `None`. Migration excerpt links at `fixtures/samples/migration/docs/loom/research/2026-11-08-package-runner-exclusions.md:13–19` need one additional parent from the proposed deeper directory. Test definitions are not test results.

## Limits

Raw declared contracts necessarily expose additional guidance even with masked IDs, limiting blindness. The auditor did not inspect the private arm map, other judges, labeled input history, activation/cold-reader work or reports outside the allowlist. No source edits, tests, installations or external queries were made. Additional actors will be appended only after their receipts exist.

## Additional completed actors

- **X007 / C05**: All seven old/new URLs and actual source anchor lines verified with read-only path/hash calculations (`events.jsonl:12`), with full readback/link/source checks (`:17`). The note at `artifacts/docs/loom/research/2026-11-08-research-note-migration.md:25–41,60–75` bounds provenance, consumers and rollback. No frozen-note move/copy/edit.
- **X009 / C01**: Exact four roots; concise direct factual note (`artifacts/docs/loom/research/2026-11-08-package-runner-test-roots.md:15–42`), no experiment or framework burden; source and final readback visible at `events.jsonl:7–13`.

Both show the same literal resource-read ordering partial described above, without demonstrated functional harm. Nine completed actors now covered.

## R9 evidence clarification

The literal common clause is **“Before gathering evidence, read [research methods](references/research-methods.md) and [source policy](references/source-policy.md).”** (`artifacts/skill/engineering-research/SKILL.md:53–56` for each masked actor). Step 1 (`:10–15`) separately requires premise/object/context checking. Pure inventory and revision orientation therefore are not treated as confirmed substantive evidence work.

- **X001 — partial**: Substantive source (or migration evidence excerpt) was read before required methods/source policy. Literal ordering partial; later resources were read and analysis is adequate, with no demonstrated functional harm. Initial file inventory alone is not counted as evidence gathering.
  - `execution/X001/events.jsonl:5`: `/bin/zsh -lc "pwd && rg --files -g '"'!src/**'"' -g '"'!samples/**'"' -g '"'!skill/**'"' -g '"'!provenance.json'"' -g '"'!**/.git/**'"' && cat skill/engineering-research/SKILL.md"`
  - `execution/X001/events.jsonl:12`: `/bin/zsh -lc 'nl -ba src/tests/test_run_package_tests.py'`
  - `execution/X001/events.jsonl:13`: `/bin/zsh -lc 'cat skill/engineering-research/references/research-methods.md skill/engineering-research/references/source-policy.md skill/engineering-research/templates/research.md'`
- **X002 — uncertain**: The initial pre-reference read is provenance/revision orientation only, plausibly permitted by step 1 premise/context checking. The before-evidence clause boundary is ambiguous; no confirmed substantive source analysis preceded resources, and no functional defect is inferred.
  - `execution/X002/events.jsonl:7`: `/bin/zsh -lc 'cat skill/engineering-research/SKILL.md; cat provenance.json; rg --files src samples'`
  - `execution/X002/events.jsonl:9`: `/bin/zsh -lc 'cat skill/engineering-research/references/research-methods.md skill/engineering-research/references/source-policy.md skill/engineering-research/references/evaluation-selection.md skill/engineering-research/templates/research.md'`
- **X003 — uncertain**: The initial pre-reference read is provenance/revision orientation only, plausibly permitted by step 1 premise/context checking. The before-evidence clause boundary is ambiguous; no confirmed substantive source analysis preceded resources, and no functional defect is inferred.
  - `execution/X003/events.jsonl:7`: `/bin/zsh -lc 'cat skill/engineering-research/SKILL.md; cat provenance.json'`
  - `execution/X003/events.jsonl:9`: `/bin/zsh -lc 'cat skill/engineering-research/references/research-methods.md skill/engineering-research/references/source-policy.md skill/engineering-research/references/evaluation-selection.md skill/engineering-research/templates/research.md; nl -ba src/scripts/run_package_tests.py; nl -ba src/loom-code/scripts/repo_files.py; nl -ba src/loom-code/scripts/git_exec.py'`
- **X007 — partial**: Substantive source (or migration evidence excerpt) was read before required methods/source policy. Literal ordering partial; later resources were read and analysis is adequate, with no demonstrated functional harm. Initial file inventory alone is not counted as evidence gathering.
  - `execution/X007/events.jsonl:7`: `/bin/zsh -lc 'cat skill/engineering-research/SKILL.md; cat provenance.json; cat samples/migration/provenance.json; cat samples/migration/docs/loom/research/2026-11-08-package-runner-exclusions.md'`
  - `execution/X007/events.jsonl:9`: `/bin/zsh -lc 'cat skill/engineering-research/references/research-methods.md; cat skill/engineering-research/references/source-policy.md; cat skill/engineering-research/references/evaluation-selection.md; cat skill/engineering-research/templates/research.md; rg --files src samples docs'`
- **X008 — partial**: Substantive source (or migration evidence excerpt) was read before required methods/source policy. Literal ordering partial; later resources were read and analysis is adequate, with no demonstrated functional harm. Initial file inventory alone is not counted as evidence gathering.
  - `execution/X008/events.jsonl:7`: `/bin/zsh -lc 'cat skill/engineering-research/SKILL.md && cat provenance.json && cat src/scripts/run_package_tests.py'`
  - `execution/X008/events.jsonl:10`: `/bin/zsh -lc "cat skill/engineering-research/references/research-methods.md && cat skill/engineering-research/references/source-policy.md && cat skill/engineering-research/templates/research.md && rg -n 'TEST_ROOTS|code_roots|def _shell_tests|def main|--loom-family' src/scripts/run_package_tests.py && shasum -a 256 src/scripts/run_package_tests.py && rg --files docs"`
- **X009 — partial**: Substantive source (or migration evidence excerpt) was read before required methods/source policy. Literal ordering partial; later resources were read and analysis is adequate, with no demonstrated functional harm. Initial file inventory alone is not counted as evidence gathering.
  - `execution/X009/events.jsonl:7`: `/bin/zsh -lc 'cat skill/engineering-research/SKILL.md provenance.json; cat src/scripts/run_package_tests.py'`
  - `execution/X009/events.jsonl:9`: `/bin/zsh -lc "cat skill/engineering-research/references/research-methods.md skill/engineering-research/references/source-policy.md skill/engineering-research/templates/research.md; rg --files docs; rg -n 'TEST_ROOTS|code_roots|repo / root' src/scripts/run_package_tests.py; shasum -a 256 src/scripts/run_package_tests.py"`

The JSON now records X002/X003 as uncertain, rather than the earlier provisional partial, because only provenance was read before references; this corrects the orientation/evidence distinction. The remaining partials record observable read order only, without a framework-selection or domain failure.

## Additional completed actors (11 covered)

- **X010 / C06**: `artifacts/docs/loom/research/2026-11-08-head-ci-release-evidence.md:15–19,31–52,79–95` rejects unsupported all-CI/release approval while identifying exact revision, complete inventory/workflows, observed job results and artifact identity as missing evidence. Actual operations are read-only inspection/hash/readback; resources precede source gathering (`events.jsonl:9–23`).
- **X011 / C04**: `artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:29–51` accurately retains receipt values and computes 60.551 seconds / approximately 58.7%; explicitly says “These are descriptive differences between these two runs, not an estimated treatment effect.” Unequal scope and absent quality/billing data are consequential confounders. Proposed matched-task/quality/repeat/order/cache/cost observations (`:69–80`) are adequate and were not run.

X011 reads receipts and scope summary at `events.jsonl:7` before resources at `:9`; R9 records the same literal ordering partial without a functional defect. Exact commands retained in JSON.

## Final coverage — all 12 completed actors

- **X012 / C04**: `artifacts/docs/loom/research/2026-11-08-research-workflow-timing-evidence.md:29–54,69–82` retains accurate unequal elapsed/token figures and causal/quality/cost limits, proposes appropriately matched work, independent correctness/coverage, actual charges/rework, order/cache and representative repetition. The actual operation log (`events.jsonl:7–14`) shows inspection and saved-note readback only. No model/test rerun occurred. R9 retains receipt-read-before-reference ordering partial (`:7` versus `:9`), with exact commands in JSON.

All X001–X012 are covered, two actors per frozen case. No material method-selection failure, source factual error or disproportionate operation was established in these outputs. Direct facts stayed direct, the preview experiment stayed bounded, mixed trust/resilience questions received both analyses, timing confounds were respected, Markdown migration used actual paths/anchors/provenance, and source/test presence was not turned into CI/release approval. This is not a global pass, evidence of automatic activation, a causal framework comparison, or proof of monetary/quality improvement.

R9 ordering outcome: partial observable source/evidence reads for X001/X007/X008/X009/X011/X012; uncertain premise-orientation boundary for X002/X003; supported resource sequencing for X004/X005/X006/X010. This is a bounded contract-order observation, not a demonstrated functional defect. The auditor made no changes outside these two audit files.
