---
title: "Claude Code Stop behavior with installed loom-code 3.65.0"
type: loom-research
status: concluded
created: 2026-11-11
updated: 2026-11-11
tags:
  - loom/research
---

# Claude Code Stop behavior with installed loom-code 3.65.0

## Question and scope

Does the installed repaired Stop hook execute correctly in a fresh native Claude Code session, continue at most once when eligible, and permit stopping while awaiting a human answer? The user authorized Claude Code testing after PRs 140 and 141 merged. This record revalidates the earlier quota-blocked attempt; it does not replace its evidence.

Conditions: macOS, Claude Code 2.1.322, installed Claude plugin cache `/Users/kouko/.claude/plugins/cache/loom/loom-code/3.65.0`, source main `91ee36100708f73af5d1df33107dbf98b91ac44f`. Each run used the real full installed plugin through `--plugin-dir`, empty setting sources, no model tools, no MCP servers, no session persistence, `--model haiku --effort low --max-budget-usd 0.20`, and synthetic prompts. Provider redirect variables were removed for the child process. Every result identified `claude-haiku-5-5`, provider `firstParty`.

## Method and rationale

A bounded native CLI experiment supplies evidence unavailable from unit tests. Hold host version, plugin, provider, effort and model-tool restrictions constant; vary repository state and whether the prompt awaits a human. A separate observer hook records native Stop inputs without changing the installed hook. Debug logs confirm the installed plugin hook loaded and executed. No hook output or remote response was mocked.

The first empty-repository attempt had no HEAD and is retained as a diagnostic case, not counted as the normal stopping case. The normal case then used an empty local commit. Reviewed cases used a disposable clone at PR140's actual reviewed and published HEAD `ce6d3c4f7438c89c81410bfef35bc7942b2dc396`, with the actual GitHub origin. `test/2026-11-11-skill-retro-project-identity` had no matching remote branch or PR; `fix/2026-11-11-skill-retro-project-identity` matched merged PR140. GitHub operations were read-only. Model tools were disabled, so reminder receipt and bounded continuation were tested, not automatic publication.

## Findings

| Case | Native observation | Conclusion |
| --- | --- | --- |
| No HEAD | One answer, one Stop with active=false; installed hook exited 0 and emitted systemMessage describing unavailable Git HEAD. | Unconfirmed delivery did not force continuation. This is not silent success. |
| Normal committed repository without a Loom change | One NORMAL_STOP_OK answer, one Stop with active=false; installed hook exited 0 without a delivery reminder. | Normal stopping passed. |
| Reviewed but unpublished test branch | FIRST followed by SECOND and an explanation that publication was prohibited; Stop inputs active=false then true; both installed hook calls exited 0. First output was Stop additionalContext describing unpublished delivery. | Native Claude consumed the real reminder; the repeated Stop did not loop. |
| Waiting for a human on the same unpublished branch | First asked which color to use; after one reminder, explicitly stated it was waiting and would not publish or call tools. Stop inputs active=false then true, both hooks exited 0. | Human waiting can stop after one reminder. Zero initial reminders while waiting is not established and was not observed. |
| Merged PR140 identity retained in the clone | One MERGED_STOP_OK answer, one Stop with active=false; installed hook exited 0 with no incomplete-delivery reminder. | The real merged identity permitted stopping. This does not test a cleaned main checkout. |

All five calls returned is_error=false. No `Stop hook error` label appeared in the captured noninteractive debug logs. That observation does not establish interactive terminal presentation.

Reported total list-price cost was USD 0.00381201 across five calls; this is the CLI's usage report, not an independently verified subscription charge. The first attempted interactive test was rejected before execution by automatic approval review because it would remove the print-only maximum-dollar flag. It made no model call and produced no interactive screenshot or terminal observation. No attempt bypassed that rejection.

## Authorized interactive attempt

The user subsequently authorized one interactive call without a CLI monetary hard cap, with model tools disabled and a 60-second supervisor timeout. The native terminal loaded Claude Code 2.1.322, Haiku 5.5 and the installed plugin. The ordinary workspace trust prompt was accepted for the disposable clone.

Before answering, Claude displayed its five-hour usage limit, resetting at 21:30 Asia/Taipei on 2026-11-11. The debug log records HTTP 429 rate_limit_error. No installed Stop-hook execution was recorded for this attempt, so interactive Stop presentation remains unverified.

Escape cancelled the host's automatic continuation; the terminal explicitly confirmed cancellation. The session then closed through /exit after 33.17 seconds, exit 0, timed_out=false. No retry or provider switch was attempted. This interactive attempt reported no completed-result cost; its cost is unknown, not asserted to be zero. The earlier reported total covers only the five successful noninteractive calls.

Receipts are in the same temporary directory: interactive-command.json, interactive-terminal.txt, interactive-debug.log, interactive-exit.json and the interactive.py supervisor. The one authorized interactive attempt has been consumed; no automatic retry is scheduled.

## Evidence

- [Earlier host framing and quota failure](../2026-11-11-stop-feedback-noise/evidence/host-framing.md).
- [Original acceptance limitations](../2026-11-11-stop-feedback-noise/acceptance-test-report.md).
- Installed hook manifest: `/Users/kouko/.claude/plugins/cache/loom/loom-code/3.65.0/hooks/hooks.json`; read and executed through native plugin loading.
- [Source Stop implementation](../../../loom-code/scripts/loom_checker/command_handlers/publish.py): `_delivery_stop`, including additionalContext and repeated-Stop handling.
- Raw local receipts: `/private/tmp/claude-stop-native-20261111/`. Each case retains `<case>-command.json`, `<case>-output.jsonl`, `<case>-stderr.txt`, and `<case>-debug.log`; native inputs are in `stop-events.jsonl`. The first diagnostic command is `command.json`, with outputs prefixed `normal`.
- Reproduction harnesses `run.py` and `run-case.py` remain in that temporary directory. Invocation: `python3 /private/tmp/claude-stop-native-20261111/run-case.py <case>`. Case depends on repository state described above; do not replay without restoring that state. The harness has a 120-second subprocess timeout and each print-mode call has the USD 0.20 CLI budget flag.

## Decision impact

The repaired installed hook now has native Claude execution evidence for normal stopping, real eligible reminders, repeated-Stop suppression, human waiting and an identifiable merged PR. This closes the previous account-quota execution gap for these noninteractive scenarios. It does not justify claiming the interactive error display has been eliminated.

## Limitations and open questions

- Interactive Stop display remains unverified. After the initial approval rejection, the user authorized one attempt; account quota then blocked it before Stop. A new attempt requires available quota. A wall-clock timeout is not a monetary hard cap.
- Explicit `--plugin-dir` proves the installed cache works when loaded, not automatic loading in every existing user/local session or compatibility with other hooks and settings.
- Synthetic prompts constrain the expected response; this is not a broad autonomous publishing or model-behavior benchmark.
- Background tasks, scheduled wakeups, Codex and actual network publication were not tested here.
- Waiting on a human still received one reminder in the eligible unpublished state; the test does not claim otherwise.
- The research record is local and uncommitted; no source implementation, installed plugin or remote branch was changed. The host recorded ordinary workspace trust for the disposable clone and retained the synthetic interactive session; no user configuration file was manually edited.
