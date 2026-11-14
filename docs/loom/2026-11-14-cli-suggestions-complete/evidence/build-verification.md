# Build verification — complete CLI advisory guidance

## Scope and checkpoint

- Intent: [confirmed scope](../../intent/2026-11-14-cli-suggestions-complete.md); [spec](../spec.md); [plan](../plan.md).
- Comparison base: `adcd4cbfa468b374b5f8e0b9363adf0304b53e33` (main, loom-code 3.78.0).
- Implementation and help checkpoint before this release packet: `5e385830380e96123d261841854e168e484d0083`.
- Release packet: loom-code 3.79.0; canonical Claude manifest changed, three derived manifests generated with `python3 scripts/sync_codex_manifests.py --all`. `--all --check` exited 0. Localized README changes are version strings only.
- This is the implementer's bounded Build handoff, not independent acceptance or a generated closing attestation. No workflow step was skipped.

## Test-first implementation and focused verification

Each row ran the named test modules in full unless a single existing release guard is explicitly identified. Counts are invocation results, not unique tests; overlapping suites must not be summed. All successful focused runs had zero skips.

| Packet | Observed RED | Observed GREEN | Existing modules / retained session logs |
|---|---|---|---|
| W1-01 | 6 failed, 57 passed | 63 passed; final refactor rerun 63 passed in 24.65s | `test_loom_checker_cli.py`, `test_preparation_json.py`, `test_checked_readonly.py`, `test_loom_python_runtime.py`; `/private/tmp/loom-all-w1-red.txt`, `/private/tmp/loom-all-w1-green-final.txt` |
| W2-01 | 11 failed, 38 passed | 91 passed in 103.69s | `test_delivery.py`, `test_delivery_stop.py`, `test_preparation_json.py`, authorized whole CLI module; `/private/tmp/loom-all-w2-red.txt`, `/private/tmp/loom-all-w2-green.txt` |
| W3-01 | 8 failed, 43 passed | 51 passed in 35.91s | `test_sync_trunk.py`, `test_github_rules.py`; `/private/tmp/loom-all-w3-01-red.txt`, `/private/tmp/loom-all-w3-01-green.txt` |
| W3-02 | 3 failed, 47 passed; strengthened stream-fault case separately failed before source edits | 50 passed in 6.52s | `test_loom_checker_standing.py`, `test_pr_floor.py`, `test_pr_floor_workflow.py`; `/private/tmp/loom-all-w3-02-red.txt`, `/private/tmp/loom-all-w3-02-write-red.txt`, `/private/tmp/loom-all-w3-02-green.txt` |
| W3-03 | 1 failed, 134 passed | 135 passed in 57.57s | `test_land_sweep.py`, `test_land_cleanup.py`, `test_land_merge.py`, `test_loom_publish.py`; `/private/tmp/loom-all-w3-03-red.txt`, `/private/tmp/loom-all-w3-03-green.txt` |
| Delivery usage fix | 2 failed, 89 passed | 91 passed in 103.48s | Whole CLI, delivery, Stop and preparation modules; `/private/tmp/loom-all-delivery-usage-red.txt`, `/private/tmp/loom-all-delivery-usage-green.txt` |
| W4-01 | Documentation/help only; no artificial RED | 48 passed; final rerun 48 passed in 0.22s; additional public-entry replay modules 60 passed in 21.40s | `test_write_plan_station_text.py`, `test_loom_runtime_skill_commands.py`, `test_closing_review_recovery_rules.py`; additional whole CLI/preparation/runtime modules; `/private/tmp/loom-all-w4-tests-final.txt`, `/private/tmp/loom-all-w4-public-replays.txt` |
| W5-01/02 | Existing release metadata guard: 1 failed after changing only expected version | Same guard 1 passed; whole `test_write_plan_station_text.py`: 43 passed in 0.20s | `/private/tmp/loom-all-w5-version-red.txt`, `/private/tmp/loom-all-w5-version-green.txt`, `/private/tmp/loom-all-w5-green.txt` |

