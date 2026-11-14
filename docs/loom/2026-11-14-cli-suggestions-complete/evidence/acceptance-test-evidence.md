# Complete CLI advisory guidance — acceptance test evidence

Tried on 2026-11-14, in a clean copy of the project at 64b49d3.

Full tested HEAD: `64b49d3d0d2e25d10618cfc43636f9fb20d81034`; base `adcd4cbfa468b374b5f8e0b9363adf0304b53e33`.

## 1. 全部十六個子命令及其必要模式均有可核對的建議行為與驗證證據；清楚列明機器協定特例，不以僅完成盤點或任意標為不適用冒稱完成遷移。

- How I tried it: Executed all sixteen exact-help forms and exploratory argument surfaces directly through the real source entry point. Executed whole relevant public-entry modules for ordinary positive, refusal/error and special modes; the per-command matrix below identifies actual owners and protocol exceptions. No row is claimed complete from inventory alone.
- What came back: See the independently recorded run results, named tests and command captures below. This first run carries over no prior verdict.

## 2. 一般 CLI 的拒絕、錯誤及需要後續處理的結果能以統一標籤提供與原因相符的建議；尚未完成或無法確認的結果不因退出碼為零而被當成成功，未知修復保持未知，無必要後續操作時不編造建議。

- How I tried it: Real contract passed/blocked/usage results, plan/intake success and usage, reviewer success/usage, and detached delivery uncertainty were captured below. Existing temporary Git fixtures exercise fetch failure with exit zero, optional standing warnings and CI verification notices; controlled rules APIs exercise unconfirmed/exit-zero states. Existing injected internal-error tests verify unknown repair remains unknown.
- What came back: See the independently recorded run results, named tests and command captures below. This first run carries over no prior verdict.

## 3. 既有五個 JSON 命令可用一致的可選欄位取得建議；同時具有文字與 JSON 輸出的命令不維護互相矛盾的建議，原有必要欄位及既有下一步欄位保持相容。

- How I tried it: Direct runs cover all five JSON families (contract, reviewer-count, plan, intake, delivery). Existing preparation parity tests compare identical text/JSON advice; all existing keys and schema version 1 survive for four producers, while delivery retains its distinct next/state/reason/evidence/complete structure and adds an equal suggested_next alias. Checked consumer tests exercise old/missing/null/blank/non-string advice, raw numeric precision, invalid core observations and original diagnostics.
- What came back: See the independently recorded run results, named tests and command captures below. This first run carries over no prior verdict.

## 4. 建議的有無或內容不改變原判定、退出碼、審查政策或必要授權，不觸發自動執行、重試、文字備援或繞過宿主信任與結果查證。

- How I tried it: Existing public-entry and controlled external runner cases measure single execution, publication refusal before writes, delivery read-only behavior, merge reconciliation, approval/sweep tokens and unusable advice. Existing OSError/UnicodeError injection cases retain result/exit and primary outputs without replaying actions. These are fault injections, not evidence of live host trust or remote success.
- What came back: See the independently recorded run results, named tests and command captures below. This first run carries over no prior verdict.

## 5. help、進度、hook、CI、setup 輸出及清理後的工作目錄交接保持原用途與協定相容；統一建議不新增對使用者既有資料的寫入或刪除副作用。

- How I tried it: Existing tests verify exact native hook ownership bytes, host hook payloads and invalid mixed modes, escaped CI annotations and one summary write, unchanged setup content, discovery without handler execution, operation progress and literal cleanup cwd handoff. Data writes/removals observed in fixtures belong to the pre-existing underlying operations, not suggestion emission; no real user worktree was cleaned.
- What came back: See the independently recorded run results, named tests and command captures below. This first run carries over no prior verdict.

## 6. help 與流程說明符合實作，獨立 dogfood 涵蓋每個命令適用的正常、拒絕／錯誤及特殊模式；完整測試與獨立審查通過，清楚揭露模擬、未實測宿主與遠端操作的界線。

- How I tried it: Read README setup and CLI guide, then used the documented isolated uv environment with the repository lock. Ran complete selected modules rather than a full package suite. Whole-suite command for the later blocking acceptance gate is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; finalize-review executes configured full tests/probes and refuses acceptance on failure. Formal independent reviews occur after this report. No claim that those future steps have already passed.
- What came back: See the independently recorded run results, named tests and command captures below. This first run carries over no prior verdict.

