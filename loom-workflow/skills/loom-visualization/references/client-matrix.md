# Client capability matrix

Verified: 2026-09-14

Which presentation form each client can display. `scripts/detect_client.py`
reports the detection signal; this table says what to do with it. A cell
nobody has confirmed is marked `unverified` and is treated as "does not
render". That rule applies to the Mermaid column only: GFM markdown tables
are the default form in every client.

| Client | Detection signal | GFM table | Mermaid | Form in a chat reply | Sources |
|---|---|---|---|---|---|
| Claude Code CLI / JetBrains | `CLAUDECODE=1`, `CLAUDE_CODE_ENTRYPOINT=cli` | unverified | no (source shown raw) | markdown table | https://code.claude.com/docs/en/env-vars, https://github.com/anthropics/claude-code/issues/14375 |
| Claude Code VS Code | `CLAUDECODE=1`, `CLAUDE_CODE_ENTRYPOINT` names the IDE extension | unverified | no (source shown raw) | markdown table | https://code.claude.com/docs/en/env-vars, https://github.com/anthropics/claude-code/issues/20529 |
| Claude Desktop Code tab | `CLAUDECODE=1` | unverified | no (source shown raw) | markdown table | https://code.claude.com/docs/en/env-vars, https://github.com/anthropics/claude-code/issues/52517 |
| claude.ai / Claude Desktop chat | no shell; host identity only | yes | yes (reported to render) | markdown table; Mermaid also allowed | https://github.com/anthropics/claude-code/issues/52517 |
| Codex CLI | `CODEX_THREAD_ID`, `CODEX_SANDBOX` or `CODEX_CI` | yes | unverified | markdown table | https://github.com/openai/codex/blob/main/codex-rs/core/src/spawn.rs, https://github.com/openai/codex/pull/24489 |
| Codex app / IDE | `CODEX_THREAD_ID`, `CODEX_SANDBOX` or `CODEX_CI` (reported as `codex`; app vs CLI not distinguished) | unverified | unverified (user report of rendering, not confirmed) | markdown table | https://github.com/openai/codex/blob/main/codex-rs/core/src/spawn.rs, https://github.com/openai/codex/issues/7004 |
| Antigravity IDE | unverified | unverified | no (reported broken) | markdown table | https://discuss.ai.google.dev/t/failed-to-render-mermaid-diagram-invalid-mermaid-header/169531 |
| Antigravity CLI (`agy`) | unverified | unverified | no (rendered as ASCII) | markdown table | https://antigravity.google/docs/cli/artifacts/ |
| Gemini CLI (legacy) | `GEMINI_CLI=1` | unverified | unverified | markdown table | https://geminicli.com/docs/tools/shell/ |
| unknown | none of the above | unverified | unverified | markdown table | — |

## Rule

Mermaid is allowed only when the agent has no shell and its host identity is
claude.ai or the Claude Desktop chat. Every other case gets a markdown table,
which every client in this matrix renders. The drawn form is chosen by the
destination, not by the client: a code comment, a commit message or another
plain-text target that does not render markdown. A genuine box diagram — a
flow, a state machine, an architecture — may still be drawn in a reply when a
table would lose what the reader needs. `remote_viewer` changes nothing here;
it is a Mermaid signal only. A wrong Mermaid choice shows the user raw source;
a markdown table still reads everywhere.
