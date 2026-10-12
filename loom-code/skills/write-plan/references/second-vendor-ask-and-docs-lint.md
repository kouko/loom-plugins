# Second-vendor modes and `docs-lint:`

This file owns local CLI availability checks and the user-facing behavior for
`second-vendor: suggest`, `second-vendor: ask`, and a fixed provider choice.

## Availability probe

An independent cross-model review counts only when the **selected model's
provider family** differs from the current model's family. CLI names alone do
not establish this: `agy` can run models from several families. Map provider
families to the standing values `claude` (Anthropic), `codex` (OpenAI), and
`gemini` (Google); the plan's `selection-confirmed` value remains that family.
Detect a locally installed executor with `command -v <cli>` **and** a local
`<cli> --version` check that exits 0. The eligible executors are `claude`,
`codex`, and `agy`. In zsh `command -v` may print an alias or a
function body rather than a path; do not try to parse it. **Any non-empty
output plus a `<cli> --version` that exits 0 counts as present**, and
nothing else does. Never `which`: it reports shell aliases and stale
hashes. An installed CLI alone is not evidence of a different model family.

Before recorded consent, do not run network-backed model discovery, a model
probe, or an outside review. An installed `agy` with no approved model evidence
may be supplied as `{executor: "agy"}`. The resolver then emits
`availability-unverified`: describe a possible outside model family, explicitly
say that its family is unverified, and continue without waiting. This notice
does not select a vendor or authorize execution. If already authorized model
evidence is available, pass each candidate as `{executor, model, vendor}` in
`usable_vendors` after
checking the model identifier's family. `host_vendor` is the current **model**
family, including when the host is Antigravity CLI. Exclude same-family
candidates even when they use a different executable. If no model family is
known, do not guess from CLI branding. The policy
chooses canonical family order, then executor and model order. Its
`notice_executor`/`notice_model` or `effective_executor`/`effective_model`
fields identify the actual candidate. Do not install or authenticate CLIs.
When the defaults file has no
`second-vendor:` line, create it from the template if needed and record
`- second-vendor: suggest — default non-blocking visibility (<date>)`.

## `second-vendor: suggest`

Run the policy only after the plan's Risk lines exist. The policy owns risk
classification and vendor choice; the station supplies grounded risk items
as `{signal, anchors}`; do not reclassify risk or synthesize a reason
the returned JSON did not contain.

For `availability`, tell the user that the returned model candidate is
available. For `recommendation`, recommend it and render the returned
`recommendation_reasons` with their anchors. In both cases, continue without
waiting. There is no background listener, reminder, or persistent opt-in
state: only a reply received in the active task before Closing Review starts
can authorize this change's discovery or selection.
For `availability-unverified`, describe only the locally available executor
and the missing model-family evidence. At the existing consent checkpoint,
record the executor, readable scope, cost, vendor egress, local execution and
the allowed non-host model families. Reevaluate with `response: "accept"` and
no `response_vendor`: `discovery-authorized` permits only bounded model
discovery for `effective_executor` within `allowed_vendors`. It is not a
selected reviewer and must not produce a `selection-confirmed` plan line.
After consented discovery, identify a concrete model and verify its family;
reevaluate with that candidate and `response_vendor` under the same approval.
Only `selection-confirmed` then records the provider family in plan Risks, or
in intent Constraints when plan is skipped. Do
not ask a second time unless executor, readable scope, cost/egress disclosure,
or allowed model-family bounds change. If discovery finds no eligible model,
report the limitation and do not record a reviewer.

Render each initial suggest notice as a one-column Markdown table with exactly one
heading and one descriptive cell. Emit exactly two blank lines before and after
the table. Keep the source readable as raw Markdown:

```markdown


| <heading> |
|---|
| <description> |


```

Use the semantic heading `Independent review from a different model family`
for availability, `Independent review from a different model family
recommended` for recommendation, and `Outside model family unverified` for
availability-unverified. Render the heading and description in the
user's current conversation language. Put the vendor, grounded reasons when
present, opt-in cutoff, and `continue without waiting` statement together in
the single description cell. Name the executor, model and provider family when
the result supplies them. Add no second column or decorative row.

