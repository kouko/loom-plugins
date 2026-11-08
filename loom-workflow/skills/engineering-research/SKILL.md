---
name: engineering-research
description: |
  Resolve evidence gaps in Loom tasks or standalone engineering discussions when an unresolved premise could change a decision, including a small capability or version check. Routine lookups without a consequential gap remain ordinary work.
---

# Engineering research

Use evidence proportionate to the engineering question.

1. Check the premise. Identify the object being discussed, the question to
   answer, and the user's established outcome and constraints. Check these
   against the available conversation and artifacts. Resolve factual gaps
   yourself when possible. Ask only when an unresolved ambiguity would change
   the work's direction or requires a user preference or authorization;
   continue independent work while waiting. Do not invent a new goal.

2. Check whether the evidence answers this question. Before relying on a
   claim to recommend or take action, check its basis and relevance: the same
   behavior, project context, version, and conditions where they matter.
   Recheck relevance when the question changes. Similar terminology or an
   earlier research report alone does not establish equivalence.

3. Fill consequential gaps. Gather evidence when a factual uncertainty,
   contradiction, repeated failed attempt, or unverified assumption could
   change the decision. For current project behavior, inspect local code,
   configuration, tests, and history. For external support or practice, use
   applicable original documentation and relevant implementations or reports;
   do not infer industry consensus from a few examples. When feasibility
   depends on the environment or execution, use the smallest permitted
   experiment that answers the question. Reading, external research, and
   measurement are alternatives or complements, not mandatory steps in order.
   Use an existing research tool when its scope fits. Routine lookups do not
   require this capability when no consequential gap exists. A low-cost check
   still warrants research when its unresolved premise could change the
   decision; once invoked, retain the bounded research record required below.

4. Stop when the decision has sufficient support. Do not broaden research
   merely because more sources may exist. If accessible evidence cannot
   settle a consequential uncertainty, report that limitation rather than
   search indefinitely or claim certainty. Distinguish observed behavior,
   source-supported claims, inference, and what remains untested. Report the
   evidence and material limitations concisely in the research record. Its
   length follows the question; a short investigation can have a short record.

5. Verify this research's claims and records. Before declaring a finding,
   experiment or research document complete, inspect the actual evidence and
   read back the saved record. A successful exit, file existence or completion
   message alone does not establish the claimed finding. Reuse adequate
   verification; report any remaining uncertainty. Ordinary implementation and
   delivery verification remains the owning task's responsibility.

## Research method and source selection

Initial conversation and artifact orientation may establish the question,
current revision and existing evidence. Before collecting new substantive
evidence or executing a new experiment, read
[research methods](references/research-methods.md) and
[source policy](references/source-policy.md). Reused evidence still requires
applicability checks. Choose the smallest method or combination that resolves
the consequential gap; do not run every method or visit a fixed number of sites.
Record the chosen method and why it fits.

For GitHub/GitLab repository research about behavior or implementation, inspect
the relevant source code and connected execution path. README, documentation,
search snippets, stars and discussion status alone are not implementation
verification. Follow the repository-specific requirements in the source policy.

## Choosing an evaluation approach

For an assessment of alternatives, design/change quality, experimental effects
or operational risks, read [evaluation selection](references/evaluation-selection.md).
Choose by the pending decision and missing evidence, not by a preferred framework
name. A factual question can be settled directly without a named framework.
Record why the selected approach fits; combine approaches only for distinct,
consequential gaps. Preserve the existing proportionate-method and source rules.

## Optional structural relationships

When branches, dependencies, interactions, state changes or competing causal
hypotheses are easier to inspect as relationships, read
[structured relationships](references/structured-relations.md). Add a compact
Mermaid diagram only when it improves the research record. Simple facts and
comparisons can remain prose or a table. Keep the findings and evidence readable
without rendering; a diagram does not establish causality or replace sources.

## Retained research records

Every invocation produces or updates a Markdown research record, including an
inconclusive investigation or a finding that existing evidence is sufficient.
Use [the research template](templates/research.md). Keep metadata flat and the
body readable in Obsidian, GitHub and plain Markdown editors. No Obsidian plugin
is required. Use standard relative Markdown links to project artifacts and
ordinary URLs for external sources; paths must resolve from the record.

- **Split by question, not invocation.** Create one file for each independently
  answerable question. Split unrelated questions from the same invocation.
  Reopen the existing file for a continuation of the same question under the
  same conditions, adding evidence and updating the conclusion and date.
- **Preserve earlier decisions.** If materially different versions, environments
  or assumptions make the earlier answer inapplicable, retain that record and
  create a separately scoped revalidation, linking the two. Do not silently
  replace the evidence on which an earlier decision depended. Respect frozen
  trial records and explicit no-edit boundaries.
- **Use the active change.** Save under
  `docs/loom/<change-id>/research/<sequence>-<topic>.md`. Read existing records
  before allocating the next unused sequence; a matching filename alone is not
  proof that two records answer the same question. Use descriptive lowercase
  hyphenated filenames. Do not overwrite a different question on a collision.
- **Without an active change**, save under
  `docs/loom/research/<YYYY-MM-DD>-<topic>.md`, adding a distinguishing suffix
  on a collision. Do not invent a goal or intent just to obtain a directory.
  Later changes can reference that record without copying it.
- **Metadata:** require `title`, `type: loom-research`, `status`, `created`,
  `updated` and a `tags` list containing `loom/research`. Add `change` only when
  an actual active change is known. Dates use YYYY-MM-DD. Preserve `created`
  when updating. Keep property names and value types consistent.
- `status` is `in-progress`, `concluded` or `superseded`; it describes the work,
  not evidence quality or user acceptance. `concluded` can still mean that a
  consequential question cannot currently be settled. Explain that in the body.
- Retain the question and applicable conditions, findings, source or experiment
  evidence, decision impact, and limitations/open questions. Evidence includes
  relevant versions and conditions, source paths/URLs, and commands plus actual
  results where measured. Do not fabricate missing observations. Save a useful
  summary and links, not an entire browsing transcript.
- Specs and plans reference relevant research records; do not duplicate their
  evidence. A separate index is optional and contains links rather than a
  second copy of the conclusions.
- An explicit no-write request or unavailable write access takes precedence:
  provide an unsaved draft and identify the missing saved artifact. Do not claim
  it was retained, override that boundary, or treat a schema check as proof of
  research quality.

## Return to the owning task

This is an on-demand capability, not another Loom station. Identify the pending decision and the factual gap before doing work. Preserve the active station and confirmed authorization. If evidence is already sufficient, reuse it in the retained record and return without additional investigation. Otherwise inspect relevant local artifacts, consult applicable original sources, or run the smallest authorized measurement. Use an existing research tool when its scope fits.

Return the decision, the actual saved record path, and remaining material uncertainty in the conversation; resume the owning task within its authorization. Verify the record content before calling it saved or complete. Do not start a new goal, install tools, publish, or advance a human decision point on the user's behalf.

## Optional long-term preservation

Only when finishing a merged change with relevant research, or explicitly asked
to preserve research from an earlier merged change, read
[preservation guidance](references/preservation.md). This optional proposal
does not block the owning task or authorize a Vault write. Ordinary research
does not load this reference.
