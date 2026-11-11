# Stop feedback without false hook errors
intent: 2026-11-11-stop-feedback-noise@57803f88
pre-build-review: required — host-specific Stop response contracts and continuation boundaries change.

## Requirements
REQ-1 — Quiet normal pauses
  WHEN normal work or a user decision pauses the session, the delivery hook shall avoid repeated error-framed publication reminders → Acceptance #1
REQ-2 — Preserve delivery truth
  The delivery observer shall retain distinct incomplete, unconfirmed and completed results without treating absent evidence as success → Acceptance #2
REQ-3 — Grounded host evidence
  The verification record shall distinguish hook execution failure, intentional continuation and host presentation, recording actual Claude Code and Codex results separately from untested boundaries → Acceptance #3

## Design decision
- agent-decided — retain the existing delivery observer and publication authorization checks. Correct only Stop applicability and response framing; publication, remote identity, CI, merge and explicit delivery exits remain unchanged.
- agent-decided — select the host explicitly in packaged hook commands: `delivery --hook --host claude` and `delivery --hook --host codex`. Keep legacy `--hook` as the existing Codex-compatible response mode; reject host selection outside hook mode or unknown host values. Explicit selection avoids guessing from optional payload fields or environment variable names. The shell-wrapper recovery hint must remove both `--host` and its value when replacing `--hook` with `--json`; preserve the literal executable path, working directory and stdin. Update the existing recovery replay tests to execute that exact valid command.
- agent-decided — return silently before Git/network lookup when `stop_hook_active` is true. This means no second continuation and no repeated diagnostic; it does not certify delivery. Claude's documented nonempty background_tasks or session_crons arrays also permit a normal pause without remote lookup. Only structurally valid nonempty arrays of task objects count; malformed values cannot silently suppress inspection. Codex does not document these fields and ignores them for this decision.
- agent-decided — for a first applicable incomplete Claude Stop, emit `hookSpecificOutput` with `hookEventName: Stop` and `additionalContext`, not `decision: block`. Keep conditional guidance to stop and explain when waiting for a user or publication was withdrawn. The host can continue once without its error notification. Codex retains documented `decision: block` and reason, because a native probe showed additionalContext does not continue Codex. No classifier of natural-language completion claims or questions, no new persistent session ledger, and no automatic merge.
- agent-decided — unavailable evidence and bounded observer exceptions use a JSON `systemMessage` diagnostic without a continuation decision for either host. It explicitly says delivery is unconfirmed and gives the existing recovery command. Actual launcher failure remains separately handled by the existing shell wrapper. Published/irrelevant/unauthorized/user-confirmation-boundary cases remain silent.
- agent-decided — keep the 20-second observation deadline and 25-second hook timeout. Update runtime documentation to distinguish a single normal continuation from a failure and state actual host limits. Use a minor loom-code release because the hook invocation contract changes.
- user-decided — the reported interface is Claude Code; also test Codex, per the user's subsequent request. Do not change normal installed settings or PR #140. Native tests use synthetic fixed-output prompts with no model tools and the existing first-party accounts. Claude quota exhaustion blocks native Stop execution today; record this boundary without substituting a gateway or claiming a runtime pass.

## Alternatives considered
- Disable Stop hooks or weaken explicit delivery checks — violates the confirmed outcome.
- Share Claude's additionalContext response with Codex — native Codex 0.167.0 ignored it for continuation.
- Treat every unpushed stop as an error — creates the reported misleading UI notification and repeats diagnostics during expected pauses.
- Infer questions/completion from response text — brittle across languages and unnecessary to correct host framing and repeated continuation.
- Persist a new per-session delivery state — unnecessary; both documented and observed stop_hook_active already identifies continuation.

## Current state evidence
- Forward: `loom-code/hooks/hooks.json:Stop` and `hooks-codex.json:Stop` call the same delivery hook with no host mode.
- Reverse: `loom-code/scripts/loom_checker/command_handlers/publish.py:cmd_delivery` routes `--hook` to `_delivery_stop`.
- Error: `publish.py:_delivery_stop` emits `decision: block` for expected incompletion and writes another diagnostic on repeated Stop after querying the remote again.
- Data: `loom-code/tests/test_delivery_stop.py:stop` exercises first/repeated Stop but supplies no background-task metadata and treats repeated stderr as desired behavior.
- Boundary: `publish.py:observe_delivery` and the explicit delivery command own actual completeness; their identity/authorization/CI semantics must not change.

## UI flows
| Case | Action | Result |
| --- | --- | --- |
| No applicable change | End a normal response outside authorized delivery | No delivery reminder; no claim of success. |
| Work in progress | Claude pauses with a background task or scheduled wakeup | No delivery error or forced publication continuation. |
| First premature finish | End before an authorized change is published | Claude receives normal hook feedback; Codex receives its existing single continuation prompt. Guidance preserves the user's decision boundary. |
| Continued turn or waiting for user | End again after a hook continuation | No repeated hook output or remote lookup; the agent explains any pending user decision. |
| Evidence unavailable | Delivery lookup cannot establish the result | A non-continuing warning says unconfirmed and gives a recovery command; no success claim. |
| Published | End with exact remote publication and CI evidence | No reminder; merge remains subject to acceptance. |
| Actual host execution blocked | Model quota prevents a test response | Record native behavior as not verified, separately from local contract tests. |

## External grounding and observed probes
- [Claude Code Stop input and output](https://code.claude.com/docs/en/hooks#stop), retrieved 2026-11-11: background_tasks/session_crons distinguish paused sessions; additionalContext is non-error continuation, while decision block is displayed as a hook error.
- [Codex Stop](https://learn.chatgpt.com/docs/hooks#stop), retrieved 2026-11-11: turn_id and stop_hook_active; decision block requests continuation. No equivalent Stop additionalContext continuation is documented.
- Native Codex 0.167.0, explicit OpenAI provider, gpt-6-astra/low: fixed-output block test returned FIRST then SECOND with stop_hook_active false then true and one unchanged turn_id. The feedback-format test returned only FIRST. Synthetic hook wrote metadata only; no model tool ran. Raw receipts remain in /private/tmp/stop-host-probe; durable summary will be retained in acceptance evidence.
- Claude Code 2.1.322, explicit haiku/low, US$0.20 cap: request returned an account five-hour quota limit before Stop ran, cost US$0. This is not evidence for or against the proposed Stop behavior; no retry against another provider.