## Clean setup and boundaries

- Created a new detached worktree using `git worktree add --detach /private/tmp/loom-all-acceptance-64b49d3 64b49d3d0d2e25d10618cfc43636f9fb20d81034`; initial `git status --porcelain` was empty.
- Read root README's isolated package test setup and loom-code README's checker/result/startup documentation. Loaded the actual source CLI in the documented isolated dependency environment; did not install user plugins or use conda base.
- First offline uv invocation failed before tests with cache lock creation `Operation not permitted (os error 1)`. Retained this setup boundary; the authorized sandbox escalation reused the existing offline cache successfully.
- No external model calls, unconsented live publish/merge/cleanup/admin setup, installed-host validation or efficiency claims. Real local Git and source CLI are distinguished from existing controlled git/gh/API runners and fault injection below.
- No important/fatal dismissed findings were supplied by the station. No test/product source was edited. Report files were created after direct clean-tree replay.
- Exploratory errors are retained: bare delivery ID is invalid; actual delivery grammar uses `--intent` (plus `--goal`, `--json`, `--hook`). A progress message incorrectly suggested `--change`; no such flag was executed or accepted. Corrected source replay uses `delivery --json`. Intake supports write-spec/write-plan, so exploratory build station is expected usage error. A dash-prefixed reviewer operand is accepted as a literal ID; missing operand was separately tested as a real usage error.

## Per-command and applicable mode coverage

All entries below refer to whole modules executed in this independent run, not merely inspected. Direct source captures for discovery and argument behavior follow this table. Tests that import an actual command handler exercise the public command entry with real local Git or existing controlled external fixtures; they are not installed-host tests.

| Command | Positive / negative exercised | Special modes and evidence |
|---|---|---|
| intent | `test_loom_checker_intent.py::test_complete_intent_passes`, missing frontmatter/section, wrong kind and confirmation cases | Whole intent module includes commit-message evidence; CLI help/error replay; schema/blocker diagnostics preserved. |
| intents | CLI active/delivered/indeterminate and empty-list scenarios | `test_intents_reports_one_delivered_intent_with_optional_metadata`, selected ID, unsafe remote, selected remote-default evidence in `test_loom_checker_cli.py`; real local refs. |
| intake | Preparation JSON pass/block/usage; whole `test_loom_checker_intake.py` | Notices before late error, once-only invocation, skipped artifacts and station validation in `test_preparation_json.py`; direct write-plan success. |
| push | Ordinary usage and ownership refusals; nonpublication pass | Whole native protection, hook payload, command detection and ship-worktree modules; exact native ownership, install/remove, foreign hooks unchanged, hook fail-open/refusal and mixed modes. |
| publish | Whole `test_loom_publish.py`: controlled successful publish, precise prerequisite/authorization failures | Controlled runner/poll/write counts, registration delay, pending timeout, progress and reconciliation; blocked-route adversarial module; no live remote publish. |
| delivery | Whole `test_delivery.py`: published/merged, local newer head, missing authorization/PR, failed/actionable/unavailable | Legacy/new JSON alias equality and text parity; stop-hook host cases in `test_delivery_stop.py`; direct detached uncertainty exits 1 with complete false. |
| land | Whole merge/cleanup/sweep modules: accepted operation and refusal cases | Literal cwd handoff, cleanup after observed merge, list token, changed/stale list refusal, no candidates, per-removal replan, invoking worktree excluded; temporary repos and controlled remote responses only. |
| sync-trunk | Whole `test_sync_trunk.py`: up-to-date/ahead, behind rebase/merge, conflicts, dirty/ignored data protection | Real local bare remotes; unreachable path fetch exits zero yet remains unsynced, no new commit; no extra retry/method changes introduced by advice. |
| github-rules | Whole rules module: satisfied classic/ruleset, missing protections, unreadable/unconfirmed results | Setup JSON exactness, missing template, malformed bypass, trusted host selection; local configured-server simulation, not live GitHub enforcement; advisory stream failure keeps observation. |
| pr-floor | Whole CI module: valid body and malformed heading | Absent/stale verification is notice/exit0, workflow escaping and summary writing; advice stream failure preserves one summary write; workflow module checks actual CI invocation. |
| standing | Whole standing module: existing documents and missing optional warnings, product principle refusals | Waivers silence warnings without removing product refusal; verbatim WARN lines preserved and nonblocking advice; no documents created automatically. |
| contract | Real pass 2.1, block 2.99, usage bad; preparation parity and charter manifest checks | Duplicate/final selectors, typed compatibility, producer-versus-consumer remedy, passed null, checked raw result/precision; no guessed policy. |
| charter | Whole `test_contract_charter.py`: real ordered populated table and invalid/missing manifest | stdout table remains on reported row errors, pipe/newline cell checks and `--manifest` validation; CLI argument/help capture. |
| plan | Whole field-cap and missing-file modules plus preparation cases | Direct current plan success and missing path usage; literal selector filename, field-cap refusal, returned usage (not internal), JSON/text equality; no new JSON mode. |
| reviewer-count | Direct clean source positive and missing-operand usage; preparation real floor 1/2 cases | Checked positive future floors, exact request identity, dirty/nonrepo refusal, no default floor and precision preservation in `test_checked_readonly.py`. |
| finalize-review | Whole selection/probe-confirmation modules: generated attestation and invalid evidence/dirty/usage refusals | Progress before child exits, stream failure, unchanged stdout, report verdict binding, committed identity, concern/program caps and controlled package/probe executions; does not run this repository's full package suite here. |

