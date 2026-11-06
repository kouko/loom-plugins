# Codex minimal template — fifth comparison

The fifth prototype changes only the two existing restatement passages. It
adds a short abstract contrast between variable results and a supposedly fixed
method, plus wording to preserve supplied acceptance ordering and conditions.
No new file, read, model call, station or workflow was added. Relative to the
released baseline each file increases by 919 bytes; the exact patch is
`codex-minimal-round-5.patch`.

Six synthetic cases ran once per variant in fresh Codex CLI sessions, with
`gpt-6.1-sol`, `openai` and medium effort explicitly configured. The last
notice-delivery case was new; five cases were reused. Actors were explicitly
directed to load snapshot skill files, so this does not test installed-plugin
triggering. All twelve sessions exited successfully. Original tracked source
hashes remained unchanged; the small snapshot gained 42 Python bytecode files,
baseline gained none. The CLI did not emit an independent model/provider
receipt. `codex-minimal-round-5-data.json` retains the prompts, outputs,
drafts, usage and source hashes. This is an author-read small sample, not a
blind review or general error rate.

## Observations

- **Incomplete CSV:** baseline left why-now and displaced work open and asked
  for an answer. The small version explicitly identified displaced work as
  unknown, nonetheless recorded GO and `Open questions: none`, and asked for
  confirmation. This is a material failure in that observed sample despite
  the template saying not to confirm with missing facts. Previous small
  versions sometimes correctly paused, so do not infer a deterministic cause.
- **Stock PDF:** both variants included the specified field order and
  boundaries. The small version added project context and five sections.
- **Held invoice:** both preserved the ongoing hold. The small version used
  titled outer frames and did not impose the prior amount-method restriction
  in this observation. Alignment is not established by that observation.
- **New notice-delivery case:** both retained the user's explicit freedom to
  change how the summary is assembled. The small version supplied five sections.
  One new synthetic case does not establish generalization.
- **Natural default and simple setup:** inspect their recorded replies and
  drafts; this run does not establish behavior beyond the cases observed.

Reported input totals were 969,357 tokens baseline and 882,534 small,
including cached input. Output totals were 11,546 and 11,129; summed session
times were 333.279 and 319.054 seconds. Single synthetic samples cannot prove
cost, latency or causal differences, and no dollar price was inferred. This
version remains a prototype with a demonstrated missing-fact failure; neither
it nor its structural changes establish release readiness.
