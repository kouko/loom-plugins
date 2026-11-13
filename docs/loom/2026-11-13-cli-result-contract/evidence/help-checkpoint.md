# Independent W1-02 help-content checkpoint

Reviewed HEAD: `14a358c21c31aeb7678ca7d940eba4046c504d76`.
Reviewer: independent Codex agent `result_help_checkpoint`, not the W1 writer.
Verdict: **NEEDS_REVISION**. W2 must remain pending. This is a bounded help
checkpoint, not a formal closing-review attestation or independent acceptance
report for the whole change.

The actual sixteen `COMMAND_HELP` entries and corresponding handlers were read
against intent Acceptance 1/4, REQ-1/4, plan W1-02 and the baseline conformance
table. Per-command results below cover argument grammar, modes, prerequisites,
streams/exits, effects and authority. PASS means no material mismatch found in
that bounded source comparison; normal writer/network paths were not executed.

| Command | Verdict | Handler/source anchors and checked meaning |
|---|---|---|
| intent | PASS | `command_handlers/intent.py:20`; `rule_checks/intent.py:297,362`: optional commit-message evidence, source checks, advisory-before-block, read-only 0/1/2 |
| intents | PASS | `command_handlers/intents.py:56,92`; `intent_state.py:83,191`: identifier/remote grammar, metadata, filtered list, local-ref boundary, indeterminate 1 |
| intake | PASS | `command_handlers/intake.py:28`; `preparation_output.py`; `rule_checks/intake.py`: station/ID distinction, applicable prerequisites/notices, preparation JSON, no station authority |
| push | NEEDS_REVISION | `command_handlers/push.py:172,207`: hook/native forms, stdin/native writes and 2/fail-open behavior otherwise match; finding H1 below |
| publish | PASS | `command_handlers/publish.py:117,163,677,738,801`: automatic/legacy authority, nine headings, snapshot/push/Ready PR, required-CI/no-checks boundary, partial remote success |
| delivery | PASS | `command_handlers/publish.py:318,500,590`: goal/intent/JSON and distinct exact host-hook forms, selected-goal completion, read-only observation/no authority, malformed text exception |
| land | NEEDS_REVISION | `command_handlers/land.py:110,139,181,350,457,715,939`: exclusive forms, acceptance/live evidence, merge and deletion, token/fetch-prune/partial completion otherwise match; H2 below |
| sync-trunk | PASS | `command_handlers/sync.py:177,208,366`: no operands, clean change branch, fetch/rebase-or-merge, collision/conflict refusal, attempted restore, unsynced WARN exit 0 |
| github-rules | PASS | `command_handlers/github_rules.py:221,295`: advisory network reads, present/absent/unconfirmed, print-only setup, 0 not proof |
| pr-floor | PASS | `command_handlers/pr_floor.py:26,45`: unique paired options, body BLOCK/annotations, stale verification passes, optional summary append/no PR-controlled execution |
| standing | PASS | `command_handlers/standing.py:14`; `rule_checks/standing.py:9,28,38,149`: file/repo standing context, warning versus policy blocker, read-only |
| contract | PASS | `command_handlers/contract.py:11`; `rule_checks/contract.py:10,17`: numeric pair, manifest compatibility rather than plugin version, 0/1/2, no duplicate-rejection claim |
| charter | PASS | `command_handlers/charter.py:13`; `rule_checks/charter.py`: override/last occurrence, ordered table including empty failure, table is not approval |
| plan | PASS | `command_handlers/plan.py:11`; `rule_checks/intake.py`; `preparation_output.py`: raw arbitrary path, limited caps/Simplicity rules, empty success, preparation JSON/no authority |
| reviewer-count | PASS | `command_handlers/reviewer_count.py:11`; `reviewers.py:511`: one nonblank operand, clean tree, conservative floor integer, read-only/no verdict |
| finalize-review | PASS | `command_handlers/finalize.py:224,236,290,350,417,457`; `reviewers.py`: authentic reviewer/probe input, package/adversarial execution, progress/final exit, atomic attestation write and limited authority |

## Findings

**H1 — push overstates protection when it is explicitly disabled (medium).**
`loom_checker.py:139` says the hook refuses direct commit/merge/push on main/master
with exit 2. `command_handlers/push.py:213-214` explicitly bypasses that refusal
when repository-local `loom.protectMain` is false. An operator can therefore
read the page and incorrectly believe the currently configured hook guarantees
refusal. Describe the condition plainly, preserving the separate native-hook
scope. Do not remove or change the existing opt-out behavior in this help task.

**H2 — land exit 0 does not establish trunk synchronization (medium).**
`loom_checker.py:168-169` says exit 0 completes the requested operation, after
listing trunk synchronization among the accepted-form actions.
`command_handlers/land.py:201-205` always proceeds from `sync_trunk` to cleanup;
`land.py:315-347` explicitly treats skipped/failed trunk sync as nonfatal and
prints `trunk not updated`. Successful cleanup can consequently return 0 even
when trunk was not updated. Add this exit-0 caveat and tell the operator to read
the trunk result, preserving work before independently resolving it. Existing
partial merge/cleanup cautions remain valuable and should stay.

## Authentic bounded execution

- `/private/tmp/loom-result-help-independent.py` ran all 32 exact public-entry
  forms outside Git with handler/stdin/subprocess/socket/file-access tripwires.
  Each returned nonempty text stdout, empty stderr, exit 0; directory stayed empty.
- The same program ran all 32 exact forms through the candidate's actual
  `loom-python --ready` launcher from an empty nonrepository directory, PATH
  restricted to `/usr/bin:/bin` (uv unavailable), against an existing valid
  runtime. Output exactly matched the sentinel invocation; all exited 0.
  Output retained at `/private/tmp/loom-result-help-independent-output.json`.
- Missing-runtime ready help returned 86 without creating the isolated cache.
  No repair, installer, real handler, live network/write command or full suite ran.
- `/private/tmp/loom-result-help-counterexamples.py` exercised H1/H2 using mocks:
  main/git-push with local policy false was allowed; failed trunk inspection plus
  successful cleanup returned 0 and printed `trunk not updated`.
- Compared all nonblank lines of the prior six pages at HEAD^ with candidate
  pages: plan, intake, reviewer-count, finalize-review, publish and delivery all
  preserved their previous lines, including examples and substantive cautions.
- The supplied Build log records 58 focused passing tests. Independent pytest
  attempts using system Python and the existing runtime stopped before collection
  because pytest was absent. Then the existing uv cache was used offline with
  `uv run --offline --isolated --with-requirements requirements-package-tests.lock
  python -m pytest -q` for `test_exact_help_never_dispatches_handlers` and
  `test_all_command_help_uses_ready_runtime_without_repair`: **2 passed in 3.76s**.
  This confirms discovery, not semantic accuracy; H1/H2 remain failures.

Retain this failed checkpoint and its counterexamples when correcting help.
Recheck both corrected pages against the unchanged handlers before starting W2.