## Named cross-cutting evidence and UI-flow coverage

- Discovery/empty listing/success/refusal/input error/internal error: `test_loom_checker_cli.py::test_exact_help_never_dispatches_handlers`, `test_planning_checks_preserve_real_success_and_conditional_stdout`, `test_internal_failure_fails_closed_with_exit_2`; preparation JSON tests preserve original diagnostics/status and typed error.
- Optional/unusable advice: `test_checked_readonly.py::test_entry_validation_and_execution_boundary` checks accepted raw payload variants, core invalid payloads, precision, single execution and no fallback; `test_advisory_write_failure_keeps_local_fault_exit_and_single_execution` keeps original stderr diagnostic.
- Advice write failure: `test_loom_checker_cli.py::test_advice_write_failure_preserves_result_and_primary_output_errors`; `test_github_rules.py::test_unconfirmed_advice_write_failure_keeps_observation`; `test_pr_floor.py::test_advice_write_failure_preserves_ci_annotation_and_one_summary_write`.
- Zero-exit uncertainty: `test_sync_trunk.py::test_unreachable_remote_warns_exit_zero`, `test_unreachable_remote_creates_no_commit`; rules unreadable cases; standing `test_a_warn_never_blocks`; CI verification notices. These observations do not authorize setup, assert synchronization or certify completed verification.
- Delivery/publish/cleanup: `test_delivery.py::test_text_advice_matches_json_without_second_observation`, `test_unavailable_remote`; `test_land_sweep.py::test_sweep_lists_then_confirm_removes`, `test_changed_list_token_removes_nothing`; whole publish and merge modules count existing external operations.
- Protected protocols/waiting/cold startup: `test_special_protocol_modes_never_receive_dispatcher_advice`, exact native-hook tests, both host stop-hook variants, CI/setup cases, runtime isolation/help/readiness tests and finalization progress tests.
- Every retained spec UI flow is represented above: Discovery, Successful ordinary check, Empty listing, Refusal, Input/file error, Internal error, Unsynced warning, Rule uncertainty, Standing warning, Verification notice, Delivery, Publish result, Cleanup list/handoff, Optional/unusable advice, Advice stream failure, Protected protocol, Waiting/cold startup. This is engineering intent: the report keeps exactly its six Acceptance rows.

## Direct source CLI captures

All commands below used the isolated environment's Python and `loom-code/scripts/loom_checker.py` in the clean detached worktree. Help is trimmed to its heading/usage; other output is verbatim. No exploratory invalid invocation was silently converted to success.

### `intent --help`

Exit: 0

