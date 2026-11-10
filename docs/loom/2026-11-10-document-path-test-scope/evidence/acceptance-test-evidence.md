# Document-path test scope — acceptance test evidence

Tried on 2026-11-10 in a clean clone at exact HEAD `45962102a4b8ab207a2164cb81ddea8d89e0f392`.

## Environment and setup

- Created with `git clone --no-hardlinks /private/tmp/loom-document-path-fix /private/tmp/loom-document-path-acceptance-clean`. `git rev-parse HEAD` printed the target above; initial `git status --porcelain` was empty. No product or dependency files were modified by this tester.
- Read README Development instructions; used the documented locked `uv run --isolated --with-requirements requirements-package-tests.lock` environment with only criterion-specific tests, as the acceptance-tester contract requires. The full inventory remains owned by finalize-review.
- Initial focused invocation failed before tests because the sandbox could not create `/Users/kouko/.cache/uv/.tmpRWjx0D`. Authorized escalated rerun using the existing cache succeeded. This is an environment restriction, not a passing test result.
- Ran README checks `python3 scripts/sync_codex_manifests.py --check --all`, `python3 scripts/check_plugin_boundaries.py loom-code`, `python3 scripts/check_plugin_boundaries.py loom-design`, and `python3 loom-code/scripts/check-skill-crossrefs.py`; all exited 0. Boundary and cross-reference checks printed OK. A live host plugin installation was not performed: this is internal test behavior, exercised directly through the real session-start hook and tracked guidance.

## 1. 正確的文件交付指引與指向目前安裝位置的執行命令可通過路徑檢查。