Focused command form:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest <named whole modules above> -q -rs
```

The version RED/GREEN selected the existing `test_current_release_metadata_is_synchronized` guard before the whole-module GREEN. The W3-02 stream-fault case initially passed because it did not observe an advice attempt; it was strengthened to require that attempt and failed before production changes. Existing assertions were extended for intended output additions, not removed or skipped to obtain GREEN.

## Coverage and direct source replays

The [CLI result guide](../../../../loom-code/references/cli-results.md#command-coverage-and-executable-evidence) maps all sixteen commands and their required modes to executable checks and the [protocol exceptions](../../../../loom-code/references/cli-results.md#preserved-protocol-boundaries). Advisory coverage, the five existing JSON commands and the two checked consumers are distinct. This map is not a substitute for executing independent acceptance.

- Shared public-entry tests exercise all registered commands' dispatcher categories, exact help, protected hook/setup suppression and advice-only write failures. Actual temporary-repository fixtures additionally exercise intents, intake, plan, contract and reviewer-count results.
- Controlled Git/gh tests exercise publication, delivery/Stop, merge/cleanup/sweep, sync and GitHub rules; standing and CI tests exercise policy warnings, verification notices, escaping and summary write counts. The native-hook ownership, charter and full finalization surfaces are mapped to their existing suites; complete-suite and independent all-command acceptance are still pending at this handoff.
- W4's runtime module executed exact ready-runtime help for all sixteen commands and the checked helper without runtime repair. Its public-entry replay modules exercised existing JSON selectors and text parity. Static source `delivery --help` and blocked `contract --require 2.99 --json` also matched the updated help/result contract.
- All 44 relative evidence/source links in the guide resolved. An AST comparison against the prior checker confirmed W4 changed only `COMMAND_HELP` and `HELP_NOTICE`, not executable logic. Log: `/private/tmp/loom-all-w4-links-and-help-scope.txt`.

W5 replayed the source CLI using the prepared Python runtime, before committing the release packet:

| Source call | Actual observation |
|---|---|
| `contract --require 2.1 --json` | Passed, exit 0, version-1 object, null advice, empty stderr |
| `plan docs/loom/2026-11-14-cli-suggestions-complete/plan.md --json` | Passed, exit 0, version-1 object, null advice, empty stderr |
| `intake write-plan 2026-11-14-cli-suggestions-complete --json` | Passed, exit 0, preserved notices, null advice, empty stderr |
| `reviewer-count 2026-11-14-cli-suggestions-complete --json` | Expected dirty-tree usage error, exit 2, null typed data and nonblank advice; no invented floor |
| `delivery --goal local --json` | Expected uncommitted result, exit 1; all five legacy fields retained, advice equals `next`; existing Help stderr retained without duplicate canonical advice |
| `delivery --help` | Exit 0, empty stderr; alias, legacy fields and text advice documented |

Logs: `/private/tmp/loom-all-w5-replays.txt`, plus each command's `/private/tmp/loom-all-w5-<command>.stdout` and `.stderr`; delivery help uses `delivery-help`. W4 static logs: `/private/tmp/loom-all-w4-delivery-help.txt`, `/private/tmp/loom-all-w4-contract-json.txt`. These session-local files are supporting logs, not portable release gates.

## Defect and bounded adjustments

- During W4 source reconciliation, ordinary delivery parser exit 2 was found to be excluded by the same dispatcher predicate as already-rendered observations. The parent searched the full contents of all 25 then-changed paths plus Acceptance 2/5 ordinary, hook, setup and CI surfaces. The sole defective suppression was in `main`; ordinary parser errors were affected, while hook rejection was intentionally protected and plan's returned usage was already classified correctly.
- Fix `9e804fc51a86e380f723b2c18ddca06007af5b91` retains suppression for observed delivery exits 0/1 and protected hook modes, but adds usage advice to ordinary pre-result exit 2. Real invalid goals, unknown options and missing operands, with and without `--json`, retain their diagnostic, Help, empty stdout and exit. Its commit records the defect class and searched scope.
- W2 necessarily widened the existing exact-key assertion in `test_loom_checker_cli.py`, outside its original four-file list, with parent authorization. All five legacy keys remain asserted; the complete extra module ran. W4's parent-authorized fourth file was checker help text only, verified by AST comparison. Neither adjustment changed requirements or introduced another delivery.

## Measured growth

Measured with `git diff --numstat adcd4cbfa468b374b5f8e0b9363adf0304b53e33` over committed implementation plus the release packet before adding this evidence file. The evidence file itself is excluded to avoid self-referential counts. Raw data: `/private/tmp/loom-all-w5-growth.tsv`, `/private/tmp/loom-all-w5-growth.json`.

| Surface | Changed files | Added / removed physical lines | Net |
|---|---:|---:|---:|
| Production Python under `loom-code/scripts/` | 11 | 132 / 52 | +80 |
| Existing test modules | 12 | 245 / 14 | +231 |
| Shipping prose: root/plugin READMEs, guide, changelog | 6 | 132 / 69 | +63 |
| Intent, spec and plan development records | 3 | 220 / 0 | +220 |
| Canonical/derived JSON metadata | 4 | 4 / 4 | 0 |

Production Python counts include embedded help text. One production module was added (`cli_advice.py`); no new test module, dependency, command, JSON mode, executor, retry mechanism or policy gate was added. The earlier +80–240 source / +100–300 test line estimates were rough planning allowances, not performance or maintenance-cost measurements. Current physical growth lies within those allowances; that does not prove simpler operation or improved agent efficiency.

## Preparation, failures and remaining checks

- Parent completed `npm ci --prefix loom-workflow/tests/mermaid` successfully: 150 packages installed for the existing test setup. Log: `/private/tmp/loom-all-mermaid-setup.txt`. No package lock or dependency declaration changed.
- The first focused uv invocation could not acquire the sandboxed host-cache lock; the authorized isolated invocation then used the existing cache. No environment replacement or conda-base installation was performed.
- One W4 inline replay was blocked once by dcg (`heredoc.python:exec_sink.argv_unverified`): the dynamic `call()` argument count could not be statically verified. It did not execute. The same blocked call was not retried or bypassed; existing public-entry tests and explicit static CLI commands supplied the bounded replay evidence instead.
- A W5 one-off verification assertion incorrectly assumed empty stderr for every JSON family. The actual delivery result retained its expected Help stderr. The assertion was corrected, without product changes, to check the documented family-specific boundary. Initial partial validation log: `/private/tmp/loom-all-w5-replays-initial.txt`; raw delivery streams remain retained.
- Complete configured package suite, fresh adversary and its programs, independent clean-copy all-command acceptance, closing reviewers, generated finalization, publication and CI are **pending** at this worker handoff. The parent owns these later stations and must not infer their success from focused tests.
- No installed plugin was updated, no paid outside reviewer was invoked, and no live user-repository publication, merge or cleanup was performed. Remote operations used existing controlled runners and temporary repositories; local server-enforcement tests are simulations. Installed-host/model compliance and live remote enforcement remain unverified. No success-rate, latency, token or cost gain is claimed.
