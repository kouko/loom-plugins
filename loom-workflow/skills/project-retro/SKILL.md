---
name: project-retro
description: |
  Review one current or specified coding session for source-backed project
  development improvements. Use for a requested retrospective, including
  振り返り seeking improvements; not for current-progress recaps or recurring skill mining.
user-invocable: true
---

# Project Retro

Review one coding session at the user's request. This is read-only advice about
the adopting project's development environment, not a Loom station or quality gate.
Do not modify files, create issues, or send session content to an additional
service or agent as part of this skill. Use tools for inspection only;
do not run commands that mutate the project or session records.

## Select and read the session

1. Use the specified session when the user identifies one; otherwise use the
   current session. Do not combine sessions. If the target is ambiguous, ask
   which session they mean before drawing conclusions.
2. Inspect the available primary source: the visible conversation and tool
   events for the current session, or the identified transcript for a
   specified session. Include enough surrounding events to distinguish a
   genuine obstacle from an intentional choice or changed user priority.
   Exclude hidden reasoning and encrypted content. Reading a local transcript
   through a tool does not isolate it: tool output enters the model context
   and may be processed by the host service. For specified transcripts,
   redact secrets locally before any excerpt appears in tool output when
   feasible. If sensitive source cannot be safely inspected, ask for a
   redacted excerpt or state the limitation. The current conversation is
   already visible to the model; minimize quotations in the response.
3. Inspect relevant project instructions, documentation, check commands, and
   CI configuration before recommending a new pointer or automated check.
   Identify existing checks that are absent from the workflow, broken, or
   insufficient before proposing a duplicate.

If the session source is unavailable or incomplete, say which source and
portion are unavailable. Do not invent events, time costs, or outcomes; do
not present a recommendation that the available record cannot substantiate.
You may report a bounded observation from the visible portion, marked as
partial, or ask the user for the missing source.

## Analyze and report

Look for concrete friction in navigation, checks, instructions, tool use, and
information access. Project recommendations may target that repository's
project implementation workflow, documentation, check tools or CI, and
repository-level agent instructions. For each candidate, connect an observed
event to its effect, identify the concrete target in that project, and check
whether the proposed remedy already exists. Challenge an apparent problem when
the record also supports a simpler explanation. Omit generic advice without a
source. If the likely remedy changes a reusable skill, plugin, connector, or
other cross-project tool, keep it in Skill candidates instead.

Return two clearly separated sections:

### Project recommendations

Rank recommendations by likely impact on future project work, then by
confidence. For each, give: rank, concrete target, observed session event with
a traceable source pointer (message, tool call, log line, or file and line when
available), proposed outcome and suggested change, why it matters, uncertainty
or trade-off, and a verification idea for an independent implementation
workflow. A source pointer must let the user find the event without exposing
more private session text than needed. Say when no supported project
recommendation exists.

### Skill candidates

List possible reusable-tool problems separately, with the observed behavior,
same source pointer, suspected target surface, uncertainty, and a bounded next
source check. A single session can identify a candidate but cannot establish a
recurring skill defect or promote it into a skill or plugin change. For
cross-session installed-skill evidence, route a later, separately requested
investigation to `skill-retro`. Say when this section has no supported
candidate.

The result is a proposal list for user review and independent implementation
handoff only. Do not modify any project, agent-instruction, or skill file, plugin,
or connector or automatically apply the advice. A retrospective approval is a
decision about the proposal, not authorization for this skill to implement it.
