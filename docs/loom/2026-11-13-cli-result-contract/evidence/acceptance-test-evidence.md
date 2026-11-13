# Help-first CLI delivery — acceptance test evidence

Tried on 2026-11-13, in a clean copy of the project at 1ccb7f514ec63aaf2d02d90108ea5b67d65fe4b7.

## Re-run on 2026-11-13, at 4e6e2d4dac8e904c527e15e425c8ea337a4769b7

### Bounded risk-guidance correction and preserved history

Fresh clone: `git clone --no-hardlinks /private/tmp/loom-cli-result-contract /private/tmp/loom-help-acceptance-rerun-4e6`, success. Actual HEAD:4e6e2d4dac8e904c527e15e425c8ea337a4769b7. Existing worktrees preserved.

Read actual e244a5f3..4e6e2d4 plan diff and both full task blocks: W3-02 Risk now describes independent adversarial/full-suite execution, no padding, failure preservation, no live writers/paid calls; W3-04 Risk now describes existing consent, same scope, equivalent identity/current references/confirmation ancestry and preserved historical evidence. Those match each task's Files/Test/purpose. Round2 reviewers had found copied Risk text from unrelated tasks; this was a real documentation finding, now fixed, not dismissed. It supplements the already preserved initial partly discovery finding and round1 finalization provenance refusal below. No successful finalization is inferred.

`git diff 6aad2e920 4e6e2d4 --name-only -- loom-code/scripts loom-code/tests loom-code/hooks loom-code/contract docs/loom/intent/2026-11-13-cli-result-contract.md docs/loom/2026-11-13-cli-result-contract/spec.md`: empty. Full cumulative paths only plan and this change's acceptance/build/provenance evidence. Thus intent identity, confirmation selection, spec, four Acceptance lines, all help/source/tests/hooks/contracts/version and existing consumer assertions are unchanged.

### README setup and actual checks

Followed README startup in the new clean clone:
`/bin/sh loom-code/scripts/loom-python --repair contract --require 2.3`.
Exit0; stdout `contract 2.3.1 satisfies requires-contract >=2.3`; empty stderr. Uses actual pre-existing valid cached runtime; no first-install/download claim.

Separately ran each check to obtain individual tool exit codes:
- `/bin/sh loom-code/scripts/loom-python --ready plan docs/loom/2026-11-13-cli-result-contract/plan.md`: exit0, empty stdout/stderr.
- `/bin/sh loom-code/scripts/loom-python --ready intake write-plan 2026-11-13-cli-result-contract`: exit0, empty stderr; stdout exactly:
  `interface-surfaces (manifest default (KICKOFF-DEFAULTS adds nothing new)): **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** (non-code paths under **/templates/** excluded)`.

The interface line is advisory and these checks do not approve or execute a station. A Python wrapper attempted solely to collect individual exits was blocked before execution by the local command guard because its expanded subprocess argv could not be statically verified. Used the direct fixed commands above successfully; no permission bypass or source repair occurred.

Reused the same external temporary probe in memory, replacing candidate root with /private/tmp/loom-help-acceptance-rerun-4e6 and capture destination with /private/tmp/loom-help-acceptance-round3-captures.json. No executable file added. Explicit /Users/kouko/.conda/envs/dbt-redshift/bin/python3 returned0:
`32 ready exact-help calls identical to initial captures; overall discovery lists16; README current and research historical boundaries correct; coldready86no-cache; clean tree`.

All16 commands intent/intents/intake/push/publish/delivery/land/sync-trunk/github-rules/pr-floor/standing/contract/charter/plan/reviewer-count/finalize-review were actually invoked with both exact --help and -h outside repo. Every result exit0/empty stderr and stdout byte-identical to original full capture retained below. Overall help still lists16. Fixed README/research/current-conformance paths remain accurate. Missing-ready cache still exits86 with prescribed diagnostic and no cache directory; clean tree confirmed. Earlier tripwire tests are unchanged carried evidence, not a new test execution.

### Current row decisions

- **1: re-tested**, over all16 help/inventory surfaces plus current plan/provenance documentation. Read corrected W3-02/04 Risks against real tasks, retained current scope/identity and original16handler source anchors; actual plan/intake and all32help calls passed.
- **2: carried over —** no source/help/spec/test change since prior tested6aad or341; original independent16handler readback and actual help text remain valid. Full stdout equality independently re-observed.
- **3: carried over —** no intent/schema/consumer/hook/test/runtime/version change; original25base-equivalence outputs and45JSON/delivery/Stop consumer passes remain applicable. The90second deadline suite was not repeated.
- **4: re-tested**, all16x2 exact help calls, overview/current documentation and cold-ready behavior as above. Bounded risk prose does not change execution safety; prior tripwire tests remain valid.

All four current verdicts are works; no new findings or important dismissals. Only canonical report and this evidence edited by this tester. Report EOF normalized to one newline. No live writer, paid call or outside review CLI.

Complete suite remains finalization's responsibility; no step skipped. Station supplies round3 Build exit0/4269passed/6skipped plus all runner groups and the same declared adversary39passed9.57s. Those supplied results are not this tester's rerun; formal finalization and reviews remain separate from acceptance.

## Re-run on 2026-11-13, at 6aad2e920e7d2507f26a659295ab573e4518dfd8

### Provenance repair, prior refusal and scope

Read current intent/spec/plan, confirmation-provenance-fix.md, prior canonical report and prior dated evidence. Read actual fix diff 9e19e2d2..6aad2e920 and cumulative file list since prior tested34143f6. Only intent/spec/plan/provenance and report/build evidence changed; scripts/tests/hooks/contract bytes are unchanged. All four Acceptance lines and substantive spec requirements are unchanged. The pin presentation changed40characters to12; it is the same normalized identity. Spec/plan now reference canonical confirmation2f29db8ab63a49c5b69decf2973d201112e63f59. Plan file-cap compression and localized README task separation do not change delivered functionality.

Preserve prior formal failure: station reports round1 finalization executed the complete suite and adversarial program successfully, then refused intake.intent-version because earlier noncanonical subject16d9157b left old01d73c1a JSON-scope confirmation selected. This is not a successful attestation. This acceptance rerun independently checks the corrected canonical selection, not the entire finalization process. No important finding was dismissed. Original partly report and all historical failures/captures below remain unchanged.

Initial abbreviated diff command used6aad and failed with "short object ID6aad is ambiguous" (commit6aad2e920 versus blob6aad843d1). Repeated with6aad2e920 successfully; no evidence is inferred from the failed command.

### Fresh clone and actual setup

`git clone --no-hardlinks /private/tmp/loom-cli-result-contract /private/tmp/loom-help-acceptance-rerun-6aad`: success.
`git rev-parse HEAD`:6aad2e920e7d2507f26a659295ab573e4518dfd8.
Followed README startup again:
`/bin/sh loom-code/scripts/loom-python --repair contract --require 2.3`
from fresh clone: exit0, stdout `contract 2.3.1 satisfies requires-contract >=2.3`, empty stderr. Reused actual existing ready user cache; no new install/download claim.

`git diff 34143f6 6aad2e920 --name-only -- loom-code/scripts loom-code/tests loom-code/hooks loom-code/contract`: empty output. Full cumulative changed-path list contains only this change's intent/spec/plan and acceptance/build/provenance evidence. Runtime/version/JSON/consumer code and all prior focused-test assertions remain identical.

### Actual confirmation and plan checks

Using the existing cached Loom Python from the clean clone, imported the unmodified checker helper and intent_version functions with loom-code/scripts on sys.path, loaded the bundled manifest and ran:
- pinned_confirmation(manifest,repo,change): **2f29db8ab63a49c5b69decf2973d201112e63f59**.
- intent_identity(current_intent): **66583a51db46b4517f692cab4dcf61318fc19b21**.
- check_intent_version(manifest,repo,change,{},{"intent_confirmed_sha":identity}): **[]**.

These were actual calls, with assertions of all three values and exit0. They neither create reviewer evidence nor establish attestation. Read the existing implementation: status/pin lines are excluded from normalized identity and pin-prefix agreement is permitted. This validates same-scope identity and corrected selection without inferring consent from a generated artifact.

`/bin/sh loom-code/scripts/loom-python --ready plan docs/loom/2026-11-13-cli-result-contract/plan.md`: exit0, empty stdout/stderr. This is implemented field-cap validation only, not plan approval. Final candidate git status --porcelain: empty.

