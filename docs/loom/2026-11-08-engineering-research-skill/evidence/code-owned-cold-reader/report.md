# Code-owned engineering-research cold-reader observation

One fresh native Codex invocation answered Probe C's fixed question set from only the seven runtime Markdown files embedded in its request. This is an advisory cold-read observation, not an activation measurement, executed-workflow result, independent acceptance verdict, or pass stamp.

## Reproducibility and observed boundary

- Source and request/config hashes were frozen before execution in `frozen-inputs.json`; the seven source hashes were unchanged after execution.
- Full request, frozen snapshot and executable harness remain only at `/private/tmp/code-owned-engineering-research-cold-reader-20261108/`. The source package excludes developer README material.
- Native CLI: `/Users/kouko/.local/bin/codex`, locally reported `codex-cli 0.167.0`.
- Requested pin: `gpt-6.1-sol`, built-in `openai`, reasoning effort `medium`. Isolated HOME and CODEX_HOME; explicitly allowlisted environment has no proxy or provider override variables. No model/provider override configuration was inherited. The CLI was invoked with `--ignore-user-config`, `--ignore-rules`, `--no-daemon`, read-only sandbox, disabled web search and disabled shell tool/apps.
- Authorization: user's exact quote `授權做聯網 dogfood testing`, recorded in `/private/tmp/loom-code-owned-dogfood-authorization.json` after disclosure. The single network call received escalation approval; no rejected call was retried or worked around.
- Authentication used a temporary symlink to existing auth infrastructure, without the harness reading or printing credential content. The symlink was removed in `finally` (receipt confirms).
- Exit 0 after 40.19 seconds; no timeout; no observable actor tool calls. Observable trajectory: thread start, turn start, one final agent message, turn completed. Reasoning events were excluded from retained logs.
- Reported usage: 18,113 input tokens (8,960 cached), `output_tokens: 1420` and `reasoning_output_tokens: 154`. Token usage is receipt data, not reasoning content.
- No returned event confirms the actual server-selected model or reasoning effort. Those remain requested values; `server_confirmed_model` and `server_confirmed_effort` are null in the receipt.
- Orchestrator model/effort: inherited and not independently observable; recorded as null.

## Reader-raised advisory findings

These are observations about what this one first-time reader understood, not independently established runtime defects. The full unedited response is `answer.md`.

| Observation | Actual response evidence | Package location | Suggested edit class |
|---|---|---|---|
| Cold-start integration vocabulary is underspecified | `answer.md:25` and `answer.md:32`: reader cannot determine how to discover an active change or its identifier | `SKILL.md:105-116`, `SKILL.md:134-138` | Clarify discovery or required owning-workflow context |
| Optional preservation relies on an unidentified finishing command and cleanup proof | `answer.md:26` and `answer.md:33`: reader calls this path partially executable | `references/preservation.md:3-16` | Identify the integration contract or the evidence to request when unavailable |
| Trigger boundary remains uncertain for capability checks and general review | `answer.md:8-11` gives exactly two uncertain request examples | `SKILL.md:4`, `SKILL.md:24-36`, evaluation-selection approach guidance | Decide whether examples would clarify the existing consequential-gap rule; do not infer measured misrouting |
| Other specialized terms lack explanations in this package | `answer.md:34-36`: frozen trial records, loader/host behavior, Vault and named CLI capability | `SKILL.md:100-104`, `references/preservation.md:34-42`, `references/preservation.md:62-66` | Consider brief definitions or a clearer explicit prerequisite |

The reader also found standalone bounded investigation executable and correctly recognized unavailable evidence, resources, authorization, CLI access and write access as explicit prerequisites/fallbacks (`answer.md:1`, `answer.md:19-26`). It did not treat every judgment word as a procedure-breaking defect (`answer.md:38`). It observed that the package does not formally define modes (`answer.md:15`).

## Limits

One cold read is one advisory sample. The actor received all seven files inline, so this does not test actual progressive loading, automatic activation, routing precision, tool execution, saved research correctness, preservation writes, installed-host behavior or downstream acceptance. The cold reader had no author intent, specification, prior findings, case oracles, historical sessions or Vault contents. Its access restrictions are supported by the explicit request/config and absence of observable tool calls; they are not a claim of OS-level denial of every readable path. No implementation files were changed and no commits were made by this task.