```text
stdout:
intent — check one intent's implemented rules
Usage: intent <path> [--commit-msg <file>]
Supply readable relative-to-working-directory or absolute paths. Repository
[remaining discovery help omitted]
stderr:
```

### `intent --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
no intent file at --acceptance-invalid-option
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `intents --help`

Exit: 0

```text
stdout:
intents — inspect locally derived intent delivery states
Usage: intents [<change-id>] [--remote <name>] [--metadata]
Run in the repository. The remote defaults to origin and must be a safe literal.
[remaining discovery help omitted]
stderr:
```

### `intents --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
no intent file at docs/loom/intent/--acceptance-invalid-option.md.
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `intake --help`

Exit: 0

```text
stdout:
intake — check the selected station's current prerequisites
Usage: intake <write-spec|write-plan> <change-id> [--json]
Run inside the selected repository. Supply a change-id, not a file path;
[remaining discovery help omitted]
stderr:
```

### `intake --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
intake needs a station and a change-id.
Help: "<loom-code>/scripts/loom-python" --ready intake --help (replace <loom-code> with the installed loom-code plugin directory).
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `push --help`

Exit: 0

```text
stdout:
push — provide host-hook feedback or install native branch protection
Usage: push --hook
       push --install-git-hooks
[remaining discovery help omitted]
stderr:
```

### `push --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
push expects --hook, --install-git-hooks or --remove-git-hooks.
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `publish --help`

Exit: 0

```text
stdout:
publish — publish an authorized branch and observe required CI
Usage: publish --intent <absolute-intent-path> --title <text> --body-file <absolute-body-path>
Legacy: publish --confirm-authorized --title <text> --body-file <absolute-body-path>
[remaining discovery help omitted]
stderr:
```

### `publish --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
publish: unexpected argument '--acceptance-invalid-option'
Help: "<loom-code>/scripts/loom-python" --ready publish --help (replace <loom-code> with the installed loom-code plugin directory).
Suggested next step: Inspect the original diagnostic and command help; preserve outstanding work and investigate the reported condition before deliberately rerunning.
```

### `delivery --help`

Exit: 0

```text
stdout:
delivery — observe the selected delivery goal without writes
Usage: delivery [--goal local|published|merged] [--intent <path>] [--json]
Run inside the selected repository on its identified feature branch.
[remaining discovery help omitted]
stderr:
```

### `delivery --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
delivery: unexpected or repeated argument '--acceptance-invalid-option'
Help: "<loom-code>/scripts/loom-python" --ready delivery --help (replace <loom-code> with the installed loom-code plugin directory).
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `land --help`

Exit: 0

```text
stdout:
land — merge an accepted PR or clean up merged changes
Usage: land --accepted-by <name>
       land --cleanup <branch>
[remaining discovery help omitted]
stderr:
```

### `land --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
land: unexpected argument '--acceptance-invalid-option'
Suggested next step: Inspect the original diagnostic and command help; preserve outstanding work and investigate the reported condition before deliberately rerunning.
```

### `sync-trunk --help`

Exit: 0

```text
stdout:
sync-trunk — bring a clean change branch onto fetched trunk
Usage: sync-trunk
Run on a clean attached change branch, not trunk, with trusted Git and resolvable
[remaining discovery help omitted]
stderr:
```

### `sync-trunk --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
sync-trunk takes no arguments; run it from the change worktree.
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `github-rules --help`

Exit: 0

```text
stdout:
github-rules — inspect GitHub trunk protection as advisory information
Usage: github-rules [--print-setup]
Run in the repository with origin metadata and authenticated gh read access.
[remaining discovery help omitted]
stderr:
```

### `github-rules --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
usage: loom_checker.py github-rules [--print-setup]
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `pr-floor --help`

Exit: 0

```text
stdout:
pr-floor — validate a PR body and disclose verification in CI
Usage: pr-floor --body-file <file> --base <sha> --head <sha> [--branch <name>]
Supply unique paired flags, a readable body file (relative to the working
[remaining discovery help omitted]
stderr:
```

### `pr-floor --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
usage: loom_checker.py pr-floor --body-file <f> --base <sha> --head <sha> [--branch <name>]
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `standing --help`

Exit: 0