### Per-row rerun and carry-over reasons

- **1: re-tested**, across all16 named surfaces. Actual32help outputs remain byte-identical to initial full captures; all16 source files/inventory remain unchanged. Re-read current inventory links, README current16coverage, historical research boundary and canonical intent/spec/plan pointers; actual checker selection/identity above confirms the documented current help-only scope. Original per-handler readback remains available below.
- **2: carried over —** actual cumulative source/test/contract diff is empty and all32help stdout match original full captures; requirements are unchanged. The earlier independent16handler content comparison and49focused test passes remain applicable.
- **3: carried over —** no implementation/schema/hook/test/version changes; same normalized intent identity and all4Acceptance lines. Earlier25base-equality tuples and45preparation/delivery/Stop consumer passes remain applicable; no repeated90second deadline suite was necessary or performed.
- **4: re-tested**, across all16commands and both exact spellings, outside repo. All32return0/empty stderr/finite text exactly matching prior capture. Overall help lists16; fixed README/runtimesafety and research labels remain accurate. Cold-ready isolated cache still returns86 without provisioning/cache creation; tree stays clean. Unchanged earlier handler/stdin/subprocess/socket/artifact tripwires are carried evidence, not newly executed tests this round.

### Actual help command

Executed the existing external temporary rerun probe through explicit /Users/kouko/.conda/envs/dbt-redshift/bin/python3, replacing only its candidate root to /private/tmp/loom-help-acceptance-rerun-6aad and capture destination to /private/tmp/loom-help-acceptance-round2-captures.json in memory. No repository executable was added.

Exit0, stdout:
`32 ready exact-help calls identical to initial captures; overall discovery lists16; README current and research historical boundaries correct; coldready86no-cache; clean tree`.

No full suite or90second Stop tests rerun by acceptance tester. Station supplies latest Build complete-suite exit0/4269passed/6skipped plus all runner groups, and declared adversarial39passed9.38s, with round2 raw logs. Those remain supplied Build results, not this tester's execution. No skips; finalize-review will run the declared complete suite and adversary and may still refuse later evidence conditions. Current acceptance4works does not claim generated finalization success.

No source/plan edits, live writers, paid calls or outside review CLI were used. Only canonical report and this evidence were edited.

### Round2 capture

```json
{
  "tested_sha": "6aad2e920e7d2507f26a659295ab573e4518dfd8",
  "help": [
    {
      "command": "intent",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "intent",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "intents",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "intents",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "intake",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "intake",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "push",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "push",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "publish",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "publish",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "delivery",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "delivery",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "land",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "land",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "sync-trunk",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "sync-trunk",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "github-rules",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "github-rules",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "pr-floor",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "pr-floor",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "standing",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "standing",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "contract",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "contract",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "charter",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "charter",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "plan",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "plan",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "reviewer-count",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "reviewer-count",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "finalize-review",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "finalize-review",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    }
  ],
  "overview": "\n\n    loom_checker.py --list-rules\n    loom_checker.py --help\n    loom_checker.py intent <path> [--commit-msg <file>]\n    loom_checker.py intents [<change-id>] [--remote <name>] [--metadata]\n    loom_checker.py intake <station> <change-id> [--json]\n    loom_checker.py push --hook\n    loom_checker.py push --install-git-hooks\n    loom_checker.py push --remove-git-hooks\n    loom_checker.py publish --intent <absolute-path> --title <text> --body-file <absolute-path>\n    loom_checker.py publish --confirm-authorized --title <text> --body-file <absolute-path>\n    loom_checker.py delivery [--goal local|published|merged] [--intent <path>] [--json]\n    loom_checker.py land --accepted-by <name>\n    loom_checker.py land --cleanup <branch>\n    loom_checker.py land --sweep [--confirm <token>]\n    loom_checker.py sync-trunk\n    loom_checker.py github-rules [--print-setup]\n    loom_checker.py pr-floor --body-file <f> --base <sha> --head <sha> [--branch <name>]\n    loom_checker.py reviewer-count <change-id>\n    loom_checker.py finalize-review <change-id> --input <review-input.json>\n    loom_checker.py standing <path-to-intent>\n    loom_checker.py contract --require <major.minor>\n    loom_checker.py charter [--manifest <path>]\n    loom_checker.py plan <path-to-plan.md> [--json]\n\nWith the launcher, the checker is selected automatically; omit loom_checker.py:\n    \"<loom-code>/scripts/loom-python\" --repair plan \"<path-to-plan.md>\"\n    \"<loom-code>/scripts/loom-python\" --ready intake <station> <change-id>\nReplace <loom-code> with the installed plugin directory and <path-to-plan.md>\nwith your plan file path.\nPlan takes a file path; intake takes a station and a change-id.\nPlan and intake accept an optional final --json selector; text remains default.\nDetailed help: finalize-review --help, publish --help, delivery --help\n              plan --help, intake --help, reviewer-count --help\n              intent --help, intents --help, push --help, land --help\n              sync-trunk --help, github-rules --help, pr-floor --help\n              standing --help, contract --help, charter --help\nEvery listed sub-command supports <command> --help or <command> -h.\nOnly exact command-plus-help forms are help.\nNo validation runs for --help or -h alone.\n\nExit codes depend on the command: 0 may include advisory or unsynced results;\n1 means a failed check or incomplete operation; 2 means usage/internal error\nor a hook refusal. See each command's help for its completion limits.\nThe publication hook allows on unexpected exceptions; other commands exit 2.\n\nSchemas are not restated here: the required frontmatter fields, sections,\nstation names, interface-surface defaults and artifact paths are read\nfrom `loom-code/contract/manifest.yaml`, which is the versioned contract\npackage this checker ships with.\n",
  "cold": {
    "exit": 86,
    "stderr": "loom-python: checker runtime is missing or invalid; run loom-python --repair with the same arguments in an agent station.\n",
    "cache_created": false
  },
  "readme_current_coverage": true,
  "research_snapshot_label": true,
  "clean": true
}
```

## Re-run on 2026-11-13, at 34143f6cc4a1aa349ba5672caaaf0de95487de8d

This dated section supersedes only the current verdicts; the original run, its partly result, original captures and failed setup attempts below are preserved unchanged. Original canonical report was committed at b824c462 before the documentation fix. The new canonical report names the actual new tested commit.

### Clean setup repeated

`git clone --no-hardlinks /private/tmp/loom-cli-result-contract /private/tmp/loom-help-acceptance-rerun-34143f6` succeeded. `git rev-parse HEAD` returned 34143f6cc4a1aa349ba5672caaaf0de95487de8d.

Followed plugin README startup again:
`/bin/sh /private/tmp/loom-help-acceptance-rerun-34143f6/loom-code/scripts/loom-python --repair contract --require 2.3`.
Exit 0, stdout `contract 2.3.1 satisfies requires-contract >=2.3`, empty stderr. As on the first run, this reuses the actual existing valid cached runtime; clean first-time downloading/installing is not claimed.

### Fix diff and carried-over checks

Read full `git diff b824c462 34143f6`: only README.md, the research guide and plan W3-03 changed. README now documents all sixteen exact-help forms, ordinary parsing outside those forms, ready exit86, repair provisioning, unchanged six-command failure hints and no new JSON. Research intro now says pre-implementation study, links current conformance evidence and narrowed intent; inventory is explicitly historical fbdc29a/3.72.0. Historical rows were preserved, not changed into current implementation data. W3-03 records those bounded changes and no skip.

`git diff 1ccb7f5 34143f6 --name-only -- loom-code/scripts loom-code/tests loom-code/hooks loom-code/contract` produced no output. The full fix diff also shows no schema/consumer/runtime change elsewhere. Carry-over reasons were checked against both the named fix range and original tested content; the source-to-help comparison and ordinary compatibility conclusions remain applicable.

