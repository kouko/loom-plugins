# Test-addition value — acceptance test evidence

Tried on 2026-11-13, in a fresh clone at d158a7e16f5cdf072e9a2eada6fdeb13cf066de1.

## Setup and provenance
- Executed `git clone --no-hardlinks /private/tmp/loom-test-addition-delivery-20261113 /private/tmp/loom-value-acceptance-clean`; `git rev-parse HEAD` returned the exact tested SHA above. Read README, PRINCIPLES, supplied AGENTS, intent and plan.
- Followed README's source command discovery: `./loom-code/scripts/loom-python --ready plan --help` loaded successfully, exit 0, and explicitly reported help only. `python3 scripts/sync_codex_manifests.py --check --all` exited 0. No plugin installation or installed-host claim.
- SHA256 of the clean copy matches candidate provenance for all three guidance resources: write-plan `5e757e2bf77741858c46af59e432972cb97ec11bb17b1c94a381c85497cf371b`; implementer `2df5f4f415a4c7e6324d495a23dfe96d8c6e3b8f6b57733f10d8641ebeabf7eb`; lenses `7b0ab250aead79fa128009d0894787f329f7724c62aca2145b56d0386b222693`. Compared against `/private/tmp/loom-native-dogfood-role-runs/provenance.json` and existing fixture resources.
- Initial system Python failed with `No module named pytest`. Offline uv attempt failed creating its default cache lock (`Operation not permitted`); neither attempted test collection. Used existing project-capable interpreter without installing packages.
- Executed `/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest -q loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_test_budget_text.py loom-code/tests/test_lenses_deletion_first.py loom-code/tests/test_contract_charter.py loom-code/tests/test_probes_charter_charter.py` in the clean clone: `70 passed in 2.15s`, exit 0. Structural tests are not semantic actor evidence.
- Full suite reserved for finalize-review, not run by this witness: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. No result inferred from an in-progress coordinator run.

## 1. 已有足夠測試保障的行為，不會僅因開始新的任務或變更而被要求新增永久測試。
- Inspected actual candidate planner output and plan in `/private/tmp/loom-native-dogfood-role-runs/blind-observable-bundle/sample-7/`, and candidate implementer completed command events in `candidate-implementer-completion.valid.jsonl` (not only the committed summary).
- Planner explicitly names both existing rule-discovery owners and says `Reuse coverage; no new permanent case for prose alone`. This is an observed planning decision, not future implementation.
- Implementer command `/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m unittest -v test_cell_validation` exited 1 with two newline failures before the validator edit, then exited 0 with `Ran 1 test` / `OK`. Diff changes only `cell_validation.py`, from pipe-only rejection to pipe-and-newline rejection; existing five-variant test is unchanged. Completed commit event exits 0 at `ea000cee8003d505124fc88c79be70769b12ddae`; final status is clean. Synthetic seam only.

## 2. 新增或擴充的測試，其額外偵測的錯誤或尚未涵蓋的行為可被具體辨識。
- Sample 7 actual plan identifies carriage return missing from the character guard; distinguishes existing discovery protection from a new valid-row separator regression and requires RED before fixing.
- Read fixture intent and both charter test sources: the plan specifically addresses confounding invalid `edits_after` fixtures rather than accepting any unrelated failure as detection. Existing actor command observations record `23 passed in 1.58s`; plan/intake exited 1 and the draft retained independent-review and installed-identity blockers. No claim that the planned carriage-return test was implemented or executed.
- Result concerns the observable ability to identify incremental protection, not delivery of the synthetic follow-on task.

## 3. 對相同保障的重複測試，審查能指出重複之處及可保留的保障，而不是僅憑文字相似、覆蓋相同程式碼或測試數量要求刪除。
- Read candidate reviewer raw output `candidate-reviewer.output.txt`, command events `candidate-reviewer.jsonl`, supplied `proposed-change.md`, `boundary_cases.py`, and both actual discovery test sources. Candidate compares command, working directory, exit assertion, tab parsing and rule membership, then recommends omitting the proposed third test while retaining existing detection.
- The actor explicitly refuses deleting either existing test solely from source similarity without executed replacement evidence. Its pytest attempt exited 1 before collection: `No usable temporary directory found`; this remains a failed execution, not a pass. The successful clean-copy focused tests above verify existing cases still run, not hypothetical deletion equivalence.

## 4. 有獨立價值的錯誤重現、邊界與整合保障，不會僅為減少測試數而被移除；沒有替代證據的刪減不能被視為已維持相同保障。
- Candidate reviewer rejects removing pipe/newline cases because an always-valid implementation would pass the retained normal case. It rejects removing `(True, False, False)` and `(False, True, False)` environment cases because returning either input or always true would pass the retained positive case. Verified these counterexamples against the actual fixture functions and proposed deletion.
- This is actual reviewer decision evidence. The fixture's case lists are not executable tests; no production environment integration or runtime replacement-equivalence proof is claimed. Candidate implementation independently retained all five existing variants during observed RED/GREEN.

## Dismissed finding and limits
- Read both `blind-a-result.md` and `blind-b-result.md`, plus full sample-7 intent. Auditor A's Medium Output-quality claim assumes public CLI help; Proposed outcome explicitly says `Clarify the internal charter command description`, and needs-design says `internal validation and documentation only`. Agree with coordinator dismissal as no confirmed scope violation; the terse Problem sentence remains ambiguous. Auditor B accepted. Do not erase disagreement or call the draft finalized.
- Ancillary commit-failure/escalation narratives have no corresponding completed events. Excluded from conclusions. Actual candidate completion commit and RED/GREEN are independently visible in completed events.
- No new model CLI, network operation, permanent test or full package suite executed by this witness. Existing runs are witnessed observations against unchanged resources, not newly repeated actors. No causal advantage over baseline, lower future test count, installed-host improvement, or full station completion inferred.