Only when the concrete-candidate reevaluation returns `selection-confirmed`, append
`user-decided — second-vendor selection-confirmed: <vendor>` to the plan's
`## Risks` section and commit that plan edit before Closing Review starts.
When plan is skipped, append the exact Markdown bullet
`- user-decided — second-vendor selection-confirmed: <vendor>` to the
confirmed intent's `## Constraints` instead. If a plan is created later, copy
the unbulleted line into its Risks before review. The checker reads plan Risks
first and intent Constraints when plan is absent or has no selection.
Here `<vendor>` is the selected model's provider family, not the executable;
the selected executor and model remain in the approved execution record.
The plan charter's `plan-maintained` edits-after rule authorizes this update
even when the initial plan commit already exists. Closing Review consumes
that line as the selected reviewer; it is a result record, not a fabricated
entry in `## Questions asked`.

A reply after Closing Review starts gets the policy's `next-change-only`
result; it does not mutate the current reviewer identity or the standing
default. No reply means no second vendor for this change.

## `second-vendor: ask`

`ask` is a standing choice that puts one cross-model review question to the
user on each change that lacks a qualifying direct user request. Skip the per-change question when a direct user request names an outside coding agent and an unambiguous active review target.
That request authorizes one review without a second question. Quote
that request, target and final `selected_executor` in JSON
`authorization_source` at dispatch; record the provider family in the separate
machine line above. Do not add a question to
`## Questions asked`. Show cost, vendor
egress, `review_root`, outside-root access and local-execution disclosure
before any network-backed discovery or execution, without asking for the same
review again. The execution record keeps the complete disclosure fields;
they state what was shown, not separate acknowledgments. If provider or target
is ambiguous, or material scope expands beyond the active task, ask for the
missing choice. A suggestion alone does not authorize review, so under `ask`
ask one per-change question as below. The answer governs only that change
and never rewrites the KICKOFF line. Check local executable availability
first, but defer model discovery and execution until authorization and
disclosure are recorded for the specific executor and review root.

With a runnable candidate or an unverified `agy`, prefer the current host's
native question tool.
Claude Code uses `AskUserQuestion` when it is available in the current agent;
the authoritative tool reference names that tool and owns its live schema
([Claude Code tools reference](https://code.claude.com/docs/en/tools-reference)).
Codex uses `request_user_input` only when the host exposes it in the active
mode; its live tool schema owns the valid question shape and availability, and
the official implementation enforces both mode and root-thread availability
([Codex handler](https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/request_user_input.rs)).
Ask whether to use the named candidate for an independent review by a different
model family; for unverified `agy`, say eligibility will be established after
consented discovery. Treat the two choice meanings as `decline this change` and
`use <tool>`, and render both choices in the user's current conversation
language. If the native interface requires one option to be recommended, mark
`decline this change` as recommended so extra quota use and repository-data
egress remain opt-in.

When a runnable executor exists but the native tool is unavailable, ask one
blocking plain-language Markdown question with the same two choices and no
fabricated recommendation. When no eligible or unverified executor is runnable,
state that no such review tool is currently available and continue without asking.

Add the question to the running list kept in step 3, so it lands in the
plan's `## Questions asked` section and the intent's decision record. That
answer names a CLI or declines cross-model review for this change.

## Fixed CLI

A fixed provider choice remains the standing reviewer choice. Check its
executor locally and follow the existing review failure behavior if it is not
usable; do not silently substitute another model or provider. `agy` is a valid
executor only when its selected model has the requested family and the shared
external-review execution contract verifies its explicit settings. A fixed
choice without recorded cost, vendor-egress, readable-scope and local-execution
consent must be confirmed at the existing intent decision point before any
network-backed discovery or review.

## `docs-lint: <command> | none — <why>`

`docs/loom/KICKOFF-DEFAULTS.md` may also carry this line — a repo declaring
its own prose linter, so the closing-review station's reviewer contract can
trust it instead of raising style findings itself (declared → no style findings;
`none` → style findings capped at `nit`).

This station never installs a docs linter and never asks about one on first
contact with a repo. When the line is absent, treat it as `none` — there is
no detection step for it the way there is for `package-tests:`.
