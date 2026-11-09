---
title: "Host termination checks without an independent workflow"
type: loom-research
status: concluded
created: 2026-11-09
updated: 2026-11-09
tags:
  - loom/research
change: 2026-11-09-git-delivery-enforcement
---

# Question and scope

Can existing host adapters invoke a delivery check when the agent ends a turn? Local source revision 24b5bc0f; documents fetched 2026-11-09. No production hooks installed or live sessions created by this investigation.

## Method and rationale

Inspect existing adapters and official hook contracts. This answers whether an adapter can use a documented continuation event; documentation does not establish that a particular local host trusted or ran a hook. No general evaluation framework is needed for this bounded capability question.

## Findings and evidence

- [Codex Hooks](https://learn.chatgpt.com/docs/hooks#stop): Stop accepts a JSON block decision/reason or exit 2 with feedback; stop_hook_active distinguishes a continuation. Plugin hooks require review/trust. Relevant installed CLI reports 0.167.0, but no new Stop hook was executed. An earlier guessed developers.openai.com/docs/hooks URL returned 404; the current guide was reached through the official plugin packaging link.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks#stop): Stop controls continuation and exposes stop_hook_active; it does not run for user interruption. A loop bound is required. This is protocol support, not live validation.
- [OpenCode Server SessionHooks](https://opencode.ai/docs/build/plugins/server#session-reference): the published interface lists prompt, context, compaction, generate, title, model/transport and retry hooks, without a termination decision event. Existing scripts/opencode/loader.js and its packaged copies implement context/prompt/pre/post-tool adapters only. No claim is made that an undocumented future/private event cannot exist.
- [Antigravity adapter](/Users/kouko/GitHub/loom-plugins/loom-code/hooks/agy_adapter.py): currently maps pre-invocation and pre-tool decisions. A termination decision is not verified; no inferred Stop mapping is added.

## Decision impact

Reuse one read-only delivery command on all hosts. Add documented synchronous Stop adapters only for Claude/Codex; disclose the absent verified stop boundary for OpenCode/Antigravity and retain the same Git-native protection and executable delivery checks. Never label a configuration-only unit test as a live host success. The user specifically reiterated OpenCode usability; independent acceptance must execute the packaged OpenCode entry/adapter and command, not only inspect prose.

## Limitations

No runtime observation of Claude/Codex termination, Antigravity termination, or OpenCode live plugin activation yet. Mocked adapter tests can prove mapping and emitted payloads, not installed-host permission/trust. Sources were read, command/version output observed, and this record read back after writing.
