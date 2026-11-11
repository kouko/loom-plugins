# Native host framing investigation

Date: 2026-11-11. These are pre-implementation protocol probes, not validation of an installed repair.

## Inputs and isolation

User identified Claude Code as the affected interface and separately requested Codex testing. The local versions were Claude Code 2.1.322 and codex-cli 0.167.0. Claude's installed loom-code user scope was 3.64.0, matching the source hook commands. No normal plugin/settings file or installed cache was changed.

A disposable hook at `/private/tmp/stop-host-probe/hook.py` read Stop JSON and retained only event name, continuation flag, turn ID, final fixed response and optional task arrays. On the first event it requested exactly SECOND; on a continued event it returned empty JSON. The user prompt requested exactly FIRST and prohibited tools. Two response shapes were compared: decision/block/reason and hookSpecificOutput/Stop/additionalContext. No repository contents or private transcripts were supplied.

## Codex native results

Both runs selected `--model gpt-6-astra`, `model_provider="openai"`, `model_reasoning_effort="low"`, `--ignore-user-config`, `--ephemeral`, `--sandbox read-only` and a disposable inline Stop hook. OPENAI_BASE_URL and OPENAI_API_KEY were unset for first-party account routing. The one-off hook was inspected before using the CLI's documented automation trust override; the CLI emitted its override warning, which is unrelated to the reported delivery message. This test did not alter persisted hook trust. That override is not an installation or adoption remedy.

| Shape | Agent messages | Stop records | Result |
| --- | --- | --- | --- |
| decision/block/reason | FIRST, SECOND | false then true, same turn ID | One continuation, then normal completion; exit 0. |
| Stop additionalContext | FIRST | false only | No continuation; exit 0. |

No model tool call was emitted. The first run reported 32,356 input tokens (24,320 cached), 10 output tokens and zero reasoning tokens; the second reported 18,243 input tokens (12,160 cached), 5 output tokens and zero reasoning tokens. No dollar cost was reported. Raw output remains in `/private/tmp/stop-host-probe/codex-block-result.jsonl` and `codex-feedback-result.jsonl`; event summaries are `block-events.jsonl` and `feedback-events.jsonl` beside them. This proves framing behavior in native noninteractive Codex, not interactive UI presentation or the repaired plugin end to end.

## Claude runtime attempt and limitation

The request selected haiku/low, a US$0.20 maximum, empty setting sources, explicit disposable hook settings, no model tools, no MCP servers and no session persistence. Third-party base URL/provider flags were unset. It returned `is_error: true` before a Stop record: `You've hit your 5-hour limit · resets 4:20pm (Asia/Taipei)`. Reported cost was US$0; no Stop event ran. No provider switch or quota retry was attempted. This is an account availability failure, not a hook result.

The installed Claude executable contains the `Stop hook feedback` presentation label, but finding a string is only static support evidence, never a native execution pass. Actual Claude presentation and continuation remain unverified until an authorized fresh-session run can execute after quota recovery.

## Source grounding

- [Claude Code hooks: Stop](https://code.claude.com/docs/en/hooks#stop), read 2026-11-11: Stop additionalContext continues without the hook-error notification; stop_hook_active identifies an existing continuation; background task/wakeup arrays distinguish pauses.
- [Codex hooks: Stop](https://learn.chatgpt.com/docs/hooks#stop), read 2026-11-11: decision/block continues, and stop_hook_active applies to the same turn. It documents no Stop additionalContext continuation.
- Source `loom-code/scripts/loom_checker/command_handlers/publish.py:_delivery_stop` currently emits the block shape for both hosts and repeats stderr after the continuation flag. Existing tests explicitly require that repeated diagnostic. This grounds the correction independently of missing historical session logs.