- **1: re-tested**, in full. Revisited current sixteen-command inventory against all sixteen actual help pages; each new page is byte-identical to the original fully captured/readback version, and all sixteen handler sources are unchanged. Rechecked current README discovery, research historical inventory, baseline labels/current-conformance link and plan W3-03. The original source anchors/outcome boundaries and prior actual ordinary outputs under section1 remain accurate; the documentation now clearly distinguishes present coverage from historical availability.
- **2: carried over —** only documentation changed; all sixteen handler implementations, actual help strings and source-accuracy evidence remain unchanged. Actual new 32 help subprocess outputs also match the original complete captures byte-for-byte. No source/content uncertainty calls for broader retesting.
- **3: carried over —** no programs, tests, hook adapters, preparation-v1 or delivery contracts/consumers changed. The original 25 complete base-equality tuples and 45 preparation/delivery/Stop consumer passes remain applicable. README now describes the already-existing no-new-JSON boundary. This carry-over does not claim another full consumer-suite execution.
- **4: re-tested**, in full. Actual ready-launcher --help and -h calls for intent, intents, intake, push, publish, delivery, land, sync-trunk, github-rules, pr-floor, standing, contract, charter, plan, reviewer-count and finalize-review: 32 calls outside a repository, all exit0/empty stderr and identical to the original output. Overall --help lists all16. Re-read fixed current guidance and historical snapshot distinction against the actual pages. Cold-ready with isolated nonexistent cache and PATH=/usr/bin:/bin returned86, prescribed diagnostic and no cache created. Candidate remained clean.

### Actual rerun commands and results

`/Users/kouko/.conda/envs/dbt-redshift/bin/python3 /private/tmp/loom-help-acceptance-rerun-probe.py`: exit0, output:
`32 ready exact-help calls identical to initial captures; overall discovery lists16; README current and research historical boundaries correct; coldready86no-cache; clean tree`.

`/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_loom_python_runtime.py -q` from new clean clone: exit0, **49 passed in19.02s**. This reruns all16 handler/stdin/subprocess/socket/artifact tripwires, non-exact ordinary dispatch, ready/missing-runtime startup cases and public CLI/runtime coverage. It is focused coverage, not the complete package suite.

No complete package suite was run by this tester. Station supplies a fixed-HEAD Build result of4269passed/6skipped, exit0, plus declared adversarial39passed; those are supplied Build evidence, not an independent acceptance rerun result. No step is skipped; finalize-review still executes and blocks on the complete suite. No live writer, paid call or provisioning download occurred.

### Findings disposition

A4-1 important current README contradiction: **fixed and independently re-tested**, not dismissed.
A4-2 nit research present-versus-historical ambiguity: **fixed and independently re-read**, original snapshot preserved.
No new finding; no important-or-worse dismissal. Current verdicts:1works,2works(carried),3works(carried),4works.

### Rerun captures

Each stdout_identity flag compares the complete actual stdout to the initial full capture below; stderr and exit are actual results. Overall help and missing-runtime diagnostic are captured here.

```json
{
  "tested_sha": "34143f6cc4a1aa349ba5672caaaf0de95487de8d",
  "help": [
    {
      "command": "intent",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "intent",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "intents",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "intents",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "intake",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "intake",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "push",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "push",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "publish",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "publish",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "delivery",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "delivery",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "land",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "land",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "sync-trunk",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "sync-trunk",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "github-rules",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "github-rules",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "pr-floor",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "pr-floor",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "standing",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "standing",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "contract",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "contract",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "charter",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "charter",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "plan",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "plan",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "reviewer-count",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "reviewer-count",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "finalize-review",
      "flag": "--help",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    },
    {
      "command": "finalize-review",
      "flag": "-h",
      "exit": 0,
      "stdout_identical_to_initial_capture": true,
      "stderr": ""
    }
  ],
  "overview": "\n\n    loom_checker.py --list-rules\n    loom_checker.py --help\n    loom_checker.py intent <path> [--commit-msg <file>]\n    loom_checker.py intents [<change-id>] [--remote <name>] [--metadata]\n    loom_checker.py intake <station> <change-id> [--json]\n    loom_checker.py push --hook\n    loom_checker.py push --install-git-hooks\n    loom_checker.py push --remove-git-hooks\n    loom_checker.py publish --intent <absolute-path> --title <text> --body-file <absolute-path>\n    loom_checker.py publish --confirm-authorized --title <text> --body-file <absolute-path>\n    loom_checker.py delivery [--goal local|published|merged] [--intent <path>] [--json]\n    loom_checker.py land --accepted-by <name>\n    loom_checker.py land --cleanup <branch>\n    loom_checker.py land --sweep [--confirm <token>]\n    loom_checker.py sync-trunk\n    loom_checker.py github-rules [--print-setup]\n    loom_checker.py pr-floor --body-file <f> --base <sha> --head <sha> [--branch <name>]\n    loom_checker.py reviewer-count <change-id>\n    loom_checker.py finalize-review <change-id> --input <review-input.json>\n    loom_checker.py standing <path-to-intent>\n    loom_checker.py contract --require <major.minor>\n    loom_checker.py charter [--manifest <path>]\n    loom_checker.py plan <path-to-plan.md> [--json]\n\nWith the launcher, the checker is selected automatically; omit loom_checker.py:\n    \"<loom-code>/scripts/loom-python\" --repair plan \"<path-to-plan.md>\"\n    \"<loom-code>/scripts/loom-python\" --ready intake <station> <change-id>\nReplace <loom-code> with the installed plugin directory and <path-to-plan.md>\nwith your plan file path.\nPlan takes a file path; intake takes a station and a change-id.\nPlan and intake accept an optional final --json selector; text remains default.\nDetailed help: finalize-review --help, publish --help, delivery --help\n              plan --help, intake --help, reviewer-count --help\n              intent --help, intents --help, push --help, land --help\n              sync-trunk --help, github-rules --help, pr-floor --help\n              standing --help, contract --help, charter --help\nEvery listed sub-command supports <command> --help or <command> -h.\nOnly exact command-plus-help forms are help.\nNo validation runs for --help or -h alone.\n\nExit codes depend on the command: 0 may include advisory or unsynced results;\n1 means a failed check or incomplete operation; 2 means usage/internal error\nor a hook refusal. See each command's help for its completion limits.\nThe publication hook allows on unexpected exceptions; other commands exit 2.\n\nSchemas are not restated here: the required frontmatter fields, sections,\nstation names, interface-surface defaults and artifact paths are read\nfrom `loom-code/contract/manifest.yaml`, which is the versioned contract\npackage this checker ships with.\n",
  "cold": {
    "exit": 86,
    "stderr": "loom-python: checker runtime is missing or invalid; run loom-python --repair with the same arguments in an agent station.\n",
    "cache_created": false
  },
  "readme_current_coverage": true,
  "research_snapshot_label": true,
  "clean": true
}
```

## Setup and limits

Fresh clones: `git clone --no-hardlinks /private/tmp/loom-cli-result-contract /private/tmp/loom-help-acceptance-clean` and an independent base clone `/private/tmp/loom-help-acceptance-base`, detached at fbdc29af358413bc9d55b599231b2a6cbcb4524d. Both succeeded; candidate HEAD is the SHA above. No existing worktree was removed. Candidate git status remained empty after execution.

Read the root README, plugin README runtime instructions, intent, spec, plan, help-conformance inventory and Build record. Followed plugin README startup with `/bin/sh /private/tmp/loom-help-acceptance-clean/loom-code/scripts/loom-python --repair contract --require 2.3`: exit 0, stdout `contract 2.3.1 satisfies requires-contract >=2.3`, empty stderr. This reused the actual pre-existing valid user cache; it proves clean-checkout load/startup, not a first-time download/install. Deliberately requesting 1.1 first returned authentic BLOCK contract.requires / exit 1 explaining the old consuming major. It was a wrong requirement supplied by this tester, not a setup defect.

Initial focused command `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_loom_python_runtime.py -q` failed before collection with exit 2: `Could not acquire lock ... Operation not permitted ... /Users/kouko/.cache/uv/.tmp1C1GNq`. Trying bare python3 -m pytest exited 1 with Homebrew Python 3.15 `No module named pytest`; shell resolution differed from the earlier combined import check. Diagnosed by using the explicit existing /Users/kouko/.conda/envs/dbt-redshift/bin/python3. No dependencies were installed.

Focused CLI/runtime command, from candidate root:
`/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_loom_python_runtime.py -q`
Exit 0: **49 passed in 19.09s**.

Focused existing JSON/delivery/host-consumer command:
`/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest loom-code/tests/test_preparation_json.py loom-code/tests/test_delivery.py loom-code/tests/test_delivery_stop.py -q`
Exit 0: **45 passed in 90.00s**. Real bounded deadline tests account for the wait; no paid/model calls or live remote writes.

