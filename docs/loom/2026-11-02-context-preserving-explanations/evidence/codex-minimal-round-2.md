# Codex minimal template — second comparison

The second prototype changes only the same two existing restatement passages
as round 1, adding 109 bytes to each first prototype file. It explicitly limits
the five sections to ready confirmations and asks for aligned frame edges;
it does not add a required read, tool, model call, station or workflow. The
exact patch against released `41211a0b` is `codex-minimal-round-2.patch`.

Five previously used synthetic cases were each run once against released and
second-prototype snapshots in Codex CLI, explicitly configured for
`gpt-6.1-sol`, `openai` and medium effort. The model was told to load the
specified skill path; this is not an installed-plugin or triggering test.
The corrected harness asks actors to stop before implementation/publication
without granting or denying future publication. The CLI did not provide a
separate model/provider receipt. The prompts, results, drafts, usage, source
manifests and integrity details are in `codex-minimal-round-2-data.json`.

All ten model sessions returned successfully, but the harness itself exited
nonzero: the small snapshot gained 42 Python bytecode files despite the
environment flag, while baseline gained none. No original tracked file was
missing or changed. Do not call the snapshot read-only or claim a full
integrity pass. This run is a non-blind, one-sample-per-case comparison of
reused synthetic cases; it cannot establish general reliability.

- **Incomplete CSV:** both actors asked for displaced work rather than
  requesting ready confirmation. The small version did not present the five
  sections. Both treated the stated monthly burden as the urgency context;
  neither explicitly asked the separately missing why-now question. The
  baseline draft had already recorded GO while the small draft deferred it.
- **Stock PDF:** the small version supplied five sections with the work's
  context and boundaries; baseline gave a shorter account. Neither reply
  repeated the previous invented table rows. The small reply added an
  unrequested example of a report-management system to exclude.
- **Explicit hold and requested graph:** both preserved the hold. Baseline
  provided labeled but unframed lines; small provided two labeled frames,
  but raw ASCII line widths alternated between 52 and 53 columns. The added
  alignment instruction therefore did not suffice in this sample.
- **Natural default:** both described later push and reviewable PR after
  checks, opt-out before publication and separate merge. No actual push or PR
  occurred.
- **Simple setup correction:** both wrote an open draft before confirmation.
  The small version gave five short headings and retained the relevant command
  and boundaries; baseline was more compact.

Across these five pairs the reported total input token counts were 867,789
for baseline and 819,887 for the small version; output counts were 9,899 and
8,617. Cached input is included in input. Elapsed session-time totals were
278.651 and 247.828 seconds. These single synthetic observations are not a
reliable cost or latency estimate, and do not establish that the added words
reduce cost. Actual prices were not inferred. The known alignment failure and
source-bytecode side effect remain unresolved; continue with a small example
only if it does not add a runtime step or large ongoing cost.
