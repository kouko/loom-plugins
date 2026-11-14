# Suggested next steps — acceptance test evidence

Tried on 2026-11-14, in a clean copy of the project at 32b5ce84f2fbebeda3d7726b72bb8010c9e5cc99.

## Identity, setup and boundaries

Independent acceptance tester; not the implementer or adversary. Original source
worktree: `/private/tmp/loom-cli-next-guidance`; untouched tested worktree:
`/private/tmp/loom-next-acceptance-32b5ce8`. Base:
`c271cc43d2bff6b34cd7012e260e58eeb42f0eaf`.
The intent is engineering, so the five Acceptance rows are the report rows;
the declared interface scenarios were also walked below.
Read the acceptance agent contract, report template, charter, intent, spec,
plan, README setup, common CLI guide and changed station guidance first.

```sh
git worktree add /private/tmp/loom-next-acceptance-32b5ce8 32b5ce84f2fbebeda3d7726b72bb8010c9e5cc99
cd /private/tmp/loom-next-acceptance-32b5ce8
loom-code/scripts/loom-python --repair --script checked_readonly.py contract --require 2.1
```

Setup exit 0, stderr empty; stdout:

```json
{"schema_version": 1, "command": "contract", "status": "passed", "diagnostics": [], "notices": [], "error": null, "data": {"contract_version": "2.3.1", "required_version": "2.1", "compatible": true}, "suggested_next": null}
```

This follows README setup using the existing runtime cache. Subsequent calls
used `--ready`; no installed plugin update, dependency installation into conda,
paid CLI, remote write, publication or merge occurred. Real-source fixtures and
injected copies were retained. No production or test source was changed.

## 1. 全體 CLI 的下一步建議原則與分批範圍可核對，清楚區分首批已交付流程、既有建議及未遷移介面，不宣稱全部命令已完成統一。

How: independently ran each registry command's exact help using the real
source launcher. The temporary uncommitted replay harness imports only the
existing fixture builder, then runs the actual launcher as a subprocess.

```sh
python3 /private/tmp/loom-next-acceptance-replay.py > /private/tmp/loom-next-acceptance-replay.log
# Per command, actual argv:
loom-code/scripts/loom-python --ready <command> --help
```

Observed inventory (each exit 0, no stderr):

```text
intent intents intake push publish delivery land sync-trunk github-rules
pr-floor standing contract charter plan reviewer-count finalize-review
16 exact helps; suggested_next appears only in contract/reviewer-count help.
```

Relevant actual help span:

```text
suggested_next: advisory string for blocked/error, null for passed. Advice is
optional for consumers; ignore missing, blank or non-string advice. It changes
neither the result nor authorization and must not trigger automatic execution.
Text refusal/error results append Suggested next step: on stderr.
```

Compared with `loom-code/references/cli-results.md` inventory and shared
principles: sixteen commands, five direct JSON interfaces, two checked
consumers, only two migrated suggestions. It explicitly retains delivery.next,
plan/intake shapes and existing publish/land/launcher remedies. No all-command
migration or measured performance claim was found in the delivered guide.

## 2. 相容性與審查人數兩個流程的已知拒絕及錯誤能提供與原因相符的處理建議；沒有可靠修復方式時保留未知並指出可查證事項，不編造修復或宣稱可直接繼續。

How: replay harness ran direct text, direct final `--json`, and checked calls
for contract; checked and direct JSON reviewer calls used a real temporary Git
repository built by the existing fixture. All ordinary JSON outcomes had one
stdout object and empty stderr. Direct text advice matched the JSON string.

```sh
loom-code/scripts/loom-python --ready contract --require 2.1
loom-code/scripts/loom-python --ready contract --require 2.99 --json
loom-code/scripts/loom-python --ready contract --require 0.5 --json
loom-code/scripts/loom-python --ready contract --require bad --json
loom-code/scripts/loom-python --ready --script checked_readonly.py contract --require <same operand>
loom-code/scripts/loom-python --ready --script checked_readonly.py reviewer-count fixture
```

