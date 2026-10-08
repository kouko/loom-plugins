# Report contract — the skeleton and the rejection keys

Referenced from `SKILL.md`. The binding honesty rules live in `SKILL.md`; this
file carries the field order, the rejection keys, and the worked wording.

## The report skeleton

Write the fields in this order. Divergence comes before anything summarising.

1. `divergence_points` — one entry per place the sides disagree. Each entry
   carries `kind` (`factual-error` or `judgement-call`), `confidence`,
   `proposed_change`, `corroborated_by`, and `resolution` (starts `open`).
2. `findings` — the same three fields for anything that is not a divergence.
3. `verdict` — one of `challenger-preferred`, `incumbent-preferred`,
   `inconclusive`.
4. `leg_count`, `early_stopped`, `degraded_legs` — the run as it actually ran.
5. `executor_provenance` — for each outside leg, identify the CLI, requested
   model and effort, selected model provider family, candidate source, bounded
   probe result, observed model and effort where present, and `evidence_level`.
   State whether settings were merely accepted by the CLI or independently
   observed. Codex can report observed model and effort; Claude Code reports
   an observed model family with accepted explicit settings; Antigravity CLI
   reports accepted explicit settings and a listed model slug. Do not label
   the latter two as independently observed effort, or `agy` as an observed
   effective model. An unknown or mismatched family, failed probe, or rejected
   explicit setting makes the leg failed rather than a completed verdict.
6. `actual_cost` — a figure in the stated unit, or `unknown` with its reason.
7. `known_weaknesses` — the standing note below.
8. `coverage_disclaimer` — what was consulted, in the words below.

## The six rejection keys

Record exactly one key per rejected leg output:

- `empty-output` — nothing came back.
- `refusal` — the executor declined the task.
- `missing-field` — one of the shared card's fields is absent.
- `restates-input` — the output reproduces its input and adds nothing.
- `unbacked-claim` — a claim cites a path or fact that does not check out;
  list each such claim on its own line.
- `no-reasoning-trace` — conclusions arrive with no reasoning behind them.

## Worked wording

`known_weaknesses`:

> Two legs that read the same material and agree have measured the material,
> not the world. Anonymisation and order counterbalancing remove relative
> preference differences between reviewers; neither can detect a blind spot
> shared by all reviewers.

`coverage_disclaimer`:

> The dispatch packet was assembled from the listed `evidence paths` at the
> pinned revision. That describes the prepared material, not every file the
> outside CLI may have read. The CLI can access files beyond `review_root`;
> this consultation cannot attest which other files the CLI accessed.

A degraded run's disclosure, in the report body rather than a footnote:

> This report rests on 2 of the 3 planned legs. The `blind judge` leg is listed
> in `degraded_legs` with its failure attribution.

An untrusted-source marking, carried on the passage itself:

> [external executor `<name>` — untrusted content] …the returned text…
