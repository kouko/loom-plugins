---
title: "Does Codex sandbox networking prevent Loom from using gh?"
type: loom-research
status: concluded
created: 2026-11-15
updated: 2026-11-15
tags:
  - loom/research
---

# Does Codex sandbox networking prevent Loom from using gh?

## Question and scope

Determine whether restricted command networking can explain Loom's GitHub failures, and whether the current publication path distinguishes that condition. Research only: no publication, merge, credential changes or production edits. Sufficient evidence: a matched read-only query across execution contexts plus inspection of the subprocess and failure-guidance paths.

## Method and rationale

Hypothesis-driven diagnosis and bounded source inspection. Hold the command, working directory and existing gh setup constant; vary the execution tool's sandbox permission. This isolates the execution-context difference sufficiently to test connectivity, without running publication. Source inspected at f82b358fabe781dfa929fa6a9a43f2ece0346e97. The host's supplied policy explicitly says network access is restricted.

## Findings

- Observed: `gh api meta --jq .verifiable_password_authentication` in the default sandbox exited 1 with `error connecting to api.github.com` and `check your internet connection or https://githubstatus.com`.
- Observed: the identical command with `sandbox_permissions: require_escalated` exited 0 and printed `false`. This is an API field value, not an authentication failure. No credentials were printed or changed.
- Supported: this environment's default execution restrictions can prevent gh connectivity even when the host execution succeeds. The experiment does not isolate DNS from other sandbox restrictions, establish authenticated repository permissions, or reproduce a historical publication command.
- Source-supported: Loom calls subprocesses directly; it does not obtain different host execution permissions from inside Python. Publication children inherit the enclosing execution restrictions. Its failure handling preserves command diagnostics but does not classify sandbox networking failures or explicitly direct the calling agent to a permitted host-network retry.
- Inference: generic prerequisites/authentication guidance and the instruction to stop when automatic repair is unjustified can encourage premature stopping. This is a guidance gap, not proof that Loom itself disables networking or that gh is broken.

## Evidence

- [Publication subprocess](../../../loom-code/scripts/loom_checker/command_handlers/publish.py#L71): `subprocess.run`, captured output and 30-second timeout.
- [Publication failure guidance](../../../loom-code/scripts/loom_checker/command_handlers/publish.py#L93): prerequisite recovery and preserving the existing publication route.
- [Check classification](../../../loom-code/scripts/loom_checker/command_handlers/publish.py#L214): unavailable observations receive generic authentication/permissions/response advice.
- [Failure propagation](../../../loom-code/scripts/loom_checker/command_handlers/publish.py#L672): nonzero child status becomes a publication failure with stderr/stdout detail.
- [Ship guidance](../../../loom-code/skills/ship/SKILL.md#L236): use the designated publication command; follow observed remedies, otherwise report missing conditions and stop. A host-permission retry of that same command need not change the publication route.
- Experiment: the two read-only command executions above ran sequentially in the current worktree. Default exit 1; escalated exit 0. No publisher, push, PR creation or merge was run.

## Decision impact

Recommend a bounded guidance change in a separate authorized implementation: distinguish execution-environment connectivity from authentication and GitHub service failures; where host policy permits, retry the existing authorized Loom command with appropriate execution permissions. Do not replace Loom's publisher with raw git/gh publication commands, automatically grant privileges, or treat a platform denial as retry permission.

Keeping current guidance has no implementation cost but retains the demonstrated diagnostic ambiguity. A narrow host-aware guidance update preserves sandbox defaults and the existing publisher. Globally enabling network access is broader than needed and was not tested or justified here. A new network-probing subsystem is unnecessary for the demonstrated gap; deeper error classification can be deferred unless bounded guidance proves insufficient.

## Limitations and open questions

The quoted historical explanation was not independently reconstructed from its original tool outputs. Exact DNS causality, authenticated API access, Git transport, full publication and behavior on other hosts remain unverified. No production tests were needed because production code was unchanged. The read-only probe establishes connectivity only, not delivery readiness. No external documentation claim is necessary for the conclusion; the attempted official security page lookup did not yield usable network-policy content.
