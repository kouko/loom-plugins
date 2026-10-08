# Outside executor handoff

`loom-code:external-review` is the sole executor selection and execution
boundary. Invoke that named skill, not a file inside loom-code. This preserves
the workflow-to-code plugin dependency. The advisor supplies the owning review
packet on stdin, authorized scope, selected executor, model, effort, provider
family and complete consent record. The named skill returns JSON evidence and
status; the owning review skill still judges whether its verdict is valid.

## Before the handoff

The advisor may make local, non-network observations to explain the available
choices. Such observations do not verify a model or effort. Never run model
discovery, a live probe, or a review before the single complete consent
checkpoint. Record the consent for cost, vendor and packet egress, readable
scope, local setup and every leg assignment. A different executor, model,
family or scope invalidates it and requires a new complete checkpoint.

If no different-family candidate is known, say so and stop. Do not substitute
the current executor. If the user chooses a same-family option, record that
choice and do not describe its result as a different-family opinion.

## Returned evidence and failures

Preserve the named skill's status and evidence level without strengthening
either. In particular, an accepted explicit setting is not an observed
effective setting. A rejected model or effort, unavailable candidate,
unidentified provider family, timeout, nonzero exit or observed mismatch is
a failed outside leg. Show the concrete reason and keep that leg separate
from the incumbent result. Do not retry with a default model or another
executor without renewing the complete checkpoint.