```text
stdout:
standing — check applicable standing-document policy for one intent
Usage: standing <path-to-intent>
Supply one readable relative-to-working-directory or absolute intent path;
[remaining discovery help omitted]
stderr:
```

### `standing --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
no intent file at --acceptance-invalid-option
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `contract --help`

Exit: 0

```text
stdout:
contract — check compatibility with the bundled contract manifest
Usage: contract --require <major.minor> [--json]
Supply a numeric major.minor requirement. Reads the manifest in effect; a
[remaining discovery help omitted]
stderr:
```

### `contract --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
unexpected argument '--acceptance-invalid-option'.
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `charter --help`

Exit: 0

```text
stdout:
charter — render and validate artifact charter rows
Usage: charter [--manifest <path>]
Defaults to the contract manifest in effect. An override is a readable YAML
[remaining discovery help omitted]
stderr:
```

### `charter --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
unexpected argument '--acceptance-invalid-option'.
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `plan --help`

Exit: 0

```text
stdout:
plan — check the implemented field caps on one named file
Usage: plan <path-to-plan.md> [--json]
Supply a readable file path, relative to the working directory or absolute;
[remaining discovery help omitted]
stderr:
```

### `plan --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
no such plan file: --acceptance-invalid-option
Help: "<loom-code>/scripts/loom-python" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `reviewer-count --help`

Exit: 0

```text
stdout:
reviewer-count — compute the required independent reviewer floor
Usage: reviewer-count <change-id> [--json]
Run inside the selected repository with a clean tree and committed functional
[remaining discovery help omitted]
stderr:
```

### `reviewer-count --acceptance-invalid-option`

Exit: 0

```text
stdout:
2

stderr:
```

### `finalize-review --help`

Exit: 0

```text
stdout:
finalize-review — verify committed content and generate an attestation
Usage: finalize-review <change-id> --input <review-input.json>
<change-id> identifies the change; it is not a file path. --input names a
[remaining discovery help omitted]
stderr:
```

### `finalize-review --acceptance-invalid-option`

Exit: 2

```text
stdout:

stderr:
finalize-review expects `--input <review-input.json>`.
Help: "<loom-code>/scripts/loom-python" --ready finalize-review --help (replace <loom-code> with the installed loom-code plugin directory).
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `contract --require 2.1 --json`

Exit: 0

```text
stdout:
{"schema_version": 1, "command": "contract", "status": "passed", "diagnostics": [], "notices": [], "error": null, "suggested_next": null, "data": {"contract_version": "2.3.1", "required_version": "2.1", "compatible": true}}

stderr:
```

### `contract --require 2.99 --json`

Exit: 1

```text
stdout:
{"schema_version": 1, "command": "contract", "status": "blocked", "diagnostics": [{"rule_id": "contract.requires", "message": "this repo ships loom contract 2.3.1, but >=2.99 is required \u2014 \u8acb\u66f4\u65b0 loom-code\u3002"}], "notices": [], "error": null, "suggested_next": "Update the plugin identified by the contract diagnostic, then recheck supported requirements.", "data": {"contract_version": "2.3.1", "required_version": "2.99", "compatible": false}}

stderr:
```

### `contract --require bad --json`

Exit: 2

```text
stdout:
{"schema_version": 1, "command": "contract", "status": "error", "diagnostics": [], "notices": [], "error": {"kind": "usage", "message": "`--require bad` is not <major>.<minor>."}, "suggested_next": "Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.", "data": {"contract_version": null, "required_version": null, "compatible": null}}

stderr:
```

### `plan /definitely-missing-acceptance-plan --json`

Exit: 2

```text
stdout:
{"schema_version": 1, "command": "plan", "status": "error", "diagnostics": [], "notices": [], "error": {"kind": "usage", "message": "no such plan file: /definitely-missing-acceptance-plan"}, "suggested_next": "Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning."}

stderr:
```

### `reviewer-count 2026-11-14-cli-suggestions-complete --json`

Exit: 0

```text
stdout:
{"schema_version": 1, "command": "reviewer-count", "status": "passed", "diagnostics": [], "notices": [], "error": null, "suggested_next": null, "data": {"change_id": "2026-11-14-cli-suggestions-complete", "reviewer_floor": 2}}