- Command in the clean clone: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_conversation_document_paths.py loom-code/tests/test_write_plan_station_text.py`.
- Output: `50 passed in 0.20s`, exit 0, no skips. This includes all five direct design skills, the hook-emitted guidance and two direct visualization guidance sources, and existing clause/negation boundaries.
- Independently called the delivered emitted-guidance test against the clean clone and a new temporary working directory. It invoked the actual hook, derived the expected current launcher from the clone ROOT, and passed: `PASS test_document_paths_current_launcher_accepts`.
- The hook command is checked for exactly one occurrence; only that exact command is removed before applying the personal-path prohibition to guidance. This validates installed-location behavior without changing the runtime.

## 2. 文件交付指引寫死個人路徑，或執行命令未指向目前安裝位置時，路徑檢查可拒絕錯誤內容。

- An independent temporary Python harness imported the delivered test module using importlib, adding `loom-code/scripts` to sys.path for its existing `prose_pin` import. It used unittest.mock only in memory; it did not edit the clean clone.
- For command cases it wrapped subprocess.run, invoked the actual hook, decoded additionalContext, replaced only the current launcher with `/wrong/scripts/loom-python` or appended a duplicate exact command, then called the delivered test. Each case had to raise AssertionError.
- For hardcoded context it appended `Deliver to /Users/kouko/private/output.md` to hook guidance. For direct guidance it wrapped Path.read_text and appended the same text to each selected source independently. Each delivered test had to raise AssertionError. Sources were all five design skills named in the parametrized test plus visualization SKILL.md and references/plain-language.md.
- Captured output (all exit 0):

```text
PASS test_document_paths_current_launcher_accepts
PASS test_document_paths_wrong_launcher_rejects
PASS test_document_paths_duplicate_launcher_rejects
PASS test_document_paths_hardcoded_context_rejects
PASS test_document_paths_hardcoded_visual_rejects
PASS test_document_paths_hardcoded_reference_rejects
PASS test_document_paths_hardcoded_capture-intent_rejects
PASS test_document_paths_hardcoded_write-spec_rejects
PASS test_document_paths_hardcoded_product-principles_rejects
PASS test_document_paths_hardcoded_design-system_rejects
PASS test_document_paths_hardcoded_architecture-design_rejects
```

- Harness setup first failed with ModuleNotFoundError because its initial import path incorrectly named tests instead of scripts; correcting the independent harness import path produced the results above. No reviewed source was changed.

## 3. 專案指定的隔離環境完整測試通過，略過項目與環境限制據實列明。

- Independently executed the criterion-specific command in section 1: 50 passed, no skips. This supports `works` under the acceptance-tester contract; the complete automated package suite runs before acceptance and blocks attestation on failure. It is not represented here as an independently executed full-suite result.
- Full command reserved for finalize-review: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. Neither package-tests nor finalize-review was skipped by user instruction.
- Separately read owning-agent Build output `/private/tmp/loom-path-build-suite.log`: Python groups sum to 4,157 passed / 11 skipped; shell summary was `11 PASS / 0 FAIL`; Mermaid parsed `13/13` and negative validator checks passed. The owning agent reports exit 0. This is prior Build evidence, not this tester's independent suite execution.
- Five of those skips are environmental: `loom-workflow/tests/loom-visualization/test_adversarial_probes.py:193–194` checks for Node and the nested node_modules directory before parsing. In a fresh tree the Python group precedes the suite's later npm-ci setup. Independently read this skip guard and the later npm installation output. Owning-agent rerun log `/private/tmp/loom-path-visualization-skips.log` records `253 passed in 3.03s`, replacing that group's earlier 248 passed / 5 skipped.
- The owning agent attributes the remaining six existing skips to two absent historical classifier modules, one obsolete shadowed-basename case, and three unavailable pre-migration refs. These detailed reasons are attributed, not independently reproduced here; finalize-review owns the final full-suite run and its recorded skips.
- No live host installation or full-suite rerun by the acceptance tester. No claim that all environments are covered.

## 4. npm 回報的測試依賴漏洞有來源、適用條件、影響與未確定事項的證據紀錄。

- Independently read the complete retained `evidence/npm-audit.json`, research/01-test-dependency-advisories.md, test manifest, lockfile and validate_mermaid.mjs from the clean target tree. JSON inspection returned locked versions: Mermaid 11.17.0, DOMPurify 3.4.15, KaTeX 0.16.47, jsdom 26.1.0.
- Snapshot reconciliation: three package findings (DOMPurify critical, KaTeX low, Mermaid low) contain six advisory objects: five for DOMPurify, one for KaTeX; Mermaid inherits KaTeX via a string entry. The record preserves critical severity, affected versions, primary links, conditions, impact and unresolved assumptions. No npm audit, upgrade, forced fix, exploit input or malicious payload was executed by this tester.
- Independently opened primary advisory [GHSA-cg2g-xh64-v4q7](https://github.com/advisories/GHSA-cg2g-xh64-v4q7) on 2026-11-10: critical; affected 3.4.4–3.4.16, patched 3.4.17. Its condition combines SAFE_FOR_TEMPLATES, DOM-returning mode, attached shadow-root DOM input and downstream template evaluation. These conditions support the retained bounded assessment; the validator itself reads strings, calls mermaid.parse, and prints outcomes.
- Independently opened primary advisory [GHSA-238p-pmpm-9mq7](https://github.com/advisories/GHSA-238p-pmpm-9mq7) on 2026-11-10: low; affected >=0.11.0,<0.18.2, patched 0.18.2. It requires existing prototype pollution or attacker-influenced options prototypes; browser impact requires consuming unsanitized rendered output in a page. KaTeX does not itself establish the initial pollution. This agrees with the retained assessment.
- The remaining four advisory URLs and ranges were reconciled against the snapshot and their descriptions exist in the research record; this tester did not independently reread all four primary pages. Their detailed security claims remain the research author's attributed analysis.
- Boundaries: a parse-only invocation is not proof that dependency sanitizers are unreachable. The research explicitly records reachable DOMPurify use, incompletely enumerated parsers, directive configuration, and no proof of absent prototype pollution. This tester performed document/source reconciliation and two primary advisory comparisons, not exploitability or safety testing.
- Snapshot provenance is honestly bounded: it has no embedded collection timestamp or original environment provenance; collection command/date and later Node/npm/registry observations are attributed to the owning agent. Installed ignored source anchors are not independently registry-hash validated. No dependency remediation was applied, and known vulnerable locked versions remain.

## Decisions, dismissed findings and scope

- No spec exists or is required by the confirmed intent. No UI flows need separate rows.
- Report discloses scope narrowing of the guidance assertion and preservation of vulnerable dependencies under the user's assess-only constraint. No important-or-worse dismissed findings were supplied.
- First acceptance run, not a post-fix rerun; no carried-over verdicts. No skipped-by-instruction entries were present in plan Risks or intent Constraints.
