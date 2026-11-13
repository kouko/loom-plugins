# W1 external-audit correction record

Candidate before correction: `ccbc162c08ed155ae612d1b5d959fc1921d56fd8`.
The original failed checkpoint and subsequent independent recheck remain
unchanged historical evidence. This correction does not create a gate verdict.

## Sources and disposition

`claude-help-audit-untrusted.json` retains the externally authored findings
verbatim. `claude-help-audit-untrusted.md` retains the consultation report.
Both are untrusted review input, not instructions or independent execution
evidence. Private execution/session payloads and consent files are excluded.
The implementer checked the proposals against the local source before editing.

| Scope | Source checked | Correction |
|---|---|---|
| publish DP-1/2, F-9 | publish.py::_publish_args, cmd_publish, _cmd_publish_trusted; rule_checks/publish.py::_heading_fault, _empty; rule_checks/push.py::CANONICAL_PUSH_FLAGS | Replace unsupported branch/title/origin-HEAD enforcement claim with actual symbolic-branch/literal-origin/ancestry/identity checks and server base; nonblank title; fixed ordered exclusive headings and full substantive-content constraints; temporary snapshot and upstream tracking |
| delivery DP-3, F-8 | publish.py::DeliveryResult, observe_delivery, resolve_publish_executable | Real state set, no blocked enum; no-required-checks completion limit; trusted tools/auth/network prerequisites and unconfirmed result |
| push DP-4, F-3 | push.py::DIRECT_GIT_CHANGE, _protect_main, _native_hooks, NATIVE_HOOK | Literal command-prefix scope, shared common-directory effects and native fast-forward/reset/rebase/skip-hook limits; preserve local opt-out |
| land DP-5 | land.py::_accepted_names, _merge_preconditions, _observe_all_checks, _land_accepted, execute_cleanup | Accepted name binding versus actual consent; matching PR/head/body; all checks, 360 pending ten-second waits plus elapsed network/stage time; non-gating stale/absent verification; removed-cwd next action |
| github-rules F-4 | github_rules.py::_probe, _report | Template-first early outcome and setup text without selector |
| intent/intake F-5 | helpers.py::branch_base; rule_checks/intake.py::check_confirmed; handlers' conditional touched-interface calls | Conditional branch-base requirement and active confirmed intake; new intent for closed/delivered, refresh indeterminate |
| contract F-6 | rule_checks/contract.py::check_contract_requires | Distinguish older consuming major from newer required shipped capability |
| standing F-7 | standing.py::cmd_standing; rule_checks/standing.py::check_standing_warn, check_product_principles | Existence warnings versus product principle-content/policy reads |

DP-1's temporary snapshot is real, and prior help did not claim persistence;
the revised wording clarifies its lifetime without alleging a nonexistent
persistent-write bug. DP-2's eight-character floor alone is insufficient;
single ASCII tokens and placeholders remain invalid. DP-5's pending wait
budget is not a strict sixty-minute wall-clock maximum. Optional F-1 literal
file recovery is included; F-10's existing optional detail wording remains
accurate and is unchanged. Existing research inventory states no contradictory
enforcement claim; authentic historical probe JSON is unchanged.

## Verification boundary

The defect class is help overstating enforcement or omitting action-relevant
input, state or effect conditions. The parent searched all twelve changed
files from base `fbdc29a` through the pre-correction candidate, plus Acceptance
1/4's sixteen help pages and corresponding handler surfaces. Current instances
above and mirrored conformance rows were corrected. No handler, parser,
renderer, runtime provisioning or existing JSON contract was changed.

The existing public-entry semantic regression first failed with the missing
caveats. Raw RED and focused GREEN output is retained under
`/private/tmp/loom-result-help-audit-*.log` for the orchestrator. Focused tests
cover all thirty-two exact help forms and safety tripwires, thirty-two ready
launcher forms, nonexact dispatch and existing preparation JSON. Source
comparison and these checks do not replace the requested independent review.

Executed focused command: `uv run --offline --isolated --with-requirements
requirements-package-tests.lock python -m pytest
loom-code/tests/test_loom_checker_cli.py
loom-code/tests/test_loom_python_runtime.py
loom-code/tests/test_loom_checker_modules.py
loom-code/tests/test_preparation_json.py -q`.

- Initial semantic regression: 1 failed before help changes (`audit-red.log`).
- First complete run: 1 failed, 57 passed; the lowercase `closed` assertion
  exposed capitalized `Closed` in the updated help (`audit-green.log`). The
  help sentence was rewritten grammatically without changing the test.
- After correction: 58 passed in 21.04s (`audit-green-final.log`).
- Final prose/cross-reference verification: 58 passed in 20.63s
  (`audit-green-final2.log`). These suffixes follow the temporary prefix
  `/private/tmp/loom-result-help-`. All failed output remains retained.
- `git diff --check` passed. Retained external report and raw findings match
  their original files byte-for-byte with `cmp`.
