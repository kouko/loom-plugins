# Outside executor handoff

`loom-code:external-review` is the sole executor selection and execution
boundary. Invoke that named skill, not a file inside loom-code. This preserves
the workflow-to-code plugin dependency. The advisor supplies the owning review
packet on stdin, `review_root` (the CLI starting directory), selected executor
and complete consent record. A consent record may authorize selection within
one provider family and effort bound; Antigravity may use `allowed_families`
excluding the incumbent's family because `agy models` reveals the concrete
family only after consent. After discovery under that record, the named skill
chooses and runs with an explicit model and effort, plus the selected provider
family.
The named skill returns JSON evidence and
status; the owning review skill still judges whether its verdict is valid.

## Before the handoff

The advisor may make local, non-network observations to explain the available
choices. Such observations do not verify a model or effort. Never run model
discovery, a live probe, or a review before the single complete consent
checkpoint. Record the consent for cost, vendor and packet egress, `review_root`,
local setup and every leg assignment. The record must acknowledge
`filesystem_access_outside_root` and `filesystem_write_not_guaranteed`:
`review_root` only selects the CLI's working directory, not a read boundary;
startup, plugins and caches may write despite restrictions on model tools.
Exact model selection before
discovery is optional when bounded selection was approved. A different
executor or root, or a model/effort/family outside the recorded bounds,
invalidates consent and requires a new complete checkpoint. A model selected
within the recorded bounds does not require another question.

If no outside family is permitted after excluding the incumbent, stop. If
Antigravity discovery finds no candidate in `allowed_families`, report the
failed leg without substituting the current executor. If the user chooses a
same-family option, record that choice and do not describe its result as a
different-family opinion.

## Returned evidence and failures

Preserve the named skill's status and evidence level without strengthening
either. In particular, an accepted explicit setting is not an observed
effective setting. A rejected model or effort, unavailable candidate,
unidentified provider family, timeout, nonzero exit or observed mismatch is
a failed outside leg. Show the concrete reason and keep that leg separate
from the incumbent result. Do not retry with a default model or another
executor without renewing the complete checkpoint.