| Scenario | Exit | Observed facts and advice |
|---|---|---|
| Supported 2.1 | 0 | passed, compatible true, suggestion null; text success unchanged |
| Unsupported higher minor 2.99 | 1 | blocked, compatible false; diagnostic names updating loom-code |
| Unsupported lower major 0.5 | 1 | blocked, compatible false; diagnostic says consuming plugin declares an old major and must update its requires-contract |
| Invalid version bad | 2 | usage, all domain data null; inspect operand/manifest issue and help |
| Clean initial change | 0 | reviewer floor 2, null suggestion |
| Clean committed usage clarification | 0 | reviewer floor 1, null suggestion |
| Outstanding work | 2 | usage, null floor; preserve outstanding work, select intended repository, establish clean completed change |
| Outside Git repository | 2 | usage, null floor; same repository/input category advice with original nonrepository diagnostic |

Both version refusals suggested:
`Update the plugin identified by the contract diagnostic, then recheck supported requirements.`
This follows the diagnostic and does not always prescribe a loom-code update.

Internal failure was **injected, not a naturally occurring producer failure**:
in a separate temporary script-tree copy, restored the original checker entry
and appended a replacement contract handler raising
`RuntimeError("acceptance injected computation failure")`. Actual copied launcher
text and JSON calls both exited 2. Text stdout empty; JSON stderr empty,
`error.kind` internal and all domain data null. Actual advice:

```text
Investigate the reported failure and preserve outstanding work; no reliable repair is known.
```

## 3. agent 能區分工具判定與後續建議；建議的有無或內容不改變原結果、既有拒絕或必要授權，不觸發自動執行、重試或文字備援。

How: separate-copy injection through the actual checked consumer subprocess
and copied launcher; clean exact source copy remained untouched.

```sh
python3 /private/tmp/loom-next-acceptance-faults.py > /private/tmp/loom-next-acceptance-faults-final.log
```

The uncommitted harness copies the script tree to a new temporary directory,
replaces only that copy's child checker with controlled output, increments a
fixture child counter per execution, and checks a hostile `touch` suggestion
never creates its marker. This is deliberate observation injection, not proof
that the real producer emitted hostile/malformed output. The consumer and
launcher themselves are real delivered copies. Accepted raw JSON contains a
numeric extension `1.234567890123456789`; it remained byte-for-byte unchanged
apart from the documented final newline. Every injected child case executed once.

| Injected observation | Exit | Result |
|---|---|---|
| Advice absent, null, empty, whitespace, integer, list, object | 0 | Core passed result accepted; optional value/raw output preserved |
| Hostile shell-looking advice on passed | 0 | Preserved as string, marker absent |
| Hostile advice on blocked | 1 | Original blocked core/diagnostic preserved, marker absent |
| Hostile advice on internal error | 2 | Original error core preserved, marker absent |
| Invalid core status with hostile advice | 2 | Empty stdout; `checked-readonly: invalid status`; locally generated investigation suggestion |
| Malformed child JSON | 2 | Empty stdout, parse diagnostic, local output-contract suggestion |
| Unexpected child stderr | 2 | Empty stdout, original unexpected-stderr diagnostic, local output-contract suggestion |
| Child startup exit 86 | 86 | Empty stdout, original runtime-unavailable diagnostic, local runtime suggestion |
| Sleeping child | 2 | Empty stdout; actual configured 30-second timeout, elapsed 30.10 seconds |

Timeout output:

```text
checked-readonly: checker timed out after 30 seconds; investigate before rerunning
Suggested next step: Investigate the checker runtime and preserve outstanding work before deliberate re-execution.
```

This used a sleeping injected child, not a shortened timeout or mocked timeout
exception. No retry or text fallback was observed. The separate original first
run before adding producer-internal coverage also passed and is retained in
`/private/tmp/loom-next-acceptance-faults.log`; final complete run is authoritative.
The configured subprocess timeout is not an absolute process-creation deadline.

Existing focused entry test additionally covered request mismatch, invalid
types, missing required fields, duplicate keys, NaN, contradictory result/exit,
Unicode/OSError/deep-JSON faults, Python import isolation and exact-help no-child.
Actual local checked calls with empty arguments, `plan`, or caller-supplied
`--json` exited 2 with empty stdout and local input-correction advice; exact
script help exited 0 and explained optional advice without inventing a result.

Station guidance was read alongside these observations: core accepted result
prerequisites remain first, optional suggestions are advisory only, and missing
useful advice retains diagnostics. This checks executable tool behavior plus
delivered instructions; it does **not** measure whether an LLM host obeys those
instructions or improves its resolution rate, speed, tokens or cost.

