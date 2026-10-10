---
name: external-review
description: |
  Execute one consented independent review through Codex, Claude Code, or Antigravity CLI with an explicit model and effort. The calling review skill keeps its own criteria and verdict checks.
version: 1.0.0
---

# External Review

Use this named skill when an owning Loom review skill needs an outside coding
agent. It provides one execution boundary. The owning skill supplies the task
packet, keeps its incumbent review, validates the returned review against its
own criteria, and reports a failed outside leg separately. A successful CLI
run alone is not an accepted review verdict.

`<loom-code>` is `${CLAUDE_PLUGIN_ROOT}` on Claude Code; on any other host it
is the directory two levels above this SKILL.md.

## Before discovery

Require a complete consent record for this executor and review root. The root is
the CLI's existing starting directory, **not a filesystem read boundary**. The CLI may
read files outside it through host tools or configuration; CLI startup,
plugins, and caches may write files even when model tools are restricted. The
record must identify `authorization_source`: either a quoted direct user request
with the final selected executor and an unambiguous active review target, or a
separate accepted selection. A direct user request authorizes one bounded
review without a second yes/no checkpoint. Show cost, vendor data transfer,
the actual filesystem limits, and local CLI execution before discovery, probe
or dispatch; for a
direct request, disclosure booleans mean these facts were shown, not that the
user separately acknowledged each one. Do not run network-backed model discovery,
a preflight, or a review until this record exists. If the selected executor or root changes,
obtain a new choice at the owning flow's authorization point. Never infer
consent from a prior fixed setting alone. Static local binary checks can occur
before authorization is recorded.

The JSON record passed to the script has this shape when the user authorizes
selection within one provider family and effort bound:

```json
{
  "approved": true,
  "authorization_source": {"kind": "direct-user-request", "quote": "<verbatim request>", "target": "<active review target>", "selected_executor": "codex"},
  "executor": "codex",
  "review_root": "/absolute/review/root",
  "selection_authorized": true,
  "family": "openai",
  "allowed_efforts": ["high"],
  "disclosures": {
    "cost": true,
    "vendor_egress": true,
    "local_execution": true,
    "filesystem_access_outside_root": true,
    "filesystem_write_not_guaranteed": true
  }
}
```

An exact user selection can instead record `"model": "<id>"` and
`"effort": "<level>"`. The bounded form lets the agent select a model from
current candidates without a second user question. Either form must be tied
to the same executor, review root, and disclosures. A change outside the authorized
bounds needs a new choice. A provider or review target that cannot be determined
from the direct request and active task also needs a choice before dispatch;
material scope beyond that task is not covered by the request. A suggestion
alone supplies no `authorization_source`.
An accepted suggestion or `ask` answer uses
`{"kind":"accepted-selection","selection":"<executor>","target":"<review target>"}`
as its source. For a direct request, the quoted text must name the final
selected executor, `selected_executor` must equal `executor`, and the target
must be nonempty. The owning review flow interprets the full request, including
refusals and corrections, and records its final authorized executor and target.
The script checks required source fields and their binding to the selected
executor, review root, disclosures, model, and effort; the quote remains audit
evidence. The owning flow withholds approval when the full request cancels,
replaces, or leaves the choice ambiguous. Route ambiguous requests to that
flow's choice point before setting `approved`.

Immediately before each owner call to the script for discovery or execution,
re-evaluate the latest user choice across all conversation turns available
then. Refresh the record for the current executor and target, or invalidate a
stale approved record when the user cancels, changes executor, or leaves the
choice ambiguous. A clear direct request still proceeds without a second
yes/no checkpoint after disclosure. One execution call runs discovery,
preflight, and review consecutively; a new user turn during that call can be
handled before the next outside call, and transmitted material cannot be
recalled.

For Antigravity, the model's provider family may be unknown until the
consented `agy models` result arrives. A bounded record may replace `family`
with `"allowed_families": ["anthropic", "google"]`, using only normalized
`anthropic`, `openai`, and `google` names. The owning review flow excludes the
incumbent's provider family when recording this set. After discovery, select
one listed model and pass its concrete family with `--family`. The executor
rejects an empty set, an unknown family, or a selected family outside the
recorded set before starting the probe.

After this consent, list candidates with:

```sh
python3 <loom-code>/scripts/external_review.py --list-candidates \
  --executor <codex|claude|agy> --scope <absolute-review-root> \
  --consent-record <path-to-record>
```

Select a candidate model and effort explicitly. Codex candidates come from
app-server `model/list`; Antigravity candidates from `agy models`; Claude Code
accepts its documented `opus`, `sonnet`, and `haiku` aliases or an explicit
Claude model ID. A list is a present observation, not a promise that the
account has entitlement or quota. The selected model's provider family must
match the requested independent vendor family. Antigravity is a multi-provider
CLI, so its CLI name does not establish vendor independence. Unknown model
families require another explicit choice; do not guess.

## Execute

Pass the owning skill's complete review packet on stdin. The skill may ask for
code, a plan, or a decision review; this boundary does not substitute a new
rubric or output schema.

```sh
python3 <loom-code>/scripts/external_review.py \
  --executor <codex|claude|agy> \
  --model <selected-model> --effort <selected-effort> \
  --family <openai|anthropic|google> \
  --scope <absolute-review-root> \
  --consent-record <path-to-record> < <review-packet-file>
```

The script first verifies the consent and explicit selection. It then performs
bounded discovery, one short preflight, and one bounded review with the same
model and effort. It emits one JSON result. `status: completed` means only
that the outside process ran and produced review text; the owning skill still
validates that text. Any other status is a failed outside leg. Never reuse a
preflight as the review, call a default model, downgrade effort, switch CLI, or
count a failed leg as a completed review.

The execution asks Codex for a read-only command sandbox, Claude Code for plan
mode with only `Read`, `Glob`, and `Grep` model tools, and Antigravity for plan
mode with its terminal sandbox. For each Antigravity probe and review, the
script also attaches the absolute review root with `--add-dir`; setting the
process working directory alone does not attach that workspace in print mode.
These flags constrain model actions but do not
prove host-wide read or write confinement. In particular, a review root is
only a working directory. The result reports this filesystem limit; the
owning skill must carry it into the user-facing report. Do not describe the
selected root as the only path the CLI could read.

Report the requested profile, candidate source, preflight outcome, observed
fields, and `evidence_level` alongside the owning skill's verdict. Codex's
CLI header on stderr must show the requested model and effort, yielding
`observed-model-and-effort`. Claude Code's JSON `modelUsage` must name a model
in the selected family, yielding `accepted-explicit-settings`; it does not
independently reveal effective effort. Antigravity must list the selected slug
and accept both flags, also yielding `accepted-explicit-settings`; it does not
independently reveal effective model or effort. A stale candidate, failed
flag, timeout, missing observation, or family mismatch remains a failure with
its concrete reason. A later capability change requires a fresh preflight and,
if the executor or review root changes, fresh consent.
