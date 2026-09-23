# Make acceptance testing lighter without losing what only it catches — plan
intent: 2026-09-23-lighter-acceptance-testing@39d26091
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/closing-review/SKILL.md:204-213` dispatches `loom-code:acceptance-tester`; `loom-code/agents/acceptance-tester.md:23-37` gives its steps — clean start, README setup, walk every line, capture evidence.
- Reverse: `loom-code/scripts/loom_checker/command_handlers/land.py:759-768` reads only the report path for `Accepted-by`; `ship/SKILL.md:223` presents the report at ③; `hooks/session-start:86` promises one line per condition.
- Error: `acceptance-tester.md:72-73` only forbids reporting the suite; `:32-33` and template `acceptance-test-report.md:25,72-73` invite named tests as evidence, so full-suite runs go unforbidden.
- Data: `acceptance-test-report.md:20-57` puts How/What/Evidence/Verdict in each block; `contract/manifest.yaml:204-219` charter lists five sections, two absent from the template.
- Boundary: `loom_checker/probes.py:183-189` refuses only programs outside `evidence/probes/`; `helpers.py:234-268` counts suffix, 755 mode or `#!`, so a plain `.md` evidence file passes.
- Boundary: `command_handlers/finalize.py:132-136` runs the package suite unless `package-tests` is skipped; `closing-review/SKILL.md:343-347` skips finalize-review entirely on a plain-words skip.

## Task DAG

### Wave 0 — the report template

**W0-01 Report becomes rows, decisions and questions; evidence moves out**  after: —  acceptance: 2, 3
- Files: `loom-code/skills/closing-review/references/acceptance-test-report.md`, `loom-code/scripts/test_acceptance_test_report_shape.py`
- Test: A2 positive: template-has-one-row-per-criterion-and-evidence-file-path; negative: template-row-carries-no-how-or-evidence-cell. A3 positive: row-has-carried-over-marker-with-reason; boundary: retested-row-has-no-carry-reason.
- Risk: no existing test pins template headings; new test widens coverage. Keep the data paragraph and gate-only section; evidence file `evidence/acceptance-test-evidence.md`, never `#!`; agent-decided.

### Wave 1 — the tester's contract and the station

**W1-01 Tester cites finalize-review, keeps the setup check, re-tests in full**  after: W0-01  acceptance: 1, 3, 4
- Files: `loom-code/agents/acceptance-tester.md`, `loom-code/skills/closing-review/SKILL.md`, `loom-code/scripts/test_acceptance_test_report_shape.py`
- Test: A1 positive: suite-criterion-cites-finalize-review-command; negative: no-full-suite-run-instruction. A3 positive: rerun-retests-every-named-surface; negative: partial-surface-retest-forbidden. A4 positive: rules-live-in-contract-and-template; negative: no-new-gate-marker.
- Risk: `test_simplified_station_text.py`, `test_probes_language_policy.py`, `test_review_convergence_contract.py`, `closing-review/probes/test_recovery_rules.py` pin sentences kept verbatim; coverage preserved. Skipped package-tests: run that criterion's own tests; agent-decided.

### Wave 2 — release

**W2-01 Minor release metadata 3.11.0**  after: W1-01  acceptance: 4
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/scripts/test_write_plan_station_text.py`
- Test: A4 positive: list-rules-still-26-and-versions-synchronized; negative: check-mechanisms-baseline-main-not-raised.
- Risk: `test_write_plan_station_text.py` pins 3.10.0; rewritten to 3.11.0, coverage preserved. Minor because station guidance and the tester contract change; loom-design and loom-workflow unchanged, no bump; agent-decided.

**W2-02 README version lines 3.11.0**  after: W2-01  acceptance: 4
- Files: `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `README.md`
- Test: A4 positive: four-readmes-show-3.11.0; negative: no-readme-names-3.10.0-as-current.
- Risk: root `README.md` carries the version twice (plugin table and loom-code section); both lines change. No test pins README versions today; agent-decided.

## Questions asked
① — scope — 好，先核實再開 intent
① — addition — 好，加進 intent，然後繼續跑完

## Risks
1. The report is committed before finalize-review runs, so a suite-settled row cites the suite command and finalize-review's refusal on failure, not a result; a red suite still blocks the attestation.
2. The evidence file is functional content like the report: it must be committed before reviewers read the digest, or it forces another round under the three-digest limit.
3. A carried-over verdict is only as good as its reason; the contract makes the tester check each reason against the fix diff, and any doubt means re-testing that criterion in full.
4. Pre-existing drift: the manifest charter lists "Review summary" and "Questions I asked you", which the template lacks; left unchanged here to keep the contract manifest version stable; agent-decided.