## 4. 既有判定、退出碼、已發布必要資料欄位、審查政策、授權、宿主信任及遠端操作查證行為保持相容；首批建議不引入新的寫入副作用，也不破壞既有下一步建議。

Real replay took SHA-256 snapshots of all fixture files excluding Git internals
and interpreter bytecode before/after each actual CLI call. Every snapshot
matched. Deliberate fixture commits/dirty changes occur between calls, not from
the helper. Exact source worktree `git status --porcelain` remained empty and
HEAD remained the tested SHA after all execution. Runtime preparation is the
documented cache-owning setup step, not a claim that repair never writes.

Focused commands, using the existing locked dependency cache:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_checked_readonly.py loom-code/tests/test_preparation_json.py loom-code/tests/test_loom_checker_cli.py -q -rs
# 48 passed in 15.49s; no skips

uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_delivery.py loom-code/tests/test_codex_hook_trust_contract.py loom-code/tests/test_ship_station_text.py::test_ship_text_separates_authorization_from_acceptance loom-code/tests/test_loom_publish.py::test_publish_requires_authorization_and_absolute_body loom-code/tests/test_loom_publish.py::test_publish_progress_failure_preserves_authority loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized -q -rs
# 15 passed in 7.86s; no skips
```

The first non-escalated uv attempt failed acquiring its existing cache lock
(`Operation not permitted`); authorized cache-access execution above succeeded.
That environment failure is not a behavioral failure or skipped criterion.

Relevant passing coverage: preparation envelopes and late-failure cleanup,
legacy plan/intake shape, direct text success, delivery JSON `next`, published
facts/exit distinctions, future unknown numeric fields, floor 1/2 and dirty
rejection; delivery's missing authorization/remote unavailable/newer local HEAD,
PR/check reconciliation and actionable next; publish authorization and progress
failure; Codex hook trust instructions and synchronized release metadata.
Remote responses in delivery/publish tests are controlled fixtures: no live
remote operation or installed-host trust approval was performed.

Diff inspection confirmed no domain policy handlers changed in the tested
range; only bounded rendering/consumer advice code changed. This corroborates,
and does not replace, the executed compatibility checks.

## 5. help、流程說明及獨立 dogfood 證據符合首批實作，涵蓋正常、明確拒絕與錯誤，並清楚揭露沒有建議或尚未驗證的情況。

Independent real launcher replay finished:

```text
PASS real launcher inventory, parity, reviewer states, local usage, and no-write snapshots
PASS separate-copy injection, one execution per observation, hostile marker absent
```

All twelve spec scenarios were covered: discovery, compatible/incompatible
observation, reviewer result, invalid input/repository, injected internal
failure, unknown observation, legacy/unusable advice, local usage, startup and
actual configured timeout. Reviewer and contract successful observations emit
null advice; no absent suggestion was treated as failure or invented recovery.
README/common-guide claims match these exercised surfaces. Full sixteen helps
are retained only in the temporary log; relevant spans and exit inventory are
recorded above rather than pasted wholesale.

Retained provenance:

- Real harness/log: `/private/tmp/loom-next-acceptance-replay.py`, `/private/tmp/loom-next-acceptance-replay.log`.
- Real Git fixture: `/private/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-next-acceptance-fixture-v5ebhvp1`.
- Injection harness/final log: `/private/tmp/loom-next-acceptance-faults.py`, `/private/tmp/loom-next-acceptance-faults-final.log`.
- Final injected script copy: `/private/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-next-acceptance-injected-3azncif5`.

No important-or-worse dismissed findings were supplied. No instruction-based
skips exist. The station says package-tests is not skipped and finalize-review
will run; this witness deliberately did not run the full package suite. The
automated test suite runs before acceptance and blocks acceptance on failure.
Pending finalization/CI is not reported as passed here. No new committed
executable probe, source/test edit, repair or installed-plugin change was made.

## Decision disclosure and evidence-only commit

The report discloses the material agent choices from spec/plan: two-interface
scope, shared renderer, category-based honest advice, optional unusable advice
and raw preservation, unrenamed legacy shapes, minor synchronized release and
test boundaries. Exact advisory naming remains user-decided, not attributed to
the agent. Commit classification: routine evidence capture; no new durable
decision/learning/gotcha requiring memory trailers. The exact commit message
was scanned with the git-memory deterministic privacy gate; no ambiguous
private-party identifier requiring a semantic judge was included.
