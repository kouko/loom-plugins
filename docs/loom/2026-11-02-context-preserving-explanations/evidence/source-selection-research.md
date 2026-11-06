# Alternatives: evidence selection and confirmation control

## Outcome

An extractive, program-rendered prototype can restrict displayed source excerpts
to exact substrings, but this pilot does not establish correct confirmation
readiness or a usable user-facing workflow. Do not integrate or release it.
Its CSV actor marked the request ready without the required displaced-work
answer. The pilot supplied only a generic value-case instruction, not the full
intake contract, so this cannot establish how the approach performs with full
requirements. The result does demonstrate that a renderer trusting a model's
`ready` flag cannot enforce the real prerequisite.

## Evidence and alternatives

- Fine-grained factuality research assesses individual assertions against a
  source, rather than assuming a whole response is sound
  ([FActScore](https://aclanthology.org/2023.emnlp-main.741/)). Citation or
  quotation alone does not establish that a source supports the surrounding
  claim ([ALCE](https://aclanthology.org/2023.emnlp-main.398/)).
- Separating model-generated fields from program-controlled conversation flow
  is used in Google's published
  [dialogue framework example](https://github.com/GoogleCloudPlatform/cxas-scrapi/blob/main/examples/bella_notte/slot_filling_dag_framework.md).
  That example is not a Loom evaluation; extracting the wrong field or state
  still creates a wrong decision. Only explicit state transitions based on
  authoritative inputs could be enforced by code, not semantic truth itself.
- A separate reviewer is not a new solution here: `evidence-check-pilot.md`
  records that the previous checker and reviser both missed a narrowed CSV
  source being broadened. The checker lacked the full workflow contract, so the
  observation does not disprove all possible reviewers.
- A broader or more expensive reasoning process is not a demonstrated fix:
  [summarization research](https://aclanthology.org/2026.findings-acl.859/)
  reports that increasing reasoning does not consistently improve factual
  consistency. That study does not directly test this Loom use case.

Loom currently checks that `Open questions` is `- none` when a new plan is
checked, but this is a downstream plan check in
`loom-code/scripts/loom_checker/rule_checks/intake.py`, not a pre-display
guarantee. The current `loom-code/hooks/hooks.json` does not register a Stop
hook. Claude Code documents a
[Stop event](https://code.claude.com/docs/en/hooks), but no test here establishes
that it can suppress text already streamed to a user, or that all supported
hosts offer equivalent behavior.

## Small extractive pilot

Four previously used synthetic cases ran once, in a tools-disabled empty
environment, with explicit native `claude-sonnet-5-5` and requested medium
effort. The model selected verbatim source spans and a proposed ready flag; a
Python check verified each span occurs in the named input, and a Python renderer
chose either a missing-information block or a confirmation placeholder from
that flag. The supplied evidence was synthetic request and fixture text; the
actor was not running the Loom skill or its actual hooks. Returned modelUsage
matched the requested model in all four calls; CLI-estimated total cost was
USD 0.0550077. The actual prompt, sources, selections and rendered text are
retained in `source-selection-pilot-data.json`; the byte-preserved historical
pilot sources are `historical-source-selection-run.py.txt` and
`historical-source-selection-render.py.txt`. They were originally recorded
under `probes/` but are not reusable adversarial tests.

| Case | Direct observation | Limit |
|---|---|---|
| Unknown date | Selected exact user and document snippets; marked not ready. | User's report of a wrong date and the inspected placeholder remain different evidence, not automatically reconciled. |
| Incomplete CSV | Every selected snippet occurred in its source, including the CSV qualifier; marked ready despite no displaced-work answer. | Prompt omitted the full required-fields contract. A program that trusts this flag would take the wrong branch. |
| Setup correction | Selected supplied correct command and marked ready. | Literal source excerpts mix English and Chinese and duplicate content. |
| Currency, explicit hold | Selected the stated currency problem and preserved the hold flag. | The output only quotes the request for a graph; it does not generate the graph. |

The renderer is deliberately a proof of concept: its ready branch contains a
publication-disclosure placeholder, not the actual authorization contract;
it emits source excerpts, not a complete fluent explanation or intent file.
It therefore is not a functional replacement. It also cannot prove the selected
excerpts are complete, accurately classified, current, mutually consistent,
or representative; a substring check establishes only literal occurrence.

## Candidate for a next experiment

Compare the existing workflow with a prototype that (1) captures narrowly
scoped evidence together with its origin and reported-versus-observed status;
(2) computes only explicitly represented, contract-defined missing requirements
in program code, refusing readiness if a required field is absent or unknown;
and (3) lets a writer explain those inputs while preserving the five sections,
applicable authorization, and requested diagram. Test selection, rendered reply,
saved intent and actual host execution separately. Include conflicting source
evidence, missing value case, both publication modes, omitted material details,
explicit changed outcomes, and novel holdouts, plus reading-comprehension and
latency/cost checks. The model's mapping of evidence into fields remains a
failure surface and must be measured, not treated as code-verified truth.

Before spending on a full integration, first verify whether the supported host
can actually make this path authoritative for user-visible confirmation. If
the agent can bypass the renderer, if output is already visible before a hook,
or if another host lacks an equivalent interception point, a programmatic
pre-display guarantee cannot be claimed. These are open engineering questions,
not demonstrated host defects. Stop or simplify if this cannot be achieved
without disproportionate complexity; do not add a reviewer or schema merely to
rename an unverified model judgment as a gate.
