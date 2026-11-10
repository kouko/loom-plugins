# Planning command recovery — acceptance test evidence

Tried on 2026-11-11, in a clean copy of the project at 92044c2ef24cad416e0b624640d8bd31b8bc7108.

## Setup and independence

The acceptance tester did not implement the change. Created a fresh clone using `git clone --no-hardlinks /private/tmp/loom-planning-command-recovery /private/tmp/loom-recovery-acceptance-clean`; `git rev-parse HEAD` returned the full SHA above. Read the repository README development instructions and used its isolated locked dependency environment for focused tests. The first uv invocation hit the sandbox cache permission boundary (`Could not acquire lock`, `Operation not permitted`); the same command succeeded with cache access. This was an environment permission issue, not a product failure.

The clean checkout's launcher ran successfully. `python3 scripts/sync_codex_manifests.py --check --all` exited 0 with no output. Existing runtime availability was used by the manual plan trial; cold-runtime help and bootstrap behavior were separately exercised by the focused runtime tests, not inferred from this warm run. No host installation or private configuration was changed by this tester.

## 1. Recover observed calls

Synthetic existing plan `/private/tmp/loom-acceptance-valid-plan.md`:

```markdown
charter: 1.0
## Task DAG
**T1 Example** after: none
- Files: src/a.py
- Test: works
- Risk: agent-decided — low
```

The fixture follows the existing valid-plan test format. Recovery was selected from emitted error/help text, without reading launcher implementation. In the commands below `L=./loom-code/scripts/loom-python`, `C=loom-code/scripts/loom_checker.py`, and `P=/private/tmp/loom-acceptance-valid-plan.md`; variables abbreviate the exact literal arguments used in subprocess calls.

| Command | Exit | Exact relevant output |
|---|---|---|
| `$L $C --repair plan $P` | 2 | `loom-python: use --repair or --ready before checker arguments.` |
| `$L --repair $C plan $P` | 2 | `loom-python: omit the redundant loom_checker.py path; pass the checker command directly.` |
| `$L --repair plan $P` | 0 | No stdout or stderr. |
| `$L --ready plan $P` | 0 | No stdout or stderr. |

Both error forms also printed these exact lines:

```text
Usage: loom-python (--repair|--ready) <checker-command> [arguments...]
The checker is selected automatically; omit loom_checker.py from the arguments.
Planning: "<loom-code>/scripts/loom-python" --repair plan "<path-to-plan.md>"
Checker commands: "<loom-code>/scripts/loom-python" --repair --help
No validation has run when usage is displayed.
```

Following that planning example required only removing the redundant checker path and placing the mode before `plan`. Re-read the valid fixture after the trial: its content remained identical to the block above.

### Independent inspection of supplied live-host recordings

Read actual tool events in `/private/tmp/loom-recovery-hosts/codex-events.jsonl` and `claude-events.jsonl`, not final narrative summaries. `tested-sha.txt` identifies the same full SHA. Commands use the synthetic marketplace clone under that directory. No credentials, configuration contents or whole conversations are reproduced here.

- Codex completed command `item_1` put `loom_checker.py` before `--ready`: exit 2, `loom-python: use --repair or --ready before checker arguments.` Completed `item_6` removed that path and ran `--ready plan .../codex/plan.md`: exit 0, empty output. Completed `item_5` checked `invalid-plan.md`: exit 1, `BLOCK plan.field-caps: T1.Test missing`.
- Codex completed `item_2` (`--help`) and `item_3` (`--ready --help`) both exited 0 with usage text. The latter includes `loom_checker.py plan <path-to-plan.md>`, `loom_checker.py charter [--manifest <path>]` and the valid launcher example.
- The orchestrator explicitly selected Codex `gpt-6.1-sol` with OpenAI. This model/provider assertion is launch provenance supplied by the orchestrator, not independently proved by the command-event stream or generic agent prose.
- Claude initialization identifies `claude-sonnet-5-5` and `loom-code@inline` version `3.63.0` loaded from the synthetic marketplace clone. Tool call `toolu_01HRRceogHEwyFUotJaLgmPJ` put the checker path after `--ready`; its matching tool result includes the targeted redundant-path diagnostic and `exit=2`.
- Claude tool call `toolu_018uibXCnWFDjdJeS79b7QUX` retried `--ready plan .../claude/plan.md`; the matching result begins `plan_exit=0`. It later reports `BLOCK plan.field-caps: T1.Test missing` and `invalid_exit=1` for the invalid fixture.
- Claude's second help invocation pipes to `head -40`. The result contains supported commands and a `help_exit=0` label, but that pipeline is not treated here as independent proof of the checker's own exit status. Direct local help and Codex's direct help command provide that evidence.
- Codex's later metadata/config-search command (`item_7`) exits 1 after displaying plugin manifests. This is not a plan validation failure and is not used as evidence of model identity.
- OpenCode live-host execution is deferred by user instruction. Automated hook replay includes its manifest; that does not establish live OpenCode execution.