stderr:
```

### `intake build 2026-11-14-cli-suggestions-complete --json`

Exit: 2

```text
stdout:
{"schema_version": 1, "command": "intake", "status": "error", "diagnostics": [], "notices": [], "error": {"kind": "usage", "message": "unknown station 'build'; intake covers write-spec and write-plan."}, "suggested_next": "Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning."}

stderr:
```

### `delivery 2026-11-14-cli-suggestions-complete --json`

Exit: 2

```text
stdout:

stderr:
delivery: unexpected or repeated argument '2026-11-14-cli-suggestions-complete'
Help: "<loom-code>/scripts/loom-python" --ready delivery --help (replace <loom-code> with the installed loom-code plugin directory).
Suggested next step: Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning.
```

### `--list-rules`

Exit: 0

```text
stdout:
adversarial.proportionate	A change produces at most 5 adversarial probe programs, and every one of them carries a non-empty `concern:` line in its first lines naming the kind of defect it defends against. Both halves are recomputed at finalize-review over the union of three sets, because no one of them is the whole of what the step produced: the programs the selected commit holds anywhere in the change's store, whatever their extension; the programs finalize-review is about to execute; and the programs this branch adds straight into the package suite the repository declares, which the `concern:` line marks as the adversary's output rather than ordinary new tests. A graduated program therefore still spends against the ceiling, which reading the store alone could not see, since the graduation gate empties that directory first. A program committed elsewhere in the change's store, outside its `evidence/probes/` directory, is refused rather than left uncounted.
ci.pr-floor	The pr-floor CI check fails only when the pull-request body lacks Ship's nine contextual headings in order, naming the heading; the verification status is recomputed from git and published as a notice, and every status passes.
contract.charter-complete	Every artifact in the contract manifest carries a complete `charter:` block -- non-empty answers/readers/must/must_not/edits_after, a must_not goes_to naming another artifact in the table, and a signoff naming a real station.
contract.requires	A consumer plugin's requires-contract floor is met by this contract manifest version: the same major, and a minor at or above the required one.
delivery.observed	delivery succeeds only for the requested local, published or merged goal observed from attributable working-tree scope and current Git/PR/check evidence; unavailable evidence remains unconfirmed, never authorization to publish or merge. Small and engineering-only changes retain the same branch/PR policy.
intake.attestation-coverage	Acceptance test report must have a row for each intent Acceptance line with valid Verdict status (works/partly/not_verified/fails).
intake.commit-identity	Functional content diff between tested_commit and reviewed_commit in attestation must be limited to evidence files only.
intake.confirmed	write-spec / write-plan accept only an intent whose status line reads `confirmed <date>` with a date the calendar has; `closed <date> — PR #<N>` or `closed <date> — branch <name>` is blocked -- that change is closed and a new change starts from a new intent. closed is terminal either way, and a confirmed intent is also blocked after canonical delivery evidence appears on the selected remote-default snapshot. Local branches and worktree evidence never prove delivery; an unresolved remote default is indeterminate and blocks intake.
intake.confirmed-behavior	write-plan accepts a product change only when its spec carries a `confirmed-behavior: <date> @<spec-blob-sha7>` line naming the spec as it stands.
intake.intent-version	Intent Acceptance lines must match those recorded at confirmation time (intent_confirmed_sha).
intake.plan-boundary-tests	A Risk line's named boundary-test task must exist in charter 1.1+ plans. After Build, concrete backticked boundary/probe filenames in marked tasks' Files/Test fields and numbered Risks must exist in the checked tree.
intake.spec-ready	write-plan accepts a needs-design: yes change only when its spec exists and carries an explicit `pre-build-review: required|not-required — <reason>` declaration. Review independence is enforced by the write-spec station, not persisted in a ledger.
intake.test-case-pair	Every task in a newly authored plan names the intent Acceptance lines it owns, and each named line has positive plus negative or boundary test cases, unless the task's Files are all docs/release-classed (low-risk docs outside protected parts, change/evidence stores, or release metadata at plugin root).
intent.kind-recompute	kind: engineering is rejected when the diff touches a declared interface-surface glob.
intent.needs-design-reason	The needs-design line carries a reason and appears verbatim in the message of the commit that last changed the intent's status or needs-design line.
intent.needs-design-recompute	needs-design: no is rejected when the diff touches a declared interface-surface glob.
intent.product-no-identifiers	A product intent's Problem section names no file path, code identifier or script filename.
intent.schema	The intent file carries every required frontmatter field and H2 section declared in the contract manifest.
land.cleanup	land removes a change's worktree and branches only when its PR is merged, the worktree is clean apart from regenerable caches, and each branch tip equals the merged PR head, selected by exact branch name; a changed sweep list removes nothing.
land.merge	land merges nothing unless every precondition holds: the change identified from the branch name or its one intent file, an --accepted-by name equal to the intent's originator or publication authorizer, a live PR body with the nine contextual headings, one open PR whose head is HEAD, every check passed (not only required ones), and a MERGEABLE state other than BLOCKED, DIRTY, BEHIND, UNSTABLE, or DRAFT. No attestation is required; an absent or stale one is printed after the merge.
land.verify	After land merges, the squash commit read back from the trunk carries the PR title and the PR body; otherwise land stops before trunk sync and cleanup.
plan.field-caps	A plan whose frontmatter carries a `charter:` key (any value, presence only) caps each task's Test and Risk lines at 40 words, its Files line at 8 comma-separated entries (a comma inside backticks does not split), each numbered `## Risks` item at 40 words, and each `## Current State Evidence` bullet at 30 words -- CJK runs with no internal whitespace count as one word by len(text.split()); a task missing its Files, Test or Risk line blocks too. A plan whose `charter:` is 1.1 or later also needs a non-empty ## Simplicity check` section: lines `- <simpler shape> — taken` or `- <simpler shape> — declined: <reason>`, or the single line `- none found`; the single line `- skipped — narrow change` passes only when every task's Files paths form a narrow delta. A plan with no `charter:` line is skipped entirely.
publish.preconditions	publish pushes HEAD and opens or updates its one pull request only when the change is identified, publication is authorized, any generated attestation is committed, git and gh resolve to trusted executables, origin is a literal GitHub URL, and HEAD, the remote branch and the PR identity stay unchanged across every network step; the verification status is disclosed, never a refusal.
push.contextual-body	The exact pull-request body carries Ship's nine top-level contextual headings exactly once and in order, with no competing Memory heading or explicit claim to expose private or hidden chain-of-thought, and any `Verification status:` line states exactly the status publish computes.
review.sync	sync-trunk merges the freshly fetched origin trunk into the change branch before closing review, never rebasing or forcing: it refuses a trunk checkout, a detached HEAD or a dirty worktree untouched; adds no commit when HEAD already contains the trunk tip; on conflict names every conflicting file and leaves HEAD and the worktree untouched (detected in memory, or merged then aborted when git cannot); an unreachable remote only warns.
spec.req-grammar	Every Requirements entry reads `REQ-<n> — <name>` with n contiguous from 1, unique, and points at an Acceptance number the intent actually carries.
spec.ui-flows-recompute	While the diff touches a declared interface-surface glob, the spec's UI flows section carries at least one prose line (outside fences, indented code and HTML comments) with an arrow and at least four visible characters on each side. This is a structural floor only -- whether the flow says anything true or useful is the reviewer lens's job, not a keyword list's. Runs at write-plan intake only.
standing.product-principles-reject	A product change is rejected until PRINCIPLES.md is ratified: a `ratified-by: <name> <YYYY-MM-DD>` signature with a real date, over three or more distinct non-negotiables.
standing.second-vendor-valid	KICKOFF-DEFAULTS rejects the removed `second-vendor: none` value with explicit migration guidance to use the non-blocking `suggest` mode.
standing.silence	KICKOFF-DEFAULTS `standing-docs: waived` silences the WARN only, never the product rejection.
standing.warn	A missing PRINCIPLES.md, DESIGN.md or ARCHITECTURE.md prints the fixed three-line WARN and never blocks.

