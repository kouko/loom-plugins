# Confirmation display boundary — native Claude Code probe

## Outcome

The tested Stop hook cannot ensure that an earlier assistant message is absent
from Claude Code's streamed JSON output. MessageDisplay replaces the completed
assistant and result messages in the tested non-interactive mode, but the raw
partial-message stream already exposed the original. When the display hook
failed, the completed result contained the original. Neither mechanism alone
establishes a cross-host, pre-display correctness guarantee.

This is a host-mechanism experiment, not a test of an integrated Loom change,
semantic correctness, interactive terminal rendering, installed plugin state,
other consumers, or other hosts.

## Method

Three synthetic, tools-disabled native `claude -p` calls used Claude Code
`2.1.317`, explicit `claude-sonnet-5-5`, requested medium effort, and
`stream-json` with partial messages and hook events. Returned modelUsage matched
the requested model on all three; estimated total CLI cost was USD 0.0142199.
No plugin resources or project files were loaded. A hook sandbox denied the
synthetic private sentinel, network bind, and outside-directory writes. The
initial network check could not launch the user-specific Python interpreter
because that path was denied; the same check with `/usr/bin/python3` returned
77 as expected. All fixture values are synthetic markers.

1. A Stop hook blocked the first stop and instructed the actor to emit a new
   marker. Raw stream order was: partial original marker, complete original
   assistant message, Stop hook start/response, partial replacement marker,
   complete replacement assistant message, final replacement result. The
   hook input received the original marker; a second Stop saw the replacement.
2. A MessageDisplay hook replaced the assistant's text with a fixed marker.
   Raw partial events carried the original before the hook start; the later
   complete assistant message and final result carried the replacement. The
   hook input contained the complete original (`index: 0`, `final: true`).
3. A MessageDisplay hook deliberately exited 1. The hook response recorded
   an error, and the final result contained the original marker.

Events and exact test scripts are in `display-boundary-pilot-data.json`; the
records retain event order, model receipts and marker contents, while omitting
session IDs. No screen recording or human observer was used. In particular,
streaming an event to a client does not establish how every client renders it.

## Host and source boundaries

The [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)
describes Stop as controlling continuation; MessageDisplay transforms screen
text, preserves the original transcript/model context, and falls back to the
original on error or timeout. Interactive display batches differ from `-p`,
and verbose output may expose the original. This matches the limited probe but
does not prove behavior on an interactive terminal or another release.

The current repository registers no Stop or MessageDisplay handler in
`loom-code/hooks/hooks.json` or `loom-code/hooks/hooks-codex.json`. Its
`loom-code/opencode/loader.js` handles context, prompt and before/after tool
hooks; it does not implement message interception. These are observations about
current Loom configuration, not claims about every host's capabilities. Codex,
OpenCode and Antigravity display interception were not tested here.

## Decision

Do not build a general correctness guarantee around these hooks. A controlled
host application could buffer a complete response before displaying it, but
such an application is not the current Loom skill and would add integration,
streaming and failure-mode costs; its feasibility and accuracy are untested.
Continue evaluating less invasive designs without presenting a renderer's
model-supplied readiness or exact-quote check as a semantic guarantee. A small
native test with the actual intake contract and fresh adversarial examples is
needed before claiming any improvement.