The complete package suite was not rerun by this acceptance tester, as required by its role. The station says no skips and will execute finalize-review. Suite command to be executed there:
`uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
Build's reported 4264 passes/11 skips plus visualization supplement is prior evidence, not this tester's result; remaining skips remain skips. No formal attestation or full-suite success is claimed here.

## 1. 全部主要子命令的既有輸入、輸出、狀態、退出碼與副作用有可追溯盤點，各命令的適用方式及例外可被獨立核對。

Walked the inventory against actual handler parsers and output/effect branches, then read the actual generated help (full captures below). Commands below name source under loom-code/scripts/loom_checker/command_handlers unless specified. Inventory is evidence/help-conformance.md; it explicitly labels the old six-page baseline and narrowed current scope. `git diff fbdc29a HEAD --name-only -- loom-code/scripts loom-code/hooks` returns only loom-code/scripts/loom_checker.py. Handler bodies, result schemas and hook programs are unchanged.

| Command | Independent source readback and meaning checked |
|---|---|
| intent | intent.py cmd_intent: path and optional commit-message input, conditional interface calculation, checks-only non-authority, possible advisory stdout before later failure. |
| intents | intents.py parser/cmd/metadata: origin default, metadata requires ID, filtered list, two-field versus detail/metadata rows, committer timestamp; local observation with indeterminate exit 1 and no fetch. |
| intake | intake.py cmd_intake: two stations, ID grammar, canonical artifact resolution, confirmation before conditional checks, advisory notices and preparation result path. |
| push | push.py cmd_push/read_hook_payload/_protect_main/_native_hooks: three exact modes; malformed payload, repository-local opt-out, global-option matcher limits, shared hooks, core.hooksPath refusal, owned-file writes/removal and rollback attempt. |
| publish | publish.py _publish_args/_intent_authorizes_publication/cmd_publish/_cmd_publish_trusted/_observe_required_ci: absolute files, nonblank title, authentic authority, body snapshot, origin/HEAD guards, remote write before CI observation and no-required-checks exit 0. |
| delivery | publish.py cmd_delivery/observe_delivery/_delivery_stop: selected-goal JSON object, hook-only forms and host replies, duplicate/malformed text errors, local completion distinct from finalization, observation without authority. |
| land | land.py _land_args/cmd_land/_land_accepted/_sync_and_clean/execute_cleanup/_land_sweep/_merge_preconditions/_observe_all_checks: acceptance name not consent, live body/HEAD, all checks, merge before later failure, best-effort trunk sync ignored as cleanup return decides exit, sweep fetch/prune before token. |
| sync-trunk | sync.py cmd_sync_trunk/_may_rebase/_preflight_conflicts/_refuse: clean attached change branch, fetch warning returns 0 with no sync, conditional rebase/merge and attempted restore, re-pin after rebase. |
| github-rules | github_rules.py _probe/_report/cmd_github_rules: optional setup printing, trunk template checked before rules, unconfirmed advisory still exit 0, setup command printed without execution. |
| pr-floor | pr_floor.py _options/cmd_pr_floor: paired flags, contextual body failure annotations and BLOCK, verification status disclosed even stale, optional GITHUB_STEP_SUMMARY append. |
| standing | standing.py cmd_standing and rule_checks/standing.py: root/document discovery, architecture root only, warnings versus blocking second-vendor/product policy; no ratification. |
| contract | contract.py cmd_contract and rule_checks/contract.py: major/minor of manifest, not release; repeated require last wins; mismatch direction and no lowered requirement workaround. Actual pass/fail/duplicate cases below. |
| charter | charter.py cmd_charter: optional last manifest override, output table before completeness failure, empty mapping fails. Actual empty-manifest failure below. |
| plan | plan.py cmd_plan: raw arbitrary file operand, no-charter empty pass, charter1.1 simplicity blocker, final JSON selector in dispatcher. Actual empty/block/error results below. |
| reviewer-count | reviewer_count.py cmd_reviewer_count and reviewers.py required_reviewer_count: nonblank single operand, clean tree, integer floor/conservative two; no review dispatch. CLI focused tests exercised clean/dirty. |
| finalize-review | finalize.py cmd_finalize_review/_finalize: input object/clean delta, distinct authentic passing reviewers, executable probe and package verification, stable tree checks, atomic attestation write after validation. Actual missing-operand refusal below; full finalization remains station work. |

This was not sixteen real writer executions. The semantic conclusions combine direct readback with safe actual invocations and isolated fixtures. Remote publication, merge, hook installation/removal and cleanup were deliberately not performed; their documented consequences were checked against unchanged implementation.

## 2. 全部主要命令的 help 與實際參數、模式、前置條件、結果、錯誤路徑及操作後果一致，並經獨立逐一核對。

Read all sixteen actual pages returned by ready launcher, not only keyword/snapshot assertions. Matched each row above for syntax, operand kinds, prerequisites, outputs/exits, effects and recovery. Important outcome boundaries visibly retained:
- push exposes loom.protectMain=false as host opt-out, separate native mode, matcher bypasses and no authorization.
- land exposes fetch/prune during unconfirmed sweep, merge before verification/cleanup failure, exit 0 even with "trunk not updated", named cleanup without sync, and next: cd after invoking worktree removal.
- sync-trunk says fetch warning may mean no synchronization despite exit 0.
- github-rules says template gating/unconfirmed is advisory; printed setup is not executed.
- pr-floor says summary append is a write and stale verification still passes body check.
- publish says no required checks is not testing and a remote write may precede failed observation; inspect delivery before retry.
- delivery enumerates actual state values, separates hook and ordinary JSON, and discloses malformed invocation text with --json.
- six old detailed pages retain substantial evidence/body/JSON/authenticity examples; new pages do not imply running a station or acquiring authority.
Actual ordinary inputs/outcomes (section 3) confirm empty plan text, blocking charter1.1, table with failure, contract mismatch, missing publication authority and missing merge acceptance. No discrepancy was found in the runtime pages themselves. The stale README finding under section 4 remains unresolved.

## 3. 既有文字呼叫、已發布 JSON 介面、退出狀態、檢查條件及授權行為保持相容；現有 JSON 支援範圍明確揭露，本輪不新增 JSON 介面。

Temporary probe outside the repository: `/Users/kouko/.conda/envs/dbt-redshift/bin/python3 /private/tmp/loom-help-acceptance-probe.py`.
Exit 0: `32 ready exact-help calls passed; 25 ordinary cases byte-identical to base; cold-ready 86 with no cache created`.
It invokes real checker subprocesses on candidate/base from an outside-repository directory using identical read-only fixture files, comparing the complete (exit,stdout,stderr) tuple. All 25 results are captured below. No live remote writer is exercised. The probe is temporary acceptance tooling, not a new committed executable.

The 49 focused tests include actual CLI errors/conditional notices/clean reviewer floor and handler bypass; the 45 consumer tests exercise preparation-v1 pass/block/usage/internal errors, notices, selector boundaries; delivery published/merged/local/failed/unconfirmed/no-required-checks states using isolated external-call fakes; actual host Stop feedback shapes, permission/non-authority boundaries and bounded deadlines. Reading those test assertions confirms exact preparation keys and delivery keys rather than inferring compatibility from a count. The captured base comparison independently confirms no changed streams/exits for the ordinary cases tested. JSON is only disclosed where already supported; no new serializer/selector/schema or handler change appears in the functional diff. This does not claim exhaustive real-network behavior across every operation.

## 4. 全部主要公開子命令提供清楚且可安全探索的說明，操作者能了解功能、必要輸入、結果與操作後果，而不因查閱說明執行實際工作。

Actual 32 ready-launcher invocations: every command in the sixteen-row table, each followed by exactly --help and -h, from /private/tmp/loom-help-acceptance-outside. All exit 0, stderr empty, finite stdout, both forms identical. Full text captures follow. The existing ready runtime was validated; no --repair provisioning was needed for these calls.

Cold runtime fixture: XDG_CACHE_HOME=/private/tmp/loom-help-acceptance-outside/cold-cache and PATH=/usr/bin:/bin, `/bin/sh <candidate>/loom-code/scripts/loom-python --ready push --help` returned 86, no stdout, prescribed repair diagnostic, and no cache directory created. This proves missing-ready handling, not downloading a fresh runtime.

Named focused test test_exact_help_never_dispatches_handlers ran successfully: all16x2 with handler/stdin/subprocess/socket/Path read/open/write tripwires outside repo; non-exact extra-argument calls hit ordinary dispatch. The runtime test test_all_command_help_uses_ready_runtime_without_repair also ran. Non-exact plan --help --json returned ordinary preparation usage error and matched base; help is safe only for exact forms, not combinations.

### Finding A4-1 — important, unresolved at tested commit
README.md:275-293 still lists only six available detailed help commands and states "Help for other commands ... remain future migrations". The actual checker has all sixteen. This is user-facing discovery guidance, not historical evidence; it contradicts this delivery and warrants AC4 partly despite safe actual help. Fix the current README guidance to describe all sixteen and distinguish unchanged six-command ordinary error hints from all-command help. Do not broaden the normal error stream.

### Finding A4-2 — nit, unresolved at tested commit
docs/loom/research/2026-11-13-cli-agent-design-guidelines.md:18 calls the intent "still-open"; lines88-118 retain the six-page baseline. The document already explicitly pins fbdc29a /3.72.0, so that table is a historical snapshot, not a false current runtime assertion. Clarify that it predates implementation and the narrowed scope decision, and point to current conformance evidence; preserve research history rather than rewriting it into present-day data.

No important-or-worse finding was dismissed by this tester; station supplied none as formally dismissed. Previously failed help checkpoint evidence was read as historical evidence and not overwritten or relabelled.

## Captured actual help and base-comparison outputs

The capture below was generated during this run, before either report file was written. All stdout/stderr strings are exact; assertions checked 32 help calls and 25 equality comparisons. Temporary absolute fixture paths are evidence only.

```json
{
  "tested_sha": "1ccb7f514ec63aaf2d02d90108ea5b67d65fe4b7",
  "help": [
    {
      "command": "intent",
      "help": "intent — check one intent's implemented rules\nUsage: intent <path> [--commit-msg <file>]\nSupply readable relative-to-working-directory or absolute paths. Repository\ncontext is resolved from the intent; the bundled manifest defines its schema.\n--commit-msg supplies design-reasoning evidence; it does not create a commit.\nChecks cover schema, map existence, product identifiers, design reasoning and\napplicable touched-interface/kind rules. Advisory stdout may precede a blocker;\nsuccess may have empty stdout.\nConditional interface recomputation needs a resolvable branch base; run on a\nchange branch rather than trunk and resolve missing trunk metadata as directed.\nExit 0 means these checks passed, Exit 1 reports\nBLOCK diagnostics on stderr, Exit 2 means arguments, files or internal failure.\nReads only; it neither creates nor confirms intent or authorizes delivery.\nCorrect the reported source artifact or path through its owning workflow and retry.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "intents",
      "help": "intents — inspect locally derived intent delivery states\nUsage: intents [<change-id>] [--remote <name>] [--metadata]\nRun in the repository. The remote defaults to origin and must be a safe literal.\nIdentifiers contain letters, digits, dots, underscores and hyphens; a selected\nID needs its canonical intent file. --metadata requires one ID.\nWithout an ID, lists active/indeterminate confirmed intents and may print nothing.\nWith an ID, reports its state. Tab-separated rows start with ID and state;\nnamed active rows add detail, and indeterminate rows add detail plus refresh\nadvice. Delivered --metadata rows append available commit/pr/committed_at\nkey=value fields (pr may be absent; dates are committer, not merge dates).\nOther rows may contain only two fields; there is no fixed three-column shape.\nExit 0 is a local-ref observation, not live freshness proof. Indeterminate gives\nexit 1 and refresh advice; Exit 2 means invocation or internal error on stderr.\nReads local Git only, never fetches. Refresh the selected remote-default ref\nexplicitly when needed, then retry; this does not perform delivery.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "intake",
      "help": "intake — check the selected station's current prerequisites\nUsage: intake <write-spec|write-plan> <change-id> [--json]\nRun inside the selected repository. Supply a change-id, not a file path;\naccepted identifiers contain only letters, digits, dots, underscores and\nhyphens. Canonical artifacts are resolved through the bundled contract.\n\nText results: exit 0 means the applicable prerequisites passed for this snapshot;\nit does not perform the station, authorize publication or verify the change.\nConditional interface-surfaces (...) information may appear on stdout for\nengineering intents or applicable needs-design=yes write-plan intake.\nThat information is advisory and may precede a later BLOCK; it is not a\nsuccess result. Other intake paths have no stdout payload.\n\nExit 1 reports BLOCK <rule>: <reason> on stderr. Supply or correct authentic\nrequired artifacts through their owning workflow, then rerun. Exit 2 means\ninvalid station/change-id/arguments or an internal failure; correct the\ninvocation or repository/environment from the diagnostic. These checks are\nread-only and synchronous; no previous pass waives the next check.\nStation and prerequisite guidance: <loom-code>/skills/write-plan/SKILL.md.\nThe intent needs a real confirmed date and active delivery state. A closed or\ndelivered intent requires a new intent; indeterminate delivery needs refreshed\nremote-default evidence. Conditional interface recomputation needs a resolvable\nbranch base on a change branch rather than trunk.\nOptional JSON: append --json as the final argument only. Exact --help/-h\nremains text; help combined with --json is checked as an ordinary invocation.\nDuplicate selectors are usage errors. Earlier --json tokens without a final\nselector retain their existing operand meaning; ./--json names a literal file.\n\nJSON stdout is one object plus newline; checker stderr is empty. Fields:\nschema_version: 1; command: plan|intake; status: passed|blocked|error;\ndiagnostics: ordered [{rule_id, message}]; notices: ordered strings;\nerror: null or {kind: usage|internal, message}. Empty arrays are [], not null.\nExit 0 means passed, 1 blocked, 2 error. Blocked includes rule diagnostics;\nerror has empty diagnostics. Notices may precede a blocker or internal error\nand never imply success. Status covers only this invocation's checks, not\nworkflow completion or authority. Do not depend on key order or message prose.\nLauncher/startup failures, termination and broken pipes are outside this\nin-process result guarantee. Read the actual process result; do not retry\nautomatically. Without --json, existing text streams and exits are unchanged.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "push",
      "help": "push — provide host-hook feedback or install native branch protection\nUsage: push --hook\n       push --install-git-hooks\n       push --remove-git-hooks\nOnly --hook reads PreToolUse JSON from stdin; invalid ordinary calls do not.\nThe host matcher handles command text beginning with literal git commit, git\nmerge or git push while the payload cwd is on main/master, with refusal exit 2\nunless repository-local loom.protectMain=false explicitly allows those commands.\nThis opt-out affects the host hook, not the separate native hooks below.\nMalformed/missing payload also exits 2. Publication reminders may emit a host\nJSON systemMessage on stdout and a diagnostic on stderr; reminder failures and\nunexpected top-level hook exceptions allow exit 0. It performs no publication.\n\nNative modes are explicit repository configuration operations. They read and\nrefuse a core.hooksPath override or unreadable setting without changing it.\nInstall validates local and live origin default metadata; it may create the\nGit hooks directory and writes three owned hooks: pre-commit, pre-merge-commit,\npre-push. The shared Git common directory's hooks affect all worktrees.\nRemove deletes only those owned files. Foreign/edited hooks and\nsymlinked locations are refused; preserve them and arrange hook-owner integration.\nNative success prints installed/removed on stdout, exit 0. Caught failures\nprint loom: diagnostics on stderr, exit 2, without BLOCK. Inspect origin and\nrepair default metadata as directed before retry. Native hooks protect main,\nmaster and the origin default branch, but are ordinary Git safeguards, not a\nsecurity boundary or proof of remote branch protection. Help grants no consent.\nGlobal options before the Git verb, wrappers and later compound commands can\nevade the host matcher. Native hooks do not intercept fast-forward merges or\nreset/rebase; Git options that skip hooks can bypass applicable native checks.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "publish",
      "help": "publish — publish an authorized branch and observe required CI\nUsage: publish --intent <absolute-intent-path> --title <text> --body-file <absolute-body-path>\nLegacy: publish --confirm-authorized --title <text> --body-file <absolute-body-path>\n\nPublication may perform a remote write (push and create/update a Ready PR).\n--intent must name this change's canonical, committed, confirmed intent with\nan existing valid automatic-publication authorization that remains unrevoked.\nThe legacy --confirm-authorized argument records an actual explicit user\npublication decision; it is not a way to supply missing consent. If neither\nauthorization exists, stop and obtain that decision. Help grants no authority.\nObservation grants neither publication nor merge authorization.\n\n--title is checked here only for nonblank text; title policy remains workflow guidance.\n--body-file must be an absolute path to a readable UTF-8 Markdown file.\nPrepare the body from the confirmed intent, current diff, review and actual\nverification evidence. Include each of these nine headings exactly once,\nin this order, with no other level-two headings. Each needs substantive visible\ncontent: at least eight alphanumeric characters, beyond a single ASCII token\nor template placeholder (Follow-ups may say None):\n## Context\n## Intended outcome\n## Scope\n## Decisions\n## Implementation\n## Behaviour change\n## Verification\n## Risks and rollback\n## Follow-ups\n\nUnder Verification include Verification status: <computed status>.\nThe checker reports valid, absent or stale (<reason>); if refused, copy the\nreported corrected Verification status: line into the body without inventing\na stronger status. Disclose actual instructed skips and missing evidence.\nWhen recorded, include Adversarial outcome: no program — <recorded reason>.\nDetailed body, skipped-step and risk requirements: <loom-code>/skills/ship/SKILL.md.\nThe checker requires a safe symbolic branch, one literal supported GitHub origin\nwithout redirect overrides, known nondiverged remote ancestry and unchanged\nHEAD/origin identity between operations. The PR base is the server default\nbranch. Correct named conditions, preserving work. Use trusted git/gh and\ncommitted selected content; an existing attestation must be committed.\nA temporary body snapshot is removed on return. The nonforce push can set\nupstream tracking; remote operations are not rolled back on later failure.\n\nResults: exit 0 completes publication and its required-check observation;\nexit 1 means blocked or unconfirmed; exit 2 means invocation or authorization\nerrors, or internal failures. Read the diagnostic to determine the next action;\nthe exit code alone is not a reason to retry.\nVerification output or a PR URL alone is not completion. Stderr progress is\nadvisory and can also contain errors; while CI is pending keep observing the\nsame process. Inspect the final exit and evidence. Exit 0 with\n\"No required checks registered\" means no checks registered, not tests passed.\nAn observation failure may follow a successful remote write. Before considering\nanother publish, run delivery --goal published --json to observe existing\nstate and follow its diagnostic; do not blindly repeat a write or switch routes.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "delivery",
      "help": "delivery — observe the selected delivery goal without writes\nUsage: delivery [--goal local|published|merged] [--intent <path>] [--json]\nRun inside the selected repository on its identified feature branch.\n--goal defaults to published. local checks that attributable paths are committed;\nit does not check finalization, attestation or verification. published checks the\nmatching Ready PR and required CI; merged checks merged delivery evidence.\n--intent optionally identifies the change's canonical committed intent (a\nrelative or absolute path); it does not create or grant authorization.\nLocal observation does not claim publication. Observation never authorizes\npublication or merge, and does not perform either action.\n\n--json emits the existing object on stdout:\nstate: observed delivery condition; reason: why it was classified that way;\nnext: suggested next action, subject to existing authorization;\nevidence: observations supporting the result; complete: whether the goal is met.\nA JSON object by itself, especially complete: false, is not proof of delivery.\nUse state, reason, next and evidence together with the process exit status.\nExit 0 means the selected goal was achieved; exit 1 means incomplete or\nunconfirmed; exit 2 means invocation/internal error. State values are local,\nuncommitted, unpublished, missing_pr, mismatched_pr, pending, failed, cancelled,\naction_required, published, merged and unconfirmed. Pending means wait and\nobserve again; other incomplete states require the stated next action.\nUnconfirmed means evidence is unavailable, not success. Correct errors using the\ndiagnostic. Re-observation grants no permission to retry a remote write.\nStderr progress is advisory and can also contain errors; inspect final results.\nMore workflow guidance: <loom-code>/skills/ship/SKILL.md.\nHook forms: delivery --hook; delivery --hook --host claude|codex.\nHook mode consumes host stdin and emits host-specific feedback with its own\nexit semantics; it is separate from ordinary --json. Do not mix hook forms\nwith observation options. Duplicate options are invalid. Malformed ordinary\ninvocations may report text on stderr even when --json was supplied.\nPublished/merged observation needs trusted git/gh from supported host install\nlocations, a literal GitHub origin, authenticated gh and network read access;\nmissing prerequisites can yield unconfirmed/exit 1. Published completion with\n\"No required checks registered\" does not mean tests passed.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "land",
      "help": "land — merge an accepted PR or clean up merged changes\nUsage: land --accepted-by <name>\n       land --cleanup <branch>\n       land --sweep [--confirm <token>]\nChoose exactly one form; --confirm applies only to sweep. Run in the repository\nwith trusted git/gh, eligible change branch/PR and live evidence/checks. A real\nmaintainer acceptance must already exist; the name or help supplies no consent.\nThe accepted name must match the committed intent originator or automatic\npublication authorizer; matching a name does not establish actual consent.\nExactly one open PR against the default branch must match HEAD, and its live\nbody must satisfy the nine-heading validator. Land polls all registered checks,\nincluding non-required checks, with at most 360 pending 10-second waits; network\ncalls and other stages add elapsed time. Failed/cancelled/action-required checks\nrefuse the merge. Absent/stale local verification is disclosed after merge,\nnot a gate that prevents it; no registered checks is not proof of testing.\nSee publish --help for the body heading order and content requirements.\nThe accepted form may squash merge remotely, verify, sync trunk, then delete\nthe change worktree and local/remote branch. Cleanup targets a named merged\nchange. Sweep computes candidates and a confirmation token; even without a\ntoken it fetches/prunes refs. A matching revalidated token enables deletion.\nDo not run cleanup when worktree preservation was requested.\nExit 0 can follow successful merge/cleanup even when best-effort trunk sync\nwas skipped or failed and stdout says \"trunk not updated\". Read the trunk\nresult; preserve work before independently resolving local trunk conditions.\nNamed cleanup never syncs trunk. Sweep listing also returns exit 0. Exit 1 reports\nrefusal or failed stage with BLOCK stderr, Exit 2 reports usage/internal errors.\nProgress/results appear on stdout. Merge can succeed before verification or\ncleanup fails: inspect remote merge and preserved work before corrective action;\nuse cleanup for an already merged change instead of blindly repeating a merge.\nDirty work and divergent local trunk are preserved/refused, not force-discarded.\nIf cleanup removes the invoking worktree, follow the printed next: cd command\nto leave the removed working directory.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "sync-trunk",
      "help": "sync-trunk — bring a clean change branch onto fetched trunk\nUsage: sync-trunk\nRun on a clean attached change branch, not trunk, with trusted Git and resolvable\ntrunk metadata. Preserve and commit work before resolving a dirty-tree refusal.\nFetches origin, then may rebase safe unpublished commits or merge trunk. Refuses\npreflight conflicts/collisions; abort/rollback is attempted after mutation failure,\nnot guaranteed. Results appear on stdout; WARN/BLOCK diagnostics on stderr.\nExit 0 includes fetch WARN with no sync, already-current and completed sync.\nExit 1 means BLOCK review.sync; Exit 2 means arguments/internal error. Read the\nwarning before assuming synchronization. Resolve origin/network or conflicts\nthrough normal Build and retry. Changed content needs full tests/probes again;\nrebased commit identities require updating pinned references before review.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "github-rules",
      "help": "github-rules — inspect GitHub trunk protection as advisory information\nUsage: github-rules [--print-setup]\nRun in the repository with origin metadata and authenticated gh read access.\nUses network reads to report present, absent or unconfirmed rules on stdout.\nIt first requires the PR-floor workflow template on trunk; \"template not on\"\ninstructions can return before inspecting any rules. Setup text may also appear\nwithout --print-setup when missing rules are found.\nExit 0 includes unavailable/unconfirmed protection; it does not prove protection\nor verification. Exit 2 means invalid arguments or unexpected internal failure\non stderr. Restore origin, authentication/network and read access, then rerun.\n--print-setup prints a setup command when prerequisites permit, without executing\nit. It never changes GitHub rules. Running printed setup is a separate mutation\nrequiring its own authorization; help grants none.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "pr-floor",
      "help": "pr-floor — validate a PR body and disclose verification in CI\nUsage: pr-floor --body-file <file> --base <sha> --head <sha> [--branch <name>]\nSupply unique paired flags, a readable body file (relative to the working\ndirectory or absolute), required base/head Git evidence and optional branch.\nRun in the repository. Emits CI error/notice annotations on stdout. Body\nstructure failures also report BLOCK ci.pr-floor on stderr, exit 1. Exit 0\nmeans the body passed; recomputed verification may still be stale or absent.\nExit 2 means invocation, unreadable file or internal failure. Correct named\nheadings or Git context; never fabricate stronger verification status.\nCan append a verification line to GITHUB_STEP_SUMMARY when set, so it is not\nstrictly read-only. It runs no PR-controlled commands, tests or reviews and\ndoes not authorize publication or merge.\nSee publish --help for the body heading order and content requirements.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "standing",
      "help": "standing — check applicable standing-document policy for one intent\nUsage: standing <path-to-intent>\nSupply one readable relative-to-working-directory or absolute intent path;\nrepository context is resolved from that file. Checks existence of PRINCIPLES.md,\nDESIGN.md and root ARCHITECTURE.md; reads PRINCIPLES.md content for product\nintents and KICKOFF-DEFAULTS.md standing/second-vendor policy records. Principles\nand design discovery checks root first, then docs/loom; architecture is root-only.\nWarnings on stderr can coexist with passing checks and empty stdout. Exit 0\nmeans implemented policy checks passed, not semantic certification of documents.\nExit 1 reports BLOCK diagnostics for second-vendor/product-principles policy;\nExit 2 means missing file, invalid arguments or internal failure. Correct the\nauthentic policy/document record through its owning workflow, then rerun.\nRead-only; does not ratify documents or perform review.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "contract",
      "help": "contract — check compatibility with the bundled contract manifest\nUsage: contract --require <major.minor>\nSupply a numeric major.minor requirement. Reads the manifest in effect; a\nmatching major and sufficiently high minor pass. Exit 0 prints current and\nrequired versions on stdout; Exit 1 reports BLOCK contract.requires on stderr;\nExit 2 means malformed/missing arguments or internal failure. Follow the\ndiagnostic: an older major requirement needs the consuming plugin's\nrequires-contract updated to a supported major; update loom-code when a newer\nmajor/minor is required. Do not lower a requirement just to pass. Then retry.\nRead-only: this does not check plugin release version, provision\nruntime, run station prerequisites or authorize a later operation.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "charter",
      "help": "charter — render and validate artifact charter rows\nUsage: charter [--manifest <path>]\nDefaults to the contract manifest in effect. An override is a readable YAML\npath, relative to the working directory or absolute. Repeated --manifest uses\nthe last path. No repository mutation occurs.\nPrints a Markdown table on stdout in manifest artifact order, including an\nempty table for missing/empty artifacts. Exit 0 means implemented row checks\npassed; Exit 1 reports BLOCK contract.charter-complete on stderr. A table can\ncoexist with failure and is not an approval. Exit 2 means file, arguments or\ninternal failure. Correct the reported manifest charter fields and retry.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "plan",
      "help": "plan — check the implemented field caps on one named file\nUsage: plan <path-to-plan.md> [--json]\nSupply a readable file path, relative to the working directory or absolute;\nthis command does not resolve a change-id or select a canonical plan.\n\nThe check applies field caps only when the file has a charter: frontmatter\nkey. Charter 1.1 or later also requires a valid Simplicity check record.\nA file without that key, including an empty file, may pass. Passing does not\napprove the plan, prove its requirements are complete or verify the change.\n\nText results: exit 0 has no success payload on stdout; the implemented checks on\nthe named file passed. Exit 1 reports BLOCK plan.field-caps on stderr;\ncorrect the reported field and rerun. Exit 2 means a missing/unreadable file,\ninvalid invocation or internal failure; correct the path, access or invocation\nfrom the diagnostic. No artifact is rewritten and no later station runs.\nPlanning guidance: <loom-code>/skills/write-plan/SKILL.md.\nOptional JSON: append --json as the final argument only. Exact --help/-h\nremains text; help combined with --json is checked as an ordinary invocation.\nDuplicate selectors are usage errors. Earlier --json tokens without a final\nselector retain their existing operand meaning; ./--json names a literal file.\n\nJSON stdout is one object plus newline; checker stderr is empty. Fields:\nschema_version: 1; command: plan|intake; status: passed|blocked|error;\ndiagnostics: ordered [{rule_id, message}]; notices: ordered strings;\nerror: null or {kind: usage|internal, message}. Empty arrays are [], not null.\nExit 0 means passed, 1 blocked, 2 error. Blocked includes rule diagnostics;\nerror has empty diagnostics. Notices may precede a blocker or internal error\nand never imply success. Status covers only this invocation's checks, not\nworkflow completion or authority. Do not depend on key order or message prose.\nLauncher/startup failures, termination and broken pipes are outside this\nin-process result guarantee. Read the actual process result; do not retry\nautomatically. Without --json, existing text streams and exits are unchanged.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "reviewer-count",
      "help": "reviewer-count — compute the required independent reviewer floor\nUsage: reviewer-count <change-id>\nRun inside the selected repository with a clean tree and committed functional\ncontent. Supply one nonblank change-id operand. Preserve work and finish and\ncommit the change before requesting the floor; do not discard files to pass.\n\nResults: exit 0 prints the integer floor and newline on stdout. Obtain that\nmany independent reviewers; the number is not a verdict or proof of review,\nacceptance, finalization or completed verification. The policy conservatively\nrequires two when it cannot classify the complete committed delta.\nExit 2 means missing/extra operands, a dirty tree or an internal failure;\nuse the diagnostic to correct the invocation or repository condition, then\nrerun. This read-only command neither dispatches reviewers nor writes evidence.\nReview guidance: <loom-code>/skills/closing-review/SKILL.md.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    },
    {
      "command": "finalize-review",
      "help": "finalize-review — verify committed content and generate an attestation\nUsage: finalize-review <change-id> --input <review-input.json>\n<change-id> identifies the change; it is not a file path. --input names a\nreadable JSON file (relative to the working directory or absolute). Keep this\ntemporary input outside the repository so the checkout stays clean.\n\nRun inside the selected repository after committing functional content, intent,\nplan, required acceptance report and adversarial programs. Resolve the trunk\nused for the branch diff. Review the current HEAD's content; the diff base is\nthe comparison starting point, not the reviewed target. Compute the required\nreviewer count with reviewer-count <change-id>; use distinct real reviewers\nindependent of the writer. Preserve each original verdict and its findings;\nnever invent identities, passing judgments, probe evidence or authorization.\n\nIllustrative JSON shape only — replace placeholders with authentic output;\nthis is not ready-to-submit review evidence:\n{\n  \"verdicts\": [{\n    \"reviewer\": \"<actual reviewer id>\", \"vendor\": \"<actual vendor>\",\n    \"model\": \"<actual model>\", \"lens\": \"<actual review lens>\",\n    \"verdict\": \"<original verdict>\", \"findings\": []\n  }],\n  \"findings\": [],\n  \"adversarial\": [{\"command\": \"<artifact-bound execution command>\",\n                   \"artifact\": \"<committed repository-relative program path>\"}]\n}\nRepeat verdict rows for the required reviewers. Empty findings arrays are\nappropriate only when the source has none; top-level findings carry every\nunresolved adversarial finding from Build. Finalization accepts only PASS or\nPASS_WITH_NOTES verdicts; a failing judgment requires the normal fix/review\nroute, not relabelling. Preserve scores and notes from the actual review too.\nFor a selected outside reviewer, retain its complete external_review runner\nresult, dimension_scores, notes and reviewed_sha; review_target_sha is the\nconcrete HEAD supplied to that review, not the diff base. The raw review output\nmust match the attributed verdict. Do not manufacture a receipt.\n\nUse the actual committed probe and supported runner command from Build's\nhandoff. Where required, copy the reviewer's probe confirmation as\n\"confirmation\": {\"reviewer\": \"<id>\", \"reviewed_sha\": \"<reviewed commit>\",\n                 \"quote\": \"<whole output lines naming this probe>\"}.\nIf the adversary actually recorded no program, replace the adversarial list\nwith [{\"no_program\": \"<observed reason>\"}]; never mix it with program rows.\nThe reason must be nonblank, single-line, trimmed and contain no HTML comment.\nThis observed outcome is not a bypass. Follow existing explicit skip\ninstructions: when reviewers, adversarial or package-tests were skipped by\ninstruction, skip finalization and disclose absent verification. The checker\nstill recomputes any automatic narrow-change simplification.\nComplete outside-review receipt and probe rules: <loom-code>/skills/closing-review/SKILL.md.\n\nResults: exit 0 announces the generated attestation; exit 1 reports a BLOCK\nrule and reason; exit 2 reports invocation/internal errors. Correct malformed\nJSON or missing inputs using the diagnostic; obtain missing authentic evidence\nthrough the normal review workflow. A passed stage is not overall success.\nStderr progress is advisory and can also contain errors: while running, keep\nobserving the same process; inspect its final exit and generated evidence.\nFinalization executes the package suite and declared adversarial commands and\natomically writes the generated attestation. It grants no publication authority.\nCommit that generated attestation before publication.\n\nNo validation or publication occurred: help only, exit 0.\nUse \"<loom-code>/scripts/loom-python\" --ready <command> <arguments>.\nReplace <loom-code> with the installed loom-code plugin directory; launcher\nruntime readiness is still required. Bundled paths above are plugin-relative.\n--ready with missing runtime exits 86 without provisioning. --repair may use\nnetwork and write runtime caches/locks before checker help; it is not offline.\nFor a literal file operand named --help or -h, use ./--help or ./-h.\n",
      "spellings_identical": true,
      "exit": 0,
      "stderr": ""
    }
  ],
  "compatibility": [
    {
      "args": [
        "plan",
        "/private/tmp/loom-help-acceptance-outside/empty.md"
      ],
      "result": {
        "exit": 0,
        "stdout": "",
        "stderr": ""
      },
      "equal_base": true
    },
    {
      "args": [
        "plan",
        "/private/tmp/loom-help-acceptance-outside/empty.md",
        "--json"
      ],
      "result": {
        "exit": 0,
        "stdout": "{\"schema_version\": 1, \"command\": \"plan\", \"status\": \"passed\", \"diagnostics\": [], \"notices\": [], \"error\": null}\n",
        "stderr": ""
      },
      "equal_base": true
    },
    {
      "args": [
        "plan",
        "/private/tmp/loom-help-acceptance-outside/bad-plan.md"
      ],
      "result": {
        "exit": 1,
        "stdout": "",
        "stderr": "BLOCK plan.field-caps: Simplicity check section missing or empty (charter 1.1)\nHelp: \"<loom-code>/scripts/loom-python\" --ready plan --help (replace <loom-code> with the installed loom-code plugin directory).\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "plan",
        "/private/tmp/loom-help-acceptance-outside/bad-plan.md",
        "--json"
      ],
      "result": {
        "exit": 1,
        "stdout": "{\"schema_version\": 1, \"command\": \"plan\", \"status\": \"blocked\", \"diagnostics\": [{\"rule_id\": \"plan.field-caps\", \"message\": \"Simplicity check section missing or empty (charter 1.1)\"}], \"notices\": [], \"error\": null}\n",
        "stderr": ""
      },
      "equal_base": true
    },
    {
      "args": [
        "plan",
        "/private/tmp/loom-help-acceptance-outside/missing",
        "--json"
      ],
      "result": {
        "exit": 2,
        "stdout": "{\"schema_version\": 1, \"command\": \"plan\", \"status\": \"error\", \"diagnostics\": [], \"notices\": [], \"error\": {\"kind\": \"usage\", \"message\": \"no such plan file: /private/tmp/loom-help-acceptance-outside/missing\"}}\n",
        "stderr": ""
      },
      "equal_base": true
    },
    {
      "args": [
        "intake",
        "invalid",
        "case",
        "--json"
      ],
      "result": {
        "exit": 2,
        "stdout": "{\"schema_version\": 1, \"command\": \"intake\", \"status\": \"error\", \"diagnostics\": [], \"notices\": [], \"error\": {\"kind\": \"usage\", \"message\": \"unknown station 'invalid'; intake covers write-spec and write-plan.\"}}\n",
        "stderr": ""
      },
      "equal_base": true
    },
    {
      "args": [
        "contract",
        "--require",
        "2.3"
      ],
      "result": {
        "exit": 0,
        "stdout": "contract 2.3.1 satisfies requires-contract >=2.3\n",
        "stderr": ""
      },
      "equal_base": true
    },
    {
      "args": [
        "contract",
        "--require",
        "2.99"
      ],
      "result": {
        "exit": 1,
        "stdout": "",
        "stderr": "BLOCK contract.requires: this repo ships loom contract 2.3.1, but >=2.99 is required — 請更新 loom-code。\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "contract",
        "--require",
        "2.99",
        "--require",
        "2.3"
      ],
      "result": {
        "exit": 0,
        "stdout": "contract 2.3.1 satisfies requires-contract >=2.3\n",
        "stderr": ""
      },
      "equal_base": true
    },
    {
      "args": [
        "charter",
        "--manifest",
        "/private/tmp/loom-help-acceptance-outside/empty.yaml"
      ],
      "result": {
        "exit": 1,
        "stdout": "| artifact | answers | readers | must | must not → goes to | sign-off | edits after |\n| --- | --- | --- | --- | --- | --- | --- |\n",
        "stderr": "BLOCK contract.charter-complete: manifest carries no artifacts: mapping (absent or empty) -- every charter row is missing.\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "delivery",
        "--goal",
        "bad",
        "--json"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "delivery: --goal must be local, published or merged\nHelp: \"<loom-code>/scripts/loom-python\" --ready delivery --help (replace <loom-code> with the installed loom-code plugin directory).\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "delivery",
        "--hook",
        "--host",
        "bad"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "delivery: use --hook alone or --hook --host claude|codex\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "push"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "push expects --hook, --install-git-hooks or --remove-git-hooks.\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "push",
        "--hook"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "push --hook expects a PreToolUse JSON payload on stdin.\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "publish"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "publish: --intent or --confirm-authorized is required for publication authorization\nHelp: \"<loom-code>/scripts/loom-python\" --ready publish --help (replace <loom-code> with the installed loom-code plugin directory).\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "land"
      ],
      "result": {
        "exit": 1,
        "stdout": "",
        "stderr": "BLOCK land.merge: acceptance not recorded; pass --accepted-by <name> after the maintainer accepts; next: Inspect the merge diagnostics and resolve the named condition before retrying land; preserve work and do not switch merge routes.\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "sync-trunk",
        "extra"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "sync-trunk takes no arguments; run it from the change worktree.\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "github-rules",
        "extra"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "usage: loom_checker.py github-rules [--print-setup]\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "pr-floor"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "usage: loom_checker.py pr-floor --body-file <f> --base <sha> --head <sha> [--branch <name>]\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "standing"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "standing needs a path to the intent file.\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "intent"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "intent needs a path to the intent file.\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "intents",
        "--metadata"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "--metadata requires one change-id.\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "reviewer-count"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "reviewer-count needs one change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready reviewer-count --help (replace <loom-code> with the installed loom-code plugin directory).\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "finalize-review"
      ],
      "result": {
        "exit": 2,
        "stdout": "",
        "stderr": "finalize-review needs a change-id.\nHelp: \"<loom-code>/scripts/loom-python\" --ready finalize-review --help (replace <loom-code> with the installed loom-code plugin directory).\n"
      },
      "equal_base": true
    },
    {
      "args": [
        "plan",
        "--help",
        "--json"
      ],
      "result": {
        "exit": 2,
        "stdout": "{\"schema_version\": 1, \"command\": \"plan\", \"status\": \"error\", \"diagnostics\": [], \"notices\": [], \"error\": {\"kind\": \"usage\", \"message\": \"no such plan file: --help\"}}\n",
        "stderr": ""
      },
      "equal_base": true
    }
  ],
  "cold_ready": {
    "exit": 86,
    "stdout": "",
    "stderr": "loom-python: checker runtime is missing or invalid; run loom-python --repair with the same arguments in an agent station.\n",
    "cache_created": false
  }
}
```