## 2. Discover valid usage

`$L --help` returned launcher usage and the exact planning example above, exit 0. `$L --ready --help` exited 0 and included:

```text
    loom_checker.py charter [--manifest <path>]
    loom_checker.py plan <path-to-plan.md>
With the launcher, the checker is selected automatically; omit loom_checker.py:
    "<loom-code>/scripts/loom-python" --repair plan "<path-to-plan.md>"
    "<loom-code>/scripts/loom-python" --ready intake <station> <change-id>
Plan takes a file path; intake takes a station and a change-id.
No validation runs for --help or -h alone.
```

The example was executed successfully in section 1. Focused tests `test_launcher_help_and_invalid_calls_need_no_runtime` and `test_help_covers_commands_without_claiming_validation` passed: they exercise unconfigured runtime/cache behavior and command-list completeness. `test_checker_help_recovers_to_plan_validation` passed as a separate executable help-to-validation path.

## 3. Preserve validation and host hints

The correct calls in section 1 returned 0. `$L --ready plan $P extra` returned 2 with `unexpected argument 'extra'.`. An invalid synthetic copy with only `- Test: works` removed returned 1 with `BLOCK plan.field-caps: T1.Test missing`. No-argument launcher call returned 2 with complete launcher usage and `No validation has run when usage is displayed.`

Focused command, run in the clean clone:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_loom_python_runtime.py loom-code/tests/test_loom_checker_cli.py loom-code/tests/test_hooks_json.py loom-code/tests/test_hook_recovery_literal_path.py loom-code/tests/test_delivery_stop.py loom-code/tests/test_github_rules.py
```

Exact final output: `131 passed in 34.35s`, exit 0.

Coverage includes `test_script_mode_uses_runtime_and_preserves_script_exit` (custom script receives its own help and spaced argument, preserves exit 7); `test_failed_hook_hint_replays_operation_without_launcher_on_path` (Claude, Codex, OpenCode, Antigravity replay retains executable, operation and stdin); `test_hint_dollarpath_preservesroot` (literal dollar-containing installation path); `test_missing_ready_runtime_reports_repair_without_checker_refusal`; and `test_missing_rules_listed_with_command`. The replay tests execute synthetic recorder scripts and do not publish or mutate GitHub policy. The Stop hint explicitly instructs changing `--ready` to `--repair` and `--hook` to `--json`, preserving other arguments, working directory and stdin.

The full suite was intentionally not rerun by this acceptance tester. It remains the automated suite that runs before acceptance and blocks it on failure, executed by `finalize-review`:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

## Spec and plan coverage

Read retained `spec.md` and `plan.md`. REQ-1 maps to the two manual recovery trials plus live-host event inspection; REQ-2 maps to direct help and executable help tests; REQ-3 maps to valid, invalid and extra-argument trials plus focused regressions. All eight listed UI cases are covered: Empty (manual exit 2), Help (manual plus cold-runtime test), Checker help (manual exit 0), Missing mode and Redundant path (manual errors and successful recovery), Correct call (0/1/2 exercised), Custom script (focused test preserving arguments/exit 7), Hook recovery (four-host replay and literal-path tests). This is an engineering change, so the report retains one row per intent Acceptance line rather than additional product UI rows.

The plan's four waves are represented by launcher/checker tests, emitted recovery tests, synchronized release metadata check, and literal-path recovery tests. No important-or-worse dismissed findings were supplied. No product artifact was repaired during acceptance testing.
