# Carry details agreed before the intent into the spec, and use tables and diagrams where they help
originator: kouko
kind: engineering
needs-design: no — skill and reference guidance for capture-intent, write-spec and write-plan; no surface a user reads or types into changes
status: confirmed 2026-09-15
publication: automatic — authorized 2026-09-15 by kouko

## Problem
kouko often discusses a change's detailed flow and reactions with the agent
before the intent is written. The intent deliberately leaves those details out
(behaviour is deferred to the spec, method to the plan), but nothing requires
the agreed details to reach the spec: the capture-intent hand-off carries only
unresolved questions, and a change marked `needs-design: no` gets no spec at
all. Reviewers and the blind run check the intent, spec and plan, so a detail
that never reached a file is checked by nobody, and it survives only in the
conversation, which compaction can drop. kouko cannot tell whether the
implementation will follow what was agreed.

When details do reach the spec, they are hard to take in: the `## UI flows`
section and the behaviour read-back at decision point ② are both long runs of
one-line items (`loom-design/skills/write-spec/references/ui-flows.md`
prescribes that shape), so a misunderstanding in a multi-case flow can pass a
confirmation the user could not really read.

## Proposed outcome
Every detail agreed before the intent is recorded in the spec that follows,
and intents, specs and both confirmations use tables and diagrams wherever
they let the reader see cases side by side or trace paths.

## Acceptance
1. When details of flow or reaction were agreed in the conversation before the intent, the change's spec records each of them, including for a change that would otherwise have no spec.
2. A spec written after this change records a flow with several parallel cases as a table and a flow with branching states or paths as a diagram in its UI flows section, while a short flow may stay as plain lines.
3. At behaviour confirmation in the conversation, the agent presents such a flow as a table or a text diagram before the per-case sentences, and never as a diagram form the conversation shows only as raw code.
4. The same guidance applies whether write-spec or write-plan writes the spec and runs the confirmation.
5. For an engineering change, the intent confirmation message shows the details that will be carried into the spec as a table, confirmed by the same answer as the intent; when nothing was agreed beforehand, no table appears.
6. An intent written after this change may use tables and diagrams in its sections when they make the content easier to read, while its Acceptance stays a numbered list, it still holds no detailed flows, and the intent checker still accepts it.
7. The repository's package tests and mechanism checks pass.

## Constraints
- The intent's sections and Acceptance numbering do not change; detailed flows stay out of the intent file.
- user-decided (kouko, 2026-09-15): engineering changes show the carried details at intent confirmation rather than only recording them in the spec.
- user-decided (kouko, 2026-09-15): carried details get no new final-acceptance check; a product change's blind run already walks the spec's UI flows, and an engineering change's details are checked by the spec reviewers only.
- Only details kouko stated or explicitly agreed to in the conversation are carried; the agent adds no detail of its own to the carried list, and agent proposals kouko did not agree to are not carried.
- No new mechanism beyond carrying the details into the spec; the existing spec review and decision point ② are what check them.
- Decision point ② still never shows design rationale.
- A terminal conversation does not render Mermaid; diagrams shown in chat are text diagrams, while Mermaid is allowed in files.

## Out of scope
- Rewriting specs that already exist.
- Adding or removing intent sections, or changing the blind-run report.
- Generating a short intent from the user's words when they ask to skip it (dropped: no current pain).

## Open questions
- none
