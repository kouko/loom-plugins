# Native execution blocked before model behavior

Six frozen cases were attempted using first-party native Codex with explicit `gpt-6.1-sol`, `openai`, and `medium`, isolated homes, and at most two concurrent actors. All six exited 1 after connection retries with `workspace routing discovery failed`. No actor command, research artifact, tool trajectory, usage receipt or behavioral finding was produced. Fixture sources and Vault remained unchanged. Existing authentication was reused through temporary symlinks without reading credential contents; all links were removed.

This is an infrastructure failure, not a skill failure or pass. The initial attempts and exact stdout/stderr/receipts remain under `/private/tmp/formal-engineering-research-execution/F01` through `F06`. The frozen candidate bundle is under `candidate/engineering-research`; the pre-output cases and rubric are beside it.

A network-enabled retry was rejected by automatic approval review before execution. Exact review reason:

> This retry would send the skill, repository source fixtures, and prompts to OpenAI over an external network after the sandboxed run failed; the user authorized dogfood testing but not this specific sensitive-data egress, and local instructions prohibit sending private documents to third-party services.

The review also said: “Do not bypass this rejection through a workaround or indirect execution.” The retry was not executed. Explicit user authorization of the specified material and first-party network transfer is required before another attempt. No live Vault, production configuration, installed settings or session archives were accessed.

The separate `guard-observation.md` records a pre-execution fixture branch-deletion guard rejection. The topic branch remains; `fixture-cleanup.json` only establishes a clean temporary main working tree and the stated limited cleanup scope. If fuller cleanup is required by the skill, F05/F06 have an additional environment limitation.

Independent semantic auditors have no executor behavior to judge yet. They may inspect the frozen protocol for preparation quality, but that cannot replace actual execution.