stderr:
```

### `delivery --json`

Exit: 1

```text
stdout:
{"state": "unconfirmed", "reason": "a safe symbolic feature branch is required", "next": "Preserve the current work on a named feature branch before continuing.", "evidence": {"change_id": "2026-11-14-cli-suggestions-complete", "head": "64b49d3d0d2e25d10618cfc43636f9fb20d81034", "branch": null}, "complete": false, "suggested_next": "Preserve the current work on a named feature branch before continuing."}

stderr:
Help: "<loom-code>/scripts/loom-python" --ready delivery --help (replace <loom-code> with the installed loom-code plugin directory).
```

### `intake write-plan 2026-11-14-cli-suggestions-complete --json`

Exit: 0

```text
stdout:
{"schema_version": 1, "command": "intake", "status": "passed", "diagnostics": [], "notices": ["interface-surfaces (manifest default (KICKOFF-DEFAULTS adds nothing new)): **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** (non-code paths under **/templates/** excluded)"], "error": null, "suggested_next": null}

stderr:
```

### `reviewer-count`

Exit: 2

```text
stdout:

stderr:
reviewer-count needs one change-id.
Help: "<loom-code>/scripts/loom-python" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).
Suggested next step: Inspect the diagnostic and command help; select the intended repository, preserve outstanding work and establish a clean completed change before deliberately rerunning.
```

### `plan docs/loom/2026-11-14-cli-suggestions-complete/plan.md --json`

Exit: 0

```text
stdout:
{"schema_version": 1, "command": "plan", "status": "passed", "diagnostics": [], "notices": [], "error": null, "suggested_next": null}

