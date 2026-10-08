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

Require a recorded user opt-in for this executor and review root. The root is
the CLI's starting directory, **not a filesystem read boundary**. The CLI may
read files outside it through host tools or configuration; CLI startup,
plugins, and caches may write files even when model tools are restricted. The
record must state that the user accepted those limits, cost, vendor data
transfer, and local CLI execution. Do not run network-backed model discovery,
a preflight, or a review until this record exists. If the selected executor or root changes,
obtain a new record at the owning flow's existing user checkpoint. Never infer
consent from a prior fixed setting alone. Static local binary checks can occur
before that checkpoint.

The JSON record passed to the script has this shape when the user authorizes
selection within one provider family and effort bound:

```json
{
  "approved": true,
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
bounds needs the owning flow's existing checkpoint again.

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
mode with its terminal sandbox. These flags constrain model actions but do not
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