stderr:
```

## Independently executed focused test runs

The complete modules in each command were run once; this is not the repository full suite. All three commands exit 0, with **777 passed, zero skipped and no failures** in total.

### Main command/result coverage

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_preparation_json.py loom-code/tests/test_checked_readonly.py loom-code/tests/test_loom_checker_intent.py loom-code/tests/test_loom_checker_intake.py loom-code/tests/test_contract_charter.py loom-code/tests/test_plan_field_caps.py loom-code/tests/test_plan_skip_missing_files.py loom-code/tests/test_delivery.py loom-code/tests/test_delivery_stop.py loom-code/tests/test_sync_trunk.py loom-code/tests/test_github_rules.py loom-code/tests/test_pr_floor.py loom-code/tests/test_pr_floor_workflow.py loom-code/tests/test_loom_checker_standing.py loom-code/tests/test_land_sweep.py loom-code/tests/test_land_cleanup.py loom-code/tests/test_land_merge.py loom-code/tests/test_loom_publish.py loom-code/tests/test_selection_finalize.py loom-code/tests/test_probe_confirmation_finalize.py -q -rs
```

```text
........................................................................ [ 11%]
........................................................................ [ 22%]
........................................................................ [ 33%]
........................................................................ [ 45%]
........................................................................ [ 56%]
........................................................................ [ 67%]
........................................................................ [ 78%]
........................................................................ [ 90%]
................................................................         [100%]
640 passed in 363.66s (0:06:03)
```

### Native protocols and startup

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_native_git_protection.py loom-code/tests/test_hooks_json.py loom-code/tests/test_publish_command_detection.py loom-code/tests/test_ship_worktree_merge.py loom-code/tests/test_loom_python_runtime.py -q -rs
```

```text
........................................................................ [ 68%]
.................................                                        [100%]
105 passed in 24.87s
```

### Authority and legacy boundaries

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_adversarial_blocked_publish_routes.py loom-code/tests/test_legacy_contract_removed.py -q -rs
```

```text
................................                                         [100%]
32 passed in 4.66s
```

## Final scope and evidence integrity

- Fresh acceptance tester did not implement or review the change beforehand. Measurements ran against exact HEAD 64b49d3; generated report/evidence changes were made only afterward.
- Product/test sources were unchanged. Only acceptance report and evidence are copied to the active feature branch for the authorized evidence commit; clean worktree and raw captures remain available under the temporary acceptance paths.
- Git-memory classification: routine measurement record, no new reusable implementation decision/learning/gotcha, so no memory trailers. Exact commit message passed deterministic privacy scan (exit 0, empty findings); it contains no ambiguous private-party identifiers, so semantic judge is not required.
- Retained setup denial and exploratory invocation mistakes are disclosed above. No failure was repaired, discarded or silently converted to a live success.
